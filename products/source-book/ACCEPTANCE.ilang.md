::ILANG::v5.0
[TYPE:acceptance][ID:ILANG-SOURCE-BOOK-ACCEPTANCE][VERSION:2.9][DATE:2026-10-30][LANG:en]
[FROM:@SUN][TO:@AGENT][STATUS:active]

::OBJECTIVE{id:source_book_v29|owner:@SUN|trust:trusted|version:1|status:active}
  target: the Source Book 2.9 in this directory is the one every engineering book is anchored to: it lints clean against the canon, carries its IML form, is served by the site byte for byte, and has produced books that pass its own acceptance items
  ACCEPT: every ::RUBRIC item below passes; the human items pass only on an ::EVIDENCE line signed by a person who did not do the work

::FACT{key:module|value:SPEC-v5.0.md Part I MODULE::PRODUCT, items PRODUCT-1 to PRODUCT-4|conf:confirmed}
::FACT{key:file_name|value:METHOD-TO-BOOK-MOTHER is the name the document carries in its own header; the product is published as the Source Book, the engineering book that other engineering books are anchored to|conf:confirmed}
::FACT{key:checker|value:goal-check, ilang-conformance 2.2.0, run from the repository root with --allow-cmd|conf:confirmed}

::RUBRIC{B1: the Source Book passes the canon grammar validator in strict mode|check:cmd|run:"python ilang_grammar_validator.py --lint products/source-book/METHOD-TO-BOOK-MOTHER-v2.9-2026-10-30.ilang.md --strict"|expect:0}
::RUBRIC{B2: the IML file is what the reference codec of IML 0.5 compiles from the Source Book and it decompiles back to it|check:cmd|run:"python products/check_product.py --dir products/source-book --iml"|expect:0}
::RUBRIC{B3: the iLang file is the released one|check:file|path:products/source-book/METHOD-TO-BOOK-MOTHER-v2.9-2026-10-30.ilang.md|sha256:20debddbb0b536eb1335495e3e8a15cf2989f164174f93c96909587efcab5503}
::RUBRIC{B4: the IML file is the released one|check:file|path:products/source-book/METHOD-TO-BOOK-MOTHER-v2.9-2026-10-30.iml|sha256:ea4d4ffc51350978cabc47ea24c1eade7ab78625c0f9f729fa0629e19f535676}
::RUBRIC{B5: the file the site serves is byte-identical to the Source Book|check:cmd|run:"python products/check_product.py --dir products/source-book --site https://ilang.ai/source-book/METHOD-TO-BOOK-MOTHER-v2.9-2026-10-30.ilang.md"|expect:0}
::RUBRIC{B6: given a tutorial, an agent running the Source Book delivers a BOOK.md that passes the book's own items A1 and A2, with the one-line score at the end, as the owner's four sample runs did|check:human}
::RUBRIC{B7: no key, price, link or earning claim of a tutorial reaches a produced book, as the owner's four sample runs showed|check:human}

::FALLBACK{B5_before_the_site_publishes_the_file⇒unknown_not_fail|codec_clone_blocked⇒run_B2_with_--codec_pointing_at_a_local_checkout_of_iml-protocol_at_the_pinned_commit}

[READ:@SRC|path=products/source-book/ACCEPTANCE.ilang.md]=>[CHEK|whr=each_item]=>[LOG]=>[Ω]
::ILANG::v5.0
