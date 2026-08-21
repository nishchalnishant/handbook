// Runnable backing for notes/WORKED_EXAMPLES.md
// Every line of output quoted in that file is produced here.
//   javac WorkedExampleProofs.java && java WorkedExampleProofs

import java.util.*;
import java.util.concurrent.*;

public class WorkedExampleProofs {

    // ================= A. BookMyShow: the double-booking proof =================

    enum SeatType {
        REGULAR(100), PREMIUM(250);
        private final double price;
        SeatType(double p) { price = p; }
        double price() { return price; }
    }
    enum BookingStatus { HELD, CONFIRMED, EXPIRED }

    record Movie(String title, int mins) {}
    record Seat(String id, SeatType type) {}

    interface PaymentMethod { boolean pay(double amount); }

    static class Show {
        private final Movie movie;
        private final List<Seat> seats;                     // aggregation: seats outlive the show
        private final Map<String, String> seatToBooking = new HashMap<>();  // composition

        Show(Movie m, List<Seat> s) { movie = m; seats = List.copyOf(s); }

        // BROKEN: check-then-act is not atomic
        boolean holdUnsafe(String seatId, String bookingId) {
            if (seatToBooking.containsKey(seatId)) return false;
            try { Thread.sleep(1); } catch (InterruptedException e) {}  // widen the race window
            seatToBooking.put(seatId, bookingId);
            return true;
        }

        synchronized boolean holdSafe(String seatId, String bookingId) {
            if (seatToBooking.containsKey(seatId)) return false;
            seatToBooking.put(seatId, bookingId);
            return true;
        }
    }

    static int raceForOneSeat(boolean safe) throws Exception {
        Show show = new Show(new Movie("Dune", 155), List.of(new Seat("A1", SeatType.PREMIUM)));
        int threads = 10;
        CountDownLatch start = new CountDownLatch(1);
        Set<String> winners = ConcurrentHashMap.newKeySet();
        ExecutorService pool = Executors.newFixedThreadPool(threads);
        for (int i = 0; i < threads; i++) {
            String user = "user" + i;
            pool.submit(() -> {
                try { start.await(); } catch (InterruptedException e) { return; }
                boolean got = safe ? show.holdSafe("A1", user) : show.holdUnsafe("A1", user);
                if (got) winners.add(user);
            });
        }
        start.countDown();
        pool.shutdown();
        pool.awaitTermination(5, TimeUnit.SECONDS);
        return winners.size();
    }

    // ============ B. Chess: the case where abstract class is correct ============

    enum Colour { WHITE, BLACK }

    record Pos(int row, int col) {
        boolean onBoard() { return row >= 0 && row < 8 && col >= 0 && col < 8; }
    }

    // Cannot be an interface: `pos` is per-object MUTABLE state.
    // `interface Piece { Pos pos; }` does not compile.
    static abstract class Piece {
        protected final Colour colour;
        protected Pos pos;
        protected Piece(Colour c, Pos p) { colour = c; pos = p; }

        void moveTo(Pos p) { this.pos = p; }        // shared behaviour, written ONCE
        abstract boolean canMove(Pos to);           // the ONE thing that differs
        Colour colour() { return colour; }
    }

    static class King extends Piece {
        King(Colour c, Pos p) { super(c, p); }
        boolean canMove(Pos to) {
            if (!to.onBoard()) return false;
            int dr = Math.abs(to.row() - pos.row()), dc = Math.abs(to.col() - pos.col());
            return (dr | dc) != 0 && dr <= 1 && dc <= 1;
        }
    }
    static class Rook extends Piece {
        Rook(Colour c, Pos p) { super(c, p); }
        boolean canMove(Pos to) {
            if (!to.onBoard() || to.equals(pos)) return false;
            return to.row() == pos.row() || to.col() == pos.col();
        }
    }
    static class Bishop extends Piece {
        Bishop(Colour c, Pos p) { super(c, p); }
        boolean canMove(Pos to) {
            if (!to.onBoard() || to.equals(pos)) return false;
            return Math.abs(to.row() - pos.row()) == Math.abs(to.col() - pos.col());
        }
    }

    // ==================== C. Vending Machine: State pattern ====================

    enum Coin {
        FIVE(5), TEN(10);
        private final int value;
        Coin(int v) { value = v; }
        int value() { return value; }
    }
    record Product(String code, String name, int price) {}

    interface VendingState {
        VendingState insert(Machine m, Coin c);
        VendingState select(Machine m, String code);
        VendingState dispense(Machine m);
        String name();
    }

    static class Idle implements VendingState {
        public String name() { return "IDLE"; }
        public VendingState insert(Machine m, Coin c) { m.addCredit(c.value()); return new HasMoney(); }
        public VendingState select(Machine m, String code) { m.log("insert money first"); return this; }
        public VendingState dispense(Machine m) { m.log("nothing selected"); return this; }
    }

    static class HasMoney implements VendingState {
        public String name() { return "HAS_MONEY"; }
        public VendingState insert(Machine m, Coin c) { m.addCredit(c.value()); return this; }
        public VendingState select(Machine m, String code) {
            Product p = m.stock(code);
            if (p == null) { m.log("no such product " + code); return this; }
            if (m.credit() < p.price()) { m.log("need " + (p.price() - m.credit()) + " more"); return this; }
            m.setSelected(p);
            return new Dispensing();
        }
        public VendingState dispense(Machine m) { m.log("select a product first"); return this; }
    }

    static class Dispensing implements VendingState {
        public String name() { return "DISPENSING"; }
        public VendingState insert(Machine m, Coin c) { m.log("busy dispensing"); return this; }
        public VendingState select(Machine m, String code) { m.log("busy dispensing"); return this; }
        public VendingState dispense(Machine m) {
            Product p = m.selected();
            int change = m.credit() - p.price();
            m.log("dispensing " + p.name() + ", change " + change);
            m.reset();
            return new Idle();
        }
    }

    static class Machine {
        private VendingState state = new Idle();
        private int credit;
        private Product selected;
        private final Map<String, Product> stock = new LinkedHashMap<>();

        void stockUp(Product p) { stock.put(p.code(), p); }
        Product stock(String code) { return stock.get(code); }

        // one line each -- no if/else anywhere, ever
        void insert(Coin c)      { state = state.insert(this, c); }
        void select(String code) { state = state.select(this, code); }
        void dispense()          { state = state.dispense(this); }

        void addCredit(int v) { credit += v; }
        int credit() { return credit; }
        void setSelected(Product p) { selected = p; }
        Product selected() { return selected; }
        void reset() { credit = 0; selected = null; }
        String stateName() { return state.name(); }
        void log(String s) { System.out.println("    -> " + s); }
    }

    // ================================= main =================================

    public static void main(String[] args) throws Exception {
        System.out.println("=== A. BookMyShow: 10 threads race for 1 seat ===");
        System.out.println("  unsafe: " + raceForOneSeat(false) + " users got the SAME seat  <-- double booking");
        System.out.println("  safe:   " + raceForOneSeat(true)  + " user got the seat        <-- correct");
        System.out.println("  seat price via enum: PREMIUM = " + SeatType.PREMIUM.price());

        System.out.println("\n=== B. Chess: one call site, three movement rules ===");
        List<Piece> pieces = List.of(
            new King(Colour.WHITE, new Pos(0, 4)),
            new Rook(Colour.WHITE, new Pos(0, 0)),
            new Bishop(Colour.BLACK, new Pos(7, 2)));
        for (Pos target : List.of(new Pos(0, 5), new Pos(0, 7), new Pos(5, 0))) {
            for (Piece p : pieces) {
                System.out.printf("  %-5s %-7s at (%d,%d) -> (%d,%d)? %s%n",
                    p.colour(), p.getClass().getSimpleName(),
                    p.pos.row(), p.pos.col(), target.row(), target.col(),
                    p.canMove(target));   // dynamic dispatch picks the rule
            }
        }
        Piece rook = pieces.get(1);
        rook.moveTo(new Pos(3, 0));       // inherited, defined once in Piece
        System.out.println("  rook moved via INHERITED moveTo -> " + rook.pos);

        System.out.println("\n=== C. Vending Machine: state drives itself ===");
        Machine m = new Machine();
        m.stockUp(new Product("A1", "chips", 15));
        System.out.println("  state=" + m.stateName());
        System.out.println("  select A1");   m.select("A1");
        System.out.println("  insert 10");   m.insert(Coin.TEN);
        System.out.println("  state=" + m.stateName());
        System.out.println("  select A1");   m.select("A1");
        System.out.println("  insert 10");   m.insert(Coin.TEN);
        System.out.println("  select A1");   m.select("A1");
        System.out.println("  state=" + m.stateName());
        System.out.println("  dispense");    m.dispense();
        System.out.println("  state=" + m.stateName() + "  credit=" + m.credit());
    }
}
