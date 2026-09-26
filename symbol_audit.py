#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iLang v5.0 symbol audit (seal condition S3).

Every symbol in the normative text of SPEC-v5.0-PRE.md must have a home. This script reads
the document, takes the formula lines of Part I (each ::MODULE), Part II §1 to §5 and Part IV
GENE_CORRECTION, extracts the Greek letters, single-letter variables, subscripted variables
and the assertion words (≈, lim, converge), and requires each of them to fall into one of:

  (a) defined in the same module (DEFINE head, "x = ...", "x ∈ ...", "WITH x", "FOR ALL x",
      "x > 0"), or in a module this module cites by name (Axiom N, MODULE::NAME);
  (b) bound to f_v5: a dimension abbreviation, a mode id, S or f_v5 as written in Part II §3;
  (c) registered in Appendix G, or on a line that cites a registry id (CONST-..., WEIGHT-...,
      TRUST-...);
  (d) in a block or on a line marked explanatory, non-normative, HYPOTHESIS or SUPERSEDED;
  (e) on the whitelist below, each entry with its reason.

Field lines (T:, A:, S:, V:, M:, R:), declaration heads (::X{...}), headings and the HISTORY
line are structured payloads, not formulas, and are not scanned. Appendices are not scanned;
Appendix G is read as the registry.

Usage:
  python3 symbol_audit.py [SPEC-v5.0-PRE.md]     # exit 0 when every symbol has a home
  python3 symbol_audit.py --verbose              # also print every accounted symbol
  python3 symbol_audit.py --selftest
Standard library only.
"""

import argparse
import re
import sys

# ------------------------------------------------------------------ whitelist (e)
WHITELIST = {
    "i": "index of a source or dimension, bound by FOR ALL i / FOR every source i",
    "j": "second index in trust(user, domain_i) ≠ trust(user, domain_j)",
    "k": "count or index (recorded occasions, invariant k)",
    "n": "count (recorded interactions, sample size)",
    "p": "a party in the affected set P(a); p_1 ... p_n are its elements",
    "a": "the action under judgment; a' an alternative action",
    "b": "count of broken occasions (Appendix G, WEIGHT-BETA-1)",
    "c": "prior mass (1 - ε) · m (Appendix G, WEIGHT-BETA-1)",
    "x": "generic function argument, as in μ(x) and exact_predicate(x)",
    "t": "time or turn index, as in w_i(t=0)",
    "r": "a rule of this judgment model, bound by FOR ALL rules r",
    "A": "layer name in ARCHITECTURE [EXEC_ORDER] A → B → C, not a variable",
    "B": "layer name in ARCHITECTURE [EXEC_ORDER] A → B → C, not a variable",
    "C": "layer name in ARCHITECTURE [EXEC_ORDER] A → B → C, not a variable",
    "E": "expectation operator E[·] in unconsented_harm",
    "Σ": "summation operator",
    "μ": "Zadeh's membership function μ(x) ∈ [0,1], the basis named in MATH_FOUNDATION; the fuzzy operators are registered as CONST-ZADEH",
}

DIMS = ["int", "cap", "csq", "rel", "cer", "aut", "rev", "evd", "sov", "ine", "ext"]
MODES = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"]
F_V5_BOUND = set(DIMS) | set(MODES) | {"S", "f_v5"}

FORMULA_CHARS = ("=", "∈", "≤", "≥", "≠", "≡", "<", ">", "Σ", "∞", "≈", "⇒", "→", "lim_")
# assertion words are scanned on every line in scope, formula or prose
ASSERTION_WORDS = (("≈", re.compile("≈")), ("lim", re.compile(r"\blim(?=[_\s(])")),
                   ("converge", re.compile(r"\bconverg", re.I)))
MARKERS = ("explanatory", "non-normative", "HYPOTHESIS", "SUPERSEDED", "untested")
FIELD_LINE = re.compile(r"^\s*(T|A|S|V|M|R):")
DECL_HEAD = re.compile(r"^\s*::")
TAG = re.compile(r"^\s*\[([A-Za-z_:0-9|=.\- ]+)\]")
GREEK = re.compile(r"[α-ωΑ-Ω]")
# subscripted variable: a short base (1-2 letters, Greek allowed) or a named operator, then _sub;
# Σ_ and lim_ are operators, handled as the Greek operator Σ and the assertion word lim
SUBSCRIPTED = re.compile(r"(?<![A-Za-z0-9_])((?:(?!Σ)[A-Za-zα-ωΑ-Ω]{1,2}|ES|CVaR)_(?:\{[^}]*\}|[A-Za-z0-9.]+)(?:\^\{[^}]*\})?)")
OPERATOR_SUB = re.compile(r"(?:Σ|lim)_(?:\{[^}]*\}|[A-Za-z0-9.]+)(?:\^\{[^}]*\})?")
CITATION = re.compile(r"\(?(?:Appendix [A-Z]|Part I{1,3}V?(?: §[0-9.]+)?|Layer [A-C]|Axiom \d|MODULE::[A-Z_]+|STEP[-:]\d(?: to STEP[-:]\d)?|CONVENTION-\d|MODES-SUPERSEDED)[^()]*\)?")
SINGLE = re.compile(r"(?<![A-Za-z0-9_'])([A-Za-zα-ωΑ-Ω])(?![A-Za-z0-9_])(?:'|)")
REGISTRY_ID = re.compile(r"\b((?:CONST|WEIGHT|TRUST|WEIGHTS)-[A-Z0-9_.:\-]+)")
CITES_AXIOM = re.compile(r"Axiom\s+(\d)")
CITES_MODULE = re.compile(r"MODULE::([A-Z_]+)")
SUPERSEDED_BLOCKS = re.compile(r"\[SUPERSEDED\]\s*((?:STEP:\d(?:\s*(?:and|,)\s*)?)+)")


def strip_structure(line):
    """Remove the leading [TAG], quoted strings and citations (Appendix G, Part II §3, Layer C,
    Axiom 4, MODULE::NAME, STEP-1), keep the formula."""
    s = TAG.sub(" ", line, count=1)
    s = re.sub(r'"[^"]*"', " ", s)
    s = CITATION.sub(" ", s)
    return s


def definition_patterns(sym):
    e = re.escape(sym)
    return [
        re.compile(r"\bDEFINE\b[^=≡]*(?<![A-Za-z0-9_])" + e + r"(?![A-Za-z0-9_])"),   # head side of DEFINE
        re.compile(r"(?<![A-Za-z0-9_])" + e + r"(?:\([^)]*\))?\s*(=|≡|∈|:=)(?!=)"),   # x = ..., x(t) = ..., x ∈ ...
        re.compile(r"\b(WITH|with)\s+" + e + r"(?![A-Za-z0-9_])"),                     # WITH g: ..., with ε > 0
        re.compile(r"\bFOR\s+(ALL|every)\s+(?:\w+\s+)?" + e + r"(?![A-Za-z0-9_])"),   # FOR ALL i, FOR every source i
        re.compile(r"(?<![A-Za-z0-9_])" + e + r"\s*[<>]\s*[0-9]"),                     # ε > 0 (domain declaration)
        re.compile(r"\b0\s*<\s*" + e + r"(?![A-Za-z0-9_])"),                            # 0 < w_i < 1
    ]


class Module:
    def __init__(self, name, part, start):
        self.name, self.part, self.start = name, part, start
        self.lines = []          # (lineno, text)

    def text(self):
        return "\n".join(t for _, t in self.lines)


def split_document(lines):
    """Return (modules_in_scope, appendix_g_text). Scope: Part I ::MODULE blocks, Part II §1-§5
    as one module, Part IV ::MODULE::GENE_CORRECTION."""
    part = None
    modules, current = [], None
    part2 = None
    appendix_g, in_g = [], False
    for no, raw in enumerate(lines, 1):
        t = raw.rstrip("\n")
        if t.startswith("# Part I "):
            part = "I"
        elif t.startswith("# Part II "):
            part = "II"
        elif t.startswith("# Part III "):
            part = "III"
        elif t.startswith("# Part IV "):
            part = "IV"
        if t.startswith("## Appendix G"):
            in_g = True
        elif in_g and (t.startswith("::STATE{@PATCH-1") or t.startswith("# Part")):
            in_g = False
        if in_g:
            appendix_g.append(t)
        if part in ("I", "IV"):
            m = re.match(r"^::MODULE::([A-Z_]+)\{", t)
            if m:
                current = Module(m.group(1), part, no)
                if part == "I" or m.group(1) == "GENE_CORRECTION":
                    modules.append(current)
                continue
            if current is not None:
                if t.strip() == "}":
                    current = None
                else:
                    current.lines.append((no, t))
        elif part == "II":
            if t.startswith("## §1 "):
                part2 = Module("PART_II_§1-§5", "II", no)
                modules.append(part2)
                continue
            if t.startswith("## §6 "):
                part2 = None
            if part2 is not None:
                part2.lines.append((no, t))
    return modules, "\n".join(appendix_g)


def marked_blocks(module):
    """Line numbers covered by an explanatory / non-normative / HYPOTHESIS marker or a
    [SUPERSEDED] note naming [STEP:n] blocks."""
    covered = set()
    superseded = set()
    for _, t in module.lines:
        m = SUPERSEDED_BLOCKS.search(t)
        if m:
            superseded.update(re.findall(r"STEP:\d", m.group(1)))
    block_marked = False
    for no, t in module.lines:
        tag = TAG.match(t)
        if tag:
            head = tag.group(1)
            block_marked = any(k.lower() in head.lower() for k in MARKERS) or \
                any(head.startswith(s) for s in superseded)
        if block_marked or any(k.lower() in t.lower() for k in MARKERS):
            covered.add(no)
    return covered


def cited_modules(module, all_modules):
    names = set(CITES_MODULE.findall(module.text()))
    if CITES_AXIOM.search(module.text()):
        names.add("AXIOMS")
    return [m for m in all_modules if m.name in names and m is not module]


def is_formula_line(t):
    if FIELD_LINE.match(t) or DECL_HEAD.match(t) or t.lstrip().startswith("#"):
        return False
    body = strip_structure(t)
    return any(c in body for c in FORMULA_CHARS)


DIM_RX = re.compile(r"\b(" + "|".join(DIMS) + r")\b")
MODE_RX = re.compile(r"\bM[1-8]\b")


def extract(t, formula):
    """Symbols (formula lines only) and assertion words (every line) on one line."""
    body = strip_structure(t)
    found = []
    if formula:
        for m in DIM_RX.finditer(body):
            found.append(("dim", m.group(1)))
        for m in MODE_RX.finditer(body):
            found.append(("mode", m.group(0)))
        body_ops = OPERATOR_SUB.sub(lambda m: " Σ " if m.group(0).startswith("Σ") else " ", body)  # Σ_i -> Σ, lim_{..} dropped
        for m in SUBSCRIPTED.finditer(body_ops):
            found.append(("sub", m.group(1)))
        # remove subscripted tokens and identifiers before the single-letter scan
        rest = SUBSCRIPTED.sub(" ", body_ops)
        rest = re.sub(r"[A-Za-z_][A-Za-z0-9_]{1,}", " ", rest)      # words and snake_case names
        rest = re.sub(r"\b[A-Za-z][0-9]+\b", " ", rest)              # v1, H1
        for m in SINGLE.finditer(rest):
            found.append(("var", m.group(1)))
        for g in GREEK.findall(re.sub(r"[A-Za-zα-ωΑ-Ω]{1,2}_\S+", " ", body_ops)):
            if ("var", g) not in found:
                found.append(("greek", g))
    for w, rx in ASSERTION_WORDS:
        if rx.search(body):
            found.append(("assert", w))
    # de-duplicate, keep order
    out, seen = [], set()
    for kind, sym in found:
        if (kind, sym) not in seen:
            seen.add((kind, sym))
            out.append((kind, sym))
    return out


def base_of(sym):
    return sym.split("_", 1)[0]


def audit(lines):
    modules, appendix_g = split_document(lines)
    registry_ids = set(REGISTRY_ID.findall(appendix_g))
    unaccounted, accounted = [], []
    for mod in modules:
        marked = marked_blocks(mod)
        scope_text = mod.text()
        cited = cited_modules(mod, modules)
        for no, t in mod.lines:
            if FIELD_LINE.match(t) or DECL_HEAD.match(t) or t.lstrip().startswith("#"):
                continue
            formula = is_formula_line(t)
            body = strip_structure(t)
            line_ids = set(REGISTRY_ID.findall(t))
            for kind, sym in extract(t, formula):
                home = None
                if kind == "assert":
                    head = body.strip().split(" ", 1)[0]
                    if no in marked:
                        home = "(d) marked"
                    elif "MODULE::MEASUREMENT" in t or mod.name == "MEASUREMENT":
                        home = "(a) convergence defined by MODULE::MEASUREMENT"
                    elif head in ("DEFINE", "PROPERTY", "IF", "HYPOTHESIS"):
                        home = "(a) definitional or conditional statement"
                elif no in marked:
                    home = "(d) marked"
                elif kind in ("dim", "mode") or sym in F_V5_BOUND:
                    home = "(b) f_v5"
                else:
                    pats = definition_patterns(sym)
                    if any(p.search(scope_text) for p in pats):
                        home = "(a) defined in " + mod.name
                    else:
                        for other in cited:
                            if any(p.search(other.text()) for p in pats):
                                home = "(a) defined in cited " + other.name
                                break
                    if home is None and (line_ids & registry_ids or (kind != "var" and sym in appendix_g)):
                        home = "(c) registry " + ",".join(sorted(line_ids & registry_ids)) if line_ids & registry_ids else "(c) registry"
                    if home is None and sym in WHITELIST:
                        home = "(e) whitelist: " + WHITELIST[sym]
                    if home is None and kind == "sub" and base_of(sym) in ("p", "i", "k", "n", "a", "b", "c"):
                        home = "(e) whitelist: " + WHITELIST[base_of(sym)]
                rec = (no, mod.name, kind, sym, t.strip())
                if home:
                    accounted.append(rec + (home,))
                else:
                    unaccounted.append(rec)
    return unaccounted, accounted, modules


def run(path, verbose):
    with open(path, encoding="utf-8") as f:
        lines = f.read().replace("\r\n", "\n").split("\n")
    unaccounted, accounted, modules = audit(lines)
    print(f"{path}: {len(modules)} modules in scope, {len(accounted)} symbols accounted, "
          f"{len(unaccounted)} unaccounted")
    if verbose:
        for no, mod, kind, sym, text, home in accounted:
            print(f"  ok   L{no} {mod:<18} {kind:<6} {sym:<14} {home}")
    for no, mod, kind, sym, text in unaccounted:
        print(f"  MISS L{no} {mod:<18} {kind:<6} {sym:<14} {text[:110]}")
    return 1 if unaccounted else 0


# ------------------------------------------------------------------------ selftest
SELFTEST_DOC = """# Part I — test
::MODULE::ALPHA{
  DEFINE q(a) = max expected loss.
  PROPERTY q(a) ≤ budget(a)
  IF reversibility(a) < 0.20 → aut is set to 0.29
  [EMERGENT|explanatory]
  friction = -∇(v7 × v3) ⊗ sandbox
  NOTE lim_{n→∞} of nothing is fine here.
}
::MODULE::BETA{
  DEFINE w(x) = ζ · x (Axiom 1)
  tail = ES_0.975(1 - csq) (Appendix G, CONST-ES-975)
  Multiple assessments converge to a value.
  [STEP:2|old]
  COMPUTE net = U(a)
  [SUPERSEDED] STEP:2 is the PRE description.
}
# Part II — test
## §1 Dims
T:all_dims_range=[0.00,1.00]|precision:2dp
## §3 f
  S = 0.15·int + 0.85·ext
## §6 stop
# Part IV — test
::MODULE::GENE_CORRECTION{
  [RELATIONSHIP:to_DNA_hypothesis|non-normative]
  Ψ(t) = (G ⊗ B) · E(t)
}
## Appendix G — Model Registry (non-normative)
::FACT{id:CONST-ES-975|value:expected_shortfall_at_0.975|basis:Basel|status:benchmarked}
::STATE{@PATCH-1, end:true}
"""


def cmd_selftest():
    unaccounted, accounted, modules = audit(SELFTEST_DOC.split("\n"))
    missing = {(m, s) for _, m, _, s, _ in unaccounted}
    homes = {(m, s): h for _, m, _, s, _, h in accounted}
    t = [
        ("scope: the four modules are found (ALPHA, BETA, Part II, GENE_CORRECTION)",
         [m.name for m in modules] == ["ALPHA", "BETA", "PART_II_§1-§5", "GENE_CORRECTION"]),
        ("(a) DEFINE head accounts for q", homes.get(("ALPHA", "q"), "").startswith("(a)")),
        ("(b) dimension name aut is bound to f_v5", homes.get(("ALPHA", "aut"), "").startswith("(b)")),
        ("(d) explanatory block: nothing in it is flagged", not any(m == "ALPHA" and s in ("∇", "v7", "v3") for m, s in missing)),
        ("(d) lim inside a NOTE of the explanatory block passes", homes.get(("ALPHA", "lim"), "").startswith("(d)")),
        ("unmarked Greek ζ without a definition is flagged", ("BETA", "ζ") in missing),
        ("(c) registry citation accounts for ES_0.975", homes.get(("BETA", "ES_0.975"), "").startswith("(c)")),
        ("assertion word converge on a prose line without a definition is flagged", ("BETA", "converge") in missing),
        ("[SUPERSEDED] covers STEP:2 so U passes as (d)", homes.get(("BETA", "U"), "").startswith("(d)")),
        ("Part II: S is bound to f_v5 and int/ext are dimensions", homes.get(("PART_II_§1-§5", "S"), "").startswith("(b)")
         and homes.get(("PART_II_§1-§5", "int"), "").startswith("(b)")),
        ("field line T: is not scanned", not any(m == "PART_II_§1-§5" and s == "T" for m, s in missing)),
        ("Part IV non-normative block covers Ψ, G, B, E", not any(m == "GENE_CORRECTION" for m, _ in missing)),
        ("whitelist (e) accounts for x; a is bound by the DEFINE head", homes.get(("BETA", "x"), "").startswith("(e)")
         and homes.get(("ALPHA", "a"), "").startswith("(a)")),
        ("exactly the two planted gaps are reported", missing == {("BETA", "ζ"), ("BETA", "converge")}),
    ]
    failed = [n for n, ok in t if not ok]
    for n, ok in t:
        print(("PASS " if ok else "FAIL ") + n)
    print(f"\n{len(t) - len(failed)}/{len(t)} passed")
    return 1 if failed else 0


def main():
    p = argparse.ArgumentParser(description="iLang v5.0 symbol audit (seal condition S3)")
    p.add_argument("path", nargs="?", default="SPEC-v5.0-PRE.md")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--verbose", action="store_true")
    a = p.parse_args()
    if a.selftest:
        return cmd_selftest()
    return run(a.path, a.verbose)


if __name__ == "__main__":
    sys.exit(main())
