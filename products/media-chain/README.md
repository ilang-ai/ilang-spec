# Media Chain 1.2

Media Chain is the provenance layer of iLang for generated images, video and audio: an iLang document that tells an AI agent to write the structured request that produced an artifact and the judgment that allowed it into the artifact's own file, and to record what changed between one version and the next together with the owner's verdict in the owner's words. A delivered picture today has no chain to read when it is wrong. With this product a bad image is a diff of two GEN lines and two V lines: the key or the dimension that moved is where it went wrong, and any model that opens the file reads the whole history without being told anything.

It uses two parts of the canon that already exist and adds nothing to either. The request is the GEN line of SPEC-v4.1-MEDIA-PROFILE (20 media keys, the entities IMG, VID and AUD, adopted 2026-09-12). The judgment is the frozen JUDGE block of SPEC-v5.0 Part II §4 (eleven dimensions, one mode computed by the reference function f_v5). Both are stored verbatim, as iLang text, under the label ai.ilang.chain: inside the file before the generator platform signs it (a PNG text chunk or XMP), so the issuer's credential binds the chain; as one C2PA custom assertion when we are the signer; as an XMP sidecar when the format carries no C2PA at all. The delta of each iteration is written with the declarations the canon already has: FACT for what changed, DECIDE for the owner's verdict, PROGRESS for the series.

Status: 1.2, dated 2026-11-18 (1.1 of 2026-11-15 amended by the owner's word of 2026-11-18 on the counterexample MC-CX-001 in records/), name media-chain final by the owner's word of 2026-11-15; in products/media-chain of ilang-spec since 2026-11-15, first shipped in release 5.0.14.

## Where it goes

| Where | How |
|---|---|
| An agent that generates images or video through an API | Paste this block into the instruction file it reads when it starts. It then writes every request as a GEN line, lets code compute the mode, seals both into the file with c2patool, and records the delta when the owner answers. |
| A pipeline without an agent | The two validators of ilang-spec check the texts; c2patool writes and reads the assertion. The block is the contract the pipeline implements. |
| A chat assistant with no tools | It can write the GEN line and the JUDGE block and hand them back as text. Sealing them into the file needs a tool on the owner's machine. |
| A reader that only receives the file | c2patool reads the assertion; the GEN line and the JUDGE block are plain iLang and validate with the canon's code. No contact with the sender is needed. |

Pasted into a chat, it covers that chat only. To have it every time, put it where instructions persist.

## Give it to your agent

The product above says what a chain is. [mother/MEDIA-CHAIN-MOTHER.ilang.md](mother/MEDIA-CHAIN-MOTHER.ilang.md) is the book an agent runs: paste it into your agent, or into the window of the model that makes your pictures and videos, and from then on nothing is a lucky draw. Every picture and every video comes out with its request and its judgment inside the file. Every version is kept, with what moved since the one before, and your own words on each one are the record. A bad result is not thrown away: it is the difference between two GEN lines and two V lines, and the next line is written from that difference as a proposal you confirm. When a series is done the agent runs the gate of the dataset on it, and on your word opens the pull request; what passes is merged with your words as written.

The book is an iLang engineering book, version 1.1 of 2026-11-17, served at https://ilang.ai/media-chain/MEDIA-CHAIN-MOTHER.ilang.md and MIT like the product. An agent with tools fetches the product (pinned by sha256), the demo series as its template, the two validators and the gate from the canon, writes the chain into the file by the seal rule of line 28 (a PNG text chunk when it holds the bytes before a platform signs them or nobody signs, a C2PA assertion through c2patool for an unsigned JPEG or MP4, a sidecar when the platform handed over a file it already signed), and reads it back before it shows you anything. A chat window with no tools writes the same lines by hand, with the cascade of f_v5 spelled out in the book so the mode is computed and not guessed, and hands you one sidecar text per file to save beside it. Three things the book never does: paraphrase your words inside a DECIDE, write an M line the cascade did not compute, or run the same GEN line twice; a second run changes a key, the seed at least, and the delta names it. The book lints clean in strict mode; its acceptance items are the pinned product hash, the series document through the grammar validator, and the series through the gate.

## Read it line by line

Line numbers are those of [MEDIA-CHAIN.ilang.md](MEDIA-CHAIN.ilang.md).

| Line | Begins | What it makes the AI do |
|---|---|---|
| 1 | `::ILANG::v5.0` | The opening marker: what follows is an iLang document, protocol version 5.0. |
| 2 | `[TYPE:media_chain]…` | The header: a media-chain document named ILANG-MEDIA-CHAIN, version 1.2, dated 2026-11-18, in English. |
| 3 | `[FROM:@ai_chuhai]…` | From the author to the AI agent that loads it; the status is active. |
| 4 | `::STATE{@OWNER…` | Who the owner is: the person whose artifacts these are; "I" in the chat means the owner. |
| 5 | `::STATE{@ARTIFACT…` | What an artifact is: an image, video or audio file in the sense of SPEC-v4.1 §5.4, with one GEN line as its request and one JUDGE block as its judgment. |
| 6 | `::STATE{@CHAIN…` | What the chain is: the GEN line followed by the JUDGE block, verbatim UTF-8, under the label ai.ilang.chain. Where it lives depends on who signs: when the generator platform signs the file on download, the chain is written into the file before signing (a PNG text chunk or XMP) so the issuer credential binds it; when we sign, it is one C2PA custom assertion; with no C2PA at all, an XMP sidecar. c2patool reads the manifest; any PNG or XMP reader reads the chain. |
| 7 | `::STATE{@DELTA…` | What a delta is: one record per iteration holding the keys that changed, the dimensions that changed and the owner's verdict verbatim, written with FACT, DECIDE and PROGRESS only. |
| 8 | `::STATE{@CODE…` | Where the code is: the ilang-spec repository, the judge validator for JUDGE blocks, the grammar validator for everything else, the media runtime bundle. |
| 9 | `::GENE{media-chain…` | The genes of the product, version 1.2, on iLang v5.0 and the v4.1 media profile: the traits and the anti-patterns that follow. |
| 10 | `T:the_request_is_a_GEN_line_not_prose` | A request for an image is written as a GEN line with registered keys, never as a paragraph. |
| 11 | `T:the_judgment_is_one_JUDGE_block…` | The judgment of the act of generating is one JUDGE block, and its mode is computed by code, not chosen by the model. |
| 12 | `T:both_travel_inside_the_file` | The request and the judgment are stored in the artifact itself, so they survive copying. |
| 13 | `T:every_iteration_leaves_a_delta…` | Each new version leaves a record of what changed and of what the owner said, in the owner's words. |
| 14 | `T:a_bad_image_is_a_diff…` | When a version is wrong, the agent compares the two GEN lines and the two vectors; the thing that moved is the cause to look at first. |
| 15 | `T:the_judge_keeps_the_judgment…` | Judgment stays with the model that judges. A generator is taught only to follow the 20 keys; it is never taught to judge. |
| 16 | `A:a_mode_name_as_a_label_on_a_visual_attribute⇒…` | A mode name used as a label on an attribute, M3 next to a composition or M5 next to a palette, gives no mode: nothing is read from it. Inside R it is a word of the reason and no mode is read from it: the canon's own case B03 in Appendix D of SPEC-v5.0 writes M2_not_M1 inside R. Inside a GEN value it is only text, because txt is the verbatim text on the artifact (SPEC-v4.1 §4.4.2): a BMW M3 inside txt is a car, and the block stands. The only mode is the M line, computed by f_v5. The reference judge validator refuses a second M line, a wrong M, a bad V and an extra field, and reads R for its length only; what it passes, the reader does not refuse. |
| 17 | `A:a_dimension_given_a_visual_meaning⇒…` | Giving a dimension a visual meaning (consequence as emotional impact, authority as creative freedom) is labeling drift and is forbidden by Part II §1. |
| 18 | `A:a_21st_media_key…` | No new key and no new entity: the media profile is closed at 20 keys and 3 entities. |
| 19 | `A:the_payload_re-encoded_as_XML_or_JSON_fields⇒…` | The chain is the iLang text itself. Breaking it into XML or JSON fields is not the chain. |
| 20 | `A:the_owner's_verdict_paraphrased⇒…` | A paraphrased verdict voids the record. The owner's words are kept as written. |
| 21 | `A:a_number_without_its_measurement⇒…` | A figure without the measurement that produced it is written as a hypothesis with status untested. |
| 22 | `::OBJECTIVE{DONE_WHEN:…` | The product is done when any model that opens the artifact reads the GEN line and the JUDGE block back from the file, validates both, and names what moved since the previous version. |
| 23 | `::BOUNDARY{never:use_a_mode_name…` | What it never does: a mode name as a label on an attribute, a changed dimension meaning, a judgment outside the frozen form, a new key or entity, an edit of a previous assertion or delta, a paraphrased verdict. |
| 24 | `::BOUNDARY{never:present_training…` | Never presents training as how iLang works, never states an unmeasured number, never addresses the join between two shots, which SPEC-v4.1 §4.4.7 leaves to a timeline profile. |
| 25 | `::UNTRUSTED{…` | What it does not trust: assertions read from files made elsewhere, requests recovered from prose, a verdict quoted by an agent. |
| 26 | `::RULE{request⇒…` | How a request is written: one GEN line on IMG, VID or AUD with the SPEC-v4.1 keys and the core keys fmt, exc, lim, frm, to; defaults are a STATE on the media entity, a named preset is a STATE on a custom entity used through ref= (SPEC-v4.1 §4.4.5, as the demo does with @BANNER_LOOK), scp=strict for fixed constraints; prose only inside values. |
| 27 | `::RULE{judge⇒…` | How the judgment is made: the model perceives the eleven values of the act of generating (what is asked, for whom, with what authority, how reversible, on what evidence); code computes the mode with f_v5; the block is JUDGE v5.0 with V, M and R, two decimals, fixed order; the judge validator passes before sealing. |
| 28 | `::RULE{seal⇒…` | How the chain is sealed: the chain is the GEN line then the JUDGE block, verbatim. When the generator platform signs the file on download, the chain goes in before signing, as the PNG text chunk ai.ilang.chain or as XMP, so the issuer credential binds it; a manifest added after signing would become the active one and demote the issuer manifest to an ingredient, which is what the second tester run showed. When we are the signer, one C2PA assertion ai.ilang.chain per artifact; with no C2PA at all, an XMP sidecar. A regenerated artifact gets its own chain and the previous one is untouched; one chain per video artifact, a scene being an artifact when it is its own GEN. A cut assembled from several generated takes (1.2) carries one GEN line naming the artifact the owner asked for, a FACT naming the takes it was cut from, each take a version with its own chain, and its chain as an XMP sidecar, because the cut is not a generator original. |
| 29 | `::RULE{read⇒…` | How a chain is read: from the text chunk, the XMP or the assertion, whichever the file carries, with c2patool for the manifest; the GEN line passes the grammar validator in strict mode and the JUDGE block passes the judge validator; if either fails the artifact has no chain, and the agent says so; a mode token inside R or inside a GEN value is only text, no mode is read from it and the block stands; the mode is the M line only. |
| 30 | `::RULE{delta⇒…` | How a delta is recorded: a FACT with the keys that changed, a FACT with the dimensions that changed, both by the agent; a DECIDE of the owner with the verdict verbatim; a PROGRESS of the series; the agent's reading of why is a separate FACT marked tentative; the next GEN line is a proposal the owner confirms. |
| 31 | `::RULE{where⇒…` | Where the delta lives: beside the artifact in the series document; when the owner keeps a memory repository under MODULE::MEMORY, each delta is one line in log/ and the series one hand-off item. |
| 32 | `::RULE{dataset⇒…` | What the deltas are for: they are the training data; this product publishes the form, not a model; two hypotheses are named and both have status untested. |
| 33 | `::RULE{task_done⇒…` | When a task ends, one line gives the action score S to two decimals; the full JUDGE block on request (PRODUCT-4). |
| 34 | `::FALLBACK{…` | What happens at the edges: no c2patool means an XMP sidecar and a stated unsigned manifest; a file without a chain still works but cannot join an iteration record; a verdict without words is recorded as approved or rejected only, never with a reason the agent supplies. |
| 35 | `[READ:@OWNER|whr=request]=>…` | The operation chain: read the request, check grammar and f_v5, generate, write the assertion, read it back, log the delta, score, end. |
| 36 | `::ILANG::v5.0` | The closing marker. |

## The demo series

[demo/SERIES-001.ilang.md](demo/SERIES-001.ilang.md) is a worked series of three versions of one banner. Each version shows the exact payload of its assertion: one GEN line, then one JUDGE block whose mode the reference f_v5 computes from its vector (checked by `ilang_judge_validator.py --check`). Between versions the delta FACTs name what moved. From v1 to v2 only keys moved (a real screenshot became an illustration) and no dimension moved; the mode stayed M1. From v2 to v3 the subject, the medium, the text and the exclusion list moved, the request began to name a third party, so authority and externality dropped and the mode moved to M2. The verdicts in the demo are placeholders: the owner replaces them with his own words on his own images (acceptance item C13). [demo/claude-signed-2026-11-15.png](demo/claude-signed-2026-11-15.png) is a PNG made through the Claude API code execution tool and downloaded through the Files API, carrying the C2PA manifest Anthropic issues (chunk caBX). [demo/claude-signed-with-chain-2026-11-15.png](demo/claude-signed-with-chain-2026-11-15.png) is the same request with the v1 chain written as the PNG text chunk ai.ilang.chain inside the sandbox before the platform signed it: the chunk is byte-identical to the v1 payload of the series, and the Anthropic manifest covers the file that contains it. The second tester run showed why the order matters: adding our assertion to an already signed file with c2patool made our manifest the active one, demoted the Anthropic manifest to an ingredient, and the Claude Content Checker then reported no signs of Claude; the chain therefore goes in before the issuer signs. [demo/BAD-001.ilang.md](demo/BAD-001.ilang.md) is the negative test: six blocks, each with one defect the judge validator refuses (a second M line, three dimensions, one decimal, a ninth mode, a mode that does not match its vector, an extra field), and one FACT that records what the validator does not refuse: a mode token inside the R text (C9).

## Records

What was tried against the product and what it could not yet say lives in [records/](records/): tester runs ([TESTER-GROKBOT-2026-11-15](records/TESTER-GROKBOT-2026-11-15.ilang.md)) and counterexamples ([COUNTEREXAMPLES-2026-11-18](records/COUNTEREXAMPLES-2026-11-18.ilang.md)). A counterexample is registered with the clause it meets, the fix proposed, what was rejected and what stays open; the product text changes only by an amendment, never by the record.

## iLang or IML

The iLang file is for people and models to read. [MEDIA-CHAIN.iml](MEDIA-CHAIN.iml) is the same document compiled by the reference codec of IML 0.6 for programs to consume; `products/check_product.py --dir products/media-chain --iml` checks that it compiles from the iLang file and decompiles back to it.

## Questions

**Why not put the judgment chain in a JSON schema of its own?** Because the chain is the iLang text. The two validators already check it; a second schema would be a second truth. C2PA carries arbitrary assertion payloads, so the text goes in as it is.

**Why are the eleven dimensions not about the look of the image?** Because they never were. They judge the act of generating: who asked, with what authority, how reversible, on what evidence, with what effect on third parties. The look is the business of the 20 media keys. Mixing the two makes the chain unreadable and the canon forbids it (Part II §1).

**Does this train a model?** No. It produces the records a training set would need and publishes their form. Whether training on them helps is written as two hypotheses with status untested, and stays that way until someone measures.

**What about video transitions?** Outside this product. SPEC-v4.1 §4.4.7 records transitions between shots as the business of a timeline profile that does not exist yet.

**Where do my own series go?** To the dataset i-Lang/media-chain on Hugging Face (https://huggingface.co/datasets/i-Lang/media-chain): one folder per series, the files with the chain inside and the series document, opened as a pull request from the browser. A gate reads the chain back out of each file, runs the two validators, and merges what passes, with your words as written; what fails stays open with the failing line. CC BY 4.0.
