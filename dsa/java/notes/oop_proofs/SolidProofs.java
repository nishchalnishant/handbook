// The three principles that were blank in your notes, as runnable code.
//   javac SolidProofs.java && java SolidProofs
// Predict each output before running.

import java.util.*;

// ============ L — Liskov Substitution ============
// A Square IS-A Rectangle in maths, but is NOT substitutable in code.
class Rect {
    protected int w, h;
    void setWidth(int w)  { this.w = w; }
    void setHeight(int h) { this.h = h; }
    int area() { return w * h; }
}
class Sq extends Rect {
    @Override void setWidth(int w)  { this.w = w; this.h = w; }   // invariant: sides equal
    @Override void setHeight(int h) { this.w = h; this.h = h; }
}
// The LSP-respecting design: no inheritance, no breakable setters.
interface Shape2 { int area(); }
record ImmutableRect(int w, int h) implements Shape2 {
    public int area() { return w * h; }
}
record ImmutableSquare(int side) implements Shape2 {
    public int area() { return side * side; }
}

// ============ I — Interface Segregation ============
interface FatWorker { void work(); void eat(); void attendMeeting(); }
class RobotBad implements FatWorker {
    public void work() { System.out.println("    robot works"); }
    public void eat() { throw new UnsupportedOperationException("robots don't eat"); }
    public void attendMeeting() { throw new UnsupportedOperationException("nor meet"); }
}
interface Workable { void work(); }
interface Feedable { void eat(); }
class RobotGood implements Workable {                 // implements ONLY what applies
    public void work() { System.out.println("    robot works, zero dead methods"); }
}
class Human implements Workable, Feedable {
    public void work() { System.out.println("    human works"); }
    public void eat()  { System.out.println("    human eats"); }
}

// ============ D — Dependency Inversion ============
class MySqlDb { void save(String s) { System.out.println("    MySQL saved " + s); } }
class BadService {
    private final MySqlDb db = new MySqlDb();         // welded in: untestable, unswappable
    void register(String u) { db.save(u); }
}
interface Database { void save(String s); }
class MySql implements Database {
    public void save(String s) { System.out.println("    MySQL saved " + s); }
}
class InMemDb implements Database {                   // a test double
    final List<String> rows = new ArrayList<>();
    public void save(String s) { rows.add(s); System.out.println("    in-memory saved " + s); }
}
class GoodService {
    private final Database db;
    GoodService(Database db) { this.db = db; }        // injected: the CALLER decides
    void register(String u) { db.save(u); }
}

public class SolidProofs {

    // a caller written against Rect. Its expectation is entirely reasonable.
    static void resizeAndCheck(String label, Rect r) {
        r.setWidth(5);
        r.setHeight(4);
        System.out.printf("    %-11s expected 20, got %2d %s%n",
            label, r.area(), r.area() == 20 ? "ok" : "<-- LSP VIOLATED");
    }

    public static void main(String[] args) {
        System.out.println("L — Liskov Substitution");
        resizeAndCheck("Rect:", new Rect());
        resizeAndCheck("Square:", new Sq());
        System.out.println("    the type checker was happy. the behaviour was not.");
        System.out.println("    fix — no inheritance, no breakable setters:");
        List<Shape2> shapes = List.of(new ImmutableRect(5, 4), new ImmutableSquare(4));
        for (Shape2 s : shapes) System.out.println("      " + s + " area=" + s.area());

        System.out.println("\nI — Interface Segregation");
        new RobotBad().work();
        try {
            new RobotBad().eat();
        } catch (UnsupportedOperationException e) {
            System.out.println("    forced dead method -> " + e.getMessage());
        }
        System.out.println("    fix — split the fat interface:");
        new RobotGood().work();
        new Human().eat();

        System.out.println("\nD — Dependency Inversion");
        System.out.println("    violated (constructs its own dependency):");
        new BadService().register("alice");
        System.out.println("    fixed (dependency injected):");
        new GoodService(new MySql()).register("bob");
        InMemDb fake = new InMemDb();
        new GoodService(fake).register("carol");
        System.out.println("    same class, fake db, zero edits. test asserts: " + fake.rows);

        System.out.println("""

            Rules of thumb:
              L — if an override throws UnsupportedOperationException, don't inherit
              I — if implementors leave methods empty, the interface is too fat
              D — if you type `new` on a collaborator, make it a constructor param""");
    }
}
