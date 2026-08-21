import java.util.*;
import java.util.concurrent.*;

/*
 * Proofs for Part 5 of validating_CORRECTED.md — design patterns.
 *   javac PatternProofs.java && java PatternProofs
 *
 * Covers the four claims worth testing:
 *   A. "singleton = only one instance" — the naive version does NOT deliver that
 *   B. "factory delegates to subclasses" — true of Factory Method, not Simple Factory
 *   C. abstract factory = a FAMILY of products, not one
 *   D. the pairs everyone confuses: adapter/decorator, strategy/state
 */

// ===============================================================
// A. Singleton — the definition has a thread-safety hole
// ===============================================================
class NaiveSingleton {
    private static NaiveSingleton instance;
    private NaiveSingleton() { try { Thread.sleep(5); } catch (InterruptedException e) {} }
    static NaiveSingleton get() {
        if (instance == null) instance = new NaiveSingleton();   // race: two threads both pass
        return instance;
    }
}
class HolderSingleton {                       // correct + lazy. memorise this one.
    private HolderSingleton() {}
    private static class H { static final HolderSingleton INSTANCE = new HolderSingleton(); }
    static HolderSingleton get() { return H.INSTANCE; }   // JVM guarantees one-time class init
}
enum EnumSingleton { INSTANCE; }              // simplest correct one

// ===============================================================
// B/C. The three things all called "factory"
// ===============================================================
interface Shape { String draw(); }
class Circle implements Shape { public String draw(){ return "circle"; } }
class Square implements Shape { public String draw(){ return "square"; } }

class SimpleFactory {                          // NOT a GoF pattern. no subclass.
    static Shape create(String kind) {
        return switch (kind) { case "circle" -> new Circle(); default -> new Square(); };
    }
}
abstract class Dialog {                        // FACTORY METHOD: subclass decides
    abstract Shape createShape();
    String render(){ return "dialog showing " + createShape().draw(); }
}
class CircleDialog extends Dialog { Shape createShape(){ return new Circle(); } }

interface Button   { String label(); }         // ABSTRACT FACTORY: a family
interface Checkbox { String tick();  }
class MacButton   implements Button   { public String label(){ return "mac button"; } }
class MacCheckbox implements Checkbox { public String tick(){  return "mac check";  } }
interface GuiFactory { Button button(); Checkbox checkbox(); }     // TWO products
class MacFactory implements GuiFactory {
    public Button button(){ return new MacButton(); }
    public Checkbox checkbox(){ return new MacCheckbox(); }
}

// ===============================================================
// D. Adapter vs Decorator  /  Strategy vs State
// ===============================================================
class LegacyPrinter { void printOld(String s){ System.out.println("      legacy:" + s); } }
interface ModernPrinter { void print(String s); }
class PrinterAdapter implements ModernPrinter {        // ADAPTER: changes the interface
    private final LegacyPrinter legacy;
    PrinterAdapter(LegacyPrinter l){ legacy = l; }
    public void print(String s){ legacy.printOld(s); }
}
class PlainPrinter implements ModernPrinter { public void print(String s){ System.out.println("      " + s); } }
class TimestampPrinter implements ModernPrinter {      // DECORATOR: same interface, adds
    private final ModernPrinter inner;
    TimestampPrinter(ModernPrinter i){ inner = i; }
    public void print(String s){ inner.print("[t0] " + s); }
}

interface OrderState { OrderState next(); String label(); }
class NewOrder implements OrderState                 { public OrderState next(){ return new Paid(); }    public String label(){ return "new"; } }
class Paid     implements OrderState { public OrderState next(){ return new Shipped(); } public String label(){ return "paid"; } }
class Shipped  implements OrderState { public OrderState next(){ return this; }          public String label(){ return "shipped"; } }

public class PatternProofs {
    public static void main(String[] args) throws Exception {
        System.out.println("A. SINGLETON — \"only one instance\" is a goal, not a guarantee");
        Set<NaiveSingleton> seen = ConcurrentHashMap.newKeySet();
        ExecutorService ex = Executors.newFixedThreadPool(8);
        CountDownLatch gate = new CountDownLatch(1);
        for (int i = 0; i < 8; i++) ex.submit(() -> { gate.await(); seen.add(NaiveSingleton.get()); return null; });
        gate.countDown(); ex.shutdown(); ex.awaitTermination(5, TimeUnit.SECONDS);
        System.out.println("      naive, 8 threads -> " + seen.size() + " distinct instances  <-- BROKEN");

        Set<HolderSingleton> ok = ConcurrentHashMap.newKeySet();
        ExecutorService ex2 = Executors.newFixedThreadPool(8);
        CountDownLatch g2 = new CountDownLatch(1);
        for (int i = 0; i < 8; i++) ex2.submit(() -> { g2.await(); ok.add(HolderSingleton.get()); return null; });
        g2.countDown(); ex2.shutdown(); ex2.awaitTermination(5, TimeUnit.SECONDS);
        System.out.println("      holder idiom   -> " + ok.size() + " distinct instance   correct");

        System.out.println("\nB. the three \"factories\"");
        System.out.println("      simple factory  : " + SimpleFactory.create("circle").draw() + "   (a switch, NO subclass)");
        System.out.println("      factory method  : " + new CircleDialog().render() + "   (subclass decided)");
        GuiFactory f = new MacFactory();
        System.out.println("      abstract factory: " + f.button().label() + " + " + f.checkbox().tick() + "   (a FAMILY)");

        System.out.println("\nD. the confusable pairs");
        System.out.println("   ADAPTER — changes the interface, adds no behaviour:");
        new PrinterAdapter(new LegacyPrinter()).print("hello");
        System.out.println("   DECORATOR — keeps the interface, adds behaviour:");
        new TimestampPrinter(new PlainPrinter()).print("hello");
        System.out.print("   STATE — the object advances itself: ");
        OrderState s = new NewOrder();
        for (int i = 0; i < 3; i++) { System.out.print(s.label() + " -> "); s = s.next(); }
        System.out.println(s.label() + "   (strategy would have the CALLER choose)");
    }
}
