#!/usr/bin/env python3
"""Build the iLang runtime bundles from the canon files listed in runtime/sources.json.

The bundles are what a loader injects into a model's context. They are generated,
never edited by hand: every byte comes from a canon file at the commit named in the
bundle header. Standard library only.

    python runtime/build.py           # write ilang-latest.md, ilang-media-latest.md, manifest.json
    python runtime/build.py --check   # verify what is on disk, change nothing
"""
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True,
                          text=True).stdout.strip()


HEADING = re.compile(r"^(#+) ")


def trim(text, drops, path):
    """Leave out every section whose heading starts with one of drops, with everything under it.
    Headings inside code fences do not count. A rule that matches no heading stops the build, so a
    renamed heading in the canon cannot silently change what the bundle carries."""
    out, cut, level, fence, used = [], [], None, False, set()
    for line in text.split("\n"):
        is_fence = line.lstrip().startswith("```")
        m = None if (fence or is_fence) else HEADING.match(line)
        if m:
            depth = len(m.group(1))
            if level is not None and depth <= level:
                level = None
            hit = next((d for d in drops if line.startswith(d)), None) if level is None else None
            if hit:
                level = depth
                used.add(hit)
                cut.append(line[depth:].strip())
                continue
        if is_fence:
            fence = not fence
        if level is None:
            out.append(line)
    missing = [d for d in drops if d not in used]
    if missing:
        raise SystemExit("runtime: drop rules matched no heading in %s: %s" % (path, missing))
    return "\n".join(out), cut


def render(name, spec, commit, date):
    parts, index, left_out = [], [], []
    for n, src in enumerate(spec["sources"], 1):
        with open(os.path.join(ROOT, src["path"]), "rb") as f:
            raw = f.read()
        text = raw.decode("utf-8").replace("\r\n", "\n").rstrip("\n")
        if src.get("drop"):
            text, cut = trim(text, src["drop"], src["path"])
            left_out.append("- %s: %s" % (src["path"], "; ".join(cut)))
        index.append("%d. %s: %s. sha256:%s" % (n, src["path"], src["layer"], sha256(raw)))
        parts.append("===== BEGIN %s =====\n\n%s\n\n===== END %s =====" % (src["path"], text, src["path"]))
    note = []
    if left_out:
        note = ["",
                "Left out of this bundle, and kept in the full text at %s :" % spec["full_text"],
                *left_out,
                "",
                "When you are unsure how a rule applies, or you need one of the parts left out, read the full "
                "text before you answer. If you cannot open it, name the rule you are unsure about instead of "
                "guessing."]
    head = "\n".join([
        "# iLang runtime bundle (%s)" % name,
        "",
        spec["purpose"],
        "",
        "Generated from the iLang canon; not edited by hand.",
        "Source: https://github.com/ilang-ai/ilang-spec at commit %s (%s)." % (commit, date),
        "Contents, in order. Each document states its own status and scope:",
        "",
        *index,
        *note,
    ])
    return (head + "\n\n" + "\n\n".join(parts) + "\n").encode("utf-8")


def build():
    with open(os.path.join(HERE, "sources.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    commit = git("rev-parse", "HEAD")
    date = git("log", "-1", "--format=%cI", "HEAD")
    bundles, files = {}, {}
    for name, spec in cfg["bundles"].items():
        data = render(name, spec, commit, date)
        digest = sha256(data)
        files[spec["file"]] = data
        files[spec["file"].replace(".md", ".sha256")] = ("%s  %s\n" % (digest, spec["file"])).encode()
        bundles[name] = {"url": "%s/%s" % (cfg["raw_base"], spec["file"]), "sha256": digest,
                         "bytes": len(data), "sources": [s["path"] for s in spec["sources"]]}
    version = "%s-%s" % (date[:10].replace("-", "."), bundles["core"]["sha256"][:12])
    core_file = cfg["bundles"]["core"]["file"]
    manifest = {"brand": cfg["brand"], "runtime_schema": cfg["runtime_schema"], "channel": "latest",
                "version": version,
                # the single-bundle fields a minimal client reads (loader book 4); bundles has them all
                "bundle_url": bundles["core"]["url"],
                "sha256_url": "%s/%s" % (cfg["raw_base"], core_file.replace(".md", ".sha256")),
                "source_repo": "https://github.com/ilang-ai/ilang-spec",
                "source_commit": commit, "commit": commit, "updated_at": date, "bundles": bundles,
                "pinned": "%s/versions/%s/manifest.json" % (cfg["raw_base"], version)}
    files["manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    pinned = dict(manifest, channel="pinned")
    pinned["bundles"] = {n: dict(b, url="%s/versions/%s/%s" % (cfg["raw_base"], version,
                                                                   os.path.basename(b["url"])))
                         for n, b in bundles.items()}
    vdir = os.path.join("versions", version)
    pinned["bundle_url"] = pinned["bundles"]["core"]["url"]
    pinned["sha256_url"] = "%s/versions/%s/%s" % (cfg["raw_base"], version, core_file.replace(".md", ".sha256"))
    for name, spec in cfg["bundles"].items():
        files[os.path.join(vdir, spec["file"])] = files[spec["file"]]
        sha_file = spec["file"].replace(".md", ".sha256")
        files[os.path.join(vdir, sha_file)] = files[sha_file]
    files[os.path.join(vdir, "manifest.json")] = (json.dumps(pinned, indent=2) + "\n").encode()

    for rel, data in files.items():
        path = os.path.join(HERE, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
    print("iLang runtime %s  %s" % (version, "  ".join("%s %d bytes" % (n, b["bytes"]) for n, b in bundles.items())))
    return verify()


def verify():
    """What a loader relies on: every bundle is non-empty, matches the sha256 the
    manifest and the .sha256 file give, and names the commit it was built from."""
    problems = []
    with open(os.path.join(HERE, "manifest.json"), encoding="utf-8") as f:
        manifest = json.load(f)
    for pinned in (False, True):
        m = manifest
        if pinned:
            with open(os.path.join(HERE, "versions", manifest["version"], "manifest.json"),
                      encoding="utf-8") as f:
                m = json.load(f)
        for name, b in m["bundles"].items():
            rel = b["url"].split("/runtime/", 1)[1]
            with open(os.path.join(HERE, rel), "rb") as f:
                data = f.read()
            if len(data) < 1000:
                problems.append("too small: %s" % rel)
            if sha256(data) != b["sha256"] or len(data) != b["bytes"]:
                problems.append("hash or size mismatch: %s" % rel)
            if ("at commit %s" % m["source_commit"]).encode() not in data[:4000]:
                problems.append("source commit not recorded: %s" % rel)
            if not pinned:
                side = os.path.join(HERE, rel.replace(".md", ".sha256"))
                if open(side, encoding="utf-8").read().split()[0] != b["sha256"]:
                    problems.append(".sha256 file disagrees: %s" % rel)
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print("verified %s" % manifest["version"])
    return 0


if __name__ == "__main__":
    sys.exit(verify() if "--check" in sys.argv else build())
