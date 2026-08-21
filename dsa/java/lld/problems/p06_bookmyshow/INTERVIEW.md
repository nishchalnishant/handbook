# BookMyShow — THE SCRIPT, run end to end

> Spoiler. Attempt Phases 1–4 in `ATTEMPT.md` first.
>
> **Verified backing**: `javac BookMyShow.java && java BookMyShow` → **24 PASS, 0 FAIL**,
> including two multi-threaded contention tests. Every number below is from a real run.

This problem is rated Hard, and the rating is about exactly one thing. The class
diagram is easy — Movie, Show, Seat, Booking, and nobody gets that wrong. The
interview is won or lost on: **what happens when two people click the same seat
at the same millisecond?**

---

## Phase 1 — SCOPE (0:00–5:00)

1. **"When two users select the same seat simultaneously, who gets it?"**
   → The whole problem. Ask it first, out loud, so the interviewer knows you have
   seen it.
2. **"Is a seat hold time-limited?"** → Yes, 10 minutes. That single word (TTL)
   adds a *time dimension* to the state: a seat is not free/taken, it is
   free/taken-until-T. Most bugs live here.
3. **"Must a multi-seat booking be all-or-nothing?"**
   → *Planted.* Yes. A family of four given two seats is worse than a rejection.
   This forces rollback logic that you cannot bolt on later.
4. **"Is payment synchronous, and can it be slow?"**
   → *Planted.* If payment takes 30s, the hold can expire *during* payment, so
   `confirm()` must re-verify rather than trust the hold it was handed.
5. **"One JVM or many?"** → One, in-memory. I will say what changes for many in
   Phase 6, because that answer is different, not just bigger.

**Not building:** search/discovery, seat-map UI, pricing tiers, real payment
gateway, persistence, recommendations.

---

## Phase 2 — NOUNS (5:00–10:00)

*movie, show, theatre, screen, seat, row, user, booking, payment, hold, lock,
status, refund, cancellation policy.*

| Noun | Test | Verdict |
|---|---|---|
| Movie, Seat | pure values | `record` |
| Hold | value + expiry, replaced not mutated | `record Hold(userId, bookingId, expiresAt)` |
| Show | owns its seat list, has identity | `class` |
| Booking | state changes over time | `class` with a guarded transition |
| BookingStatus | fixed known list | `enum PENDING, CONFIRMED, CANCELLED, EXPIRED` |
| RefundPolicy | "per cancellation policy" = varies | `interface`, injected |

Cut: **theatre/screen/row** (real in production, but they add nothing to the
hard part — say "I'd add them, they're containment relationships, they don't
change the concurrency answer"). **Lock** is not a class; it is the *shape of the
map*. **Payment** is one mechanism today → Q4 → plain, not an interface yet.

**A noun the statement does not contain but the design needs: the clock.**
Time is an input, so inject it — `Supplier<Long>`, not
`System.currentTimeMillis()` buried in the logic. Otherwise testing a 10-minute
TTL means sleeping for 10 minutes, and you will simply not test it. In this
file every TTL test moves a counter instead. That is a design decision made for
testability, and saying so scores.

---

## Phase 3 — DECIDE (10:00–15:00)

### The wrong answer that looks right

```java
if (seat.isAvailable()) {      // thread A reads true. thread B reads true.
    seat.setHeldBy(user);      // both write. Two tickets, one seat.
}
```

This is **check-then-act**, and the things that do *not* fix it are worth naming:

- making the field `volatile` — visibility is not atomicity;
- using a `ConcurrentHashMap` to store seats — a thread-safe *container* does not
  make your two-step read-then-write a single step;
- `synchronized` on `Seat` — works, but now you hold a lock across a payment call
  if you are careless, and it does not survive a second JVM.

### The answer

Make claiming a seat **one atomic operation**. The seat's occupancy *is* a map
entry, and the claim *is* `putIfAbsent`:

```java
Hold existing = holds.putIfAbsent(seat, mine);
if (existing == null) return true;            // free -> I won it
if (existing.expiredAt(now)) return holds.replace(seat, existing, mine);  // CAS
return false;
```

There is no window between the check and the act, because **there is no check**.
Exactly one `putIfAbsent` can return null.

Note the second line carefully. Displacing an expired hold is *itself* a
check-then-act if you write `if (expired) holds.put(...)` — two threads both see
the same stale hold and both overwrite. `replace(key, expected, new)` is the
compare-and-swap that closes it. **This is the line most candidates get wrong
after getting the first one right.**

### TTL: lazy expiry, not a sweeper

Expiry is evaluated *at the moment of contention*. The consequence is worth
stating: the background sweeper becomes a **memory optimisation, never a
correctness requirement**. If it never runs, no seat is ever wrongly withheld —
the next claimant displaces the corpse. A design where correctness depends on a
timer thread having run is a design that breaks when the thread dies.

### Two maps, not one field

`holds` (temporary, expirable) and `sold` (permanent). Separating them means
"confirmed" cannot be accidentally aged out by TTL logic. Confirmation is
one-way.

---

## Phase 4 — API (15:00–20:00)

```java
Optional<Booking> holdSeats(String userId, List<Seat> seats);  // empty = lost the race
boolean           confirm(String bookingId);                   // false = hold lapsed
int               cancel(String bookingId);                    // refund, minor units
```

`Optional` rather than an exception: losing a race is a normal outcome under
load, not an error. `int` minor units for money — never `double`.

---

## Phase 5 — CODE (20:00–35:00)

Two subtleties in `holdSeats`, both easy to miss:

**Rollback must be identity-aware.**

```java
for (Seat r : got) holds.remove(r, mine);   // two-arg remove
```

One-arg `remove(seat)` would delete whatever hold is there *now* — including
another user's hold that legitimately landed on that seat microseconds ago. You
would fix your own failed booking by corrupting someone else's successful one.
Two-arg `remove(k, v)` only deletes if it is still yours.

**`confirm()` re-verifies every seat.** The hold you were handed may have expired
during the payment round trip. Re-check before taking money, and mark the booking
`EXPIRED` rather than silently failing.

---

## Phase 6 — EXTEND (35:00–45:00)

**1. "Prove the concurrency actually works."**

Two tests in the file, both with a `CountDownLatch` starting gun so the threads
genuinely collide rather than trickling:

- 200 threads, one seat → `holders = 1, confirmed = 1`
- 100 threads, the same three seats → `bookings = 1, seats held = 3`

**2. "How do you know those tests can fail?"** — the question you should ask
yourself. So I mutation-tested them: replaced `putIfAbsent` with the
check-then-act version and re-ran.

Result, and it is more interesting than a clean pass. The **3-seat test caught it
on 5 runs out of 5** (`bookings = 2, seats held = 2` — two users each believing
they had the row, and only two of three seats actually held). The **1-seat test
did not catch it on any run**: 200 threads hammering a single key almost never
interleave inside that two-instruction window, and `confirm()`'s re-verification
then masks the damage downstream.

Two lessons I would say out loud:
- **Wider transactions expose races that narrow ones hide.** Acquiring three keys
  in sequence opens a window orders of magnitude larger than acquiring one.
- **Assert at the layer that can break.** The original test only counted
  confirmations, and `confirm()` re-verifies ownership — so it corrected the bug
  before the assertion could see it. Counting *holders* tests `claim()` itself.
  That is why the file now asserts both.

A race test that has never been observed failing is not evidence of anything.

**3. "Now run it on 10 machines."** In-process atomics are gone; the map was
never the real source of truth. Options, in order of what I would actually reach
for:
- **Database as the arbiter.** `UPDATE seats SET held_by = ?, expires_at = ?
  WHERE seat_id = ? AND (held_by IS NULL OR expires_at < now())` and check the
  affected row count. This is `putIfAbsent` expressed in SQL — same shape, one
  atomic statement, the DB does the arbitration.
- **A version column CAS**, if the row carries other mutable state.
- **Redis `SET key value NX PX 600000`** — literally putIfAbsent with a TTL, and
  the TTL is enforced by the store rather than by your comparison. Fast, but now
  Redis is a correctness dependency, so you need a fencing token to survive a
  failover.
- **Never** `SELECT` then `UPDATE` in two statements without `FOR UPDATE`. That is
  the same check-then-act bug with a network round trip in the middle, which
  makes the window *larger*, not smaller.

Also: payments must be **idempotent** (a retry after a timeout must not
double-charge), keyed by booking id.

**4. "Booking a whole row of 10 — deadlock?"** Two users grabbing overlapping
seat sets in opposite orders could livelock on retry. Fix: **acquire in a global
total order** (sort seats by label before claiming). Cheap, and it makes
deadlock structurally impossible rather than unlikely.

**5. "Waitlist when a show sells out."** Observer: `Show` keeps listeners; cancel
fires them. Note this changes `cancel()` from a private operation into an event
source, which is exactly the "adding a class, not editing a switch" test.

**6. "Dynamic pricing."** `interface PricingStrategy` injected into `Show` —
same shape as `RefundPolicy`, which is already there. The fact that the second
strategy costs nothing structurally is the evidence the first one was placed
correctly.

---

## Self-check

- Did you use a single atomic op to claim, or a check followed by an act?
- Did you notice that *displacing an expired hold* is a second, separate race?
- Is your rollback identity-aware (`remove(k, v)`), or does it clobber?
- Does `confirm()` re-verify, or does it trust a hold that may be minutes stale?
- Did you inject the clock, or is your TTL untestable without sleeping?
- Have you ever seen your concurrency test fail? If not, you have no evidence it works.
