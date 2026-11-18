# Big-Tech DSA Interview Prep (Google L3 base + L4/senior deltas)

Topic-first prep for big-company coding loops (Google, Meta, Amazon, Microsoft, Apple, Uber-style). The **base track is Google L3**: 4–5 rounds, one medium problem each, 35–45 minutes. Harder loops (L4/SDE-2+, Meta's two-per-round pace, hard-round companies) layer on via the deltas and the `💤 T3` material. Dense notes, curated must-solve lists, no 500-problem grind.

> **At L3, do not drill segment trees / Fenwick trees** — prefix sum, sorting + binary search, or a heap solve the L3 versions. They are covered in [Range Queries](02-algorithms/19-range-queries.md) as `💤 T3` for L4+ and hard rounds. Details: [What to Skip at L3](00-start-here/L3_CHEATSHEET.md)

---

## What this repo covers

| Area | Topics | Where |
|---|---|---|
| **Data structures** | array, hashing, string, matrix/grid, stack, queue/deque, linked list, tree/BST, trie, heap, graph | [`01-data-structures/`](01-data-structures/README.md) |
| **Algorithms** | sorting, string matching, two pointers, sliding window, recursion, recursion → DP, binary search, backtracking, union-find, DP (15 patterns), greedy/intervals, bit manipulation & math (interview depth), range queries (prefix sums / Fenwick / segment tree) | [`02-algorithms/`](02-algorithms/README.md) |
| **Practice bank** | 200 walkthrough problems, tier-tagged, one file per topic + design-a-data-structure | [`04-practice/`](04-practice/README.md) |
| **Thinking & patterns** | first-principles derivation, pattern triggers, ladders, in-interview judgment, mocks | [`03-patterns/`](03-patterns/README.md) |
| **Behavioral** | Googliness attributes, STAR story bank | [`05-behavioral/`](05-behavioral/README.md) |
| **Round execution** | 45-min clock, constraint → Big-O, edge cases, what to skip | [L3 Cheatsheet](00-start-here/L3_CHEATSHEET.md) |

**Not in scope:** system design, LLD, concurrency, SQL. **Covered but `💤 T3` at L3** (promote for L4+ / hard rounds): segment trees / Fenwick trees, advanced graphs (Floyd-Warshall, Tarjan/SCC), bitmask/digit/game DP — see [What to Skip at L3](00-start-here/L3_CHEATSHEET.md) and the [L4 delta](00-start-here/l4-sde2-delta.md).

**Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](00-start-here/l3-google-roadmap.md#tier-legend)). L4/senior bars layer on top via the [L4 delta](00-start-here/l4-sde2-delta.md) and [senior delta](00-start-here/sde3-senior-delta.md).

---

## How loops differ by company

The DSA core is the same everywhere; the format changes what to drill. Verify current format with your recruiter — loops change.

| Company | Coding format (typical) | Adjust your prep |
|---|---|---|
| **Google** | 1 medium(-hard) per 45 min, follow-ups escalate; Google Doc / no autocomplete; hiring committee reads notes | Narrate complexity and trade-offs; expect "now make it streaming / scale it" follow-ups ([senior chains](03-patterns/INTERVIEW_JUDGMENT.md#part-e--senior-follow-up-chains)) |
| **Meta** | **2 problems in ~40 min**, mostly LeetCode-medium staples; speed and bug-free code matter most | Drill T1 to < 15 min each; less exploration, more pattern recall; run timed doubles in [mocks](03-patterns/INTERVIEW_JUDGMENT.md#part-d--mock-rounds) |
| **Amazon** | 1–2 problems per round, each round also probes **Leadership Principles** | Prepare LP stories alongside code ([behavioral](05-behavioral/README.md)); design-a-data-structure is common ([design practice](04-practice/data-structures/14-design.md)) |
| **Microsoft / Apple** | Team-dependent; mediums, often linked lists, trees, strings, design-a-class | T1/T2 breadth; clean OOP for design problems |
| **Uber / Stripe / fintech** | Longer practical problems (parsing, simulation, rate limiters, iterators) | [Design practice](04-practice/data-structures/14-design.md), heap/interval simulation, clean code over tricks |
| **Hard-round companies** (some L4+ Google/Meta, HFT, competitive-leaning) | Hards: range queries, bitmask/digit DP, game DP | Promote `💤 T3` in [Range Queries](02-algorithms/19-range-queries.md), [DP](04-practice/algorithms/15-dynamic-programming.md), [Graph algorithms](04-practice/algorithms/13-graph-algorithms.md) |

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
| 1 | Read the plan and the round clock | [L3 roadmap](00-start-here/l3-google-roadmap.md) · [L3 Cheatsheet](00-start-here/L3_CHEATSHEET.md) |
| 2 | Learn how to derive patterns | [How to Think](03-patterns/HOW_TO_THINK.md) |
| 3 | Per topic: lecture, then the practice file, T1 first | [DS index](01-data-structures/README.md) · [Algo index](02-algorithms/README.md) |
| 4 | Recursion & DP from zero | [Masterclass](03-patterns/RECURSION_AND_DP_MASTERCLASS.md) |
| 5 | Pressure-test with ladders and mocks | [Ladders](03-patterns/HOW_TO_THINK.md#part-iv--pattern-ladders) · [Mocks](03-patterns/INTERVIEW_JUDGMENT.md#part-d--mock-rounds) · [Interview Judgment](03-patterns/INTERVIEW_JUDGMENT.md) |
| 6 | Behavioral stories | [Behavioral + Googliness](05-behavioral/BEHAVIORAL_GOOGLINESS.md) |
| 7 | Final week | [Revision guide](03-patterns/INTERVIEW_JUDGMENT.md#part-c--round-execution--revision) · [Mind map](03-patterns/mindmap.md) |

---

## Quick revision

| What | Link |
|------|------|
| Mind map | [`mindmap.md`](03-patterns/mindmap.md) |
| Pattern triggers, decision trees, problem recognition | [`03-patterns/patterns-master.md`](03-patterns/patterns-master.md) |
| Full problem index (200, by topic) | [`04-practice/README.md`](04-practice/README.md) |
| Interview strategy / day-of revision | [`03-patterns/INTERVIEW_JUDGMENT.md` Part C](03-patterns/INTERVIEW_JUDGMENT.md#part-c--round-execution--revision) |
| L4 (SDE-2) delta | [`00-start-here/l4-sde2-delta.md`](00-start-here/l4-sde2-delta.md) |
| SDE-3 / senior delta | [`00-start-here/sde3-senior-delta.md`](00-start-here/sde3-senior-delta.md) |
| Senior follow-up chains | [`03-patterns/INTERVIEW_JUDGMENT.md` Part E](03-patterns/INTERVIEW_JUDGMENT.md#part-e--senior-follow-up-chains) |
| Striver A2Z course notes (lesson-by-lesson) | [`striver-a2z/`](striver-a2z/README.md) |

### Flashcards (189 cards, spaced repetition)

Every lecture ends with a `## Flashcards` section. A card is a bold question line tagged `#flashcard`, followed by the answer up to the next blank line:

```
**What does `lps[i]` mean in KMP?** #flashcard
Longest proper prefix of pattern[:i+1] that is also a suffix…
```

- **Anki:** export every card to a tab-separated file, then *File → Import* into a Basic note type with "Allow HTML" on. Multi-line answers are joined with `<br>`. The command skips `striver-a2z/` (~1,400 course cards); drop `--exclude-dir=striver-a2z` to include them.
  ```sh
  grep -rl --include='*.md' --exclude-dir=striver-a2z '#flashcard$' . | xargs awk '/#flashcard$/{if(q)print q"\t"a; q=$0; sub(/ *#flashcard$/,"",q); a=""; next} q&&/^(---)?$/{if(a!=""){print q"\t"a; q=""}; next} q{a=(a==""?$0:a"<br>"$0)} END{if(q)print q"\t"a}' > flashcards.tsv
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

Full daily plan: [`00-start-here/l3-google-roadmap.md`](00-start-here/l3-google-roadmap.md)
