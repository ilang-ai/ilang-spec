::ILANG::v5.0
[TYPE:acceptance][ID:ILANG-CODE-CHAIN-ACCEPTANCE][VERSION:1.0][DATE:2026-11-19][LANG:en]
[FROM:@SUN][TO:@TESTER][STATUS:active]

::OBJECTIVE{id:code_chain_v10|owner:@SUN|trust:trusted|version:1|status:active}
  target: the Code Chain 1.0 product in this directory is the one an agent loads to put the request and the judgment inside a git commit and the one a gate reads back: it lints clean against the canon, carries its IML form, fits one instruction field, and its first repository reads its own chained commits back with 0 invalid
  ACCEPT: every ::RUBRIC item below passes; the human items pass only on an ::EVIDENCE line that names a record made by someone or something other than the author of the product, a tester's run or a CI run; that line is the tester's own text, stored verbatim in records/

::FACT{key:module|value:SPEC-v5.0.md Part I MODULE::PRODUCT, items PRODUCT-1 to PRODUCT-4; the vocabulary it uses is the FACT declaration of §1 and SPEC-v5.0.md Part II §1 §2 §4 (eleven dimensions, f_v5, the frozen JUDGE block); the sibling products/media-chain uses the same chain for a media file|conf:confirmed}
::FACT{key:owner|value:decision of @SUN on 2026-11-19: 做 先在DSH自己的commit上跑; the product lives under products/ of ilang-spec; the first repository is github.com/adsorgcn/DeepSeekHarness and its gate is tools/code_chain.py|conf:confirmed}
::FACT{key:checker|value:goal-check, ilang-conformance goal/goal_check.py, run from this repository's root with --allow-cmd; the validators ilang_grammar_validator.py and ilang_judge_validator.py of ilang-spec sit at the root|conf:confirmed}

::RUBRIC{C1: CODE-CHAIN.ilang.md passes the canon grammar validator in strict mode|check:cmd|run:"python -X utf8 ilang_grammar_validator.py --lint products/code-chain/CODE-CHAIN.ilang.md --strict"|expect:0}
::RUBRIC{C2: CODE-CHAIN.iml is what the reference codec of IML 0.6 compiles from CODE-CHAIN.ilang.md and it decompiles back to it|check:cmd|run:"python -X utf8 products/check_product.py --dir products/code-chain --iml"|expect:0}
::RUBRIC{C3: the iLang file is the released one|check:file|path:products/code-chain/CODE-CHAIN.ilang.md|sha256:b3610620c0334c75b6b545fdeeb17b6c288b3770eb0856c98a99a375c987c5e0}
::RUBRIC{C4: the IML file is the released one|check:file|path:products/code-chain/CODE-CHAIN.iml|sha256:c53bf16bfe548ad402903675fbe47e784d1e9abf9ae79582bee49dd8a384c785}
::RUBRIC{C5: the document fits one instruction field, at most 6000 characters|check:cmd|run:"python -X utf8 products/check_product.py --dir products/code-chain --length 6000"|expect:0}
::RUBRIC{C6: the chain in the README, the request line then the JUDGE block, passes both validators when written to a file under the canon header|check:human}
::RUBRIC{C7: the first repository, DeepSeekHarness, reads its chained commits back with its gate tools/code_chain.py check and reports 0 invalid, in a CI run|check:human}
::RUBRIC{C8: a reader given only git log of one chained commit names who asked, in his own words, and the mode, and the answer matches the chain|check:human}

::FALLBACK{codec_clone_blocked⇒run_C2_with_--codec_pointing_at_a_local_checkout_of_iml-protocol_at_the_pinned_commit|a_commit_without_a_chain_before_the_repository_names_its_first_required_commit⇒counted,not_failed}

[READ:@SRC|path=products/code-chain/ACCEPTANCE.ilang.md]=>[CHEK|whr=each_item]=>[LOG]=>[Ω]
::ILANG::v5.0
