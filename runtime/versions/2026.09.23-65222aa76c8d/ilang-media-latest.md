# iLang runtime bundle (media)

Optional extension for image, video and audio work.

Generated from the iLang canon; not edited by hand.
Source: https://github.com/ilang-ai/ilang-spec at commit 09e5a153e08e02bd00fa59f2d1c4b67742666e96 (2026-09-23T00:33:52+08:00).
Contents, in order. Each document states its own status and scope:

1. SPEC-v4.1-MEDIA-PROFILE.md: media profile: image, video and audio vocabulary (v4.1). sha256:065c94ad795a9604afbd57515f88a6925af7df6d4699b81bebdccf2262524078
2. SPEC-v4.2-MEDIA-REGIONS-AND-LAYERS.md: media regions, masks and image layers (v4.2). sha256:5dde4ceaa2f16eaab697e42b83df5e0e4d22a9bcfb1e8b83ee16fc0187e181a4

===== BEGIN SPEC-v4.1-MEDIA-PROFILE.md =====

# iLang v4.1 — Media Profile and Media Entities

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

===== END SPEC-v4.1-MEDIA-PROFILE.md =====

===== BEGIN SPEC-v4.2-MEDIA-REGIONS-AND-LAYERS.md =====

# iLang v4.2: Media Regions and Image Layers

::STATE{@SPEC, id:v4.2-MEDIA-REGIONS-AND-LAYERS, layer:expression, status:adopted, date:2026-09-18}
::STATE{@SPEC, extends:SPEC-v4.1-MEDIA-PROFILE, stable_line:v4, builds_on:SPEC-v4.0-FINAL}
::STATE{@SPEC, adopts:PROPOSAL-MEDIA-REGIONS-AND-LAYERS, proposal_filed:2026-09-12, proposal_first_release:v4.1.0}
::STATE{@SPEC, authors:Long_Quan_Zhu(Max/@SUN)+CC(@CLAUDE), orcid:0009-0004-4540-8082, registered_by:@SUN, registered:2026-09-18}
::STATE{@SPEC, first_published:release_v4.2.0}
::STATE{@SPEC, core_modifiers:29, media_profile:20, both_unchanged:true, region_body_keys:4, counted_separately:true}
::STATE{@SPEC, entities_core:8, entities_external:6, entities_role:8, media_tier:3, all_unchanged:true}
::STATE{@SPEC, verbs:88, verbs_unchanged:true, greek_aliases:13, aliases_unchanged:true, structural_declarations:32, declarations_unchanged:true}
::STATE{@SPEC, judgment_layer_touched:false, see:SPEC-v5.0-PRE}


Purpose: SPEC-v4.1-MEDIA-PROFILE §4.4.7 left two things outside the media profile: region and mask operations, and layer and canvas composition. PROPOSAL-MEDIA-REGIONS-AND-LAYERS, filed on 2026-09-12 and published in release v4.1.0, scoped them and set six constraints. This document meets those constraints with the vocabulary the protocol already has. It adds no verb, no core modifier, no profile key, no registered entity and no declaration type.

A region is a custom entity whose `::STATE` body carries its geometry. An image layer is a custom entity named on a line of a `::LIST` that a `MERGE` composes. Operations reach a region through `whr=`, and the line order of the list is the stacking order. The composite result is an `@IMG` artifact, so no canvas entity is registered.

This is an expression-layer extension on the v4 stable line. It does not touch the v5.0 judgment layer: the 11 dimensions, the 8 modes, the reference function and the JUDGE schema are unchanged.

The whole normative change is four pieces of text, set out with the lines they amend in §4.12: the value domain of `whr` inside media operations, a table of four region body keys, image layers as media targets, and a clause giving `::LIST` line order a meaning where image layers are composed.

::CLAUSE{SCOPE|conf:confirmed|scope:v4.2}
T:expression_layer_extension|extends_SPEC-v4.1_§4.4_§5.4
T:no_new_verbs|88_reaffirmed
T:no_new_core_modifiers|core_29_closed_and_unchanged
T:no_new_profile_keys|media_profile_20_unchanged
T:no_registered_entity|regions_masks_and_image_layers_are_document_scoped_custom_entities
T:no_canvas_entity|composite_result_is_an_image_artifact
T:region_body_keys_4|declaration_body_keys|counted_separately|not_modifiers
T:whr_value_domain_widened_inside_media_operations|meaning_unchanged
T:list_order_is_stacking_order_where_image_layers_are_composed
T:judgment_layer_untouched|11_dims+8_modes+f_v5+JUDGE_schema_unchanged
A:reading_region_body_keys_as_modifier_keys⇒drift
A:writing_geometry_inside_a_modifier_value⇒misparse
A:adding_a_key_or_entity_for_image_layers⇒contradicts_this_extension

---

## 4.5 Media Regions

### 4.5.1 Addressing an area with `whr`

Inside a media operation (§4.4.1 position 1, as amended in §4.6.1) on a verb to which §4.5.6 gives `whr` an area, `whr` names the area of the frame that the operation acts on. It takes one of three values:

1. A region entity (§4.5.2): `whr=@SKY`.
2. An entity whose artifact is a mask (§4.5.5), including `@PREV` after a step that produced one: `whr=@PREV`.
3. A condition string that describes the area, interpreted contextually as SPEC.md §4.2 states for every `whr`: `whr="the sky above the roofline"`.

The key keeps its registered meaning, a filter or match condition: an area is the part of a frame that matches. What widens is the value domain, from a string to a string or an entity, in the way §4.4.4 widened `frm` and `to` to entities. Geometry is never written inside the value. It lives in the declaration of the region entity, so the key=value grammar carries no nested list, no nested equals sign and no dotted path.

Outside media operations `whr` is unchanged.

::CLAUSE{WHR-MEDIA|conf:confirmed|scope:v4.2}
T:inside_media_operations_on_the_verbs_to_which_§4.5.6_gives_an_area_whr_names_the_area_of_the_frame_the_operation_acts_on
T:value=region_entity|mask_entity|condition_string
T:meaning_unchanged=filter_or_match_condition|value_domain_widened_to_entities|precedent_v4.1_§4.4.4_frm_to
T:outside_media_operations_whr_is_unchanged
T:on_a_media_verb_without_an_area_in_§4.5.6_a_condition_string_in_whr_reads_as_before
T:reading_change_from_v4.2.0=an_entity_in_whr_on_an_area_verb_was_a_condition_string|now_names_an_area|recorded_in_§4.12.5
A:entity_in_whr_on_a_media_verb_without_an_area_in_§4.5.6⇒reported|not_guessed
A:entity_in_whr_that_is_neither_a_region_nor_holds_a_mask⇒reported
A:geometry_written_inside_a_modifier_value⇒not_defined|declare_a_region_entity
A:src_or_ref_used_to_name_a_mask⇒drift|src_is_consumed_payload|ref_is_a_borrowed_look

### 4.5.2 Declaring a region

A region is a custom entity (SPEC.md §5.3) introduced by `::STATE` with exactly one region body key on a body line:

```
::STATE{@SKY, scope:session}
  bnd:[0.00,0.00,1.00,0.45]
```

A geometry key is written as a B4 vector line and `msk` as a B2 field line (SPEC-v5.0-PRE Part III §1.2). Neither is written in the header, where a comma separates fields. A region body carries its one region body key and nothing else. `scope:` is a header field and stays in the header, as in the example; any other body key has no meaning on a region.

A region is document scoped like every custom entity and is not added to the entity registry. The Core, External, Role and Media tiers keep 8, 6, 8 and 3, in the way SPEC-v5.0-PRE Part III §2.3 keeps its identity conventions out of the registered count.

A region belongs to the operation that names it, not to the target artifact. One region can serve several operations, and an artifact carries no region of its own.

### 4.5.3 Region body keys (4)

| Key | Line form | Selects |
|-----|-----------|---------|
| pts | `pts:[x,y,...]`, one or more points | The object or area that contains the points. The implementation resolves the extent and reports the extent it used. |
| bnd | `bnd:[x1,y1,x2,y2]` | The axis-aligned rectangle with top left corner (x1,y1) and bottom right corner (x2,y2), where x1 < x2 and y1 < y2. |
| vtx | `vtx:[x1,y1,x2,y2,x3,y3,...]`, three or more vertices | The polygon through the vertices in order, closed from the last vertex back to the first. |
| msk | `msk:value`, a path, URI or entity | The area marked by an existing mask asset (§4.5.5). |

Point, box, polygon and painted mask each have one key, and no smaller set covers the four without overloading a key. A shape outside them, such as an ellipse, a rotated rectangle or several separate areas, is written as a polygon or as a mask.

A region body key is a declaration body key, in the sense of `V:` under `::JUDGE` or `ACCEPT:` under `::OBJECTIVE` (SPEC-v5.0-PRE Part III §1.4). It is never an operation modifier: `[FILL:@IMG|bnd=...]` carries an unregistered modifier and is reported as E302. Outside the body of a region declaration the four names have no meaning.

::CLAUSE{REGION-KEY-COUNT|conf:confirmed|scope:v4.2}
T:region_body_keys=4|pts+bnd+vtx+msk
T:counted_separately|not_core_modifiers|not_media_profile_keys
T:in_force_only_on_body_lines_of_a_::STATE_that_introduces_a_region
T:core_modifiers=29_and_media_profile=20_unchanged_by_this_table
T:registered_2026-09-18_by_@SUN|procedure_as_v4.1_MOD-COUNT
A:region_body_key_used_as_an_operation_modifier⇒E302
A:citing_a_region_key_total_without_amending_this_table⇒drift

### 4.5.4 Coordinates

Axes. Every coordinate pair is written x first, then y. The origin is the top left corner of the frame, x grows to the right and y grows downward.

Frame. Coordinates are measured in the frame of the artifact that the operation produces. For `FILL`, `EXTC`, `SPLIT` and every other operation that keeps the frame, this is the frame of the input artifact. For `EXPD` it is the enlarged frame. For an operation on an image layer it is the composite frame (§4.6.3).

Units. All items on one geometry line use one of two units:

- Normalised: a decimal from 0.00 to 1.00 with two to four decimal places. 0.00 is the left or top edge and 1.00 the right or bottom edge, so `bnd:[0.00,0.00,1.00,1.00]` is the whole frame on any grid.
- Absolute: a non-negative integer followed by `px`, counting pixels of the frame's own grid from 0. A rectangle covers x1 ≤ x < x2 and y1 ≤ y < y2, so `bnd:[0px,0px,2048px,1152px]` is the whole of a 2048x1152 frame.

A line that mixes the two units or writes a bare integer carries an invalid value (E303). Normalised units are the ordinary choice because they do not depend on one system's pixel grid. Absolute units serve a request that has to land on exact pixels. They need a known grid, so an operation that uses them and changes the frame size states `rsl`; `asp` alone does not fix a grid.

A system that uses another convention, such as an origin at the bottom left or a width and height in place of the second corner, converts at its own boundary, in the way §4.4.8 leaves the conversion of an adherence dial to the implementation.

::CLAUSE{REGION-COORDINATES|conf:confirmed|scope:v4.2}
T:pair_order=x_then_y|origin=top_left|x_grows_right|y_grows_down
T:frame=the_frame_of_the_artifact_the_operation_produces
T:normalised=decimal_0.00_to_1.00|two_to_four_decimal_places
T:absolute=non_negative_integer_with_px|pixels_of_the_frame_grid_from_0|rectangle_upper_edges_exclusive
T:one_unit_per_geometry_line
T:absolute_units_with_a_frame_size_change⇒the_operation_states_rsl
A:mixed_units_or_bare_integer_on_a_geometry_line⇒E303

### 4.5.5 Masks

A mask is an image with the aspect ratio of the frame. White marks the area, black marks what lies outside it, and grey marks partial coverage, which is how a soft edge is carried. A mask on a different pixel grid is scaled to the frame. A mask whose aspect ratio differs from the frame is reported rather than stretched.

A mask is named in one of two ways. A region body names an existing mask asset with `msk`. An operation names a mask held by an entity directly with `whr`, which is the usual form in a chain (`whr=@PREV`). Painting a mask is a tool action outside the protocol; the painted file is then named with `msk`.

A mask is produced with `EXTC` and `typ=mask` (§4.7.3). `typ` is the core key for the expected type of a result, typed as a string in SPEC.md §4, and SPEC.md §10.1 already writes `typ=topic`. `mask` is a value of that key, not a new key.

### 4.5.6 `whr` on each verb

| Verb | `whr` names | Outside the area |
|------|-------------|------------------|
| FILL | The area regenerated. Inpainting and object removal. | Unchanged. |
| EXPD | The area added beyond the edges of the source, measured in the enlarged frame. Outpainting. | The source, unchanged. |
| EXTC | The area taken out: a mask with `typ=mask`, otherwise the content of the area. | Not in the result; transparent when `plc=transparent` and `fmt=png` are written (§4.4.4). |
| SPLIT | The area separated onto its own image layer. | The rest of the frame, on the image layer beneath, with the area filled as its surroundings continue. |
| GEN, CREA or FILL on an image layer | Where the new content is placed in the layer's frame. | Transparent for GEN and CREA; unchanged for FILL. |
| SET on an image layer | Where the asset named by `src` is placed, fitted inside the area's bounding rectangle with its aspect ratio kept and centred in it. Without `whr` the area is the whole frame. | Transparent. |
| GEN on `@IMG` | Where the stated subject is placed. | Generated as usual. |
| MERGE | No area, as for a verb outside this table: a condition string reads as SPEC.md §4.2 states and an entity is reported. Stacking order is list order and placement is written inside each image layer (§4.6). | |

A verb not in this table, and `MERGE` inside it, gives `whr` no area meaning. On such a verb an entity in `whr` is reported rather than guessed at, and a condition string reads as SPEC.md §4.2 states, unchanged. On the verbs of this table an entity that is neither a region nor holds a mask is reported in the same way.

This is where v4.2 changes the reading of an earlier document, and it is the only operation-syntax reading it changes: before v4.2.0 an entity written in `whr` on one of these verbs was a condition string that happened to start with `@`, and the released validator accepts it; from v4.2.0 it names an area. The change is recorded in §4.12.5.

Outpainting and inpainting therefore share one form, a region named with `whr`, and differ by verb: `FILL` works inside the frame and `EXPD` works beyond its edges, which is the division §5.4 already makes when it assigns extension to `EXPD`.

`SPLIT` with `whr` returns two image layers whose merge reproduces the source: the lower one is the frame with the area filled, the upper one holds the area on transparency.

---

## 4.6 Image Layers

### 4.6.1 Definition and media target

An image layer is an image artifact that takes part in a composite. It is a custom entity, not a registered one, and it has no key of its own. An entity is an image layer when it is named on a body line of a `::LIST` that a `MERGE` on a media target consumes, either through `src=` or as the output of the step before it in the same chain (§4.6.2). Its look may be declared with `::STATE` as §4.4.5 describes for any preset.

An image layer is a media target. It resolves to `@IMG` for §4.4.1: in an operation whose target is an image layer, and in the `::STATE` body of an image layer, the profile keys in force are the keys in force on `@IMG`. `dur`, `fps` and `mvt` therefore have no meaning on an image layer.

One entity is either a region or an image layer, not both. A composite result is an `@IMG` artifact. A layered composite is a way of making an image rather than a different kind of artifact, which keeps the reading of §5.4 that a media entity states what an artifact is, and it is why no canvas entity is registered.

::CLAUSE{IMAGE-LAYER|conf:confirmed|scope:v4.2}
T:image_layer=custom_entity_named_on_a_::LIST_line_that_MERGE_on_a_media_target_consumes|through_src_or_from_the_previous_step
T:image_layer_is_a_media_target|resolves_to_the_image_entity_for_v4.1_§4.4.1_positions_1_and_2
T:image_layers_of_one_composite_share_the_composite_frame|transparent_where_empty
T:placement=content_inside_the_layer_frame|written_with_whr_when_the_layer_is_made
T:composite_result=@IMG|no_canvas_entity
T:one_image_layer_has_one_frame|composites_that_name_it_share_that_frame
T:composite_frame_order=asp_rsl_on_MERGE|then_the_frame_the_bottom_image_layer's_operation_would_have_on_its_own_under_§4.5.4|else_reported
A:key_for_image_layers_or_for_a_layer_position⇒not_registered|use_list_order
A:one_entity_as_both_region_and_image_layer⇒reported
A:one_image_layer_named_by_two_composites_with_different_frames⇒reported|not_rescaled
A:image_layer_asp_or_rsl_differing_from_the_composite_frame⇒reported|not_rescaled
A:region_or_mask_entity_in_whr_on_MERGE⇒reported|placement_is_inside_each_image_layer
A:the_bare_word_layer_as_a_key_or_entity_name⇒drift|layer_already_names_protocol_layers

### 4.6.2 Stacking order

Where image layers are composed, list order is stacking order. The first item is the bottom image layer, and each later item lies above every item before it. The rule applies to three lists: the body lines of a `::LIST` that a `MERGE` on a media target consumes, the list that a `SPLIT` on a media target returns, and a list that a `MERGE` on a media target takes from `@PREV`.

```
::LIST{@POSTER}
  @BASE
  @PHOTO
  @TITLE
```

`@BASE` is at the bottom and `@TITLE` on top. Stacking order is a property of the composition, so one image layer can sit at different heights in two lists that share a frame (§4.6.3). There is no per-layer order key. `pri` (task scheduling priority), `top` (a count, Top N) and `dep` (traversal depth) do not carry stacking order.

Every other `::LIST` keeps its line order with no meaning attached, as before.

::CLAUSE{LIST-ORDER|conf:confirmed|scope:v4.2}
T:where_image_layers_are_composed_list_order_is_stacking_order
T:first_item=bottom|each_later_item_above_all_earlier_items
T:applies_to=::LIST_consumed_by_MERGE_on_a_media_target|list_returned_by_SPLIT_on_a_media_target|list_taken_by_MERGE_on_a_media_target_from_the_previous_step
T:every_other_::LIST_keeps_line_order_without_meaning
A:pri_top_or_dep_as_a_stacking_position⇒drift

### 4.6.3 Composition

`MERGE` on a media target composes the image layers of its list, bottom to top, into one `@IMG` artifact. The composite frame is fixed in this order: the `asp` and `rsl` that the `MERGE` states; otherwise the frame that the operation making the bottom image layer would have on its own, taking the rule of §4.5.4 for its verb and leaving aside that section's sentence on image layers: the input frame for an operation that keeps the frame (`FILL`, `EXTC`, `SPLIT`, or `SET` of a whole asset) or the `asp` and `rsl` stated by an operation that sets one (`CREA`, `GEN`, `EXPD`); otherwise the frame is undefined and the `MERGE` is reported as an incomplete composite (§4.14). With `asp` and no `rsl` the aspect ratio is fixed and the pixel grid is the implementation's, so a region written in `px` on that composite needs `rsl` (§4.5.4). Every image layer of that list is made on the composite frame, and it is transparent wherever it has no content, so an upper image layer covers a lower one only where it has content. An operation that makes an image layer may state `asp` or `rsl`; where they differ from the composite frame, however it was fixed, that image layer is reported rather than rescaled.

An image layer has one frame. Where one image layer is named on two lists, the two composites share a frame, each fixed by the order above. Two composites with different frames do not share an image layer. An implementation reports the second use rather than rescaling the layer, and a document that wants the same content on two frames makes two image layers.

Replacing one image layer and merging again leaves the other image layers untouched. That is the reason to compose an image rather than regenerate it flat.

---

## 4.7 Operation Map

Nine of the ten operations in the proposal's scope are written with a registered verb; reordering is a rewritten `::LIST` and needs no verb. The storage step that closes an example is `WRIT`. None needs a verb outside the 88.

| Operation | Verb | Keys that carry it |
|-----------|------|--------------------|
| Inpaint | FILL | `src`, `whr` with a region, profile keys for the new content |
| Remove an object | FILL | `whr` with a region or description, `exc` naming the object as a noun (§4.4.4) |
| Select to mask | EXTC | `whr` with a `pts`, `bnd` or `vtx` region or a description, `typ=mask` |
| Split into image layers | SPLIT | `src`, `lim` for the number of image layers, or `whr` for one area |
| Composite | MERGE | `src` naming a `::LIST`, `asp`, `rsl`, `fmt` |
| Reorder | A rewritten `::LIST` | None. Line order is the order (§4.6.2). |
| Replace an image layer | SET, or GEN on the image layer | `src` for an existing asset, profile keys for a new one |
| Blank canvas | CREA | `asp`, `rsl`, `pal` or `plc=transparent`, `fmt` |
| Text layer | GEN on an image layer | `txt`, `mdm`, `pal`, `plc=transparent`, `whr` |
| Outpaint | EXPD | `src`, `asp`, `rsl`, `whr` for the added area |

### 4.7.1 Inpaint

```
::STATE{@SKY}
  bnd:[0.00,0.00,1.00,0.42]

[FILL:@IMG|src=assets/harbour.jpg,whr=@SKY,sbj="low storm clouds",lgt="flat grey daylight"]=>[WRIT:@LOCAL|path=out/harbour-storm.png]
```

Everything below 0.42 of the frame height is kept. The new sky is described with profile keys, as any generated content is.

### 4.7.2 Remove an object

```
::STATE{@BIN}
  vtx:[0.62,0.55,0.71,0.53,0.73,0.80,0.61,0.82]

[FILL:@IMG|src=assets/street.jpg,whr=@BIN,exc="rubbish bin",plc="the pavement continues"]=>[WRIT:@LOCAL|path=out/street-clean.png]
[FILL:@IMG|src=assets/street.jpg,whr="the rubbish bin by the door",exc="rubbish bin"]=>[WRIT:@LOCAL|path=out/street-clean-b.png]
```

Removal is filling with the object excluded. The exclusion is written as a noun, as §4.4.4 requires, so the profile needs no removal key. The second line locates the object by description instead of by polygon.

### 4.7.3 Select to mask

```
::STATE{@DOG_SEED}
  pts:[0.41,0.58]

[EXTC:@IMG|src=assets/park.jpg,whr=@DOG_SEED,typ=mask,fmt=png]=>[WRIT:@LOCAL|path=masks/dog.png]
```

The saved mask is later named by reference:

```
::STATE{@DOG}
  msk:masks/dog.png

[FILL:@IMG|src=assets/park.jpg,whr=@DOG,sbj="a sleeping fox"]=>[WRIT:@LOCAL|path=out/park-fox.png]
```

Or, in one chain, the mask is used where it is made:

```
[EXTC:@IMG|src=assets/park.jpg,whr="the dog",typ=mask,fmt=png]=>[FILL:@IMG|src=assets/park.jpg,whr=@PREV,sbj="a sleeping fox"]=>[WRIT:@LOCAL|path=out/park-fox.png]
```

`src` stays on the photograph in the second step, so the mask from `@PREV` is not consumed as picture content; it only locates the area.

### 4.7.4 Split into image layers

```
[SPLIT:@IMG|src=assets/flat-poster.png,lim=3,fmt=png]=>[WRIT:@LOCAL|path=layers/]
```

The result is a list of three image layers, bottom first. With `whr` the split separates one area:

```
::STATE{@RIDER}
  bnd:[0.30,0.20,0.62,0.95]

[SPLIT:@IMG|src=assets/street.jpg,whr=@RIDER,fmt=png]=>[MERGE:@IMG|fmt=png]=>[WRIT:@LOCAL|path=out/street-roundtrip.png]
```

The `MERGE` takes the two image layers from `@PREV` in stacking order and reproduces the source, which is the property §4.5.6 states for `SPLIT` with `whr`.

### 4.7.5 Composite

```
::STATE{@PHOTO, mdm:photo, pal:warm_tones}

::LIST{@POSTER}
  @BASE
  @PHOTO
  @TITLE

[MERGE:@IMG|src=@POSTER,asp=4:5,rsl=1080x1350,fmt=png]=>[WRIT:@LOCAL|path=out/poster.png]
```

`@BASE`, `@PHOTO` and `@TITLE` are image layers because the list that names them is consumed by a `MERGE` on `@IMG`. The `::STATE` line gives `@PHOTO` defaults, which apply because an image layer is a media target.

### 4.7.6 Reorder

Reordering is writing the list in the new order. A second list names the same image layers in another order, and a `MERGE` on it composes them that way:

```
::LIST{@POSTER_B}
  @BASE
  @TITLE
  @PHOTO

[MERGE:@IMG|src=@POSTER_B,asp=4:5,rsl=1080x1350,fmt=png]=>[WRIT:@LOCAL|path=out/poster-b.png]
```

No operation carries a stacking order in a modifier value. A list of entities inside a value would be the same writing that §4.5.1 keeps geometry out of, and `srt` keeps its registered reading, a field to sort by (SPEC.md §4).

### 4.7.7 Replace an image layer

```
::STATE{@PHOTO_AREA}
  bnd:[0.00,0.00,1.00,0.66]

::LIST{@POSTER}
  @BASE
  @PHOTO
  @TITLE

[SET:@PHOTO|src=assets/beach-v2.jpg,whr=@PHOTO_AREA]=>[MERGE:@IMG|src=@POSTER,asp=4:5,rsl=1080x1350,fmt=png]
[GEN:@PHOTO|sbj="two surfers carrying boards",plc="a wide beach at low tide",mdm=photo,whr=@PHOTO_AREA]=>[MERGE:@IMG|src=@POSTER,asp=4:5,rsl=1080x1350,fmt=png]
```

`SET` assigns an existing asset to the image layer. `GEN` on the image layer makes new content for it. Either way `@BASE` and `@TITLE` are not regenerated.

### 4.7.8 Blank canvas

```
::LIST{@POSTER}
  @BASE
  @PHOTO
  @TITLE

[CREA:@BASE|asp=4:5,rsl=1080x1350,pal="#F4EFE6",fmt=png]
[MERGE:@IMG|src=@POSTER,asp=4:5,rsl=1080x1350,fmt=png]
```

A blank asset is `CREA` with a media target (§5.4), here an image layer filled with one colour. A transparent blank image outside any composite is `[CREA:@IMG|rsl=1080x1350,plc=transparent,fmt=png]`, using the transparency pair of §4.4.4.

### 4.7.9 Text layer

```
::STATE{@TITLE_BAND}
  bnd:[0.06,0.72,0.94,0.88]

::LIST{@POSTER}
  @BASE
  @PHOTO
  @TITLE

[GEN:@TITLE|txt="SUMMER SALE",mdm="bold condensed sans-serif lettering",pal="#FFFFFF",plc=transparent,whr=@TITLE_BAND,fmt=png]
[MERGE:@IMG|src=@POSTER,asp=4:5,rsl=1080x1350,fmt=png]
```

The words go on `txt`, reproduced verbatim (§4.4.2). The band fixes where they sit, and the rest of the image layer stays transparent.

### 4.7.10 Outpaint

```
::STATE{@NEW_RIGHT}
  bnd:[1728px,0px,2048px,1152px]

[EXPD:@IMG|src=assets/beach-3x2.png,asp=16:9,rsl=2048x1152,whr=@NEW_RIGHT,plc="the shoreline and the dunes continue"]=>[WRIT:@LOCAL|path=out/beach-16x9.png]
```

The source is 1728x1152. The region is written in pixels of the enlarged 2048x1152 frame and names the 320 pixel strip added on the right, which is why the operation states `rsl`.

---

## 4.8 Boundaries

Each pair below can be mistaken for the other, so the division is fixed here.

| Pair | Division |
|------|----------|
| whr / src | `src` is the payload an operation consumes. `whr` locates the area it acts on. A mask named by `whr` is not consumed as picture content. |
| whr / ref | `ref` borrows a look. `whr` locates an area. Neither does the other's job. |
| whr / rng | `rng` is a one-dimensional `start:end` interval. `whr` in a media operation is an area of a frame. |
| bnd / rsl, asp | `bnd` is an area inside a frame. `rsl` and `asp` are the geometry of the frame itself. |
| pts / sbj | `sbj` states that a subject is the same subject as another. `pts` states where something is in this frame. |
| msk / ref | `msk` names the asset that defines an area. `ref` names an asset whose look is borrowed. |
| FILL / EXPD | `FILL` changes an area inside the frame. `EXPD` adds area beyond the edges. Both locate with `whr`. |
| region / image layer | A region is an area that operations act on. An image layer is content that a composite stacks. One entity is never both. |
| list order / pri, top, dep | Stacking order is list order. `pri` is scheduling, `top` is a count, `dep` is traversal depth. |
| image layer / preset | A preset (§4.4.5) is named with `ref=` and lends its keys. An image layer is named on a composed `::LIST` and is content. A `::STATE` body can serve an image layer as defaults, as it serves `@IMG`. |

---

## 4.9 Naming

The four region body keys follow the rules of §4.4.6.

They are three letters, lower case, built by truncation: `pts` for points, `bnd` for bounds, `vtx` for vertices, `msk` for mask.

The one-letter check was run against the 29 core keys, the 20 profile keys and each other, counting a substitution, a transposition, one inserted or deleted letter and a prefix. There were no hits. The check applies even though these are body keys and not modifiers: a `::STATE` body also carries core and profile keys as defaults (§4.4.5), so a mistyped geometry key that landed on one of them would be read silently as a default.

Each name was also checked against every value the dictionary lists for a modifier, the rule under which `med` was rejected. None of the four is a legal value.

Names rejected under these rules, recorded so the question is not reopened:

| Name | Reason |
|------|--------|
| `box` | One letter from the core key `bot`. |
| `ply` | One letter from the profile keys `plc` and `qly`. |
| `rct` | One letter from the profile key `act`. |
| `rec` | One letter from the profile key `ref`. |
| `reg` | One letter from `rng` and from `ref`. |
| `rgn` | A transposition of `rng`. |
| `roi` | One letter from `row`. |
| `pol` | One letter from `col`, `pov` and `pal`. |
| `shp` | One letter from `scp`. |
| `pth` | One letter deleted from `path`. |
| `sel` | One letter from `sed`. |
| `zon` | One letter from `ton`. |
| `pos` | One letter from `pov`. |
| `pgn` | Passes the key check but transposes to `png`, a legal value of `fmt`. |
| `mask` | Four letters, and identical to the value this extension gives `typ`. |
| `poly`, `rect` | Four letters, against the three-letter truncation habit. |

Names that pass and were not taken: `crd` reads as card; `geo` is too general and sits one letter from the verbs `GET` and `GEN`; `loc` reads as location and prefixes the value `local`; `are` is an English word; `aoi` and `bbx` are initialisms, and §4.4.6 allows one initialism, `fps`, because it is the term in ordinary use.

Near matches in other slots are recorded and do not disqualify, as in §4.4.6. `msk` is one letter from the value `mask` that `typ` takes in §4.5.5. The two sit in different lexical slots, a body key and a modifier value, but a writer who types `typ=msk` produces an unknown value of an open key, which a validator does not catch.

The word layer. The canon already uses layer for protocol layers (the header field `layer:expression` of this document and of SPEC-v4.1), for the judgment layers A, B and C of SPEC-v5.0-PRE Part I, and for the SOUL layer of SPEC.md §7. This extension therefore writes image layer in prose, registers no key or entity named layer, and uses no `LAYER` token in its examples.

---

## 4.10 Outside this extension

Recorded so that each absence is a decision rather than an oversight.

| Not defined | Reason |
|-------------|--------|
| Regions on `@VID` and `@AUD` | An area that moves over time needs tracking and a timeline binding. This extension defines regions on still frames: `@IMG` and image layers. |
| Exclusion points, and the union or subtraction of areas | One region carries one geometry key. A combined area is written as one mask. |
| Ellipses, rotated rectangles and curves | Written as a `vtx` polygon or a `msk` mask. |
| Opacity and blend modes | Compositing parameters with no key among the 29 or the 20. Not approximated with an existing key. |
| A composite inside a composite | A list item is an image layer, not a list. Merge the inner composite to an image first and name that image as an image layer. |
| Moving, scaling or rotating an image layer after it is made | Remake the image layer with `whr`, or `SET` its asset again with another region. |
| A canvas entity | A composite result is an `@IMG` artifact (§4.6.1). |
| Painting a mask | A tool action. The painted file is named with `msk`. |
| Edge softness as a number | Grey values in a mask carry soft edges. |
| A region attached to one reference among several | The key=value grammar does not address inside a value (proposal §2, SPEC-v4.1-MEDIA-PROFILE §4.4.7 on per-reference weighting). Two references with two areas are two operations joined by a pipe, each with its own `whr`. |

---

## 4.11 Worked example, poster

Before, a request in prose:

```
make a 4:5 poster, 1080x1350 png. warm cream background. put my beach photo in the
top two thirds but take out the bin on the left of the photo. big white SUMMER SALE
lettering across the lower band. then try the second beach photo instead and keep
everything else the same.
```

After:

```
::STATE{@BIN}
  vtx:[0.05,0.38,0.14,0.37,0.15,0.62,0.04,0.63]
::STATE{@PHOTO_AREA}
  bnd:[0.00,0.00,1.00,0.66]
::STATE{@TITLE_BAND}
  bnd:[0.06,0.72,0.94,0.88]

::LIST{@POSTER}
  @BASE
  @PHOTO
  @TITLE

[CREA:@BASE|asp=4:5,rsl=1080x1350,pal="#F4EFE6",fmt=png]
[FILL:@IMG|src=assets/beach.jpg,whr=@BIN,exc="rubbish bin",plc="the sand continues"]=>[SET:@PHOTO|src=@PREV,whr=@PHOTO_AREA]
[GEN:@TITLE|txt="SUMMER SALE",mdm="bold condensed sans-serif lettering",pal="#FFFFFF",plc=transparent,whr=@TITLE_BAND,fmt=png]
[MERGE:@IMG|src=@POSTER,asp=4:5,rsl=1080x1350,fmt=png]=>[WRIT:@LOCAL|path=out/summer-sale.png]

[SET:@PHOTO|src=assets/beach-2.jpg,whr=@PHOTO_AREA]=>[MERGE:@IMG|src=@POSTER,asp=4:5,rsl=1080x1350,fmt=png]=>[WRIT:@LOCAL|path=out/summer-sale-2.png]
```

Notes on the rewrite. The prose mixed three kinds of statement: what the image layers are, where things sit, and what to do. They separate here into the `::LIST`, the three region declarations and the operation lines. `@BIN` is measured in the frame of `assets/beach.jpg`, because `FILL` produces an artifact in that frame, while `@PHOTO_AREA` and `@TITLE_BAND` are measured in the composite frame, because they are used on image layers. The request to try the second photo is one `SET` and one `MERGE`: the background and the lettering are neither described nor generated again. Stacking needs no key; `@TITLE` is above `@PHOTO` because its line comes later.

---

## 4.12 Amendments

This section states the entire normative change, as four amendments. No released file is edited. SPEC.md, SPEC-v4.0-FINAL.md, SPEC-v5.0-PRE.md and SPEC-v4.1-MEDIA-PROFILE.md stay as released, and each amendment below is read together with the lines it quotes from release v4.2.0 on, in the way SPEC-v4.1 extended SPEC.md §4 and §5 without editing SPEC.md. Line numbers refer to ilang-spec at commit 58d0c86.

### 4.12.1 Amendment 1: the value domain of `whr` inside media operations

Amends SPEC.md:280:

```
| whr | string | Filter/match condition |
```

and SPEC.md:304:

```
- `whr` is a condition string, interpreted by the AI contextually
```

and SPEC-v4.1-MEDIA-PROFILE.md:135:

```
Four core keys carry extended value domains inside media operations, with no new key:
```

From v4.2.0 the sentence at v4.1:135 reads `The core keys below carry extended value domains inside media operations, with no new key:` and the list that follows it carries one more item:

- `whr` widens from a condition string to a region entity, an entity holding a mask, or a condition string, and on the verbs to which §4.5.6 gives an area names the area of the frame that the operation acts on (§4.5.1). On any other verb, `MERGE` included, a condition string reads as before and an entity is reported. An entity in `whr` on an area verb read as a condition string before v4.2.0 and names an area from v4.2.0 on (§4.5.6, §4.12.5).

The released sentence counts four entries for five keys, since `frm` and `to` share one entry. The amended sentence carries no number, so the count cannot drift again; the entries from v4.2.0 are `fmt`, `exc`, `lim`, `frm` and `to`, and `whr`.

Outside media operations SPEC.md:280 and :304 read as released. The meaning of the key, a filter or match condition, is unchanged, which is what SPEC-v4.1-MEDIA-PROFILE.md:64 requires of core keys inside media operations.

### 4.12.2 Amendment 2: the region body key table

Amends SPEC-v5.0-PRE.md:716-717:

```
`R:` and `T:` carry different meanings under different parents. Interpretation is
scoped to the enclosing declaration; there is no global key namespace.
```

and SPEC-v5.0-PRE.md:734:

```
T:unknown_key_in_known_declaration⇒parse_as_B2_field|do_not_reject
```

and uses the B4 form of SPEC-v5.0-PRE.md:663-666 unchanged:

```
::BODY{B4|name:vector}
T:form=`KEY:[item,item,...]`
T:items=scalar|`k=v`_pairs
T:no_nesting|flat_list_only
```

From v4.2.0 the parent-scoped keys of PRE Part III §1.4 include the four region body keys of §4.5.3, with the parent `::STATE` introducing a region, counted by the REGION-KEY-COUNT clause and interpreted by §4.5.4 and §4.5.5. A document that writes one of the four names in any other declaration keeps the reading of PRE:734.

This amendment, with amendment 1, resolves the row at SPEC-v4.1-MEDIA-PROFILE.md:199, which stays in the released text as the record of why the question was deferred:

```
| Region and mask operations | Need two-dimensional coordinates; `rng`, `col` and `row` are one-dimensional or tabular. Left for a later proposal rather than approximated here. |
```

### 4.12.3 Amendment 3: image layers as media targets

Amends SPEC-v4.1-MEDIA-PROFILE.md:61-62:

```
1. In an operation whose target entity resolves to `@IMG`, `@VID` or `@AUD` (§5.4).
2. In a `::STATE` declaration body whose header entity is a media entity, or a preset entity that a media operation names with `ref=` (§4.4.5).
```

From v4.2.0 the two positions read:

1. In an operation whose target entity resolves to `@IMG`, `@VID` or `@AUD` (§5.4), or is an image layer (v4.2 §4.6.1).
2. In a `::STATE` declaration body whose header entity is a media entity or an image layer, or a preset entity that a media operation names with `ref=` (§4.4.5).

Amends SPEC-v4.1-MEDIA-PROFILE.md:267:

```
The target entity determines which profile keys are in force. `dur`, `fps` and `mvt` have no meaning on `@IMG`; `pov`, `fcl`, `lgt` and `pal` have none on `@AUD`. An implementation reports a key that is out of force for the target rather than acting on it.
```

From v4.2.0 one sentence follows it: An image layer is in force as `@IMG` (v4.2 §4.6.1).

This amendment, with amendment 4, resolves the row at SPEC-v4.1-MEDIA-PROFILE.md:200, and leaves its canvas half unregistered for the reason in §4.6.1:

```
| Layer and canvas composition | A multi-layer document is a different abstraction from a generation target. Left for a later proposal. |
```

### 4.12.4 Amendment 4: `::LIST` line order

Amends SPEC-v5.0-PRE.md:763-766:

```
Enumeration block. The header names the collection (`::LIST{@REPOS}`); the body is
one B6 prose line per item. `::LIST` is a declared prose-body type under §1.2 B6.
Registered 2026-08-11 through this section's DECL-COUNT amendment channel, codifying
canon usage in `AUTHORS.md`.
```

From v4.2.0 the paragraph is followed by the LIST-ORDER clause of §4.6.2: where a `MERGE` on a media target consumes the list, body line order is stacking order, first line at the bottom. Every other `::LIST`, including `::LIST{@REPOS}` in AUTHORS.md, keeps line order without meaning.

### 4.12.5 What does not change

Nothing else in the released specification changes. The verb table, the 29 core modifiers and their types apart from amendment 1, the 20 profile keys, the four entity tiers, the 32 structural and 13 narrative declarations and the body form set B1 to B8 stay as released. `typ` keeps its text: §4.5.5 gives it the value `mask` in its open domain. `srt` is not used by this extension.

Two readings of earlier documents change, and no released document gains an error:

1. An entity in `whr` inside a media operation on an area verb of §4.5.6 was a condition string before v4.2.0 and names an area from v4.2.0 on (amendment 1). The released validator accepts such a line and keeps accepting it.
2. A body line of a `::STATE` whose key is `pts`, `bnd`, `vtx` or `msk` was an unknown B2 field under PRE:734 and is a region body key from v4.2.0 on (amendment 2). Its checks (§4.14) are reported as warnings, so a document that was valid before v4.2.0 stays valid; a malformed geometry line is warned about, not rejected.

The public vocabulary line (`88 verbs, 29 core modifiers plus a 20-key media profile, 25 entities (17 addressable, 8 role), 13 Greek aliases`) is unchanged. It counts verbs, modifiers, entities and aliases. Region body keys are none of these, in the same way that the body keys `V:`, `M:` and `R:` are not in it.

::CLAUSE{AMENDMENTS|conf:confirmed|scope:v4.2}
T:amendment_1=whr_value_domain_inside_media_operations|amends_SPEC.md:280+:304+v4.1:135
T:v4.1:135_reads_without_a_number_from_v4.2.0|entries=fmt+exc+lim+frm/to+whr|keys=6
T:amendment_2=region_body_key_table|amends_PRE:716-717+:734|uses_PRE_B4_unchanged|resolves_v4.1:199
T:amendment_3=image_layers_as_media_targets|amends_v4.1:61-62+:267|resolves_v4.1:200
T:amendment_4=::LIST_order_where_image_layers_are_composed|amends_PRE:763-766
T:released_files_not_edited|amendments_read_with_the_quoted_lines_from_v4.2.0
T:reading_changes_from_v4.2.0=entity_in_whr_on_an_area_verb|region_body_keys_in_a_::STATE_body
T:no_released_document_gains_an_error|region_checks_are_warnings
T:public_vocabulary_line_unchanged
A:a_fifth_normative_change_without_amending_this_list⇒drift

---

## 4.13 Closing the proposal

Constraints of PROPOSAL-MEDIA-REGIONS-AND-LAYERS §3:

| Constraint | How it is met |
|------------|---------------|
| 1. No new verbs | Nine of the ten operations in §4.7 use one of `FILL`, `EXTC`, `EXPD`, `SPLIT`, `MERGE`, `SET`, `GEN`, `CREA`; reordering is a rewritten `::LIST` with no verb; storage in the examples is `WRIT`. The count stays 88. |
| 2. New keys follow the v4.1 naming rule | §4.9: three letters, lower case, checked against the 29 and the 20 for substitution, transposition, insertion, deletion and prefix, and against the listed legal values. |
| 3. Vendor-neutral coordinates, absolute pixels allowed | §4.5.4: normalised 0.00 to 1.00 by default, `px` items when a request needs exact pixels, one origin rule for both. |
| 4. A mask by reference as well as by geometry | §4.5.5: `msk` in a region body, or an entity holding a mask in `whr`. |
| 5. The key=value grammar stays intact | No nested equals sign and no dotted path anywhere. Geometry lives on B4 body lines of a declaration, so no modifier value carries a coordinate list either (§4.5.1). |
| 6. Core counts stay; anything registered is counted in its own table | Verbs 88, core modifiers 29, profile 20, entity tiers 8, 6, 8 and 3, structural declarations 32. The only registered item is the table of 4 region body keys, counted by REGION-KEY-COUNT. |

Open questions of §5:

1. A region belongs to the operation, through `whr`. Placement inside an image layer is content of that image layer, written with `whr` when it is made.
2. Stacking order is a property of the composition: list order.
3. Outpainting shares the region form with inpainting and differs by verb, `EXPD` against `FILL`.
4. Four keys: `pts`, `bnd`, `vtx`, `msk`.

Candidate directions of §4: the mask as an entity is adopted, named through `whr` or `msk`. Image layers as declared entities are adopted, ordered by list order rather than by a key. A region as a key value is not adopted: this extension registers no modifier key (SCOPE clause) and addresses a region as an entity that `whr=` names (§4.5.1), so the quoting and separator rules for a coordinate list inside a value, the open issue the proposal records for that direction, do not arise. A canvas media entity is not adopted (§4.6.1).

The proposal's status moved from open to adopted with this document on 2026-09-18. The proposal file is kept as the dated record.

---

## 4.14 Conformance tooling (non-normative)

The reference grammar validator ships in the same repository (SPEC-v5.0-PRE Part III §3). Release 4.2.0 ships the validator change with this text. For this extension the validator provides:

1. Media gating for image layers: an entity named on a `::LIST` line that a `MERGE` on a media target consumes, through `src=` or from the previous step of the chain, is treated as a media target, so profile keys on it are not reported as E302.
2. Region body checks, all at warning level so that no previously valid document becomes invalid: one region body key per region and B4 form for `pts`, `bnd` and `vtx` (structure, E300); one unit per line, item counts, bare integers, and x1 < x2 and y1 < y2 for `bnd` (values, E303).
3. Quote-aware splitting of operation groups and modifiers, so that a bracket or a comma followed by an equals sign inside a quoted value is read as content. In the repository since commit 31e8fc8 (quoted values are opaque).
4. Reports for the frame rules of §4.6.3: a `MERGE` whose composite frame cannot be fixed, an image layer whose stated `asp` or `rsl` differs from the composite frame, and one image layer named on two lists whose composites fix different frames. Reported as warnings (E303) so that no released document becomes invalid, and only where the text decides the frame without inference.
5. Self-test cases for the above (64 in all with the earlier 31), and this document in the canon gate. `SPEC-v4.1-MEDIA-PROFILE.md` is in the gate since commit 31e8fc8.

Reports that depend on what an entity holds at run time, an entity in `whr` that is neither a region nor holds a mask, or an entity in `whr` on `MERGE`, are made by the implementation rather than by the static validator.

===== END SPEC-v4.2-MEDIA-REGIONS-AND-LAYERS.md =====
