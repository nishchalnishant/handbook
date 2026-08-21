import java.util.*;

/*
 * Proofs for Part 4 of validating_CORRECTED.md — how each relationship
 * is actually implemented in Java.
 *   javac ImplementationProofs.java && java ImplementationProofs
 *
 * Headline: only Realization and Inheritance are implemented with a KEYWORD.
 * The other four are all implemented with a FIELD (or no field at all).
 * An interface is NOT what makes something aggregation or composition.
 */

// ===============================================================
// A. Aggregation and composition need no interface whatsoever
// ===============================================================
class Wheel { public String toString(){ return "wheel"; } }

class Trailer {                                    // AGGREGATION, concrete type
    private final List<Wheel> wheels;
    Trailer(List<Wheel> wheels) { this.wheels = wheels; }   // passed in
    List<Wheel> wheels(){ return wheels; }
}

class Frame { public String toString(){ return "frame"; } }
class Bicycle {                                    // COMPOSITION, concrete type
    private final Frame frame;
    Bicycle() { this.frame = new Frame(); }        // created inside
    String spec(){ return "bicycle with " + frame; }
}

// ===============================================================
// B. Ownership and field-type are INDEPENDENT axes.
//    All four combinations are legal Java.
// ===============================================================
interface Logger { void log(String s); }
class FileLogger implements Logger { public void log(String s){ System.out.println("      " + s); } }

class SvcA {                                       // composition + interface field
    private final Logger logger;
    SvcA(){ this.logger = new FileLogger(); }
    void run(){ logger.log("composition + interface-typed field"); }
}
class SvcB {                                       // composition + class field
    private final FileLogger logger;
    SvcB(){ this.logger = new FileLogger(); }
    void run(){ logger.log("composition + class-typed field"); }
}
class SvcC {                                       // aggregation + interface field  <- DIP sweet spot
    private final Logger logger;
    SvcC(Logger logger){ this.logger = logger; }
    void run(){ logger.log("aggregation  + interface-typed field  <- most flexible"); }
}
class SvcD {                                       // aggregation + class field
    private final FileLogger logger;
    SvcD(FileLogger logger){ this.logger = logger; }
    void run(){ logger.log("aggregation  + class-typed field"); }
}

// ===============================================================
// C. Dependency: no field at all
// ===============================================================
class Invoice {}
class Mailer { void send(Invoice i){ System.out.println("      sent " + i.getClass().getSimpleName()); } }
class Clerk {
    void process() { new Mailer().send(new Invoice()); }   // local var only
}

// ===============================================================
// D. Realization and Inheritance: the only keyword-driven ones
// ===============================================================
interface Payable { double amount(); }             // realization -> implements
abstract class Employee {                          // inheritance  -> extends
    protected final String name;
    Employee(String name){ this.name = name; }
    String label(){ return name + " earns " + ((Payable) this).amount(); }
}
class Contractor extends Employee implements Payable {
    Contractor(String n){ super(n); }
    public double amount(){ return 500.0; }
}

public class ImplementationProofs {
    public static void main(String[] args) {
        System.out.println("A. aggregation / composition with ZERO interfaces");
        List<Wheel> ws = new ArrayList<>(List.of(new Wheel(), new Wheel()));
        Trailer t = new Trailer(ws);
        System.out.println("      trailer: " + t.wheels());
        t = null;
        System.out.println("      whole gone, parts alive: " + ws + "   (aggregation)");
        System.out.println("      " + new Bicycle().spec() + "            (composition)");
        System.out.println("      => no interface was needed for either");

        System.out.println("\nB. ownership vs field-type are independent");
        new SvcA().run();
        new SvcB().run();
        FileLogger shared = new FileLogger();
        new SvcC(shared).run();
        new SvcD(shared).run();

        System.out.println("\nC. dependency = no field");
        new Clerk().process();
        System.out.println("      Clerk declares no Mailer field");

        System.out.println("\nD. the only two implemented by a keyword");
        Contractor c = new Contractor("dev");
        System.out.println("      " + c.label());
        System.out.println("      extends Employee  -> inheritance (is-a)");
        System.out.println("      implements Payable -> realization (can-do)");
    }
}
