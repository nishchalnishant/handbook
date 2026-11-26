// Every claim in validating_CORRECTED.md, as runnable code.
//   javac OopProofs.java && java OopProofs
// Predict each output BEFORE running. Wrong predictions are the useful part.

// ---------- 1. abstract classes force only the abstract methods ----------
abstract class Shape {
    protected String name;
    Shape(String name) { this.name = name; }        // abstract classes CAN have constructors
    abstract double area();                          // a hole: subclass MUST fill this
    void describe() {                                // concrete: inherited for free
        System.out.printf("%s area=%.4f%n", name, area());
    }
}
class Circle extends Shape {
    private final double r;
    Circle(double r) { super("circle"); this.r = r; }
    @Override double area() { return Math.PI * r * r; }
    // describe() never written here, yet it works
}

// ---------- 2. one extends, many implements ----------
interface Walker { default void move() { System.out.println("  walking (default method)"); } }
interface Swimmer { void swim(); }
abstract class Creature { protected String id = "creature"; }
class Duck extends Creature implements Walker, Swimmer {
    @Override public void swim() { System.out.println("  swimming"); }
}
// class Bad extends Creature, Duck {}   // uncomment: syntax error. only ONE parent.

// ---------- 5. overriding is dynamic dispatch ----------
class Super {
    void greet()  { System.out.println("  SUPER greet"); }
    void caller() { System.out.print("  Super.caller() calls greet() -> "); greet(); }
}
class Sub extends Super {
    @Override void greet() { System.out.println("SUB greet"); }
}

// ---------- super.method() ----------
class Base { void hi() { System.out.println("  base hi"); } }
class Derived extends Base {
    @Override void hi() {
        super.hi();                                  // the ONLY route to the parent version
        System.out.println("  derived hi");
    }
}

// ---------- encapsulation enforcing an invariant ----------
class Account {
    private double balance;                          // private: no outside scribbling
    void deposit(double amt) {
        if (amt <= 0) throw new IllegalArgumentException("must be positive");
        balance += amt;
    }
    double getBalance() { return balance; }
}

public class OopProofs {

    // ---------- 4. overloading is resolved at COMPILE time ----------
    static void f(Object o) { System.out.println("  f(Object)"); }
    static void f(String s) { System.out.println("  f(String)"); }
    // static long f(int x)  and  static int f(int x)  would collide:
    // return type alone cannot distinguish overloads.

    public static void main(String[] args) {
        System.out.println("1. abstract: only abstract methods are forced");
        new Circle(1).describe();          // describe() inherited, area() supplied
        // new Shape("x");                 // uncomment: "Shape is abstract; cannot be instantiated"

        System.out.println("\n2. one extends + many implements");
        Duck d = new Duck();
        d.move();                          // from the Walker default method
        d.swim();

        System.out.println("\n3. encapsulation enforces the invariant");
        Account acc = new Account();
        acc.deposit(100);
        try {
            acc.deposit(-50);
            System.out.println("  FAIL: negative deposit accepted");
        } catch (IllegalArgumentException e) {
            System.out.println("  blocked: " + e.getMessage());
        }
        System.out.println("  balance stayed valid: " + acc.getBalance());

        System.out.println("\n4. OVERLOADING -> compile time, DECLARED type");
        Object x = "I am really a String";
        f(x);                              // predict:
        f((String) x);                     // predict:

        System.out.println("\n5. OVERRIDING -> run time, ACTUAL object  (the big one)");
        Super ref = new Sub();             // declared Super, actually a Sub
        System.out.print("  ref.greet()  -> "); ref.greet();      // predict:
        ref.caller();                                             // predict:
        System.out.print("  new Super().greet() -> "); new Super().greet();

        System.out.println("\n6. super.method() reaches the parent");
        new Derived().hi();

        System.out.println("""

            The rule:
              overloading -> compile time, chosen by DECLARED type
              overriding  -> run time,     chosen by ACTUAL object""");
    }
}
