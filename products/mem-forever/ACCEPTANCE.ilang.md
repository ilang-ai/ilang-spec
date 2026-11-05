::ILANG::v5.0
[TYPE:acceptance][ID:ILANG-MEM-FOREVER-ACCEPTANCE][VERSION:2.1][DATE:2026-11-05][LANG:en]
[FROM:@SUN][TO:@AGENT][STATUS:active]

::OBJECTIVE{id:mem_forever_v21|owner:@SUN|trust:trusted|version:1|status:active}
  target: the Mem-Forever 2.1 product in this directory is the one an agent loads to keep its owner's memory: it lints clean against the canon, carries its IML form, fits one instruction field, is served by the site byte for byte, and its template repository passes its own acceptance checks
  ACCEPT: every ::RUBRIC item below passes; the human items pass only on an ::EVIDENCE line signed by a person who did not do the work

::FACT{key:module|value:SPEC-v5.0.md Part I MODULE::PRODUCT, items PRODUCT-1 to PRODUCT-4; the protocol it implements is MODULE::MEMORY of the same Part|conf:confirmed}
::FACT{key:template|value:github.com/ilang-ai/Mem-Forever, concept DOI 10.5281/zenodo.22865160, release 2.1.0; its README is the engineering book and its skills/mem-forever/SKILL.md the normative text for agents that have the repository open|conf:confirmed}
::FACT{key:checker|value:goal-check, ilang-conformance 2.2.0, run from the repository root with --allow-cmd|conf:confirmed}

::RUBRIC{C1: MEM-FOREVER.ilang.md passes the canon grammar validator in strict mode|check:cmd|run:"python ilang_grammar_validator.py --lint products/mem-forever/MEM-FOREVER.ilang.md --strict"|expect:0}
::RUBRIC{C2: MEM-FOREVER.iml is what the reference codec of IML 0.5 compiles from MEM-FOREVER.ilang.md and it decompiles back to it|check:cmd|run:"python products/check_product.py --dir products/mem-forever --iml"|expect:0}
::RUBRIC{C3: the iLang file is the released one|check:file|path:products/mem-forever/MEM-FOREVER.ilang.md|sha256:50ae0ebb239bd0b873f25a0f243a68cb46a590e38794af5c5efb3f1d205bcd86}
::RUBRIC{C4: the IML file is the released one|check:file|path:products/mem-forever/MEM-FOREVER.iml|sha256:d8fc74f0f88747a13466f731d06af8424066efdd3825c3c3127c38c7822c3cb4}
::RUBRIC{C5: the document fits one instruction field, at most 6000 characters|check:cmd|run:"python products/check_product.py --dir products/mem-forever --length 6000"|expect:0}
::RUBRIC{C6: the file the site serves is byte-identical to MEM-FOREVER.ilang.md|check:cmd|run:"python products/check_product.py --dir products/mem-forever --site https://ilang.ai/memory/MEM-FOREVER.ilang.md"|expect:0}
::RUBRIC{C7: the template repository at release 2.1.0 passes its own acceptance checks: brain.py check 0 errors, every Markdown file with blocks validator-clean in strict mode, the five instruction files byte-identical to the body of the skill|check:human}
::RUBRIC{C8: a chat AI with no tools reads the pasted card and hand-off, restates the items verbatim, and its write-back passes handoff review before it is accepted, as the owner's web-endpoint run showed|check:human}

::EVIDENCE{id:e7|deliverable:C7|kind:manual_check|ref:github.com/ilang-ai/Mem-Forever README section 5 Measured, release 2.1.0, 2026-11-05|verified_by:@SUN|result:pass|date:2026-11-05}
::EVIDENCE{id:e8|deliverable:C8|kind:manual_check|ref:github.com/ilang-ai/Mem-Forever README section 5, one web endpoint, ChatGPT free tier signed out, 2026-11-05|verified_by:@SUN|result:pass|date:2026-11-05}

::FALLBACK{C6_before_the_site_publishes_the_file⇒unknown_not_fail|codec_clone_blocked⇒run_C2_with_--codec_pointing_at_a_local_checkout_of_iml-protocol_at_the_pinned_commit}

[READ:@SRC|path=products/mem-forever/ACCEPTANCE.ilang.md]=>[CHEK|whr=each_item]=>[LOG]=>[Ω]
::ILANG::v5.0
