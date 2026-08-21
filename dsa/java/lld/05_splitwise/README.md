# LLD 05 — Splitwise (the capstone)

> **Spoiler warning — this folder now contains a worked solution.**
> `Splitwise.java` is a complete, compiling reference implementation and
> `INTERVIEW.md` is the same design spoken aloud as a 45-minute answer,
> following `notes/THE_SCRIPT.md`.
>
> **Write your own version first.** Do Phases 1–4 (scope, nouns, decisions, API
> signatures) yourself — 20 minutes, no bodies — then implement, and only then
> read either file. Opening them first turns production practice back into
> reading, which is the exact gap this repo exists to close.
>
>     javac Splitwise.java && java Splitwise

The hardest one here, and closest to a real 45-minute interview.

## Requirements
- users, groups
- add an expense: payer, amount, participants, split type
- split types: EQUAL, EXACT amounts, PERCENTAGE  (-> interface, obviously)
- `balances(user)` — who owes them, whom they owe
- `simplify(group)` — minimize the number of transactions to settle up

## Where people go wrong
Storing a single net number per user loses information about WHO owes WHOM.
Model the debt graph properly: a map of (debtor, creditor) -> amount.
Get that data model right and the rest falls out; get it wrong and every
method fights you.

`simplify` is a genuinely interesting greedy algorithm: repeatedly match
the largest creditor with the largest debtor. Use a priority queue.

## Done when
- an expense split three ways with a remainder distributes cents correctly
  (do NOT use double for money — use long paise/cents, or BigDecimal.
   Ask yourself why 0.1 + 0.2 != 0.3 before you decide.)
- simplify reduces a 3-person cycle to fewer transactions and you can
  prove the totals still balance

## Stretch
- multiple currencies
- an audit log of every change (event sourcing, lightly)
