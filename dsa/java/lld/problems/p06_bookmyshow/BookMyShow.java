import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/*
 * Design BookMyShow -- worked solution.
 *
 * SCOPE   Browse shows, hold seats for a TTL window, pay to confirm, cancel with
 *         a refund. The one hard requirement: no double-booking under concurrent
 *         load. Single JVM, in-memory. No real payment gateway, no search, no
 *         seat-map rendering, no pricing tiers.
 *
 * THE DECISION
 *   This is not a class-shape problem. Every candidate produces roughly the same
 *   nouns (Movie, Show, Seat, Booking). The interview is decided entirely by ONE
 *   question: what happens when two people click the same seat at the same
 *   instant?
 *
 *   The wrong answer that looks right:
 *
 *       if (seat.isAvailable()) {          // thread A and B both read "true"
 *           seat.setHeldBy(user);          // both write. Two tickets, one seat.
 *       }
 *
 *   That is check-then-act. It is not fixed by making the fields volatile, and
 *   it is not fixed by using a ConcurrentHashMap -- a thread-safe container does
 *   not make a two-step read-then-write atomic.
 *
 *   The fix is to make claiming a seat a SINGLE atomic operation:
 *   ConcurrentHashMap.putIfAbsent. The map key is the seat, the value is the
 *   hold. Exactly one putIfAbsent can win. There is no window between the check
 *   and the act because there is no check.
 *
 * TTL     A hold expires. Rather than run a sweeper thread, expiry is evaluated
 *         LAZILY at the moment of contention -- an expired hold is displaced by
 *         the next claimant, atomically, via replace(k, expected, new). A
 *         background sweeper is then only a memory optimisation, never a
 *         correctness requirement. That distinction is the point worth making.
 *
 * CLOCK   Time is injected as a Supplier<Long>, not read from
 *         System.currentTimeMillis() inside the logic. Otherwise testing TTL
 *         expiry means Thread.sleep(600_000) and the test is untestable.
 */

enum BookingStatus { PENDING, CONFIRMED, CANCELLED, EXPIRED }

record Movie(String id, String title) {}
record Seat(String showId, String label) {}          // value: identity IS its fields

/** A temporary claim on a seat. Immutable -- expiry replaces it, never mutates it. */
record Hold(String userId, String bookingId, long expiresAtMillis) {
    boolean expiredAt(long now) { return now >= expiresAtMillis; }
}

class Show {
    private final String id;
    private final Movie movie;
    private final long startsAt;
    private final List<Seat> seats = new ArrayList<>();

    Show(String id, Movie movie, long startsAt, int rows, int perRow) {
        this.id = id; this.movie = movie; this.startsAt = startsAt;
        for (char r = 'A'; r < 'A' + rows; r++)
            for (int n = 1; n <= perRow; n++) seats.add(new Seat(id, "" + r + n));
    }
    String id() { return id; }
    Movie movie() { return movie; }
    long startsAt() { return startsAt; }
    List<Seat> seats() { return Collections.unmodifiableList(seats); }
}

class Booking {
    private final String id;
    private final String userId;
    private final List<Seat> seats;
    private final int amountMinor;
    private BookingStatus status = BookingStatus.PENDING;

    Booking(String id, String userId, List<Seat> seats, int amountMinor) {
        this.id = id; this.userId = userId;
        this.seats = List.copyOf(seats); this.amountMinor = amountMinor;
    }
    String id() { return id; }
    String userId() { return userId; }
    List<Seat> seats() { return seats; }
    int amountMinor() { return amountMinor; }
    synchronized BookingStatus status() { return status; }

    /**
     * The state machine, enforced in one place. Returns false rather than
     * throwing for a transition that is merely late (a race the caller lost),
     * because two threads legitimately trying to confirm the same booking is a
     * real scenario, not a programming error.
     */
    synchronized boolean transitionTo(BookingStatus next) {
        boolean legal = switch (status) {
            case PENDING   -> next == BookingStatus.CONFIRMED || next == BookingStatus.CANCELLED
                                                              || next == BookingStatus.EXPIRED;
            case CONFIRMED -> next == BookingStatus.CANCELLED;
            case CANCELLED, EXPIRED -> false;             // terminal
        };
        if (legal) status = next;
        return legal;
    }
}

/** What varies: how much you get back. Interface, injected -- not a switch on a string. */
interface RefundPolicy {
    int refundMinor(int paidMinor, long showStartsAt, long now);
}

/** Full refund > 24h out, half inside 24h, nothing after the show starts. */
class TieredRefundPolicy implements RefundPolicy {
    private static final long DAY = 24L * 60 * 60 * 1000;
    public int refundMinor(int paid, long showStartsAt, long now) {
        if (now >= showStartsAt)            return 0;
        if (showStartsAt - now >= DAY)      return paid;
        return paid / 2;
    }
}

public class BookMyShow {

    private static final long HOLD_TTL_MILLIS = 10 * 60 * 1000L;
    private static final int  PRICE_MINOR     = 25000;          // 250.00

    private final Map<String, Show> shows = new ConcurrentHashMap<>();

    /** THE critical structure. seat -> current hold. Absence means free. */
    private final ConcurrentHashMap<Seat, Hold> holds = new ConcurrentHashMap<>();

    /** seat -> booking id, once money has changed hands. Confirmed is forever. */
    private final ConcurrentHashMap<Seat, String> sold = new ConcurrentHashMap<>();

    private final Map<String, Booking> bookings = new ConcurrentHashMap<>();
    private final java.util.function.Supplier<Long> clock;
    private final RefundPolicy refundPolicy;
    private final AtomicLong ids = new AtomicLong();

    BookMyShow(java.util.function.Supplier<Long> clock, RefundPolicy refundPolicy) {
        this.clock = clock; this.refundPolicy = refundPolicy;
    }

    void addShow(Show s) { shows.put(s.id(), s); }
    List<Show> showsFor(String movieId) {
        return shows.values().stream().filter(s -> s.movie().id().equals(movieId)).toList();
    }

    /**
     * Claim one seat atomically. This is the whole interview.
     *
     * Returns true iff THIS caller now owns the hold. No check-then-act: the
     * decision and the mutation are the same operation.
     */
    private boolean claim(Seat seat, Hold mine) {
        if (sold.containsKey(seat)) return false;      // sold is terminal, safe to read first

        Hold existing = holds.putIfAbsent(seat, mine);
        if (existing == null) return true;             // free -> won it

        // Occupied. Only displaceable if the incumbent has expired -- and the
        // displacement itself must be atomic, or two threads both observe the
        // same stale hold and both replace it. replace(k, expected, new) is the
        // compare-and-swap that closes that window.
        if (existing.expiredAt(clock.get())) return holds.replace(seat, existing, mine);
        return false;
    }

    /**
     * Hold seats for a user. ALL-OR-NOTHING: a booking for 3 seats that gets 2
     * is worse than useless, so partial success is rolled back.
     */
    Optional<Booking> holdSeats(String userId, List<Seat> wanted) {
        if (wanted.isEmpty()) throw new IllegalArgumentException("no seats requested");
        String bookingId = "B" + ids.incrementAndGet();
        Hold mine = new Hold(userId, bookingId, clock.get() + HOLD_TTL_MILLIS);

        List<Seat> got = new ArrayList<>();
        for (Seat s : wanted) {
            if (claim(s, mine)) got.add(s);
            else {
                // Release only the holds WE took. remove(k, v) so we can never
                // delete someone else's hold that landed on this seat since.
                for (Seat r : got) holds.remove(r, mine);
                return Optional.empty();
            }
        }
        Booking b = new Booking(bookingId, userId, got, PRICE_MINOR * got.size());
        bookings.put(bookingId, b);
        return Optional.of(b);
    }

    /** Pay and finalize. Re-verifies the hold: TTL may have elapsed while paying. */
    boolean confirm(String bookingId) {
        Booking b = bookings.get(bookingId);
        if (b == null) return false;
        long now = clock.get();

        // Re-verify EVERY seat before taking money. The hold could have expired
        // and been taken by someone else during the payment round trip.
        for (Seat s : b.seats()) {
            Hold h = holds.get(s);
            if (h == null || !h.bookingId().equals(bookingId) || h.expiredAt(now)) {
                b.transitionTo(BookingStatus.EXPIRED);
                return false;
            }
        }
        if (!b.transitionTo(BookingStatus.CONFIRMED)) return false;
        for (Seat s : b.seats()) { sold.put(s, bookingId); holds.remove(s); }
        return true;
    }

    /** Cancel, returning the refund in minor units. Frees the seats either way. */
    int cancel(String bookingId) {
        Booking b = bookings.get(bookingId);
        if (b == null) return 0;
        boolean wasConfirmed = b.status() == BookingStatus.CONFIRMED;
        if (!b.transitionTo(BookingStatus.CANCELLED)) return 0;   // already terminal

        for (Seat s : b.seats()) { holds.remove(s); sold.remove(s, bookingId); }
        if (!wasConfirmed) return 0;                              // never paid, nothing to refund
        Show show = shows.get(b.seats().get(0).showId());
        return refundPolicy.refundMinor(b.amountMinor(), show.startsAt(), clock.get());
    }

    boolean isAvailable(Seat s) {
        if (sold.containsKey(s)) return false;
        Hold h = holds.get(s);
        return h == null || h.expiredAt(clock.get());
    }

    /** Memory hygiene only -- correctness never depends on this running. */
    int sweepExpired() {
        long now = clock.get();
        int[] n = {0};
        holds.forEach((seat, h) -> { if (h.expiredAt(now) && holds.remove(seat, h)) n[0]++; });
        return n[0];
    }

    // ------------------------------------------------------------------
    private static int passes = 0, fails = 0;
    private static void check(boolean ok, String what) {
        System.out.println((ok ? "PASS  " : "FAIL  ") + what);
        if (ok) passes++; else fails++;
    }

    public static void main(String[] args) throws Exception {
        AtomicLong now = new AtomicLong(1_000_000L);
        long showTime = now.get() + 72L * 3600 * 1000;            // 3 days out

        java.util.function.Supplier<BookMyShow> fresh = () -> {
            BookMyShow sys = new BookMyShow(now::get, new TieredRefundPolicy());
            sys.addShow(new Show("S1", new Movie("M1", "Dune"), showTime, 3, 5));
            return sys;
        };

        BookMyShow sys = fresh.get();
        Show s1 = sys.shows.get("S1");
        check(s1.seats().size() == 15, "show has 15 seats (3 rows x 5)");
        check(sys.showsFor("M1").size() == 1, "browse shows by movie");

        Seat a1 = s1.seats().get(0), a2 = s1.seats().get(1);

        // --- basic hold / confirm
        Booking b = sys.holdSeats("alice", List.of(a1, a2)).orElseThrow();
        check(b.status() == BookingStatus.PENDING, "hold creates a PENDING booking");
        check(!sys.isAvailable(a1), "held seat is not available");
        check(sys.confirm(b.id()), "confirm succeeds inside the TTL");
        check(b.status() == BookingStatus.CONFIRMED, "-> CONFIRMED");
        check(sys.holdSeats("bob", List.of(a1)).isEmpty(), "sold seat cannot be held");

        // --- all-or-nothing
        BookMyShow aon = fresh.get();
        Show s2 = aon.shows.get("S1");
        Seat x = s2.seats().get(0), y = s2.seats().get(1), z = s2.seats().get(2);
        aon.holdSeats("alice", List.of(y)).orElseThrow();
        check(aon.holdSeats("bob", List.of(x, y, z)).isEmpty(), "partial availability -> no booking");
        check(aon.isAvailable(x) && aon.isAvailable(z), "rolled back: bob holds nothing");

        // --- TTL expiry, tested by moving the clock, not by sleeping
        BookMyShow ttl = fresh.get();
        Seat t = ttl.shows.get("S1").seats().get(0);
        ttl.holdSeats("alice", List.of(t)).orElseThrow();
        check(!ttl.isAvailable(t), "held before expiry");
        now.addAndGet(HOLD_TTL_MILLIS + 1);
        check(ttl.isAvailable(t), "available again after TTL elapses");
        Booking bobs = ttl.holdSeats("bob", List.of(t)).orElseThrow();
        check(ttl.confirm(bobs.id()), "bob takes the expired seat");
        now.addAndGet(-(HOLD_TTL_MILLIS + 1));

        // --- confirming after your own hold expired must fail, not steal
        BookMyShow late = fresh.get();
        Seat l = late.shows.get("S1").seats().get(0);
        Booking slow = late.holdSeats("alice", List.of(l)).orElseThrow();
        now.addAndGet(HOLD_TTL_MILLIS + 1);
        check(!late.confirm(slow.id()), "confirm after TTL fails");
        check(slow.status() == BookingStatus.EXPIRED, "-> EXPIRED, not CONFIRMED");
        now.addAndGet(-(HOLD_TTL_MILLIS + 1));

        // --- refunds
        BookMyShow rf = fresh.get();
        Booking far = rf.holdSeats("alice", List.of(rf.shows.get("S1").seats().get(0))).orElseThrow();
        rf.confirm(far.id());
        check(rf.cancel(far.id()) == PRICE_MINOR, "full refund > 24h before the show");
        check(far.status() == BookingStatus.CANCELLED, "-> CANCELLED");
        check(rf.cancel(far.id()) == 0, "double cancel refunds nothing (terminal state)");
        check(rf.isAvailable(rf.shows.get("S1").seats().get(0)), "cancelled seat is resellable");

        BookMyShow near = fresh.get();
        Booking soon = near.holdSeats("bob", List.of(near.shows.get("S1").seats().get(1))).orElseThrow();
        near.confirm(soon.id());
        now.addAndGet(72L * 3600 * 1000 - 3600 * 1000);           // 1h before show
        check(near.cancel(soon.id()) == PRICE_MINOR / 2, "half refund inside 24h");
        now.addAndGet(-(72L * 3600 * 1000 - 3600 * 1000));

        // --- illegal transitions
        BookMyShow st = fresh.get();
        Booking p = st.holdSeats("alice", List.of(st.shows.get("S1").seats().get(0))).orElseThrow();
        st.cancel(p.id());
        check(!st.confirm(p.id()), "cannot confirm a cancelled booking");

        // ==============================================================
        // THE TEST THAT MATTERS: 200 threads, one seat, exactly one winner.
        // ==============================================================
        int threads = 200;
        BookMyShow race = fresh.get();
        Seat contested = race.shows.get("S1").seats().get(0);
        ExecutorService pool = Executors.newFixedThreadPool(32);
        CountDownLatch gun = new CountDownLatch(1);
        AtomicInteger winners = new AtomicInteger(), holders = new AtomicInteger();
        List<Future<?>> fs = new ArrayList<>();
        for (int i = 0; i < threads; i++) {
            final String user = "u" + i;
            fs.add(pool.submit(() -> {
                gun.await();                                       // all block, then go at once
                race.holdSeats(user, List.of(contested)).ifPresent(bk -> {
                    holders.incrementAndGet();                     // won the HOLD
                    if (race.confirm(bk.id())) winners.incrementAndGet();
                });
                return null;
            }));
        }
        gun.countDown();
        for (Future<?> f : fs) f.get();
        pool.shutdown();
        System.out.println("  " + threads + " threads raced for one seat; holders = "
                           + holders.get() + ", confirmed = " + winners.get());
        // Assert on the HOLD, not only the confirmation. confirm() re-verifies
        // ownership, so it masks a broken claim() -- a check-then-act bug still
        // yields one confirmation while several threads wrongly believed they
        // held the seat. Asserting holders == 1 tests the layer that can break.
        check(holders.get() == 1, "exactly one thread wins the HOLD on the contested seat");
        check(winners.get() == 1, "exactly one thread confirms the contested seat");

        // The same race, all-or-nothing across 3 seats: no thread may end up
        // holding a subset, and the total held must be 0 or 3, never 1 or 2.
        BookMyShow race3 = fresh.get();
        List<Seat> trio = race3.shows.get("S1").seats().subList(0, 3);
        ExecutorService pool3 = Executors.newFixedThreadPool(16);
        CountDownLatch gun3 = new CountDownLatch(1);
        AtomicInteger got3 = new AtomicInteger();
        List<Future<?>> f3 = new ArrayList<>();
        for (int i = 0; i < 100; i++) {
            final String user = "v" + i;
            f3.add(pool3.submit(() -> {
                gun3.await();
                race3.holdSeats(user, trio).ifPresent(bk -> got3.incrementAndGet());
                return null;
            }));
        }
        gun3.countDown();
        for (Future<?> f : f3) f.get();
        pool3.shutdown();
        long heldSeats = trio.stream().filter(s -> !race3.isAvailable(s)).count();
        System.out.println("  100 threads raced for the same 3 seats; bookings = " + got3.get()
                           + ", seats held = " + heldSeats);
        check(got3.get() == 1 && heldSeats == 3, "all-or-nothing holds under contention");

        // --- sweeper is an optimisation, not a correctness requirement
        now.addAndGet(HOLD_TTL_MILLIS + 1);
        int swept = race3.sweepExpired();
        System.out.println("  sweeper reclaimed " + swept + " expired hold(s)");
        check(swept == 3, "sweeper frees expired holds it did not need to free");

        System.out.println("\n" + passes + " passed, " + fails + " failed");
    }
}
