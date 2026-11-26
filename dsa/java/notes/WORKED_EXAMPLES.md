# Three real interview questions, worked end to end

Companion to `notes/TEXT_TO_CODE.md`. That file gives the procedure; this one
**runs it three times** on questions actually asked at product companies.

Runnable proof: `notes/oop_proofs/WorkedExampleProofs.java`

Each walkthrough uses the same six moves:

```
1. clarify + scope      2. nouns -> candidates      3. decision tree on each noun
4. verbs -> owners      5. API, signatures only     6. the follow-up question
```

**Read these actively.** Cover the answer column, decide yourself, then compare.
The three are deliberately different: one is about **concurrency**, one is the rare
case where **inheritance is correct**, one is about **state**.

---
---

# Example 1 — BookMyShow (seat booking)

> *"Design a movie ticket booking system. Users browse shows and book seats."*

Asked at: Flipkart, Swiggy, PhonePe, Uber. The concurrency follow-up is guaranteed.

## Step 1 — clarify + scope (say this out loud)

> "Scoping: single city, in-memory, no payment gateway — `pay()` returns a boolean.
> One user books for one show at a time. I'll focus on seat selection and the
> double-booking problem, since that's the interesting part."

Then ask 2–3 real questions:
- Can a user hold seats before paying? *(→ yes, with a timeout — that's why HELD exists)*
- Are seats priced differently? *(→ yes, regular/premium)*
- Multiple theatres per movie? *(→ yes)*

## Step 2 — nouns

> "Design a **movie** ticket booking system. **Users** browse **shows** and book **seats**."
> Plus, from the clarifications: **theatre**, **screen**, **booking**, **payment**.

## Step 3 — run each through the decision tree

| Noun | Reasoning | Answer |
|---|---|---|
| Movie | title, duration — a value, never changes | `record Movie(String title, int mins)` |
| Seat | id + type. Immutable — the *seat* doesn't change, its booking does | `record Seat(String id, SeatType type)` |
| SeatType | fixed list, differs only by **price** → **Q1 = YES** | `enum SeatType { REGULAR(100), PREMIUM(250) }` |
| BookingStatus | fixed list of states | `enum BookingStatus { HELD, CONFIRMED, EXPIRED }` |
| Theatre / Screen | identity + mutable contents | `class` |
| Show | owns seat→booking map, **changes** | `class Show` |
| Booking | has status that **changes** | `class Booking` |
| Payment | "different ways to pay" → **Q3 = YES** | `interface PaymentMethod` |
| PricingRule | weekend/matinee pricing varies | `interface PricingStrategy` |

**Note what did NOT happen: no `abstract class`, no inheritance.** Q1 caught `SeatType`,
Q3 caught the two interfaces. This is the typical shape.

## Step 4 — verbs onto owners

| Verb | Data it needs | Owner |
|---|---|---|
| browse shows | list of shows | `Theatre` |
| hold seat | the seat→booking map | **`Show`** ← owns the map, so it owns the method |
| confirm booking | booking status | `Booking` |
| pay | amount | `PaymentMethod` |
| price a seat | seat type + show time | `PricingStrategy` |

`hold()` on `Show`, not on `Seat` — because `Show` owns the map. That's rule 3 from
TEXT_TO_CODE: *if a method doesn't use its own class's fields, it's on the wrong class.*

## Step 5 — the API

```java
record Movie(String title, int mins) {}
record Seat(String id, SeatType type) {}

enum SeatType { REGULAR(100), PREMIUM(250);
    private final double price;
    SeatType(double p){ price = p; }
    double price(){ return price; }
}
enum BookingStatus { HELD, CONFIRMED, EXPIRED }

interface PaymentMethod   { boolean pay(double amount); }
interface PricingStrategy { double price(Seat seat, Show show); }

class Show {
    private final Movie movie;
    private final List<Seat> seats;                        // aggregation
    private final Map<String,String> seatToBooking;        // composition
    synchronized boolean hold(String seatId, String bookingId);   // <-- see below
    synchronized void release(String seatId);
    List<Seat> availableSeats();
}

class Booking {
    private BookingStatus status;
    boolean confirm(PaymentMethod method);
}
```

## Step 6 — THE follow-up: "two users click the last seat at the same instant"

This is the question. Without `synchronized`:

```java
boolean hold(String seatId, String bookingId) {
    if (seatToBooking.containsKey(seatId)) return false;   // both threads pass here
    seatToBooking.put(seatId, bookingId);                  // both write
    return true;
}
```

Verified with 10 threads on 1 seat: **10 users got the same seat.** With `synchronized`:
**1 user.** (Section A of the proof file.)

Answer in three layers — say all three:

1. **In-process:** `synchronized` on the hold method, or `ConcurrentHashMap.putIfAbsent`,
   which is atomic and doesn't block the whole object:
   ```java
   return seatToBooking.putIfAbsent(seatId, bookingId) == null;
   ```
2. **Held seats need a timeout** — otherwise an abandoned checkout locks the seat forever.
   A scheduled sweep flips HELD → EXPIRED.
3. **Multi-server:** a lock in one JVM means nothing across machines. You need the database
   to arbitrate — a unique constraint on `(show_id, seat_id)`, or `SELECT ... FOR UPDATE`,
   or optimistic locking with a version column.

Layer 3 is what separates a strong answer. Most candidates stop at `synchronized`.

---
---

# Example 2 — Chess

> *"Design a chess game."*

Asked at: Amazon, Microsoft, Adobe. This is the **one** classic where the answer to Q2
is genuinely YES — worth knowing precisely because it's the exception.

## Step 1 — scope

> "Two-player, same machine, no clock, no AI, no castling/en-passant initially — I'll
> mention where they'd slot in. Focus on the board, pieces, and move validation."

## Step 2 — nouns

**board**, **piece**, **player**, **move**, **position**, **colour**, **game**.
Piece kinds: king, queen, rook, bishop, knight, pawn.

## Step 3 — the decision tree, and why Chess is different

| Noun | Reasoning | Answer |
|---|---|---|
| Position | row+col, a pure value | `record Pos(int row, int col)` |
| Colour | fixed pair | `enum Colour { WHITE, BLACK }` |
| Move | from+to, a value | `record Move(Pos from, Pos to)` |
| Board | owns the 8×8 grid, mutable | `class Board` |
| Player | identity + colour | `class Player` |
| Game | owns turn order, mutable | `class Game` |
| **Piece** | **see below** | **`abstract class`** |

Now run **Piece** through the tree carefully:

```
Q1. Do King/Rook/Bishop differ only by DATA?
    NO — each has a different movement RULE (behaviour).      -> Q2

Q2. Do they need to SHARE MUTABLE STATE?
    YES — every piece has a colour and a CURRENT POSITION,
    and position changes as the game runs.                    -> ABSTRACT CLASS
```

**Stop at Q2.** This is the case where an interface is impossible: `pos` is per-object
mutable state, and an interface field is silently `public static final`. If you tried
`interface Piece { Pos pos; }` the compiler rejects it outright.

```java
abstract class Piece {
    protected final Colour colour;      // shared state
    protected Pos pos;                  // shared MUTABLE state -> interface impossible
    protected Piece(Colour c, Pos p){ colour = c; pos = p; }
    void moveTo(Pos p){ this.pos = p; } // shared behaviour, written ONCE
    abstract boolean canMove(Pos to);   // the ONE thing that differs
}
class King   extends Piece { boolean canMove(Pos to){ /* one square any dir */ } }
class Rook   extends Piece { boolean canMove(Pos to){ /* same row or col   */ } }
class Bishop extends Piece { boolean canMove(Pos to){ /* equal row/col delta */ } }
```

Verified output — one call site, three rules (dynamic dispatch doing the work):

```
WHITE King   at (0,4) -> (0,5)? true      WHITE Rook at (0,0) -> (0,7)? true
WHITE Rook   at (0,0) -> (0,5)? true      BLACK Bishop at (7,2) -> (5,0)? true
BLACK Bishop at (7,2) -> (0,5)? false     WHITE King at (0,4) -> (0,7)? false
```

`moveTo()` is written once in the parent and inherited by all six pieces. **That
inheritance is buying you something** — which is exactly the justification test.

## Step 4 — verbs onto owners

`canMove` → `Piece` (needs its own position). `isPathClear` → `Board` (needs the grid —
a piece can't see other pieces). `makeMove` → `Game` (needs turn + board + history).

Splitting `canMove` (shape of the move) from `isPathClear` (obstruction) is a real
design insight. Say it — it shows you thought about who owns what.

## Step 5 — API

```java
record Pos(int row, int col) { boolean onBoard(); }
record Move(Pos from, Pos to) {}
enum Colour { WHITE, BLACK }

abstract class Piece {
    abstract boolean canMove(Pos to);
    void moveTo(Pos p);
    Colour colour();
}

class Board {
    private final Piece[][] grid = new Piece[8][8];
    Piece at(Pos p);
    boolean isPathClear(Move m);
    void apply(Move m);
}

class Game {
    private Colour turn = Colour.WHITE;
    boolean makeMove(Move m);          // validates turn, canMove, path, self-check
    boolean isCheck(Colour c);
    boolean isCheckmate(Colour c);
}
```

## Step 6 — follow-ups

- **"Add castling / en passant."** These aren't piece-local — they depend on game
  history. Add a `MoveValidator` interface (chain of responsibility), or keep a
  `List<Move>` in `Game` and check it there. Don't cram it into `Piece.canMove`.
- **"Undo a move."** → **Command pattern**. Each `Move` becomes an object with
  `execute()`/`undo()` storing the captured piece.
- **"Why not `interface Piece`?"** → the state answer above. This is the question
  the whole problem exists to ask.

---
---

# Example 3 — Vending Machine

> *"Design a vending machine."*

Asked at: Amazon, Uber, Atlassian. Tests whether you recognise a **state machine**.

## Step 1 — scope

> "Single machine, coins only, exact denominations, no card reader. It has an inventory,
> takes coins, dispenses a product and change."

## Step 2 — nouns

**machine**, **product**, **coin**, **inventory**, **change**, plus the implied
**state** (idle / has-money / dispensing).

## Step 3 — decision tree

| Noun | Reasoning | Answer |
|---|---|---|
| Product | code, name, price — a value | `record Product(String code, String name, int price)` |
| Coin | fixed denominations, differ by **value only** → Q1 YES | `enum Coin { FIVE(5), TEN(10) }` |
| Inventory | mutable counts | `class` (or a `Map` inside `Machine`) |
| Machine | mutable, owns everything | `class Machine` |
| **State** | **behaviour changes by state → Q3** | **`interface VendingState`** |

### The signal you must learn to hear

> *"If the user presses select **before** inserting money, nothing happens."*

Behaviour depends on **what has happened so far** → that's a state machine. The naive
version is a flag soup:

```java
if (hasMoney && !dispensing && selected != null) { ... }    // grows forever
```

The State pattern replaces every flag with a class:

```java
interface VendingState {
    VendingState insert(Machine m, Coin c);      // each returns the NEXT state
    VendingState select(Machine m, String code);
    VendingState dispense(Machine m);
}
class Idle       implements VendingState { ... }
class HasMoney   implements VendingState { ... }
class Dispensing implements VendingState { ... }
```

Each method **returns the next state** — the object drives its own transition. That's
the strategy/state difference from Part 5: strategy is chosen by the caller, state
advances itself.

## Step 4 — verbs onto owners

`insert`/`select`/`dispense` → `Machine`, which **delegates to the current state**:

```java
void insert(Coin c){ state = state.insert(this, c); }   // one line, no if-else, ever
```

Illegal transitions are refused by the state that receives them — not by a validation
block. Verified:

```
state=IDLE
  select A1        -> "insert money first"     (refused by Idle)
  insert 10        -> state=HAS_MONEY
  select A1        -> "need 5 more"            (refused by HasMoney)
  insert 10
  select A1        -> state=DISPENSING
  dispense         -> "dispensing chips, change 5"
state=IDLE  credit=0
```

## Step 5 — API

```java
enum Coin { FIVE(5), TEN(10); int value(); }
record Product(String code, String name, int price) {}

interface VendingState {
    VendingState insert(Machine m, Coin c);
    VendingState select(Machine m, String code);
    VendingState dispense(Machine m);
    String name();
}

class Machine {
    private VendingState state = new Idle();
    private int credit;
    private Product selected;
    private final Map<String,Product> stock;
    void insert(Coin c);
    void select(String code);
    void dispense();
}
```

## Step 6 — follow-ups

- **"Refund button."** → one new method on the interface, three small implementations.
  Adding a *state* (e.g. OUT_OF_ORDER) needs zero edits to existing states — that's OCP.
- **"Change with fewest coins."** → greedy over sorted denominations; mention it fails
  for arbitrary denomination sets, where you need DP. Knowing the limit scores.
- **"Thread safety?"** → a physical machine has one user, so it's moot. **Saying that
  is the right answer** — recognising when you *don't* need concurrency is a signal.

---
---

# The pattern across all three

| | BookMyShow | Chess | Vending Machine |
|---|---|---|---|
| records | Movie, Seat | Pos, Move | Product |
| enums | SeatType, BookingStatus | Colour | Coin |
| **abstract class** | none | **Piece** | none |
| interfaces | PaymentMethod, PricingStrategy | (MoveValidator) | VendingState |
| main pattern | strategy | template/dispatch | **state** |
| the follow-up | **concurrency** | why not interface | adding states |

Three observations worth internalising:

1. **Records and enums do most of the work.** Every design starts with 2–4 of them.
   Candidates who jump straight to class hierarchies overbuild.
2. **Abstract class appeared once in three designs.** It is the exception. When it does
   appear, it's always for the same reason: **shared mutable state** (Q2).
3. **Interfaces always came from the same phrase** — "different ways to X". Payment
   methods, pricing rules, states. If the spec doesn't say it varies, don't make it vary.

# Now do it yourself

Pick `lld/02_elevator/README.md`. Give yourself **10 minutes** and produce only
declarations — no method bodies:

- [ ] nouns underlined, each run through the tree
- [ ] every verb assigned to the class owning its data
- [ ] the varying thing identified as an interface (the README names it)
- [ ] one sentence on the follow-up you'd expect

Then paste the declarations and get them graded before writing a single body.
