# Chess — THE SCRIPT, run end to end

> Spoiler. Attempt Phases 1–4 in `ATTEMPT.md` first.
>
> **Verified backing**: `javac Chess.java && java Chess` → **30 PASS, 0 FAIL**,
> including `perft(3) = 8902` against the published node counts. Every number
> below is from a real run.

Chess is where candidates over-engineer. The winning answer is *smaller* than
the one most people reach for, and it hinges on two decisions: one hierarchy
choice and one separation.

---

## Phase 1 — SCOPE (0:00–5:00)

1. **"Castling, en passant, promotion — in or out?"** → Ask first. These are
   three special cases that between them double the code. I scope them **out**
   and say so explicitly rather than quietly omitting them. (Phase 6 covers what
   each would cost.)
2. **"Do I need move notation (PGN/FEN) parsing?"** → No. It is string parsing,
   not design.
3. **"An AI opponent?"** → *Planted.* If yes, the board must be cheaply
   copyable and I need make/unmake rather than copy-on-every-move. That is a
   performance decision that must be made in minute 3, not minute 40.
4. **"Draw by repetition / 50-move rule?"** → Out. Both need move *history*,
   which is a different data structure (a position hash count).
5. **"Is this one game in memory, or a server with many?"** → One, in-memory.

---

## Phase 2 — NOUNS (5:00–10:00)

*board, square, piece, king, queen, rook, bishop, knight, pawn, player, colour,
move, turn, check, checkmate, stalemate, game.*

| Noun | Test | Verdict |
|---|---|---|
| Square | pure value, validates itself | `record Square(int row, int col)` |
| Colour | fixed list of two | `enum Colour { WHITE, BLACK }` |
| GameState | fixed list | `enum { IN_PROGRESS, WHITE_WINS, BLACK_WINS, STALEMATE }` |
| Piece + 6 kinds | see Phase 3 | `abstract class` + 6 subclasses |
| Board | owns the grid, mutates | `class` |
| Game | owns turn + state | `class Chess` |

Cut: **Player** — it holds a colour and nothing else; `Colour` already *is* the
player. **Move** — I use `(from, to)`; a `Move` record earns its place only when
you add undo, and I say that rather than pre-building it. **Check/checkmate** are
not nouns in the design, they are *computed predicates*.

---

## Phase 3 — DECIDE (10:00–15:00)

### Decision 1: the one place an abstract class genuinely wins

Every other problem in this repo lands on `interface`. This one does not, and
the reason is mechanical rather than aesthetic. Run the tree:

- **Q1: do the variants differ only by data?** No. A knight and a bishop differ
  by *behaviour*, not by a number. (Contrast the parking lot, where vehicle types
  differ only by size and rate → enum.)
- **Q2: do they share mutable state?** **Yes.** Every piece has a `colour` and a
  `hasMoved` flag. That state must live *somewhere*, and an interface cannot hold
  it — `interface P { int x; }` compiles, but silently becomes
  `public static final`: a shared constant, not per-object state.

Q2 says yes, so: **`abstract class Piece`**. Stop.

Say that out loud as a sentence:

> "Pieces share state — colour and hasMoved — so an interface is off the table;
> the compiler would turn those fields into shared constants. Abstract class,
> holding the shared state and the shared sliding logic, with each subclass
> supplying only what actually differs."

The hierarchy also earns real reuse, which is the test for whether it deserves
to exist: `slide()` is written once and used by Bishop, Rook and Queen;
`step()` is written once and used by Knight and King. Six subclasses, two shared
helpers, no duplication.

**And the pawn is deliberately not made to fit.** Pawns move one way, capture
another, get a double-step from home, and promote. Forcing them into a generic
movement abstraction is the classic over-engineering trap here. They get their
own subclass with no shared helper, and that asymmetry is correct.

### Decision 2: pseudo-legal vs legal — the separation that makes check tractable

Two different notions, and conflating them is *the* chess bug:

- **pseudoLegal** — does this piece move like that, and is the destination not
  occupied by my own side?
- **legal** — pseudoLegal **and** it does not leave *my own* king attacked.

`isAttacked()` must use **pseudo-legal** moves. Two reasons, both worth saying:

1. **A pinned piece still gives check.** A piece that cannot legally move because
   it is pinned still attacks squares, so filtering by legality here gives the
   wrong answer.
2. **Legality would recurse forever.** `legal` → "am I in check?" → `isAttacked`
   → `legal` → … Keeping the two separate is precisely what terminates it.

Once separated, checkmate and stalemate collapse into **one** test:

```java
if (!allLegalMoves(turn).isEmpty()) return IN_PROGRESS;
return inCheck(turn) ? opponentWins : STALEMATE;
```

"No legal moves" is the shared condition; being in check is the only thing that
distinguishes losing from drawing. Candidates who write two independent searches
have missed the insight.

---

## Phase 4 — API (15:00–20:00)

```java
boolean      move(String from, String to);   // "e2","e4"; false = illegal
List<Square> legalMoves(Square from);
boolean      inCheck(Colour c);
GameState    state();
```

`move` returns `boolean`: an illegal move is an expected outcome of a UI
handing you a click, not a programming error.

---

## Phase 5 — CODE (20:00–35:00)

### A real bug I hit here, and what I changed because of it

My first test setup did this:

```java
Chess g = new Chess(new Board(), Colour.BLACK);   // empty board
g.board().put("g1", new King(Colour.WHITE));      // ...then place pieces
```

Three assertions failed. The cause: the constructor calls `recomputeState()`,
which on an *empty* board finds no legal moves and no king, so it latches
`STALEMATE` — and every subsequent `move()` is then refused by the game-over
guard. Move generation was fine all along; `legalMoves("d8")` returned the right
13 squares.

The tempting fix is to fix the test. **The right fix was to fix the API**, because
an object that must be mutated after construction to become valid is an object
whose state is stale from birth, and the next person will hit it too. So:

- `Board.with(...)` returns `this`, so a position is built as one expression and
  arrives at the constructor **complete**;
- the constructor **rejects** a position missing either king;
- a regression test asserts that rejection.

That is the general lesson worth carrying: when your own test misuses your API,
that is evidence about the API, not just about the test.

---

## Phase 6 — EXTEND (35:00–45:00)

**1. "How do you know your move generation is right?"**

This is the question that separates chess answers. Unit tests on individual
pieces prove almost nothing — the bugs live in *interactions*. The standard
ground truth is **perft**: count the leaf nodes of the legal-move tree to depth
*n*. Those counts are published and agreed by every engine ever written, so it is
a differential test against the entire field rather than against my own
assumptions.

Real output from this file:

```
perft(1) = 20    expected 20      [1 ms]
perft(2) = 400   expected 400     [3 ms]
perft(3) = 8902  expected 8902    [26 ms]
```

Depth 3 is the honest stopping point given my scope: castling, en passant and
promotion are all unreachable within the first three plies, so these three
numbers are valid *despite* those omissions. Depth 4 (197,281) would begin to
diverge, and claiming it would be dishonest.

**2. "Have you seen those tests fail?"** Mutation-tested, two injected bugs:

| Injected bug | What caught it |
|---|---|
| Pawns may capture straight ahead | perft(1) ✅ passes, perft(2) ✅ passes, **perft(3) fails: 9070 vs 8902** |
| Skip the pin filter (allow moves exposing your own king) | 8 assertions fail, including Fool's Mate and both mate tests |

The first row is the interesting one. A shallow test suite would have declared
that bug absent: pawns cannot contact each other until ply 3, so the error is
literally invisible at lower depths. **Depth is what makes the test sensitive**,
and the 168-node gap is a precise signal, not a vague "something's wrong".

**3. "Add castling."** State I already have — `hasMoved` on King and Rook is
there for exactly this. The rule needs three checks: neither piece has moved, the
squares between are empty, and the king is not in check *and* does not pass
*through* an attacked square. That last clause is the one everybody forgets, and
it is why castling needs `isAttacked` on the intermediate square, not just the
destination.

**4. "Add en passant."** This one does *not* fit the current design, and I would
say so. It depends on the **previous move**, and my `Board` is memoryless. It
needs an `enPassantTarget` field set on each double pawn push and cleared every
other move. A rule that depends on history is a genuine structural change, not a
new subclass.

**5. "Add an AI."** `perft` is already the move tree; minimax with
alpha–beta walks the same generator. The bottleneck would show immediately:
`legalMoves` copies the whole board per candidate move. Real engines use
make/unmake with an undo record. I would only make that change once profiling
demanded it — the copy is O(64) and perft(3) runs in 26 ms, so it is not the
problem yet.

**6. "Draw by repetition / 50-move rule."** Both need history: a
`Map<positionHash, count>` (Zobrist hashing is the standard) and a halfmove
clock. Again — history, not hierarchy.

---

## Self-check

- Did you justify abstract-class-over-interface with the **shared state** rule,
  or just assert "pieces are a hierarchy"?
- Did you separate pseudo-legal from legal, and can you say why it prevents
  infinite recursion?
- Did you notice checkmate and stalemate are one test with one branch?
- Did you resist forcing the pawn into the generic movement abstraction?
- Do you have ground truth (perft), or only tests that encode your own beliefs?
