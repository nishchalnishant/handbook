import java.util.*;

/*
 * Design Tic-Tac-Toe -- worked solution.
 *
 * SCOPE   NxN board, two players alternating, X first. Win on row/column/either
 *         diagonal, draw when the board fills. Single process, no UI, no AI
 *         opponent, no undo, no persistence.
 *
 * API     Game(int n)
 *         GameState move(Mark player, int row, int col)
 *         GameState state()
 *
 * THE DECISION
 *   The interesting choice is win detection. The obvious implementation rescans
 *   the board after every move: O(N^2) per move, O(N^4) for a full game. But a
 *   move can only ever complete a line THROUGH THE CELL JUST PLAYED, so we keep
 *   running counters -- one per row, one per column, two for the diagonals --
 *   and a win is a counter reaching +N or -N. O(1) per move, O(N) memory.
 *
 *   X adds +1, O adds -1 to the same counter. |counter| == N means N marks of
 *   one player and none of the other, because a mixed line can never reach N.
 *   That sign trick is the whole algorithm and it is worth saying out loud.
 */

enum Mark {
    X(+1), O(-1);
    private final int delta;
    Mark(int d) { delta = d; }
    int delta() { return delta; }
    Mark other() { return this == X ? O : X; }
}

enum GameState { IN_PROGRESS, X_WINS, O_WINS, DRAW }

public class TicTacToe {

    private final int n;
    private final Mark[][] board;

    // The counters that make win detection O(1). rows[i] is the running sum of
    // deltas in row i; diag is the main diagonal, anti the other one.
    private final int[] rows, cols;
    private int diag, anti;

    private Mark turn = Mark.X;                 // "X goes first" from the spec
    private int filled = 0;
    private GameState state = GameState.IN_PROGRESS;

    public TicTacToe(int n) {
        // Invariant from the spec: a board smaller than 1x1 is meaningless.
        if (n < 1) throw new IllegalArgumentException("board must be at least 1x1, got " + n);
        this.n = n;
        this.board = new Mark[n][n];
        this.rows = new int[n];
        this.cols = new int[n];
    }

    public GameState state() { return state; }
    public Mark turn()       { return turn; }

    /**
     * Apply one move. Throws on an illegal move rather than returning a
     * boolean: a wrong-turn or occupied-cell move is a caller bug, not an
     * expected outcome, and a silent false is how those bugs stay hidden.
     */
    public GameState move(Mark player, int row, int col) {
        if (state != GameState.IN_PROGRESS)
            throw new IllegalStateException("game is over: " + state);
        if (player != turn)
            throw new IllegalArgumentException("not " + player + "'s turn, it is " + turn + "'s");
        if (row < 0 || row >= n || col < 0 || col >= n)
            throw new IllegalArgumentException("cell (" + row + "," + col + ") is off the board");
        if (board[row][col] != null)
            throw new IllegalArgumentException("cell (" + row + "," + col + ") already holds " + board[row][col]);

        board[row][col] = player;
        filled++;

        int d = player.delta();
        rows[row] += d;
        cols[col] += d;
        if (row == col)         diag += d;
        if (row + col == n - 1) anti += d;

        // Only lines through the played cell can have been completed.
        if (Math.abs(rows[row]) == n || Math.abs(cols[col]) == n
                || Math.abs(diag) == n || Math.abs(anti) == n) {
            state = (player == Mark.X) ? GameState.X_WINS : GameState.O_WINS;
        } else if (filled == n * n) {
            state = GameState.DRAW;
        } else {
            turn = turn.other();
        }
        return state;
    }

    public String render() {
        StringBuilder sb = new StringBuilder();
        for (Mark[] r : board) {
            for (Mark m : r) sb.append(m == null ? "." : m.name());
            sb.append('\n');
        }
        return sb.toString();
    }

    // ------------------------------------------------------------------
    /**
     * Deliberately stupid reference implementation: rescan every line, every
     * time. O(N^2) and obviously correct, which is exactly what a differential
     * test needs -- you check the clever code against the dumb code.
     */
    private static GameState bruteForce(Mark[][] b, int n) {
        List<Mark[]> lines = new ArrayList<>();
        Mark[] diag = new Mark[n], anti = new Mark[n];
        for (int i = 0; i < n; i++) {
            Mark[] row = new Mark[n], col = new Mark[n];
            for (int j = 0; j < n; j++) { row[j] = b[i][j]; col[j] = b[j][i]; }
            lines.add(row); lines.add(col);
            diag[i] = b[i][i]; anti[i] = b[i][n - 1 - i];
        }
        lines.add(diag); lines.add(anti);

        for (Mark[] line : lines) {
            Mark first = line[0];
            if (first == null) continue;
            boolean all = true;
            for (Mark m : line) if (m != first) { all = false; break; }
            if (all) return first == Mark.X ? GameState.X_WINS : GameState.O_WINS;
        }
        for (Mark[] row : b) for (Mark m : row) if (m == null) return GameState.IN_PROGRESS;
        return GameState.DRAW;
    }

    private static int passes = 0, fails = 0;
    private static void check(boolean ok, String what) {
        System.out.println((ok ? "PASS  " : "FAIL  ") + what);
        if (ok) passes++; else fails++;
    }

    public static void main(String[] args) {
        // --- a row win
        TicTacToe g = new TicTacToe(3);
        g.move(Mark.X, 0, 0); g.move(Mark.O, 1, 0);
        g.move(Mark.X, 0, 1); g.move(Mark.O, 1, 1);
        GameState s = g.move(Mark.X, 0, 2);
        System.out.print(g.render());
        check(s == GameState.X_WINS, "top row completes -> X_WINS");

        // --- a diagonal win, and O can win too
        TicTacToe d = new TicTacToe(3);
        d.move(Mark.X, 0, 1); d.move(Mark.O, 0, 0);
        d.move(Mark.X, 0, 2); d.move(Mark.O, 1, 1);
        d.move(Mark.X, 2, 1); d.move(Mark.O, 2, 2);
        check(d.state() == GameState.O_WINS, "main diagonal completes -> O_WINS");

        // --- anti-diagonal, the one people forget to implement
        TicTacToe a = new TicTacToe(3);
        a.move(Mark.X, 0, 2); a.move(Mark.O, 0, 0);
        a.move(Mark.X, 1, 1); a.move(Mark.O, 1, 0);
        a.move(Mark.X, 2, 0);
        check(a.state() == GameState.X_WINS, "anti-diagonal completes -> X_WINS");

        // --- a genuine draw: board full, no line
        TicTacToe dr = new TicTacToe(3);
        int[][] order = {{0,0},{0,1},{0,2},{1,1},{1,0},{1,2},{2,1},{2,0},{2,2}};
        GameState last = GameState.IN_PROGRESS;
        for (int[] c : order) last = dr.move(dr.turn(), c[0], c[1]);
        System.out.print(dr.render());
        check(last == GameState.DRAW, "full board with no line -> DRAW");

        // --- the counter trick: a MIXED line never reaches |N|
        TicTacToe m = new TicTacToe(3);
        m.move(Mark.X, 0, 0); m.move(Mark.O, 0, 1); m.move(Mark.X, 0, 2);
        check(m.state() == GameState.IN_PROGRESS,
              "X O X in one row sums to +1, not 3 -- mixed lines cannot win");

        // --- NxN really is configurable
        TicTacToe big = new TicTacToe(5);
        for (int i = 0; i < 4; i++) { big.move(Mark.X, 2, i); big.move(Mark.O, 3, i); }
        check(big.move(Mark.X, 2, 4) == GameState.X_WINS, "5x5 row win needs all 5 cells");

        // --- 1x1 is the degenerate case: X wins immediately
        check(new TicTacToe(1).move(Mark.X, 0, 0) == GameState.X_WINS, "1x1 board: first move wins");

        // --- illegal moves are rejected loudly
        TicTacToe e = new TicTacToe(3);
        e.move(Mark.X, 1, 1);
        try { e.move(Mark.X, 0, 0); check(false, "should reject out-of-turn move"); }
        catch (IllegalArgumentException ok) { check(true, "rejects a move out of turn"); }
        try { e.move(Mark.O, 1, 1); check(false, "should reject occupied cell"); }
        catch (IllegalArgumentException ok) { check(true, "rejects an occupied cell"); }
        try { e.move(Mark.O, 3, 0); check(false, "should reject off-board cell"); }
        catch (IllegalArgumentException ok) { check(true, "rejects an off-board cell"); }
        try { new TicTacToe(0); check(false, "should reject a 0x0 board"); }
        catch (IllegalArgumentException ok) { check(true, "rejects a 0x0 board"); }

        // --- a finished game stays finished
        try { g.move(Mark.O, 2, 2); check(false, "should reject a move after the win"); }
        catch (IllegalStateException ok) { check(true, "rejects any move after the game ends"); }

        // --- differential fuzz: the O(1) counters vs a brute-force O(N^2) scan.
        // This is how you actually trust an optimised algorithm. It is also what
        // would have caught `row + col == n` instead of `n - 1`, on the one board
        // in many where the anti-diagonal is the only completed line.
        int games = 0, mismatches = 0;
        Random rnd = new Random(42);              // seeded -> reproducible failures
        for (int iter = 0; iter < 3000; iter++) {
            int n = 3 + rnd.nextInt(3);           // 3x3 .. 5x5
            TicTacToe t = new TicTacToe(n);
            List<int[]> cells = new ArrayList<>();
            for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) cells.add(new int[]{r, c});
            Collections.shuffle(cells, rnd);
            for (int[] cell : cells) {
                if (t.state() != GameState.IN_PROGRESS) break;
                t.move(t.turn(), cell[0], cell[1]);
                if (t.state() != bruteForce(t.board, n)) mismatches++;
            }
            games++;
        }
        System.out.println("differential fuzz: " + games + " games, mismatches = " + mismatches);
        check(mismatches == 0, "O(1) counters agree with a brute-force scan on every position");

        System.out.println("\n" + passes + " passed, " + fails + " failed");
    }
}
