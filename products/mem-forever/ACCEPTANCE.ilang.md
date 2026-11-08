::ILANG::v5.0
[TYPE:acceptance][ID:ILANG-MEM-FOREVER-ACCEPTANCE][VERSION:3.0][DATE:2026-11-08][LANG:en]
[FROM:@SUN][TO:@AGENT][STATUS:active]

::OBJECTIVE{id:mem_forever_v30|owner:@SUN|trust:trusted|version:1|status:active}
  target: the Mem-Forever 3.0 product in this directory is the one an agent loads to keep its owner's memory as a derivation from the keys: it lints clean against the canon, carries its IML form, fits one instruction field, is served by the site byte for byte, and its template repository passes its own acceptance checks and behavior tests
  ACCEPT: every ::RUBRIC item below passes; the human items pass only on an ::EVIDENCE line that names a record made by someone or something other than the author of the change, a person's check or a CI run

::FACT{key:module|value:SPEC-v5.0.md Part I MODULE::PRODUCT, items PRODUCT-1 to PRODUCT-4; the protocol it implements is MODULE::MEMORY of the same Part, whose WHERE and SECRETS lines name the ledger since 5.0.9 (AMENDMENT-MODULE-MEMORY-SECRETS v1.0, accepted by the owner 2026-11-08)|conf:confirmed}
::FACT{key:template|value:github.com/ilang-ai/Mem-Forever, concept DOI 10.5281/zenodo.22865160, release 3.0.0 (version DOI 10.5281/zenodo.24048280, tag v3.0.0, main b80fcc5); its README is the engineering book and its skills/mem-forever/SKILL.md the normative text for agents that have the repository open; the design record is MEM-FOREVER-3-ILANG-CRYPTO-DESIGN v1.1 (2026-11-08), kept by the owner|conf:confirmed}
::FACT{key:checker|value:goal-check, ilang-conformance 2.2.0, run from the repository root with --allow-cmd|conf:confirmed}

::RUBRIC{C1: MEM-FOREVER.ilang.md passes the canon grammar validator in strict mode|check:cmd|run:"python ilang_grammar_validator.py --lint products/mem-forever/MEM-FOREVER.ilang.md --strict"|expect:0}
::RUBRIC{C2: MEM-FOREVER.iml is what the reference codec of IML 0.5 compiles from MEM-FOREVER.ilang.md and it decompiles back to it|check:cmd|run:"python products/check_product.py --dir products/mem-forever --iml"|expect:0}
::RUBRIC{C3: the iLang file is the released one|check:file|path:products/mem-forever/MEM-FOREVER.ilang.md|sha256:ec08d9ded4c5b0b40f9a5e6abe921a07b844d9050340cf9f80bd12f0217db5c3}
::RUBRIC{C4: the IML file is the released one|check:file|path:products/mem-forever/MEM-FOREVER.iml|sha256:fa537313b4d79fe163d0a373999c40d09a9b6f92f7048eeb2000a971123d10d9}
::RUBRIC{C5: the document fits one instruction field, at most 6000 characters|check:cmd|run:"python products/check_product.py --dir products/mem-forever --length 6000"|expect:0}
::RUBRIC{C6: the file the site serves is byte-identical to MEM-FOREVER.ilang.md|check:cmd|run:"python products/check_product.py --dir products/mem-forever --site https://ilang.ai/memory/MEM-FOREVER.ilang.md"|expect:0}
::RUBRIC{C7: the template repository at release 3.0.0 passes its own acceptance checks: brain.py check 0 errors, every Markdown file with blocks validator-clean in strict mode, the five instruction files byte-identical to the body of the skill, the hook scripts parse, and tools/test_brain.py passes its 26 scenarios|check:human}
::RUBRIC{C8: a chat AI with no tools reads the pasted card and hand-off, restates the items verbatim, and its write-back passes handoff review before it is accepted|check:human}
::RUBRIC{C9: the recognition and unlock rules behave as the design says on the template's test vectors: an agent-written boundary is rewritten as advice, an unsupported owner_verbatim claim is downgraded, a top door refuses the record and opens once by code, a key is refused until a next item names its door, the owner's turn is recognized and a stranger's is not|check:human}

::EVIDENCE{id:e7|deliverable:C7|kind:ci_run|ref:github.com/ilang-ai/Mem-Forever actions, workflow tests on main b80fcc5, 2026-11-08, conclusion success (check, instructions check, test_brain.py, sh -n on both hooks)|verified_by:@CI|result:pass|date:2026-11-08}
::EVIDENCE{id:e8|deliverable:C8|kind:manual_check|ref:github.com/ilang-ai/Mem-Forever README section 5, one web endpoint, ChatGPT free tier signed out, 2026-11-05, on the 2.1 message; the 3.0 message adds the ledger rows without values after the hand-off and has not yet been run through a web endpoint|verified_by:@SUN|result:pass_for_2.1_pending_for_3.0|date:2026-11-05}
::EVIDENCE{id:e9|deliverable:C9|kind:ci_run|ref:github.com/ilang-ai/Mem-Forever tools/test_brain.py on main b80fcc5, the scenarios named in README section 5 Measured, 2026-11-08|verified_by:@CI|result:pass|date:2026-11-08}

::FALLBACK{C6_before_the_site_publishes_the_file⇒unknown_not_fail|codec_clone_blocked⇒run_C2_with_--codec_pointing_at_a_local_checkout_of_iml-protocol_at_the_pinned_commit|C8_for_3.0⇒the_2.1_run_stands_until_the_owner_runs_the_3.0_message_through_a_web_endpoint}

[READ:@SRC|path=products/mem-forever/ACCEPTANCE.ilang.md]=>[CHEK|whr=each_item]=>[LOG]=>[Ω]
::ILANG::v5.0
