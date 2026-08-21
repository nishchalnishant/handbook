import java.util.*;
import java.util.concurrent.*;
import java.util.function.LongSupplier;

/**
 * Runnable backing for the five lld/*_/INTERVIEW.md walkthroughs.
 *
 * Every number quoted in those files is printed by this program. If a claim in a
 * walkthrough is not reproduced here, it should not be in the walkthrough.
 *
 *   javac notes/oop_proofs/LldInterviewProofs.java -d /tmp/proofs
 *   java  -cp /tmp/proofs LldInterviewProofs
 *
 * Sections:
 *   1  parking lot   -- find-then-claim race, and the smallest correct lock
 *   2  elevator      -- dispatch strategy swap, TreeSet next-stop-in-direction
 *   3  rate limiter  -- fixed window vs token bucket on an injected fake clock
 *   4  cache         -- LRU vs FIFO behind one EvictionPolicy, + a 200-op oracle
 *   5  splitwise     -- money in paise, remainder distribution, debt graph, simplify
 */
public class LldInterviewProofs {

    // ======================================================================
    // 01 Parking Lot   (lld/01_parking_lot/INTERVIEW.md)
    // ======================================================================
    static class Section1ParkingLot {

        enum VehicleType { BIKE, CAR, TRUCK }
        record Vehicle(String plate, VehicleType type) {}

        static class Spot {
            final int id; final VehicleType fits; volatile Vehicle occupant;
            Spot(int id, VehicleType fits) { this.id = id; this.fits = fits; }
            boolean free() { return occupant == null; }
        }

        static class Lot {
            private final List<Spot> spots;
            private final Object lock = new Object();
            Lot(List<Spot> s) { spots = s; }

            // BROKEN: find-then-claim is two steps
            Spot parkUnsafe(Vehicle v) {
                Spot s = spots.stream().filter(x -> x.free() && x.fits == v.type()).findFirst().orElse(null);
                if (s == null) return null;
                try { Thread.sleep(1); } catch (InterruptedException e) {}
                s.occupant = v;
                return s;
            }

            // CORRECT, and minimal: lock only the find+claim, not the fee maths
            Spot parkSafe(Vehicle v) {
                synchronized (lock) {
                    Spot s = spots.stream().filter(x -> x.free() && x.fits == v.type()).findFirst().orElse(null);
                    if (s != null) s.occupant = v;
                    return s;
                }
            }
        }

        static int distinctCarsOnOneSpot(boolean safe) throws Exception {
            Lot lot = new Lot(new ArrayList<>(List.of(new Spot(1, VehicleType.CAR))));
            int threads = 10;
            CountDownLatch start = new CountDownLatch(1);
            Map<Integer, Set<String>> spotToCars = new ConcurrentHashMap<>();
            ExecutorService pool = Executors.newFixedThreadPool(threads);
            for (int i = 0; i < threads; i++) {
                Vehicle v = new Vehicle("KA-" + i, VehicleType.CAR);
                pool.submit(() -> {
                    try { start.await(); } catch (InterruptedException e) { return; }
                    Spot s = safe ? lot.parkSafe(v) : lot.parkUnsafe(v);
                    if (s != null) spotToCars.computeIfAbsent(s.id, k -> ConcurrentHashMap.newKeySet()).add(v.plate());
                });
            }
            start.countDown();
            pool.shutdown();
            pool.awaitTermination(5, TimeUnit.SECONDS);
            return spotToCars.getOrDefault(1, Set.of()).size();
        }

        public static void main(String[] args) throws Exception {
            System.out.println("=== LLD 01 exercise 5: 10 cars race for 1 spot ===");
            System.out.println("  unsafe: " + distinctCarsOnOneSpot(false) + " cars assigned the SAME spot  <-- broken");
            System.out.println("  safe:   " + distinctCarsOnOneSpot(true)  + " car assigned the spot        <-- correct");
            System.out.println("  smallest correct block = find + claim together (they must be ONE atomic step)");
            System.out.println("  fee calculation stays OUTSIDE the lock -- it touches no shared state");
        }

    }

    // ======================================================================
    // 02 Elevator   (lld/02_elevator/INTERVIEW.md)
    // ======================================================================
    static class Section2Elevator {


        enum Direction { UP, DOWN, IDLE }
        record Request(int floor, Direction dir) {}

        static class Elevator {
            private final int id;
            private int currentFloor;
            private Direction direction = Direction.IDLE;
            private final TreeSet<Integer> stops = new TreeSet<>();   // "next stop in direction" cheaply

            Elevator(int id, int floor) { this.id = id; this.currentFloor = floor; }

            int id() { return id; }
            int floor() { return currentFloor; }
            Direction direction() { return direction; }
            boolean isIdle() { return direction == Direction.IDLE; }
            int distanceTo(int floor) { return Math.abs(currentFloor - floor); }

            void addStop(int floor) {
                stops.add(floor);
                if (direction == Direction.IDLE)
                    direction = floor > currentFloor ? Direction.UP
                              : floor < currentFloor ? Direction.DOWN : Direction.IDLE;
            }

            // TreeSet gives next-stop-in-direction in O(log n)
            Integer nextStop() {
                if (stops.isEmpty()) return null;
                return direction == Direction.DOWN ? stops.floor(currentFloor) != null
                            ? stops.floor(currentFloor) : stops.first()
                     : stops.ceiling(currentFloor) != null ? stops.ceiling(currentFloor) : stops.last();
            }

            void step() {
                Integer target = nextStop();
                if (target == null) { direction = Direction.IDLE; return; }
                if (target > currentFloor) { currentFloor++; direction = Direction.UP; }
                else if (target < currentFloor) { currentFloor--; direction = Direction.DOWN; }
                if (currentFloor == target) {
                    stops.remove(currentFloor);
                    if (stops.isEmpty()) direction = Direction.IDLE;
                }
            }
            boolean hasWork() { return !stops.isEmpty(); }
        }

        // the varying thing -> interface
        interface DispatchStrategy { Elevator pick(List<Elevator> cars, Request r); }

        static class NearestElevator implements DispatchStrategy {
            public Elevator pick(List<Elevator> cars, Request r) {
                return cars.stream()
                    .min(Comparator.<Elevator>comparingInt(e -> e.isIdle() ? 0 : 1)
                                   .thenComparingInt(e -> e.distanceTo(r.floor())))
                    .orElseThrow();
            }
        }
        static class RoundRobin implements DispatchStrategy {
            private int next = 0;
            public Elevator pick(List<Elevator> cars, Request r) {
                Elevator e = cars.get(next % cars.size()); next++; return e;
            }
        }

        static class ElevatorSystem {
            private final List<Elevator> cars;
            private final DispatchStrategy strategy;      // injected -> swapping needs NO edit here
            ElevatorSystem(List<Elevator> cars, DispatchStrategy s) { this.cars = cars; this.strategy = s; }
            void external(Request r) { strategy.pick(cars, r).addStop(r.floor()); }
            void step() { cars.forEach(Elevator::step); }
            boolean allServed() { return cars.stream().noneMatch(Elevator::hasWork); }
            String state() {
                StringBuilder sb = new StringBuilder();
                for (Elevator e : cars) sb.append(String.format("E%d@%d%-4s ", e.id(), e.floor(), e.direction()));
                return sb.toString();
            }
        }

        static int runSim(DispatchStrategy s, boolean print) {
            List<Elevator> cars = List.of(new Elevator(0,0), new Elevator(1,5), new Elevator(2,9));
            ElevatorSystem sys = new ElevatorSystem(new ArrayList<>(cars), s);
            List<Request> reqs = List.of(new Request(3,Direction.UP), new Request(7,Direction.DOWN),
                                         new Request(1,Direction.UP), new Request(9,Direction.DOWN),
                                         new Request(5,Direction.UP));
            reqs.forEach(sys::external);
            int tick = 0;
            while (!sys.allServed() && tick < 30) {
                sys.step(); tick++;
                if (print && tick <= 6) System.out.println("    tick " + tick + ": " + sys.state());
            }
            return tick;
        }

        public static void main(String[] args) {
            System.out.println("=== NearestElevator, 3 cars / 10 floors / 5 requests ===");
            int a = runSim(new NearestElevator(), true);
            System.out.println("  all 5 requests served in " + a + " ticks");

            System.out.println("\n=== RoundRobin, IDENTICAL system, only the strategy swapped ===");
            int b = runSim(new RoundRobin(), true);
            System.out.println("  all 5 requests served in " + b + " ticks");

            System.out.println("\n  nearest=" + a + " ticks, roundrobin=" + b + " ticks"
                + " -> strategy swapped with ZERO edits to Elevator or ElevatorSystem");

            System.out.println("\n=== TreeSet gives next-stop-in-direction ===");
            Elevator e = new Elevator(9, 5);
            e.addStop(8); e.addStop(2); e.addStop(6);
            System.out.println("  at floor 5 going UP, stops {2,6,8} -> next = " + e.nextStop() + " (O(log n) via ceiling)");
        }

    }

    // ======================================================================
    // 03 Rate Limiter + 04 Cache   (lld/03_rate_limiter/INTERVIEW.md, lld/04_cache/INTERVIEW.md)
    // ======================================================================
    static class Section3RateLimiterAndCache {


        // ================= LLD 03: rate limiter, fake clock =================
        interface RateLimiter { boolean allow(String clientId); }

        static class FixedWindow implements RateLimiter {
            private final int limit; private final long windowMs; private final LongSupplier now;
            private final Map<String, long[]> state = new HashMap<>();   // [windowStart, count]
            FixedWindow(int limit, long windowMs, LongSupplier now) {
                this.limit = limit; this.windowMs = windowMs; this.now = now;
            }
            public boolean allow(String id) {
                long t = now.getAsLong();
                long[] s = state.computeIfAbsent(id, k -> new long[]{t, 0});
                if (t - s[0] >= windowMs) { s[0] = t; s[1] = 0; }
                if (s[1] < limit) { s[1]++; return true; }
                return false;
            }
        }

        static class TokenBucket implements RateLimiter {
            private final long capacity; private final double refillPerMs; private final LongSupplier now;
            private final Map<String, double[]> state = new HashMap<>();  // [tokens, lastRefillMs]
            TokenBucket(long capacity, double refillPerMs, LongSupplier now) {
                this.capacity = capacity; this.refillPerMs = refillPerMs; this.now = now;
            }
            public boolean allow(String id) {
                long t = now.getAsLong();
                double[] s = state.computeIfAbsent(id, k -> new double[]{capacity, t});
                s[0] = Math.min(capacity, s[0] + (t - s[1]) * refillPerMs);
                s[1] = t;
                if (s[0] >= 1) { s[0] -= 1; return true; }
                return false;
            }
        }

        // ================= LLD 04: cache, eviction as interface =================
        interface EvictionPolicy<K> {
            void recordAccess(K key);
            void recordInsert(K key);
            void remove(K key);
            K evictCandidate();
        }

        // LRU via doubly linked list -> O(1) touch and evict
        static class LruPolicy<K> implements EvictionPolicy<K> {
            private static class Node<K> { K key; Node<K> prev, next; Node(K k){key=k;} }
            private final Map<K, Node<K>> nodes = new HashMap<>();
            private Node<K> head, tail;                       // head = most recent
            private void unlink(Node<K> n) {
                if (n.prev != null) n.prev.next = n.next; else head = n.next;
                if (n.next != null) n.next.prev = n.prev; else tail = n.prev;
                n.prev = n.next = null;
            }
            private void pushFront(Node<K> n) {
                n.next = head; if (head != null) head.prev = n; head = n;
                if (tail == null) tail = n;
            }
            public void recordAccess(K key) {
                Node<K> n = nodes.get(key);
                if (n != null) { unlink(n); pushFront(n); }
            }
            public void recordInsert(K key) {
                Node<K> n = new Node<>(key); nodes.put(key, n); pushFront(n);
            }
            public void remove(K key) {
                Node<K> n = nodes.remove(key); if (n != null) unlink(n);
            }
            public K evictCandidate() { return tail == null ? null : tail.key; }
        }

        static class FifoPolicy<K> implements EvictionPolicy<K> {
            private final LinkedHashSet<K> order = new LinkedHashSet<>();
            public void recordAccess(K key) { }                // FIFO ignores access
            public void recordInsert(K key) { order.add(key); }
            public void remove(K key) { order.remove(key); }
            public K evictCandidate() { return order.isEmpty() ? null : order.iterator().next(); }
        }

        static class Cache<K, V> {
            private final int capacity;
            private final Map<K, V> map = new HashMap<>();
            private final EvictionPolicy<K> policy;           // DIP: injected
            Cache(int capacity, EvictionPolicy<K> policy) { this.capacity = capacity; this.policy = policy; }
            V get(K key) {
                if (!map.containsKey(key)) return null;
                policy.recordAccess(key);
                return map.get(key);
            }
            void put(K key, V value) {
                if (map.containsKey(key)) { map.put(key, value); policy.recordAccess(key); return; }
                if (map.size() >= capacity) {
                    K victim = policy.evictCandidate();
                    map.remove(victim); policy.remove(victim);
                }
                map.put(key, value); policy.recordInsert(key);
            }
            int size() { return map.size(); }
        }

        public static void main(String[] args) {
            // ---- rate limiter with a FAKE clock, zero Thread.sleep ----
            long[] clock = {1000};
            LongSupplier now = () -> clock[0];

            System.out.println("=== FixedWindow: 3 per 1000ms, fake clock ===");
            RateLimiter fw = new FixedWindow(3, 1000, now);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < 5; i++) sb.append(fw.allow("c1") ? "Y" : "n");
            System.out.println("  burst of 5 -> " + sb + "   (3 allowed, then blocked)");
            clock[0] += 1000;
            System.out.println("  after clock +1000ms -> " + (fw.allow("c1") ? "Y allowed again" : "n"));

            System.out.println("\n=== TokenBucket: capacity 3, refill 1 per 500ms ===");
            clock[0] = 1000;
            RateLimiter tb = new TokenBucket(3, 1.0/500, now);
            sb = new StringBuilder();
            for (int i = 0; i < 5; i++) sb.append(tb.allow("c1") ? "Y" : "n");
            System.out.println("  burst of 5 -> " + sb + "   (burst up to capacity)");
            clock[0] += 500;
            System.out.println("  after +500ms (1 token) -> " + (tb.allow("c1") ? "Y" : "n")
                             + (tb.allow("c1") ? "Y" : "n") + "   (exactly one refilled)");
            System.out.println("  identical call site for both -> strategy pattern");

            // ---- cache: same call site, two policies, different victims ----
            System.out.println("\n=== Cache capacity 2, LRU vs FIFO, IDENTICAL operations ===");
            for (EvictionPolicy<String> p : List.of(new LruPolicy<String>(), new FifoPolicy<String>())) {
                Cache<String,Integer> c = new Cache<>(2, p);
                c.put("a",1); c.put("b",2);
                c.get("a");                 // touch a -- only LRU cares
                c.put("c",3);               // evicts something
                System.out.printf("  %-11s after put a,b / get a / put c -> a=%s b=%s c=%s%n",
                    p.getClass().getSimpleName(), c.get("a"), c.get("b"), c.get("c"));
            }
            System.out.println("  LRU kept 'a' (recently used), FIFO evicted 'a' (oldest) -> policy swapped, cache untouched");

            // ---- capacity never exceeded, 200 random ops vs reference ----
            System.out.println("\n=== 200 random ops: capacity invariant + LinkedHashMap reference ===");
            Cache<Integer,Integer> mine = new Cache<>(8, new LruPolicy<Integer>());
            LinkedHashMap<Integer,Integer> ref = new LinkedHashMap<>(16, 0.75f, true) {
                protected boolean removeEldestEntry(Map.Entry<Integer,Integer> e) { return size() > 8; }
            };
            Random r = new Random(42);
            int mismatches = 0, maxSize = 0;
            for (int i = 0; i < 200; i++) {
                int k = r.nextInt(12);
                if (r.nextBoolean()) { mine.put(k, i); ref.put(k, i); }
                else {
                    Integer a = mine.get(k), b = ref.get(k);
                    if (!Objects.equals(a, b)) mismatches++;
                }
                maxSize = Math.max(maxSize, mine.size());
            }
            System.out.println("  mismatches vs LinkedHashMap access-order: " + mismatches);
            System.out.println("  max size observed: " + maxSize + " (capacity 8) -> never exceeded");
        }

    }

    // ======================================================================
    // 05 Splitwise   (lld/05_splitwise/INTERVIEW.md)
    // ======================================================================
    static class Section5Splitwise {


        // ---- claim 1: why long paise, not double ----
        static void moneyClaim() {
            System.out.println("  0.1 + 0.2 == 0.3 ? " + (0.1 + 0.2 == 0.3));
            System.out.println("  0.1 + 0.2         = " + (0.1 + 0.2));
            System.out.println("  1000/3 as double x3 = " + (1000.0/3 * 3));
            long each = 1000 / 3, rem = 1000 % 3;
            System.out.println("  1000 paise / 3 -> each=" + each + " remainder=" + rem);
        }

        // ---- claim 2: EQUAL split must distribute the remainder ----
        interface SplitStrategy { Map<String,Long> split(long totalPaise, List<String> people, List<Long> args); }

        static class EqualSplit implements SplitStrategy {
            public Map<String,Long> split(long total, List<String> people, List<Long> ignored) {
                Map<String,Long> out = new LinkedHashMap<>();
                long n = people.size(), base = total / n, rem = total % n;
                for (int i = 0; i < n; i++)
                    out.put(people.get(i), base + (i < rem ? 1 : 0));  // first `rem` pay 1 extra
                return out;
            }
        }
        static class ExactSplit implements SplitStrategy {
            public Map<String,Long> split(long total, List<String> people, List<Long> amounts) {
                long sum = amounts.stream().mapToLong(Long::longValue).sum();
                if (sum != total) throw new IllegalArgumentException("exact amounts must sum to total");
                Map<String,Long> out = new LinkedHashMap<>();
                for (int i = 0; i < people.size(); i++) out.put(people.get(i), amounts.get(i));
                return out;
            }
        }
        static class PercentageSplit implements SplitStrategy {
            public Map<String,Long> split(long total, List<String> people, List<Long> pcts) {
                long sum = pcts.stream().mapToLong(Long::longValue).sum();
                if (sum != 100) throw new IllegalArgumentException("percentages must sum to 100");
                Map<String,Long> out = new LinkedHashMap<>();
                long assigned = 0;
                for (int i = 0; i < people.size(); i++) {
                    long share = (i == people.size()-1) ? total - assigned : total * pcts.get(i) / 100;
                    out.put(people.get(i), share);
                    assigned += share;
                }
                return out;
            }
        }

        // ---- claim 3: the debt graph, not a net number ----
        static class DebtGraph {
            private final Map<String, Map<String, Long>> owes = new HashMap<>();
            void add(String debtor, String creditor, long paise) {
                if (debtor.equals(creditor)) return;
                owes.computeIfAbsent(debtor, k -> new HashMap<>()).merge(creditor, paise, Long::sum);
            }
            Map<String, Long> net() {
                Map<String, Long> net = new TreeMap<>();
                owes.forEach((d, m) -> m.forEach((c, amt) -> {
                    net.merge(d, -amt, Long::sum);
                    net.merge(c,  amt, Long::sum);
                }));
                return net;
            }
            int edgeCount() { return owes.values().stream().mapToInt(Map::size).sum(); }
        }

        record Transfer(String from, String to, long paise) {}

        // greedy: largest debtor pays largest creditor, repeat
        static List<Transfer> simplify(Map<String, Long> net) {
            PriorityQueue<Map.Entry<String,Long>> creditors =
                new PriorityQueue<>((a,b) -> Long.compare(b.getValue(), a.getValue()));
            PriorityQueue<Map.Entry<String,Long>> debtors =
                new PriorityQueue<>(Comparator.comparingLong(Map.Entry::getValue));
            net.forEach((p, v) -> {
                if (v > 0) creditors.add(Map.entry(p, v));
                else if (v < 0) debtors.add(Map.entry(p, v));
            });
            List<Transfer> out = new ArrayList<>();
            while (!creditors.isEmpty() && !debtors.isEmpty()) {
                var c = creditors.poll(); var d = debtors.poll();
                long amt = Math.min(c.getValue(), -d.getValue());
                out.add(new Transfer(d.getKey(), c.getKey(), amt));
                long cLeft = c.getValue() - amt, dLeft = d.getValue() + amt;
                if (cLeft > 0) creditors.add(Map.entry(c.getKey(), cLeft));
                if (dLeft < 0) debtors.add(Map.entry(d.getKey(), dLeft));
            }
            return out;
        }

        public static void main(String[] args) {
            System.out.println("=== money ===");
            moneyClaim();

            System.out.println("\n=== EQUAL split of 1000 paise 3 ways (remainder) ===");
            var eq = new EqualSplit().split(1000, List.of("a","b","c"), List.of());
            System.out.println("  " + eq + "  sum=" + eq.values().stream().mapToLong(Long::longValue).sum());

            System.out.println("\n=== PERCENTAGE split 1000 paise 33/33/34 ===");
            var pc = new PercentageSplit().split(1000, List.of("a","b","c"), List.of(33L,33L,34L));
            System.out.println("  " + pc + "  sum=" + pc.values().stream().mapToLong(Long::longValue).sum());

            System.out.println("\n=== EXACT split rejects bad input ===");
            try { new ExactSplit().split(1000, List.of("a","b"), List.of(400L, 500L)); }
            catch (IllegalArgumentException e) { System.out.println("  rejected: " + e.getMessage()); }

            System.out.println("\n=== 3-person cycle: a->b 500, b->c 500, c->a 500 ===");
            DebtGraph g = new DebtGraph();
            g.add("a","b",500); g.add("b","c",500); g.add("c","a",500);
            System.out.println("  edges before simplify: " + g.edgeCount());
            var net = g.net();
            System.out.println("  net: " + net);
            var tx = simplify(net);
            System.out.println("  transfers after simplify: " + tx.size() + " -> " + tx);
            System.out.println("  net sums to zero? " + (net.values().stream().mapToLong(Long::longValue).sum() == 0));

            System.out.println("\n=== why net-per-user loses information ===");
            DebtGraph g2 = new DebtGraph();
            g2.add("x","y",300);
            DebtGraph g3 = new DebtGraph();
            g3.add("x","z",300);
            System.out.println("  x owes y 300 -> net " + g2.net());
            System.out.println("  x owes z 300 -> net " + g3.net());
            System.out.println("  same net for x, DIFFERENT creditor -> net alone cannot answer 'whom do I owe'");
        }

    }

    public static void main(String[] args) throws Exception {
        System.out.println("##################################################################");
        System.out.println("# SECTION 1 -- 01 Parking Lot");
        System.out.println("##################################################################");
        Section1ParkingLot.main(args);

        System.out.println();
        System.out.println("##################################################################");
        System.out.println("# SECTION 2 -- 02 Elevator");
        System.out.println("##################################################################");
        Section2Elevator.main(args);

        System.out.println();
        System.out.println("##################################################################");
        System.out.println("# SECTIONS 3 & 4 -- 03 Rate Limiter and 04 Cache");
        System.out.println("##################################################################");
        Section3RateLimiterAndCache.main(args);

        System.out.println();
        System.out.println("##################################################################");
        System.out.println("# SECTION 5 -- 05 Splitwise");
        System.out.println("##################################################################");
        Section5Splitwise.main(args);
    }
}
