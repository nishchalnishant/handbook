# 05 Splitwise — THE SCRIPT, run end to end

Procedure: `notes/THE_SCRIPT.md`. Decision tree: `notes/TEXT_TO_CODE.md`.

> **Read this AFTER your own attempt.** This is the capstone — closest to a real
> 45-minute round. Do Phases 1–4 yourself before opening this.

The distinguishing feature: **the data model is the whole answer.** Get the debt graph
right and every method falls out. Get it wrong and you fight the problem for 45 minutes.

---

## PHASE 1 — SCOPE (0:00–5:00)

> "So we're building expense sharing. Users in groups, someone pays, the cost splits
> among participants, and we can ask who owes whom — plus a settle-up that minimises
> transactions.
>
> Scoping to in-memory, single currency, no auth, no persistence. I'll represent money
> as **long paise, not double** — I'll say why in a second.
>
> The two interesting parts are the **debt data model** and the **simplify algorithm**,
> so that's where I'll spend the time. Sound right?"

**The three questions:**

| Ask | What you're really doing |
|---|---|
| "What split types — equal, exact, percentage?" | fishing for the **interface** |
| "Do I need who-owes-whom, or just a net balance per person?" | **the pivotal question** — see Phase 3 |
| "Should settle-up minimise the number of transactions?" | scoping in the greedy algorithm |

### Say the money thing early — **verified**

> *"One thing up front: I'll use `long` paise rather than `double`, because
> `0.1 + 0.2 != 0.3` in binary floating point — money errors accumulate and you can't
> reconcile a ledger that's off by a fraction of a cent."*

```
0.1 + 0.2 == 0.3 ?  false
0.1 + 0.2        =  0.30000000000000004
```

Unprompted, in Phase 1, this lands very well. The README asks you to know it.

---

## PHASE 2 — NOUNS (5:00–10:00)

```
User   Group   Expense   Split   SplitType   Balance   Debt   Transaction   Currency
```

**Merge and defer:**
- *"`Currency` is out of scope — single currency for now."*
- *"`Balance` isn't stored; it's **derived** from the debt graph. If I store it too,
  I have two sources of truth that can disagree."*
- *"`Transaction` I'll keep, as the output of settle-up — a record."*

Leaves: **User, Group, Expense, SplitStrategy, DebtGraph, Transfer.**

"Balance is derived, not stored" is a real modelling insight — say it.

---

## PHASE 3 — DECIDE (10:00–15:00)

| Noun | Question asked | Answer |
|---|---|---|
| `User` | identity, stable | **record** `User(String id, String name)` |
| `Transfer` | value: from, to, amount | **record** `Transfer(String from, String to, long paise)` |
| `Expense` | value once created | **record** |
| `Group` | membership changes | **class** |
| `DebtGraph` | the mutable core | **class** |
| `SplitStrategy` | Q3 — "EQUAL, EXACT, PERCENTAGE" | **interface** |

### The pivotal decision — say this out loud, it is the whole problem

> *"The tempting model is a single net number per user. It's wrong, and here's the
> proof: if X owes Y 300, X's net is −300. If X owes Z 300 instead, X's net is **also**
> −300. Same net, different creditor — so a net number literally cannot answer 'whom do
> I owe'. I need the edge, not the node."*

**Verified:**
```
x owes y 300 -> net {x=-300, y=300}
x owes z 300 -> net {x=-300, z=300}
same net for x, DIFFERENT creditor
```

So: `Map<Debtor, Map<Creditor, Long>>`. Net balances are computed **from** it when
needed, never stored alongside it.

---

## PHASE 4 — API (15:00–20:00)

```java
record User(String id, String name) {}
record Transfer(String from, String to, long paise) {}

interface SplitStrategy {
    // returns how much each participant OWES for this expense, in paise
    Map<String, Long> split(long totalPaise, List<String> participants, List<Long> args);
}

class EqualSplit      implements SplitStrategy { }   // args ignored
class ExactSplit      implements SplitStrategy { }   // args = exact paise, must sum to total
class PercentageSplit implements SplitStrategy { }   // args = percents, must sum to 100

class DebtGraph {
    private final Map<String, Map<String, Long>> owes;   // debtor -> creditor -> paise
    void add(String debtor, String creditor, long paise);
    Map<String, Long> net();                             // DERIVED
}

class ExpenseService {
    void addExpense(String payer, long totalPaise, List<String> participants,
                    SplitStrategy strategy, List<Long> args);
    Map<String, Long> balances(String user);
    List<Transfer> simplify();
}
```

**Say:** *"`args` being a `List<Long>` is a little loose — exact amounts and percentages
mean different things. In production I'd use a sealed type per split. For 45 minutes
this keeps one interface, and I'll note the trade-off."*

Flagging your own compromise is better than the interviewer finding it.

**Checkpoint:** *"Model look right before I write simplify?"*

---

## PHASE 5 — CODE (20:00–35:00)

> "I'll implement `EqualSplit` with correct remainder handling, and `simplify`."

### The remainder — the README's explicit "done when" — **verified**

1000 paise split three ways is 333.33 each. You cannot drop the paisa:

```java
public Map<String,Long> split(long total, List<String> people, List<Long> ignored) {
    Map<String,Long> out = new LinkedHashMap<>();
    long n = people.size(), base = total / n, rem = total % n;
    for (int i = 0; i < n; i++)
        out.put(people.get(i), base + (i < rem ? 1 : 0));   // first `rem` people pay 1 extra
    return out;
}
```

```
1000 paise / 3 -> {a=334, b=333, c=333}   sum=1000
```

> *"The invariant is that the shares sum **exactly** to the total. I give the remainder
> paise to the first N people. Any deterministic rule works — what matters is that
> nothing is lost."*

Percentage has the same trap, solved by giving the last person the remainder:

```
1000 paise at 33/33/34 -> {a=330, b=330, c=340}   sum=1000
```

And `ExactSplit` **validates**: `rejected: exact amounts must sum to total`.

### simplify — greedy, with a priority queue

```java
// largest debtor pays largest creditor, repeat
while (!creditors.isEmpty() && !debtors.isEmpty()) {
    var c = creditors.poll(); var d = debtors.poll();
    long amt = Math.min(c.getValue(), -d.getValue());
    out.add(new Transfer(d.getKey(), c.getKey(), amt));
    if (c.getValue() - amt > 0) creditors.add(Map.entry(c.getKey(), c.getValue() - amt));
    if (d.getValue() + amt < 0) debtors.add(Map.entry(d.getKey(), d.getValue() + amt));
}
```

---

## PHASE 6 — EXTEND (35:00–45:00)

### The proof — a 3-person cycle vanishes — **verified**

```
a->b 500, b->c 500, c->a 500
  edges before simplify: 3
  net: {a=0, b=0, c=0}
  transfers after simplify: 0
  net sums to zero? true
```

> *"Three debts, zero transactions. Everyone owes exactly what they're owed, so the
> cycle cancels. That's the case that shows simplify is doing something real."*

This is a much stronger demo than reducing 3 edges to 2.

### Follow-up #1 — "Is greedy optimal?"

Be honest — this is a known hard problem:

> *"Greedy gives at most n−1 transfers, which is a good bound, but it is **not** always
> minimal. Minimising exactly is NP-hard — it's equivalent to a set-partition problem,
> since you'd need to find every subset that sums to zero and settle it internally.
> Greedy is what production systems ship, and I'd say so rather than claim optimality."*

Saying "NP-hard, and here's why greedy is still right" is a senior-level answer.

### Follow-up #2 — "Add a new split type" (e.g. shares/weights)

> *"One new class implementing `SplitStrategy`, zero edits. Same remainder discipline —
> shares sum to the total."*

### Follow-up #3 — "Multiple currencies" (README stretch)

> *"Money becomes `record Money(long minorUnits, Currency ccy)` and you refuse to add
> two different currencies — that's a bug, not a conversion. Conversion needs a rate
> **and a timestamp**, since the rate at expense time differs from settle time. I'd
> store the original currency and convert only for display."*

### Follow-up #4 — "Audit log of every change" (README stretch)

> *"Event sourcing, lightly: store `List<ExpenseAdded>` as the source of truth and make
> the debt graph a **projection** you can rebuild by replay. That also gives undo for
> free — drop the event and rebuild. It's the Command pattern at the system level."*

### Follow-up #5 — "Concurrency — two people add expenses at once"

1. **In-process:** `addExpense` is read-modify-write on the graph; needs to be atomic
   per group. Lock per group, not globally — different groups never interact.
2. **Correctness:** *"`simplify` must see a consistent snapshot, or it emits transfers
   for a state that never existed."*
3. **Multi-machine:** *"the debt graph goes to a database with a transaction per
   expense. With the event log, appends are naturally serialisable — you append events
   and rebuild, which sidesteps most of the locking."*

---

## Done when (from the README)

- three-way split with a remainder distributes paise correctly
- `simplify` reduces a 3-person cycle and totals still balance

---

## Self-check

- [ ] Said the `double` money problem in Phase 1, unprompted
- [ ] Proved why net-per-user is insufficient before choosing the graph
- [ ] Said "balance is derived, not stored"
- [ ] Handled the remainder so shares sum exactly
- [ ] Admitted greedy isn't optimal and named why
- [ ] Reached Phase 6 with time left

Verified backing: `notes/oop_proofs/LldInterviewProofs.java` — class `Section5Splitwise`.
