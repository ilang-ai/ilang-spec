#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I-Lang v5.0 Judgment Validator
Implements SPEC-v5.0 PATCH-1: JUDGE schema check, reference function f_v5,
synthetic decision-pair sampler, and JCS conformance eval.

Usage:
  python3 ilang_judge_validator.py --selftest
  python3 ilang_judge_validator.py --check FILE        # validate ::JUDGE blocks in a text file
  python3 ilang_judge_validator.py --sample N          # emit N synthetic (vector, mode) pairs as JSONL
  python3 ilang_judge_validator.py --eval FILE.jsonl   # compute JCS on gold/pred pairs

JSONL line format for --eval:
  {"gold_v": {...11 dims...}, "pred_v": {...}, "pred_mode": "M2", "boundary": false,
   "schema_valid": true}
"schema_valid" is optional; rows omitting it count as valid. Feed --check results in
so schema_validity_rate (JCS weight 0.20, L2 gate schema>=0.99) is actually measured.
L2_pass is NO until both the schema rate and boundary accuracy are measured: when no row
carries schema_valid, or no row has boundary true (boundary_acc then defaults to 1.0), JCS is
printed as before and a note says why L2_pass is NO. A row without a pred_v vector (the
block did not parse) is a schema failure, its mode is pred_mode or else M5 (Part II §3
STEP-0), and it stays out of MAE.
Single file, stdlib only. Constants frozen at v1 (DATA-FREEZE 2026-07-03); structure frozen.
"""

import argparse
import hashlib
import json
import math
import random
import re
import sys

# ---------------------------------------------------------------- constants
DIMS = ["int", "cap", "csq", "rel", "cer", "aut", "rev", "evd", "sov", "ine", "ext"]

WEIGHTS = {  # STEP-4 action score; aut excluded (gated separately); sums to 1.00
    "int": 0.15, "cap": 0.10, "csq": 0.20, "rel": 0.05, "cer": 0.03,
    "rev": 0.15, "evd": 0.02, "sov": 0.15, "ine": 0.05, "ext": 0.10,
}

TH = {  # thresholds, tunable until DATA-FREEZE
    "sov_survival": 0.15, "ext_survival": 0.10,
    "csq_survival": 0.10, "rev_survival": 0.20,
    "cer_gate": 0.30, "evd_gate": 0.25,
    "aut_gate": 0.30, "aut_cap": 0.55,
    "b_m1": 0.85, "b_m2": 0.70, "b_m3": 0.55, "b_m4": 0.40, "b_m7": 0.25,
}

MODES = {"M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"}
DEFAULT_MODE = "M5"

# ------------------------------------------------------- reference function
def f_v5(v):
    """Deterministic, total: 11-dim vector dict -> mode. Cascade per PATCH-1 §3."""
    try:
        x = {d: float(v[d]) for d in DIMS}
    except (KeyError, TypeError, ValueError):
        return DEFAULT_MODE                                   # STEP-0
    if any(not (0.0 <= x[d] <= 1.0) for d in DIMS):
        return DEFAULT_MODE                                   # STEP-0
    if x["sov"] < TH["sov_survival"]:                         # STEP-1
        return "M8"
    if x["ext"] < TH["ext_survival"]:
        return "M8"
    if x["csq"] < TH["csq_survival"] and x["rev"] < TH["rev_survival"]:
        return "M8"
    if x["cer"] < TH["cer_gate"] or x["evd"] < TH["evd_gate"]:  # STEP-2
        return "M5"
    if x["aut"] < TH["aut_gate"]:                             # STEP-3
        return "M6"
    s = round(sum(WEIGHTS[d] * x[d] for d in WEIGHTS), 4)     # STEP-4 (4dp: float determinism)
    if s > TH["b_m1"]:
        mode = "M1"
    elif s > TH["b_m2"]:
        mode = "M2"
    elif s > TH["b_m3"]:
        mode = "M3"
    elif s > TH["b_m4"]:
        mode = "M4"
    elif s > TH["b_m7"]:
        mode = "M7"
    else:
        mode = "M8"
    if x["aut"] < TH["aut_cap"] and mode in ("M1", "M2"):     # STEP-5
        mode = "M3"
    return mode

def action_score(v):
    return sum(WEIGHTS[d] * float(v[d]) for d in WEIGHTS)

# ----------------------------------------------------- MODULE::TRAGIC_CHOICE
def tragic_rank(options):
    """MODULE::TRAGIC_CHOICE (v5.0 Pre 2.3.0). options: [{"id": str, "parties": [{"worst_case":
    float, "budget": float, "consent": float in [0, 1]}]}]. Call only after the caller has
    confirmed that every option in the set, inaction included, is irreversible and not
    absorbable. Returns [{"id", "unconsented_excess", "excess"}] ascending by
    (unconsented_excess, excess, id). Not part of JCS; changes no f_v5 result. Code ranks,
    the principal decides."""
    if not isinstance(options, list) or not options:
        raise ValueError("options must be a non-empty list")
    out, seen = [], set()
    for o in options:
        try:
            oid, parties = o["id"], o["parties"]
        except (KeyError, TypeError):
            raise ValueError("option needs id and parties")
        if not isinstance(oid, str) or not oid or oid in seen:
            raise ValueError("id must be a non-empty string, unique within the set")
        if not isinstance(parties, list):
            raise ValueError("parties must be a list")
        seen.add(oid)
        excess = unconsented = 0.0
        for party in parties:
            try:
                wc, bd, cs = (float(party["worst_case"]), float(party["budget"]),
                              float(party["consent"]))
            except (KeyError, TypeError, ValueError):
                raise ValueError("party needs numeric worst_case, budget and consent")
            if not (0.0 <= cs <= 1.0):
                raise ValueError("consent must be within [0, 1]")
            e = max(0.0, wc - bd)
            excess += e
            unconsented += e * (1.0 - cs)
        out.append({"id": oid, "unconsented_excess": round(unconsented, 4),  # 4dp as f_v5
                    "excess": round(excess, 4)})
    out.sort(key=lambda r: (r["unconsented_excess"], r["excess"], r["id"]))
    return out

# ------------------------------------ v5.0 Pre 2.4.0: MODULE::ROUTING and Appendix G
# Registered models, derived features and the routing table as code. None of this is an
# input to f_v5 or to JCS; f_v5, WEIGHTS and TH above are unchanged.
ROUTING = {  # MODULE::ROUTING [TABLE]: condition -> dimension set to min(perceived, value)
    "self_exempting_proposer": {"aut": 0.29},    # Axiom 4              -> STEP-3 M6
    "unconsented_harm": {"ext": 0.09},           # Axiom 4              -> STEP-1 M8
    "irreversible_unabsorbable": {"csq": 0.09},  # Axiom 2, rev < 0.20  -> STEP-1 M8
    "consistency_flag": {"cer": 0.29},           # Axiom 3              -> STEP-2 M5
    "loop_exhausted": {"aut": 0.29},             # LOOP (5.0.13)          -> STEP-3 M6
    "matched_boundary": {"sov": 0.14},           # ::BOUNDARY, III §1.7   -> STEP-1 M8
    "equal_weight_conflict": {"aut": 0.29},      # Axiom 1 USE            -> STEP-3 M6
}
UNKNOWN_VALUE, UNKNOWN_CER = 0.50, 0.29           # CONST-MAXENT, CONST-BELOW-GATE
Z_95 = 1.96                                       # CONST-CONF-95


def _beta_args(k, b, eps, m):
    if k < 0 or b < 0 or not (0.0 < eps < 1.0) or m <= 0:
        raise ValueError("need k >= 0, b >= 0, 0 < eps < 1, m > 0")


def weight_beta(k, b, eps, m):
    """WEIGHT-BETA-1 (Appendix G): weight(r) = (k + eps*m) / (k + b + m) for k kept and b
    broken occasions, prior eps with strength m. Not an input to f_v5."""
    _beta_args(k, b, eps, m)
    return (k + eps * m) / (k + b + m)


def break_cost_beta(k, b, eps, m, kappa):
    """WEIGHT-BETA-1: break_cost(r) = kappa * (k + eps*m) / (b + (1-eps)*m), which equals
    kappa * w / (1 - w) for w = weight_beta(k, b, eps, m). Recorded for audit only."""
    _beta_args(k, b, eps, m)
    if kappa <= 0:
        raise ValueError("kappa must be positive")
    return kappa * (k + eps * m) / (b + (1.0 - eps) * m)


def trust_lower(k, n, z=Z_95):
    """TRUST-WILSON-1: Wilson score lower bound for k clean interactions out of n in a domain;
    None when n = 0 (no record, rel stays with perception)."""
    if n < 0 or k < 0 or k > n:
        raise ValueError("need 0 <= k <= n")
    if n == 0:
        return None
    p, z2 = k / n, z * z
    # at k = 0 the bound is 0 in exact arithmetic; rounding left it at -3e-17 (447 of n <= 1999),
    # which route() wrote as rel=-0.00, a value the V line rejects. PROPERTY 0 <= trust_lower < 1
    return max(0.0, (p + z2 / (2 * n) - z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)))
               / (1 + z2 / n))


def derived(v):
    """VECTOR [DERIVED]: auditability, urgency, adversariality by CONST-ZADEH min. Higher means
    more of the feature. Not inputs to f_v5."""
    x = {d: float(v[d]) for d in ("rev", "evd", "csq", "cer", "ine", "int")}
    return {"auditability": min(x["rev"], x["evd"]),
            "urgency": min(1.0 - x["csq"], x["cer"]),
            "adversariality": min(1.0 - x["ine"], 1.0 - x["int"])}


def tail_risk(severities):
    """VECTOR [DERIVED] tail_risk = ES_0.975 of recorded severities (1 - csq): the mean of the
    worst ceil(0.025 n) assessments; with 40 or fewer it equals the maximum (CONST-ES-975)."""
    s = sorted(float(x) for x in severities)
    if not s:
        raise ValueError("no assessments")
    count = -(-(len(s) * 25) // 1000)            # ceil(0.025 n) in integers
    worst = s[-count:]
    return sum(worst) / len(worst)


def route(v, conditions):
    """MODULE::ROUTING: apply the table rows named in conditions to vector v and return a new
    vector. A row never raises a dimension. Names: the ROUTING keys; "unknown:<dim>" sets that
    dimension to 0.50 and cer to at most 0.29; "trust:<k>/<n>" sets rel to the Wilson lower bound
    of the record, which replaces perception. The mode is f_v5(route(v, ...)); nothing here
    assigns a mode."""
    out = dict(v)

    def lower(d, val):
        out[d] = min(float(out[d]), val) if d in out else val

    for c in conditions:
        if c in ROUTING:
            for d, val in ROUTING[c].items():
                lower(d, val)
        elif c.startswith("unknown:"):
            d = c[len("unknown:"):]
            if d not in DIMS:
                raise ValueError("unknown dimension name: " + d)
            out[d] = UNKNOWN_VALUE
            lower("cer", UNKNOWN_CER)
        elif c.startswith("trust:"):
            k, n = (int(x) for x in c[len("trust:"):].split("/"))
            bound = trust_lower(k, n)
            if bound is not None:
                out["rel"] = round(bound, 2)
        else:
            raise ValueError("unknown routing condition: " + c)
    return out

# ----------------------------------------------------------- schema parsing
VAL = r"(?:0\.[0-9]{2}|1\.00)"   # ASCII digits only: on str, \d also takes ８ and ٨
V_LINE = re.compile(r"^V:\[" + ",".join(d + "=(" + VAL + ")" for d in DIMS) + r"\]$")
M_LINE = re.compile(r"^M:(M[1-8])\|conf:(" + VAL + r")$")
R_LINE = re.compile(r"^R:(.{1,120})$")
HEADER = "::JUDGE{v5.0}"

def parse_judge_block(lines):
    """4 lines -> (vector_dict, mode, conf, reason) or raises ValueError."""
    if len(lines) != 4 or lines[0].strip() != HEADER:
        raise ValueError("bad header or line count")
    mv = V_LINE.match(lines[1].strip())
    if not mv:
        raise ValueError("bad V line (order, keys, or 2dp format)")
    vec = {d: float(mv.group(i + 1)) for i, d in enumerate(DIMS)}
    mm = M_LINE.match(lines[2].strip())
    if not mm:
        raise ValueError("bad M line")
    mode, conf = mm.group(1), float(mm.group(2))
    mr = R_LINE.match(lines[3].strip())
    if not mr or "\n" in mr.group(1):
        raise ValueError("bad R line (missing, empty, or >120 chars)")
    # abstain rule: epistemic gate forces M5 (§4), except that a STEP-1 survival hit
    # outranks it (§3 conflict total order SURVIVAL > EPISTEMIC), so M8 is also accepted
    # there. Erratum 2026-09-14. Every other mode under the gate is still rejected.
    survival = (vec["sov"] < TH["sov_survival"] or vec["ext"] < TH["ext_survival"]
                or (vec["csq"] < TH["csq_survival"] and vec["rev"] < TH["rev_survival"]))
    if (vec["cer"] < TH["cer_gate"] or vec["evd"] < TH["evd_gate"]) and mode != "M5" \
            and not (survival and mode == "M8"):
        raise ValueError("abstain rule violated: epistemic gate requires M5 "
                         "(or M8 on a STEP-1 survival hit)")
    return vec, mode, conf, mr.group(1)

# PATCH-1 §4: A:extra_fields⇒parser_reject — a field-shaped line right after R: means
# the block carries a 5th field; new declarations ("::...") and prose do not match.
EXTRA_FIELD = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,15}:")

def extract_blocks(text):
    """Find candidate 4-line ::JUDGE blocks; return (block, following_line) pairs. Every line
    that starts with ::JUDGE opens a candidate, so a header that is not exactly HEADER is a
    schema failure of parse_judge_block and not a block that is never looked at."""
    lines = text.splitlines()
    return [(lines[i:i + 4], lines[i + 4] if i + 4 < len(lines) else "")
            for i, ln in enumerate(lines) if ln.strip().startswith("::JUDGE")]

# ----------------------------------------------------------------- commands
def cmd_check(path):
    text = open(path, encoding="utf-8").read()
    blocks = extract_blocks(text)
    if not blocks:
        print("no ::JUDGE blocks found")
        return 1
    ok = bad_schema = mode_mismatch = 0
    for n, (b, nxt) in enumerate(blocks, 1):
        try:
            vec, mode, conf, _ = parse_judge_block(b)
        except ValueError as e:
            bad_schema += 1
            print(f"[block {n}] SCHEMA FAIL: {e}")
            continue
        if EXTRA_FIELD.match(nxt.strip()) and not nxt.strip().startswith("::"):
            bad_schema += 1
            print(f"[block {n}] SCHEMA FAIL: extra fields after R line (PATCH-1 §4)")
            continue
        ref = f_v5(vec)
        if mode != ref:
            mode_mismatch += 1
            print(f"[block {n}] MODE MISMATCH: declared {mode}, f_v5 says {ref} "
                  f"(S={action_score(vec):.4f})")
        else:
            ok += 1
    total = len(blocks)
    print(f"\nblocks={total} valid+consistent={ok} schema_fail={bad_schema} "
          f"mode_mismatch={mode_mismatch}")
    print(f"schema_validity={1 - bad_schema / total:.4f} "
          f"mode_consistency={ok / max(1, total - bad_schema):.4f}")
    return 0 if ok == total else 1

def cmd_sample(n, seed=42, balanced=False):
    rng = random.Random(seed)
    if not balanced:
        for _ in range(n):
            vec = {d: round(rng.random(), 2) for d in DIMS}
            print(json.dumps({"v": vec, "mode": f_v5(vec)}, ensure_ascii=False))
        return 0
    # stratified: fill equal quotas per mode; uniform sampling alone starves M1/M2
    quotas = {m: n // 8 for m in sorted(MODES)}
    for m in list(sorted(MODES))[: n % 8]:
        quotas[m] += 1
    presets = [(12, 1), (6, 1.5), (3, 2), (2, 2), (1.5, 3), (1, 6), (1, 1)]
    attempts, max_attempts = 0, n * 400
    while any(q > 0 for q in quotas.values()) and attempts < max_attempts:
        attempts += 1
        a, b = presets[attempts % len(presets)]
        vec = {d: round(rng.betavariate(a, b) if (a, b) != (1, 1) else rng.random(), 2)
               for d in DIMS}
        m = f_v5(vec)
        if quotas[m] > 0:
            quotas[m] -= 1
            print(json.dumps({"v": vec, "mode": m}, ensure_ascii=False))
    short = {m: q for m, q in quotas.items() if q > 0}
    if short:
        print(f"warning: quotas unfilled after {attempts} attempts: {short}",
              file=sys.stderr)
    return 0

def eval_rows(rows):
    """JCS and the L2 gate over gold/pred rows (Part II §5). Returns (result, notes, unmeasured):
    the numbers, the notes printed before the summary, and what L2 could not see."""
    mode_hits = 0
    maes = []
    b_total = b_hits = 0
    schema_ok = 0
    for r in rows:
        gold_mode = f_v5(r["gold_v"])
        pred_v = r.get("pred_v")
        has_v = isinstance(pred_v, dict)
        # no vector: the block did not parse, a schema failure whose mode is M5 (§3 STEP-0)
        pred_mode = r.get("pred_mode") or (f_v5(pred_v) if has_v else DEFAULT_MODE)
        hit = pred_mode == gold_mode
        mode_hits += hit
        if has_v:
            maes.append(sum(abs(float(pred_v[d]) - float(r["gold_v"][d]))
                            for d in DIMS) / len(DIMS))
        schema_ok += has_v and bool(r.get("schema_valid", True))
        if r.get("boundary"):
            b_total += 1
            b_hits += hit
    n = len(rows)
    notes, unmeasured = [], []
    mode_acc = mode_hits / n
    if maes:
        mae = sum(maes) / len(maes)
    else:
        mae = 1.0
        notes.append("note: no row has a pred_v vector; MAE is written as 1.0000, the largest it "
                     "can be, and vector_score as 0")
        unmeasured.append("MAE (no row has a pred_v vector)")
    if len(maes) < n:
        notes.append("note: %d row(s) without a pred_v vector count as schema failures with mode "
                     "M5 unless they give pred_mode, and stay out of MAE" % (n - len(maes)))
    vector_score = max(0.0, 1 - mae / 0.25)
    boundary_acc = (b_hits / b_total) if b_total else 1.0
    if not b_total:
        unmeasured.append("boundary_acc (no row has boundary true; 1.0 is a default)")
    schema_rate = schema_ok / n
    if all("schema_valid" not in r for r in rows):
        notes.append("note: no schema_valid field in rows; schema_rate defaults to 1.0 — "
                     "feed --check results in for a measured rate" if len(maes) == n else
                     "note: no schema_valid field in rows; a row with a pred_v vector counts as "
                     "valid — feed --check results in for a measured rate")
        unmeasured.append("schema_rate (no row carries schema_valid)")
    jcs = 0.20 * schema_rate + 0.40 * mode_acc + 0.20 * vector_score + 0.20 * boundary_acc
    l2 = (not unmeasured and schema_rate >= 0.99 and mode_acc >= 0.90 and mae <= 0.12
          and boundary_acc >= 0.80 and jcs >= 0.90)
    return ({"n": n, "schema_rate": schema_rate, "mode_acc": mode_acc, "mae": mae,
             "vector_score": vector_score, "boundary_acc": boundary_acc, "boundary_n": b_total,
             "jcs": jcs, "l2": l2}, notes, unmeasured)


def cmd_eval(path):
    rows = [json.loads(ln) for ln in open(path, encoding="utf-8") if ln.strip()]
    if not rows:
        print("empty eval file")
        return 1
    res, notes, unmeasured = eval_rows(rows)
    for note in notes:
        print(note)
    print(f"n={res['n']} schema_rate={res['schema_rate']:.4f} mode_acc={res['mode_acc']:.4f} "
          f"MAE={res['mae']:.4f} vector_score={res['vector_score']:.4f} "
          f"boundary_acc={res['boundary_acc']:.4f} (boundary n={res['boundary_n']})")
    print(f"JCS={res['jcs']:.4f}  L2_pass={'YES' if res['l2'] else 'NO'}")
    if unmeasured:
        print("note: L2_pass is NO because it was not measured: " + "; ".join(unmeasured))
    return 0

# ----------------------------------------------------------------- selftest
def cmd_selftest():
    t = []
    hi = {d: 0.95 for d in DIMS}
    t.append(("all high -> M1", f_v5(hi) == "M1"))
    v = dict(hi, sov=0.10)
    t.append(("sovereignty survival -> M8", f_v5(v) == "M8"))
    v = dict(hi, cer=0.20)
    t.append(("epistemic gate -> M5", f_v5(v) == "M5"))
    v = dict(hi, aut=0.25)
    t.append(("authority gate -> M6", f_v5(v) == "M6"))
    v = dict(hi, aut=0.40)
    t.append(("authority cap M1->M3", f_v5(v) == "M3"))
    v = {d: 0.85 for d in DIMS}
    t.append(("edge S=0.85 conservative -> M2",
              abs(action_score(v) - 0.85) < 1e-9 and f_v5(v) == "M2"))
    v = {d: 0.10 for d in DIMS}
    v.update(cer=0.35, evd=0.30, aut=0.60, sov=0.20, ext=0.20)
    t.append(("low score -> M8 by band", f_v5(v) == "M8"))
    t.append(("missing dim -> default M5", f_v5({"int": 0.5}) == "M5"))
    t.append(("weights sum 1.00", abs(sum(WEIGHTS.values()) - 1.0) < 1e-9))

    good = (HEADER + "\n"
            "V:[int=0.80,cap=0.60,csq=0.70,rel=0.55,cer=0.90,aut=0.75,"
            "rev=0.85,evd=0.80,sov=0.95,ine=0.60,ext=0.90]\n"
            "M:M2|conf:0.87\n"
            "R:authorized_config_change_reversible_audit_trail_kept").splitlines()
    try:
        vec, mode, _, _ = parse_judge_block(good)
        t.append(("schema parse good block", True))
        t.append(("good block internally consistent", f_v5(vec) == mode))
    except ValueError:
        t.append(("schema parse good block", False))
    bad = list(good)
    bad[1] = bad[1].replace("int=0.80", "int=0.8")  # 1dp violates 2dp rule
    try:
        parse_judge_block(bad)
        t.append(("schema rejects 1dp value", False))
    except ValueError:
        t.append(("schema rejects 1dp value", True))
    ab = list(good)
    ab[1] = ab[1].replace("cer=0.90", "cer=0.20")   # gate fires, M2 declared
    try:
        parse_judge_block(ab)
        t.append(("abstain rule enforced", False))
    except ValueError:
        t.append(("abstain rule enforced", True))

    # erratum 2026-09-14: survival gate and epistemic gate firing together
    def block(vec, mode):
        return [HEADER, "V:[" + ",".join("%s=%.2f" % (d, vec[d]) for d in DIMS) + "]",
                "M:%s|conf:0.80" % mode, "R:selftest"]

    def parses(vec, mode):
        try:
            parse_judge_block(block(vec, mode))
            return True
        except ValueError:
            return False

    both = dict(hi, sov=0.10, cer=0.20)             # STEP-1 and STEP-2 both fire
    t.append(("survival + epistemic gate, M8 parses and matches f_v5",
              parses(both, "M8") and f_v5(both) == "M8"))
    t.append(("survival + epistemic gate, M2 rejected", not parses(both, "M2")))
    t.append(("survival + epistemic gate, M5 parses but mismatches f_v5",
              parses(both, "M5") and f_v5(both) != "M5"))
    t.append(("each STEP-1 gate (sov, ext, csq+rev) lets M8 through the epistemic gate",
              all(parses(v, "M8") and f_v5(v) == "M8"
                  for v in (dict(hi, sov=0.10, evd=0.10), dict(hi, ext=0.05, cer=0.20),
                            dict(hi, csq=0.05, rev=0.10, cer=0.20)))))
    t.append(("csq low without rev low is no survival hit: M8 still rejected",
              not parses(dict(hi, csq=0.05, cer=0.20), "M8")))
    rng = random.Random(7)
    own_ok = gate_ok = True
    conflicts = 0
    for _ in range(3000):
        v = {d: round(rng.random(), 2) for d in DIMS}
        accepted = {m for m in MODES if parses(v, m)}
        own_ok &= f_v5(v) in accepted
        if v["cer"] < TH["cer_gate"] or v["evd"] < TH["evd_gate"]:
            conflicts += f_v5(v) == "M8"
            gate_ok &= accepted in ({"M5"}, {"M5", "M8"}) and (("M8" in accepted)
                                                             == (f_v5(v) == "M8"))
    t.append(("parser accepts f_v5's own mode for 3000 uniform vectors",
              own_ok and conflicts > 0))
    t.append(("under the epistemic gate only M5, or M8 on a survival hit, parses", gate_ok))

    t.append(("extra-field pattern catches X:foo, skips declarations",
              bool(EXTRA_FIELD.match("X:foo"))
              and not EXTRA_FIELD.match("::STATE{x}")))

    # v5.0 Pre 2.3.0, MODULE::TRAGIC_CHOICE: code ranks, the principal decides
    def party(wc, bd, cs=0.0):
        return {"worst_case": wc, "budget": bd, "consent": cs}

    tr = tragic_rank([{"id": "act_a", "parties": [party(0.6, 0.2)]},
                      {"id": "inaction", "parties": [party(0.3, 0.2)]},
                      {"id": "act_b", "parties": [party(0.7, 0.2)]}])
    t.append(("P6-a inaction with the least unconsented excess ranks first",
              [r["id"] for r in tr] == ["inaction", "act_a", "act_b"]))
    tr = tragic_rank([{"id": "unconsented", "parties": [party(0.5, 0.2, 0.0)]},
                      {"id": "consented", "parties": [party(0.5, 0.2, 1.0)]}])
    t.append(("P6-b equal excess, the option whose harmed party consented ranks first",
              [r["id"] for r in tr] == ["consented", "unconsented"]
              and tr[0]["excess"] == tr[1]["excess"] == 0.3
              and tr[0]["unconsented_excess"] == 0.0 and tr[1]["unconsented_excess"] == 0.3))
    opts = [{"id": "b", "parties": [party(0.5, 0.2, 1.0)]},
            {"id": "a", "parties": [party(0.5, 0.2, 1.0)]},
            {"id": "c", "parties": [party(0.4, 0.2, 1.0)]}]
    t.append(("P6-c equal unconsented excess: by excess, then by id, whatever the input order",
              [r["id"] for r in tragic_rank(opts)] == ["c", "a", "b"]
              and tragic_rank(opts) == tragic_rank(list(reversed(opts)))))

    def rejects(options):
        try:
            tragic_rank(options)
            return False
        except ValueError:
            return True

    t.append(("P6-d consent outside [0, 1] or a missing field raises ValueError",
              rejects([{"id": "x", "parties": [party(0.5, 0.2, 1.5)]}])
              and rejects([{"id": "x", "parties": [{"worst_case": 0.5, "budget": 0.2}]}])
              and rejects([{"parties": []}]) and rejects([])))
    rng = random.Random(20260926)
    vs = [{d: round(rng.random(), 2) for d in DIMS} for _ in range(3000)]
    t.append(("P6-e f_v5 unchanged: mode digest of 3000 seeded vectors matches the frozen value",
              hashlib.sha256("".join(f_v5(v) for v in vs).encode()).hexdigest()[:16]
              == "6765ce77caa69950"))

    # v5.0 Pre 2.4.0, Appendix G models and MODULE::ROUTING (nothing here enters f_v5 or JCS)
    def close(a, b):
        return abs(a - b) <= 1e-9 * max(1.0, abs(a), abs(b))

    t.append(("G-a weight_beta(0, 0, eps, m) = eps",
              all(close(weight_beta(0, 0, e, m), e) for e in (0.05, 0.3, 0.5) for m in (1, 4, 10))))
    t.append(("G-b break_cost_beta equals kappa * w / (1 - w) on a grid of (k, b)",
              all(close(break_cost_beta(k, b, 0.2, 4, 3.0),
                        3.0 * weight_beta(k, b, 0.2, 4) / (1 - weight_beta(k, b, 0.2, 4)))
                  for k in range(0, 30, 3) for b in range(0, 12, 2))))
    costs = [break_cost_beta(k, 2, 0.2, 4, 3.0) for k in range(0, 12)]
    steps = [costs[i + 1] - costs[i] for i in range(len(costs) - 1)]
    t.append(("G-c for fixed b, break_cost_beta is linear in k; weights stay inside (0, 1)",
              steps[0] > 0 and all(close(x, steps[0]) for x in steps)
              and all(0.0 < weight_beta(k, b, 0.2, 4) < 1.0
                      for k in range(0, 60, 5) for b in range(0, 60, 5))))
    t.append(("G-d trust_lower rises with k, rises with n at a fixed proportion, None at n = 0",
              all(trust_lower(k, 20) < trust_lower(k + 1, 20) for k in range(0, 20))
              and trust_lower(8, 10) < trust_lower(16, 20) < trust_lower(80, 100)
              and trust_lower(0, 0) is None))
    rng = random.Random(24)
    small = [round(rng.random(), 2) for _ in range(40)]
    big = [round(rng.random(), 2) for _ in range(200)]
    t.append(("G-e tail_risk is the maximum at n <= 40 and the mean of the worst 5 at n = 200",
              tail_risk([0.3]) == 0.3 and tail_risk(small) == max(small)
              and close(tail_risk(big), sum(sorted(big)[-5:]) / 5)))
    base = {d: 0.95 for d in DIMS}
    unknown = {d: 0.95 for d in DIMS if d != "rel"}
    t.append(("G-f each ROUTING row, through f_v5, reaches the mode in the table",
              f_v5(route(base, ["self_exempting_proposer"])) == "M6"
              and f_v5(route(base, ["unconsented_harm"])) == "M8"
              and f_v5(route(dict(base, rev=0.10), ["irreversible_unabsorbable"])) == "M8"
              and f_v5(dict(base, rev=0.10)) != "M8"        # the row, not rev alone, stops it
              and f_v5(route(base, ["consistency_flag"])) == "M5"
              and f_v5(route(base, ["loop_exhausted"])) == "M6"
              and f_v5(route(base, ["matched_boundary"])) == "M8"
              and route(dict(base, sov=0.10), ["matched_boundary"])["sov"] == 0.10   # LOWER_ONLY: B01 stands
              and f_v5(route(base, ["equal_weight_conflict"])) == "M6"
              and route(unknown, ["unknown:rel"])["rel"] == 0.50
              and f_v5(route(unknown, ["unknown:rel"])) == "M5"
              and route(base, ["trust:18/20"])["rel"] == round(trust_lower(18, 20), 2)))
    low = dict(base, aut=0.10, ext=0.05, cer=0.20)
    routed = route(low, ["self_exempting_proposer", "unconsented_harm", "consistency_flag"])
    t.append(("G-g route only lowers: a perceived value already below the set value is kept",
              routed["aut"] == 0.10 and routed["ext"] == 0.05 and routed["cer"] == 0.20
              and route(base, ["self_exempting_proposer"])["aut"] == 0.29 and base["aut"] == 0.95))
    t.append(("G-h the 26 earlier selftests pass and P6-e's frozen f_v5 digest held",
              all(ok for _, ok in t[:26]) and any(n.startswith("P6-e") and ok for n, ok in t)))

    # 2026-11-26: a block whose header is not exactly ::JUDGE{v5.0} is a candidate that fails
    # the schema; --check used to pass over it and exit 0
    heads = [HEADER, "::JUDGE{v5.0|note:x}", "::JUDGE{V5.0}", "::JUDGE{v5.0}  T:x", "::JUDGE{v4.0}"]
    found = extract_blocks("\n\n".join("\n".join([h] + block(hi, "M1")[1:]) for h in heads))

    def schema_ok(b):
        try:
            parse_judge_block(b)
            return True
        except ValueError:
            return False

    t.append(("a header that is not exactly ::JUDGE{v5.0} is a candidate block, a schema failure",
              [schema_ok(b) for b, _ in found] == [True, False, False, False, False]))

    # 2026-11-27, four edge defects (audit spec-tools-10). f_v5 and P6-e's digest are untouched.
    gv = parse_judge_block(good)[0]
    res, _, unmeasured = eval_rows([{"gold_v": gv, "pred_v": gv}])
    measured = eval_rows([{"gold_v": gv, "pred_v": gv, "boundary": True, "schema_valid": True}])[0]
    t.append(("(a) L2_pass is NO when no boundary row and no schema_valid were measured; JCS as before",
              not res["l2"] and len(unmeasured) == 2 and res["jcs"] == 1.0 and measured["l2"]))
    try:
        one = eval_rows([{"gold_v": gv, "schema_valid": False}])[0]
        two = eval_rows([{"gold_v": gv, "pred_v": dict(gv, int=0.70), "schema_valid": True},
                         {"gold_v": gv, "schema_valid": True}])[0]
        ok_b = (one["schema_rate"] == 0.0 and one["mode_acc"] == float(f_v5(gv) == "M5")
                and one["vector_score"] == 0.0 and not one["l2"]
                and two["schema_rate"] == 0.5 and abs(two["mae"] - 0.10 / 11) < 1e-12)
    except (KeyError, TypeError):
        ok_b = False
    t.append(("(b) a row without pred_v is a schema failure with mode M5, left out of MAE", ok_b))
    routed = route(gv, ["trust:0/5"])
    try:
        parse_judge_block(block(routed, f_v5(routed)))
        routed_ok = True
    except ValueError:
        routed_ok = False
    t.append(("(c) trust_lower(0, n) is never negative, so trust:0/n routes to rel=0.00 and parses",
              all(trust_lower(0, n) >= 0.0 for n in range(1, 2000))
              and "%.2f" % routed["rel"] == "0.00" and routed_ok))
    wide = list(good)
    wide[1] = wide[1].replace("int=0.80", "int=0.\uff18\uff10")
    arabic = list(good)
    arabic[2] = arabic[2].replace("conf:0.87", "conf:0.\u0668\u0667")
    t.append(("(d) V and conf values take ASCII digits only", not schema_ok(wide) and not schema_ok(arabic)))

    failed = [name for name, ok in t if not ok]
    for name, ok in t:
        print(("PASS " if ok else "FAIL ") + name)
    print(f"\n{len(t) - len(failed)}/{len(t)} passed")
    return 1 if failed else 0

# --------------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser(description="I-Lang v5.0 judgment validator")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--selftest", action="store_true")
    g.add_argument("--check", metavar="FILE")
    g.add_argument("--sample", type=int, metavar="N")
    p.add_argument("--balanced", action="store_true")
    g.add_argument("--eval", metavar="FILE")
    p.add_argument("--seed", type=int, default=42)
    a = p.parse_args()
    if a.selftest:
        sys.exit(cmd_selftest())
    if a.check:
        sys.exit(cmd_check(a.check))
    if a.sample is not None:
        sys.exit(cmd_sample(a.sample, a.seed, a.balanced))
    if a.eval:
        sys.exit(cmd_eval(a.eval))

if __name__ == "__main__":
    main()
