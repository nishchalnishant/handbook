# LLD 02 — Elevator System (you build this)

> **Spoiler warning.** `INTERVIEW.md` in this folder is a full worked answer
> following `notes/THE_SCRIPT.md`. Do Phases 1–4 (scope, nouns, decisions, API
> signatures) yourself first — 20 minutes, no bodies — and only then open it to
> compare. Opening it first turns production practice back into reading.

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
`java ElevatorSystem` runs a simulation of at least 15 ticks with 3
elevators and 10 floors, servicing 5 requests, printing each tick, and
every request is eventually served.

## Stretch
- an elevator has a weight capacity; refuse boarding when full
- express elevators that only stop on floors divisible by 5
- what data structure gives you "next stop in the current direction" cheaply?
