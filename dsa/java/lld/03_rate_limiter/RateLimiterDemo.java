import java.util.*;
import java.util.function.LongSupplier;

/*
 * SCOPE (Phase 1)
 *   In-process, per-client rate limiting. One JVM. Out of scope: distributed
 *   coordination, persistence, per-endpoint tiers (covered as a follow-up).
 *
 * THE ONE TRICK THAT MATTERS
 *   Time is INJECTED as a LongSupplier, never read from System.currentTimeMillis()
 *   inside the algorithm. That is the difference between a test suite that runs
 *   in 3 milliseconds and one that sleeps for 30 seconds. Everything below is
 *   tested with a fake clock and there is not one Thread.sleep in this file.
 *
 * API (Phase 4)
 *   interface RateLimiter { boolean allow(String clientId); }
 *   three implementations, identical call site -> strategy pattern
 */

interface RateLimiter {
    boolean allow(String clientId);
}

/** Test double: time only moves when you say so. */
final class FakeClock implements LongSupplier {
    private long now;
    FakeClock(long start) { now = start; }
    public long getAsLong() { return now; }
    void advance(long ms)   { now += ms; }
}

// ---------- 1. fixed window: cheapest, but bursty at the boundary ----------
class FixedWindow implements RateLimiter {
    private final int limit;
    private final long windowMs;
    private final LongSupplier clock;
    private final Map<String, long[]> state = new HashMap<>();  // [windowStart, count]

    FixedWindow(int limit, long windowMs, LongSupplier clock) {
        this.limit = limit; this.windowMs = windowMs; this.clock = clock;
    }

    public boolean allow(String id) {
        long now = clock.getAsLong();
        long window = now / windowMs;
        long[] s = state.computeIfAbsent(id, k -> new long[]{window, 0});
        if (s[0] != window) { s[0] = window; s[1] = 0; }   // new window -> reset
        if (s[1] < limit) { s[1]++; return true; }
        return false;
    }
}

// ---------- 2. sliding log: exact, but stores every timestamp ----------
class SlidingWindowLog implements RateLimiter {
    private final int limit;
    private final long windowMs;
    private final LongSupplier clock;
    private final Map<String, Deque<Long>> log = new HashMap<>();

    SlidingWindowLog(int limit, long windowMs, LongSupplier clock) {
        this.limit = limit; this.windowMs = windowMs; this.clock = clock;
    }

    public boolean allow(String id) {
        long now = clock.getAsLong();
        Deque<Long> q = log.computeIfAbsent(id, k -> new ArrayDeque<>());
        while (!q.isEmpty() && q.peekFirst() <= now - windowMs) q.pollFirst();  // evict
        if (q.size() < limit) { q.addLast(now); return true; }
        return false;
    }
}

// ---------- 3. token bucket: allows bursts, smooths the average ----------
class TokenBucket implements RateLimiter {
    private final double capacity, refillPerMs;
    private final LongSupplier clock;
    private final Map<String, double[]> state = new HashMap<>();  // [tokens, lastRefillMs]

    TokenBucket(double capacity, double refillPerSecond, LongSupplier clock) {
        this.capacity = capacity;
        this.refillPerMs = refillPerSecond / 1000.0;
        this.clock = clock;
    }

    public boolean allow(String id) {
        long now = clock.getAsLong();
        double[] s = state.computeIfAbsent(id, k -> new double[]{capacity, now});
        // LAZY refill: we do not run a timer, we compute what would have accrued.
        double elapsed = now - s[1];
        s[0] = Math.min(capacity, s[0] + elapsed * refillPerMs);
        s[1] = now;
        if (s[0] >= 1.0) { s[0] -= 1.0; return true; }
        return false;
    }
}

public class RateLimiterDemo {

    private static String burst(RateLimiter rl, String id, int n) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) sb.append(rl.allow(id) ? 'Y' : 'n');
        return sb.toString();
    }

    private static void check(String label, String got, String want) {
        System.out.println((got.equals(want) ? "PASS  " : "FAIL  ") + label
                           + "  got=" + got + " want=" + want);
    }

    public static void main(String[] args) {
        // ---- fixed window: 3 per 1000ms
        FakeClock c1 = new FakeClock(0);
        RateLimiter fw = new FixedWindow(3, 1000, c1);
        check("fixed  burst of 5", burst(fw, "u1", 5), "YYYnn");
        c1.advance(1000);
        check("fixed  after window rolls", burst(fw, "u1", 2), "YY");

        // ---- sliding log: 3 per 1000ms, exact
        FakeClock c2 = new FakeClock(0);
        RateLimiter sl = new SlidingWindowLog(3, 1000, c2);
        check("sliding burst of 5", burst(sl, "u1", 5), "YYYnn");
        c2.advance(999);
        check("sliding still blocked at 999ms", burst(sl, "u1", 1), "n");
        c2.advance(1);
        check("sliding opens at exactly 1000ms", burst(sl, "u1", 3), "YYY");

        // ---- token bucket: capacity 5, refill 2/sec
        FakeClock c3 = new FakeClock(0);
        RateLimiter tb = new TokenBucket(5, 2, c3);
        check("bucket burst of 7", burst(tb, "u1", 7), "YYYYYnn");
        c3.advance(500);                       // 500ms * 2/sec = 1 token
        check("bucket after +500ms", burst(tb, "u1", 2), "Yn");

        // ---- clients are isolated from each other
        FakeClock c4 = new FakeClock(0);
        RateLimiter iso = new FixedWindow(2, 1000, c4);
        String a = burst(iso, "alice", 3), b = burst(iso, "bob", 3);
        check("per-client isolation (alice)", a, "YYn");
        check("per-client isolation (bob)",   b, "YYn");

        // ---- the boundary burst: why fixed window is the weakest of the three
        FakeClock c5 = new FakeClock(900);
        RateLimiter weak = new FixedWindow(3, 1000, c5);
        String before = burst(weak, "u", 3);
        c5.advance(100);                       // crosses into the next window
        String after = burst(weak, "u", 3);
        System.out.println("fixed window boundary: " + before + " then " + after
                           + "  -> 6 requests in 100ms despite a limit of 3/sec");
        System.out.println(before.equals("YYY") && after.equals("YYY")
            ? "PASS  demonstrates the fixed-window boundary flaw"
            : "FAIL  boundary demo");

        // ---- same call site for all three: that is the strategy pattern
        FakeClock c6 = new FakeClock(0);
        List<RateLimiter> all = List.of(
            new FixedWindow(2, 1000, c6),
            new SlidingWindowLog(2, 1000, c6),
            new TokenBucket(2, 1, c6));
        boolean uniform = all.stream().allMatch(r -> burst(r, "x", 3).equals("YYn"));
        System.out.println(uniform ? "PASS  all three agree on 2-then-block"
                                   : "FAIL  implementations disagree");
    }
}
