# LLD Interview — 60 Minute Playbook

## Timeline

| Time | Phase | What you produce | Say out loud |
|---|---|---|---|
| **0–06** | Scope & clarify | 4–6 bullet requirement list | "Let me lock scope before I design." |
| **06–12** | Entities & actors | Noun list → candidate classes | "Here are the core objects and who acts on them." |
| **12–18** | API / public surface | Method signatures on the main service | "This is the contract clients code against." |
| **18–24** | Class model | Classes, fields, relationships, enums | "Composition here, not inheritance, because…" |
| **24–44** | **Code it** | Working Java for the core flow | Narrate while typing. Never type silently. |
| **44–50** | Concurrency & extension | Locking strategy + one extension demo | "If we add X tomorrow, only this class changes." |
| **50–55** | Edge cases & tests | 4–5 named cases, one written | "Here's what breaks and how I'd test it." |
| **55–60** | Q&A | Trade-offs you'd revisit | — |

**Hard rule:** be typing real code by minute 25. Design-only for 40 minutes reads as a fail.

---

## Stage 1 — Scope (0–06)
Ask exactly these, then stop:
1. **Who are the actors?** (user, admin, system/cron)
2. **In or out?** Payments, auth, persistence, distributed, UI — kill 3 of them explicitly.
3. **Scale?** Single-process in-memory, or multi-threaded? (This decides your whole concurrency answer.)
4. **What's the one flow you most want to see?** — this makes the interviewer hand you the rubric.

Write requirements as numbered lines in the editor. They become your checklist at minute 50.

## Stage 2 — Entities (06–12)
Underline nouns from the requirements → those are classes. Verbs → methods.
State for each: **entity** (has ID + lifecycle), **value object** (immutable, no ID), or **service** (stateless behavior).
Draw relationships in comments: `Order --* OrderItem`, `Vehicle <|-- Car`.

## Stage 3 — API (12–18)
Write the facade first — the 5–8 methods that answer the requirements:
```java
public interface ParkingLot {
    Ticket park(Vehicle v) throws NoSpotAvailableException;
    Receipt unpark(String ticketId);
    Availability availability(VehicleType t);
}
```
Return **result objects, not primitives**. Throw **domain exceptions, not `null`**.

## Stage 4 — Class model (18–24)
Say the design principle out loud as you place each class:
- **SRP** — one reason to change per class
- **Open/Closed** — new type = new class, not a new `if`
- **DIP** — depend on the interface, inject the impl

Any `switch` on a type enum is a smell → name the pattern that removes it.

## Stage 5 — Code (24–44)
Order: **enums → value objects → entities → interfaces → service → main flow.**
- Constructor-inject every dependency (`private final X x;`)
- Real bodies for the core path; `// TODO` bodies for peripheral setters
- Skip getters/setters unless asked — say "assuming standard accessors"
- Compile it in your head every 5 minutes

## Stage 6 — Concurrency (44–50)
Pick one and defend it:
- `ConcurrentHashMap` + `computeIfAbsent` for the registry
- `synchronized` on the smallest critical section (allocation, not the whole method)
- `ReentrantLock` per-resource when you need granularity or `tryLock`
- `AtomicInteger` for counters

Name the race you're preventing: *"two threads seeing the same free spot."*

## Stage 7 — Edge cases (50–55)
Duplicate request · empty/full capacity · concurrent same-resource · invalid state transition · null/expired ID · clock skew.
Write one JUnit test for the nastiest one.

---

## Pattern trigger map

| Signal in the prompt | Pattern |
|---|---|
| "different rules for pricing / matching / routing" | **Strategy** |
| "support multiple types of X" | **Factory / Abstract Factory** |
| "notify when something changes" | **Observer** |
| "one shared instance" | **Singleton** (say: enum or DI-managed) |
| "many optional fields" | **Builder** |
| "add behavior at runtime" | **Decorator** |
| "state transitions / lifecycle" | **State** |
| "undo, replay, queue of requests" | **Command** |

Use **at most two**. Say *why*, never just the name.

---

## Scoring signals

| Green | Red |
|---|---|
| Clarified before coding | Coded before clarifying |
| Compiling, runnable code | Pseudocode or boxes-only |
| Interfaces + injection | `new` scattered everywhere |
| Named a race condition | "It's single-threaded, so…" when it isn't |
| "Trade-off is X vs Y" | Pattern-name-dropping with no rationale |
| Drove the clock yourself | Waited to be prompted |

## Recovery lines
- Stuck: *"Let me code the happy path first and revisit this."*
- Wrong turn: *"That's coupling these two — let me pull it behind an interface."*
- Out of time: *"Core flow is complete. The remaining pieces are A and B — A would be a new Strategy impl, B goes in the repository layer."*
