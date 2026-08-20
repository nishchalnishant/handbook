# Java, by writing it

A practice repo, not a reading repo. Almost every file here is incomplete
on purpose. You finish them.

## Why the old contents were deleted

This folder used to hold side-by-side Python/Java examples with READMEs
explaining the differences. That format teaches recognition, not recall —
you read Java, it makes sense, and you still can't produce it from a blank
file. That gap is exactly the problem being solved here, so the finished
examples had to go. (One worked example survives, in lld/01_parking_lot,
because you need one model of what "done" looks like.)

## Start here, in this order

1. `reference/00_WHY_YOU_FEEL_LOST.md` — read once, properly. 15 minutes.
   Four mental models Python let you skip. This is the actual fix.
2. `drills/d01` through `d10` — one per session, in order.
3. `lld/00_HOW_TO_DO_LLD.md` — the 6-step procedure.
4. `lld/01_parking_lot` — the one fully worked example. Study it, then do
   its 5 exercises.
5. `lld/02`–`05` — specs only. You build them.

## Running anything

    cd drills/d01
    javac Hello.java && java Hello

No Maven, no Gradle, no IDE required. JDK 25 is already installed.
`.class` files are gitignored.

## The rules that make this work

- **Compile every 5 lines.** Not every 50. You want the error while you
  still remember what you intended.
- **Guess before you look it up.** Wrong guess + compiler correction beats
  reading the right answer. It costs 20 seconds and it actually sticks.
- **Type it out. Never paste.** The muscle memory IS the skill you lack.
- **Predict output before running.** Every wrong prediction is a bug you
  now won't ship.
- **Log every error that costs 5+ minutes** in `notes/error_log.md`, in
  your own words.

## A realistic schedule

Week 1: d01–d05, one per day, 45 minutes each.
Week 2: d06–d10. d10 will be hard and should be — that's the exam.
Week 3: the parking lot, studied and then all 5 exercises done.
Week 4+: one LLD problem per week, from the spec, from empty.

Then rewrite the earliest ones from scratch. Second attempts are where
design sense forms, and they take a quarter of the time.

## The one thing to internalize

You already know how to program. You know loops, data structures, objects,
and design — all of it, in Python. You are not learning to program again.
You are learning one language's spelling, plus one genuinely new idea:
that types are declared up front and checked before the program runs.

That's a smaller gap than it feels like from inside. The lost feeling is
about unfamiliar syntax and an unforgiving compiler, not about ability.
It goes away with volume, and only with volume — which is why this repo
is 40 files you have to fill in rather than 40 files you can read.
