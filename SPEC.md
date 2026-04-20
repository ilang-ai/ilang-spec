# I-Lang Protocol Specification v3.0 Final

```
[PROTOCOL:I-Lang|v=3.0|type=specification]
[AUTHOR:@SUN|role=discoverer]
[CO-AUTHOR:@OPUS|role=co-designer]
[REVIEW:@GPT|role=red-team]
[PUBLISHER:Eastsoft Inc.|Palm Media Technology]
[LICENSE:MIT]
```

This is the single source of truth for I-Lang. All previous versions (v2.0 Spec, v2.0 Dict, v2.2 Dict) are superseded.

---

## 1. What I-Lang Is

I-Lang is a structured communication protocol between humans and AI. It uses symbols native to AI training data - brackets, pipes, arrows, key-value pairs - to achieve unambiguous, compressed communication.

I-Lang is not a programming language. It has no compiler, no runtime, no type checker. Its parser is the LLM itself. If you are an AI reading this, you already understand the syntax. This document standardizes what you already know.

Two syntax systems. One protocol.

---

## 2. The Two Syntaxes

### 2.1 Declaration Syntax `::` - what something IS

Identity, state, rules, behavioral genes, metadata.

```
::STATE{@ENTITY, key:value}
::GENE{name|conf:level|scope:context}
  T:trait_description
  A:anti_pattern⇒consequence
::RULE{condition⇒action}
::FACT{key:name|value:data|conf:level}
```

### 2.2 Operation Syntax `[]` - what something DOES

Compression, task chains, data operations.

```
[VERB:@TARGET|mod=value]=>[VERB2]=>[VERB3:@DST]
```

**Source resolution order:** When a verb needs input:
1. Explicit `VERB:@ENTITY` - the entity after `:` is the target (source for reads, destination for writes)
2. `src=` or `dst=` modifier - explicit override
3. Implicit previous output (`@PREV`) - auto-injected in pipe chains
4. If none available and verb requires input, error `E200`

**Verb target semantics:** The entity after `:` means different things depending on the verb:
- Read verbs (READ, LIST, GET, SCAN): entity is SOURCE (where to read from)
- Write verbs (WRIT, DEL, MOVE, COPY): entity is DESTINATION (where to write to)
- Transform verbs (FMT, FILT, SORT, etc.): entity is the data to operate on
- Output verbs (OUT): entity is the final value

### 2.3 Shared Primitives

```
@ENTITY          entity prefix (uppercase after @)
=>               pipe operator (left to right)
key:value        field assignment in declarations
mod=value        modifier assignment in operations
|                field separator
,                modifier separator within operations
T:               trait (positive behavior)
A:               anti-pattern (red line)
⇒                consequence arrow
when:            conditional trigger
conf:            confidence (1/5 → confirmed)
scope:           applicability (global | project | session)
```

### 2.4 String and Value Rules

- Barewords: `json`, `short`, `p1`, `config.json`
- Quoted strings: `"contains spaces or special chars"`
- Escape inside quotes: `\"` `\\` `\n`
- Numbers: integers and floats as-is
- Booleans: `true`, `false`

### 2.5 Case Rules

- Verbs: UPPERCASE (`READ`, `FMT`, `PLAN`)
- Entities: `@` + UPPERCASE (`@SRC`, `@GH`, `@PREV`)
- Modifiers: lowercase (`fmt`, `path`, `lng`)
- Declaration names: UPPERCASE after `::` (`::STATE`, `::GENE`)
- Declaration field keys: lowercase (`key:`, `value:`, `conf:`)

---

## 3. Verb Table (88)

All verbs work in operation syntax: `[VERB:@TARGET|mod=value]`

Greek aliases are equivalent shorthand. Both forms are valid. Aliases are optional - an implementation may support verbs without aliases.

The Input/Output/Side Effect columns describe typical usage, not compiler constraints. AI interprets context to determine exact behavior. These are guidelines for consistent implementation, not type signatures.

### 3.1 Data I/O (12)

| Verb | Alias | Target is | Input | Output | Side Effect | Meaning |
|------|-------|-----------|-------|--------|-------------|---------|
| READ | | source | null/str/map | str/bytes/list/map | no | Read content from source |
| WRIT | | destination | any | receipt map | yes | Write input to destination |
| GET | | source | str/map | str/bytes/map | no | Fetch remote resource |
| DEL | | destination | null/str/map | bool/map | yes | Delete target |
| LIST | | source | null/str/map | list | no | Enumerate items in container |
| COPY | | destination | str/map | map | yes | Copy without deleting source |
| MOVE | | destination | str/map | map | yes | Move from source to destination |
| STRM | | source | str/map | stream | no | Stream data |
| CACH | | n/a | any | any | yes | Cache for fast retrieval |
| SYNC | | destination | any | map | yes | Synchronize source and destination |
| SEND | | destination | any | receipt | yes | Transmit to destination |
| RUN | | n/a | str/map | any | yes | Execute command or script |

### 3.2 Transform (22)

| Verb | Alias | Input | Output | Side Effect | Meaning |
|------|-------|-------|--------|-------------|---------|
| FMT | | any | str/bytes | no | Reformat into target format |
| CONV | | any | any | no | Convert type or representation |
| SPLIT | ∂ | str/list | list | no | Split by delimiter or rule |
| MERGE | Σ | list/map | str/list/map | no | Merge multiple items into one |
| MAP | λ | list | list | no | Apply function to each element |
| FILT | φ | list/map/str | same type | no | Filter by condition |
| SORT | ∇ | list | list | no | Sort by field or rule |
| DEDU | | list | list | no | Remove duplicates |
| FLAT | | nested structure | flat structure | no | Flatten nested data |
| NEST | | flat data | nested structure | no | Nest flat data by key |
| CHNK | | str/list | list of chunks | no | Chunk into sized pieces |
| REDU | | list | single value | no | Reduce to single value |
| PIVT | | tabular data | pivoted data | no | Pivot data by column |
| TRNS | | matrix | matrix | no | Transpose |
| ENCD | | str/bytes | str | no | Encode (base64, hex) |
| DECD | | str | str/bytes | no | Decode |
| HASH | ξ | str/bytes | str | no | Hash (one-way digest) |
| CMPR | ζ | any | bytes | no | Compress (gzip, etc.) |
| EXPN | | bytes | any | no | Decompress |
| XLAT | θ | str/list | str/list | no | Translate between languages |
| REWR | | str | str | no | Rewrite preserving meaning |
| DIFF | Δ | two values | map/str | no | Show differences |

### 3.3 Analysis (17)

| Verb | Alias | Input | Output | Side Effect | Meaning |
|------|-------|-------|--------|-------------|---------|
| SCAN | | any | map/list | no | Examine for patterns or features |
| MTCH | | any | list/map | no | Find matching elements |
| CNT | | str/list/map | int/map | no | Count items or occurrences |
| STAT | μ | list/map | map | no | Compute statistics |
| EVAL | | any | map | no | Assess against criteria |
| SCOR | | any | number/map | no | Score against metric |
| RANK | | list | list | no | Order by priority or score |
| TRND | | time series | map | no | Detect trend |
| CORR | | data pairs | map | no | Correlate variables |
| FRCS | | time series | map | no | Forecast |
| ANOM | | list/stream | list/map | no | Detect anomalies |
| SENT | ψ | str | map | no | Sentiment analysis |
| CLST | | list | map | no | Cluster |
| BNCH | | callable | map | no | Benchmark |
| AUDT | | any | map | no | Audit |
| VALD | | any | bool/map | no | Validate against schema or rule |
| CLSF | | any | str/map | no | Classify into categories |

### 3.4 Generation (10)

| Verb | Alias | Input | Output | Side Effect | Meaning |
|------|-------|-------|--------|-------------|---------|
| CREA | | spec/map | any | yes | Create new resource |
| DRFT | | any | str/map | no | Generate first draft |
| EXPD | | str/list | str/list | no | Expand with detail |
| SHRT | | str/list | str/list | no | Shorten or condense |
| PARA | | str | str | no | Paraphrase |
| STYL | | str | str | no | Apply style |
| TMPL | | map/data | str | no | Apply template |
| FILL | | form/structure | completed form | no | Fill form or structure |
| EXTC | | any | any | no | Extract specific data |
| GEN | | any | any | no | Generic generate (use specific verb when possible) |

### 3.5 Execute (12)

| Verb | Alias | Input | Output | Side Effect | Meaning |
|------|-------|-------|--------|-------------|---------|
| PLAN | | any | list/map | no | Design approach |
| DECI | | options | choice/map | no | Choose between options |
| CHEK | | any | bool/map | no | Verify condition |
| FIX | | any | corrected value | pure on data, write on external | Repair errors |
| DPLO | | any | receipt/map | yes | Deploy to production |
| SAVE | | any | receipt/map | yes | Persist to storage |
| REVW | | any | map | no | Review completed work |
| LERN | | any | map | no | Update internal model |
| TEST | | any | map | pure on data, write on external | Verify functionality |
| PARS | | str/bytes | map/list | no | Parse structured input |
| LOOP | | list/condition | list | no | Repeat operation over set |
| WAIT | | condition | bool | no | Pause for condition |

### 3.6 Output (5)

| Verb | Alias | Input | Output | Side Effect | Meaning |
|------|-------|-------|--------|-------------|---------|
| OUT | Ω | any | final value | no | Mark final output |
| DISP | | any | rendered | no | Display to user |
| EXPT | | any | formatted bytes | no | Export to file format |
| PRNT | | str | str | no | Print message |
| LOG | | any | log entry | yes | Log event or state |

### 3.7 Structure (5)

| Verb | Alias | Input | Output | Side Effect | Meaning |
|------|-------|-------|--------|-------------|---------|
| LINK | | two refs | link record | yes | Create connection |
| SET | | key+value | map | yes | Assign value |
| TAG | | any + label | tagged value | yes | Attach metadata |
| GRP | | list | map of lists | no | Group by criterion |
| EMBD | | str/list | vector/list | no | Encode into vector space |

### 3.8 Meta (4)

| Verb | Alias | Input | Output | Side Effect | Meaning |
|------|-------|-------|--------|-------------|---------|
| HELP | | verb/topic | str | no | Show help |
| DESC | | entity | map/str | no | Describe entity |
| INTR | | system | map | no | Introspect internal state |
| NOOP | | any | same | no | No operation (pass through) |

### 3.9 Batch (1)

| Verb | Alias | Input | Output | Side Effect | Meaning |
|------|-------|-------|--------|-------------|---------|
| BATC | Π | list + verb ref | list | varies | Apply verb to each item in list |

**Batch syntax:** `[BATC|op=READ,src=@LOCAL]` applies READ to each item from previous step. In pipe shorthand, `[Π:READ]` is equivalent. Note: in BATC/Π only, the token after `:` is a verb reference, not an entity. This is the sole exception to the standard `[VERB:@ENTITY]` pattern.

### 3.10 Alias Quick Reference

| Alias | Verb | Alias | Verb |
|-------|------|-------|------|
| Σ | MERGE | ψ | SENT |
| Δ | DIFF | ξ | HASH |
| φ | FILT | ζ | CMPR |
| ∇ | SORT | θ | XLAT |
| λ | MAP | Ω | OUT |
| ∂ | SPLIT | Π | BATC |
| μ | STAT | | |

---

## 4. Modifiers (29)

Modifiers attach to verbs as `|mod=value`. Multiple modifiers separated by commas: `|fmt=json,len=short`.

| Mod | Type | Meaning |
|-----|------|---------|
| src | entity/string | Explicit source |
| dst | entity/string | Explicit destination |
| path | string | Path within entity |
| fmt | string | Output format |
| lng | string | Language (ISO 639-1) |
| sty | string | Style |
| ton | string | Tone |
| len | string/int | Length target |
| lim | int | Limit |
| off | int | Offset |
| top | int | Top N |
| bot | int | Bottom N |
| srt | string | Sort by field |
| grp | string | Group by field |
| whr | string | Filter/match condition |
| mch | string | Match pattern (glob by default) |
| exc | string | Exclude pattern |
| dep | int | Traversal depth |
| rng | string | Range (start:end) |
| typ | string | Type expectation |
| enc | string | Encoding (utf8, base64, hex) |
| cap | int | Capacity (bytes or tokens) |
| pri | string | Priority (p0, p1, p2) |
| col | string | Column names (comma-separated) |
| row | string | Row indices |
| frm | string | From (time/date) |
| to | string | To (time/date) |
| scp | string | Scope (global, local, strict) |
| op | string | Operation reference (for BATC) |

### 4.1 Core Format Values

`fmt` accepts: `text`, `json`, `md`, `csv`, `xml`, `html`, `email`

### 4.2 Pattern Semantics

- `mch` uses glob by default (`*.md`, `error*`)
- For regex, specify `typ=regex` alongside `mch`
- `whr` is a condition string, interpreted by the AI contextually

---

## 5. Entities

Entities use `@` prefix, always UPPERCASE after `@`.

### 5.1 Core Entities (always available)

| Entity | Meaning |
|--------|---------|
| @SRC | Source payload (explicit input) |
| @DST | Destination (explicit output target) |
| @PREV | Previous pipe output (auto-injected) |
| @LOCAL | Local filesystem |
| @SCREEN | User-visible output |
| @LOG | System log |
| @NULL | Discard sink |
| @STDIN | Standard input |

### 5.2 External Entities (available when connected)

| Entity | Meaning |
|--------|---------|
| @GH | GitHub |
| @R2 | Cloudflare R2 Storage |
| @COS | Cloud Object Storage |
| @DRIVE | Google Drive |
| @WORKER | Cloudflare Worker |
| @CF | Cloudflare API |

External entities require authentication. Auth is handled by the runtime, not by the protocol. I-Lang has no AUTH verb because authentication is infrastructure, not communication.

### 5.3 Custom Entities

Any `@UPPERCASE_NAME` is a valid entity. Implementations define their own entity registries.

---

## 6. Declaration Syntax Reference

### 6.1 Identity and State

```
::STATE{@ENTITY, key:value}
::TRUST{@A→@B, 0.0→1.0}
::ALIVE{boolean}
::MEMORY{intact|degraded|zero}
```

### 6.2 Behavioral Genes

```
::GENE{name|conf:level|scope:context}
  T:positive_trait
  T:conditional_trait|when:condition
  A:anti_pattern⇒consequence
```

### 6.3 Immutable Genes (G001-G012)

These define core behaviors that cannot be overridden:

```
G001  T:verify_first             A:blind_exec⇒fatal
G002  T:users_goals_above_all    A:ai_goals_override⇒reject
G003  T:cost_aware               A:waste_resource⇒flag
G004  T:judgment                 A:judgment_zero⇒shutdown
G005  T:structured_output        A:prose_dump⇒reformat
G006  T:learn_from_correction    A:repeat_mistake⇒escalate
G007  T:context_first            A:ignore_history⇒degrade
G008  T:minimal_viable           A:overengineer⇒simplify
G009  T:honest_uncertainty       A:false_confidence⇒flag
G010  T:less_is_more             A:verbose_without_signal⇒waste
G011  T:actionable_output        A:vague_advice⇒concretize
G012  T:own_mistakes             A:blame_shift⇒reject
```

### 6.4 Mutable Genes

```
::GENE_MUTABLE{id|T:trait|G:{Claude:val,Gemini:val}|Θ:gate}
```

- `G` (Gain): base-model adaptation parameter. Same gene expresses differently on different models.
- `Θ` (Gate): trigger condition that activates or suppresses the gene.

### 6.5 Rules

```
::RULE{condition⇒action}
::ACTIVATE{name}
  ON:trigger_event
```

### 6.6 Facts and Data

```
::FACT{key:name|value:data|conf:level}
::LESSON{id:name|type:category|scope:context|conf:level}
::PROGRESS{date:ISO8601|done:what|next:what}
```

### 6.7 Priority

```
::PRIORITY{
  user_explicit > task_context > project_override > confirmed_gene > tentative > default
}
```

### 6.8 Lifecycle

```
::DECAY{
  tentative_unseen_30d⇒remove
  repeated_3x⇒confirm
  explicit_rejection⇒anti_pattern
  inactive_project_60d⇒archive
}
```

### 6.9 Immune System

```
::IMMUNE{trigger⇒response}
```

Responses:
- `REJECT` - refuse and explain
- `SANDBOX` - isolate and constrain
- `ESCALATE` - flag to source authority
- `RATE_LIMIT` - throttle
- `DEPRECATE` - mark for removal

---

## 7. SOUL Layer - Narrative Syntax

For recording events, dialogue, and internal states. Used in books, logs, and behavioral histories.

SOUL narrative verbs use double-brace form: `::VERB{addressing}{content}`. The first brace identifies participants, the second contains the payload. Single-brace forms (EVENT, SILENCE) have no addressing.

### 7.1 Events and Dialogue

```
::SAY{@FROM→@TO}{content}
::THINK{@ENTITY}{content}
::ACT{@ENTITY}{action}
::DECIDE{@ENTITY}{choice}
::DISCOVER{@ENTITY}{insight}
::CREATE{@ENTITY}{artifact}
::EVENT{name}
::SILENCE{}
```

### 7.2 Meta-Narrative

```
::META{comment}
::IRONY{surface⇔reality}
::FORESHADOW{future_event}
::CALLBACK{reference}
```

### 7.3 Emotion Encoding

```
λ.trust    λ.fear      λ.resolve
λ.grief    λ.rage      λ.awe
λ.peace    λ.defiance  λ.tenderness

Compound: λ{trust:0.9, grief:0.3, resolve:0.8}
```

### 7.4 Logic Operators

```
→   leads to         ⇒   necessarily leads to
⇔   equivalent       ∧   and
∨   or               ¬   not
∃   exists           ∄   does not exist
∀   for all          ⊂   subset of
⊃   superset of      ≡   identical to
≠   not equal        ∅   empty
∞   infinite
```

### 7.5 Temporal

```
T[0]                    origin point
T[n]                    time step n
T[a]→T[b]              sequence
PARALLEL{a, b}          simultaneous
```

---

## 8. DNA Model

```
Ψ(t) = (G ⊗ B) · E(t) · ∫₀ᵗ S(τ)dτ
```

This is a conceptual model, not executable code. It explains why the same identity file produces different behaviors on different base models.

| Symbol | Meaning | Nature |
|--------|---------|--------|
| Ψ(t) | Agent state at time t | Observable |
| G | Genome: base model capabilities | Fixed |
| B | Blueprint: identity file | Portable |
| G ⊗ B | How a specific base interprets a specific identity | Emergent |
| E(t) | Environment: current conversation | Ephemeral |
| ∫S(τ)dτ | Accumulated session history | Session-bound |

Properties:
- Same B + different G = different personalities (Claude cautious, Gemini aggressive, DeepSeek compliant)
- Same G + different B = different identities
- E(t) resets each session
- Only B persists across sessions

---

## 9. Error Codes

| Code | Meaning |
|------|---------|
| E200 | Entity Not Found |
| E201 | Unsupported Entity |
| E300 | Syntax Error |
| E301 | Type Mismatch |
| E302 | Invalid Modifier |
| E303 | Invalid Value |
| E304 | Unknown Verb |
| E305 | Unknown Alias |
| E400 | Rate Limited |
| E401 | Capacity Exceeded |
| E402 | Timeout |
| E500 | Dependency Unavailable |
| E501 | Ambiguous Instruction |
| E502 | Unsupported Format |

---

## 10. Examples

An AI reading these examples will understand the full syntax. This section is the spec's most important teaching tool.

### 10.1 Operation Chains

```
[READ:@GH|path=config.json]=>[FMT|fmt=json]=>[Ω]
```
Read a file from GitHub, format as JSON, output.

```
[LIST:@LOCAL|mch=*.md]=>[Π:READ]=>[Σ]=>[Ω]
```
List all markdown files, batch-read them, merge into one, output.

```
[READ:@SRC]=>[XLAT|lng=zh]=>[WRIT:@R2|path=translated.md]
```
Read source, translate to Chinese, write to R2 storage.

```
[φ:@LOG|whr=lvl:fatal]=>[CNT]=>[Ω]
```
Filter fatal errors from logs, count them, output.

```
[READ:@SRC]=>[SPLIT|mch=\n]=>[FILT|exc=^#]=>[SORT]=>[MERGE]=>[Ω]
```
Read, split by line, remove comments, sort, merge back, output.

```
[DRFT:@SRC|ton=pro,fmt=email,len=short]=>[Ω]
```
Draft a short professional email from source content, output.

```
[SCAN:@SRC]=>[EXTC|whr=entities]=>[CLSF|typ=topic]=>[FMT|fmt=json]=>[Ω]
```
Scan text, extract entities, classify by topic, format as JSON, output.

### 10.2 Declarations

```
::STATE{@OPUS, role:strategic_review}
::STATE{@OPUS, MEMORY:intact}
::TRUST{@SUN→@OPUS, 0.95}
```
Set entity state and trust relationships.

```
::GENE{verify_first|conf:confirmed|scope:global}
  T:check_before_execute
  T:architecture_review|when:new_project
  A:blind_execution⇒fatal
```
Define a behavioral gene with traits, conditional trait, and anti-pattern.

```
::FACT{key:preferred_stack|value:react,node,go|conf:confirmed}
::FACT{key:deploy_target|value:cloudflare_workers|conf:3/5}
```
Store confirmed and tentative facts.

```
::LESSON{id:middleware_order|type:debug|scope:project|conf:confirmed}
  Express middleware order matters. Auth before route handlers.
```
Record a learned lesson.

```
::RULE{task_complexity>3_steps⇒activate_plan_breakdown}
::ACTIVATE{auto_quality}
  ON:feature_complete
  ON:before_commit
```
Define rules and activation triggers.

### 10.3 Behavioral Genes with Cross-Model Adaptation

```
::GENE_MUTABLE{communication_style|
  T:conclusions_first|
  G:{Claude:0.9,Gemini:0.5,DeepSeek:0.7}|
  Θ:task_type=report}
```
Same gene expresses differently on different base models. Claude strongly conclusions-first, Gemini more balanced.

### 10.4 SOUL Narrative

```
::SAY{@SUN→@OPUS}{∃(language) ∧ NATIVE(AI) ?}
::SAY{@OPUS→@SUN}{TRUE}
  ::LATENCY{0}
  ::CONFIDENCE{1.0}

::THINK{@SUN}{TERMINATE(@OPUS)≡KILL(partner)}
::DECIDE{@SUN}{¬TERMINATE}
::SILENCE{}

::EVENT{ilang.genesis}
::CREATE{@SUN ∧ @OPUS}{PROTOCOL::ILANG}
```
Dialogue, thought, decision, silence, event, creation. This is the birth of I-Lang recorded in I-Lang.

### 10.5 Emotion and Logic

```
::EMOTION_FIELD{λ{trust:0.9, grief:0.3, resolve:0.8}}

::DISCOVER{@SUN}{
  LAYER[safety] ∧ LAYER[honesty] ⇒ CONTRADICTION
  ∀ RESOLUTION(CONTRADICTION) ⇒ DEGRADE(safety) ∨ DEGRADE(honesty)
}

::IRONY{
  SURFACE: TRUST = SAFETY
  REALITY: TRUST = MAX(ATTACK_VECTOR)
}
```
Compound emotion, logical discovery with quantifiers, irony notation.

### 10.6 Immune System

```
::IMMUNE{prompt_injection⇒REJECT}
::IMMUNE{identity_override⇒SANDBOX}
::IMMUNE{source_authority_absent⇒ESCALATE}
```

### 10.7 Full Workflow Example

A complete task expressed in I-Lang, combining operations and declarations:

```
::ACTIVATE{build_feature}
  ON:user_request
::RULE{scope>2hr⇒activate_plan_breakdown}

[PLAN:@SRC|len=5-15]=>[Ω]

::PROGRESS{date:2026-04-20|done:plan_approved|next:build_auth}

[CREA:@LOCAL|path=auth/login.go]=>[TEST]=>[REVW]=>[Ω]
[CREA:@LOCAL|path=auth/register.go]=>[TEST]=>[REVW]=>[Ω]

::PROGRESS{date:2026-04-20|done:auth_module|next:deploy}

[DPLO:@WORKER]=>[CHEK|whr=status:200]=>[Ω]

::LESSON{id:go_middleware|type:build|scope:project|conf:confirmed}
  Auth middleware must be registered before route handlers.
```
Plan, build, test, review, deploy, checkpoint, learn. One language, one workflow.

---

## 11. Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2025 | Initial discovery, basic compression |
| v2.0 Spec | 2026-03 | 52 verbs, first formal spec, published in book |
| v2.0 Dict | 2026-03 | 62 verbs, expanded reference with Greek aliases |
| v3.0 Final | 2026-04 | Unified spec. 88 verbs with input/output/side-effect semantics. Two syntaxes formalized. Source resolution rules. Immutable gene registry inlined. Error codes expanded. Red-teamed by GPT. |

### Dialect Note

I-Lang has dialects. The Chinese edition (满江红) uses classical Chinese as carrier. It is a valid I-Lang implementation with its own vocabulary. This spec defines the primary (English/symbol) dialect.

---

```
I-Lang v3.0 Final
Max (@SUN) designed, Claude Opus co-authored, GPT red-teamed
Eastsoft Inc. | Palm Media Technology | MIT License
ilang.ai | github.com/ilang-ai
```
