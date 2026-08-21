# OOPS — corrected

Same structure as `validating .md` so you can diff them section by section.
Every claim here was compiled and run on JDK 25 before being written down.

Markers:
  ✅ you had this right
  ❌ you had this wrong — the correction follows
  ➕ you didn't mention it, and it matters

---

OOPS -- object oriented programming

It deals with objects and classes.  ✅

Classes are the blueprint of anything, while objects are the instances of
those classes.  ✅

➕ Worth adding: a class defines two things — what an object **knows**
(fields / state) and what it can **do** (methods / behaviour). Every design
decision in OOP is really a decision about which class knows what.

OOPS has 4 major principles.  ✅

---

## Abstraction

Hiding the implementation details of the methods from the users is known as
abstraction.  ✅

These are achieved by using abstract classes and interfaces.  ✅

➕ Sharper definition: abstraction is exposing **what** something does while
hiding **how**. You already do this constantly in Python — when you call
`list.sort()` you don't know or care that it's Timsort. That's abstraction.
The interface is the "what"; the implementing class is the "how".

### abstract classes (IS-A)  ✅ the IS-A label is correct

❌ **"when a subclass is created out of those abstract classes it is forced
to implement all the methods mentioned in the abstract class"**

Only the methods marked `abstract` (the ones with **no body**) must be
implemented. Concrete methods are inherited and work as-is:

    abstract class Shape {
        protected String name;
        Shape(String name) { this.name = name; }   // abstract classes CAN have constructors
        abstract double area();                     // a HOLE the subclass must fill
        void describe() {                           // shared, already-working code
            System.out.println(name + " area=" + area());
        }
    }

    class Circle extends Shape {
        private final double r;
        Circle(double r) { super("circle"); this.r = r; }
        @Override double area() { return Math.PI * r * r; }
        // describe() was never written here, but new Circle(1).describe() works
    }

Verified output: `circle area=3.141592653589793`

**This is the whole reason abstract classes exist.** They give you shared
working code *plus* holes. If a class had no shared code, you'd use an
interface instead. So an abstract class is a partially-built thing, and the
subclass finishes it.

➕ An abstract class cannot be instantiated. `new Shape("x")` is a compile
error: *"Shape is abstract; cannot be instantiated"*. It's incomplete by
definition — there's a hole where `area()` should be.

❌ **"a class can have only one abstract class while an abstract class can be
used to create multiple subclasses"**

The second half is right. The first half fuses two separate rules:

  - A class can `extend` **exactly one** class — abstract or not.
    `class Child extends P1, P2 {}` is a syntax error. Verified.
  - A class can `implement` **many** interfaces, and do both at once:
    `class Duck extends Creature implements Walker, Swimmer` compiles fine.

➕ **That asymmetry is the point, and it's worth understanding rather than
memorising.** Inheriting from two classes creates the "diamond problem": if
both parents have a `balance` field and a `pay()` method, which one does the
child get? Java refuses to guess, so it allows only one parent for **state**.
Interfaces carry no state, so there's nothing to collide — you can have as
many as you like.

    Single inheritance of STATE.  Multiple inheritance of CONTRACT.

### interface

❌ **"(Uses-A)"** — nonstandard, and it collides with a term that means
something else. The relationships:

    IS-A     inheritance      Dog extends Animal        — a Dog is an Animal
    CAN-DO   interface        Duck implements Swimmer   — a Duck can swim
    HAS-A    composition      Car has an Engine field   — a Car has an Engine
    USES-A   dependency       repo passed to a method   — transient use

Interfaces are **CAN-DO**: a capability, not an identity. `Serializable`
means "can be serialized." `Comparable` means "can be compared." That's why
a class can have many — a Duck can swim *and* walk *and* fly, while it can
only *be* one kind of thing.

"These are contracts between two classes where they have to implement the
methods mentioned in these interfaces."  ✅ — though phrase it as a contract
between a class and its **callers**, not between two classes. The interface
is a promise to whoever holds the reference.

"The interfaces can have their own implementation which the classes
implementing them can override."  ✅ Correct, and most people don't know it.
The keyword is `default` (Java 8+):

    interface Walker {
        default void move() { System.out.println("walking"); }  // optional to override
        void stop();                                            // mandatory
    }

➕ Interfaces cannot hold mutable state. Any field in an interface is
implicitly `public static final` — a constant. This is the technical reason
the diamond problem doesn't apply to them.

➕ **How to choose, which is what interviewers actually probe:**

    Interface       "can do"    many allowed   no state   default: pick this
    Abstract class  "is a"      one only       has state + constructors

Reach for an abstract class only when subclasses genuinely share both state
and working code. Otherwise the interface keeps you flexible.

---

## Encapsulation

"Bundling together the attributes and methods in a class is called
encapsulation; here we hide the attributes from the end users and we make
sure that they are modified using the getters and setters, instead of
directly exposing them."  ✅ This section was correct.

➕ What's missing is **why** — and the why is what makes it more than
ceremony. Two real payoffs:

**1. You can enforce invariants.** A public field can be set to anything by
anyone. A setter is a checkpoint:

    class Account {
        private double balance;
        void deposit(double amt) {
            if (amt <= 0) throw new IllegalArgumentException("must be positive");
            balance += amt;
        }
        double getBalance() { return balance; }
    }

Verified: `acc.deposit(-50)` throws, and the balance stays valid. With a
public `balance` field, `acc.balance = -50` would silently corrupt it and
you'd find out three screens later.

**2. You can change the internals without breaking callers.** If `balance`
is private, you can switch it from `double` to `BigDecimal`, or compute it
from a transaction list, and every caller of `getBalance()` still compiles.
Public fields freeze your implementation forever.

➕ Don't write getters and setters reflexively for every field. A setter for
a field that should never change after construction is a bug waiting to
happen — mark it `final` and expose only a getter. Encapsulation means
*control over* access, not *always granting* access.

---

## Inheritance (IS-A)  ✅ label correct

"Creating subclasses from superclasses where the subclass inherits all the
behaviours from the superclass."  ✅

❌ **"they can modify the behaviour but they would have to implement those
behaviours"** — same error as the abstract-class section. A subclass
inherits concrete methods for free and implements **nothing** unless the
method is `abstract`. Overriding is optional; only filling holes is required.

➕ `super` does two jobs, and you'll need both:

    super(name);        // call the parent CONSTRUCTOR — must be the first line
    super.hi();         // call the parent's VERSION of a method you overrode

Verified: `super.hi()` inside an override prints the base version first,
then the derived one.

➕ **Composition over inheritance — the most important idea missing from
your notes.** Inheritance is rigid: one parent, fixed at compile time, and
the subclass is exposed to the parent's internals. A field you can swap is
usually better:

    // inheritance — locked in at compile time
    class HourlyLot extends Lot { }

    // composition — swappable at runtime, testable in isolation
    class Lot {
        private final FeeStrategy fee;
        Lot(FeeStrategy fee) { this.fee = fee; }   // pass in whatever you want
    }

That second form is exactly `lld/01_parking_lot/ParkingLot.java`. Swapping
the entire pricing model is one line at the call site and zero edits to
`Lot`. That's the payoff, and it's why the guideline is "favour composition
over inheritance."

➕ **Liskov substitution:** a subclass must be usable anywhere its parent is,
without surprises. If overriding a method forces you to write
`throw new UnsupportedOperationException()`, inheritance was the wrong tool
— use composition instead.

---

## Polymorphism

"The same functionality can vary based on how it is used."  ✅ — the
literal meaning is "many forms," and the practical meaning is: one call
site, several possible behaviours.

Two ways to implement it: overloading and overriding.  ✅

### method overloading  ✅ mostly right

"The methods are called with different parameters and based on the
parameters different methods are called."  ✅

➕ Two precisions that get tested:

**Resolved at COMPILE time**, using the *declared* type — not the runtime
object. This surprises everyone:

    static void f(Object o) { System.out.println("f(Object)"); }
    static void f(String s) { System.out.println("f(String)"); }

    Object x = "I am really a String";
    f(x);              // prints f(Object)  — declared type is Object
    f((String) x);     // prints f(String)  — the cast changed the declared type

Verified. The object was a String both times; only the *declaration* decided.

**Return type alone cannot overload.** These two collide:

    static int  f(int x) { return x; }
    static long f(int x) { return x; }   // error: f(int) is already defined

Overloads must differ in parameter **types or count**.

### method overriding

❌ **This is the most important correction in the file.**

You wrote: *"when the subclass invokes the same method the implementation of
the subclass takes precedence, and when the superclass invokes the same
method then the implementation of the superclass takes precedence."*

The second half is wrong. **The object's actual runtime type always wins,
regardless of the declared type and regardless of who is calling.**

    class Super {
        void greet()  { System.out.println("SUPER greet"); }
        void caller() { greet(); }      // Super's OWN code calling greet()
    }
    class Sub extends Super {
        @Override void greet() { System.out.println("SUB greet"); }
    }

    Super ref = new Sub();   // declared Super, actually a Sub
    ref.greet();             // "SUB greet"  <- not SUPER
    ref.caller();            // "SUB greet"  <- Super's own code still gets Sub's version
    new Super().greet();     // "SUPER greet" <- only because the object IS a Super

Verified output, exactly as shown.

This is called **dynamic dispatch** (or late binding), and it is not a
detail — it's the entire mechanism that makes polymorphism useful. It's why
`totalArea(List<Shape>)` in `drills/d05` works for shapes that didn't exist
when it was written.

The only way to reach the parent's version is `super.greet()`, from inside
the subclass.

➕ **You already rely on this daily in Python.** `self.greet()` inside a base
class calls the subclass override there too. Identical semantics — the notes
just describe it backwards.

➕ **The rule to remember:**

    overloading  -> compile time, chosen by DECLARED type   ("static dispatch")
    overriding   -> run time,     chosen by ACTUAL object   ("dynamic dispatch")

"Note that in this case the method name as well as the parameter and the
return types are same for both the subclass and the superclass."  ✅ Name
and parameters must match exactly, otherwise it's an overload, not an
override. Return type may be a *subtype* of the original (covariant return),
but matching is the safe default.

➕ **Always write `@Override`.** It's not decoration — it makes the compiler
verify you're actually overriding something:

    class Q extends P { @Override void proccess() {} }   // typo
    // error: method does not override or implement a method from a supertype

Verified. Without the annotation that typo compiles silently and creates a
brand-new method that never gets called. You'd debug it for an hour.

---

## Summary of the five corrections

1. Abstract classes force only `abstract` methods, not all methods.
2. One `extends` (class), many `implements` (interfaces) — state vs contract.
3. Interfaces are CAN-DO, not USES-A.
4. Inheritance requires implementing nothing unless the method is abstract.
5. **Overriding is resolved by the runtime object, always — even when the
   superclass's own code makes the call.**

## The four things worth adding

- Composition over inheritance (`HAS-A`) — the highest-leverage idea for LLD.
- Encapsulation exists to enforce invariants and to let internals change.
- Overloading = compile time / declared type; overriding = runtime / actual object.
- `@Override`, `super()`, and when to pick interface vs abstract class.

## Run these yourself

Everything above is 30 lines of code you can retype. Do that rather than
trusting this file — the dynamic-dispatch example in particular is worth
typing out and predicting before you run it.
