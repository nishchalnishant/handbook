# LLD 03 — Rate Limiter

> **Spoiler warning — this folder now contains a worked solution.**
> `RateLimiterDemo.java` is a complete, compiling reference implementation and
> `INTERVIEW.md` is the same design spoken aloud as a 45-minute answer,
> following `notes/THE_SCRIPT.md`.
>
> **Write your own version first.** Do Phases 1–4 (scope, nouns, decisions, API
> signatures) yourself — 20 minutes, no bodies — then implement, and only then
> read either file. Opening them first turns production practice back into
> reading, which is the exact gap this repo exists to close.
>
>     javac RateLimiterDemo.java && java RateLimiterDemo

## Requirements
`boolean allow(String clientId)` — true if the request may proceed.

Implement `RateLimiter` as an interface with THREE implementations:
  - FixedWindow    — N requests per fixed clock window
  - SlidingWindowLog — keep timestamps, evict old ones
  - TokenBucket    — refill at a steady rate, burst up to capacity

## Why this problem is worth your time
It is the cleanest possible demonstration of the strategy pattern: three
algorithms, one interface, identical call site. It's also a real interview
favourite, and the token bucket forces you to reason about time.

Inject a `Clock` (or a `LongSupplier` for "now") instead of calling
System.currentTimeMillis() directly — otherwise you cannot test it without
real sleeps. Learning that trick is half the point of this exercise.

## Done when
A main() proves for each implementation: burst allowed up to the limit,
then blocked, then allowed again after time advances — using a FAKE clock,
with no Thread.sleep anywhere.

## Stretch
- per-client limits with different tiers (free vs paid)
- make it thread-safe; measure where the contention is
