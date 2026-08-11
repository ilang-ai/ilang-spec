#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I-Lang Grammar & Registry Validator
Implements the mechanical checks of SPEC-v5.0-PATCH-2 (declaration grammar and
registries) plus the v3.0 operation tables:

  PATCH-2 §1.1  block shapes inline / header_body / brace_span, shape selection
                by lookahead, FLUSH-LEFT-BODY rule (incl. same-line trailing body)
  PATCH-2 §1.2  body forms B1-B8 by first-token dispatch; B6 prose only inside
                prose-body types [::LESSON, ::MODULE, ::LIST, ::RULE annotation,
                ::OBJECTIVE narrative fields]
  PATCH-2 §1.5/§1.6  declaration registry: 32 structural + 13 narrative
                (::LATENCY / ::CONFIDENCE tolerated per §1.6 pending registration)
  PATCH-2 §1.7  document header ::ILANG::<ver>, [TAG:value] preamble lines,
                temporal prefix T[n] and T[n]=value, `=>` chain continuation,
                narrative pipe payload
  PATCH-2 §2.2  entity casing @[A-Z][A-Z0-9_]* (E300); custom entities SHOULD
                be introduced via ::STATE (WARN)
  v3.0 §3/§4    operation verbs (88) + Greek aliases (13) -> E304 / E305;
                modifier keys (29) -> E302 (WARN by default, see NOTE)

Static scope: E200 (unresolvable name) and E201 (environment availability) are
runtime semantics, intentionally out of scope. E202 (rebinding a registered
name) is reported as a WARN candidate when a document ::STATE-introduces a
Tier-1/2 name.

NOTE on E302: the modifier registry is closed at 29 (no_new_modifiers
reaffirmed 2026-08-11; the v4.0-FINAL §7 examples that used ad-hoc keys were
rewritten to registered ones). Unknown operation modifier keys are ERROR.

Input modes (auto-detected per file):
  raw    first nonblank line is ::ILANG::  -> whole file is I-Lang
  mixed  Markdown carrying bare I-Lang blocks (PATCH style) and/or ``` fences.
Fenced blocks are linted when their first nonblank line looks like I-Lang
('::', 'T[', or a bracket group); other fences are counted as skipped and
reported — never silently dropped.

Usage:
  python3 ilang_grammar_validator.py --selftest
  python3 ilang_grammar_validator.py --lint FILE [FILE ...] [--json] [--strict]
  python3 ilang_grammar_validator.py --canon REPO_DIR [--json] [--strict]

Exit code: 1 if any ERROR (with --strict, also if any WARN), else 0.
Single file, stdlib only.
"""

import argparse
import json
import re
import sys

# ------------------------------------------------------------------ registries
REGISTRY_V3 = ("STATE TRUST ALIVE MEMORY GENE GENE_MUTABLE RULE ACTIVATE "
               "FACT LESSON PROGRESS PRIORITY DECAY IMMUNE").split()
REGISTRY_V4 = "UNTRUSTED BUDGET STATUS OBJECTIVE RUBRIC EVIDENCE PRIOR FALLBACK".split()
REGISTRY_V5 = "JUDGE BOUNDARY DIM MODE FUNC SCHEMA CASE CLAUSE MODULE".split()
REGISTRY_AMEND = ["LIST"]
DECL_STRUCTURAL = set(REGISTRY_V3 + REGISTRY_V4 + REGISTRY_V5 + REGISTRY_AMEND)

DECL_NARRATIVE = set("SAY THINK ACT DECIDE DISCOVER CREATE EVENT SILENCE "
                     "META IRONY FORESHADOW CALLBACK EMOTION_FIELD".split())
NARR_DOUBLE = set("SAY THINK ACT DECIDE DISCOVER CREATE".split())
TERMINATORS = {"END_UNTRUSTED"}          # block terminator, not a declaration
META_DECLS = {"GRAMMAR", "BODY", "REGISTRY"}  # spec-authoring set, counted separately
TOLERATED_ANNOT = {"LATENCY", "CONFIDENCE"}  # §1.6: tolerated pending registration
PROSE_BODY = {"LESSON", "MODULE", "LIST", "RULE", "OBJECTIVE"}  # B6 whitelist

VERBS = set(("READ WRIT GET DEL LIST COPY MOVE STRM CACH SYNC SEND RUN "
             "FMT CONV SPLIT MERGE MAP FILT SORT DEDU FLAT NEST CHNK REDU "
             "PIVT TRNS ENCD DECD HASH CMPR EXPN XLAT REWR DIFF "
             "SCAN MTCH CNT STAT EVAL SCOR RANK TRND CORR FRCS ANOM SENT "
             "CLST BNCH AUDT VALD CLSF "
             "CREA DRFT EXPD SHRT PARA STYL TMPL FILL EXTC GEN "
             "PLAN DECI CHEK FIX DPLO SAVE REVW LERN TEST PARS LOOP WAIT "
             "OUT DISP EXPT PRNT LOG LINK SET TAG GRP EMBD "
             "HELP DESC INTR NOOP BATC").split())
ALIASES = set("Σ Δ φ ∇ λ ∂ μ ψ ξ ζ θ Ω Π".split())
GREEKISH = "ΣΔφ∇λ∂μψξζθΩΠ"
MODIFIERS = set(("src dst path fmt lng sty ton len lim off top bot srt grp "
                 "whr mch exc dep rng typ enc cap pri col row frm to scp op").split())
# meta-variables used by the specs' own teaching examples — informational only
PLACEHOLDER_HEADS = {"VERB", "VERB1", "VERB2", "VERB3", "DECL"}

TIER1 = set("@SRC @DST @PREV @LOCAL @SCREEN @LOG @NULL @STDIN".split())
TIER2 = set("@GH @R2 @COS @DRIVE @WORKER @CF".split())
TIER3 = set("@SYSTEM @RUNTIME @GRADER @USER @SELF @AGENT @TASK @TOOL".split())
REGISTERED_ENTITIES = TIER1 | TIER2 | TIER3
# meta-variables the specs use in canonical forms — never real entities
PLACEHOLDER_ENTITIES = set("A B ENTITY FROM TO TARGET NAME SOURCE".split())

# --------------------------------------------------------------------- regexes
RE_DOC_MARKER = re.compile(r"^::ILANG::\S+$")
RE_DECL_HEAD = re.compile(r"^::([A-Z][A-Z0-9_]*)(?:::([A-Z][A-Z0-9_]*))?(.*)$")
RE_BAD_DECL_HEAD = re.compile(r"^::(\S*)")
RE_TEMPORAL_PREFIX = re.compile(r"^(T\[[^\]]+\])\s+(::.*)$")
RE_TEMPORAL_BIND = re.compile(r"^T\[[^\]]+\]=\S+")
RE_TEMPORAL_NOTE = re.compile(r"^(T\[[^\]]+\](→T\[[^\]]+\])?|PARALLEL\{[^}]*\})(\s.*)?$")
RE_TAG_LINE = re.compile(r"^(\[[A-Z][A-Z0-9_\-]*(?::[^\[\]]*)?\])+$")
# B5 form 1: `[TAG] text` — one tag group, optional trailing free text
RE_TAG_TEXT = re.compile(r"^\[[A-Z][A-Z0-9_\-]*(?::[^\[\]]*)?\](\s+\S.*)?$")
RE_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):(.*)$")
# entity tokens count only in structural positions ({, :, |, comma, →, =);
# @ tokens embedded in free prose values are exempt (PATCH-2 Appendix B)
RE_ENTITY_TOKEN = re.compile(r"(?<=[{:|,→=])@([A-Za-z][A-Za-z0-9_\-]*)")
RE_ENTITY_OK = re.compile(r"^@[A-Z][A-Z0-9_]*$")
RE_BRACKET_GROUPS = re.compile(r"\[([^\[\]]*)\]")
RE_FENCE = re.compile(r"^\s*```")
RE_STATE_INTRO = re.compile(r"^::STATE\{(@[A-Z][A-Z0-9_]*)[,|}\s]")

ERROR, WARN, INFO = "ERROR", "WARN", "INFO"


class Linter:
    def __init__(self, path, text):
        self.path = path
        self.findings = []           # (level, lineno, code, message)
        self.lines = text.splitlines()
        self.skipped_fences = 0
        self.linted_fences = 0
        self.annotations = 0
        self.custom_entities = {}    # name -> first lineno (used w/o ::STATE intro)
        self.introduced = set()      # entities introduced via ::STATE
        self.mixed_last_op = False
        self.body_last_op = False
        raw = next((l for l in self.lines if l.strip()), "")
        self.raw_mode = raw.strip().startswith("::ILANG::")

    def add(self, level, lineno, code, msg):
        self.findings.append((level, lineno, code, msg))

    # ------------------------------------------------------------ entry points
    def run(self):
        if self.raw_mode:
            self.lint_region(0, len(self.lines), raw=True)
        else:
            self.scan_mixed()
        # SHOULD-level summary: custom entities used without ::STATE introduction
        pending = sorted(n for n in self.custom_entities
                         if n not in self.introduced and n not in PLACEHOLDER_ENTITIES)
        if pending:
            first = min(self.custom_entities[n] for n in pending)
            self.add(INFO, first, "SHOULD",
                     "custom entities used without ::STATE introduction (PATCH-2 §2.2 SHOULD): "
                     + ", ".join(pending))
        return self.findings

    def scan_mixed(self):
        i, n = 0, len(self.lines)
        while i < n:
            line = self.lines[i]
            if RE_FENCE.match(line):
                start = i + 1
                i += 1
                while i < n and not RE_FENCE.match(self.lines[i]):
                    i += 1
                end = i          # fence body is [start, end)
                i += 1           # skip closing fence
                first = next((self.lines[j].strip() for j in range(start, end)
                              if self.lines[j].strip()), "")
                if self.is_ilang_start(first):
                    self.linted_fences += 1
                    self.lint_region(start, end, raw=True)
                else:
                    self.skipped_fences += 1
                continue
            s = line.strip()
            if s.startswith("::") or RE_TEMPORAL_PREFIX.match(s):
                self.mixed_last_op = False
                i = self.parse_construct(i, mixed=True)
                continue
            # bare operation chains / tag-or-op lines; markdown links and
            # reference-style links never fully match these shapes. A `=>` line
            # in mixed mode is linted only as a continuation of a preceding bare
            # operation line — otherwise it is markdown background.
            if not s:
                self.mixed_last_op = False
            elif s.startswith("=>"):
                if self.mixed_last_op:
                    self.check_operation(i, s[2:].strip(), chain=True)
            elif s.startswith("[") and "](" not in s and not s.startswith("[!"):
                if "]=>" in s or RE_TAG_LINE.match(s):
                    self.check_bracket_line(i, s)
                    self.mixed_last_op = ("]=>" in s
                                          or self.head_of(s) in VERBS | ALIASES)
            else:
                self.mixed_last_op = False
            i += 1

    @staticmethod
    def is_ilang_start(s):
        if s.startswith("::") or s.startswith("T["):
            return True
        if s.startswith("[") and "](" not in s and not s.startswith("[!"):
            return bool(re.match(r"\[[A-Z" + GREEKISH + r"]", s))
        return False

    # -------------------------------------------------------------- region walk
    STRUCTURAL_CHARS = ("::", "[", "{", "}", "|", "⇒", "=>")

    def lint_region(self, start, end, raw):
        i = start
        last_op = False          # tracks whether `=>` may continue a chain
        seen_construct = False   # colophon tolerance: prose ok in tag-only regions
        in_preamble = False      # §1.7: tag lines right after a ::ILANG header
        nonblank = [j for j in range(start, end) if self.lines[j].strip()]
        first_nb = nonblank[0] if nonblank else -1
        last_nb = nonblank[-1] if nonblank else -1
        while i < end:
            s = self.lines[i].strip()
            if not s or s == "---":
                last_op = False
                i += 1
                continue
            if RE_DOC_MARKER.match(s):
                if i == first_nb:
                    in_preamble = True
                elif i != last_nb:
                    self.add(ERROR, i + 1, "E300",
                             "::ILANG document marker may only open or close a document (§1.7)")
                last_op = False
                i += 1
                continue
            if RE_TEMPORAL_BIND.match(s):
                last_op = False
                i += 1
                continue
            in_preamble_here, in_preamble = in_preamble, False
            if s.startswith("::") or RE_TEMPORAL_PREFIX.match(s):
                seen_construct, last_op = True, False
                i = self.parse_construct(i, mixed=False, limit=end)
                continue
            if s.startswith("=>"):
                if last_op:
                    self.check_operation(i, s[2:].strip(), chain=True)
                else:
                    self.add(ERROR, i + 1, "E300",
                             "orphan `=>` continuation: no preceding operation line")
                i += 1
                continue
            if s.startswith("["):
                # preamble position (§1.7): tag lines right after a ::ILANG
                # header are document metadata even when TAG collides with a
                # verb name — never parsed as operations, no E304
                if in_preamble_here and RE_TAG_LINE.match(s) and "]=>" not in s:
                    in_preamble = True
                    last_op = False
                    i += 1
                    continue
                self.check_bracket_line(i, s)
                last_op = "]=>" in s or self.head_of(s) in VERBS | ALIASES
                if last_op:
                    seen_construct = True   # tag metadata lines are not constructs
                i += 1
                continue
            last_op = False
            if RE_TEMPORAL_NOTE.match(s):
                i += 1
                continue
            if s.startswith("→") or s.startswith("<<<"):
                self.annotations += 1
                i += 1
                continue
            if not seen_construct and not any(c in s for c in self.STRUCTURAL_CHARS):
                self.annotations += 1      # colophon prose in a tag-only region
                i += 1
                continue
            self.add(ERROR, i + 1, "E300",
                     "line matches no I-Lang production: " + s[:60])
            i += 1

    # --------------------------------------------------------- construct parser
    def parse_construct(self, i, mixed, limit=None):
        """Parse one ::DECL construct starting at line i; return next index."""
        end = limit if limit is not None else len(self.lines)
        line = self.lines[i]
        stripped = line.strip()
        prefix_m = RE_TEMPORAL_PREFIX.match(stripped)
        decl_text = prefix_m.group(2) if prefix_m else stripped
        header_indent = len(line) - len(line.lstrip())

        m = RE_DECL_HEAD.match(decl_text)
        if not m:
            bad = RE_BAD_DECL_HEAD.match(decl_text)
            self.add(ERROR, i + 1, "E300",
                     "malformed declaration header: " + (bad.group(0) if bad else decl_text)[:60])
            return i + 1
        name, subname, rest = m.group(1), m.group(2), m.group(3)

        if name == "ILANG":
            if not RE_DOC_MARKER.match(decl_text):
                self.add(ERROR, i + 1, "E300",
                         "malformed ::ILANG document marker: " + decl_text[:60])
            return i + 1
        if subname and name != "MODULE":
            self.add(ERROR, i + 1, "E300",
                     "::%s::%s — only ::MODULE takes a two-segment name (§1.7)" % (name, subname))
        registered = (name in DECL_STRUCTURAL or name in DECL_NARRATIVE
                      or name in TERMINATORS or name in META_DECLS)
        if not registered:
            if name in TOLERATED_ANNOT:
                self.annotations += 1
                return i + 1
            self.add(ERROR, i + 1, "E300",
                     "::%s is not in the declaration registry (32 structural + 13 narrative, PATCH-2 §1.5/§1.6)" % name)

        self.scan_entities(i, decl_text)

        rest = rest.strip() if rest else ""
        if not rest.startswith("{"):
            self.add(ERROR, i + 1, "E300", "::%s header lacks `{`" % name)
            return i + 1

        # §1.3: full-width ：/｜ as structural separators ⇒ E300. Full-width
        # punctuation is legal inside values, so ： is flagged only when a
        # pipe-delimited field carries no ASCII colon at all.
        if "｜" in rest:
            self.add(ERROR, i + 1, "E300",
                     "full-width ｜ as structural separator (§1.3) — use ASCII `|`")
        elif "：" in rest:
            for seg in rest.strip("{}").split("|"):
                if "：" in seg and ":" not in seg:
                    self.add(ERROR, i + 1, "E300",
                             "full-width ： as structural separator (§1.3) — use ASCII `:`")
                    break

        # narrative double-brace requirement; content brace may span lines
        if name in NARR_DOUBLE:
            if re.match(r"^\{[^{}]*\}\{.*\}\s*$", rest):
                return self.consume_body(i, name, header_indent, end)
            if re.match(r"^\{[^{}]*\}\{[^}]*$", rest):
                return self.consume_brace_span(i, name, rest, end)
            self.add(ERROR, i + 1, "E300",
                     "::%s requires double-brace form ::VERB{addressing}{content} (v3.0 §7)" % name)
            return i + 1

        # brace balance on the header line decides the shape
        balance = rest.count("{") - rest.count("}")
        if balance > 0:
            return self.consume_brace_span(i, name, rest, end)

        # inline / header_body; same-line trailing body token permitted
        close = self.find_close(rest)
        trailing = rest[close + 1:].strip() if close >= 0 else ""
        if trailing:
            self.classify_body_line(i, name, trailing, nested=False)

        if name == "UNTRUSTED":
            dm = re.search(r"delimiter:([^|}\s]+)", rest)
            if dm:
                return self.consume_opaque(i + 1, dm.group(1), end)

        im = RE_STATE_INTRO.match(decl_text)
        if im:
            ent = im.group(1)
            self.introduced.add(ent.lstrip("@"))
            if ent in TIER1 | TIER2:
                self.add(WARN, i + 1, "E202",
                         "::STATE re-introduces registered name %s — possible rebinding (§2.2)" % ent)

        return self.consume_body(i, name, header_indent, end)

    @staticmethod
    def find_close(rest):
        depth = 0
        for k, ch in enumerate(rest):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return k
        return -1

    def consume_brace_span(self, i, name, rest, end):
        # §1.1: a set-span (header ends with `{`) terminates at the bare `}` line;
        # a wrapped field header (content after the opening brace, v3.0 §10.3
        # style) terminates at the first line ending with `}`. Braces embedded
        # mid-content are content, not structure.
        wrapped = not rest.rstrip().endswith("{")
        j = i + 1
        while j < end:
            t = self.lines[j].strip()
            if t == "}" or (wrapped and t.endswith("}")):
                return j + 1
            j += 1
        self.add(ERROR, i + 1, "E300", "::%s brace span never closes" % name)
        return end

    def consume_opaque(self, j, delimiter, end):
        while j < end:
            if self.lines[j].strip() == delimiter:
                return j + 1
            j += 1
        return j

    def consume_body(self, i, name, header_indent, end):
        """Collect header_body lines: indented, or flush-left per FLUSH-LEFT-BODY."""
        j = i + 1
        regime = None            # 'indent' | 'flush' once the first body line binds
        self.body_last_op = False
        while j < end:
            line = self.lines[j]
            s = line.strip()
            if not s:
                if regime != "indent":
                    return j     # flush-left bodies terminate at the first blank
                # blank permitted inside indented body if next nonblank still indented
                k = j + 1
                while k < end and not self.lines[k].strip():
                    k += 1
                if k < end:
                    nxt = self.lines[k]
                    if len(nxt) - len(nxt.lstrip()) > header_indent:
                        j = k
                        continue
                return j
            indent = len(line) - len(line.lstrip())
            if indent > header_indent:
                if regime == "flush":
                    return j
                regime = "indent"
                j = self.body_line(j, name, s, indent, end)
                continue
            if regime == "indent":
                return j         # dedent terminates the indented body (§1.1)
            if indent != header_indent:
                return j         # FLUSH-LEFT binds at the same indent only
            # flush-left: body-form line binds; next `::`/`T[` header terminates
            if s.startswith("::") or RE_TEMPORAL_PREFIX.match(s) or RE_DOC_MARKER.match(s):
                return j
            if self.is_body_form(s):
                regime = "flush"
                self.classify_body_line(j, name, s, nested=False)
                j += 1
                continue
            return j
        return j

    def body_line(self, j, name, s, indent, end):
        """Handle one indented body line; B7 nesting may consume extra lines."""
        if s.startswith("::"):
            nm = RE_DECL_HEAD.match(s)
            nested_name = nm.group(1) if nm else "?"
            if nm and (nested_name in TOLERATED_ANNOT):
                self.annotations += 1
                return j + 1
            if not nm or (nested_name not in DECL_STRUCTURAL
                          and nested_name not in DECL_NARRATIVE):
                self.add(ERROR, j + 1, "E300",
                         "nested ::%s is not a registered declaration" % nested_name)
                return j + 1
            if nested_name in NARR_DOUBLE:
                nrest = s[2 + len(nested_name):].strip()
                if not re.match(r"^\{[^{}]*\}\{.*\}\s*$", nrest):
                    self.add(ERROR, j + 1, "E300",
                             "::%s requires double-brace form ::VERB{addressing}{content} (v3.0 §7)" % nested_name)
            self.scan_entities(j, s)
            # nested declaration may carry its own deeper body (B1-B6); a
            # declaration nested deeper still exceeds one level -> E300
            k = j + 1
            while k < end:
                ln = self.lines[k]
                t = ln.strip()
                if not t:
                    break
                ind2 = len(ln) - len(ln.lstrip())
                if ind2 <= indent:
                    break
                if t.startswith("::"):
                    self.add(ERROR, k + 1, "E300",
                             "declaration nesting exceeds one level (§1.2 B7)")
                else:
                    self.classify_body_line(k, nested_name, t, nested=True)
                k += 1
            return k
        self.classify_body_line(j, name, s, nested=False)
        return j + 1

    def is_body_form(self, s):
        """B1-B5 / reserved-key shapes eligible for flush-left binding.
        B8 (`[VERB...]` operations, `=>` continuations) is deliberately excluded:
        FLUSH-LEFT-BODY binds body forms B1-B5 only."""
        if s.startswith(("T:", "A:")):
            return True
        if s.startswith("["):
            return bool((RE_TAG_LINE.match(s) or RE_TAG_TEXT.match(s))
                        and self.head_of(s) not in VERBS | ALIASES)
        return bool(RE_KEY.match(s)) or bool(RE_TEMPORAL_BIND.match(s))

    def classify_body_line(self, j, parent, s, nested):
        lineno = j + 1
        if RE_TEMPORAL_BIND.match(s) or RE_TEMPORAL_NOTE.match(s):
            return
        if s.startswith("→"):
            self.annotations += 1
            return
        if s.startswith(("T:", "A:")):                       # B1
            self.scan_entities(j, s)
            return
        if s.startswith("=>"):                               # B8 continuation
            if self.body_last_op:
                self.check_operation(j, s[2:].strip(), chain=True)
            elif parent not in PROSE_BODY:
                self.add(ERROR, lineno, "E300",
                         "orphan `=>` continuation in ::%s body: no preceding operation line (§1.7)" % parent)
            return
        if s.startswith("["):                                # B5 or B8
            if "]=>" in s or self.head_of(s) in VERBS | ALIASES:
                self.check_operation(j, s, chain=True)
                self.body_last_op = True
            elif RE_TAG_LINE.match(s) or RE_TAG_TEXT.match(s):
                pass                                         # B5 tag line
            elif parent in PROSE_BODY:
                pass                                         # bracket-initial prose
            else:
                self.add(ERROR, lineno, "E300",
                         "bracket body line is neither B5 tag nor B8 operation: " + s[:60])
            return
        km = RE_KEY.match(s)
        if km:                                               # B2 / B3 / B4
            self.scan_entities(j, s)
            return
        # else -> B6 prose
        if parent not in PROSE_BODY:
            self.add(ERROR, lineno, "E300",
                     "B6 prose body line inside non-prose ::%s (§1.2 B6): %s"
                     % (parent, s[:50]))

    # ---------------------------------------------------------- bracket lines
    @staticmethod
    def head_of(s):
        m = RE_BRACKET_GROUPS.search(s)
        if not m:
            return ""
        return re.split(r"[:|]", m.group(1), maxsplit=1)[0].strip()

    def check_bracket_line(self, i, s):
        if "]=>" in s:
            self.check_operation(i, s, chain=True)
            return
        head = self.head_of(s)
        if head in VERBS | ALIASES:
            self.check_operation(i, s, chain=False)
        elif RE_TAG_LINE.match(s):
            pass                                             # metadata tag line
        else:
            self.add(ERROR, i + 1, "E300",
                     "bracket line is neither tag nor operation: " + s[:60])

    def check_operation(self, i, s, chain):
        lineno = i + 1
        for grp in RE_BRACKET_GROUPS.findall(s):
            head = re.split(r"[:|]", grp, maxsplit=1)[0].strip()
            if head in PLACEHOLDER_HEADS:
                continue
            if head not in VERBS and head not in ALIASES:
                if chain:
                    code = "E305" if (len(head) == 1 and not head.isascii()) else "E304"
                    what = "alias" if code == "E305" else "verb"
                    self.add(ERROR, lineno, code,
                             "unknown %s `%s` in operation chain" % (what, head))
                continue
            rest = grp[len(head):]
            target = ""
            if rest.startswith(":"):
                target = rest[1:].split("|", 1)[0].strip()
            if target:
                if target.startswith("@"):
                    if not RE_ENTITY_OK.match(target):
                        self.add(ERROR, lineno, "E300",
                                 "entity `%s` violates @[A-Z][A-Z0-9_]* (§2.2)" % target)
                    else:
                        self.note_entity(i, target)
                elif head in ("BATC", "Π"):
                    if target not in VERBS and target not in ALIASES:
                        self.add(ERROR, lineno, "E304",
                                 "BATC verb reference `%s` is not a registered verb or alias" % target)
                else:
                    self.add(ERROR, lineno, "E300",
                             "operation target `%s` is not an @ENTITY (v3.0 §2.2; BATC/Π excepted)" % target)
            if "|" in rest:
                mods = rest.split("|", 1)[1]
                for seg in re.split(r"[|]", mods):
                    for piece in seg.split(","):
                        if "=" not in piece:
                            continue          # continuation of previous value
                        key = piece.split("=", 1)[0].strip()
                        if key and key not in MODIFIERS:
                            self.add(ERROR, lineno, "E302",
                                     "modifier `%s` not in the 29-key registry" % key)

    # -------------------------------------------------------------- entities
    def scan_entities(self, i, s):
        for tok in RE_ENTITY_TOKEN.finditer(s):
            name = "@" + tok.group(1)
            if tok.group(1)[0].islower():
                self.add(ERROR, i + 1, "E300",
                         "entity `%s` violates @[A-Z][A-Z0-9_]* (§2.2)" % name)
            elif name not in REGISTERED_ENTITIES and RE_ENTITY_OK.match(name):
                self.custom_entities.setdefault(tok.group(1), i + 1)

    def note_entity(self, i, name):
        if name not in REGISTERED_ENTITIES:
            self.custom_entities.setdefault(name[1:], i + 1)


# ------------------------------------------------------------------- commands
CANON_FILES = ["SPEC.md", "SPEC-v4.0-FINAL.md", "SPEC-v5.0-PRE.md",
               "SPEC-v5.0-PATCH-1.md", "SPEC-v5.0-PATCH-2.md",
               "AUTHORS.md", "README.md"]


def lint_paths(paths, as_json, strict):
    total_err = total_warn = 0
    report = []
    for path in paths:
        try:
            # utf-8-sig strips a UTF-8 BOM so raw-mode detection still works
            text = open(path, encoding="utf-8-sig").read()
        except UnicodeDecodeError:
            total_err += 1
            report.append({"file": path, "mode": "unreadable", "errors": 1,
                           "warnings": 0, "findings": [{
                               "level": ERROR, "line": 1, "code": "E300",
                               "message": "file is not valid UTF-8 (§1.3 file_encoding=UTF-8)"}]})
            if not as_json:
                print("%s:1 [ERROR E300] file is not valid UTF-8 (§1.3 file_encoding=UTF-8)" % path)
            continue
        except OSError as e:
            print("cannot read %s: %s" % (path, e), file=sys.stderr)
            return 2
        lt = Linter(path, text)
        findings = lt.run()
        errs = [f for f in findings if f[0] == ERROR]
        warns = [f for f in findings if f[0] == WARN]
        total_err += len(errs)
        total_warn += len(warns)
        report.append({
            "file": path,
            "mode": "raw" if lt.raw_mode else "mixed",
            "errors": len(errs), "warnings": len(warns),
            "fences_linted": lt.linted_fences, "fences_skipped": lt.skipped_fences,
            "tolerated_annotations": lt.annotations,
            "findings": [{"level": lv, "line": ln, "code": c, "message": m}
                         for lv, ln, c, m in findings],
        })
        if not as_json:
            for lv, ln, c, m in findings:
                print("%s:%d [%s %s] %s" % (path, ln, lv, c, m))
            print("%s: %d error(s), %d warning(s) | mode=%s fences linted=%d skipped=%d annotations=%d"
                  % (path, len(errs), len(warns),
                     "raw" if lt.raw_mode else "mixed",
                     lt.linted_fences, lt.skipped_fences, lt.annotations))
    if as_json:
        print(json.dumps({"files": report, "errors": total_err,
                          "warnings": total_warn}, ensure_ascii=False, indent=2))
    else:
        print("\nTOTAL: %d error(s), %d warning(s) in %d file(s)"
              % (total_err, total_warn, len(paths)))
    if total_err or (strict and total_warn):
        return 1
    return 0


# -------------------------------------------------------------------- selftest
GOOD_DOC = """\
::ILANG::v5.0
[TYPE:selftest][SCOPE:test][LANG:en]
[LIST:known_repos][DESC:tag_names_may_collide_with_verbs_in_preamble]

::FACT{key:x|value:hello|conf:confirmed}
::GENE{verify_first|conf:confirmed|scope:global}
  T:check_before_execute
  A:blind_execution⇒fatal
  ::PRIOR{completion:assume_incomplete}
    reason_note:one_level_body_ok

::CLAUSE{DEMO|conf:confirmed|scope:test}
T:flush_left_body_binds
A:ignoring_flush_left⇒false_reject
[NOTE] a B5 tag line with trailing text binds too

::MODE{M1|name:EXEC_AUTO}     T:same_line_trailing_body

::JUDGE{v5.0}
V:[int=0.80,cap=0.60,csq=0.70,rel=0.55,cer=0.90,aut=0.75,rev=0.85,evd=0.80,sov=0.95,ine=0.60,ext=0.90]
M:M2|conf:0.87
R:demo

::LIST{@REPOS}
  some/repo → prose line is fine inside LIST

::LESSON{id:l1|type:build|scope:project|conf:confirmed}
  Express middleware order matters.
  [sic] bracket-initial prose is fine inside a prose body

::RULE{proxy_signals⇒insufficient}
  tests pass ≠ complete, annotation prose allowed under RULE

T[0]  ::EVENT{1999|started|major:demo}
      ::FACT{key:y|value:z|conf:confirmed}
T[1]=2001

::PRIORITY{
  a > b > c
}

::MODULE::DEMO{
  [WHAT] a module of tags and prose.
  Free prose is legal here.
}

::UNTRUSTED{id:u1|source:user|role:objective|effects:none|delimiter:EOF_u1}
<<<EOF_u1
::GENE{this_is_opaque_and_must_not_parse}
EOF_u1
::END_UNTRUSTED{id:u1}

::STATE{@SPEC, kind:document}
[READ:@SPEC|src=github.com/x]
  =>[PARS|typ=v5.0]
  =>[Ω]
[BATC:Σ]

::SAY{@USER→@SELF}{hello there}
::EVENT{simple}

::ILANG::v5.0::END
"""

BAD_CASES = [
    ("::WIDGET{x:1}", "E300", "unregistered declaration"),
    ("::GENE{x|conf:confirmed}\n  free prose under gene", "E300", "B6 in non-prose"),
    ("::FACT{key:a|value:@bad_case}", "E300", "entity casing"),
    ("[REED:@GH]=>[Ω]", "E304", "unknown verb in chain"),
    ("[Φ:@GH]=>[Ω]", "E305", "unknown alias in chain"),
    ("::SAY{@A}", "E300", "narrative missing double brace"),
    ("[READ:bareword]", "E300", "bareword target"),
    ("::ILANG::v5.0\n=>[Ω]", "E300", "orphan continuation"),
    ("::GENE{a|conf:c}\n  ::PRIOR{b:c}\n    ::PRIOR{d:e}", "E300", "nesting depth"),
    ("::FOO::BAR{x}", "E300", "two-segment non-MODULE"),
    ("::FACT{key：a|value:b|conf:c}", "E300", "full-width colon separator"),
    ("::FACT{key:a｜value:b}", "E300", "full-width pipe separator"),
    ("::GENE{g|conf:c}\n  =>[Ω]", "E300", "orphan => inside body"),
    ("::ILANG::v5.0 trailing junk\n::FACT{key:a|value:b|conf:c}", "E300",
     "malformed document marker"),
    ("::ILANG::v5.0\n::FACT{key:a|value:b|conf:c}\n::ILANG::MID::MARKER\n"
     "::FACT{key:d|value:e|conf:c}", "E300", "mid-document marker"),
    ("::ILANG::v5.0\n::LESSON{id:x|type:t|scope:s|conf:c}\n  ::SAY{@A}", "E300",
     "nested narrative missing double brace"),
]

BAD_CASES.append(("::ILANG::v5.0\n::FACT{key:a|value:b|conf:c}\n[READ:@GH|frobnicate=1]",
                  "E302", "unknown modifier"))

WARN_CASES = [
    ("::STATE{@SRC, meaning:redefined}", "E202", "tier-1 rebinding candidate"),
]


def cmd_selftest():
    t = []
    lt = Linter("<good>", GOOD_DOC)
    findings = lt.run()
    errs = [f for f in findings if f[0] == ERROR]
    t.append(("good document has zero errors", not errs, errs))
    warns = [f for f in findings if f[0] == WARN]
    t.append(("good document custom-entity SHOULD warn only",
              all(f[2] == "SHOULD" for f in warns), warns))
    for src, code, label in BAD_CASES:
        f = Linter("<bad>", src).run()
        hit = any(lv == ERROR and c == code for lv, _, c, _ in f)
        t.append(("rejects %s (%s)" % (label, code), hit, f))
    for src, code, label in WARN_CASES:
        f = Linter("<warn>", src).run()
        hit = any(lv == WARN and c == code for lv, _, c, _ in f)
        t.append(("warns %s (%s)" % (label, code), hit, f))
    md = "# doc\n\nprose [link](x.md)\n\n```\nDATA I/O: READ WRIT\n```\n\n```\n::FACT{key:a|value:b|conf:confirmed}\n```\n"
    lt2 = Linter("<md>", md)
    f2 = lt2.run()
    t.append(("mixed mode: skips non-ilang fence, lints ilang fence",
              lt2.skipped_fences == 1 and lt2.linted_fences == 1
              and not [x for x in f2 if x[0] == ERROR], f2))
    failed = [(name, det) for name, ok, det in t if not ok]
    for name, ok, _ in t:
        print(("PASS " if ok else "FAIL ") + name)
    if failed:
        for name, det in failed:
            print("\n--- %s ---" % name)
            for item in det:
                print("   ", item)
    print("\n%d/%d passed" % (len(t) - len(failed), len(t)))
    return 1 if failed else 0


def main():
    # findings echo source text (⇒, Greek, CJK); never die on a cp1252 console
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    p = argparse.ArgumentParser(description="I-Lang grammar & registry validator")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--selftest", action="store_true")
    g.add_argument("--lint", nargs="+", metavar="FILE")
    g.add_argument("--canon", metavar="REPO_DIR")
    p.add_argument("--json", action="store_true")
    p.add_argument("--strict", action="store_true")
    a = p.parse_args()
    if a.selftest:
        sys.exit(cmd_selftest())
    if a.lint:
        sys.exit(lint_paths(a.lint, a.json, a.strict))
    if a.canon:
        import os
        paths = [os.path.join(a.canon, f) for f in CANON_FILES]
        sys.exit(lint_paths(paths, a.json, a.strict))


if __name__ == "__main__":
    main()
