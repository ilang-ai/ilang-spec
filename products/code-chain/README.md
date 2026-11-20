# Code Chain 1.1

Code Chain is the provenance layer of iLang for a change to a repository: the same chain Media Chain puts inside an image or a video, put inside a git commit. The commit message ends with one blank line, the label `ai.ilang.chain` on its own line, then five lines: one `::FACT{key:request|...}` line carrying the owner's words verbatim and the change in one clause, and one JUDGE block of SPEC-v5.0 Part II §4 (`::JUDGE{v5.0}`, `V:`, `M:`, `R:`). The commit hash covers the chain; a signed commit binds it to a key. Nothing is encoded, nothing is paraphrased, and the mode is the `M:` line only.

It adds nothing to the canon. The request is a FACT line; the judgment is the frozen JUDGE block; the two validators of ilang-spec check both. What it names is where the chain stands and how a gate reads it back from `git log`.

Status: 1.1, dated 2026-11-19, by the owner's word of the same day ("改 发5.0.18"): the anti-pattern line of the GENE on a chain in a file beside the code now gives the reason, the file travels with every later commit and any of them can edit it while the message belongs to this commit alone, in place of "the hash does not cover it", a clause that was inaccurate since a file in the tree is under the commit hash too. 1.0, the same day, by his word "做 先在DSH自己的commit上跑"; first run on github.com/adsorgcn/DeepSeekHarness, whose `tools/code_chain.py` is the first gate.

## Where it goes

| Where | How |
|---|---|
| An agent that commits code for an owner | Before `git commit`, it writes the request line from the owner's words and judges the act of changing the repository; code computes the mode; it appends the six lines to the message. |
| A repository that adopts it | Runs the gate in CI. The gate fails on an invalid chain from the first run, and on a missing chain only from the commit the repository names as its first required one; until then it prints counts. |
| A reader with git and the two validators | `git log -1 --format=%B REV`, find the label, validate the five lines, and read who asked, in his own words, and in what mode it was done. |

## The chain of a commit

```
ai.ilang.chain
::FACT{key:request|by:@SUN|words:"做 先在DSH自己的commit上跑"|change:code-chain 1.0 enters products and the first gate runs on this repository|conf:confirmed}
::JUDGE{v5.0}
V:[int=0.90,cap=0.85,csq=0.80,rel=0.90,cer=0.85,aut=0.90,rev=0.90,evd=0.85,sov=0.95,ine=0.70,ext=0.85]
M:M1|conf:0.85
R:the_owner_ordered_it_in_his_words_a_spec_and_a_gate_reversible_by_revert
```

`words` is absent when the author acted without an order. `change` is one clause. A rebase or a squash makes new commits, each with its own chain; the old one is history and is never edited.

## Files

| File | What |
|---|---|
| [CODE-CHAIN.ilang.md](CODE-CHAIN.ilang.md) | The product, iLang, written for people and models. |
| [CODE-CHAIN.iml](CODE-CHAIN.iml) | The same document compiled for programs with the IML 0.6 reference codec. |
| [ACCEPTANCE.ilang.md](ACCEPTANCE.ilang.md) | The acceptance items, run by goal-check. |

Sibling: [../media-chain/](../media-chain/), the same chain for a generated media file. License MIT.
