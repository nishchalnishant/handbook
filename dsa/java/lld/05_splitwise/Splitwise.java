import java.util.*;

/*
 * SCOPE (Phase 1)
 *   Users, groups, expenses, balances, debt simplification. In-memory,
 *   single currency, single-threaded. Out of scope: auth, payments,
 *   notifications, multi-currency (a follow-up), persistence.
 *
 * THE TWO DECISIONS THIS PROBLEM IS REALLY ABOUT
 *
 *   1. MONEY IS NOT A DOUBLE. 0.1 + 0.2 != 0.3 in binary floating point, and
 *      a cent lost per expense is a bug report. Everything here is a `long`
 *      count of paise (minor units). Formatting to rupees happens only at
 *      the edge, in money().
 *
 *   2. A NET BALANCE PER USER IS NOT ENOUGH. If Alice is -500 you know she
 *      owes 500, but not to WHOM -- and "who do I owe?" is the product's
 *      main screen. So the model is a directed debt graph:
 *          Map<debtor, Map<creditor, amount>>
 *      Net balance is DERIVED from it, never the source of truth.
 *
 * THE DECISION (Phase 3)
 *   User          identity, stable                 -> record
 *   SplitStrategy "EQUAL, EXACT, PERCENTAGE"       -> interface
 *   Expense       value, never mutated after entry -> record
 *   Group         owns members + expenses          -> class
 *   Ledger        owns the debt graph              -> class
 */

record User(String id, String name) {
    public String toString() { return name; }
}

/** Amount in paise. `total` is what the payer actually paid. */
record Expense(String id, User payer, long totalPaise, List<User> participants, String note) {}

// ---------- what varies: how a total becomes per-person shares -> interface ----------
interface SplitStrategy {
    /** Must return a map summing EXACTLY to total. Enforced by the ledger. */
    Map<User, Long> split(long totalPaise, List<User> participants);
    String name();
}

/**
 * Equal split with honest remainder handling. 1000 paise across 3 people is
 * 333.33... -- the extra paise has to go somewhere, so the first `rem` people
 * pay one extra. Sum is exactly the total, always.
 */
class EqualSplit implements SplitStrategy {
    public Map<User, Long> split(long total, List<User> people) {
        Map<User, Long> out = new LinkedHashMap<>();
        int n = people.size();
        long base = total / n, rem = total % n;
        for (int i = 0; i < n; i++)
            out.put(people.get(i), base + (i < rem ? 1 : 0));
        return out;
    }
    public String name() { return "EQUAL"; }
}

class ExactSplit implements SplitStrategy {
    private final Map<User, Long> amounts;
    ExactSplit(Map<User, Long> amounts) { this.amounts = amounts; }
    public Map<User, Long> split(long total, List<User> people) {
        long sum = amounts.values().stream().mapToLong(Long::longValue).sum();
        if (sum != total)
            throw new IllegalArgumentException("exact split sums to " + sum + " not " + total);
        return new LinkedHashMap<>(amounts);
    }
    public String name() { return "EXACT"; }
}

/** Percentages must total 100. The remainder trick appears again. */
class PercentageSplit implements SplitStrategy {
    private final Map<User, Integer> pct;
    PercentageSplit(Map<User, Integer> pct) {
        int sum = pct.values().stream().mapToInt(Integer::intValue).sum();
        if (sum != 100) throw new IllegalArgumentException("percentages sum to " + sum + " not 100");
        this.pct = pct;
    }
    public Map<User, Long> split(long total, List<User> people) {
        Map<User, Long> out = new LinkedHashMap<>();
        long assigned = 0; User last = null;
        for (Map.Entry<User, Integer> e : pct.entrySet()) {
            long share = total * e.getValue() / 100;
            out.put(e.getKey(), share);
            assigned += share; last = e.getKey();
        }
        if (last != null && assigned != total)          // rounding crumbs to the last person
            out.merge(last, total - assigned, Long::sum);
        return out;
    }
    public String name() { return "PERCENTAGE"; }
}

record Transfer(User from, User to, long amountPaise) {
    public String toString() { return from + " -> " + to + " " + Splitwise.money(amountPaise); }
}

/** Owns the debt graph. This class is the heart of the design. */
class Ledger {
    // debtor -> creditor -> amount owed. Never collapsed to a single net number.
    private final Map<User, Map<User, Long>> debts = new LinkedHashMap<>();

    void addExpense(Expense e, SplitStrategy strategy) {
        Map<User, Long> shares = strategy.split(e.totalPaise(), e.participants());

        long sum = shares.values().stream().mapToLong(Long::longValue).sum();
        if (sum != e.totalPaise())                       // invariant, checked every time
            throw new IllegalStateException(
                strategy.name() + " split lost money: " + sum + " != " + e.totalPaise());

        for (Map.Entry<User, Long> s : shares.entrySet()) {
            if (s.getKey().equals(e.payer())) continue;  // the payer owes themselves nothing
            owe(s.getKey(), e.payer(), s.getValue());
        }
    }

    /** debtor owes creditor `amount` more, netting off any debt in the other direction. */
    void owe(User debtor, User creditor, long amount) {
        if (amount <= 0 || debtor.equals(creditor)) return;
        long reverse = amountOwed(creditor, debtor);
        if (reverse > 0) {
            long offset = Math.min(reverse, amount);
            setOwed(creditor, debtor, reverse - offset);
            amount -= offset;
        }
        if (amount > 0) setOwed(debtor, creditor, amountOwed(debtor, creditor) + amount);
    }

    private void setOwed(User d, User c, long v) {
        Map<User, Long> m = debts.computeIfAbsent(d, k -> new LinkedHashMap<>());
        if (v <= 0) m.remove(c); else m.put(c, v);
        if (m.isEmpty()) debts.remove(d);
    }

    long amountOwed(User debtor, User creditor) {
        return debts.getOrDefault(debtor, Map.of()).getOrDefault(creditor, 0L);
    }

    /** The screen a net balance cannot render: who I owe, and who owes me. */
    Map<User, Long> balances(User u) {
        Map<User, Long> out = new LinkedHashMap<>();
        debts.getOrDefault(u, Map.of()).forEach((c, amt) -> out.merge(c, -amt, Long::sum));
        debts.forEach((d, m) -> {
            if (!d.equals(u) && m.containsKey(u)) out.merge(d, m.get(u), Long::sum);
        });
        out.values().removeIf(v -> v == 0);
        return out;
    }

    /** Net position: positive = owed money, negative = owes money. Derived. */
    Map<User, Long> netPositions() {
        Map<User, Long> net = new LinkedHashMap<>();
        debts.forEach((d, m) -> m.forEach((c, amt) -> {
            net.merge(d, -amt, Long::sum);
            net.merge(c,  amt, Long::sum);
        }));
        net.values().removeIf(v -> v == 0);
        return net;
    }

    int edgeCount() {
        return debts.values().stream().mapToInt(Map::size).sum();
    }

    /**
     * Greedy: repeatedly settle the biggest creditor against the biggest debtor.
     * Produces at most n-1 transfers. NOT provably minimal -- finding the true
     * minimum is set-partition, which is NP-hard. Say that out loud; it is the
     * single most impressive sentence available in this problem.
     */
    List<Transfer> simplify() {
        PriorityQueue<Map.Entry<User, Long>> creditors =
            new PriorityQueue<>((a, b) -> Long.compare(b.getValue(), a.getValue()));
        PriorityQueue<Map.Entry<User, Long>> debtors =
            new PriorityQueue<>((a, b) -> Long.compare(a.getValue(), b.getValue()));

        netPositions().forEach((u, v) -> {
            if (v > 0) creditors.add(Map.entry(u, v));
            else if (v < 0) debtors.add(Map.entry(u, v));
        });

        List<Transfer> out = new ArrayList<>();
        while (!creditors.isEmpty() && !debtors.isEmpty()) {
            var c = creditors.poll();
            var d = debtors.poll();
            long amount = Math.min(c.getValue(), -d.getValue());
            out.add(new Transfer(d.getKey(), c.getKey(), amount));

            long cLeft = c.getValue() - amount, dLeft = d.getValue() + amount;
            if (cLeft > 0) creditors.add(Map.entry(c.getKey(), cLeft));
            if (dLeft < 0) debtors.add(Map.entry(d.getKey(), dLeft));
        }
        return out;
    }
}

public class Splitwise {

    static String money(long paise) {
        return String.format("%d.%02d", paise / 100, Math.abs(paise % 100));
    }

    public static void main(String[] args) {
        User alice = new User("u1", "Alice"), bob = new User("u2", "Bob"), carol = new User("u3", "Carol");
        List<User> three = List.of(alice, bob, carol);

        // ---- why long, not double
        System.out.println("0.1 + 0.2 == 0.3 ? " + (0.1 + 0.2 == 0.3));
        System.out.println((0.1 + 0.2 != 0.3) ? "PASS  money is long paise, not double" : "FAIL");

        // ---- remainder distribution: 1000 paise / 3 people
        Map<User, Long> eq = new EqualSplit().split(1000, three);
        long sum = eq.values().stream().mapToLong(Long::longValue).sum();
        System.out.println("split 1000 three ways -> " + eq + " sum=" + sum);
        System.out.println(sum == 1000 && eq.get(alice) == 334 && eq.get(bob) == 333
            ? "PASS  remainder given to the first participant, nothing lost"
            : "FAIL  remainder handling");

        // ---- percentage split also loses nothing
        Map<User, Long> pc = new PercentageSplit(
            new LinkedHashMap<>(Map.of(alice, 33, bob, 33, carol, 34))).split(1000, three);
        long psum = pc.values().stream().mapToLong(Long::longValue).sum();
        System.out.println(psum == 1000 ? "PASS  percentage split sums exactly" : "FAIL  percentage");

        // ---- balances answer "whom do I owe", which a net number cannot
        Ledger led = new Ledger();
        led.addExpense(new Expense("e1", alice, 3000, three, "dinner"), new EqualSplit());
        System.out.println("after dinner, Bob's balances: " + led.balances(bob));
        System.out.println(led.amountOwed(bob, alice) == 1000
            ? "PASS  Bob owes Alice 10.00 specifically" : "FAIL  debt graph");

        // ---- the 3-person cycle: 3 edges collapse to 0 transfers
        Ledger cyc = new Ledger();
        cyc.owe(alice, bob, 1000);
        cyc.owe(bob, carol, 1000);
        cyc.owe(carol, alice, 1000);
        int before = cyc.edgeCount();
        List<Transfer> settle = cyc.simplify();
        System.out.println("3-person cycle: " + before + " edges -> " + settle.size() + " transfers");
        System.out.println(before == 3 && settle.isEmpty()
            ? "PASS  cycle cancels completely" : "FAIL  simplify");

        // ---- a real settle-up, and the money must balance
        Ledger g = new Ledger();
        g.addExpense(new Expense("e1", alice, 6000, three, "hotel"),  new EqualSplit());
        g.addExpense(new Expense("e2", bob,   3000, three, "petrol"), new EqualSplit());
        g.addExpense(new Expense("e3", carol, 1500, three, "snacks"), new EqualSplit());

        Map<User, Long> net = g.netPositions();
        List<Transfer> plan = g.simplify();
        System.out.println("net positions: " + net);
        plan.forEach(t -> System.out.println("  settle: " + t));

        long netSum = net.values().stream().mapToLong(Long::longValue).sum();
        System.out.println(netSum == 0 ? "PASS  net positions sum to zero" : "FAIL  money leaked");
        System.out.println(plan.size() <= three.size() - 1
            ? "PASS  at most n-1 transfers (" + plan.size() + " <= 2)" : "FAIL  too many transfers");

        // applying the plan must zero everyone out
        Map<User, Long> after = new LinkedHashMap<>(net);
        for (Transfer t : plan) {
            after.merge(t.from(),  t.amountPaise(), Long::sum);
            after.merge(t.to(),   -t.amountPaise(), Long::sum);
        }
        boolean settled = after.values().stream().allMatch(v -> v == 0);
        System.out.println(settled ? "PASS  applying the plan settles everyone to zero"
                                   : "FAIL  plan does not settle: " + after);

        // ---- a bad exact split is refused rather than silently losing money
        try {
            new Ledger().addExpense(new Expense("bad", alice, 1000, three, "x"),
                new ExactSplit(new LinkedHashMap<>(Map.of(alice, 300L, bob, 300L, carol, 300L))));
            System.out.println("FAIL  should have rejected a split summing to 900");
        } catch (IllegalArgumentException ok) {
            System.out.println("PASS  refuses a split that does not sum to the total");
        }
    }
}
