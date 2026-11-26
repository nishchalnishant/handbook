import java.util.*;

/*
 * Design Chess -- worked solution.
 *
 * SCOPE   Two players alternate, White first. Every piece enforces its own moves.
 *         A move that leaves your own king in check is illegal. Detect check,
 *         checkmate and stalemate. No clock, no notation parsing, no AI, no
 *         castling / en passant / promotion (see Phase 6 -- the omission is
 *         deliberate and I say so out loud rather than hoping nobody notices).
 *
 * THE DECISION -- this is the one problem where ABSTRACT CLASS beats interface.
 *
 *   Run the tree from notes/TEXT_TO_CODE.md on "different types of pieces":
 *     Q1 differ only by data?           No -- a knight and a bishop differ by
 *                                       BEHAVIOUR, not by a number.
 *     Q2 share mutable state?           YES. Every piece has a colour and a
 *                                       hasMoved flag, stored once in the parent.
 *                                       An interface cannot hold per-object state:
 *                                       `interface P { int x; }` silently becomes
 *                                       public static final -- a shared constant.
 *   -> abstract class Piece. Stop.
 *
 *   So: `abstract class Piece` holds colour + hasMoved and implements the shared
 *   sliding logic; each subclass supplies only what actually differs. Knight and
 *   King share "offsets"; Bishop/Rook/Queen share "slide until blocked". That
 *   sharing is real code reuse, not a hierarchy built for its own sake.
 *
 * THE SEPARATION THAT MAKES CHECK TRACTABLE
 *   Two distinct notions, and conflating them is THE classic chess bug:
 *     pseudoLegal -- does this piece move like that, and is the target not my own?
 *     legal       -- pseudoLegal AND it does not leave MY king attacked.
 *   Check detection needs pseudoLegal only. If `legal` called itself to test
 *   check, you get infinite recursion. Keeping them separate is what stops that.
 */

enum Colour {
    WHITE, BLACK;
    Colour other() { return this == WHITE ? BLACK : WHITE; }
}

enum GameState { IN_PROGRESS, WHITE_WINS, BLACK_WINS, STALEMATE }

/** A square. Pure value -> record. */
record Square(int row, int col) {
    Square {
        if (row < 0 || row > 7 || col < 0 || col > 7)
            throw new IllegalArgumentException("off board: " + row + "," + col);
    }
    static boolean onBoard(int r, int c) { return r >= 0 && r < 8 && c >= 0 && c < 8; }
    /** "e4" -> row 4, col 4. Files a-h are columns, ranks 1-8 count from White. */
    static Square of(String algebraic) {
        return new Square(algebraic.charAt(1) - '1', algebraic.charAt(0) - 'a');
    }
    public String toString() { return "" + (char)('a' + col) + (char)('1' + row); }
}

// ---------- what varies: how each piece moves -> abstract class + subclasses ----------

abstract class Piece {
    protected final Colour colour;      // SHARED STATE -- the reason this is not an interface
    protected boolean hasMoved;

    protected Piece(Colour c) { colour = c; }
    Colour colour() { return colour; }
    boolean hasMoved() { return hasMoved; }
    void markMoved() { hasMoved = true; }
    abstract char symbol();             // uppercase = White, by convention
    abstract List<Square> pseudoLegalMoves(Board b, Square from);

    /** Shared by Bishop, Rook, Queen: slide along a direction until blocked. */
    protected List<Square> slide(Board b, Square from, int[][] dirs) {
        List<Square> out = new ArrayList<>();
        for (int[] d : dirs) {
            int r = from.row() + d[0], c = from.col() + d[1];
            while (Square.onBoard(r, c)) {
                Piece p = b.at(r, c);
                if (p == null) out.add(new Square(r, c));
                else {
                    if (p.colour() != colour) out.add(new Square(r, c));   // capture
                    break;                                                 // blocked either way
                }
                r += d[0]; c += d[1];
            }
        }
        return out;
    }

    /** Shared by Knight and King: fixed offsets, one step. */
    protected List<Square> step(Board b, Square from, int[][] offsets) {
        List<Square> out = new ArrayList<>();
        for (int[] d : offsets) {
            int r = from.row() + d[0], c = from.col() + d[1];
            if (!Square.onBoard(r, c)) continue;
            Piece p = b.at(r, c);
            if (p == null || p.colour() != colour) out.add(new Square(r, c));
        }
        return out;
    }
    public String toString() {
        return colour == Colour.WHITE ? "" + symbol() : "" + Character.toLowerCase(symbol());
    }
}

class King extends Piece {
    private static final int[][] D = {{1,0},{-1,0},{0,1},{0,-1},{1,1},{1,-1},{-1,1},{-1,-1}};
    King(Colour c) { super(c); }
    char symbol() { return 'K'; }
    List<Square> pseudoLegalMoves(Board b, Square f) { return step(b, f, D); }
}

class Queen extends Piece {
    private static final int[][] D = {{1,0},{-1,0},{0,1},{0,-1},{1,1},{1,-1},{-1,1},{-1,-1}};
    Queen(Colour c) { super(c); }
    char symbol() { return 'Q'; }
    List<Square> pseudoLegalMoves(Board b, Square f) { return slide(b, f, D); }
}

class Rook extends Piece {
    private static final int[][] D = {{1,0},{-1,0},{0,1},{0,-1}};
    Rook(Colour c) { super(c); }
    char symbol() { return 'R'; }
    List<Square> pseudoLegalMoves(Board b, Square f) { return slide(b, f, D); }
}

class Bishop extends Piece {
    private static final int[][] D = {{1,1},{1,-1},{-1,1},{-1,-1}};
    Bishop(Colour c) { super(c); }
    char symbol() { return 'B'; }
    List<Square> pseudoLegalMoves(Board b, Square f) { return slide(b, f, D); }
}

class Knight extends Piece {
    private static final int[][] D = {{2,1},{2,-1},{-2,1},{-2,-1},{1,2},{1,-2},{-1,2},{-1,-2}};
    Knight(Colour c) { super(c); }
    char symbol() { return 'N'; }
    List<Square> pseudoLegalMoves(Board b, Square f) { return step(b, f, D); }
}

/**
 * The awkward one. Pawns are the reason chess is not elegant: they move one way,
 * capture another, get a double-step from home, and promote. Not a "kind of
 * slider" -- their own subclass, with no shared helper. Forcing a pawn into a
 * generic movement abstraction is the classic over-engineering trap here.
 */
class Pawn extends Piece {
    Pawn(Colour c) { super(c); }
    char symbol() { return 'P'; }
    List<Square> pseudoLegalMoves(Board b, Square f) {
        List<Square> out = new ArrayList<>();
        int dir = (colour == Colour.WHITE) ? 1 : -1;
        int r = f.row() + dir, c = f.col();

        if (Square.onBoard(r, c) && b.at(r, c) == null) {
            out.add(new Square(r, c));                       // one forward, only if empty
            int home = (colour == Colour.WHITE) ? 1 : 6;
            int rr = f.row() + 2 * dir;
            if (f.row() == home && b.at(rr, c) == null) out.add(new Square(rr, c));
        }
        for (int dc : new int[]{-1, 1}) {                    // captures: diagonal ONLY
            int cc = c + dc;
            if (!Square.onBoard(r, cc)) continue;
            Piece p = b.at(r, cc);
            if (p != null && p.colour() != colour) out.add(new Square(r, cc));
        }
        return out;
    }
}

class Board {
    private final Piece[][] grid = new Piece[8][8];

    Piece at(int r, int c) { return Square.onBoard(r, c) ? grid[r][c] : null; }
    Piece at(Square s)     { return grid[s.row()][s.col()]; }
    void put(Square s, Piece p) { grid[s.row()][s.col()] = p; }
    void put(String alg, Piece p) { put(Square.of(alg), p); }

    /**
     * Fluent placement, so a test position can be built as a single expression
     * and handed to Chess already complete. See the comment on the Chess
     * constructor: a game object that must be mutated after construction to
     * become valid is a game object whose state is stale from birth.
     */
    Board with(String alg, Piece p) { put(alg, p); return this; }

    Board copy() {
        Board b = new Board();
        for (int r = 0; r < 8; r++) System.arraycopy(grid[r], 0, b.grid[r], 0, 8);
        return b;
    }

    static Board standard() {
        Board b = new Board();
        for (int c = 0; c < 8; c++) {
            b.put(new Square(1, c), new Pawn(Colour.WHITE));
            b.put(new Square(6, c), new Pawn(Colour.BLACK));
        }
        String back = "RNBQKBNR";
        for (int c = 0; c < 8; c++) {
            b.put(new Square(0, c), make(back.charAt(c), Colour.WHITE));
            b.put(new Square(7, c), make(back.charAt(c), Colour.BLACK));
        }
        return b;
    }

    /** Factory: one place decides which concrete class to build. */
    static Piece make(char sym, Colour c) {
        return switch (Character.toUpperCase(sym)) {
            case 'K' -> new King(c);   case 'Q' -> new Queen(c);
            case 'R' -> new Rook(c);   case 'B' -> new Bishop(c);
            case 'N' -> new Knight(c); case 'P' -> new Pawn(c);
            default  -> throw new IllegalArgumentException("unknown piece: " + sym);
        };
    }

    Square findKing(Colour c) {
        for (int r = 0; r < 8; r++)
            for (int col = 0; col < 8; col++) {
                Piece p = grid[r][col];
                if (p instanceof King && p.colour() == c) return new Square(r, col);
            }
        return null;
    }

    /**
     * Is `target` attacked by `by`? Uses PSEUDO-legal moves deliberately: a
     * pinned piece still gives check, and asking for legality here would recurse
     * forever (legal -> isAttacked -> legal -> ...).
     */
    boolean isAttacked(Square target, Colour by) {
        for (int r = 0; r < 8; r++)
            for (int c = 0; c < 8; c++) {
                Piece p = grid[r][c];
                if (p == null || p.colour() != by) continue;
                if (p.pseudoLegalMoves(this, new Square(r, c)).contains(target)) return true;
            }
        return false;
    }
}

public class Chess {

    private final Board board;
    private Colour turn = Colour.WHITE;
    private GameState state = GameState.IN_PROGRESS;

    Chess() { this(Board.standard(), Colour.WHITE); }

    /**
     * The board must be COMPLETE before it gets here. recomputeState() runs now,
     * so handing in an empty board and placing pieces afterwards latches
     * STALEMATE (no legal moves, no king) and every later move is refused by the
     * game-over guard. Build the position with Board.with(...) first.
     *
     * I hit exactly this bug writing the tests below. It is not a test slip --
     * it is the API inviting misuse, so the API is what I changed.
     */
    Chess(Board b, Colour toMove) {
        if (b.findKing(Colour.WHITE) == null || b.findKing(Colour.BLACK) == null)
            throw new IllegalArgumentException("position must contain both kings");
        board = b; turn = toMove; recomputeState();
    }

    Board board() { return board; }
    Colour turn() { return turn; }
    GameState state() { return state; }

    boolean inCheck(Colour c) {
        Square k = board.findKing(c);
        return k != null && board.isAttacked(k, c.other());
    }

    /** Every move that is pseudo-legal AND does not leave your own king attacked. */
    List<Square> legalMoves(Square from) {
        Piece p = board.at(from);
        if (p == null || p.colour() != turn) return List.of();
        List<Square> out = new ArrayList<>();
        for (Square to : p.pseudoLegalMoves(board, from)) {
            Board after = board.copy();
            after.put(to, p);
            after.put(from, null);
            Square k = after.findKing(p.colour());
            if (k == null || !after.isAttacked(k, p.colour().other())) out.add(to);
        }
        return out;
    }

    List<Square[]> allLegalMoves(Colour c) {
        List<Square[]> out = new ArrayList<>();
        for (int r = 0; r < 8; r++)
            for (int col = 0; col < 8; col++) {
                Square from = new Square(r, col);
                Piece p = board.at(from);
                if (p == null || p.colour() != c) continue;
                for (Square to : legalMoves(from)) out.add(new Square[]{from, to});
            }
        return out;
    }

    boolean move(String fromAlg, String toAlg) { return move(Square.of(fromAlg), Square.of(toAlg)); }

    boolean move(Square from, Square to) {
        if (state != GameState.IN_PROGRESS) return false;
        if (!legalMoves(from).contains(to)) return false;
        Piece p = board.at(from);
        board.put(to, p);
        board.put(from, null);
        p.markMoved();
        turn = turn.other();
        recomputeState();
        return true;
    }

    /**
     * Checkmate and stalemate are the SAME test -- "no legal moves" -- separated
     * only by whether the king is currently attacked. Writing them as one
     * condition with a branch is the insight; writing two independent searches
     * is the mistake.
     */
    private void recomputeState() {
        if (!allLegalMoves(turn).isEmpty()) { state = GameState.IN_PROGRESS; return; }
        if (inCheck(turn)) state = (turn == Colour.WHITE) ? GameState.BLACK_WINS : GameState.WHITE_WINS;
        else state = GameState.STALEMATE;
    }

    /**
     * perft: count leaf nodes of the legal-move tree to depth n. This is the
     * standard ground truth in chess programming -- the numbers for the opening
     * position are published and universally agreed, so it is a DIFFERENTIAL
     * TEST against the entire world rather than against my own assumptions.
     */
    long perft(int depth) {
        if (depth == 0) return 1;
        long nodes = 0;
        for (Square[] mv : allLegalMoves(turn)) {
            Board snapshot = board.copy();
            Colour saved = turn;
            GameState savedState = state;
            Piece moved = board.at(mv[0]);
            boolean savedHasMoved = moved.hasMoved();

            board.put(mv[1], moved);
            board.put(mv[0], null);
            turn = turn.other();
            nodes += perft(depth - 1);

            for (int r = 0; r < 8; r++)
                for (int c = 0; c < 8; c++) board.put(new Square(r, c), snapshot.at(r, c));
            turn = saved; state = savedState;
            if (!savedHasMoved) moved.hasMoved = false;
        }
        return nodes;
    }

    // ------------------------------------------------------------------
    private static int passes = 0, fails = 0;
    private static void check(boolean ok, String what) {
        System.out.println((ok ? "PASS  " : "FAIL  ") + what);
        if (ok) passes++; else fails++;
    }

    public static void main(String[] args) {
        Chess g = new Chess();
        check(g.turn() == Colour.WHITE, "White moves first");
        check(g.state() == GameState.IN_PROGRESS, "opening position is in progress");
        check(g.allLegalMoves(Colour.WHITE).size() == 20, "20 legal opening moves (16 pawn + 4 knight)");

        // --- basic movement rules
        check(g.move("e2", "e4"), "e2-e4 is legal");
        check(g.turn() == Colour.BLACK, "turn alternates");
        check(!g.move("e7", "e4"), "black pawn cannot jump to an occupied square");
        check(g.move("e7", "e5"), "e7-e5 is legal");
        check(!g.move("e4", "e5"), "pawn cannot capture straight ahead");
        check(!g.move("d1", "d3"), "queen cannot move through her own pawn");
        check(g.move("g1", "f3"), "knight jumps over pawns");

        // --- you cannot move your opponent's pieces or leave your king in check
        Chess pin = new Chess(new Board()
                .with("e1", new King(Colour.WHITE))
                .with("e2", new Bishop(Colour.WHITE))
                .with("e8", new Rook(Colour.BLACK))
                .with("a8", new King(Colour.BLACK)), Colour.WHITE);
        check(pin.legalMoves(Square.of("e2")).isEmpty(),
              "absolutely pinned bishop has zero legal moves");
        check(!pin.inCheck(Colour.WHITE), "pinned-but-blocking: White is not yet in check");

        // --- FOOL'S MATE: the shortest checkmate in chess. Known result.
        Chess fool = new Chess();
        fool.move("f2", "f3"); fool.move("e7", "e5");
        fool.move("g2", "g4"); 
        check(fool.move("d8", "h4"), "Qd8-h4 delivers Fool's Mate");
        check(fool.inCheck(Colour.WHITE), "White is in check");
        check(fool.state() == GameState.BLACK_WINS, "Fool's Mate = checkmate in 2, Black wins");
        check(fool.allLegalMoves(Colour.WHITE).isEmpty(), "checkmated side has no legal move");
        check(!fool.move("e1", "f2"), "no moves accepted after game over");

        // --- BACK-RANK MATE: rook mates a king boxed in by its own pawns
        Chess back = new Chess(new Board()
                .with("g1", new King(Colour.WHITE))
                .with("f2", new Pawn(Colour.WHITE))
                .with("g2", new Pawn(Colour.WHITE))
                .with("h2", new Pawn(Colour.WHITE))
                .with("a8", new King(Colour.BLACK))
                .with("d8", new Rook(Colour.BLACK)), Colour.BLACK);
        check(back.move("d8", "d1"), "Rd8-d1 delivers back-rank mate");
        check(back.state() == GameState.BLACK_WINS, "back-rank mate detected");

        // --- STALEMATE: not in check, but no legal move exists. Classic position.
        Chess stale = new Chess(new Board()
                .with("h8", new King(Colour.BLACK))
                .with("f7", new King(Colour.WHITE))
                .with("g6", new Queen(Colour.WHITE)), Colour.BLACK);
        check(!stale.inCheck(Colour.BLACK), "Black king is NOT in check");
        check(stale.allLegalMoves(Colour.BLACK).isEmpty(), "...but has no legal move");
        check(stale.state() == GameState.STALEMATE, "-> STALEMATE, a draw, not a loss");

        // --- check that is escapable is not mate
        Chess esc = new Chess(new Board()
                .with("e1", new King(Colour.WHITE))
                .with("e8", new Rook(Colour.BLACK))
                .with("a8", new King(Colour.BLACK)), Colour.WHITE);
        check(esc.inCheck(Colour.WHITE), "White is in check from the rook");
        check(esc.state() == GameState.IN_PROGRESS, "escapable check is NOT checkmate");
        check(!esc.legalMoves(Square.of("e1")).contains(Square.of("e2")),
              "king may not step along the checking file");
        check(esc.legalMoves(Square.of("e1")).contains(Square.of("d1")),
              "king may step off the file");

        // ==============================================================
        // PERFT: the published ground truth for the opening position.
        // These numbers are agreed worldwide, so this is a differential test
        // against every chess engine ever written, not against my own opinion.
        // Depth 3 = 8902 given no castling/en-passant/promotion is reachable
        // in the first three plies -- which is why this validation is honest
        // despite those omissions.
        // ==============================================================
        // --- the constructor invariant that this file's own tests violated
        try {
            new Chess(new Board(), Colour.WHITE);
            check(false, "empty board should be rejected");
        } catch (IllegalArgumentException ok) {
            check(true, "constructor rejects a position with no kings: " + ok.getMessage());
        }

        long[] expected = {1, 20, 400, 8902};
        for (int d = 1; d <= 3; d++) {
            long t0 = System.currentTimeMillis();
            long n = new Chess().perft(d);
            long ms = System.currentTimeMillis() - t0;
            System.out.println("  perft(" + d + ") = " + n + "  expected " + expected[d]
                               + "  [" + ms + " ms]");
            check(n == expected[d], "perft(" + d + ") matches the published node count");
        }

        System.out.println("\n" + passes + " passed, " + fails + " failed");
    }
}
