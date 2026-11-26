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

---
---

# Part 2 — Design principles (audit of the added section)

You also fixed the interface label to **CAN-DO** in the original. ✅

Three entries are unfinished — Liskov, Interface Segregation, and Dependency
Inversion are blank or cut off mid-sentence. Those are filled in below.

Note on framing: SOLID/KISS/YAGNI/DRY are **design principles**, not "OOPS
principles." Abstraction/encapsulation/inheritance/polymorphism are the
*mechanisms* the language gives you; SOLID is *advice on how to aim them*.
Worth keeping separate in your head — an interviewer may ask for one and
you don't want to recite the other.

---

## SOLID

### S — Single Responsibility Principle  ✅ correct

"A class should be responsible for a single task; if there are multiple
responsibilities within a class we should create a new class and move that
extra responsibility to it."  ✅ That's right.

➕ The sharper formulation from Uncle Bob: **a class should have only one
reason to change.** That's more actionable than "one task," because "task"
is vague — is "handle orders" one task or ten?

Practical test: if you describe the class and need the word **"and"**, split
it. `Ticket` stores ticket data **and** prices it **and** writes it to the
database → three classes.

➕ The reason-to-change framing catches cases "one task" misses. An `Invoice`
class that both calculates totals and formats them as PDF has two reasons to
change: tax rules change, and the design team changes the layout. Two
different people, on two different schedules, editing the same file.

### O — Open/Closed Principle  ✅ correct

"A class should be open for extension but closed for modification; we should
have interfaces which extend the functionality of the classes instead of
modifying the existing implementation as it might break the existing
structure."  ✅ Correct, and the reasoning is right.

➕ Concrete smell that tells you you've violated it: **a `switch` or
`if/else if` chain over a type**, which you must edit every time a new type
appears.

    // closed for extension: every new payment type edits this method
    double fee(String type) {
        if (type.equals("card")) return 2.0;
        else if (type.equals("upi")) return 0.5;
        // ...and you edit here again, forever
    }

    // open for extension: a new type is a NEW class, zero edits here
    interface FeeStrategy { double fee(); }

That's exactly `FeeStrategy` in `lld/01_parking_lot`. Adding `WeekendFee`
requires no change to `Lot` at all — that's exercise 1 in that README, and
now you know what it's testing.

➕ Caveat worth having: you cannot make everything open to extension. You
make the axis you *expect to vary* open. Guessing wrong adds abstraction
nobody uses — which is exactly what YAGNI (below) warns about. These two
principles genuinely pull against each other, and judgment is the tiebreaker.

### L — Liskov Substitution Principle  ❌ blank ("It means the")

**Objects of a subclass must be usable anywhere the superclass is expected,
without the caller noticing.** Inheritance promises "IS-A"; LSP demands the
promise hold *behaviourally*, not just in the type system.

The canonical counterexample — and it's genuinely surprising:

    class Rectangle {
        protected int w, h;
        void setWidth(int w)  { this.w = w; }
        void setHeight(int h) { this.h = h; }
        int area() { return w * h; }
    }
    class Square extends Rectangle {
        @Override void setWidth(int w)  { this.w = w; this.h = w; }  // sides must stay equal
        @Override void setHeight(int h) { this.w = h; this.h = h; }
    }

    static void resizeAndCheck(Rectangle r) {
        r.setWidth(5);
        r.setHeight(4);
        // any reasonable caller expects 20
    }

Verified output:

    Rectangle:  expected 20, got 20  ok
    Square:     expected 20, got 16  <-- BROKEN

A square **is** a rectangle in mathematics. In code it is not a substitutable
one, because it breaks an assumption callers rely on: that width and height
move independently. The type checker is perfectly happy; the behaviour is
wrong. That gap is the whole lesson.

**Signs you're violating LSP:**
- an override throws `UnsupportedOperationException`
- an override tightens what it accepts (parent takes any int, child rejects negatives)
- an override weakens what it guarantees (parent never returns null, child does)
- callers need `if (x instanceof Square)` to work correctly

**The fix is almost always composition instead of inheritance.** Don't make
`Square extends Rectangle`; give both a `Shape` interface with `area()`, and
no setters that can break the invariant.

### I — Interface Segregation Principle  ❌ cut off ("two objects must be segregated by the interface, the subclasses")

**No client should be forced to depend on methods it does not use.** Many
small, focused interfaces beat one fat one. It's SRP applied to interfaces.

    interface FatWorker { void work(); void eat(); void attendMeeting(); }

    class Robot implements FatWorker {
        public void work() { }
        public void eat() { throw new UnsupportedOperationException("robots don't eat"); }
        public void attendMeeting() { throw new UnsupportedOperationException(); }
    }

Verified: calling `eat()` on the Robot throws. Two dead methods exist purely
to satisfy the compiler — that's the smell.

    // fixed
    interface Workable { void work(); }
    interface Feedable { void eat(); }

    class Robot implements Workable { }                    // only what applies
    class Human implements Workable, Feedable { }

➕ This is *why* Java lets you implement many interfaces (Part 1). Small
interfaces are only practical because you can freely combine them. ISP and
multiple-interface-inheritance are the same design idea from two directions.

➕ Detection: an implementing class with empty method bodies, or methods that
throw "not supported." Both mean the interface is too fat.

### D — Dependency Inversion Principle  ❌ blank

**Depend on abstractions, not concretions.** Two halves:

  1. High-level modules should not depend on low-level modules; both should
     depend on abstractions.
  2. Abstractions should not depend on details; details depend on abstractions.

    // violated: the service welds itself to one database
    class BadService {
        private final MySqlDb db = new MySqlDb();     // constructed inside
        void register(String user) { db.save(user); }
    }

You cannot test `BadService` without a live MySQL, and swapping to Postgres
means editing the class.

    // fixed: both sides depend on the Database interface
    interface Database { void save(String s); }

    class GoodService {
        private final Database db;
        GoodService(Database db) { this.db = db; }    // injected — the caller decides
        void register(String user) { db.save(user); }
    }

Verified: the same `GoodService` runs against `MySql` in production and an
`InMem` fake in a test, with zero changes to the class.

➕ **"Inversion" names the direction change.** Normally high-level code points
down at low-level code. DIP inverts it: the low-level `MySql` now points *up*
at the `Database` interface, which the high-level code owns. Both arrows now
point at the abstraction in the middle.

➕ The practical rule that captures 90% of it: **if you type `new` on a
collaborator inside a class, ask whether it should be a constructor
parameter instead.** That's dependency injection, and it's the same move as
`Lot(FeeStrategy fee)` and the `Clock` in `lld/03_rate_limiter`.

➕ Don't over-apply it. `new ArrayList<>()` inside a class is fine — a value
you own isn't a dependency. It applies to *collaborators*: databases, clocks,
network clients, strategies. Things you'd want to fake in a test.

---

## KISS  ✅ correct

"Keep it simple stupid — instead of creating so many interfaces and abstract
classes we should keep the logic simple and concise."  ✅ Right, and the
example you chose is the right one, because over-abstraction is the most
common way experienced developers make code worse.

➕ Note this is in direct tension with Open/Closed. Every abstraction buys
flexibility and costs a layer of indirection. KISS says: don't pay until you
need it. **Add the abstraction on the second or third occurrence, not the
first** — by then you know what actually varies, instead of guessing.

---

## YAGNI  ✅ correct

"You aren't gonna need it."  ✅ Your explanation is right — don't build for
imagined future requirements.

One small refinement to the last clause: *"we should make our code so
flexible so that we can extend it based on the needs of the future."*
Building maximum flexibility up front is itself a YAGNI violation. Aim for
**simple and easy to change**, not **flexible in advance**. Simple code is
easy to change precisely *because* there's less of it to change.

➕ YAGNI is about **speculative** features. It is not an argument against
writing tests, handling errors, or naming things well — those pay off now.

---

## DRY  ✅ correct

"Don't repeat yourself — avoid repeating code, reuse instead of rewriting."  ✅

➕ Two refinements that matter in practice:

**DRY is about knowledge, not text.** The real statement is: every piece of
knowledge should have a single authoritative representation. Two functions
that happen to look similar but encode *different rules* are not duplication
— merging them couples things that should move independently, and you'll be
tearing them apart in six months.

**The rule of three.** Two similar bits of code: leave them. Three: refactor.
Deduplicating too early, before you can see which parts genuinely vary,
produces a badly-shaped abstraction — the classic result is a shared method
with five boolean flags controlling its behaviour. That's worse than the
duplication was.

➕ The counter-principle worth knowing by name: **AHA — Avoid Hasty
Abstractions.** "Duplication is far cheaper than the wrong abstraction."
Duplication is easy to see and easy to fix; a wrong abstraction is load-
bearing and everywhere.

---

## Summary of Part 2

**Correct:** SRP ✅, OCP ✅, KISS ✅, YAGNI ✅, DRY ✅, and the CAN-DO fix ✅

**Unfinished — now filled in:**
- **L** — subclasses must be substitutable without callers noticing
  (Square/Rectangle: verified 16 instead of 20)
- **I** — no client forced to depend on methods it doesn't use
  (fat interface → dead methods that throw)
- **D** — depend on abstractions; inject collaborators rather than `new`-ing them

**The one framing to carry into interviews:** these principles conflict, and
knowing *when not to apply one* is the actual skill. OCP pushes you toward
abstraction; KISS and YAGNI push back. DRY says deduplicate; AHA says wait
until you can see the shape. Saying "I'd keep this concrete for now and
extract a strategy when a second pricing rule appears" scores far better
than reciting all five letters.

## Run these yourself

    cd notes/oop_proofs && javac SolidProofs.java && java SolidProofs

---

# Part 3 — Class relationships

Your table:

```
Association - USES-A
Aggregation - HAS-A (Weak)
composition - HAS-A (Strong)
Inheritnce  - IS-A
Abstraction - IS-A
interface   - CAN-DO
Realization -
```

Proof file: `notes/oop_proofs/RelationshipProofs.java`

## ✅ Correct

- **Association – USES-A.** Right.
- **Aggregation – HAS-A (weak).** Right.
- **Composition – HAS-A (strong).** Right.
- **Inheritance – IS-A.** Right.
- **interface – CAN-DO.** Right.

Five of seven rows correct, and you got the hard one right: weak vs strong HAS-A is
the distinction most people blur.

## ❌ Wrong

**1. "Abstraction – IS-A" does not belong in this table.**

Abstraction is a *pillar* — a way of thinking (hide detail, expose intent). It is not
a relationship between two classes. This table answers "how are class A and class B
wired together"; abstraction answers "how much of A do I show anyone".

If you meant *abstract class*, then the relationship is already listed: `Sparrow extends Bird`
is Inheritance. An abstract parent doesn't create a new kind of link — it's the same
IS-A arrow, just with a parent that can't be instantiated.

In UML the generalization arrow is identical whether the parent is abstract or concrete.

**2. "Realization" is blank — but it's the row directly above it.**

Realization *is* the UML name for `implements`. Your `interface – CAN-DO` row and your
`Realization` row are the same relationship written twice:

```
Realization = a class realizes (implements) an interface = CAN-DO
```

So the correct table has six rows, not seven: drop `Abstraction`, and merge
`interface` into `Realization`.

## ➕ Missing

**1. Dependency — the weakest link, and the true "uses-a".**

You have no row for it. This matters because you labelled Association as USES-A, and
interviewers usually reserve USES-A for Dependency:

| | link lives in | lifetime |
|---|---|---|
| **Dependency** | a parameter, return type, or local variable | one method call |
| **Association** | a **field** | as long as the object |

```java
class Desk {
    void work() { new Printer().print(new Report()); }  // dependency: no field
}
class Course {
    Teacher teacher;                                     // association: a field
}
```

Sharper labels: Dependency = "uses-a briefly", Association = "knows-a".

**2. The test that actually separates aggregation from composition: who controls the lifecycle.**

"Weak" and "strong" are the labels, not the test. The test is: **when the whole is
destroyed, does the part die with it?**

```java
// AGGREGATION — part handed in from outside, survives the whole
class Department {
    private final List<Student> students;
    Department(List<Student> students) { this.students = students; }  // received
}
// department gone -> asha and ben still exist

// COMPOSITION — part created inside, never leaks out, dies with the whole
class Car {
    private final Engine engine;
    Car(int hp) { this.engine = new Engine(hp); }   // created here
    String spec() { return "car with " + engine; }  // never RETURNS the Engine
}
```

Code tells for composition: the part is `new`ed in the constructor, the field is
`private final`, and **no getter hands it out**. The moment you write
`Engine getEngine()`, you've downgraded to aggregation — the caller can now keep a
reference that outlives the Car.

Java has no destructors, so nothing enforces this; it's a design intent you express
by controlling construction and access.

**3. The full table, ordered by coupling strength (weakest → tightest).**

| Relationship | Reads as | Java shape | Coupling |
|---|---|---|---|
| Dependency | uses-a briefly | parameter / local var | weakest |
| Association | knows-a | a field, either side | weak |
| Aggregation | has-a (weak) | field passed in; part outlives whole | medium |
| Composition | has-a (strong) | field created inside; part dies with whole | strong |
| Realization | can-do | `implements Interface` | strong (contract only) |
| Inheritance (Generalization) | is-a | `extends Parent` | tightest |

Note that Realization is strong on *contract* but weak on *implementation* — you're
bound to a set of method signatures and nothing else. Inheritance binds you to
signatures **plus** state **plus** behaviour, which is exactly why "composition over
inheritance" is the standing advice.

**4. UML notation** — asked for surprisingly often:

```
Dependency    A ----------> B     dashed line, open arrow
Association   A ----------- B     solid line (arrow if one-way)
Aggregation   A <>--------- B     hollow diamond at the WHOLE
Composition   A <#>-------- B     filled diamond at the WHOLE
Realization   A - - - - -|> B     dashed line, hollow triangle
Inheritance   A ---------|> B     solid line, hollow triangle
```

The diamond always sits on the **owner** side. Mixing up which end the diamond goes on
is the classic slip.

**5. Why this table is the core LLD skill.**

Every LLD question is answered by picking edges from this table. In
`lld/01_parking_lot/ParkingLot.java`:

- `Lot` → `Spot` — **composition**: the Lot's spots have no meaning without the Lot.
- `Spot` → `Vehicle` — **association**: the car exists before and after it parks.
- `Lot` → `FeeStrategy` — **dependency inversion via association**: injected, swappable.
- `HourlyFee` → `FeeStrategy` — **realization**.
- `Ticket` → `Vehicle`, `Spot` — **association**: the ticket references, doesn't own.

Notice there is **no inheritance anywhere** in that design. That's typical of good LLD —
the tightest arrow is used least.

---

# Part 4 — How each relationship is implemented

Your notes:

```
Realization - CAN-DO          <-- fixed from last round, good

How are these implemented
association  - it can be implemented in code using
aggregation  - it can be implmented using an interface
composition  - using an interface
inheritance  - superclass and subclass, or an abstract class
realization  - using an interface
```

Proof file: `notes/oop_proofs/ImplementationProofs.java`

## ✅ Correct

- **You merged `interface` into `Realization`.** That was the Part 3 fix and you applied it.
- **realization – using an interface.** Correct, and it's the one row where "an interface"
  is genuinely the answer.
- **inheritance – superclass and subclass, or an abstract class.** Correct. `extends`,
  and the parent may be concrete or abstract.

## ❌ Wrong

**1. Aggregation is not "implemented using an interface". Neither is composition.**

Both are implemented with a **field**. Whether that field is *typed* as an interface or
as a concrete class is a separate, independent decision. Proof — aggregation and
composition with zero interfaces in sight:

```java
class Trailer {                                  // AGGREGATION
    private final List<Wheel> wheels;
    Trailer(List<Wheel> wheels) { this.wheels = wheels; }   // passed in
}
class Bicycle {                                  // COMPOSITION
    private final Frame frame;
    Bicycle() { this.frame = new Frame(); }                 // created inside
}
```

Both compile and behave correctly. `Wheel` and `Frame` are plain classes.

**2. This is the important one: you are collapsing two independent axes.**

| | question | answer decides |
|---|---|---|
| **Axis 1 — ownership** | who creates the part, who outlives whom? | aggregation vs composition |
| **Axis 2 — field type** | is the field declared as an interface or a class? | how coupled you are (DIP) |

All four combinations are legal:

| | interface-typed field | class-typed field |
|---|---|---|
| **created inside** | composition, swappable internals | composition, rigid |
| **passed in** | **aggregation + DIP ← the sweet spot** | aggregation, rigid |

`ImplementationProofs.java` section B compiles and runs all four. So "uses an interface"
tells you nothing about which relationship you have.

**3. The association row is unfinished** — it trails off at "using".

Answer: **a field**. That's it.

```java
class Course { Teacher teacher; }    // association
```

Which raises the obvious question — if association is a field and aggregation is a field
and composition is a field, what actually separates them? See below.

## ➕ Missing

**1. The single table you actually need.**

| Relationship | Implemented by | Code tell |
|---|---|---|
| Dependency | **no field** — parameter, return type, or local var | appears only inside a method |
| Association | **a field** | plain reference, no ownership claim |
| Aggregation | **a field passed in** | assigned from a constructor/setter argument |
| Composition | **a field created inside** | `new`ed in the constructor, never returned |
| Realization | **`implements`** | keyword |
| Inheritance | **`extends`** | keyword |

Read the middle column top to bottom: **only the last two are implemented by a keyword.**
The first four are all "a field, or no field" — they differ by *where the object comes
from* and *who outlives whom*, not by syntax. That is why they're the ones people mix up:
Java gives you no keyword to tell them apart, so it's a design intent you signal through
construction and access control.

**2. Composition's three code tells, together.**

```java
class Bicycle {
    private final Frame frame;                     // 1. private final
    Bicycle() { this.frame = new Frame(); }        // 2. new'ed inside
    String spec(){ return "bicycle with " + frame; } // 3. NEVER returns frame
}
```

Add `Frame getFrame()` and you've silently downgraded to aggregation — the caller can
now hold a reference that outlives the Bicycle. Java has no destructors, so nothing
enforces composition for you; points 1–3 *are* the enforcement.

**3. Abstract class vs interface for the inheritance row.**

You listed both under inheritance, which is right, but they're different relationships in UML:

```java
class Contractor extends Employee implements Payable { ... }
//                ^ inheritance (is-a)  ^ realization (can-do)
```

`extends` = inheritance/generalization, one parent only, inherits state + behaviour.
`implements` = realization, many allowed, inherits contract only.

**4. What "implemented using an interface" is actually the answer to.**

Your instinct wasn't random — interfaces *are* central, just to a different question:
**Dependency Inversion**. Not "what relationship is this" but "how loosely coupled is it".

```java
class Lot {
    private final FeeStrategy feeStrategy;              // interface type
    Lot(List<Spot> spots, FeeStrategy feeStrategy) {    // passed in
        this.feeStrategy = feeStrategy;
    }
}
```

That's aggregation (passed in) **plus** an interface type (DIP). The aggregation makes it
injectable; the interface makes it swappable. Two decisions, both deliberate — which is
exactly why `WeekendFee` is addable without editing `Lot` in the parking-lot exercise.

---

# Part 5 — Design patterns

Proof file: `notes/oop_proofs/PatternProofs.java`

## ✅ Correct

**The three-way split is right, and it's the thing worth knowing.** Creational /
Behavioural / Structural, described as object creation / object behaviour / object
structure — that's the correct taxonomy and the correct one-line gloss for each.

**Your category assignments are all correct.** Every pattern you listed is filed under
the right heading — 21 of them, no misfiles. That's the part people get wrong.

**Definitions given:**
- **singleton** — "only one instance of a class available" ✅ (but see below — it's a
  goal, not something the obvious code delivers)
- **builder** — "builds a complex object step by step" ✅ exactly right
- **prototype** — "duplicates an existing object to save time and space" ✅ right, and
  you correctly tied it to *repeatable* objects, which is the actual use case

## ❌ Wrong / imprecise

**1. "factory — gives responsibility of creating concrete objects to the subclasses."**

That's the definition of **Factory Method** specifically, not "factory" generally. Three
different things get called factory:

| | who decides the concrete type | subclass needed? |
|---|---|---|
| **Simple Factory** (not GoF) | a `switch` in one method | no |
| **Factory Method** (GoF) | **a subclass overriding a method** ← your definition | yes |
| **Abstract Factory** (GoF) | a factory object, producing a **family** | no (composition) |

```java
Shape s = SimpleFactory.create("circle");     // switch, no subclass at all
new CircleDialog().render();                  // subclass chose -> factory method
```

Both run in `PatternProofs.java` section B. So your definition is right but attached to
the wrong name — say "factory method" and it's correct.

**2. `abstract factory` is listed with no definition** — and it's the one most likely to
be asked next, precisely because it sounds like the previous line.

**Abstract factory = a factory that produces a *family* of related products, guaranteed
to match.**

```java
interface GuiFactory { Button button(); Checkbox checkbox(); }   // TWO products
class MacFactory implements GuiFactory { ... }                   // both Mac
class WinFactory implements GuiFactory { ... }                   // both Windows
```

The point is you can't accidentally pair a Mac button with a Windows checkbox. Factory
method makes **one** product; abstract factory makes a **matched set**.

**3. Singleton's definition hides the interview follow-up.** "Only one instance" is the
*intent*. The code everyone writes doesn't achieve it:

```java
static Naive get() {
    if (instance == null) instance = new Naive();   // two threads both pass this
    return instance;
}
```

Run with 8 threads → **8 distinct instances** (verified, section A). The follow-up
question is always "is that thread safe?" Answers worth memorising:

```java
// initialization-on-demand holder — lazy AND safe, no synchronization cost
class Holder {
    private Holder() {}
    private static class H { static final Holder INSTANCE = new Holder(); }
    static Holder get() { return H.INSTANCE; }
}
enum EnumSingleton { INSTANCE; }   // simplest correct one; serialization-safe too
```

Also worth knowing: singleton is the most-criticised pattern — it's global mutable state
and it makes testing hard (you can't inject a fake). Saying that unprompted reads well.

**4. Two spellings:** `flywheel` → **flyweight** (it shares immutable state to save
memory; nothing to do with wheels). `mediatior` → **mediator**. Also `chain or
responsibility` → **chain of**.

## ➕ Missing

**1. Nine of your behavioural and structural patterns have no definition** — you defined
all five creational ones, then stopped. The one-liners:

**Behavioural**
| | |
|---|---|
| observer | one-to-many: subject notifies all subscribers on change |
| strategy | swap an algorithm at runtime behind one interface |
| command | wrap a request as an object (enables undo, queue, log) |
| state | object changes behaviour when its internal state changes |
| visitor | add a new operation to a class hierarchy without editing it |
| mediator | objects talk through a hub instead of to each other |
| iterator | walk a collection without exposing its internals |
| chain of responsibility | pass a request along handlers until one handles it |
| template method | parent fixes the algorithm's skeleton, subclass fills the steps |

**Structural**
| | |
|---|---|
| adapter | make an incompatible interface fit an expected one |
| bridge | split abstraction from implementation so both vary independently |
| composite | treat individual objects and groups uniformly (trees) |
| decorator | wrap an object to add behaviour, same interface |
| flyweight | share common immutable state across many objects |
| facade | one simple entry point over a complicated subsystem |
| proxy | a stand-in controlling access (lazy, remote, security) |

**2. The pairs that get confused — worth learning as pairs, not singly.**

**Adapter vs Decorator** — both wrap. The difference is what happens to the interface:

```java
new PrinterAdapter(legacy).print("hello");        // CHANGES interface, adds nothing
new TimestampPrinter(plain).print("hello");       // KEEPS interface, ADDS behaviour
```

**Strategy vs State** — near-identical code, opposite intent. Strategy: the **caller**
picks and it doesn't change. State: the **object** swaps its own state and transitions
itself:

```
new -> paid -> shipped     // state drives its own successor (verified, section D)
```

**Factory Method vs Abstract Factory** — one product vs a matched family (above).

**Decorator vs Proxy** — decorator adds behaviour you asked for; proxy controls *access*
to something (lazy-loads it, checks permission, calls it remotely).

**3. Patterns you've already used in this repo** — worth naming, since concrete beats
abstract:

- `FeeStrategy` / `HourlyFee` / `FlatFee` in `lld/01_parking_lot/` — **strategy**,
  injected through the constructor.
- `record Ticket(...)` — not a pattern, but the compiler-generated constructor is
  effectively **builder**'s simple case.
- The `lld/04_cache/` spec will want **proxy** (lazy load) or **decorator** (add TTL).
- `lld/03_rate_limiter/` is naturally **strategy** again (token bucket vs sliding window).

**4. The honest framing for interviews.** Don't pattern-match a name onto a problem.
The sequence that scores is: *what varies here?* → extract that → **then** notice the
result already has a name. Naming a pattern you didn't need is a YAGNI violation, which
is exactly the tension flagged in Part 2. Roughly five patterns cover most LLD rounds:
**strategy, factory method, observer, builder, singleton** — know those cold, recognise
the rest.
