# I-Lang Proposal — Media Regions and Layers

::STATE{@PROPOSAL, id:MEDIA-REGIONS-LAYERS, status:open, filed:2026-09-12, normative:false}
::STATE{@PROPOSAL, layer:expression, extends:SPEC-v4.1-MEDIA-PROFILE, version:unassigned}
::STATE{@PROPOSAL, authors:Max(@SUN)+CC(@CLAUDE), filed_by:@SUN}

Purpose: record, with a date, that region, mask and layer operations on media artifacts have
been identified and scoped as the next extension of the expression layer, and set out the
constraints any design for them has to meet.

SPEC-v4.1-MEDIA-PROFILE §4.4.7 names these operations as outside the media profile. That was
a decision rather than an oversight: they need addressing the current grammar does not carry,
and approximating them inside v4.1 would have fixed a weak design in place. This proposal
opens the question instead of leaving it implicit.

::CLAUSE{SCOPE|conf:confirmed|scope:proposal}
T:non_normative|registers_no_key_no_entity_no_verb
T:core_29_modifiers_and_media_profile_20_unchanged
T:scope=region_and_mask_operations+layer_and_canvas_composition
A:treating_any_candidate_in_this_document_as_registered⇒misread

---

## 1. What is being scoped

**Region and mask operations.** Changing part of an existing image while keeping the rest:
regenerating a masked area, extending the frame beyond its edge, replacing an object, selecting
an area by point, box or painted mask. These are routine operations in image production, and a
request for one currently has no structured form.

**Layer and canvas composition.** An artifact built from ordered parts: a background, one or more
subjects, a text overlay, each of which can be generated, replaced or reordered on its own. A
poster or a thumbnail is usually made this way.

## 2. Why v4.1 does not already cover them

| Gap | Detail |
|-----|--------|
| Two-dimensional addressing | `rng` is a one-dimensional `start:end` interval. `col` and `row` are table indices. None of them locates an area of a frame. |
| Addressing inside a value | The key=value grammar has no way to point into part of a value, so a region cannot be attached to one reference among several. |
| A different abstraction | `@IMG` is a single frame. A layered document is a container of frames with an order, which is a different kind of target. |

## 3. Constraints any design has to meet

1. **No new verbs unless one is shown to be inexpressible with the 88.** The registry already holds verbs a design should try first: `FILL` for filling a selected area, `EXTC` for taking an area out, `SPLIT` for separating an artifact into parts, `MERGE` for composing parts, `SET` for assigning a part.
2. **New keys follow the v4.1 naming rule**: three letters, lower case, checked one letter apart and transposed against the 29 core keys and the 20 profile keys.
3. **Coordinates are vendor-neutral.** A region has to be expressible without depending on one system's pixel grid, for example in normalised units, while still allowing absolute pixels where a request needs them.
4. **A mask can be given by reference as well as by geometry**, so an existing mask asset can be named rather than redrawn.
5. **The key=value grammar stays intact**: no nested equals signs and no dotted paths.
6. **Core counts stay as they are.** Anything this proposal registers is counted in its own table, as the media profile is.

## 4. Candidate directions

These are directions to evaluate, not decisions.

| Direction | Sketch | Open issue |
|-----------|--------|------------|
| Region as a key value | A registered region key carrying a normalised box or polygon as a quoted string, used with `FILL` on `@IMG` | Quoting and separator rules for coordinate lists |
| Mask as an entity | The mask is an asset addressed like any other source, named through a custom entity or `@PREV` | How to mark the role of mask without adding an entity |
| Layers as declared entities | Each layer is a custom entity introduced with `::STATE`, composed with `MERGE`, ordered by an existing key | Whether an existing key can carry stacking order without changing its meaning |
| A canvas media entity | A fourth media entity for a layered document | Whether a canvas is a target or a container, and what `GEN` on it means |

## 5. Open questions

1. Does a region belong to the target or to the operation?
2. Is stacking order a property of each layer or of the composition?
3. Should outpainting, which enlarges the frame, share a form with inpainting, which works inside it?
4. What is the smallest set of keys that covers point, box, polygon and painted mask?

## 6. Outside this proposal

Transitions between shots, musical tempo, key and metre, and per-reference weighting are recorded
separately in SPEC-v4.1-MEDIA-PROFILE §4.4.7 and are not part of this proposal.

## 7. Status

Open. This document registers nothing. It records that region, mask and layer operations were
identified and scoped as the next expression-layer extension after v4.1.
