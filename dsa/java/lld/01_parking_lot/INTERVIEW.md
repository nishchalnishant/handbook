# 01 Parking Lot — THE SCRIPT, run end to end

Procedure: `notes/THE_SCRIPT.md`. Decision tree: `notes/TEXT_TO_CODE.md`.

This is the one problem where the code already exists (`ParkingLot.java`).
Read this walkthrough, then **check the claims against that file** — every
declaration below is really in it.

---

## PHASE 1 — SCOPE (0:00–5:00)

> "So we're building a parking lot. Vehicles arrive, get a spot and a ticket,
> and pay based on how long they stayed.
>
> I'm scoping this to a single lot, in-memory, no persistence and no payment
> gateway — `pay()` will be out of scope. Single-threaded to start; I'll come
> back to concurrency because that's where the real bug is.
>
> The interesting part is the fee rules, since those change constantly in the
> real world. I'll design so a new fee rule costs one class. Sound right?"

**The three questions** (two of them planted):

| Ask | What you're really doing |
|---|---|
| "Are there different vehicle types with different sizes?" | fishing for the **enum** |
| "Do fee rules change — weekends, holidays, EV rates?" | fishing for the **interface** |
| "Can two cars arrive at the same instant?" | pre-loading the **concurrency** follow-up |

---

## PHASE 2 — NOUNS (5:00–10:00)

> "Let me pull out the entities."

```
Vehicle   Spot   Ticket   Lot   Floor   FeeRule   Payment
```

**Merge and defer, out loud:**
- *"Payment I'll defer — it doesn't affect the core flow."*
- *"Floor I'll defer too; it's a grouping of Spots and I can add it later without
  changing anything else."*

Leaves five: **Vehicle, Spot, Ticket, Lot, FeeRule.**

---

## PHASE 3 — DECIDE (10:00–15:00)

| Noun | Question asked | Answer | Say out loud |
|---|---|---|---|
| `VehicleType` | Q1 — fixed list, differ only by size? **YES** | **enum** | *"Fixed and known at compile time, and they differ only by a size number."* |
| `Vehicle` | value, never changes | **record** | *"Plate and type — pure data."* |
| `Ticket` | value, issued once | **record** | *"Issued once and never mutated."* |
| `Spot` | state changes (occupied/free) | **class** | *"Its occupant changes over time, so it's a class."* |
| `Lot` | owns the spots and tickets | **class** | *"Owns the collections, so it owns the operations."* |
| `FeeStrategy` | Q3 — "different ways to price" | **interface** | *"Open-ended and behavioural — new rules keep appearing."* |

### The distinction worth stating explicitly

> *"Note both `VehicleType` and `FeeStrategy` are 'things that vary', but they get
> different treatment. Vehicle types are a **fixed, enumerable** set that differ only
> by **data** — that's an enum. Fee rules are **open-ended** and differ by
> **behaviour** — that's an interface. Getting that split right is most of this design."*

That paragraph alone distinguishes a strong candidate. **No abstract class here** —
nothing shares mutable state.

---

## PHASE 4 — API (15:00–20:00)

```java
enum VehicleType { BIKE(1), CAR(2), TRUCK(4); int size(); }

record Vehicle(String plate, VehicleType type) {}
record Ticket(String id, Vehicle vehicle, Spot spot, LocalDateTime entryTime) {}

interface FeeStrategy {
    double calculate(Ticket ticket, LocalDateTime exit);
}

class Spot {
    boolean isFree();
    boolean canFit(VehicleType t);
    void occupy(Vehicle v);
    void release();
}

class Lot {
    private final List<Spot> spots;
    private final Map<String, Ticket> active;
    private final FeeStrategy feeStrategy;      // injected, not new'd -> DIP

    boolean hasSpace(VehicleType type);
    Ticket park(Vehicle v);
    double unpark(String ticketId, LocalDateTime exit);
}
```

**Ownership, stated:** *"`park` lives on `Lot` because `Lot` owns the spot list.
`canFit` lives on `Spot` because only the spot knows its own size."*

**Checkpoint:** *"Does this shape look right before I implement?"*

---

## PHASE 5 — CODE (20:00–35:00)

> "I'll implement `park`, `unpark`, and the hourly fee. `release` and the getters
> are one-liners — I'll stub them."

`park` is the method with the real logic:

```java
Ticket park(Vehicle v) {
    Spot spot = spots.stream().filter(s -> s.canFit(v.type())).findFirst()
                     .orElseThrow(() -> new IllegalStateException("lot full"));
    spot.occupy(v);
    Ticket t = new Ticket(UUID.randomUUID().toString(), v, spot, LocalDateTime.now());
    active.put(t.id(), t);
    return t;
}
```

Then `unpark` delegates pricing rather than computing it — that's the whole point
of the interface:

```java
double unpark(String ticketId, LocalDateTime exit) {
    Ticket t = active.remove(ticketId);
    if (t == null) throw new IllegalArgumentException("unknown ticket " + ticketId);
    t.spot().release();
    return feeStrategy.calculate(t, exit);     // Lot does NOT know how pricing works
}
```

---

## PHASE 6 — EXTEND (35:00–45:00)

### Follow-up #1 — "Add weekend pricing" (this is README exercise 1)

> *"That's one new class implementing `FeeStrategy`, and zero edits to `Lot`.
> That's exactly why the interface is there."*

```java
class WeekendFee implements FeeStrategy {
    public double calculate(Ticket t, LocalDateTime exit) { /* half rate */ }
}
```

**If you had to edit `Lot`, your Phase 3 was wrong.** That's the feedback loop.

### Follow-up #2 — "Two cars arrive at once" (README exercise 5) — **verified**

```
unsafe: 10 cars assigned the SAME spot  <-- broken
safe:   1 car assigned the spot         <-- correct
```

The bug is that find-then-claim is **two** steps:

```java
Spot s = spots.stream().filter(...).findFirst().orElse(null);   // thread A and B both see it free
s.occupy(v);                                                     // both claim it
```

The three layers:

1. **In-process:** the find and the claim must be **one atomic step**. Synchronise
   that block — not the whole method.
2. **Smallest correct block** (the README's real question): *"the fee calculation
   stays outside the lock, because it touches no shared state. Only find+claim
   needs to be atomic."*
3. **Multi-machine:** across servers a JVM lock is meaningless — you'd need a unique
   constraint on `spot_id` where occupant is null, or `SELECT … FOR UPDATE`.

### Follow-up #3 — "Add floors" (exercise 2)

> *"`Floor` owns a list of `Spot`, and `Lot` owns a list of `Floor`. The search moves
> to `Floor.findSpot()`, and `Lot` just asks each floor in order. `Spot` doesn't change
> at all — which tells me the boundary is right."*

### Follow-up #4 — "Prefer the nearest floor" (exercise 3)

> *"That's a second axis of variation, so it's a second interface —
> `SpotSelectionStrategy`. Note I would NOT have added it upfront; that's YAGNI. But
> now that a second rule exists, the interface is justified."*

Knowing *when* to add the abstraction is as valuable as knowing how.

### Follow-up #5 — "Add an ElectricSpot that bills for kWh" (exercise 4)

The trap. Think out loud:

> *"Tempting to subclass `Spot`. But run the tree: do electric spots share **mutable
> state** with regular spots? Yes — occupant. So Q2 says abstract class is defensible.
> But the difference is really about **billing**, not about being a spot. I'd rather
> keep `Spot` concrete, add a `chargedKwh` field, and put the pricing in a
> `FeeStrategy` that reads it. That keeps one axis of variation in one place."*

Committing to a trade-off with a reason scores higher than picking the "right" answer.

---

## Self-check

- [ ] Said *why* `VehicleType` is an enum but `FeeStrategy` is an interface
- [ ] Injected `FeeStrategy` rather than `new`-ing it inside `Lot`
- [ ] Answered "add weekend pricing" with one class, zero edits
- [ ] Gave all three concurrency layers, including "smallest correct block"
- [ ] Reached Phase 6 with time to spare

Verified backing: `ParkingLot.java` in this folder — `javac ParkingLot.java && java ParkingLot`
prints 4 PASS lines, and every number quoted above is copied from that run.
