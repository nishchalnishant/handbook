# THE SCRIPT — the same 45 minutes, every question

You asked for one pattern you can run on **any** LLD question so the answer is
predictable and consistent. This is it. Nothing here is question-specific.

Read order: **this file** → `TEXT_TO_CODE.md` (step 3 in detail) → `WORKED_EXAMPLES.md`
(three questions run through it).

---

## The clock

```
 0:00 ─ 5:00   PHASE 1  SCOPE      talk, don't write
 5:00 ─10:00   PHASE 2  NOUNS      the entity list
10:00 ─15:00   PHASE 3  DECIDE     record / enum / class / abstract / interface
15:00 ─20:00   PHASE 4  API        signatures only, NO bodies
20:00 ─35:00   PHASE 5  CODE       fill the 2-3 bodies that matter
35:00 ─45:00   PHASE 6  EXTEND     they attack it; you absorb it
```

**Write the six phase names in the corner of the whiteboard at 0:00.** It costs ten
seconds, it tells the interviewer you have a method, and it stops you freezing —
whenever you're lost, you look at the corner and see which phase you're in.

The most common failure is not a bad design. It is spending 25 minutes on Phase 5,
never reaching Phase 6, and running out of time with three half-written classes.

---

## PHASE 1 — SCOPE (0:00–5:00) · talk, don't write

Three sentences, in this order. Memorise the shape, swap the nouns.

> **1. Restate.** "So we're building X. Users do A, and the system does B."
> **2. Cut.** "I'm going to scope this to single-machine and in-memory — no
>    persistence, no auth, no network. I'll call out where those would slot in."
> **3. Aim.** "The interesting part here is ⟨the one hard thing⟩, so I'll spend
>    most of my time there. Does that match what you want to see?"

Then **exactly three questions**. Not seven — three. Pick from:

| Ask | Why it earns points |
|---|---|
| "How many ⟨users / requests / items⟩ roughly?" | shows you know scale changes design |
| "Is this single-machine or distributed?" | pre-empts the hardest follow-up |
| "Does ⟨entity⟩ have different types?" | this is you fishing for the interface |
| "Can two people do ⟨action⟩ at the same time?" | fishing for the concurrency follow-up |
| "Do we need history / undo / audit?" | fishing for Command or an event log |

The last three are **planted questions**. You are not asking to learn — you are asking
so that *they* tell you where the interface goes, and so the follow-up you've already
prepared arrives on your terms.

**Never skip this phase to look fast.** Starting to code at 0:30 reads as panic.

---

## PHASE 2 — NOUNS (5:00–10:00) · the entity list

Say: *"Let me pull out the entities."* Then write a bare column on the board:

```
Movie   Seat   Show   Booking   Payment   User
```

No boxes, no arrows, no fields yet. **Do not draw a class diagram.** It eats ten
minutes and you'll redraw it twice.

Two filters, out loud:

- **Merge:** "Screen and Auditorium are the same thing — I'll keep Screen."
- **Defer:** "User and Admin I'll leave out; they don't affect the core flow."

Cutting a noun scores as highly as adding one. It's YAGNI in real time.

---

## PHASE 3 — DECIDE (10:00–15:00) · the tree

Run every noun through **THE BIG DECISION** from `TEXT_TO_CODE.md`:

```
Q1. Variants differ ONLY by data, fixed list?   -> enum
Q2. Variants share MUTABLE STATE?               -> abstract class
Q3. A capability unrelated classes could have?  -> interface
Q4. Only one variant, none in sight?            -> plain class (YAGNI)
    otherwise                                   -> interface
```

Annotate the column as you go — this is the whole diagram you need:

```
Movie     record
Seat      record
SeatType  enum      (REGULAR, PREMIUM — differ by price only)
Show      class     (owns the seat map, mutable)
Booking   class     (status changes)
Payment   interface (card / UPI / wallet — "different ways to")
```

**Say the reason out loud for each one.** "SeatType is an enum because the variants
differ only by price." That single sentence is what's being graded. A candidate who
writes the same six lines silently scores far lower.

> Expect roughly: **2–4 records, 1–3 enums, 2–4 classes, 1–3 interfaces, 0–1 abstract
> classes.** If you have five interfaces you're overbuilding. If you have zero you've
> missed the variation the question was built around.

---

## PHASE 4 — API (15:00–20:00) · signatures only

Say: *"Let me write the API before any bodies, so we can agree on the shape."*

```java
class Show {
    private final List<Seat> seats;
    private final Map<String,String> seatToBooking;
    synchronized boolean hold(String seatId, String bookingId);
    void release(String seatId);
    List<Seat> availableSeats();
}
```

Bodies stay empty. Two checks, applied out loud:

- **Ownership:** *"`hold` lives on `Show` because `Show` owns the seat map."*
  If a method doesn't touch its own class's fields, it's on the wrong class.
- **Usability:** *"Could someone use this without reading the implementation?"*

**This is the natural checkpoint.** Say: *"Does this shape look right before I
implement?"* If your design is going sideways, this is where they'll redirect you —
five minutes in, not thirty.

---

## PHASE 5 — CODE (20:00–35:00) · only what matters

You cannot implement everything. Say so, and choose:

> *"I'll implement the core flow — ⟨the hard method⟩ — and stub the rest."*

Implement **two or three methods**: the one with the real logic, plus whatever it needs.
For everything else write the signature and `// straightforward` and move on.

Order: the interface and its implementations first (that's the design), then the class
that uses them. Write `main()` if there's time — running code beats a diagram.

Say **"I'm stubbing this"** every time you stub. Silence looks like you forgot.

---

## PHASE 6 — EXTEND (35:00–45:00) · the part that decides the outcome

They will now attack the design. **This is not you failing — this is the actual exam.**
Every follow-up is one of six kinds. Learn the six and you are never surprised.

### The six follow-ups

| # | They say | They're testing | Your move |
|---|---|---|---|
| 1 | "Now add ⟨new variant⟩." | **OCP** | add one class implementing the existing interface. Edit nothing. |
| 2 | "Two users do this simultaneously." | **concurrency** | the three-layer answer (below) |
| 3 | "What if this grows 100×?" | **scale** | name the bottleneck, then the data structure |
| 4 | "Can we undo it?" | **Command** | each action becomes an object with `execute()`/`undo()` |
| 5 | "How would you test this?" | **DIP** | "I injected the interface, so I pass a fake" |
| 6 | "Why not ⟨other design⟩?" | **judgement** | give the trade-off, then commit |

### #1 — the extension test (verified)

This is the single most common follow-up, and it has a scripted answer:

> *"That's one new class implementing `FeeStrategy`, and zero edits to existing code —
> that's why the interface is there."*

```
FlatFee     3h -> 50.0
HourlyFee   3h -> 60.0
WeekendFee  3h -> 190.0      <-- the new requirement
lines edited to add WeekendFee: 0
classes added: 1
```

If your answer to #1 requires editing a `switch`, your Phase 3 was wrong. That's the
feedback loop: **a hard follow-up means a missed interface.**

### #2 — the three-layer concurrency answer

Never stop at "I'd add `synchronized`." Always give all three layers:

1. **In-process:** `synchronized`, or better `ConcurrentHashMap.putIfAbsent` — atomic
   without locking the whole object.
2. **Time:** held resources need a timeout, or an abandoned request locks them forever.
3. **Multi-machine:** a JVM lock means nothing across servers — you need the database
   to arbitrate: a unique constraint, `SELECT … FOR UPDATE`, or a version column.

Layer 3 is what separates a strong answer. Most candidates never reach it.

### #6 — how to disagree

> *"I chose an interface over an abstract class because the pieces share no state.
> If they later need shared mutable state, abstract class becomes correct — but that's
> not in the requirements today."*

Trade-off, then commit. Never "you're right" if you don't think so, and never dig in
without a reason.

---

## The five sentences

If you remember nothing else, these five carry an entire interview:

1. *"Let me scope this first — single machine, in-memory, no persistence."*
2. *"⟨X⟩ is an enum because the variants differ only by data."*
3. *"⟨Y⟩ is an interface because the problem says there are different ways to do it."*
4. *"This method lives here because this class owns the data it needs."*
5. *"Adding that is one new class and zero edits to existing code."*

---

## The self-check

After any practice attempt, score yourself. Six is a pass.

- [ ] Scoped out loud before writing anything
- [ ] Asked exactly three questions, one of them planted
- [ ] Said the *reason* for every record / enum / interface choice
- [ ] Wrote signatures before bodies, and paused for agreement
- [ ] Stated what I was stubbing instead of going quiet
- [ ] Reached Phase 6 with time left
- [ ] Answered a "now add X" with one class and zero edits
- [ ] Gave all three layers on concurrency

**Anything you miss goes in `notes/error_log.md` — that file is empty and shouldn't be.**

---

## How to practise this

Reading this file again does nothing. The script only works once it's automatic.

**Round 1 — Phases 1–4 only, 20 minutes, out loud, on `lld/02_elevator`.**
Stop at the API. No bodies. The first four phases are 80% of the grade and the
cheapest to drill — you can do them four times in the time one full attempt takes.

**Round 2 — same problem, full 45 minutes, including a follow-up you invent yourself.**

**Round 3 — a fresh problem cold** (`03_rate_limiter`), self-check afterwards.

Paste your Phase 3 column and Phase 4 signatures and I'll grade them against the
checklist before you write a single body.

---

## The script, run five times

Proof that it isn't a shape that only fits one problem. Each of these is the same
six phases, same clock, on a different question:

| Walkthrough | The move worth stealing from it |
|---|---|
| `lld/01_parking_lot/INTERVIEW.md` | enum vs interface — when "different types of" is *not* a hierarchy |
| `lld/02_elevator/INTERVIEW.md` | refusing a subclass, with a reason; `TreeSet` for next-stop-in-direction |
| `lld/03_rate_limiter/INTERVIEW.md` | injecting a clock so tests need no `Thread.sleep` |
| `lld/04_cache/INTERVIEW.md` | why the linked list must be **doubly** linked |
| `lld/05_splitwise/INTERVIEW.md` | proving a net balance can't answer "whom do I owe" |

Every number quoted in those five files is printed by
`notes/oop_proofs/LldInterviewProofs.java`:

    javac notes/oop_proofs/LldInterviewProofs.java -d /tmp/proofs
    java  -cp /tmp/proofs LldInterviewProofs

For `02`–`05` they are **spoilers**. Attempt Phases 1–4 first.
