# LLD 02 — Elevator System

> **Spoiler warning — this folder now contains a worked solution.**
> `ElevatorSystem.java` is a complete, compiling reference implementation and
> `INTERVIEW.md` is the same design spoken aloud as a 45-minute answer,
> following `notes/THE_SCRIPT.md`.
>
> **Write your own version first.** Do Phases 1–4 (scope, nouns, decisions, API
> signatures) yourself — 20 minutes, no bodies — then implement, and only then
> read either file. Opening them first turns production practice back into
> reading, which is the exact gap this repo exists to close.
>
>     javac ElevatorSystem.java && java ElevatorSystem

Work the 6 steps from 00_HOW_TO_DO_LLD.md. Write the step-1 scope and the
step-5 API signatures in a comment block at the top of your file BEFORE
implementing anything. That habit is what interviewers score.

## Requirements
- N elevators, M floors
- external request: floor + direction (UP/DOWN)
- internal request: passenger inside presses a destination floor
- each elevator has: current floor, direction (UP/DOWN/IDLE), pending stops
- a dispatcher assigns an external request to ONE elevator
- `step()` advances the simulation one tick; print the state each tick

## Where the design lives
The dispatch rule is the interesting part — and it will change. Make it
a `DispatchStrategy` interface. Implement two:
  - NearestElevator (pick the closest idle or same-direction car)
  - RoundRobin (dumb, but proves the strategy swaps cleanly)

If adding the second strategy makes you edit the Elevator class, stop and
reconsider — that's the open/closed principle telling you something.

## Done when
`java ElevatorSystem` runs a simulation with 3 elevators and 10 floors,
servicing 5 hall calls plus in-car requests, printing each tick, and every
request is eventually served.

> Note: an earlier version of this file demanded "at least 15 ticks". That was
> a mistake worth keeping visible — the three cars move *in parallel*, so the
> makespan is the slowest single car, and crossing a 10-floor building can
> never take more than 9 ticks. Assert **termination and full service**, not a
> tick count you picked before doing the arithmetic.

## Stretch
- an elevator has a weight capacity; refuse boarding when full
- express elevators that only stop on floors divisible by 5
- what data structure gives you "next stop in the current direction" cheaply?
