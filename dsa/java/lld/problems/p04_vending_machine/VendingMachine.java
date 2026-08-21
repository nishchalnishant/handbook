import java.util.*;

/*
 * Design a Vending Machine -- worked solution.
 *
 * SCOPE   Select an item, insert coins, dispense with change, or cancel and get
 *         a full refund. Inventory decrements on success. Single machine,
 *         in-memory, no card payments, no network, no restock scheduling.
 *
 * API     boolean selectItem(String code)
 *         void    insertCoin(Coin c)
 *         Result  dispense()
 *         List<Coin> cancel()
 *
 * THE DECISION
 *   The spec hands you a state machine: IDLE -> ITEM_SELECTED -> HAS_MONEY ->
 *   DISPENSING -> IDLE. Two ways to build it.
 *
 *   (a) enum State + a switch in every method. Adding a state means editing
 *       every switch, and the compiler will not tell you which one you missed.
 *   (b) State pattern: one class per state, each knowing only its own legal
 *       transitions. Adding a state is one new class and zero edits.
 *
 *   This file uses (b), because the whole point of the exercise is that the
 *   illegal transitions become *unrepresentable* rather than checked. You never
 *   write `if (state != HAS_MONEY) throw` -- the IdleState simply has no
 *   working dispense().
 *
 * MONEY   Coins are an enum of fixed denominations in minor units (paise/cents)
 *         held as int. Never double: 0.1 + 0.2 != 0.3, and a vending machine
 *         that loses a cent per sale is a bug that compounds.
 */

enum Coin {
    FIVE(5), TEN(10), TWENTY(20), FIFTY(50);
    private final int value;
    Coin(int v) { value = v; }
    int value() { return value; }
}

record Item(String code, String name, int priceMinor) {
    Item {
        if (priceMinor <= 0) throw new IllegalArgumentException("price must be positive: " + priceMinor);
    }
}

/** What a dispense produced. A record, because it is a value and never mutates. */
record Result(Item item, List<Coin> change) {}

/**
 * One method per user action. Each concrete state implements only the actions
 * that are legal in it, and inherits a loud failure for the rest.
 */
interface MachineState {
    String name();
    default boolean selectItem(VendingMachine m, String code) { throw illegal("selectItem"); }
    default void    insertCoin(VendingMachine m, Coin c)      { throw illegal("insertCoin"); }
    default Result  dispense(VendingMachine m)                { throw illegal("dispense"); }
    default List<Coin> cancel(VendingMachine m)               { throw illegal("cancel"); }
    private IllegalStateException illegal(String action) {
        return new IllegalStateException(action + " is not legal in state " + name());
    }
}

// ---------- what varies #1: the legal transitions -> one class per state ----------

class IdleState implements MachineState {
    public String name() { return "IDLE"; }
    public boolean selectItem(VendingMachine m, String code) {
        Item item = m.inventory().get(code);
        if (item == null || m.stockOf(code) == 0) return false;   // expected outcome, not a bug
        m.setSelected(item);
        m.setState(new ItemSelectedState());
        return true;
    }
    // cancel() in IDLE is a no-op rather than an error: pressing refund with
    // nothing inserted should not blow up a real machine.
    public List<Coin> cancel(VendingMachine m) { return List.of(); }
}

class ItemSelectedState implements MachineState {
    public String name() { return "ITEM_SELECTED"; }
    public void insertCoin(VendingMachine m, Coin c) {
        m.addCoin(c);
        if (m.insertedTotal() >= m.selected().priceMinor()) m.setState(new HasMoneyState());
    }
    public List<Coin> cancel(VendingMachine m) { return m.refundAll(); }
}

class HasMoneyState implements MachineState {
    public String name() { return "HAS_MONEY"; }
    // Still accept coins: a user who keeps feeding coins gets them back as change.
    public void insertCoin(VendingMachine m, Coin c) { m.addCoin(c); }
    public List<Coin> cancel(VendingMachine m) { return m.refundAll(); }

    public Result dispense(VendingMachine m) {
        Item item = m.selected();
        int owed = m.insertedTotal() - item.priceMinor();

        // Make change BEFORE committing anything. If the machine cannot pay the
        // change it must refuse and refund -- dispensing and then failing to pay
        // out is the one outcome a real machine must never produce.
        List<Coin> change = m.makeChange(owed);
        if (change == null) {
            m.refundAll();
            throw new IllegalStateException("cannot make " + owed + " in change; refunded");
        }

        m.commitSale(item, change);
        m.setState(new IdleState());
        return new Result(item, change);
    }
}

public class VendingMachine {

    private final Map<String, Item> inventory = new LinkedHashMap<>();
    private final Map<String, Integer> stock  = new HashMap<>();
    private final Map<Coin, Integer> bank     = new EnumMap<>(Coin.class);   // coins available as change

    private final List<Coin> inserted = new ArrayList<>();
    private Item selected;
    private MachineState state = new IdleState();

    public VendingMachine() { for (Coin c : Coin.values()) bank.put(c, 0); }

    // --- setup
    public void stock(Item item, int qty) {
        inventory.put(item.code(), item);
        stock.merge(item.code(), qty, Integer::sum);
    }
    public void loadChange(Coin c, int qty) { bank.merge(c, qty, Integer::sum); }

    // --- the public API delegates to the current state, and does nothing else.
    // Note there is not a single `if (state == ...)` in this class.
    public boolean selectItem(String code) { return state.selectItem(this, code); }
    public void insertCoin(Coin c)         { state.insertCoin(this, c); }
    public Result dispense()               { return state.dispense(this); }
    public List<Coin> cancel()             { return state.cancel(this); }

    public String stateName() { return state.name(); }
    public int insertedTotal() { return inserted.stream().mapToInt(Coin::value).sum(); }
    public int stockOf(String code) { return stock.getOrDefault(code, 0); }
    public int bankTotal() { return bank.entrySet().stream().mapToInt(e -> e.getKey().value() * e.getValue()).sum(); }

    // --- package-private hooks the states drive
    Map<String, Item> inventory() { return inventory; }
    Item selected()               { return selected; }
    void setSelected(Item i)      { selected = i; }
    void setState(MachineState s) { state = s; }
    void addCoin(Coin c)          { inserted.add(c); }

    List<Coin> refundAll() {
        List<Coin> back = List.copyOf(inserted);
        inserted.clear();
        selected = null;
        state = new IdleState();
        return back;
    }

    /**
     * Greedy change-making over the coins actually IN THE BANK.
     *
     * Greedy is correct here only because these denominations are canonical
     * (5/10/20/50 -- each divides into the next few cleanly). It is NOT correct
     * in general: with {1,3,4}, greedy makes 6 as 4+1+1 (three coins) when 3+3
     * (two) is optimal. Say that out loud; the interviewer is often fishing for
     * exactly this. The general solution is a coin-change DP.
     *
     * @return the coins to pay out, or null if the bank cannot make the amount.
     */
    List<Coin> makeChange(int amount) {
        if (amount < 0) throw new IllegalArgumentException("negative change: " + amount);
        List<Coin> out = new ArrayList<>();
        int remaining = amount;
        List<Coin> desc = new ArrayList<>(List.of(Coin.values()));
        desc.sort(Comparator.comparingInt(Coin::value).reversed());
        for (Coin c : desc) {
            int available = bank.getOrDefault(c, 0);
            while (remaining >= c.value() && available > 0) {
                out.add(c); remaining -= c.value(); available--;
            }
        }
        return remaining == 0 ? out : null;   // null = cannot pay, caller must refund
    }

    /** Commit the sale: only reached once change is known to be payable. */
    void commitSale(Item item, List<Coin> change) {
        for (Coin c : inserted) bank.merge(c, 1, Integer::sum);      // inserted coins join the bank
        for (Coin c : change)   bank.merge(c, -1, Integer::sum);     // change leaves it
        stock.merge(item.code(), -1, Integer::sum);
        inserted.clear();
        selected = null;
    }

    // ------------------------------------------------------------------
    private static int passes = 0, fails = 0;
    private static void check(boolean ok, String what) {
        System.out.println((ok ? "PASS  " : "FAIL  ") + what);
        if (ok) passes++; else fails++;
    }

    private static VendingMachine machine() {
        VendingMachine m = new VendingMachine();
        m.stock(new Item("A1", "Chips", 45), 2);
        m.stock(new Item("A2", "Soda",  50), 1);
        for (Coin c : Coin.values()) m.loadChange(c, 5);
        return m;
    }

    public static void main(String[] args) {
        // --- the happy path, with change
        VendingMachine m = machine();
        check(m.stateName().equals("IDLE"), "starts IDLE");
        check(m.selectItem("A1"), "selecting a stocked item succeeds");
        check(m.stateName().equals("ITEM_SELECTED"), "-> ITEM_SELECTED");
        m.insertCoin(Coin.TWENTY);
        check(m.stateName().equals("ITEM_SELECTED"), "20 < 45, still ITEM_SELECTED");
        m.insertCoin(Coin.FIFTY);
        check(m.stateName().equals("HAS_MONEY"), "70 >= 45, -> HAS_MONEY");

        Result r = m.dispense();
        int changeValue = r.change().stream().mapToInt(Coin::value).sum();
        System.out.println("  bought " + r.item().name() + " for 45, paid 70, change " + r.change() + " = " + changeValue);
        check(changeValue == 25, "change is exactly 70 - 45 = 25");
        check(m.stateName().equals("IDLE"), "returns to IDLE after dispensing");
        check(m.stockOf("A1") == 1, "inventory decremented");

        // --- exact money means no change
        VendingMachine ex = machine();
        ex.selectItem("A2");
        ex.insertCoin(Coin.FIFTY);
        check(ex.dispense().change().isEmpty(), "exact payment yields no change");

        // --- cancel refunds everything, coin for coin
        VendingMachine c = machine();
        c.selectItem("A1");
        c.insertCoin(Coin.TWENTY); c.insertCoin(Coin.TEN);
        List<Coin> back = c.cancel();
        check(back.stream().mapToInt(Coin::value).sum() == 30, "cancel refunds the full 30");
        check(c.stateName().equals("IDLE"), "cancel returns to IDLE");
        check(c.stockOf("A1") == 2, "cancel does not touch inventory");

        // --- out of stock is an expected outcome, not an exception
        VendingMachine s = machine();
        s.selectItem("A2"); s.insertCoin(Coin.FIFTY); s.dispense();
        check(!s.selectItem("A2"), "second attempt on a 1-stock item returns false");
        check(!s.selectItem("ZZ"), "unknown code returns false");

        // --- ILLEGAL TRANSITIONS: this is what the State pattern buys
        VendingMachine i = machine();
        try { i.dispense(); check(false, "should refuse dispense while IDLE"); }
        catch (IllegalStateException ok) { check(true, "dispense in IDLE throws: " + ok.getMessage()); }
        try { i.insertCoin(Coin.TEN); check(false, "should refuse coins while IDLE"); }
        catch (IllegalStateException ok) { check(true, "insertCoin in IDLE throws"); }
        i.selectItem("A1");
        try { i.selectItem("A2"); check(false, "should refuse re-select mid-transaction"); }
        catch (IllegalStateException ok) { check(true, "selectItem in ITEM_SELECTED throws"); }
        try { i.dispense(); check(false, "should refuse dispense before enough money"); }
        catch (IllegalStateException ok) { check(true, "dispense in ITEM_SELECTED throws"); }

        // --- the bank cannot make change: refuse and refund, never half-commit
        VendingMachine poor = new VendingMachine();
        poor.stock(new Item("B1", "Gum", 45), 1);
        poor.loadChange(Coin.FIFTY, 2);          // only 50s: 5 in change is impossible
        poor.selectItem("B1");
        poor.insertCoin(Coin.FIFTY);
        try {
            poor.dispense();
            check(false, "should refuse when change cannot be made");
        } catch (IllegalStateException ok) {
            check(poor.stockOf("B1") == 1 && poor.stateName().equals("IDLE"),
                  "cannot make change -> refunded, stock untouched, back to IDLE");
        }

        // --- money conservation: the machine never invents or loses value
        VendingMachine acct = machine();
        int before = acct.bankTotal();
        acct.selectItem("A1");
        acct.insertCoin(Coin.FIFTY);
        Result rr = acct.dispense();
        int paidOut = rr.change().stream().mapToInt(Coin::value).sum();
        check(acct.bankTotal() == before + 50 - paidOut,
              "bank = before + inserted - change (" + before + " + 50 - " + paidOut + ")");

        // --- greedy change is only correct for canonical denominations
        System.out.println("  NOTE greedy is safe for 5/10/20/50; for {1,3,4} it makes 6 as 4+1+1, not 3+3");

        System.out.println("\n" + passes + " passed, " + fails + " failed");
    }
}
