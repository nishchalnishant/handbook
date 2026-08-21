# Vending Machine — THE SCRIPT, run end to end

> Spoiler. Attempt Phases 1–4 in `ATTEMPT.md` first.
>
> **Verified backing**: every claim below comes from running `VendingMachine.java`
> in this folder — `javac VendingMachine.java && java VendingMachine` → **20 PASS, 0 FAIL**.

This is *the* State-pattern problem. Almost everyone answers it with an enum and
a switch, which works and scores a B. The A answer is that the illegal
transitions should be **unrepresentable**, not checked.

---

## Phase 1 — SCOPE (0:00–5:00)

Five questions. Two of them are planted: the answer changes the design, not just
the code.

1. **"Can the machine run out of change, and if so what should it do?"**
   → *Planted.* If change can fail, `dispense()` must compute the payout
   **before** it commits the sale, and refund on failure. If I assume infinite
   change I write a one-line subtraction and get the ordering wrong forever.
2. **"Is cancel a full refund of the exact coins, or a refund of the value?"**
   → *Planted.* "Exact coins" means I must keep the inserted coins as a `List`,
   not just a running total. That is a data-structure decision made in minute 2.
3. **"What denominations? Fixed set or arbitrary?"** → decides whether greedy
   change-making is legal (see Phase 6).
4. **"Card payments?"** → No. If yes, `Payment` becomes a Strategy interface.
5. **"One machine, or a fleet reporting to a server?"** → One. In-memory.

**Say out loud what you are not building:** no card payments, no persistence, no
restock scheduling, no telemetry, no multi-machine coordination.

---

## Phase 2 — NOUNS (5:00–10:00)

Underlined from the statement: *machine, item, code, price, inventory, coin,
denomination, change, state, transaction, user, slot, bank*.

Thirteen nouns is a trap. Cut to five:

| Noun | Test | Verdict |
|---|---|---|
| Item | value, never mutates | `record Item(String code, String name, int priceMinor)` |
| Coin | fixed known list, differs only by a number | `enum Coin { FIVE(5), TEN(10), TWENTY(20), FIFTY(50) }` |
| Result | value returned from one call | `record Result(Item, List<Coin>)` |
| State | see Phase 3 — the whole question | `interface MachineState` + 3 classes |
| VendingMachine | owns mutable state | `class` |

Cut, with a reason each:
- **denomination** — that *is* `Coin`. Same noun twice.
- **inventory / bank / slot** — not classes, they are `Map` fields on the machine.
  A class with one field and no behaviour is a `Map` you have made harder to read.
- **transaction** — nothing outlives the call. It would be a class with a
  lifetime of four lines.
- **user** — outside the box. The machine has no idea who you are.

---

## Phase 3 — DECIDE (10:00–15:00)

Run `Coin` through THE BIG DECISION: Q1 — do the variants differ only by data
(a number), and is the list fixed? **Yes.** Enum with a field. Stop. Do not
build a `Coin` interface with four implementations.

Now `State`, the real question.

Q1: do the states differ only by data? **No** — they differ by *which actions are
legal*, which is behaviour. Q2: shared mutable state? **No** — all the mutable
state lives on the machine; a state object holds nothing. Q3: is it a capability?
**Yes**, effectively — "can accept a coin", "can dispense". → **interface**.

So: `interface MachineState` with one method per user action, and three
implementing classes: `IdleState`, `ItemSelectedState`, `HasMoneyState`.

**Why this beats an enum + switch — the sentence to say:**

> With an enum I write `if (state != HAS_MONEY) throw` at the top of every
> method, and adding a fourth state means finding every one of those checks. With
> a state class, `IdleState` simply has no working `dispense()`. The illegal
> transition isn't checked, it's absent.

The trick that makes this cheap is a **default method on the interface** that
throws:

```java
interface MachineState {
    String name();
    default Result dispense(VendingMachine m) { throw illegal("dispense"); }
    ...
}
```

Each state overrides only what it permits. `IdleState` is nine lines. Illegal
transitions get a uniform, informative error for free —
`"dispense is not legal in state IDLE"` — with no per-method boilerplate.

**Note where the states live.** They mutate the machine, not themselves. That is
why `VendingMachine` exposes package-private hooks (`addCoin`, `setState`,
`commitSale`) and the public API is four one-line delegations. There is not a
single `if (state == ...)` anywhere in `VendingMachine`. That is the check to
run on your own answer.

**The pattern I declined.** The source lists Strategy for payment and Command for
dispense. Both fail Q4: there is exactly one payment mechanism (coins) and
exactly one dispense action. YAGNI. Adding them here is inventing a hierarchy for
one thing. Say so out loud — declining a pattern for a stated reason scores
better than applying one.

**Money.** `int` minor units. Never `double`. A machine that loses a fraction of
a cent per sale is a bug that compounds across a million sales.

---

## Phase 4 — API (15:00–20:00)

Signatures before bodies:

```java
boolean    selectItem(String code);   // false = no such item / out of stock
void       insertCoin(Coin c);
Result     dispense();                // throws if not payable
List<Coin> cancel();                  // the exact coins back
```

**`selectItem` returns `boolean`, `dispense` throws.** That asymmetry is
deliberate and worth defending: out-of-stock is an *expected outcome* of a
correct call, so it is a return value. Calling `dispense()` in `IDLE` is a
*programming error* — the caller violated the protocol — so it throws. Using
exceptions for expected outcomes, or booleans for bugs, are both smells.

---

## Phase 5 — CODE (20:00–35:00)

The one piece of real logic is change-making, and it is where the sequencing
matters:

```java
public Result dispense(VendingMachine m) {
    int owed = m.insertedTotal() - item.priceMinor();
    List<Coin> change = m.makeChange(owed);      // compute...
    if (change == null) { m.refundAll(); throw ... }   // ...verify...
    m.commitSale(item, change);                  // ...only then commit
}
```

Dispensing the item and *then* discovering you cannot pay the change is the one
outcome a real machine must never produce. Compute, verify, commit — in that
order. The test asserts it holds: on failure, stock is untouched and the machine
is back in `IDLE`.

The invariant test worth writing is **money conservation**:

```
bank_after == bank_before + inserted - change_paid_out
```

Verified in the run. This catches an entire family of bugs — double-crediting
inserted coins, forgetting to debit change, refunding into the bank — that
per-operation assertions miss, because it constrains the *whole* system rather
than one call.

---

## Phase 6 — EXTEND (35:00–45:00)

**1. "Your greedy change algorithm — is it correct?"**

Only for canonical denominations. With 5/10/20/50 greedy is optimal. With
`{1, 3, 4}` it makes 6 as `4+1+1` (three coins) when `3+3` (two) is optimal, and
for `{1, 5, 8}` making 10 greedy uses `8+1+1` instead of `5+5`. Worse, greedy can
fail to find a solution that exists at all when the bank is partially stocked.
The general answer is a coin-change DP over the available inventory, O(amount ×
denominations). Volunteer this before you are asked — the interviewer is usually
fishing for exactly it.

**2. "Two people use it at once."** Three layers:
- *In-process:* one `synchronized` on the machine object is genuinely sufficient
  here — there is one physical coin slot, so serialising is the truth, not a
  compromise.
- *The hazard:* `selectItem` then `insertCoin` is check-then-act. Between them
  another thread could buy the last unit. Either hold a reservation on select, or
  re-verify stock inside the committed section. This file re-verifies at commit.
- *Multi-machine:* a fleet sharing a stock database needs `UPDATE stock SET
  qty = qty - 1 WHERE code = ? AND qty > 0` and a check of the affected-row
  count, or a version column CAS. Never read-then-write.

**3. "Add card payment."** Now Strategy *is* justified — the rule of three has
been met. `interface Payment { boolean authorize(int minor); }`, injected. Note
the state machine barely changes: `HasMoneyState` becomes "funds secured",
however they were secured.

**4. "Add a maintenance/out-of-service state."** One new class implementing
`MachineState`, overriding nothing (so everything throws) except a
`resume()` transition. **Zero edits to existing code.** That is the extension
test, and it is the payoff for Phase 3.

**5. "Partial refund when the item jams mid-dispense."** Needs a fourth state
(`DISPENSING`) and, honestly, a persistent transaction log — a power cut between
debit and drop must be recoverable. This is where an in-memory design stops being
adequate and you say so.

**6. "Test it properly."** Beyond the 20 assertions: a randomised money-conservation
fuzz — thousands of random select/insert/cancel/dispense sequences, asserting after
each that `bank + inserted == initial + revenue`. Any sequencing bug shows up as a
drift in that one number.

---

## Self-check

- Did you make illegal transitions *impossible*, or merely *checked*?
- Did you compute change before committing the sale?
- Did you volunteer the greedy-is-not-general caveat unprompted?
- Did you decline at least one pattern the problem seems to invite, with a reason?
- Is there any `if (state == ...)` left in your machine class? If yes, you wrote
  the enum answer wearing a State-pattern costume.
