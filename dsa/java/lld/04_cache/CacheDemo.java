import java.util.*;

/*
 * SCOPE (Phase 1)
 *   Fixed-capacity in-memory cache, single-threaded. get and put BOTH O(1).
 *   Out of scope: persistence, distribution, serialization.
 *
 * WHY A DOUBLY LINKED LIST (the question the README says to answer out loud)
 *   Eviction needs to remove a node from the MIDDLE of the recency order in
 *   O(1). To unlink a node you must reach its predecessor. A singly linked
 *   list can only find the predecessor by walking from the head -- O(n), which
 *   destroys the whole point. Storing a `prev` pointer is what buys O(1).
 *
 * THE DECISION (Phase 3)
 *   Node            mutable pointers                 -> class (not record)
 *   EvictionPolicy  "at least LRU, LFU, FIFO"        -> interface
 *   Cache<K,V>      owns map + list                  -> class
 */

/** Which key should die next. The cache owns storage; the policy owns order. */
interface EvictionPolicy<K> {
    void recordAccess(K key);   // a get or an overwriting put
    void recordInsert(K key);   // a brand-new key
    void remove(K key);
    K evictionCandidate();      // null when nothing is tracked
    String name();
}

/** Recency order via HashMap + doubly linked list. Every operation O(1). */
class LruPolicy<K> implements EvictionPolicy<K> {
    private static final class Node<K> { K key; Node<K> prev, next; Node(K k){key=k;} }

    private final Map<K, Node<K>> index = new HashMap<>();
    private final Node<K> head = new Node<>(null);   // sentinels remove all the
    private final Node<K> tail = new Node<>(null);   // null-checking from unlink

    LruPolicy() { head.next = tail; tail.prev = head; }

    private void unlink(Node<K> n) { n.prev.next = n.next; n.next.prev = n.prev; }
    private void pushFront(Node<K> n) {
        n.next = head.next; n.prev = head;
        head.next.prev = n; head.next = n;
    }

    public void recordAccess(K key) {
        Node<K> n = index.get(key);
        if (n == null) { recordInsert(key); return; }
        unlink(n); pushFront(n);                     // most recent -> front
    }
    public void recordInsert(K key) {
        Node<K> n = new Node<>(key);
        index.put(key, n); pushFront(n);
    }
    public void remove(K key) {
        Node<K> n = index.remove(key);
        if (n != null) unlink(n);
    }
    public K evictionCandidate() {
        return tail.prev == head ? null : tail.prev.key;   // least recent
    }
    public String name() { return "LruPolicy"; }
}

/** Insertion order, ignoring reads. */
class FifoPolicy<K> implements EvictionPolicy<K> {
    private final LinkedHashSet<K> order = new LinkedHashSet<>();
    public void recordAccess(K key) { /* FIFO deliberately ignores reads */ }
    public void recordInsert(K key) { order.add(key); }
    public void remove(K key)       { order.remove(key); }
    public K evictionCandidate()    { return order.isEmpty() ? null : order.iterator().next(); }
    public String name()            { return "FifoPolicy"; }
}

/** Fewest hits wins. Ties broken by insertion order. */
class LfuPolicy<K> implements EvictionPolicy<K> {
    private final Map<K, Integer> freq = new HashMap<>();
    private final LinkedHashSet<K> order = new LinkedHashSet<>();
    public void recordAccess(K key) { freq.merge(key, 1, Integer::sum); }
    public void recordInsert(K key) { freq.put(key, 1); order.add(key); }
    public void remove(K key)       { freq.remove(key); order.remove(key); }
    public K evictionCandidate() {
        K worst = null; int best = Integer.MAX_VALUE;
        for (K k : order) {                       // order gives a stable tiebreak
            int f = freq.getOrDefault(k, 0);
            if (f < best) { best = f; worst = k; }
        }
        return worst;
    }
    public String name() { return "LfuPolicy"; }
}

class Cache<K, V> {
    private final int capacity;
    private final Map<K, V> store = new HashMap<>();
    private final EvictionPolicy<K> policy;      // injected -> swappable

    Cache(int capacity, EvictionPolicy<K> policy) {
        if (capacity <= 0) throw new IllegalArgumentException("capacity must be > 0");
        this.capacity = capacity;
        this.policy = policy;
    }

    V get(K key) {
        V v = store.get(key);
        if (v != null) policy.recordAccess(key);
        return v;                                 // null when absent
    }

    void put(K key, V value) {
        if (store.containsKey(key)) {
            store.put(key, value);
            policy.recordAccess(key);
            return;
        }
        if (store.size() >= capacity) {
            K victim = policy.evictionCandidate();
            if (victim != null) { store.remove(victim); policy.remove(victim); }
        }
        store.put(key, value);
        policy.recordInsert(key);
    }

    int size() { return store.size(); }
    boolean containsKey(K k) { return store.containsKey(k); }
}

public class CacheDemo {

    public static void main(String[] args) {
        // ---- the classic LRU trace
        Cache<String,Integer> lru = new Cache<>(2, new LruPolicy<>());
        lru.put("a", 1); lru.put("b", 2);
        lru.get("a");                 // 'a' is now the most recent, so 'b' dies
        lru.put("c", 3);
        System.out.println("LruPolicy  a=" + lru.get("a") + " b=" + lru.get("b") + " c=" + lru.get("c"));
        System.out.println(lru.get("a") == 1 && lru.get("b") == null && lru.get("c") == 3
            ? "PASS  LRU evicted the least recently USED" : "FAIL  LRU");

        // ---- same trace, FIFO: reads do not save you
        Cache<String,Integer> fifo = new Cache<>(2, new FifoPolicy<>());
        fifo.put("a", 1); fifo.put("b", 2);
        fifo.get("a");                // ignored by FIFO -> 'a' still dies first
        fifo.put("c", 3);
        System.out.println("FifoPolicy a=" + fifo.get("a") + " b=" + fifo.get("b") + " c=" + fifo.get("c"));
        System.out.println(fifo.get("a") == null && fifo.get("b") == 2 && fifo.get("c") == 3
            ? "PASS  FIFO ignored the read, as designed" : "FAIL  FIFO");

        // ---- LFU keeps the popular key
        Cache<String,Integer> lfu = new Cache<>(2, new LfuPolicy<>());
        lfu.put("a", 1); lfu.put("b", 2);
        lfu.get("a"); lfu.get("a"); lfu.get("a");
        lfu.put("c", 3);
        System.out.println(lfu.get("a") == 1 && lfu.get("b") == null
            ? "PASS  LFU kept the frequently used key" : "FAIL  LFU");

        // ---- differential test: 200 random ops against LinkedHashMap access-order
        int mismatches = differentialTest(200, 8, 12345L);
        System.out.println("differential test, 200 ops: mismatches = " + mismatches);
        System.out.println(mismatches == 0 ? "PASS  agrees with LinkedHashMap reference"
                                           : "FAIL  diverged from reference");

        // ---- capacity is never exceeded
        Cache<Integer,Integer> cap = new Cache<>(8, new LruPolicy<>());
        int max = 0;
        for (int i = 0; i < 500; i++) { cap.put(i, i); max = Math.max(max, cap.size()); }
        System.out.println("max size observed: " + max + " (capacity 8)");
        System.out.println(max == 8 ? "PASS  capacity respected" : "FAIL  capacity exceeded");

        try {
            new Cache<String,String>(0, new LruPolicy<>());
            System.out.println("FAIL  should reject capacity 0");
        } catch (IllegalArgumentException ok) {
            System.out.println("PASS  rejects capacity 0");
        }
    }

    /**
     * The real proof. LinkedHashMap with accessOrder=true and removeEldestEntry
     * IS an LRU cache -- so run the same random operations through both and
     * require identical answers on every single get.
     */
    private static int differentialTest(int ops, int capacity, long seed) {
        Cache<Integer,Integer> mine = new Cache<>(capacity, new LruPolicy<>());

        LinkedHashMap<Integer,Integer> ref =
            new LinkedHashMap<>(16, 0.75f, true) {
                protected boolean removeEldestEntry(Map.Entry<Integer,Integer> e) {
                    return size() > capacity;
                }
            };

        Random rnd = new Random(seed);
        int mismatches = 0;
        for (int i = 0; i < ops; i++) {
            int key = rnd.nextInt(12);
            if (rnd.nextBoolean()) {
                int val = rnd.nextInt(1000);
                mine.put(key, val);
                ref.put(key, val);
            } else {
                Integer a = mine.get(key), b = ref.get(key);
                if (!Objects.equals(a, b)) mismatches++;
            }
            if (mine.size() != ref.size()) mismatches++;
        }
        return mismatches;
    }
}
