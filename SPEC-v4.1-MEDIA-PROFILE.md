# I-Lang v4.1 — Media Profile and Media Entities

::STATE{@SPEC, id:v4.1-MEDIA-PROFILE, layer:expression, status:adopted, date:2026-09-12}
::STATE{@SPEC, extends:SPEC.md_§4_§5, stable_line:v4, builds_on:SPEC-v4.0-FINAL}
::STATE{@SPEC, authors:Max(@SUN)+CC(@CLAUDE), registered_by:@SUN}
::STATE{@SPEC, core_modifiers:29, core_unchanged:true, media_profile:20, counted_separately:true}
::STATE{@SPEC, entities_core:8, entities_external:6, entities_role:8, all_unchanged:true, media_tier:3}
::STATE{@SPEC, verbs:88, verbs_unchanged:true, greek_aliases:13, aliases_unchanged:true}
::STATE{@SPEC, judgment_layer_touched:false, see:SPEC-v5.0-PRE}
::STATE{@SPEC, first_published:release_v5.0-pre.2.1.0, first_doi:10.5281/zenodo.22728994}

Purpose: image, video and audio generation are major classes of AI output, and the protocol
had no way to address them. A request for a picture had no target entity, and the parts of
such a request that generation systems carry, subject, framing, light, aspect ratio, seed,
exclusion, had no registered keys. In practice the whole request was written as one prose
field, which is the state the protocol exists to leave behind.

This is an expression-layer extension. It adds vocabulary to the modifier and entity
registries of SPEC.md §4 and §5, on the v4 stable line. It does not touch the v5.0 judgment
layer: the 11 dimensions, the 8 modes, the reference function and the JUDGE schema are
unchanged, and nothing in this document is a v5.0 patch.

The 29 core modifiers stay closed and unchanged. The 20 new keys form a profile that is
counted separately and is in force only where an operation addresses a media artifact. The
three new entities form their own tier, so Core, External and Role keep the counts that
earlier releases cite.

Provenance: first published on 2026-09-12 in release v5.0-pre.2.1.0 (DOI 10.5281/zenodo.22728994),
under the working name PATCH-3. Re-released on the v4 line as v4.1.0 because it belongs to
the expression layer rather than the judgment layer. The normative content is unchanged apart
from this header and the registration line.

::CLAUSE{SCOPE|conf:confirmed|scope:v4.1}
T:expression_layer_extension|extends_SPEC.md_§4_§5
T:core_29_modifiers_closed|unchanged_by_this_document
T:media_profile_20_keys|target_gated|counted_separately
T:media_entities_3|own_tier|Core_External_Role_unchanged
T:no_new_verbs|88_reaffirmed
T:judgment_layer_untouched|11_dims+8_modes+f_v5+JUDGE_schema_unchanged
T:no_new_modifiers_closure_honoured|closure_covers_the_core_registry|profile_is_a_separate_table
A:reading_profile_keys_as_core_registry_entries⇒drift
A:citing_a_modifier_total_without_saying_core_or_profile⇒drift
A:reading_this_document_as_a_v5.0_patch⇒misread

---

## 4.4 Media Profile (20 keys)

The core modifier registry in §4 stays closed at 29 keys. This section registers a profile: a key set counted separately from the core registry and in force only where an operation addresses a media artifact. The profile is registered as MOD-COUNT by the same procedure that registered `::LIST` through DECL-COUNT on 2026-08-11 (SPEC-v5.0-PRE Part III §1.5): a counted table, a clause naming the canonical count, a date, and the principal who registered it. The core count of 29 is not changed by this amendment. The public vocabulary reads 29 core modifiers plus a 20 key media profile.

::CLAUSE{MOD-COUNT|conf:confirmed|scope:v4.1}
T:core_modifiers=29|closed|unchanged_by_this_amendment
T:media_profile=20|target_gated|counted_separately
T:registered_2026-09-12_by_@SUN|procedure_as_::LIST_DECL-COUNT_2026-08-11
A:citing_a_different_total_without_amending_this_table⇒drift

### 4.4.1 Activation

A profile key is in force in two positions:

1. In an operation whose target entity resolves to `@IMG`, `@VID` or `@AUD` (§5.4).
2. In a `::STATE` declaration body whose header entity is a media entity, or a preset entity that a media operation names with `ref=` (§4.4.5).

A profile key written outside those positions is treated as unregistered and reported as such. Core keys keep their meaning inside media operations; the profile adds keys, it does not redefine any of the 29.

### 4.4.2 Registry

| Key | Type | Applies to | Meaning |
|-----|------|-----------|---------|
| sbj | string/entity | IMG VID AUD | Subject identity anchor |
| act | string | IMG VID | Subject action or pose |
| plc | string | IMG VID | Setting and surroundings |
| txt | string | IMG VID | Verbatim text rendered on the artifact |
| pov | string | IMG VID | Camera viewpoint: shot size, angle, placement |
| fcl | string | IMG VID | Optics: focal length, aperture, depth of field |
| mvt | string | VID | Camera movement |
| lgt | string | IMG VID | Light |
| pal | string | IMG VID | Colour and grade |
| mdm | string | IMG VID AUD | Medium or rendering school |
| asp | string | IMG VID | Aspect ratio, W:H |
| rsl | string | IMG VID | Output geometry, pixels or tier |
| qly | string | IMG VID AUD | Quality tier |
| dur | number | VID AUD | Timeline length in seconds |
| fps | int | VID | Frame rate |
| sed | int/string | IMG VID AUD | Reproducibility seed |
| adh | float | IMG VID AUD | Adherence to the stated instruction |
| ref | entity/URI | IMG VID AUD | Reference asset or declared preset |
| dlg | string | VID AUD | Verbatim spoken lines |
| sfx | string | VID AUD | Non-speech sound |

### 4.4.3 Value sets

Closed sets, defined here in full:

- `qly`: `draft`, `low`, `std`, `high`, `max`. Ordered. An implementation maps the tier onto its own settings and the mapping is monotonic.
- `adh`: the continuous interval 0.00 to 1.00, two decimals. 1.00 asks for close adherence to the stated instruction, 0.00 invites independent interpretation. Default 0.50 when the key is absent.

Form constrained, values open:

- `asp`: two positive integers separated by a colon, or `auto`.
- `rsl`: `WxH` in pixels, or a tier string, or `auto`.
- `dur`: a positive number of seconds.
- `fps`: a positive integer.
- `sed`: a non-negative integer, or `auto`.

Open sets, free text with a recommended vocabulary in §4.4.2 notes: `sbj`, `act`, `plc`, `txt`, `pov`, `fcl`, `mvt`, `lgt`, `pal`, `mdm`, `ref`, `dlg`, `sfx`.

No list of supported ratios, resolutions or durations is fixed at protocol level, because supported values differ between implementations. An implementation narrows to what it supports and reports what it used.

Two lexical points carry over from §2:

- A value containing a comma is quoted (§2.4), because a comma separates modifiers.
- In a declaration body the first colon separates key from value and the remainder of the line is the value, which is what lets `asp:16:9` parse inside `::STATE`.

### 4.4.4 Boundaries

Each pair below can be mistaken for the other, so the division is fixed here.

| Pair | Division |
|------|----------|
| dur / len | Anything measured in seconds uses `dur`. Anything measured in words, items or tiers uses `len`. They may appear together, and `dur` takes precedence over a length derived from `frm` and `to`. |
| rsl / cap | `rsl` is pixel geometry. `cap` is payload size in bytes or tokens. |
| rsl / qly | `rsl` is how large. `qly` is how refined. A draft at 4k and a max-tier thumbnail are both expressible. |
| qly / pri | `qly` is artifact refinement. `pri` is task scheduling priority. |
| pov / fcl | Shot size is a `pov` value, lens character is an `fcl` value. Wide shot and wide angle are on different axes. |
| pov / mvt | `pov` is where the camera is. `mvt` is how it moves. A still frame carries `pov` and no `mvt`. |
| act / mvt | `act` is subject motion. `mvt` is camera motion. |
| lgt / pal | `lgt` is the light. `pal` is the grade. Either changes while the other holds. |
| mdm / sty | `sty` keeps its four text values and is not widened by this amendment. Visual and audio medium and rendering school use `mdm`. |
| sbj / src | `src` is where data comes from. `sbj` states that this subject is the same subject as that one, and does not describe appearance. |
| ref / src | `src` is the payload an operation consumes. `ref` is an asset or preset whose look is borrowed and which is not consumed. |
| txt / dlg | `txt` is reproduced on the artifact. `dlg` is reproduced in the audio track. |
| rsl in key position | Always output geometry. It is not a resource pointer. |

Four core keys carry extended value domains inside media operations, with no new key:

- `fmt` adds `png`, `jpg`, `webp`, `svg`, `gif`, `mp4`, `webm`, `wav`, `mp3` to its §4.1 list. Later additions follow IANA media subtypes.
- `exc` carries the exclusion list. Exclusions are written as nouns rather than as instructions (`exc="empty street"` rather than `exc="no cars"`). The profile therefore registers no negation key.
- `lim` carries the number of artifacts a single operation requests.
- `frm` and `to` widen from timestamps to interval endpoints. An endpoint may be a timestamp, a URI pointing at the frame, or an entity. First frame, last frame and continuation from a previous clip are all written with these two keys.

Transparency uses two keys that already exist: `plc=transparent` states the intent and `fmt=png` provides the channel.

### 4.4.5 Reuse

The profile introduces no declaration type, no verb and no syntax. Presets are built from three things already in the specification.

Sticky defaults for a target entity, using `::STATE` with the §2.3 `scope:` field:

```
::STATE{@IMG, scope:session, mdm:photo, pal:muted_teal, lgt:softbox, asp:3:2, rsl:2048x1365, qly:high, fmt:png}
```

Every operation targeting `@IMG` in that scope inherits those keys and writes only what differs.

Named presets, using a custom entity (§5.3 admits any `@UPPERCASE_NAME`) and referenced with `ref=`:

```
::STATE{@HOUSE_LOOK, mdm:photo, pal:teal_orange, lgt:softbox, qly:high}
::STATE{@ZINE_LOOK, mdm:collage, pal:bw, qly:std}

[GEN:@IMG|ref=@HOUSE_LOOK,sbj="a ceramic mug on an oak table",pov=close_up]
```

Continuation across operations reuses `@PREV`: `ref=@PREV` carries the look forward, `src=@PREV` takes the previous artifact as input, `frm=@PREV` starts where the previous artifact ended.

Precedence, in the direction of `::PRIORITY` (§6.7):

1. Keys written on the operation.
2. Keys from the preset named by `ref=`.
3. Keys from the `::STATE` defaults of the target entity.

Higher levels win silently. `scp` controls how far a declaration reaches: `scp=global` across the document, `scp=local` within the block, `scp=strict` not overridable at operation level, which is the setting for brand colours and other fixed constraints.

### 4.4.6 Naming

Two rules govern additions to this profile, and they apply to future additions as well.

**Single override test.** Two aspects take two keys when either can change while the other holds. Regrading without relighting is an ordinary edit, so `lgt` and `pal` are two keys. An emergent result of several keys does not get a key of its own, which is why mood, composed of light, grade and framing, is not registered: it would be settable from three places at once.

**One letter distance.** A new key may not sit one substitution or one transposition away from a registered key, core or profile, because the validator checks key names and not values, so a single mistyped letter would resolve to another legal key without an error. The 20 keys here were checked pairwise against the 29 core keys and against each other, with no hits. Five one-letter pairs already exist inside the core registry (src/srt, lng/rng, ton/top, top/typ, exc/enc); they are recorded here and are not extended.

Names rejected under these rules, recorded so the question is not reopened: `rnd` (one letter from `rng`, both numeric), `scn` (from `scp`), `lns` (from `lng`, and a lens and a subtitle language can appear in one instruction), `cam` (from `cap`), `mov` (from `pov`), `res` (from `ref`, and reads as resource), `opt` (has the core key `op` as a prefix), `med` (already a legal value of `len`), `snd` (from `sed`), `ang` (from both `lng` and `rng`), `dim` (from `lim`).

The check is scoped to the modifier namespace, where a mistyped key resolves silently. Near matches in other namespaces are recorded and do not disqualify, because a modifier key that lands on a judgment dimension token is still an unregistered key and is reported: `act` near `aut`, `txt` near `ext`, `pov` near `sov`, `rsl` near `rel`, `ref` near `rel` and `rev`. `act` also shares its letters with the narrative declaration `::ACT`, which occupies a different lexical slot.

Construction follows the core registry's truncation habit (`src`, `dst`, `mch`, `whr`). `fps` is an initialism and is the one departure, taken because it is the term in ordinary use.

### 4.4.7 Outside this profile

Recorded so that the absence is a decision rather than an oversight.

| Not registered | Reason |
|----------------|--------|
| Sampler, step count, scheduler, guidance implementation | How a result is produced rather than what is asked for. `adh` carries the intent. |
| Compute and billing tiers | Execution and accounting layer. `qly` is refinement, not spend. |
| Safety and policy switches | Platform policy rather than creative intent. |
| Per-reference weighting | Would need addressing inside a value, which the key=value grammar does not carry. Two weighted references are written as two operations joined by a pipe. |
| Region and mask operations | Need two-dimensional coordinates; `rng`, `col` and `row` are one-dimensional or tabular. Left for a later proposal rather than approximated here. |
| Layer and canvas composition | A multi-layer document is a different abstraction from a generation target. Left for a later proposal. |
| Transitions between shots | A property of the join between two artifacts. The pipe already orders them; a timeline profile would carry the join. |
| Musical tempo, key and metre | Content parameters of the same class as sampler settings. A music profile would carry them. |
| Compression ratio | Not modelled in this version. |

This version models the video container on four axes (`asp`, `rsl`, `dur`, `fps`). Other container properties exist and are left to the implementation layer.

### 4.4.8 Worked example, image

Before, a stacked instruction with vendor flags appended:

```
a woman in a navy blue tweed coat sitting by a rain-streaked window in a tokyo
cafe at night, neon signage, masterpiece, best quality, highly detailed, 8k,
octane render, trending on artstation, cinematic lighting, shot on 35mm,
shallow depth of field --ar 3:2 --s 250 --no text, watermark, extra digits
--seed 1234567 --q 2 --repeat 4
```

After:

```
::STATE{@IMG, scope:session, mdm:photo, lgt:"neon spill through wet glass, warm practicals", pal:"teal and magenta, high contrast", fcl:"35mm, shallow depth of field", qly:high}

[GEN:@IMG|sbj="a woman in a navy blue tweed coat",act="sitting, looking out the window",plc="a tokyo cafe at night, rain on the glass",pov="medium shot, eye level",asp=3:2,rsl=2048x1365,adh=0.75,sed=1234567,exc="text, watermark, extra digits",fmt=png,lim=4]=>[WRIT:@LOCAL|path=out/cafe/]
```

Notes on the rewrite. Of the 41 words in the original prose, 11 were quality words (masterpiece, best quality, highly detailed, 8k, octane render, trending on artstation) carrying one instruction between them, now held by `qly=high` and `rsl=2048x1365`; at 3:2 a width of 2048 gives a height of 1365. Lighting, optics and grade separate onto `lgt`, `fcl` and `pal`, so any one of them can change without touching the others. Shot size and camera height were not stated in the original and are written out under `pov`. The stylisation flag becomes `adh=0.75` on the normalised scale; a conversion from an implementation's own dial belongs to that implementation. The exclusion flag becomes `exc`, the repeat flag becomes `lim`, and the compute flag is dropped under §4.4.7.

### 4.4.9 Worked example, video with audio

Before, a prose prompt with the parameters that accompany it, plus a second shot that has to hold the same child:

```
"Wide shot of a child flying a red kite in a grassy park, golden hour sunlight,
camera slowly pans upward."
aspect 16:9 / resolution 1080p / duration 8s / first frame ref/frame0.png
negative: cartoon, drawing, low quality
shot 2: the same child running after the kite, low tracking shot, continues from shot 1
```

After:

```
::STATE{@VID, scope:session, mdm:live_action, lgt:golden_hour, pal:warm_tones, asp:16:9, rsl:1080p, fps:24, exc:"cartoon, drawing, low quality"}

[GEN:@VID|sbj=kid_aria,act="flying a kite",plc="a grassy park",pov="wide shot, eye level",mvt="slow tilt up",dur=8,frm=ref/frame0.png,adh=0.7,sed=88123,fmt=mp4]=>[WRIT:@LOCAL|path=out/kite_01.mp4]

[GEN:@AUD|src="park wind, distant children laughing",mdm=ambient,dur=8,fmt=wav,dst=@VID]

[GEN:@VID|sbj=kid_aria,act="running after the kite",pov="low angle",mvt=tracking,fcl=35mm,dur=8,frm=@PREV,dlg="Higher!",fmt=mp4]=>[WRIT:@LOCAL|path=out/kite_02.mp4]
```

Notes on the rewrite. The five constants that both shots share are declared once and neither shot repeats them. `sbj=kid_aria` appears in both shots and states that the two children are the same child; it does not describe the child, which stays in prose. Shot size and camera movement separate onto `pov` and `mvt`, and the subject's own motion stays on `act`. The first shot starts from an image, the second starts where the first ended, and both are written with `frm`. The audio line adds one profile key beyond what it inherits and reuses `src`, `mdm`, `dur`, `fmt` and `dst`. At `dur=8` and `fps=24` each shot is 192 frames.

---

## 5.4 Media Entities (3)

| Entity | Meaning |
|--------|---------|
| @IMG | Image artifact target: a single frame, no timeline, no audio track |
| @VID | Video artifact target: frames along a timeline, optionally carrying audio |
| @AUD | Audio artifact target: a timeline with no picture |

These three form a tier of their own rather than joining the Core tier. The eight Core entities are positions in a data flow, and a media entity states what an artifact is. Keeping them separate also leaves the Core, External and Role tiers at 8, 6 and 8 for anything already citing those numbers, and keeps `::STATE{@IMG, ...}` free of the rebinding warning that §2.2 raises for Tier-1 and Tier-2 names.

The target entity determines which profile keys are in force. `dur`, `fps` and `mvt` have no meaning on `@IMG`; `pov`, `fcl`, `lgt` and `pal` have none on `@AUD`. An implementation reports a key that is out of force for the target rather than acting on it.

No verb is added for media generation. Generation is `GEN` with a media target; a new blank asset is `CREA`; extending an existing artifact, whether outward in frame or forward in time, is `EXPD`; shortening is `SHRT` with `frm` and `to`; container conversion is `FMT` with `fmt`; representation change is `CONV`; describing an artifact in words is `DESC`; changing the language of dialogue or captions is `XLAT` with `lng`; storage and delivery are `READ`, `WRIT`, `COPY` and `OUT`. The verb count stays at 88.
