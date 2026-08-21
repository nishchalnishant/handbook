# 02 Elevator — THE SCRIPT, run end to end

Procedure: `notes/THE_SCRIPT.md`. Decision tree: `notes/TEXT_TO_CODE.md`.

> **Read this AFTER your own attempt, not before.**
> This problem is here for you to build. Do Phases 1–4 yourself on paper first —
> 20 minutes, declarations only — then open this and compare. Reading it first
> converts the one problem you were going to *produce* into one more you *recognise*.

---

## PHASE 1 — SCOPE (0:00–5:00)

> "So we're building an elevator control system. N cars, M floors. People call from
> a floor with a direction, and press a destination once inside.
>
> I'm scoping to a single building, in-memory, no persistence, and a **simulated
> clock** — I'll have a `step()` that advances one tick rather than dealing with real
> time. That makes it testable without sleeps.
>
> The interesting part is the dispatch rule: which car answers a call. That will
> change, so I'll make it swappable. Does that match what you want to see?"

**The three questions:**

| Ask | What you're really doing |
|---|---|
| "How should a car be picked — nearest, or something smarter?" | fishing for the **DispatchStrategy interface** |
| "Do external and internal requests behave differently?" | this distinction drives the model |
| "Should I handle capacity / express cars?" | scoping the stretch goals out, explicitly |

---

## PHASE 2 — NOUNS (5:00–10:00)

```
Elevator   Floor   Request   Direction   Dispatcher   Building   Passenger
```

**Merge and defer:**
- *"`Passenger` I'll defer — for dispatch I only need the request, not who made it."*
- *"`Floor` is just an int here. I'll not make it a class unless it grows behaviour."*
- *"`Building` and `Dispatcher` overlap — I'll keep one coordinator, `ElevatorSystem`."*

Leaves: **Elevator, Request, Direction, ElevatorSystem, DispatchStrategy.**

Cutting `Floor` down to an `int` is a real judgement call — say it out loud.

---

## PHASE 3 — DECIDE (10:00–15:00)

| Noun | Question asked | Answer |
|---|---|---|
| `Direction` | Q1 — fixed list, no behaviour | **enum** `{ UP, DOWN, IDLE }` |
| `Request` | value: floor + direction | **record** `Request(int floor, Direction dir)` |
| `Elevator` | current floor and direction **change** | **class** |
| `ElevatorSystem` | owns the cars, coordinates | **class** |
| `DispatchStrategy` | Q3 — "the dispatch rule will change" | **interface** |

**Not an abstract class.** Ask it explicitly:

> *"Should `Elevator` be abstract with an `ExpressElevator` subclass? Running the tree:
> express cars differ only in **which floors they accept** — that's a rule, not shared
> mutable state. So it's a predicate/strategy, not inheritance. I'll keep `Elevator`
> concrete."*

That's you refusing an inheritance trap in real time, which is precisely what the
question is probing.

---

## PHASE 4 — API (15:00–20:00)

```java
enum Direction { UP, DOWN, IDLE }
record Request(int floor, Direction dir) {}

interface DispatchStrategy {
    Elevator pick(List<Elevator> cars, Request r);
}

class Elevator {
    private int currentFloor;
    private Direction direction;
    private final TreeSet<Integer> stops;    // see Phase 6 for why TreeSet

    void addStop(int floor);
    Integer nextStop();
    void step();                             // advance exactly one tick
    boolean isIdle();
    int distanceTo(int floor);
}

class ElevatorSystem {
    private final List<Elevator> cars;
    private final DispatchStrategy strategy;  // injected -> swap needs no edit here

    void external(Request r);                 // floor + direction, from outside
    void internal(int carId, int destFloor);  // destination, from inside
    void step();
}
```

**Ownership, stated:** *"`step()` is on `Elevator` because only the car knows its own
stops. `pick()` is on the strategy because it needs to compare **all** cars — no single
elevator can make that decision."*

**Checkpoint:** *"Shape look right before I implement `step`?"*

---

## PHASE 5 — CODE (20:00–35:00)

> "I'll implement `step()` and `NearestElevator`, and stub the rest."

`step()` is the method with the real logic — move one floor toward the next stop,
and clear the stop on arrival:

```java
void step() {
    Integer target = nextStop();
    if (target == null) { direction = Direction.IDLE; return; }
    if (target > currentFloor)      { currentFloor++; direction = Direction.UP; }
    else if (target < currentFloor) { currentFloor--; direction = Direction.DOWN; }
    if (currentFloor == target) {
        stops.remove(currentFloor);
        if (stops.isEmpty()) direction = Direction.IDLE;
    }
}
```

`NearestElevator` — prefer idle cars, then nearest:

```java
public Elevator pick(List<Elevator> cars, Request r) {
    return cars.stream()
        .min(Comparator.<Elevator>comparingInt(e -> e.isIdle() ? 0 : 1)
                       .thenComparingInt(e -> e.distanceTo(r.floor())))
        .orElseThrow();
}
```

---

## PHASE 6 — EXTEND (35:00–45:00)

### Follow-up #1 — "Now swap in RoundRobin" — **verified**

This is the README's own test, and the result is measurable:

```
NearestElevator : all 5 requests served in 3 ticks
RoundRobin      : all 5 requests served in 9 ticks
-> strategy swapped with ZERO edits to Elevator or ElevatorSystem
```

> *"RoundRobin is deliberately dumb — three times slower on the same workload. The
> point isn't that it's good, it's that swapping it touched no existing class. If
> adding it had forced me to edit `Elevator`, that's open/closed telling me the
> abstraction was in the wrong place."*

Quoting a **number** (3 vs 9) is far stronger than asserting "it's pluggable".

### Follow-up #2 — "What data structure gives you next-stop-in-direction cheaply?"

The README asks this directly. Answer:

> *"A `TreeSet<Integer>` of pending stops. Going up, the next stop is
> `stops.ceiling(currentFloor)`; going down, `stops.floor(currentFloor)`. Both are
> O(log n), and it keeps stops sorted and deduplicated for free."*

**Verified:** `at floor 5 going UP, stops {2,6,8} -> next = 6`

> *"A `PriorityQueue` is the tempting answer, but it only gives you the min — you
> can't ask 'smallest stop above me' without draining it. That's the reason to
> prefer TreeSet here."*

Naming the rejected alternative **and why** is the highest-value sentence in this answer.

### Follow-up #3 — "Add weight capacity; refuse boarding when full"

> *"A field on `Elevator` plus a guard in boarding. It doesn't touch dispatch — though
> a smart dispatcher would want to **skip full cars**, which means `DispatchStrategy`
> needs to see capacity. That's an argument for passing the whole `Elevator` to
> `pick()` rather than just its floor — which is what I did, so it already works."*

Showing an earlier decision paying off later is a strong move.

### Follow-up #4 — "Express elevators, only floors divisible by 5"

> *"Not a subclass — see Phase 3. I'd give `Elevator` a `FloorPredicate` (or a simple
> `Set<Integer> servableFloors`), and the dispatcher filters on it. One new field, no
> new hierarchy."*

### Follow-up #5 — "How would you test this?"

> *"The simulated clock is what makes this testable: `step()` is deterministic, so I
> assert exact positions per tick with no sleeps. And because `DispatchStrategy` is
> injected, I can pass a fake that always returns car 0 and test `Elevator` alone."*

---

## Done when (from the README)

`java ElevatorSystem` runs ≥15 ticks, 3 elevators, 10 floors, 5 requests, printing
each tick, every request eventually served.

Sample tick output shape:

```
tick 1: E0@1IDLE E1@5DOWN E2@9DOWN
tick 2: E0@1IDLE E1@4DOWN E2@8DOWN
tick 3: E0@1IDLE E1@3IDLE E2@7IDLE
```

---

## Self-check

- [ ] Scoped to a simulated clock, and said why (testability)
- [ ] Refused the `ExpressElevator` subclass with a stated reason
- [ ] Injected `DispatchStrategy`; swapping it edits nothing
- [ ] Justified `TreeSet` over `PriorityQueue`
- [ ] Reached Phase 6 with time left

Verified backing: `notes/oop_proofs/LldInterviewProofs.java` — class `Section2Elevator`.
