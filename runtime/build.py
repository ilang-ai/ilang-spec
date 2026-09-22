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
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True,
                          text=True).stdout.strip()


def render(name, spec, commit, date):
    parts, index = [], []
    for n, src in enumerate(spec["sources"], 1):
        with open(os.path.join(ROOT, src["path"]), "rb") as f:
            raw = f.read()
        text = raw.decode("utf-8").replace("\r\n", "\n").rstrip("\n")
        index.append("%d. %s: %s. sha256:%s" % (n, src["path"], src["layer"], sha256(raw)))
        parts.append("===== BEGIN %s =====\n\n%s\n\n===== END %s =====" % (src["path"], text, src["path"]))
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
    manifest = {"brand": cfg["brand"], "runtime_schema": cfg["runtime_schema"], "channel": "latest",
                "version": version, "source_repo": "https://github.com/ilang-ai/ilang-spec",
                "source_commit": commit, "updated_at": date, "bundles": bundles,
                "pinned": "%s/versions/%s/manifest.json" % (cfg["raw_base"], version)}
    files["manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    pinned = dict(manifest, channel="pinned")
    pinned["bundles"] = {n: dict(b, url="%s/versions/%s/%s" % (cfg["raw_base"], version,
                                                                   os.path.basename(b["url"])))
                         for n, b in bundles.items()}
    vdir = os.path.join("versions", version)
    for name, spec in cfg["bundles"].items():
        files[os.path.join(vdir, spec["file"])] = files[spec["file"]]
    files[os.path.join(vdir, "manifest.json")] = (json.dumps(pinned, indent=2) + "\n").encode()

    for rel, data in files.items():
        path = os.path.join(HERE, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
    print("iLang runtime %s  core %d bytes  media %d bytes" % (
        version, bundles["core"]["bytes"], bundles["media"]["bytes"]))
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
