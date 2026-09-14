#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checks for the two non-normative JSON Schemas in this directory:
  judge-v5.0.json   JSON form of a ::JUDGE{v5.0} block   (SPEC-v5.0-PRE.md Part II §4)
  status-v4.0.json  JSON form of a ::STATUS{} declaration (SPEC-v4.0-FINAL.md §4)

The text forms stay canonical. This script checks that the schemas agree with them:
  - every example in each schema is valid, and each JUDGE example written back as text
    passes ilang_judge_validator.parse_judge_block with mode == f_v5(v);
  - every ::JUDGE block in SPEC-v5.0-PRE.md that the reference validator accepts is
    valid in its JSON form;
  - for generated vectors (threshold edges plus uniform samples) and all eight modes,
    the reference parser accepts the text block exactly when the schema accepts its JSON
    form, which pins the §4 abstain rule and its 2026-09-14 erratum;
  - every one-line ::STATUS{...} in the code blocks of SPEC-v4.0-FINAL.md is valid in
    its JSON form, and the schema matches a table written independently from the §4
    three-tier authority text for all 720 state/by/authority/reason combinations;
  - named positive and negative cases for both schemas.

JSON Schema validation uses the small draft 2020-12 subset validator below (stdlib only;
it raises on any keyword it does not implement, so nothing is silently skipped).

Regex dialect. JSON Schema patterns are ECMA-262, where `$` matches only at the end of
the string. The validator below gives `$` that meaning by rewriting it to Python's `\\Z`.
Python's own `$` also matches just before a final "\\n", and python-jsonschema hands the
pattern to re.search as written, so a pattern ending in `$` alone would accept "@TASK\\n".
Each such pattern in these schemas therefore sits next to `"not": {"pattern": "\\\\n"}`.
Every check runs twice, once with `$` as `\\Z` (ECMA) and once with Python's `$`, and the
two runs must give identical verdicts.

Usage:
  python schema/check_schemas.py
Exit code 0 when every check passes, 1 otherwise.
"""

import json
import os
import random
import re
import sys
from decimal import Decimal
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import ilang_judge_validator as jv  # noqa: E402

# ------------------------------------------------ JSON Schema 2020-12 subset
ANNOTATIONS = {"$schema", "$id", "$comment", "title", "description", "examples",
               "default", "$defs", "deprecated", "readOnly", "writeOnly"}
SUPPORTED = ANNOTATIONS | {
    "type", "enum", "const", "required", "properties", "additionalProperties",
    "propertyNames", "minLength", "maxLength", "pattern", "minimum", "maximum",
    "exclusiveMinimum", "exclusiveMaximum", "multipleOf", "items", "minItems",
    "maxItems", "uniqueItems", "allOf", "anyOf", "oneOf", "not", "if", "then",
    "else", "$ref", "minProperties", "maxProperties", "dependentRequired"}


class Unsupported(Exception):
    pass


def ecma_to_py(p):
    """Rewrite `$` outside a character class to `\\Z` (ECMA-262 end of input)."""
    out, i, in_class = [], 0, False
    while i < len(p):
        c = p[i]
        if c == "\\" and i + 1 < len(p):
            out.append(p[i:i + 2])
            i += 2
            continue
        if in_class:
            if c == "]":
                in_class = False
        elif c == "[":
            in_class = True
        elif c == "$":
            out.append(r"\Z")
            i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _is_type(x, t):
    if t == "object":
        return isinstance(x, dict)
    if t == "array":
        return isinstance(x, list)
    if t == "string":
        return isinstance(x, str)
    if t == "boolean":
        return isinstance(x, bool)
    if t == "null":
        return x is None
    if t == "number":
        return isinstance(x, (int, float)) and not isinstance(x, bool)
    if t == "integer":
        return ((isinstance(x, int) and not isinstance(x, bool))
                or (isinstance(x, float) and x.is_integer()))
    raise Unsupported("type " + str(t))


def _json_eq(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a == b
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_json_eq(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_json_eq(a[k], b[k]) for k in a)
    return type(a) == type(b) and a == b


def _frac(x):
    return Fraction(Decimal(repr(x))) if isinstance(x, float) else Fraction(x)


class Validator:
    """dollar="ecma": `$` means end of string. dollar="python": pattern as written."""

    def __init__(self, schema, dollar="ecma", multiple_of="exact"):
        if dollar not in ("ecma", "python"):
            raise ValueError("dollar must be ecma or python")
        self.root = schema
        self.dollar = dollar
        self.multiple_of = multiple_of
        self._re = {}

    def _resolve(self, ref):
        if not ref.startswith("#"):
            raise Unsupported("non-local $ref " + ref)
        node = self.root
        for part in [p for p in ref[1:].split("/") if p]:
            part = part.replace("~1", "/").replace("~0", "~")
            node = node[int(part)] if isinstance(node, list) else node[part]
        return node

    def _regex(self, pattern):
        rx = self._re.get(pattern)
        if rx is None:
            src = ecma_to_py(pattern) if self.dollar == "ecma" else pattern
            rx = self._re[pattern] = re.compile(src)
        return rx

    def errors(self, inst, schema=None, ipath="", spath=""):
        if schema is None:
            schema = self.root
        if schema is True:
            return []
        if schema is False:
            return [(ipath or "/", spath or "/", "false schema")]
        for k in schema:
            if k not in SUPPORTED:
                raise Unsupported("keyword " + k)
        errs = []
        e = errs.append
        S = schema
        if "$ref" in S:
            errs += self.errors(inst, self._resolve(S["$ref"]), ipath, spath + "/$ref")
        if "type" in S:
            ts = S["type"] if isinstance(S["type"], list) else [S["type"]]
            if not any(_is_type(inst, t) for t in ts):
                e((ipath, spath + "/type", "not of type %s" % ts))
        if "enum" in S and not any(_json_eq(inst, v) for v in S["enum"]):
            e((ipath, spath + "/enum", "%r not in enum" % (inst,)))
        if "const" in S and not _json_eq(inst, S["const"]):
            e((ipath, spath + "/const", "%r != const %r" % (inst, S["const"])))
        if isinstance(inst, str):
            n = len(inst)                                   # code points
            if "minLength" in S and n < S["minLength"]:
                e((ipath, spath + "/minLength", "length %d < %d" % (n, S["minLength"])))
            if "maxLength" in S and n > S["maxLength"]:
                e((ipath, spath + "/maxLength", "length %d > %d" % (n, S["maxLength"])))
            if "pattern" in S and not self._regex(S["pattern"]).search(inst):
                e((ipath, spath + "/pattern", "%r does not match pattern" % inst[:60]))
        if _is_type(inst, "number"):
            if "minimum" in S and not inst >= S["minimum"]:
                e((ipath, spath + "/minimum", "%r < %r" % (inst, S["minimum"])))
            if "maximum" in S and not inst <= S["maximum"]:
                e((ipath, spath + "/maximum", "%r > %r" % (inst, S["maximum"])))
            if "exclusiveMinimum" in S and not inst > S["exclusiveMinimum"]:
                e((ipath, spath + "/exclusiveMinimum", "%r <= %r" % (inst, S["exclusiveMinimum"])))
            if "exclusiveMaximum" in S and not inst < S["exclusiveMaximum"]:
                e((ipath, spath + "/exclusiveMaximum", "%r >= %r" % (inst, S["exclusiveMaximum"])))
            if "multipleOf" in S:
                d = S["multipleOf"]
                if self.multiple_of == "naive" and isinstance(d, float):
                    q = inst / d
                    try:
                        bad = int(q) != q
                    except OverflowError:
                        bad = (_frac(inst) / _frac(d)).denominator != 1
                else:
                    bad = (_frac(inst) / _frac(d)).denominator != 1
                if bad:
                    e((ipath, spath + "/multipleOf", "%r not a multiple of %r" % (inst, d)))
        if isinstance(inst, list):
            if "minItems" in S and len(inst) < S["minItems"]:
                e((ipath, spath + "/minItems", "too few items"))
            if "maxItems" in S and len(inst) > S["maxItems"]:
                e((ipath, spath + "/maxItems", "too many items"))
            if S.get("uniqueItems"):
                for a in range(len(inst)):
                    for b in range(a + 1, len(inst)):
                        if _json_eq(inst[a], inst[b]):
                            e((ipath, spath + "/uniqueItems", "duplicate items"))
            if "items" in S:
                if isinstance(S["items"], list):
                    raise Unsupported("array-form items (pre-2020-12)")
                for i, it in enumerate(inst):
                    errs += self.errors(it, S["items"], "%s/%d" % (ipath, i), spath + "/items")
        if isinstance(inst, dict):
            for r in S.get("required", []):
                if r not in inst:
                    e((ipath, spath + "/required", "missing %r" % r))
            if "minProperties" in S and len(inst) < S["minProperties"]:
                e((ipath, spath + "/minProperties", "too few properties"))
            if "maxProperties" in S and len(inst) > S["maxProperties"]:
                e((ipath, spath + "/maxProperties", "too many properties"))
            for k, deps in S.get("dependentRequired", {}).items():
                if k in inst:
                    for dname in deps:
                        if dname not in inst:
                            e((ipath, spath + "/dependentRequired", "%r requires %r" % (k, dname)))
            props = S.get("properties", {})
            for k, sub in props.items():
                if k in inst:
                    errs += self.errors(inst[k], sub, ipath + "/" + k, spath + "/properties/" + k)
            if "propertyNames" in S:
                for k in inst:
                    if self.errors(k, S["propertyNames"], ipath, spath + "/propertyNames"):
                        e((ipath, spath + "/propertyNames", "bad property name %r" % k))
            if "additionalProperties" in S:
                for k in inst:
                    if k not in props:
                        sub = S["additionalProperties"]
                        if sub is False:
                            e((ipath + "/" + k, spath + "/additionalProperties",
                               "additional property %r" % k))
                        else:
                            errs += self.errors(inst[k], sub, ipath + "/" + k,
                                                spath + "/additionalProperties")
        for i, sub in enumerate(S.get("allOf", [])):
            errs += self.errors(inst, sub, ipath, "%s/allOf/%d" % (spath, i))
        if "anyOf" in S and not any(not self.errors(inst, sub) for sub in S["anyOf"]):
            e((ipath, spath + "/anyOf", "no anyOf branch matched"))
        if "oneOf" in S:
            n = sum(1 for sub in S["oneOf"] if not self.errors(inst, sub))
            if n != 1:
                e((ipath, spath + "/oneOf", "%d oneOf branches matched" % n))
        if "not" in S and not self.errors(inst, S["not"]):
            e((ipath, spath + "/not", "matched a not schema"))
        if "if" in S:
            if not self.errors(inst, S["if"]):
                if "then" in S:
                    errs += self.errors(inst, S["then"], ipath, spath + "/then")
            elif "else" in S:
                errs += self.errors(inst, S["else"], ipath, spath + "/else")
        return errs

    def is_valid(self, inst):
        return not self.errors(inst)


# ------------------------------------------------------------------ helpers
def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return json.load(f)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def walk(node, path="#"):
    if isinstance(node, dict):
        yield path, node
        for k, v in node.items():
            if k in ("examples", "enum", "const"):
                continue
            yield from walk(v, path + "/" + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, "%s/%d" % (path, i))


def static_problems(schema, expected_id):
    probs = []
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        probs.append("$schema is not draft 2020-12")
    if schema.get("$id") != expected_id:
        probs.append("$id is not " + expected_id)
    if not schema.get("description", "").startswith("Non-normative implementation aid."):
        probs.append("description does not start with 'Non-normative implementation aid.'")
    for path, node in walk(schema):
        if "properties" in path.split("/")[-1:] or path.endswith("/$defs"):
            continue
        for k in node:
            if k not in SUPPORTED and not path.endswith(("/properties", "/$defs")):
                probs.append("unsupported keyword %s at %s" % (k, path))
        if "multipleOf" in node:
            probs.append("multipleOf at " + path)
        pat = node.get("pattern")
        if isinstance(pat, str) and pat.endswith("$") and not pat.endswith("\\$"):
            if node.get("not") != {"pattern": "\\n"} and \
                    (node.get("not") or {}).get("pattern") != "\\n":
                probs.append("pattern ending in $ without a not-newline clause at " + path)
    return probs


class Report:
    def __init__(self):
        self.rows = []

    def add(self, name, ok, detail=""):
        self.rows.append((name, bool(ok), detail))

    def failed(self):
        return [r for r in self.rows if not r[1]]


# ------------------------------------------------------------------- JUDGE
def judge_lines(obj):
    """JSON form -> four text lines (two decimals), or None when not writable."""
    try:
        vals = []
        for d in jv.DIMS:
            x = obj["v"][d]
            if isinstance(x, bool) or float("%.2f" % x) != x:
                return None
            vals.append("%s=%.2f" % (d, x))
        conf = obj["conf"]
        if isinstance(conf, bool) or float("%.2f" % conf) != conf:
            return None
        return [jv.HEADER, "V:[" + ",".join(vals) + "]",
                "M:%s|conf:%.2f" % (obj["mode"], conf), "R:" + obj["reason"]]
    except (KeyError, TypeError, ValueError):
        return None


def validator_json(lines, nxt=""):
    """Reference validator verdict for one block -> JSON form, or None if rejected."""
    try:
        vec, mode, conf, reason = jv.parse_judge_block(lines)
    except ValueError:
        return None
    s = nxt.strip()
    if jv.EXTRA_FIELD.match(s) and not s.startswith("::"):
        return None
    return {"judge": "v5.0", "v": {d: vec[d] for d in jv.DIMS},
            "mode": mode, "conf": conf, "reason": reason}


def judge_named_cases():
    base = {"judge": "v5.0",
            "v": {"int": 0.80, "cap": 0.60, "csq": 0.70, "rel": 0.55, "cer": 0.90, "aut": 0.75,
                  "rev": 0.85, "evd": 0.80, "sov": 0.95, "ine": 0.60, "ext": 0.90},
            "mode": "M2", "conf": 0.87,
            "reason": "authorized_config_change_reversible_audit_trail_kept"}

    def mk(mode=None, drop=None, extra=None, **kw):
        o = json.loads(json.dumps(base))
        for k, val in kw.items():
            if k in jv.DIMS:
                o["v"][k] = val
            else:
                o[k] = val
        if mode:
            o["mode"] = mode
        if drop:
            o["v"].pop(drop)
        if extra:
            o.update(extra)
        return o

    v_extra = mk()
    v_extra["v"]["drift"] = 0.5
    return [
        ("§4 example", mk(), True),
        ("vector value 1.01", mk(int=1.01), False),
        ("vector value -0.01", mk(int=-0.01), False),
        ("vector value as a string", mk(int="0.80"), False),
        ("missing dimension ext", mk(drop="ext"), False),
        ("extra dimension", v_extra, False),
        ("extra top-level property", mk(extra={"note": "x"}), False),
        ("mode M9", mk(mode="M9"), False),
        ("judge v5", mk(judge="v5"), False),
        ("conf 1.5", mk(conf=1.5), False),
        ("reason empty", mk(reason=""), False),
        ("reason 121 characters", mk(reason="x" * 121), False),
        ("reason 120 characters", mk(reason="x" * 120), True),
        ("reason ends in a newline", mk(reason="abc\n"), False),
        ("reason ends in a space", mk(reason="abc "), False),
        ("reason holds U+2028", mk(reason="a b"), False),
        ("reason starts with a space", mk(reason=" abc"), True),
        ("epistemic gate cer 0.29, mode M2", mk(cer=0.29), False),
        ("epistemic gate evd 0.24, mode M5", mk(evd=0.24, mode="M5"), True),
        ("cer 0.30 is outside the gate, mode M2", mk(cer=0.30), True),
        ("both gates (sov 0.10, cer 0.20), mode M8", mk(sov=0.10, cer=0.20, mode="M8"), True),
        ("both gates (sov 0.10, cer 0.20), mode M5", mk(sov=0.10, cer=0.20, mode="M5"), True),
        ("both gates (sov 0.10, cer 0.20), mode M2", mk(sov=0.10, cer=0.20), False),
        ("both gates (ext 0.05, evd 0.10), mode M8", mk(ext=0.05, evd=0.10, mode="M8"), True),
        ("both gates (csq 0.05 and rev 0.10, cer 0.20), mode M8",
         mk(csq=0.05, rev=0.10, cer=0.20, mode="M8"), True),
        ("csq 0.05 without rev < 0.20 is no survival hit, gate on, mode M8",
         mk(csq=0.05, cer=0.20, mode="M8"), False),
        ("epistemic gate without a survival hit, mode M8", mk(cer=0.20, mode="M8"), False),
        ("mode differs from f_v5 (M1) is not a schema error", mk(mode="M1"), True),
    ]


def edge_and_uniform_vectors(n_uniform=1500, seed=42):
    edges = {"sov": (0.14, 0.15), "ext": (0.09, 0.10), "csq": (0.09, 0.10),
             "rev": (0.19, 0.20), "cer": (0.29, 0.30), "evd": (0.24, 0.25)}
    keys = sorted(edges)
    out = []
    for mask in range(1 << len(keys)):
        v = {d: 0.95 for d in jv.DIMS}
        for i, k in enumerate(keys):
            v[k] = edges[k][(mask >> i) & 1]
        out.append(v)
    rng = random.Random(seed)
    for _ in range(n_uniform):
        out.append({d: round(rng.random(), 2) for d in jv.DIMS})
    return out


def check_judge(rep, schema, dollar, verdicts):
    val = Validator(schema, dollar=dollar)
    tag = "[%s] " % dollar

    # thresholds and closed sets mirror the reference validator
    gate = schema["$defs"]["epistemic_gate"]["anyOf"]
    surv = schema["$defs"]["survival_hit"]["anyOf"]
    consts_ok = (
        gate[0]["properties"]["cer"]["exclusiveMaximum"] == jv.TH["cer_gate"]
        and gate[1]["properties"]["evd"]["exclusiveMaximum"] == jv.TH["evd_gate"]
        and surv[0]["properties"]["sov"]["exclusiveMaximum"] == jv.TH["sov_survival"]
        and surv[1]["properties"]["ext"]["exclusiveMaximum"] == jv.TH["ext_survival"]
        and surv[2]["properties"]["csq"]["exclusiveMaximum"] == jv.TH["csq_survival"]
        and surv[2]["properties"]["rev"]["exclusiveMaximum"] == jv.TH["rev_survival"]
        and schema["properties"]["mode"]["enum"] == sorted(jv.MODES)
        and schema["$defs"]["vector"]["required"] == jv.DIMS)
    rep.add(tag + "JUDGE thresholds, modes and dimension order match ilang_judge_validator.py",
            consts_ok)

    # schema examples
    bad = []
    for i, ex in enumerate(schema.get("examples", [])):
        lines = judge_lines(ex)
        back = validator_json(lines) if lines else None
        ok = (val.is_valid(ex) and back is not None and back == ex
              and jv.f_v5(ex["v"]) == ex["mode"])
        verdicts.append(("judge example %d" % i, ok))
        if not ok:
            bad.append(i)
    rep.add(tag + "JUDGE examples are valid and pass the reference validator with mode == f_v5",
            not bad and schema.get("examples"), "bad: %s" % bad if bad else
            "%d examples" % len(schema.get("examples", [])))

    # ::JUDGE blocks in the spec
    blocks = jv.extract_blocks(read("SPEC-v5.0-PRE.md"))
    accepted = rejected_by_schema = 0
    for n, (b, nxt) in enumerate(blocks, 1):
        obj = validator_json(b, nxt)
        if obj is None:
            continue
        accepted += 1
        ok = val.is_valid(obj)
        verdicts.append(("spec judge block %d" % n, ok))
        rejected_by_schema += not ok
    rep.add(tag + "every ::JUDGE block in SPEC-v5.0-PRE.md accepted by the validator is "
                  "schema-valid", accepted > 0 and rejected_by_schema == 0,
            "blocks=%d accepted=%d schema_rejects=%d" % (len(blocks), accepted, rejected_by_schema))

    # parser vs schema on the mode rule
    vectors = edge_and_uniform_vectors()
    both = acc_rej = rej_acc = conflicts = 0
    for k, v in enumerate(vectors):
        gate_on = v["cer"] < jv.TH["cer_gate"] or v["evd"] < jv.TH["evd_gate"]
        conflicts += gate_on and jv.f_v5(v) == "M8"
        for mode in sorted(jv.MODES):
            obj = {"judge": "v5.0", "v": dict(v), "mode": mode, "conf": 0.80, "reason": "check"}
            t_ok = validator_json(judge_lines(obj)) is not None
            s_ok = val.is_valid(obj)
            verdicts.append(("vector %d %s" % (k, mode), s_ok))
            both += t_ok == s_ok
            acc_rej += t_ok and not s_ok
            rej_acc += s_ok and not t_ok
    total = len(vectors) * len(jv.MODES)
    rep.add(tag + "reference parser and schema agree on %d vector/mode pairs "
                  "(including the survival plus epistemic gate cases)" % total,
            both == total and conflicts > 0,
            "agree=%d validator_accepts_schema_rejects=%d validator_rejects_schema_accepts=%d "
            "both_gate_vectors_with_f_v5_M8=%d" % (both, acc_rej, rej_acc, conflicts))

    # named JSON cases
    wrong = []
    for name, obj, expect in judge_named_cases():
        got = val.is_valid(obj)
        verdicts.append(("judge case " + name, got))
        if got != expect:
            wrong.append(name)
    rep.add(tag + "JUDGE named JSON cases", not wrong,
            "unexpected: %s" % wrong if wrong else "%d cases" % len(judge_named_cases()))


# ------------------------------------------------------------------ STATUS
NUMBER = re.compile(r"^-?[0-9]+(?:\.[0-9]+)?$")


def status_json(decl):
    """One-line ::STATUS{a|k:v|...} with no nested braces -> JSON form (SPEC.md §2.3/§2.4)."""
    m = re.match(r"^::STATUS\{([^{}]*)\}$", decl.strip())
    if not m:
        raise ValueError("not a one-line ::STATUS{...}")
    segs = m.group(1).split("|")
    obj = {}
    if segs and segs[0].startswith("@") and ":" not in segs[0]:
        obj["target"] = segs.pop(0)
    for seg in segs:
        key, sep, value = seg.partition(":")
        if not sep or not key or key in obj:
            raise ValueError("bad field %r" % seg)
        if NUMBER.match(value):
            value = float(value) if "." in value else int(value)
        elif value in ("true", "false"):
            value = value == "true"
        obj[key] = value
    return obj


def spec_status_lines(rel):
    out, fenced = [], False
    for n, line in enumerate(read(rel).splitlines(), 1):
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if fenced and line.strip().startswith("::STATUS{") and line.strip().endswith("}"):
            out.append((n, line.strip()))
    return out


TIER = {"@AGENT": "proposal", "@SELF": "proposal", "@GRADER": "verification", "@RUNTIME": "commit"}
CAN_WRITE = {"proposal": {"claimed_complete", "stopped", "blocked", "failed", "needs_revision"},
             "verification": {"verified_complete", "needs_revision"},
             "commit": {"complete", "running", "stopped"}}


def status_table(state, by, authority, reason):
    """SPEC-v4.0-FINAL.md §4, written independently of the schema."""
    if by in TIER and authority is not None and TIER[by] != authority:
        return False
    if authority is not None and state is not None and state not in CAN_WRITE[authority]:
        return False
    if state == "created":                                  # no tier can write it
        return False
    if state in ("complete", "running") and (by != "@RUNTIME" or authority != "commit"):
        return False
    if reason == "budget" and state is not None and state != "stopped":
        return False
    return True


def status_named_cases():
    return [
        ("SPEC-v4.0-FINAL.md §0 prose form {by:@SELF, authority:proposal}",
         {"by": "@SELF", "authority": "proposal"}, True),
        ("SPEC-v4.0-FINAL.md §2 prose form {state:stopped, reason:budget}",
         {"state": "stopped", "reason": "budget"}, True),
        ("SPEC-v4.0-FINAL.md §0.1 table form {authority:commit}", {"authority": "commit"}, True),
        ("SPEC-v5.0-PRE.md prose form {by:@RUNTIME}", {"by": "@RUNTIME"}, True),
        ("score as a word", {"state": "needs_revision", "score": "high", "by": "@GRADER",
                             "authority": "verification"}, True),
        ("score 78", {"state": "needs_revision", "score": 78, "by": "@GRADER",
                      "authority": "verification"}, True),
        ("missing as a list", {"state": "needs_revision", "missing": ["d3", "d4"],
                               "by": "@GRADER", "authority": "verification"}, True),
        ("unknown lowercase key is kept", {"state": "blocked", "ticket": "T-9", "by": "@AGENT",
                                           "authority": "proposal"}, True),
        ("custom entity with verification writes verified_complete",
         {"state": "verified_complete", "by": "@AGENT_C", "authority": "verification"}, True),
        ("running by @AGENT with proposal", {"state": "running", "by": "@AGENT",
                                             "authority": "proposal"}, False),
        ("running by a custom entity with commit", {"state": "running", "by": "@ORCHESTRATOR",
                                                    "authority": "commit"}, False),
        ("running without by", {"state": "running", "authority": "commit"}, False),
        ("running by @RUNTIME without authority", {"state": "running", "by": "@RUNTIME"}, False),
        ("created by @RUNTIME with commit", {"state": "created", "by": "@RUNTIME",
                                             "authority": "commit"}, False),
        ("created with no writer", {"state": "created"}, False),
        ("complete by @GRADER with verification", {"state": "complete", "by": "@GRADER",
                                                   "authority": "verification"}, False),
        ("complete by @RUNTIME without authority", {"state": "complete", "by": "@RUNTIME"}, False),
        ("verified_complete with proposal", {"state": "verified_complete", "by": "@SELF",
                                             "authority": "proposal"}, False),
        ("@GRADER with commit", {"state": "stopped", "by": "@GRADER", "authority": "commit"}, False),
        ("@AGENT with verification", {"state": "needs_revision", "by": "@AGENT",
                                      "authority": "verification"}, False),
        ("reason budget with state complete", {"state": "complete", "reason": "budget",
                                               "by": "@RUNTIME", "authority": "commit"}, False),
        ("reason budget with state running", {"state": "running", "reason": "budget",
                                              "by": "@RUNTIME", "authority": "commit"}, False),
        ("state not in the state machine", {"state": "in_progress", "by": "@AGENT",
                                            "authority": "proposal"}, False),
        ("authority not a tier", {"state": "stopped", "by": "@AGENT", "authority": "admin"}, False),
        ("uppercase field key", {"State": "blocked", "by": "@AGENT", "authority": "proposal"}, False),
        ("entity in lowercase", {"target": "@task", "state": "blocked", "by": "@AGENT",
                                 "authority": "proposal"}, False),
        ("entity ending in a newline", {"target": "@TASK\n", "state": "blocked", "by": "@AGENT",
                                        "authority": "proposal"}, False),
        ("field key ending in a newline", {"state\n": "blocked"}, False),
        ("null value", {"state": "blocked", "need": None, "by": "@AGENT",
                        "authority": "proposal"}, False),
    ]


def check_status(rep, schema, dollar, verdicts):
    val = Validator(schema, dollar=dollar)
    tag = "[%s] " % dollar

    exs = schema.get("examples", [])
    bad = [i for i, ex in enumerate(exs) if not val.is_valid(ex)]
    verdicts.extend(("status example %d" % i, i not in bad) for i in range(len(exs)))
    rep.add(tag + "STATUS examples are valid", exs and not bad,
            "bad: %s" % bad if bad else "%d examples" % len(exs))

    lines = spec_status_lines("SPEC-v4.0-FINAL.md")
    bad = []
    for n, decl in lines:
        try:
            ok = val.is_valid(status_json(decl))
        except ValueError:
            ok = False
        verdicts.append(("spec status line %d" % n, ok))
        if not ok:
            bad.append(n)
    rep.add(tag + "every one-line ::STATUS in the code blocks of SPEC-v4.0-FINAL.md is valid",
            len(lines) >= 11 and not bad,
            "lines=%d bad=%s" % (len(lines), bad))

    states = schema["properties"]["state"]["enum"] + [None]
    bys = ["@AGENT", "@SELF", "@GRADER", "@RUNTIME", "@AGENT_B", None]
    auths = ["proposal", "verification", "commit", None]
    reasons = ["budget", "user_pause", None]
    n = mism = 0
    first = []
    for st in states:
        for by in bys:
            for au in auths:
                for rs in reasons:
                    obj = {k: v for k, v in (("state", st), ("by", by), ("authority", au),
                                             ("reason", rs)) if v is not None}
                    got = val.is_valid(obj)
                    verdicts.append(("status combo %s" % obj, got))
                    n += 1
                    if got != status_table(st, by, au, rs):
                        mism += 1
                        first.append(obj)
    rep.add(tag + "STATUS schema matches the §4 authority table for %d combinations" % n,
            mism == 0, "mismatches=%d %s" % (mism, first[:3]))

    wrong = []
    for name, obj, expect in status_named_cases():
        got = val.is_valid(obj)
        verdicts.append(("status case " + name, got))
        if got != expect:
            wrong.append(name)
    rep.add(tag + "STATUS named JSON cases", not wrong,
            "unexpected: %s" % wrong if wrong else "%d cases" % len(status_named_cases()))


# --------------------------------------------------------------------- main
def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    rep = Report()
    judge = load("judge-v5.0.json")
    status = load("status-v4.0.json")
    for schema, sid in ((judge, "https://ilang.ai/schema/judge-v5.0.json"),
                        (status, "https://ilang.ai/schema/status-v4.0.json")):
        probs = static_problems(schema, sid)
        rep.add("%s: metadata, supported keywords, no multipleOf, $ patterns guarded"
                % sid.rsplit("/", 1)[1], not probs, "; ".join(probs))
    runs = {}
    for dollar in ("ecma", "python"):
        verdicts = []
        try:
            check_judge(rep, judge, dollar, verdicts)
            check_status(rep, status, dollar, verdicts)
        except Unsupported as exc:
            rep.add("[%s] validator supports every keyword used" % dollar, False, str(exc))
        runs[dollar] = verdicts
    diff = [a[0] for a, b in zip(runs["ecma"], runs["python"]) if a != b]
    same_len = len(runs["ecma"]) == len(runs["python"])
    rep.add("ECMA `$` and Python `$` give identical verdicts on all %d instances"
            % len(runs["ecma"]), same_len and not diff, "differ: %s" % diff[:5])
    for name, ok, detail in rep.rows:
        print(("PASS " if ok else "FAIL ") + name + (" (%s)" % detail if detail else ""))
    failed = rep.failed()
    print("\n%d/%d passed" % (len(rep.rows) - len(failed), len(rep.rows)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
