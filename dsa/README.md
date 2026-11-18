# Big-Tech DSA Interview Prep (Google L3 base + L4/senior deltas)

Topic-first prep for big-company coding loops (Google, Meta, Amazon, Microsoft, Apple, Uber-style). The **base track is Google L3**: 4–5 rounds, one medium problem each, 35–45 minutes. Harder loops (L4/SDE-2+, Meta's two-per-round pace, hard-round companies) layer on via the deltas and the `💤 T3` material. Dense notes, curated must-solve lists, no 500-problem grind.

> **At L3, do not drill segment trees / Fenwick trees** — prefix sum, sorting + binary search, or a heap solve the L3 versions. They are covered in [Range Queries](03-algorithms/15-range-queries.md) as `💤 T3` for L4+ and hard rounds. Details: [What to skip at L3](00-start-here/02-round-cheatsheet.md#4-what-to-skip-at-l3)

---

## What this repo covers

Folders are numbered in study order — work top to bottom.

| Step | Folder | What's inside |
|---|---|---|
| 0 | [`00-start-here/`](00-start-here/01-roadmap.md) | 4-week roadmap, round cheatsheet (45-min clock, edge cases, revision schedules), L4 and senior deltas |
| 1 | [`01-foundations/`](01-foundations/01-how-to-think.md) | How to think (derive any pattern), complexity budget + Python toolkit |
| 2 | [`02-data-structures/`](02-data-structures/README.md) | array, hashing, string, matrix/grid, stack, queue/deque, linked list, tree/BST, trie, heap, graphs (incl. graph algorithms) |
| 3 | [`03-algorithms/`](03-algorithms/README.md) | sorting, two pointers, sliding window, binary search, recursion, backtracking, recursion → DP, DP, greedy/intervals, union-find, string matching, bits, math, range queries |
| 4 | [`04-practice/`](04-practice/README.md) | 200 indexed walkthrough problems, tier-tagged, one file per topic + design-a-data-structure |
| 5 | [`05-review/`](05-review/README.md) | pattern sheet, graded ladders, interview judgment + mocks |
| 6 | [`06-behavioral/`](06-behavioral/README.md) | Googliness attributes, STAR story bank |

**Not in scope:** system design, LLD, concurrency, SQL. **Covered but `💤 T3` at L3** (promote for L4+ / hard rounds): segment trees / Fenwick trees, advanced graphs (Floyd-Warshall, Tarjan/SCC), bitmask/digit/game DP — see [What to Skip at L3](00-start-here/02-round-cheatsheet.md) and the [L4 delta](00-start-here/03-l4-sde2-delta.md).

**Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](00-start-here/01-roadmap.md#tier-legend)). L4/senior bars layer on top via the [L4 delta](00-start-here/03-l4-sde2-delta.md) and [senior delta](00-start-here/04-senior-delta.md).

---

## How loops differ by company

The DSA core is the same everywhere; the format changes what to drill. Verify current format with your recruiter — loops change.

| Company | Coding format (typical) | Adjust your prep |
|---|---|---|
| **Google** | 1 medium(-hard) per 45 min, follow-ups escalate; Google Doc / no autocomplete; hiring committee reads notes | Narrate complexity and trade-offs; expect "now make it streaming / scale it" follow-ups ([senior chains](05-review/03-interview-judgment.md#part-e--senior-follow-up-chains)) |
| **Meta** | **2 problems in ~40 min**, mostly LeetCode-medium staples; speed and bug-free code matter most | Drill T1 to < 15 min each; less exploration, more pattern recall; run timed doubles in [mocks](05-review/03-interview-judgment.md#part-d--mock-rounds) |
| **Amazon** | 1–2 problems per round, each round also probes **Leadership Principles** | Prepare LP stories alongside code ([behavioral](06-behavioral/README.md)); design-a-data-structure is common ([design practice](04-practice/data-structures/12-design.md)) |
| **Microsoft / Apple** | Team-dependent; mediums, often linked lists, trees, strings, design-a-class | T1/T2 breadth; clean OOP for design problems |
| **Uber / Stripe / fintech** | Longer practical problems (parsing, simulation, rate limiters, iterators) | [Design practice](04-practice/data-structures/12-design.md), heap/interval simulation, clean code over tricks |
| **Hard-round companies** (some L4+ Google/Meta, HFT, competitive-leaning) | Hards: range queries, bitmask/digit DP, game DP | Promote `💤 T3` in [Range Queries](03-algorithms/15-range-queries.md), [DP](04-practice/algorithms/08-dynamic-programming.md), [Graph algorithms](04-practice/algorithms/11-graph-algorithms.md) |

---

## How every lecture is laid out

1. **What this covers**: scope, what you'll be able to do, prereqs, paired practice file, time budget, section links.
2. **First-Principles Map / Breakdown**: why the structure or technique exists, its invariant, where it breaks.
3. **Theory → techniques → templates**: the mental model, then code templates with complexity.
4. **Interview questions, logic & traps**, then **Quick Revision Triggers** and flashcards.

Each concept file (`01-`, `02-`) links to its practice file in `04-practice/` and the practice file links back.

---

## Start here: study path

| Step | Do | Link |
|---|---|---|
| 1 | Read the plan and the round clock | [Roadmap](00-start-here/01-roadmap.md) · [Round cheatsheet](00-start-here/02-round-cheatsheet.md) |
| 2 | Learn how to derive patterns; set your complexity budget | [How to think](01-foundations/01-how-to-think.md) · [Complexity & Python](01-foundations/02-complexity-and-python.md) |
| 3 | Per topic: lecture, then its practice file, T1 first | [DS index](02-data-structures/README.md) · [Algo index](03-algorithms/README.md) |
| 4 | Pressure-test with ladders and mocks | [Ladders](05-review/02-ladders.md) · [Mocks](05-review/03-interview-judgment.md#part-d--mock-rounds) |
| 5 | Behavioral stories | [Behavioral + Googliness](06-behavioral/BEHAVIORAL_GOOGLINESS.md) |
| 6 | Final week | [Revision schedules](00-start-here/02-round-cheatsheet.md#revision-schedules) · [Pattern sheet](05-review/01-pattern-sheet.md) |

L4 / senior: [L4 delta](00-start-here/03-l4-sde2-delta.md) · [Senior delta](00-start-here/04-senior-delta.md) · [Senior follow-up chains](05-review/03-interview-judgment.md#part-e--senior-follow-up-chains).

---

### Flashcards (189 cards, spaced repetition)

Every lecture ends with a `## Flashcards` section. A card is a bold question line tagged `#flashcard`, followed by the answer up to the next blank line:

```
**What does `lps[i]` mean in KMP?** #flashcard
Longest proper prefix of pattern[:i+1] that is also a suffix…
```

- **Anki:** export every card to a tab-separated file, then *File → Import* into a Basic note type with "Allow HTML" on. Multi-line answers are joined with `<br>`.
  ```sh
  grep -rl --include='*.md' '#flashcard$' . | xargs awk '/#flashcard$/{if(q)print q"\t"a; q=$0; sub(/ *#flashcard$/,"",q); a=""; next} q&&/^(---)?$/{if(a!=""){print q"\t"a; q=""}; next} q{a=(a==""?$0:a"<br>"$0)} END{if(q)print q"\t"a}' > flashcards.tsv
  ```
- **Obsidian:** filter with tag search `tag:#flashcard` to review in-vault. The Spaced Repetition plugin expects `?` / `::` separators, so the Anki export is the supported route for scheduled review.

---

## 4-week overview

| Week | Focus |
|------|-------|
| **1** | Arrays, hashing, graphs (BFS/DFS), two pointers, sliding window |
| **2** | Heaps, tries, queues, binary search (incl. search on answer) |
| **3** | Trees, stacks, linked lists, union-find, greedy |
| **4** | Core DP, backtracking, recursion + **4–6 timed mocks** + behavioral |

Full daily plan: [Roadmap](00-start-here/01-roadmap.md)
