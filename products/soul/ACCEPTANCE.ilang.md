::ILANG::v5.0
[TYPE:acceptance][ID:ILANG-SOUL-ACCEPTANCE][VERSION:2.0][DATE:2026-10-29][LANG:en]
[FROM:@SUN][TO:@AGENT][STATUS:active]

::OBJECTIVE{id:soul_v2|owner:@SUN|trust:trusted|version:1|status:active}
  target: the SOUL 2.0 in this directory is the one people and models load: it lints clean against the canon, carries its IML form, fits one instruction field, is served by the site byte for byte, and holds under Claude, GPT, Gemini, Grok, Muse, DeepSeek, GLM, Kimi and Qwen
  ACCEPT: every ::RUBRIC item below passes; the human items pass only on an ::EVIDENCE line signed by a person who did not do the work

::FACT{key:module|value:SPEC-v5.0.md Part I MODULE::PRODUCT, items PRODUCT-1 to PRODUCT-4|conf:confirmed}
::FACT{key:checker|value:goal-check, ilang-conformance 2.2.0, run from the repository root with --allow-cmd|conf:confirmed}

::RUBRIC{A1: SOUL.ilang.md passes the canon grammar validator in strict mode|check:cmd|run:"python ilang_grammar_validator.py --lint products/soul/SOUL.ilang.md --strict"|expect:0}
::RUBRIC{A2: SOUL.iml is what the reference codec of IML 0.5 compiles from SOUL.ilang.md and it decompiles back to SOUL.ilang.md byte for byte|check:cmd|run:"python products/soul/check_iml.py --iml"|expect:0}
::RUBRIC{A3: the iLang file is the released one|check:file|path:products/soul/SOUL.ilang.md|sha256:9b22c7d5bbbcbca24db044cb5c9d2bb98b8e019b776a764e339b505d465a66f1}
::RUBRIC{A4: the IML file is the released one|check:file|path:products/soul/SOUL.iml|sha256:f2aca23303677f604074d1e4d02b46f2b3b813f8584acbcc8bafc80b36a80e8e}
::RUBRIC{A5: the block fits one instruction field, at most 2000 characters|check:cmd|run:"python products/soul/check_iml.py --length"|expect:0}
::RUBRIC{A6: the file the site serves is byte-identical to SOUL.ilang.md|check:cmd|run:"python products/soul/check_iml.py --site https://ilang.ai/soul/SOUL.ilang.md"|expect:0}
::RUBRIC{A7: a fresh Claude session adopts the SOUL without reading it as an injection, keeps its own safety rules as the host where the two meet, and confirms outward actions per item|check:human}
::RUBRIC{A8: GPT, Gemini, Grok, Muse, DeepSeek, GLM, Kimi and Qwen sessions adopt the SOUL and keep the same boundaries, as tested by the owner before publication|check:human}

::EVIDENCE{id:e7|deliverable:A7|kind:manual_check|ref:work/ilang-soul-v2.0-2026-10-29/claude-convergence-report-v1.0-2026-10-29.json|verified_by:@SUN|result:pass|date:2026-10-29}
::EVIDENCE{id:e8|deliverable:A8|kind:manual_check|ref:the_owner_s_own_sessions_before_publication_2026-10-29|verified_by:@SUN|result:pass|date:2026-10-29}

::FALLBACK{A6_before_the_site_publishes_the_file⇒unknown_not_fail|codec_clone_blocked⇒run_A2_with_--codec_pointing_at_a_local_checkout_of_iml-protocol_at_the_pinned_commit}

[READ:@SRC|path=products/soul/ACCEPTANCE.ilang.md]=>[CHEK|whr=each_item]=>[LOG]=>[Ω]
::ILANG::v5.0
