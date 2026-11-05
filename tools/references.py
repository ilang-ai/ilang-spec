#!/usr/bin/env python3
"""The references register of SPEC-v5.0.md (Appendix H) is the single source of every work this release cites.

    python tools/references.py generate    rewrite .zenodo.json (references, related identifiers with relation
                                           "references") and the references: block of CITATION.cff from the register
    python tools/references.py check       exit 1 when the metadata cites a work the register does not list, or when
                                           the generated form differs from the files (run generate first)
    python tools/references.py list        print the register as plain citations

Reads only Appendix H: one ::FACT{key:REF-nnn|doi:…|relation:…|used_by:…} per work, with T: lines cite=, authors=,
type=…|year=…, and takes= or contrast=. Underscores in values stand for spaces. Structural relations of the deposit
(isDescribedBy, isSupplementTo, isSupplementedBy and the version links Zenodo adds) are not references and are kept
as they are. Standard library only.
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(ROOT, "SPEC-v5.0.md")
ZENODO = os.path.join(ROOT, ".zenodo.json")
CFF = os.path.join(ROOT, "CITATION.cff")

RESOURCE = {"article": "publication-article", "preprint": "publication-preprint", "conference-paper": "publication-conferencepaper",
            "book": "publication-book", "standard": "publication-other", "software": "software"}
CFF_TYPE = {"article": "article", "preprint": "article", "conference-paper": "conference-paper", "book": "book",
            "standard": "standard", "software": "software"}


def read(path):
    return io.open(path, encoding="utf-8", newline="").read()


def words(v):
    return v.replace("_", " ")


def register(text):
    """The entries of Appendix H, in order."""
    m = re.search(r"^## Appendix H — References Register.*?$(.*?)^(?:---|# Part|## Appendix)", text.replace("\r\n", "\n"), re.S | re.M)
    if not m:
        sys.exit("SPEC-v5.0.md has no Appendix H")
    body = m.group(1)
    entries = []
    for block in re.finditer(r"^::FACT\{(key:REF-\d+\|[^}]*)\}\n((?:  T:.*\n?)*)", body, re.M):
        fields = dict(f.split(":", 1) for f in block.group(1).split("|"))
        t = {}
        for line in block.group(2).splitlines():
            line = line.strip()[2:]
            for part in line.split("|"):
                k, _, v = part.partition("=")
                t[k] = v
        e = {"key": fields["key"], "relation": fields["relation"], "used_by": fields.get("used_by", ""),
             "doi": fields.get("doi"), "also_doi": fields.get("also_doi"), "url": fields.get("url"),
             "cite": words(t.get("cite", "")), "authors": [words(a) for a in t.get("authors", "").split(";") if a],
             "type": t.get("type", "article"), "year": t.get("year")}
        entries.append(e)
    if not entries:
        sys.exit("Appendix H holds no REF entries")
    return entries


def citation_text(e):
    link = ("https://doi.org/" + e["doi"]) if e["doi"] else e["url"]
    return "%s. %s" % (e["cite"], link)


def cff_person(name):
    if name == "et al.":
        return {"name": "et al."}
    if " " not in name or name.startswith("Basel"):
        return {"name": name}
    family, given = name.split(" ", 1)
    return {"family-names": family, "given-names": given}


def generated(entries):
    z = json.loads(read(ZENODO))
    kept = [r for r in z.get("related_identifiers", []) if r.get("relation") != "references"]
    refs = []
    for e in entries:
        for doi in (e["doi"], e["also_doi"]):
            if doi:
                refs.append({"identifier": doi, "relation": "references", "resource_type": RESOURCE[e["type"]], "scheme": "doi"})
        if not e["doi"] and e["url"]:
            refs.append({"identifier": e["url"], "relation": "references", "resource_type": RESOURCE[e["type"]], "scheme": "url"})
    z["related_identifiers"] = kept + refs
    z["references"] = [citation_text(e) for e in entries]
    zenodo_text = json.dumps(z, ensure_ascii=False, indent=2) + "\n"

    cff = read(CFF).replace("\r\n", "\n")
    cff = re.sub(r"\nreferences:\n(?:  .*\n|\n)*", "\n", cff).rstrip("\n") + "\n"
    lines = ["references:"]
    for e in entries:
        lines.append("  - type: %s" % CFF_TYPE[e["type"]])
        title = e["cite"].split("). ", 1)[1].split(". ", 1)[0] if "). " in e["cite"] else e["cite"]
        lines.append('    title: "%s"' % title.replace('"', "'"))
        lines.append("    authors:")
        for a in e["authors"]:
            p = cff_person(a)
            if "name" in p:
                lines.append('      - name: "%s"' % p["name"])
            else:
                lines.append('      - family-names: "%s"' % p["family-names"])
                lines.append('        given-names: "%s"' % p["given-names"])
        if e["year"]:
            lines.append("    year: %s" % e["year"])
        if e["doi"]:
            lines.append('    doi: "%s"' % e["doi"])
        elif e["url"]:
            lines.append('    url: "%s"' % e["url"])
        lines.append('    notes: "%s; %s"' % (e["relation"].replace("_", " "), words(e["used_by"]).replace(",", ", ")))
    cff_text = cff + "\n".join(lines) + "\n"
    return zenodo_text, cff_text


def write_lf(path, text):
    io.open(path, "w", encoding="utf-8", newline="\n").write(text)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    entries = register(read(SPEC))
    if cmd == "list":
        for e in entries:
            print("%s  [%s]  %s" % (e["key"], e["relation"], citation_text(e)))
        return
    zenodo_text, cff_text = generated(entries)
    if cmd == "generate":
        write_lf(ZENODO, zenodo_text)
        write_lf(CFF, cff_text)
        print("generated: %d works -> .zenodo.json and CITATION.cff" % len(entries))
        return
    if cmd == "check":
        known = {e["doi"] for e in entries if e["doi"]} | {e["also_doi"] for e in entries if e["also_doi"]} | {e["url"] for e in entries if e["url"]}
        bad = 0
        z = json.loads(read(ZENODO))
        for r in z.get("related_identifiers", []):
            if r.get("relation") == "references" and r.get("identifier") not in known:
                print("not in Appendix H: .zenodo.json related identifier %s" % r.get("identifier")); bad += 1
        for s in z.get("references", []):
            m = re.search(r"https://doi\.org/(\S+)|(https?://\S+)$", s)
            ident = (m.group(1) or m.group(2)) if m else None
            if ident not in known:
                print("not in Appendix H: .zenodo.json reference %r" % s[:60]); bad += 1
        for m in re.finditer(r'^    (?:doi|url): "([^"]+)"', read(CFF).replace("\r\n", "\n"), re.M):
            if m.group(1) not in known:
                print("not in Appendix H: CITATION.cff reference %s" % m.group(1)); bad += 1
        if read(ZENODO).replace("\r\n", "\n") != zenodo_text:
            print("stale: .zenodo.json differs from the register; run tools/references.py generate"); bad += 1
        if read(CFF).replace("\r\n", "\n") != cff_text:
            print("stale: CITATION.cff differs from the register; run tools/references.py generate"); bad += 1
        print("references check: %d works in the register, %d problem(s)" % (len(entries), bad))
        sys.exit(1 if bad else 0)
    sys.exit("unknown command " + cmd)


if __name__ == "__main__":
    main()
