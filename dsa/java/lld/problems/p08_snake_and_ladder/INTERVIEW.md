# p08 Snake and Ladder — THE SCRIPT, run end to end

Procedure: `../../../notes/THE_SCRIPT.md`. Decision tree: `../../../notes/TEXT_TO_CODE.md`.

Every claim below is checkable against `SnakeAndLadder.java` in this folder.
Every number quoted comes from actually running it (42 PASS).

> **Read this only after you have attempted `ATTEMPT.md`.** This problem is
> labelled **Easy**, and that is a trap, not a gift. The interviewer already knows
> you can move a token around an array. Everyone produces working code here, so
> working code is the *floor*, not the score. The signal lives in exactly two
> places: whether you made the game **testable** (Phase 3), and whether you heard
> the word "invalid" in the spec as **an invariant with a home** (Phase 4).

---

## PHASE 1 — SCOPE (0:00–5:00)

> "Two to four players on a configurable board. Each turn a player rolls a dice
> and advances; landing on a snake head drops them to its tail, landing on a
> ladder base lifts them to its top. First to land exactly on the final cell wins.
>
> Scoping out: single process, in-memory, no UI, no network, no persistence, no
> save/resume. All additive.
>
> The two things actually worth designing are the **dice seam** — because a game
> driven by real randomness is a game you cannot write a single deterministic
> assertion about — and **board validation**, because the spec already hands me
> one illegal configuration and there are four more it doesn't mention."

**The five questions** (two planted):

| Ask | What you're really fishing for |
|---|---|
| "Exact roll to finish, or does overshooting bounce back?" | two legitimate variants; picking silently is the error |
| "Can a jump land you on another jump — do chains resolve?" | **planted**: this is where a board can *cycle forever* |
| "Can two players occupy the same cell, or is there a capture rule?" | scopes out a whole feature in one sentence |
| "Is the dice always six-sided?" | **planted**: sets up injecting the dice rather than hardcoding it |
| "Is the board always 100 cells with a fixed layout?" | forces `Board` to be a parameter, not a constant |

The chain question is the strongest one available. Most candidates never ask it,
then write a `while` loop that resolves jumps repeatedly — and a board with
`10→20` and `20→10` hangs the game. Asking it up front converts a runtime hang
into a constructor that throws.

---

## PHASE 2 — NOUNS (5:00–10:00)

> "Pulling the entities out of the statement."

```
Board   Cell   Player   Dice   Snake   Ladder   Position   Game   Turn   Winner
```

**Merge and cut, out loud — with a reason for each:**

- ***`Snake` and `Ladder` collapse into one type.*** This is the single most
  important cut in the problem. Both mean "landing on cell A teleports you to
  cell B". They differ only in whether B is below or above A — which is
  *derivable*, not something to store. Two classes here means every rule gets
  written twice and the two copies drift.
- *`Cell` earns nothing.* A cell is an integer. There is no per-cell state beyond
  "is there a jump starting here", which is a map lookup.
- *`Position` is a field, not a class.* It is one `int` per player.
- *`Turn` and `Winner` are outcomes, not entities.* They come out of `Game`.
- *`Player` is a `String` here.* With no scores, no history, and no profile, a
  class would hold exactly one field. **Rule of three / YAGNI.** I'd say out loud
  where it comes back: the moment players get stats, `Map<String,Integer>`
  becomes `Map<Player,...>` and nothing else changes.

Leaves four: **Jump, Board, Dice, Game.**

---

## PHASE 3 — DECIDE (10:00–15:00)

Each noun through **`TEXT_TO_CODE.md`**'s tree.

| Noun | Question that decided it | Answer |
|---|---|---|
| `Jump` | value, no behaviour, never mutates | **`record Jump(int from, int to)`** |
| `JumpKind` | Q1 — variants differ only by data, fixed list | **`enum { SNAKE, LADDER }`** |
| `Board` | has identity, but frozen after construction | **final class**, immutable |
| Dice | Q3 — "different **ways to** produce a number" | **`IntSupplier`** (see below) |
| `GameListener` | "X notifies Y when…" | **interface**, observer |
| `Game` | state that changes over time | **class** |

### The `Snake`/`Ladder` decision, stated properly

The tempting shape is `interface Jump` with `class Snake` and `class Ladder`.
Run it through the tree honestly:

- **Q1: do the variants differ only by data, from a fixed list?** Yes — the *only*
  difference is the sign of `to - from`. Q1 says stop: **enum**, or in this case
  not even that. The direction is a **derived property**, so `JumpKind` is
  computed in one line and never stored:

```java
JumpKind kind() { return to < from ? JumpKind.SNAKE : JumpKind.LADDER; }
```

Storing both a `kind` field *and* the endpoints creates a state that can lie —
a `Jump(17, 7)` tagged `LADDER`. Deriving it makes that unrepresentable. **The
best fix for an inconsistent-state bug is a design where the state doesn't exist.**

### Why the dice is `IntSupplier` and not `interface Dice`

The dice is the textbook Strategy: swap the algorithm at runtime. But the JDK
already has the exact interface — "takes nothing, returns an int" is `IntSupplier`.
Declaring `interface Dice { int roll(); }` adds a name and zero information, and
it costs you every lambda and method reference the JDK already knows how to make.

> "I'd inject it as an `IntSupplier`. It's a Strategy, but naming it `Dice` buys
> nothing the JDK doesn't already give me. What I care about is the *seam* — that
> the game never calls `Math.random()` itself."

That seam is the whole reason the test file can assert `amy ends on 22` instead of
`amy ends somewhere`. The two factories make the intent explicit:

```java
static IntSupplier fair(int faces, long seed)   // seeded -> reproducible
static IntSupplier scripted(int... rolls)       // forced  -> assertable
```

Note `fair` takes a **seed**, not a bare `Random`. An unseeded random game is
untestable *and* un-reproducible when it fails in CI.

---

## PHASE 4 — API (15:00–20:00)

Signatures before bodies. The question to ask of each: *could someone use this
without reading the implementation?*

```java
record Jump(int from, int to) { JumpKind kind(); }

final class Board {
    Board(int size, List<Jump> jumps);   // throws on every illegal configuration
    int  size();
    Jump jumpAt(int cell);               // null == plain ground
}

final class Game {
    Game(Board b, IntSupplier dice, List<String> players);
    int    playTurn();                   // returns the cell landed on
    String playToCompletion(int maxTurns);
    Status status(); String winner(); int positionOf(String p); String currentPlayer();
    void   addListener(GameListener l);
}
```

### Where the invariants live — the part that scores

The spec says one configuration is invalid. Reading it as *one* check is the
mistake. **"Invalid config is rejected at setup" is a trigger phrase**
(`TEXT_TO_CODE.md`: *"at most / at least / must be" → an invariant → validate in
the constructor, throw*). Enumerating the family gets you four more:

| # | Invariant | Why it exists | Test |
|---|---|---|---|
| 1 | endpoints are on the board | `Jump(50,120)` on a 100-board is nonsense | `off-board destination is rejected` |
| 2 | cell 1 and the final cell never *start* a jump | a jump off the winning cell makes winning unobservable | `a jump off the winning cell is rejected` |
| 3 | one jump per source cell | **this is the spec's rule** — and it also catches two snakes sharing a head | `snake head == ladder base…is rejected` |
| 4 | no chains | `20→50` and `50→80` means "move then jump" is no longer one step, and a cycle hangs the game | `a chained jump is rejected at setup` |
| 5 | a jump never targets its own cell | `Jump(42,42)` is a silent no-op | `a jump to its own cell is rejected` |

Invariant 3 is worth saying out loud, because the spec phrases it narrowly
("snake head == ladder base") and the general rule is *one jump per source*. Two
snakes sharing a head is the identical defect. Implementing the narrow phrasing
literally — comparing a snake list against a ladder list — is what having two
classes would have pushed you into. **Merging `Snake` and `Ladder` in Phase 2 is
what made this check one line:**

```java
if (m.putIfAbsent(j.from(), j) != null)
    throw new IllegalArgumentException("cell " + j.from() + " already starts a jump");
```

Invariant 4 is the one to be *honest* about rather than clever. Chains could be
resolved with a loop — but then a board can cycle, and detecting that costs a
visited-set at runtime, on every turn, forever. Rejecting chains once at setup is
strictly cheaper and it is the truthful answer: **a chaining board is a different
game, and I'd rather refuse to model it than model it wrongly.**

---

## PHASE 5 — CODE (20:00–35:00)

### The ordering inside `playTurn`, which is the actual problem

```
roll → overshoot check → move → apply jump → win check → advance turn
```

Two orderings here are wrong, and both are common:

**Wrong 1 — win check before the jump.** A player lands exactly on the final cell,
you declare a win, and *then* a snake sitting there drags them back. Invariant 2
forbids a jump on the final cell, so this can't bite in this codebase — but the
ordering must still be right for the mirror case, which *is* reachable: a **ladder
whose top is the final cell wins immediately**. That is asserted:

```
PASS  a ladder that ends on the final cell wins immediately (jump applied BEFORE the win check)
```

**Wrong 2 — an overshoot that doesn't cost the turn.** Forfeiting the *move* and
forfeiting the *turn* are different things, and it is easy to `return` early and
silently skip `advanceTurn()`, letting one player roll forever. Asserted directly:

```
PASS  an overshooting roll forfeits the move; amy stays on 7
PASS  an overshoot does not end the game
PASS  an overshoot still costs the turn
```

### The randomised check, and what it is *allowed* to claim

Scripted dice prove the rules. They cannot prove the game **terminates** — that
needs volume. 1000 seeded games, three players, real 100-cell board:

```
decided 1000/1000, mean 86.7 turns, longest 246 turns, wins {amy=352, bob=349, cal=299}
```

Here is the discipline worth copying. The obvious assertion to write is *"the
first player wins most often"* — and it would have **passed**: 352 > 349. It is
still the wrong assertion. A 3-game gap over 1000 trials is inside the noise; it
passes by luck and flips on a different seed. So the code asserts only what the
data supports, and says why in a comment:

```java
// NOT asserted: "the first seat wins more often". Over 1000 games the split
// came out 352/349/299 -- the gap between seats 1 and 2 is 3 games, which is
// inside the noise for n=1000, so an assertion on it would pass by luck and
// fail on a different seed. The only honest claim is that no seat is starved.
```

**A test that passes for the wrong reason is worse than no test**, because it
manufactures confidence. Declining to assert something you can't support is a
senior move, and saying it out loud is free signal.

---

## PHASE 6 — EXTEND (35:00–45:00)

The six follow-ups that always come.

**1. "Add a rule: rolling a 6 gives another turn."**
One line in `playTurn` — skip `advanceTurn()` when `roll == faces`. But note the
smell: `Game` doesn't know how many faces the dice has, because it only holds an
`IntSupplier`. That's the *cost* of the minimal seam, and the honest answer is
that this rule is the trigger to promote `IntSupplier` to a real `Dice` interface
exposing `faces()`. **Rule of three: the abstraction arrives when the second
requirement asks for it, not before.**

**2. "Two players landing on the same cell — the later one sends the first back to start."**
This is a rule about the *interaction* of positions, and `Game` already owns every
position, so it belongs in `Game` right after the jump is applied. Nothing else
moves. That's the extension test passing: one new block, zero edits elsewhere.

**3. "Make it multiplayer over a network — is this thread-safe?"**
No, and deliberately so. `Game` is single-threaded by construction: one `turnIndex`,
mutated on every turn. The three-layer answer:
   - *In-process:* the correct fix is **not** locking every field — it's making
     `playTurn` the synchronized unit, because a turn is the atomic operation. Any
     finer granularity is a **check-then-act** hazard: two threads both read
     `currentPlayer()`, both see `amy`, both move her.
   - *Time dimension:* a real game needs a per-turn timeout, which means an
     injected clock, exactly as p04/p06 do.
   - *Multi-machine:* the game state is a row; a turn is a conditional
     `UPDATE … WHERE turn_index = ?` checking the affected-row count, or a version
     column CAS. The losing node retries and observes it is no longer their turn.

**4. "Undo the last move."**
Needs a move log — the deferred `Move` noun from Phase 2 comes back. Command
pattern: each turn records `(player, from, to, jumpTaken)`, and undo restores
`from` and rewinds `turnIndex`. Worth flagging that undo is *not* free with a
random dice: undoing must also rewind the dice, which a bare `IntSupplier` can't
do. That's the second pressure toward a real `Dice` type.

**5. "A 10,000-cell board with 2,000 jumps — does anything degrade?"**
No. `jumpAt` is a `HashMap` lookup, O(1), independent of board size; construction
is O(J). The board is `Map.copyOf`'d, so it is immutable and safely shareable
across concurrent games — which is why the 1000-game loop constructs `Board` once
outside the loop and only `Game` inside it.

**6. "How do you know the rules are right?"**
Mutation testing — deliberately break the code and confirm the suite notices.
**A test suite you have never seen fail is a test suite you have no evidence works.**

| Mutation | Result |
|---|---|
| allow a duplicate jump source | **CAUGHT** (3 assertions) |
| remove the chain check | **CAUGHT** (1) |
| stop validating off-board endpoints | **CAUGHT** (1) |
| allow a jump off cell 1 / the final cell | **CAUGHT** (2) |
| skip `advanceTurn()` on overshoot | **CAUGHT** (1) |
| never apply a jump | **CAUGHT** (10) |
| invert SNAKE/LADDER classification | **CAUGHT** (2) |
| win on `target >= size` instead of `== size` | **SURVIVED** |

### The survivor, and why the right answer was to stop

Seven of eight died. The survivor looks like a coverage hole, so I tried to close
it — added a boundary test putting a player one cell short of the finish. **It
still survived.** Rather than keep bolting on tests, I read the control flow:

```java
if (target > board.size()) { ...forfeit...; return from; }   // guard
...
if (target == board.size()) { ...win... }                    // mutated line
```

Past the guard, `target <= size` always holds, and a jump destination is
constructor-validated to be on the board. So `>=` and `==` are **provably
identical here** — an *equivalent mutant*. No test can kill it, and writing more
tests chasing it would have been motion, not progress.

The lesson is the one worth saying in an interview: **a surviving mutant is a
question, not a verdict.** It means either "you are missing a test" or "these two
programs are the same program". Distinguishing the two requires reading the code,
and reporting an unkillable mutant honestly is better than quietly deleting it
from the table.

---

## The one-paragraph version

> "Snake and ladder are the same concept — a jump from one cell to another — so
> they're one record, with the direction *derived* rather than stored, which makes
> a mislabelled snake unrepresentable. The dice is injected as an `IntSupplier` so
> every test is deterministic. The spec mentions one invalid configuration; there
> are five, and they all live in the `Board` constructor, so no other method has
> to ask whether the board makes sense — the interesting one is rejecting chained
> jumps, because resolving them lets a board cycle forever. Inside a turn the
> order is roll, overshoot check, move, jump, win, advance: the jump has to be
> applied before the win check or a ladder onto the final cell doesn't win."
