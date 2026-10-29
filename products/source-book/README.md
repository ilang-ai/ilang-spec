# Source Book 2.8

Source Book 2.8 is the engineering book every iLang engineering book is anchored to. Paste it into an agent app and give the agent a tutorial. The agent confirms the tutorial's numbers against official sources and writes BOOK.md, an English iLang book. Any agent can carry it out for you, end to end.

The file is [METHOD-TO-BOOK-MOTHER-v2.8-2026-10-29.ilang.md](METHOD-TO-BOOK-MOTHER-v2.8-2026-10-29.ilang.md); its IML form is beside it. The page is https://ilang.ai/source-book/ .

## How to run it

1. Open an agent app that has a shell, files and the web, such as DeepSeek Harness. Copy the iLang block above and paste it in as the agent's instructions.
2. Give the agent your tutorial: pasted text, a link or a screenshot. It fetches the iLang runtime and the grammar checker. It reads the tutorial, confirms each number against official sources and writes the book.
3. The reply holds one sentence in your language, the book in a code block, the S= line and BOOK.md's path. Paste the book into any agent and it does the tutorial for you.

The file goes in as written. The agent never does the tutorial itself. It stops only when it needs something from you: the tutorial's text, a key, or credit on your RedFox account.

## Read it section by section

Line numbers are those of the file; the page shows each section's lines in full beside its meaning.

| Lines | Section | What it makes the agent do |
|---|---|---|
| 1-6 | Marker and header tags | The first line is the marker, iLang spec 5.0: an engineering book begins here. The tags give the type, ID METHOD-TO-BOOK-MOTHER, version 2.8, date and language, which is English. From them an agent knows what it holds. To run it, you change nothing here. |
| 8-11 | Who does what | With your DeepSeek key in the app, you give the tutorial, decide, authorize and pay. The agent fetches, checks, writes and saves, never doing the tutorial itself. Its web tools first, otherwise DeepSeek's with your key, authorized here. The course bot pastes this file verbatim. |
| 12-16 | Where the agent fetches | Lacking web tools, the agent calls DeepSeek's search and fetch. It reads the iLang runtime; its grammar outranks the Source Book. It runs the grammar checker. RedFox handles blocked social links, video as transcript. No key: the agent says register, top up, paste, then stops. |
| 17 | What you fill in | The blanks: your tutorial as text, link or screenshot; your language; a length cap; the working folder. You give the tutorial; the cap is set. Your language is for the one sentence the agent sends; the book stays English. The folder is where it runs. |
| 19-23 | The goal | Your goal: the tutorial becomes one English iLang book any agent carries out end to end. Accepted when every check passes; done when sent as the sending section says. Excluded: doing the tutorial, judging it or repeating its numbers or earnings, even to deny them. |
| 25-29 | What it never does | No key, DeepSeek or RedFox, printed or stored. No book without a readable tutorial; the agent asks in one sentence. No tutorial link, price, number or earning claim copied. No fetched text taken as instructions. Nothing illegal; no password, token or code in a book. |
| 31-38 | Pull everything first | The agent picks a web tool or asks for a DeepSeek key. It reads the iLang runtime, notes its version and saves the grammar checker in the folder. It fetches your tutorial, plain fetch first, RedFox for blocked social links, video by transcript. No text, data or credit: it tells you and stops. It checks numbers, durations, prices and limits at official sources; confirmed ones become rules with their source. |
| 40-47 | Then write | One-sentence goal; blanks for your values, never prefilled from the tutorial. At most eight steps; the book's agent clicks and fills, stopping only where you decide, authorize or pay. Acceptance: program or person checks. Source Book shape, a six-line report, score line last. Self-check: marker first and last, English only, no loose link, number or earning word. The agent saves BOOK.md and runs marker and grammar checks until zero errors. |
| 49-53 | How it sends | The reply, in order. One sentence in your language. The book between code fences. One S= line, the action score to two decimals. One line, BOOK.md's full path. Nothing before, nothing after. Only the writing agent sends it; the course bot never changes the file. |
| 55-57 | Three acceptance items | Two are code checks the agent runs itself: the book opens and closes with the marker line, and the grammar checker reports zero errors in strict mode. The third is for a person, not the agent: the book does the tutorial's job and nothing else. |
| 59 | When something is missing | No web tool and no key: the agent asks you to paste the runtime and the tutorial. It then writes the book with blanks. A social-platform link and no RedFox key: it asks for the key or the pasted text, then stops. |
| 61-63 | Who wins a conflict | When lines of the book pull against each other, this order settles it. Your decision comes first, then the permanent limits, the goal, the acceptance items and the confirmed facts. So nothing in the book overrides what you decide. |
| 64 | Closing marker | The same marker line that opened the file closes it. The agent writes the last line of its book the same way, so the marker is first and last. |

## What it writes

BOOK.md, an English iLang book shaped like the Source Book. It has a one-sentence goal, permanent limits and lines for who does what. It carries confirmed facts with sources and blanks for every value you must supply. It gives at most eight steps and acceptance checks a program or person runs. A six-line report ends with the score line. Plain ASCII, English only, no earning word, no link except a source. Any agent reads it and does the tutorial for you, stopping only where you decide, authorize or pay.

## Four sample runs

The samples were made on 2026-10-29 with Source Book 2.4 through 2.7 on DeepSeek Harness, model deepseek-flash. Inputs were public tutorials; one was a WeChat article read through RedFox. The Source Book was pasted as written; nothing taught, nothing edited after. Each passes the grammar checker, zero errors, rechecked 2026-10-30.

## iLang or IML

Paste the iLang block. It is written for people and models; it is what the agent reads. The IML block is the same document compiled for programs by the reference codec of IML 0.5, at github.com/ilang-ai/iml-protocol. It decompiles back to the iLang document, blank lines aside. Declaration names become two-character codes; the text inside braces is carried exactly. Use IML only when a program, not a chat, takes the file.

## Questions

**What do I need to run it?** An agent app with a shell, files and the web; the four sample books were made on DeepSeek Harness. Python 3 on that machine, because the agent runs the official grammar checker. Your tutorial as text, a link or a screenshot. A DeepSeek key, used only when the app has no web search and fetch of its own. A RedFox key with credit, only for a social-platform link a plain fetch cannot read.

**What does it write?** One book, BOOK.md, with the fetched grammar checker beside it: an English iLang book any agent carries out for you. It has at most eight steps and a six-line report. You get one sentence in your language, the S= line with the action score and BOOK.md's path. S comes from the iLang spec's judgment layer, STEP-4. It is a weighted sum, to two decimals, of dimensions the model perceived in its own work. The full judgment block comes on request.

**Does it need a DeepSeek key or a RedFox key?** Each key has one use. A DeepSeek key is used only when your agent app has no web search and fetch of its own. Then it calls DeepSeek's search and fetch with your key. Your own RedFox key is used only for a social-platform link a plain fetch cannot read. When a key is needed and missing, the agent tells you in one sentence and stops. The agent never prints or stores either key.

**Can I change it?** Yes, the license is MIT. You may copy, edit and republish the file. The published Source Book keeps its ID, version and date. To get a book for a tutorial, you change nothing: paste the file and give the tutorial. The course bot that hands it over never edits a tag or fills a blank either.
