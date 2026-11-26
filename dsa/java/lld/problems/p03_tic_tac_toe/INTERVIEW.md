# p03 Tic-Tac-Toe — THE SCRIPT, run end to end

Procedure: `../../../notes/THE_SCRIPT.md`. Decision tree: `../../../notes/TEXT_TO_CODE.md`.

Every claim below is checkable against `TicTacToe.java` in this folder.

> **Read this only after you have attempted `ATTEMPT.md`.** This problem is
> labelled Easy, which makes it *more* dangerous, not less: the interviewer has
> seen a hundred correct tic-tac-toe boards, so a correct board scores nothing.
> The signal is entirely in the win-detection argument in Phase 5.

---

## PHASE 1 — SCOPE (0:00–5:00)

> "Two-player tic-tac-toe on an NxN board. Players alternate, X first, and after
> each move I detect a win on a row, a column, or either diagonal, plus a draw
> when the board fills.
>
> I'm scoping to a single process, in-memory, two human players — no AI opponent,
> no undo, no persistence, no network. Those are all additive later.
>
> The part actually worth designing is win detection, because the naive version
> is O(N²) per move and there's an O(1) version. I'll build toward that."

**The five questions** (two planted):

| Ask | What you're really fishing for |
|---|---|
| "Is the board always 3x3, or configurable N?" | forces the general algorithm; 3x3 hides the interesting bug |
| "Do I need to detect a win after *every* move, or only on demand?" | sets up the **incremental counters** |
| "Should an illegal move throw, or return a status?" | error-handling philosophy — a real signal |
| "Do I need undo, or replay of a game?" | **planted**: if yes, you need a move log, not just a board |
| "Two human players, or is one an AI?" | **planted**: an AI needs the board to be cheaply *copyable* |

The last two are the ones that separate candidates. You are showing that you
know which future requirements would change the data structure.

---

## PHASE 2 — NOUNS (5:00–10:00)

> "Let me pull the entities out of the statement."

```
Board   Cell   Player   Mark   Move   Game   GameState   WinChecker
```

**Merge and defer, out loud:**
- *"`Cell` is just a `Mark` or empty — a whole class for it earns nothing. It's an array element."*
- *"`Player` and `Mark` collapse. In a two-human game the player IS their mark. If I
  later add names or scores, `Player` comes back as its own class holding a `Mark`."*
- *"`Move` I only need if I want undo or replay. I asked; the answer was no, so I
  defer it. I'll say where it would slot in."*
- *"`WinChecker` sounds like a class but it's one method over the board's own data.
  Pulling it out would break the rule that a method lives with the data it needs."*

Leaves three: **Mark, GameState, TicTacToe.**

> Cutting five nouns down to three, *with a reason for each cut*, is the whole
> point of this phase. Candidates who keep all eight spend Phase 5 writing
> constructors instead of the algorithm.

---

## PHASE 3 — DECIDE (10:00–15:00)

| Noun | Question asked | Answer | Say out loud |
|---|---|---|---|
| `Mark` | Q1 — fixed list, differ only by data? **YES** | **enum** | *"Exactly two, known at compile time. It carries a `delta` of +1 / −1, which I'll use for the counters."* |
| `GameState` | Q1 — fixed list of outcomes | **enum** | *"IN_PROGRESS, X_WINS, O_WINS, DRAW. Four, closed set, no behaviour."* |
| `TicTacToe` | state that changes over time | **class** | *"It owns the board and the counters, so the move logic lives here."* |
| `WinStrategy` | Q4 — one variant, none in sight | **plain method** | *"I'm deliberately NOT making this an interface."* |

### The one to defend: refusing the Strategy interface

The source material lists "Strategy (win checker)" as a pattern for this problem.
Say why you are not using it:

> *"I could put win detection behind a `WinStrategy` interface, but there's exactly
> one rule and no second one in sight — that's Q4 in my decision tree, and the
> answer is a plain method. An interface with one implementation is indirection I
> have to pay for on every read and get nothing back for.
>
> The moment there's a second variant — misère rules, or Connect-4 style
> gravity — I'd extract the interface then. That's the rule of three, and it's
> cheap to do later because the counters are already private."*

Interviewers ask "what pattern is this?" to see whether you apply patterns
reflexively. Naming a pattern and then **declining it with a reason** scores
higher than using it.

### The one you *should* accept

`Mark.other()` lives on the enum, not in the game class:

```java
enum Mark {
    X(+1), O(-1);
    Mark other() { return this == X ? O : X; }
}
```

> *"Whose turn is next is a fact about marks, not about the game. Putting it on
> the enum means the game class never writes `turn == X ? O : X` — that ternary
> would otherwise appear in three places and get one of them wrong."*

---

## PHASE 4 — API (15:00–20:00)

Signatures only, no bodies. Say: *"Could someone use this without reading the
implementation?"*

```java
enum Mark      { X, O; Mark other(); int delta(); }
enum GameState { IN_PROGRESS, X_WINS, O_WINS, DRAW }

class TicTacToe {
    TicTacToe(int n);
    GameState move(Mark player, int row, int col);   // throws on illegal
    GameState state();
    Mark      turn();
    String    render();
}
```

**Two API decisions to narrate:**

> *"`move` returns the new `GameState` rather than void. The caller almost always
> wants to know whether that move ended the game, and returning it saves a second
> call that could race in a threaded version."*

> *"Illegal moves throw, they don't return false. Playing out of turn or onto an
> occupied cell is a **caller bug**, not an expected branch. A boolean `false`
> that nobody checks is how that bug reaches production. I reserve return values
> for outcomes the caller is expected to handle."*

That second paragraph is a genuine seniority signal. Have it ready.

---

## PHASE 5 — CODE (20:00–35:00)

### The insight worth the whole interview

> *"The naive check rescans the board after every move: O(N²) a move, O(N⁴) for a
> full game. But a move can only complete a line that passes **through the cell
> just played**. So I keep running counters — one per row, one per column, two
> for the diagonals — and update four of them per move. That's O(1) per move and
> O(N) extra memory."*

### The sign trick

> *"X adds +1 and O adds −1 to the same counter. A win is `|counter| == N`. That
> works because a line containing both marks can never reach N in absolute
> value — the opposing marks cancel. So one integer per line encodes both
> 'how many' and 'whose', and I never store per-player counts."*

Prove it on the board, out loud: *"X, O, X in one row sums to +1, not 3."*
That is a real assertion in the file:

```
PASS  X O X in one row sums to +1, not 3 -- mixed lines cannot win
```

### The core, as written

```java
int d = player.delta();
rows[row] += d;
cols[col] += d;
if (row == col)         diag += d;
if (row + col == n - 1) anti += d;

if (Math.abs(rows[row]) == n || Math.abs(cols[col]) == n
        || Math.abs(diag) == n || Math.abs(anti) == n) {
    state = (player == Mark.X) ? GameState.X_WINS : GameState.O_WINS;
} else if (filled == n * n) {
    state = GameState.DRAW;
}
```

**The two conditions people get wrong:**

- `row + col == n - 1` is the anti-diagonal. Writing `row + col == n` is the
  single most common bug in this problem. Check it on a 3x3: the corner (0,2)
  gives 0 + 2 = 2 = n − 1. ✓
- Draw is checked **only after** the win check. A move that both fills the last
  cell and completes a line is a win, not a draw. Ordering these two the wrong
  way round is the second most common bug, and it only shows up in one game out
  of many — which is exactly why you assert it rather than eyeball it.

### Say this about the centre cell

> *"On an odd board the centre sits on both diagonals, so a move there updates
> four counters. Both `if`s fire. That's not a special case in the code and it
> shouldn't be — but it's worth checking, because a version that used
> `else if` there would be silently wrong on exactly one cell."*

---

## PHASE 6 — EXTEND (35:00–45:00)

### Follow-up #1 — "Now make it 10x10, win on 5 in a row"

The honest answer, and it costs you nothing to give it:

> *"That breaks my counters. They assume a winning line spans the whole board, so
> 'k in a row anywhere' needs a different algorithm — from the placed cell, walk
> outward in each of the four directions counting consecutive matching marks.
> That's O(k) per move, not O(1), but still far better than rescanning.
>
> I'd keep the same public API. `move` and `state` don't change, which is the
> point of having kept win detection private rather than exposing counters."*

Volunteering the limit of your own optimisation is a strong move. It is also
the follow-up that most often actually gets asked.

### Follow-up #2 — "Add undo"

> *"This is why I asked about it in Phase 1. Undo needs the deferred `Move`
> record — `record Move(Mark player, int row, int col)` on a `Deque`. Undo pops
> it, clears the cell, and subtracts the same four deltas. The counters are
> incrementally reversible, which is a nice property of having chosen sums over
> a rescan: I get undo in about six lines."*

### Follow-up #3 — "Add an AI opponent"

> *"Minimax needs to try a move, recurse, and take it back. That's exactly the
> undo above, so I'd build undo first and have the AI use it rather than copying
> the board at every node. For 3x3 the full tree is 9! ≈ 362,880 states, which is
> instant. For larger N you need alpha-beta pruning and a depth limit."*

### Follow-up #4 — "Two players hitting `move` concurrently"

The three-layer answer:

> *"In-process: `move` is the only mutator, so `synchronized` on it is correct
> and the contention is nil — it's microseconds and turn-based by nature.
>
> Note the check-then-act hazard: 'is it my turn' and 'apply the move' must be
> atomic, or both players can pass the turn check and both write. That's the
> real bug here, and it's why I don't expose `turn()` as a way to gate a move.
>
> Across machines: the board is shared state, so it moves to a store with a
> compare-and-set on a version column — each move carries the version it read,
> and a stale version loses. That also gives idempotent retries, which matters
> because a client that times out will resend."*

### Follow-up #5 — "How do you test this?"

> *"The four win directions, a mixed line that must NOT win, a genuine draw, the
> last-cell-wins ordering case, the 1x1 degenerate board, and every illegal move
> rejected. But the one that actually earns trust in an optimised algorithm is a
> **differential fuzz**: play thousands of random games and assert the O(1)
> counters agree, on every single position, with a deliberately stupid
> brute-force O(N²) rescan. Clever code checked against dumb code."*

That is not a suggestion in this folder — it is assertion 13:

```
differential fuzz: 3000 games, mismatches = 0
PASS  O(1) counters agree with a brute-force scan on every position
```

**And the test was itself tested.** Changing the anti-diagonal condition from
`row + col == n - 1` to `row + col == n` — the exact bug flagged in Phase 5 —
makes it fail loudly:

```
differential fuzz: 3000 games, mismatches = 611
FAIL  O(1) counters agree with a brute-force scan on every position
```

A test suite you have never seen fail is a test suite you have no evidence
works. Breaking it on purpose once is cheap, and it is the difference between
"I wrote tests" and "I know what my tests catch."

---

## Done when

`javac TicTacToe.java && java TicTacToe` prints the boards it builds and
**13 PASS** lines: row / column / both diagonals, a draw, the mixed-line case,
5x5, 1x1, four rejected illegal moves, and a 3,000-game differential fuzz
against a brute-force checker.

---

## Self-check

- [ ] Asked whether N is configurable *before* writing a 3x3-only solution
- [ ] Named the Strategy pattern and **declined** it with a reason
- [ ] Derived O(1) win detection, and said what the naive cost was
- [ ] Explained why `|counter| == N` cannot false-positive on a mixed line
- [ ] Got `row + col == n - 1` right, and checked it out loud on a corner
- [ ] Checked win *before* draw, and said why the order matters
- [ ] Volunteered where the counters break (k-in-a-row) unprompted
- [ ] Proposed a differential test against a brute-force checker
- [ ] Reached Phase 6 with time left

Verified backing: `TicTacToe.java` in this folder — `javac TicTacToe.java && java TicTacToe`
prints 13 PASS lines, and every number above is copied from that run.
