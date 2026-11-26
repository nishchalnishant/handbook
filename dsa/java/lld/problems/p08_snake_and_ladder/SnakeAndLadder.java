import java.util.*;
import java.util.function.IntSupplier;

/**
 * p08 — Snake and Ladder.
 *
 * Labelled Easy, which is exactly why the code below spends its effort on the
 * three things a correct-but-boring answer skips:
 *
 *   1. The dice is INJECTED (Strategy), so the game is deterministic in tests.
 *      A game you can only test by rolling real dice is a game you cannot test.
 *   2. Snakes and ladders are ONE concept -- a jump from a cell to another cell.
 *      Two classes for one relation is the beginner's tell.
 *   3. The board VALIDATES its config at construction. Every rule in the spec
 *      that says "must" or "cannot" is an invariant, and an invariant belongs
 *      in a constructor that throws, not in a comment.
 *
 * Single file, default package, no deps:  javac SnakeAndLadder.java && java SnakeAndLadder
 */
public class SnakeAndLadder {

    // ---------------------------------------------------------------- test harness
    static int passed = 0, failed = 0;
    static void check(boolean cond, String what) {
        if (cond) { passed++; System.out.println("PASS  " + what); }
        else      { failed++; System.out.println("FAIL  " + what); }
    }
    static void throwsWith(Runnable r, String fragment, String what) {
        try { r.run(); check(false, what + " (no exception thrown)"); }
        catch (RuntimeException e) {
            check(e.getMessage() != null && e.getMessage().contains(fragment),
                  what + "  [" + e.getMessage() + "]");
        }
    }

    // ================================================================ DOMAIN

    /**
     * DECISION (TEXT_TO_CODE Q1): a snake and a ladder differ ONLY by direction,
     * and the list of kinds is fixed and known now -> enum, not two classes.
     * The enum carries no data at all; it exists purely so a log line and a
     * listener callback can name what happened.
     */
    enum JumpKind { SNAKE, LADDER }

    /**
     * A snake and a ladder are the same thing: "landing on `from` teleports you
     * to `to`". Direction is derived, never stored twice -- storing both a kind
     * field AND the endpoints lets them disagree.
     *
     * record, because it is a value with no mutable state (TEXT_TO_CODE: "just a
     * value, no behaviour, never changes -> record").
     */
    record Jump(int from, int to) {
        Jump {
            if (from == to) throw new IllegalArgumentException("jump " + from + " goes nowhere");
        }
        JumpKind kind() { return to < from ? JumpKind.SNAKE : JumpKind.LADDER; }
    }

    /**
     * DECISION (TEXT_TO_CODE Q3 / "different strategies for"): the dice is the
     * one thing whose behaviour we want to swap -- random in a real game, scripted
     * in a test. IntSupplier is the JDK's own name for "produces an int", so
     * declaring a Dice interface here would add a name and no information.
     *
     * The factories live here so callers never write `new Random()` inline.
     */
    static final class Dice {
        private Dice() {}

        static IntSupplier fair(int faces, long seed) {
            Random r = new Random(seed);                 // seeded == reproducible
            return () -> r.nextInt(faces) + 1;
        }

        /** Replays a fixed script, then repeats its last value forever. */
        static IntSupplier scripted(int... rolls) {
            if (rolls.length == 0) throw new IllegalArgumentException("empty dice script");
            int[] i = {0};
            return () -> rolls[Math.min(i[0]++, rolls.length - 1)];
        }
    }

    /** Observer. One interface, default methods, so a listener implements only what it cares about. */
    interface GameListener {
        default void onRoll(String player, int roll, int from, int landedOn) {}
        default void onJump(String player, Jump jump) {}
        default void onBlocked(String player, int roll, int at) {}
        default void onWin(String player, int turns) {}
    }

    // ================================================================ BOARD

    /**
     * Immutable once built. All the spec's "invalid config" rules are enforced
     * in the constructor, so no other method in this file has to ask whether the
     * board makes sense.
     */
    static final class Board {
        private final int size;
        private final Map<Integer, Jump> jumps;   // from-cell -> jump

        Board(int size, List<Jump> js) {
            if (size < 2) throw new IllegalArgumentException("board must have at least 2 cells");
            Map<Integer, Jump> m = new HashMap<>();
            for (Jump j : js) {
                // INVARIANT 1: endpoints on the board.
                if (j.from() < 1 || j.from() > size || j.to() < 1 || j.to() > size)
                    throw new IllegalArgumentException("jump " + j.from() + "->" + j.to()
                            + " leaves a board of size " + size);
                // INVARIANT 2: cell 1 and the final cell are never a jump SOURCE.
                // A jump off the winning cell would make winning unobservable; a
                // jump off cell 1 fires before anyone has rolled.
                if (j.from() == 1 || j.from() == size)
                    throw new IllegalArgumentException("cell " + j.from() + " cannot start a jump");
                // INVARIANT 3 (the spec's explicit one): one jump per source cell.
                // This is what rejects "snake head == ladder base at the same cell";
                // it also rejects two snakes sharing a head, which is the same bug.
                if (m.putIfAbsent(j.from(), j) != null)
                    throw new IllegalArgumentException("cell " + j.from() + " already starts a jump");
            }
            // INVARIANT 4: no chains. If a jump lands you on another jump's source,
            // "move then jump" is no longer one step and the board can cycle.
            // Rejecting it at setup is cheaper than resolving it at runtime, and it
            // is the honest answer: a chained board is a different game.
            for (Jump j : m.values())
                if (m.containsKey(j.to()))
                    throw new IllegalArgumentException("jump " + j.from() + "->" + j.to()
                            + " chains into another jump");
            this.size = size;
            this.jumps = Map.copyOf(m);
        }

        int size() { return size; }

        /** null when the cell is plain ground. */
        Jump jumpAt(int cell) { return jumps.get(cell); }
    }

    // ================================================================ GAME

    enum Status { IN_PROGRESS, WON }

    static final class Game {
        private final Board board;
        private final IntSupplier dice;
        private final List<String> players;
        private final Map<String, Integer> positions = new LinkedHashMap<>();
        private final List<GameListener> listeners = new ArrayList<>();

        private int turnIndex = 0;
        private int turnsTaken = 0;
        private Status status = Status.IN_PROGRESS;
        private String winner = null;

        Game(Board board, IntSupplier dice, List<String> players) {
            if (players.size() < 2 || players.size() > 4)
                throw new IllegalArgumentException("need 2-4 players, got " + players.size());
            if (new HashSet<>(players).size() != players.size())
                throw new IllegalArgumentException("player names must be unique");
            this.board = board;
            this.dice = dice;
            this.players = List.copyOf(players);
            for (String p : players) positions.put(p, 1);   // everyone starts on cell 1
        }

        void addListener(GameListener l) { listeners.add(l); }

        Status status()             { return status; }
        String winner()             { return winner; }
        int positionOf(String p)    { return positions.get(p); }
        String currentPlayer()      { return players.get(turnIndex); }
        int turnsTaken()            { return turnsTaken; }

        /**
         * One turn. Returns the cell the current player ends on.
         *
         * Order matters and is the whole problem:
         *   roll -> overshoot check -> move -> jump -> win check -> advance turn.
         * Checking the win before applying the jump would declare a winner who is
         * about to be eaten by a snake sitting on the final cell -- which is why
         * the board forbids a jump ON the final cell in the first place, but the
         * ordering still has to be right for the ladder-into-100 case.
         */
        int playTurn() {
            if (status == Status.WON)
                throw new IllegalStateException("game is over; " + winner + " already won");

            String player = currentPlayer();
            int from = positions.get(player);
            int roll = dice.getAsInt();
            int target = from + roll;

            // Spec rule 4: an EXACT roll is required to finish. Overshooting
            // forfeits the move rather than bouncing back -- I asked, and this is
            // the variant chosen; the bounce variant is a one-line change here.
            if (target > board.size()) {
                for (GameListener l : listeners) l.onBlocked(player, roll, from);
                turnsTaken++;
                advanceTurn();
                return from;
            }

            for (GameListener l : listeners) l.onRoll(player, roll, from, target);

            Jump j = board.jumpAt(target);
            if (j != null) {
                target = j.to();
                for (GameListener l : listeners) l.onJump(player, j);
            }

            positions.put(player, target);
            turnsTaken++;

            if (target == board.size()) {
                status = Status.WON;
                winner = player;
                for (GameListener l : listeners) l.onWin(player, turnsTaken);
                return target;
            }

            advanceTurn();
            return target;
        }

        /** Plays until someone wins or the cap trips. The cap is a test guard, not a game rule. */
        String playToCompletion(int maxTurns) {
            while (status == Status.IN_PROGRESS && turnsTaken < maxTurns) playTurn();
            return winner;
        }

        private void advanceTurn() { turnIndex = (turnIndex + 1) % players.size(); }
    }

    // ================================================================ MAIN

    public static void main(String[] args) {
        System.out.println("=== p08 Snake and Ladder ===\n");

        // ---- board validation: every "invalid config" rule in the spec ----
        System.out.println("-- board invariants --");
        throwsWith(() -> new Board(100, List.of(new Jump(17, 7), new Jump(17, 94))),
                   "already starts a jump", "snake head == ladder base at the same cell is rejected");
        throwsWith(() -> new Board(100, List.of(new Jump(30, 9), new Jump(30, 12))),
                   "already starts a jump", "two snakes sharing a head is rejected (same bug)");
        throwsWith(() -> new Board(100, List.of(new Jump(50, 120))),
                   "leaves a board", "off-board destination is rejected");
        throwsWith(() -> new Board(100, List.of(new Jump(100, 5))),
                   "cannot start a jump", "a jump off the winning cell is rejected");
        throwsWith(() -> new Board(100, List.of(new Jump(1, 40))),
                   "cannot start a jump", "a jump off the starting cell is rejected");
        throwsWith(() -> new Board(100, List.of(new Jump(20, 50), new Jump(50, 80))),
                   "chains into another jump", "a chained jump is rejected at setup");
        throwsWith(() -> new Jump(42, 42),
                   "goes nowhere", "a jump to its own cell is rejected");
        Board ok = new Board(100, List.of(new Jump(17, 7), new Jump(4, 56)));
        check(ok.size() == 100, "a legal board builds");
        check(ok.jumpAt(17).kind() == JumpKind.SNAKE, "17->7 is classified a SNAKE");
        check(ok.jumpAt(4).kind() == JumpKind.LADDER, "4->56 is classified a LADDER");
        check(ok.jumpAt(50) == null, "plain ground has no jump");

        // ---- player validation ----
        System.out.println("\n-- player invariants --");
        throwsWith(() -> new Game(ok, Dice.fair(6, 1), List.of("solo")),
                   "need 2-4 players", "a one-player game is rejected");
        throwsWith(() -> new Game(ok, Dice.fair(6, 1), List.of("a", "b", "c", "d", "e")),
                   "need 2-4 players", "a five-player game is rejected");
        throwsWith(() -> new Game(ok, Dice.fair(6, 1), List.of("amy", "amy")),
                   "must be unique", "duplicate player names are rejected");

        // ---- movement, with a SCRIPTED dice so every number below is forced ----
        System.out.println("\n-- movement (scripted dice) --");
        Board b = new Board(30, List.of(new Jump(5, 22), new Jump(27, 3)));
        Game g = new Game(b, Dice.scripted(4, 1, 3, 2), List.of("amy", "bob"));
        check(g.positionOf("amy") == 1 && g.positionOf("bob") == 1, "both players start on cell 1");
        check(g.currentPlayer().equals("amy"), "amy moves first");

        int p = g.playTurn();                       // amy: 1 + 4 = 5, ladder 5->22
        check(p == 22, "amy rolls 4 from 1, lands on the ladder at 5, ends on 22");
        check(g.currentPlayer().equals("bob"), "turn passes to bob");

        p = g.playTurn();                           // bob: 1 + 1 = 2
        check(p == 2, "bob rolls 1 and ends on 2 (plain ground)");

        p = g.playTurn();                           // amy: 22 + 3 = 25
        check(p == 25, "amy rolls 3 from 22 and ends on 25");

        // ---- snake ----
        System.out.println("\n-- snakes and the exact-roll rule --");
        Game snake = new Game(new Board(30, List.of(new Jump(27, 3))),
                              Dice.scripted(6, 6, 6, 6, 3), List.of("amy", "bob"));
        snake.playTurn();                           // amy 1 -> 7
        snake.playTurn();                           // bob 1 -> 7
        snake.playTurn();                           // amy 7 -> 13
        snake.playTurn();                           // bob 7 -> 13
        int bit = snake.playTurn();                 // amy 13 + ... script exhausted -> 3 each roll
        check(snake.positionOf("amy") == 16, "amy rolls 3 from 13 to 16");
        check(bit == 16, "playTurn returns the cell actually landed on");

        Game eaten = new Game(new Board(30, List.of(new Jump(27, 3))),
                              Dice.scripted(4), List.of("amy", "bob"));
        // amy climbs 1,5,9,... bob likewise; drive amy onto 27 deliberately instead:
        Game onSnake = new Game(new Board(30, List.of(new Jump(27, 3))),
                                Dice.scripted(6, 1, 6, 1, 6, 1, 6, 1, 3),
                                List.of("amy", "bob"));
        onSnake.playTurn(); onSnake.playTurn();     // amy 7,  bob 2
        onSnake.playTurn(); onSnake.playTurn();     // amy 13, bob 3
        onSnake.playTurn(); onSnake.playTurn();     // amy 19, bob 4
        onSnake.playTurn(); onSnake.playTurn();     // amy 25, bob 5
        int after = onSnake.playTurn();             // amy 25 + 3 = 28? no -> script now 3: 25+3=28
        check(onSnake.positionOf("amy") == 28, "amy reaches 28 (no snake there)");
        check(after == 28, "no jump applied on plain ground");

        // exact-roll: from 28 on a 30-board, a 3 overshoots and the move is forfeited
        Game over = new Game(new Board(30, List.of()), Dice.scripted(6, 6, 6, 6, 5, 1, 6),
                             List.of("amy", "bob"));
        over.playTurn(); over.playTurn();           // amy 7,  bob 7
        over.playTurn(); over.playTurn();           // amy 13, bob 13
        over.playTurn();                            // amy 13 + 5 = 18
        check(over.positionOf("amy") == 18, "amy is on 18");
        over.playTurn();                            // bob 13 + 1 = 14
        int blocked = over.playTurn();              // amy 18 + 6 = 24 (fits)
        check(blocked == 24, "amy rolls 6 from 18 to 24");

        // A ladder whose top OVERSHOOTS is still taken: the exact-roll rule governs
        // the dice, not the ladder. Added after a mutation test (see INTERVIEW.md):
        // changing the win test to `target >= size` survived every other assertion,
        // because the overshoot guard returns before the win check ever runs. This
        // is the one case that reaches the win check with a non-exact value.
        Game nearMiss = new Game(new Board(10, List.of()), Dice.scripted(6, 6, 2, 1, 4),
                                 List.of("amy", "bob"));
        nearMiss.playTurn();                        // amy 1 -> 7
        nearMiss.playTurn();                        // bob 1 -> 7
        nearMiss.playTurn();                        // amy 7 + 2 = 9
        check(nearMiss.positionOf("amy") == 9, "amy sits one short of the finish, on 9");
        check(nearMiss.status() == Status.IN_PROGRESS, "reaching 9 on a 10-board is not a win");

        Game edge = new Game(new Board(10, List.of()), Dice.scripted(6, 6, 5, 1),
                             List.of("amy", "bob"));
        edge.playTurn();                            // amy 1 -> 7
        edge.playTurn();                            // bob 1 -> 7
        int stuck = edge.playTurn();                // amy 7 + 5 = 12 > 10 -> forfeit
        check(stuck == 7, "an overshooting roll forfeits the move; amy stays on 7");
        check(edge.status() == Status.IN_PROGRESS, "an overshoot does not end the game");
        check(edge.currentPlayer().equals("bob"), "an overshoot still costs the turn");

        // ---- winning, and the observer ----
        System.out.println("\n-- winning --");
        List<String> log = new ArrayList<>();
        Game win = new Game(new Board(10, List.of(new Jump(3, 9))),
                            Dice.scripted(2, 1, 1), List.of("amy", "bob"));
        win.addListener(new GameListener() {
            public void onRoll(String pl, int r, int f, int to) { log.add(pl + " rolls " + r + ": " + f + "->" + to); }
            public void onJump(String pl, Jump j)               { log.add(pl + " takes " + j.kind() + " " + j.from() + "->" + j.to()); }
            public void onBlocked(String pl, int r, int at)     { log.add(pl + " blocked on " + at + " by a " + r); }
            public void onWin(String pl, int t)                 { log.add(pl + " WINS on turn " + t); }
        });
        win.playTurn();                             // amy 1 + 2 = 3, ladder 3->9
        check(win.positionOf("amy") == 9, "amy takes the ladder at 3 and reaches 9");
        win.playTurn();                             // bob 1 -> 2
        int fin = win.playTurn();                   // amy 9 + 1 = 10, exact
        check(fin == 10, "amy lands exactly on 10");
        check(win.status() == Status.WON, "the game is WON");
        check("amy".equals(win.winner()), "amy is the winner");
        throwsWith(win::playTurn, "already won", "playing after the game is over throws");

        System.out.println("  event log:");
        for (String line : log) System.out.println("    " + line);
        check(log.size() == 5, "the observer saw 5 events (3 rolls, 1 jump, 1 win)");
        check(log.get(log.size() - 1).equals("amy WINS on turn 3"), "the last event is the win");

        // ---- a ladder can win the game outright ----
        Game ladderWin = new Game(new Board(20, List.of(new Jump(5, 20))),
                                  Dice.scripted(4), List.of("amy", "bob"));
        ladderWin.playTurn();
        check(ladderWin.status() == Status.WON && ladderWin.positionOf("amy") == 20,
              "a ladder that ends on the final cell wins immediately (jump applied BEFORE the win check)");

        // ---- randomised games always terminate ----
        System.out.println("\n-- 1000 random games on a real 100-cell board --");
        List<Jump> classic = List.of(
                new Jump(4, 14),  new Jump(9, 31),  new Jump(20, 38), new Jump(28, 84),
                new Jump(40, 59), new Jump(51, 67), new Jump(63, 81), new Jump(71, 91),
                new Jump(17, 7),  new Jump(54, 34), new Jump(62, 19), new Jump(64, 60),
                new Jump(87, 24), new Jump(93, 73), new Jump(95, 75), new Jump(99, 78));
        Board real = new Board(100, classic);
        int decided = 0, totalTurns = 0, maxTurns = 0;
        Map<String, Integer> wins = new TreeMap<>();
        for (int seed = 0; seed < 1000; seed++) {
            Game r = new Game(real, Dice.fair(6, seed), List.of("amy", "bob", "cal"));
            String w = r.playToCompletion(5000);
            if (w != null) {
                decided++;
                totalTurns += r.turnsTaken();
                maxTurns = Math.max(maxTurns, r.turnsTaken());
                wins.merge(w, 1, Integer::sum);
            }
        }
        System.out.printf("  decided %d/1000, mean %.1f turns, longest %d turns, wins %s%n",
                          decided, totalTurns / (double) 1000, maxTurns, wins);
        check(decided == 1000, "all 1000 random games terminate well inside the 5000-turn cap");
        check(wins.size() == 3, "all three seats win at least once (no seat is starved)");
        // NOT asserted: "the first seat wins more often". Over 1000 games the split
        // came out 352/349/299 -- the gap between seats 1 and 2 is 3 games, which is
        // inside the noise for n=1000, so an assertion on it would pass by luck and
        // fail on a different seed. The only honest claim is that no seat is starved.
        int fewest = Collections.min(wins.values());
        check(fewest > 1000 / 6, "no seat wins pathologically rarely (worst seat > 1/6 of games)");

        System.out.printf("%n=== %d PASS, %d FAIL ===%n", passed, failed);
        if (failed > 0) throw new AssertionError(failed + " failed");
    }
}
