# LLD 01 — Parking Lot (FULLY WORKED — study this one)

> **`INTERVIEW.md`** in this folder is the same design spoken aloud as a
> 45-minute interview answer, following `notes/THE_SCRIPT.md`. Read the code
> first, then that.

This is the only problem here that is finished. Read it as a demonstration
of the 6 steps in 00_HOW_TO_DO_LLD.md, then do the exercises at the bottom.

    javac ParkingLot.java && java ParkingLot

## How it was derived

**Step 1 — scope.** Single lot, in-memory, no persistence, no payment
gateway, single-threaded. Fees by hour, vehicle-type dependent.

**Step 2 — nouns.** Vehicle, Spot, Ticket, ParkingLot, FeeStrategy.

**Step 3 — verbs.** park(vehicle) -> Ticket. unpark(ticket) -> fee.
findSpot(). calculateFee().

**Step 4 — what varies?** Two things:
  - vehicle TYPES (bike/car/truck) -> enum, since the set is fixed and known
  - fee RULES (hourly, flat, weekend) -> interface, since new ones appear later
That distinction is the judgment call worth internalizing. Fixed and
enumerable -> enum. Open-ended and behavioral -> interface.

**Step 5 — API first.**
    Ticket park(Vehicle v)
    double unpark(Ticket t, LocalDateTime exitTime)
    boolean hasSpace(VehicleType type)

**Step 6 — implement, then prove it in main().**

## Exercises (do these — this is where the learning is)

1. Add a `WeekendFee` strategy that halves the rate. You should NOT need to
   modify ParkingLot at all. If you do, the design failed open/closed.
2. Add multiple floors. Where does that logic belong?
3. Make `findSpot` prefer the floor nearest the entrance.
4. Add an `ElectricSpot` that charges the car and bills for kWh used.
5. What breaks if two threads park at once? Fix it with `synchronized`.
   Now: what is the smallest block you can synchronize and still be correct?
