import java.util.*;

/*
 * Proofs for Part 3 of validating_CORRECTED.md — class relationships.
 * Ordered weakest coupling -> strongest.
 *   javac RelationshipProofs.java && java RelationshipProofs
 */

// ---------------------------------------------------------------
// 1. DEPENDENCY  "uses-a, briefly"    weakest
//    No field. The other class appears only as a parameter,
//    a return type, or a local variable. Dies at method end.
// ---------------------------------------------------------------
class Report {}
class Printer { void print(Report r) { System.out.println("    printing " + r.getClass().getSimpleName()); } }
class Desk {
    void work() {
        Printer p = new Printer();   // local only: no field
        p.print(new Report());
    }
}

// ---------------------------------------------------------------
// 2. ASSOCIATION  "uses-a, persistently"
//    A long-lived field link. Neither side owns the other.
//    Can be one-way or two-way.
// ---------------------------------------------------------------
class Teacher { final String name; Teacher(String n){ name = n; } }
class Course  { final Teacher teacher; Course(Teacher t){ teacher = t; } }

// ---------------------------------------------------------------
// 3. AGGREGATION  "has-a (weak)"
//    A whole/part association where the PART OUTLIVES THE WHOLE.
//    Tell: the part is handed in from outside (constructor/setter).
// ---------------------------------------------------------------
class Student { final String name; Student(String n){ name = n; } public String toString(){ return name; } }
class Department {
    private final List<Student> students;      // received, not created
    Department(List<Student> students) { this.students = students; }
    List<Student> students() { return students; }
}

// ---------------------------------------------------------------
// 4. COMPOSITION  "has-a (strong)"    strongest non-inheritance
//    The PART DIES WITH THE WHOLE.
//    Tell: the part is created inside and never leaks out.
// ---------------------------------------------------------------
class Engine {
    private final int hp;
    Engine(int hp) { this.hp = hp; }
    public String toString(){ return hp + "hp engine"; }
}
class Car {
    private final Engine engine;                    // created here
    Car(int hp) { this.engine = new Engine(hp); }   // owned exclusively
    String spec() { return "car with " + engine; }  // never returns the Engine
}

// ---------------------------------------------------------------
// 5. REALIZATION  "can-do"
//    class implements interface. UML's name for the interface link.
//    Inherits a CONTRACT, no state, no bodies (pre-default methods).
// ---------------------------------------------------------------
interface Flyer { void fly(); }
class Drone implements Flyer { public void fly(){ System.out.println("    drone flies"); } }

// ---------------------------------------------------------------
// 6. INHERITANCE / GENERALIZATION  "is-a"    tightest coupling
//    Inherits contract AND state AND behaviour. One parent only.
// ---------------------------------------------------------------
abstract class Bird { String id(){ return "a bird"; } abstract String sound(); }
class Sparrow extends Bird { String sound(){ return "chirp"; } }

public class RelationshipProofs {
    public static void main(String[] args) {
        System.out.println("1. DEPENDENCY  (uses-a, briefly)");
        new Desk().work();
        System.out.println("    Desk has no Printer field; the link exists only during work()");

        System.out.println("\n2. ASSOCIATION  (uses-a, persistently)");
        Course c = new Course(new Teacher("rao"));
        System.out.println("    course -> teacher " + c.teacher.name + "; neither owns the other");

        System.out.println("\n3. AGGREGATION  (has-a, weak)");
        Student s1 = new Student("asha"), s2 = new Student("ben");
        List<Student> roster = new ArrayList<>(List.of(s1, s2));
        Department d = new Department(roster);
        System.out.println("    dept: " + d.students());
        d = null;                                   // whole destroyed
        System.out.println("    dept gone, parts alive: " + s1 + ", " + s2 + "  <-- PART OUTLIVES WHOLE");

        System.out.println("\n4. COMPOSITION  (has-a, strong)");
        Car car = new Car(150);
        System.out.println("    " + car.spec());
        System.out.println("    no accessor returns the Engine  <-- PART DIES WITH WHOLE");

        System.out.println("\n5. REALIZATION  (can-do)");
        Flyer f = new Drone();
        f.fly();
        System.out.println("    Drone realizes Flyer -> " + (f instanceof Flyer));

        System.out.println("\n6. INHERITANCE  (is-a)");
        Bird b = new Sparrow();
        System.out.println("    " + b.id() + " that says " + b.sound()
            + "  <-- inherited id() for free, forced to supply sound()");
    }
}
