# Products

The products that iLang itself publishes live here, in the canon repository, under the rule the canon sets for them: `::MODULE::PRODUCT` in [SPEC-v5.0.md](../SPEC-v5.0.md), Part I. In short:

- **PRODUCT-1** A product is written in iLang. Natural language stands in values only.
- **PRODUCT-2** A product ships with its IML form: the same document compiled with the reference codec of [iml-protocol](https://github.com/ilang-ai/iml-protocol), at the current stable version of IML (0.5). The iLang file is for people and models; the IML file is for programs.
- **PRODUCT-3** Its acceptance items are `::RUBRIC` declarations with a check that [goal-check](https://github.com/ilang-ai/ilang-conformance/tree/main/goal) can run; an item code cannot decide is `check:human` and waits for a person. The one who did the work does not confirm its own items.
- **PRODUCT-4** When a product has finished a task it ends with one line giving the action score S, to two decimals; the full `::JUDGE{v5.0}` block is written when the user asks.

Nothing in this directory is normative. The canon is the five `SPEC*.md` files at the root; a product reads the canon and does not change it. The runtime bundles do not include products.

## Why here

Decision of the owner, 2026-10-29: products, templates and engineering books published by iLang go into this directory, not into new repositories. The repository's release carries them: a product is archived and cited through the version of ilang-spec that first ships it, and through the versions that change it. Concept DOI of the repository: [10.5281/zenodo.21821452](https://doi.org/10.5281/zenodo.21821452).

## Index

| Product | Version | iLang | IML | Acceptance | First shipped in |
|---|---|---|---|---|---|
| SOUL: a judgment layer for an AI's default persona | 2.0 (2026-10-29) | [soul/SOUL.ilang.md](soul/SOUL.ilang.md) | [soul/SOUL.iml](soul/SOUL.iml) | [soul/ACCEPTANCE.ilang.md](soul/ACCEPTANCE.ilang.md) | 5.0.2 |

## Layout of a product directory

```
products/<name>/
  <NAME>.ilang.md        the product, an iLang document; its own version and date are in its header line
  <NAME>.iml             the same document compiled by the reference codec of IML
  ACCEPTANCE.ilang.md    the acceptance items (::RUBRIC), and the ::EVIDENCE lines a person adds for the human items
  check_*.py             the executable checks the items name; standard library only
```

## Checks

The CI of this repository lints every `*.ilang.md` under `products/` in strict mode and runs each product's IML round trip. The acceptance file is read by goal-check from the repository root:

```
python ../ilang-conformance/goal/goal_check.py products/soul/ACCEPTANCE.ilang.md --allow-cmd
```

Exit code 0 means every item passed; 2 means the human items are still waiting for a person; 1 means an item failed.
