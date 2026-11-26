# Object-Oriented Programming & Design — Master Reference

> Theory reference for LLD interviews. Companion to `THE_SCRIPT.md` (the 45-minute
> procedure) and `TEXT_TO_CODE.md` (the class/abstract/interface/enum decision tree).
> This file is the *vocabulary*; those two are the *method*.

---

## Table of Contents

- [📖 Foundations of Object-Oriented Programming & Software Design](#foundations-of-object-oriented-programming-software-design)
  - [🗺️ Quick Reference Concepts Summary](#quick-reference-concepts-summary)
  - [🏗️ The Core Building Blocks: Classes vs. Objects](#the-core-building-blocks-classes-vs-objects)
  - [🏛️ The 4 Pillars of OOP](#the-4-pillars-of-oop)
  - [🛠️ Fundamental Design Pragmatics: DRY & YAGNI](#fundamental-design-pragmatics-dry-yagni)
- [📝 Master Notes: Object-Oriented Programming (OOP) Relationships](#master-notes-object-oriented-programming-oop-relationships)
  - [🗺️ Quick Reference Summary Table (Sorted by Coupling Strength)](#quick-reference-summary-table-sorted-by-coupling-strength)
  - [💻 Code Implementations & Rules](#code-implementations-rules)
  - [✈️ The Real-World Analogy (Putting it all together)](#the-real-world-analogy-putting-it-all-together)
- [📝 Master Notes: SOLID Design Principles](#master-notes-solid-design-principles)
  - [🗺️ Quick Reference Summary Table](#quick-reference-summary-table)
  - [💻 Code Implementations & Rules](#code-implementations-rules-1)
  - [🧭 The five smells, as one checklist](#the-five-smells-as-one-checklist)
  - [✈️ The Real-World Analogy (Putting it all together)](#the-real-world-analogy-putting-it-all-together-1)
- [📝 Master Notes: Creational Design Patterns](#master-notes-creational-design-patterns)
  - [🗺️ Quick Reference Summary Table](#quick-reference-summary-table-1)
  - [💻 Code Implementations & Rules](#code-implementations-rules-2)
  - [✈️ The Real-World Analogy (Putting it all together)](#the-real-world-analogy-putting-it-all-together-2)
- [📝 Master Notes: Behavioral Design Patterns](#master-notes-behavioral-design-patterns)
  - [🗺️ Quick Reference Summary Table](#quick-reference-summary-table-2)
  - [💻 Code Implementations & Rules](#code-implementations-rules-3)
  - [✈️ The Real-World Analogy (Putting it all together)](#the-real-world-analogy-putting-it-all-together-3)
- [📝 Master Notes: Structural Design Patterns](#master-notes-structural-design-patterns)
  - [🗺️ Quick Reference Summary Table (Ordered as Requested)](#quick-reference-summary-table-ordered-as-requested)
  - [💻 Code Implementations & Rules](#code-implementations-rules-4)
  - [✈️ The Real-World Analogy (Putting it all together)](#the-real-world-analogy-putting-it-all-together-4)
- [📝 Master Notes: Advanced Theoretical Underpinnings of OOP](#master-notes-advanced-theoretical-underpinnings-of-oop)
  - [🗺️ Quick Reference Summary Table](#quick-reference-summary-table-3)
  - [💻 Technical Explanations & Rules](#technical-explanations-rules)
  - [✈️ The Real-World Analogy (Putting it all together)](#the-real-world-analogy-putting-it-all-together-5)
- [📝 Master Notes: Object Contracts (`equals`, `hashCode`, `toString`, ordering)](#master-notes-object-contracts-equals-hashcode-tostring-ordering)
  - [🗺️ Quick Reference Summary Table](#quick-reference-summary-table-4)
- [📝 Master Notes: Immutability and `record`](#master-notes-immutability-and-record)
  - [🗺️ Why immutability wins](#why-immutability-wins)
- [📝 Master Notes: Concurrency and Thread Safety](#master-notes-concurrency-and-thread-safety)
  - [🗺️ Quick Reference Summary Table](#quick-reference-summary-table-5)
- [📝 Master Notes: Exception Design](#master-notes-exception-design)
  - [🗺️ Quick Reference Summary Table](#quick-reference-summary-table-6)
- [📝 Master Notes: Interface Evolution (`default`, `static`, `sealed`)](#master-notes-interface-evolution-default-static-sealed)
  - [🗺️ Quick Reference Summary Table](#quick-reference-summary-table-7)
- [📝 Master Notes: Object Construction](#master-notes-object-construction)
  - [🗺️ Quick Reference Summary Table](#quick-reference-summary-table-8)
- [📝 Master Notes: Generics and Variance](#master-notes-generics-and-variance)
  - [🗺️ Quick Reference Summary Table](#quick-reference-summary-table-9)
- [📝 Master Notes: Inheritance Hazards and Design Judgement](#master-notes-inheritance-hazards-and-design-judgement)
  - [1. The Fragile Base Class Problem](#1-the-fragile-base-class-problem)
  - [2. Prefer derived state over stored state](#2-prefer-derived-state-over-stored-state)
  - [3. The Rule of Three](#3-the-rule-of-three)
  - [4. Testability is a design property](#4-testability-is-a-design-property)
- [📝 Master Notes: Reading a UML Class Diagram](#master-notes-reading-a-uml-class-diagram)
  - [🗺️ Relationship arrows, by strength](#relationship-arrows-by-strength)
  - [Box notation and multiplicity](#box-notation-and-multiplicity)
- [🧭 Final self-check before an LLD round](#final-self-check-before-an-lld-round)

---

## 📖 Foundations of Object-Oriented Programming & Software Design

Before establishing class relationships or architectural patterns, software design rests on foundational building blocks, core pillars, and critical development pragmatics.

### 🗺️ Quick Reference Concepts Summary

| Concept Name | Core Meaning | Primary Architectural Purpose |
|---|---|---|
| Class | The compile-time abstract blueprint or data template. | Defines structure, variables, and potential behaviors. |
| Object | The runtime instance allocated in live system memory. | Represents a real entity holding actual data state. |
| DRY Principle | Don't Repeat Yourself. Avoid copy-pasting code blocks. | Ensures single sources of truth, reducing maintenance drag. |
| YAGNI Principle | You Ain't Gonna Need It. Avoid over-engineering features. | Keeps the codebase lean and prevents unnecessary complexity. |

### 🏗️ The Core Building Blocks: Classes vs. Objects

Understanding the divide between compile-time definitions and runtime execution is fundamental to writing stable software.

#### 1. The Class (The Blueprint)

- **What it is:** A logical blueprint or user-defined data type that outlines what properties (fields) and capabilities (methods) an entity will possess. It consumes zero heap memory storage space until instantiated.
- **Analogy:** An architectural blueprint sketch drawn on paper for a residential villa.

#### 2. The Object (The Instance)

- **What it is:** A concrete entity created at runtime that lives in your computer's memory heap. It is stamped out from its matching class blueprint and holds its own unique runtime state values.
- **Analogy:** The physical, structural house built out of brick and mortar using that paper sketch blueprint.

```java
// THE CLASS (Blueprint definition)
class BankAccount {
    public String accountHolder; // Field / Property
    public double balance;       // Field / Property

    public void deposit(double amount) { this.balance += amount; } // Method / Behavior
}

// --- Runtime Execution Logic ---
// THE OBJECTS (Concrete memory allocations)
BankAccount accountA = new BankAccount();
accountA.accountHolder = "Alice"; // Unique state

BankAccount accountB = new BankAccount();
accountB.accountHolder = "Bob";   // Distinct isolated state
```

### 🏛️ The 4 Pillars of OOP

These four conceptual pillars dictate how structural encapsulation protects data and how objects mimic real-world hierarchies.

```text
       ┌─────────────────────────────────────────────────────────┐
       │                    THE 4 PILLARS OF OOP                 │
       └────────────────────────────┬────────────────────────────┘
         ▲                          │                          ▲
         │                          ▼                          │
  ┌──────┴──────┐            ┌──────────────┐            ┌─────┴──────┐
  │Encapsulation│            │ Inheritance  │            │Polymorphic │
  │  [Data-Cap] │            │  [Identity]  │            │ [Override] │
  └─────────────┘            └──────┬───────┘            └────────────┘
                                    ▼
                             ┌──────────────┐
                             │ Abstraction  │
                             │ [Detail-Hide]│
                             └──────────────┘
```

#### 1. Encapsulation (Data Hiding & Protection)

- **Concept:** Bundling data fields and the methods that operate on them together inside one single unit (class), while restricting raw direct access from the outside world.
- **Implementation Rule:** Mark instance fields private and expose access strictly through controlled, well-validated public getter and setter method routines.
- **Code Example:**

```java
class SmartSafe {
    private int cashAmount = 0; // Shielded from raw outside changes

    public void addCash(int amount) {
        if (amount > 0) { this.cashAmount += amount; } // Controlled access validation
    }
    public int getBalance() { return this.cashAmount; }
}
```

#### 2. Abstraction (Hiding Complexity)

- **Concept:** Displaying only essential high-level structural features to the user while completely hiding the underlying low-level structural complexities.
- **Implementation Rule:** Implemented using abstract classes or interface contracts. The client interacts with simple action names without worrying about how those actions are processed underneath.
- **Code Example:**

```java
interface CoffeeMachine { void brewLatte(); } // User only sees a single clean action option
```

#### 3. Inheritance (Code Reuse & Hierarchy)

- **Concept:** The mechanic where a new class (subclass) automatically acquires properties and behaviors from an existing class (superclass), modeling a strict parent-child structure.
- **Implementation Rule:** Establishes the definitive "Is-A" relationship hierarchy using the extends keyword pattern.
- **Code Example:**

```java
class Employee { double salary = 50000; }
class Developer extends Employee { String coreLang = "Java"; } // Developer IS-AN Employee
```

#### 4. Polymorphism (Many Forms)

- **Concept:** The capability of an object or method execution path to take on multiple practical variations or behaviors depending on the target runtime context.
- **Implementation Rule:** Splits into two major engineering flavors:
  - **Compile-Time Polymorphism (Method Overloading):** Multiple methods inside the same class share an identical name but use different signature inputs.
  - **Runtime Polymorphism (Method Overriding):** A child class completely rewrites a method structure inherited from its parent class.
- **Code Example:**

```java
// Method Overriding (Runtime Polymorphism)
class Animal { void makeSound() { System.out.println("Generic sound"); } }
class Dog extends Animal { @Override void makeSound() { System.out.println("Woof!"); } }
```

### 🛠️ Fundamental Design Pragmatics: DRY & YAGNI

Beyond theoretical structure, senior architecture relies heavily on these two core pragmatic sanity checks to prevent code rot and save costs.

#### 1. DRY: Don't Repeat Yourself

- **The Rule:** Every piece of knowledge or functionality within a system must have a single, unambiguous, authoritative representation. Avoid copying and pasting calculation code blocks across separate locations.
- **Why it matters:** If an engineering equation blocks or logic rules change later, you only have to fix it in one location instead of hunting down duplicate code lines scattered throughout the repository.

#### 2. YAGNI: You Ain't Gonna Need It

- **The Rule:** Never build functionality or insert highly flexible code components under the assumption that "we might need this speculative capability down the road at some point." Only program features when they are explicitly requested.
- **Why it matters:** Over-engineering speculative infrastructure wastes time, adds unnecessary interface layers, introduces untested bug paths, and bloats the codebase with dead code that future developers are afraid to delete.

---

## 📝 Master Notes: Object-Oriented Programming (OOP) Relationships

Object-Oriented Design relies on establishing clear relationships between classes. These relationships dictate how objects communicate, reuse code, and manage memory.

### 🗺️ Quick Reference Summary Table (Sorted by Coupling Strength)

| Relationship Name | Conceptual Phrase | Structural Tool | Association Type | Coupling Strength | Lifecycle / Memory Rule |
|---|---|---|---|---|---|
| 1. Inheritance | "Is-A" | Abstract Class (extends) | Generalisation | 🔴 1. Tightest | Subclass inherits the exact structural identity of the parent. |
| 2. Realisation | "Can-Do" / "Implements-A" | Interface (implements) | Realisation | 🟠 2. Strong | Class promises to execute specific behaviors/contracts. |
| 3. Composition | "Has-A" (Strong Ownership) | Private Field + new in Constructor | Sub-type of Association | 🟡 3. Medium-Strong | Component is created inside and dies with the parent. |
| 4. Aggregation | "Has-A" (Weak Ownership) | Private Field + Parameter Passing | Sub-type of Association | 🟢 4. Medium-Weak | Component is passed in and survives if the parent dies. |
| 5. Association | "Knows-A" / "Interacts-With" | Private Fields (often bidirectional) | Base Association | 🔵 5. Weak | Peer-to-peer connection; both objects have fully independent lifecycles. |
| 6. Dependency | "Uses-A" | Method Parameter / Local Variable | Dependency | 💨 6. Loosest | Temporary relationship; exists only while the method runs. |

### 💻 Code Implementations & Rules

#### 1. Inheritance (Is-A)

- **Concept:** Defines core structural identity and hierarchical lineage.
- **Rule:** A class can only inherit from one abstract class to prevent identity confusion.
- **Code Implementation:**

```java
abstract class Vehicle {
    protected String fuelType;
    abstract void move();
}

// Car IS-A Vehicle
class Car extends Vehicle {
    @Override
    void move() { System.out.println("Driving on roads."); }
}
```

#### 2. Realisation (Can-Do / Implements-A)

- **Concept:** Defines plug-and-play capability and behavioral contracts.
- **Rule:** A class can implement multiple interfaces because a single object can have many different capabilities.
- **Code Implementation:**

```java
interface Chargeable {
    void plugIn();
}

// ElectricCar CAN-DO charging
class ElectricCar implements Chargeable {
    @Override
    public void plugIn() { System.out.println("Charging battery..."); }
}
```

#### 3. Composition (Has-A - Strong Ownership)

- **Concept:** Represents a strict "part-of" or "owns-a" relationship. The inner object cannot exist meaningfully without the container.
- **Rule:** The inner object is instantiated directly inside the container class.
- **Code Implementation:**

```java
class Engine { void fireCylinders() {} }

class Car {
    private final Engine engine; // Car HAS-A Engine (Strong)

    public Car() {
        this.engine = new Engine(); // Engine is created and dies with the Car
    }
}
```

#### 4. Aggregation (Has-A - Weak Ownership)

- **Concept:** Represents an independent whole-part association where the container groups or borrows the object. The inner object exists independently.
- **Rule:** The inner object is created outside and passed in via a constructor or setter.
- **Code Implementation:**

```java
class Wheel { }

class Car {
    private Wheel wheel; // Car HAS-A Wheel (Weak)

    public Car(Wheel externalWheel) {
        this.wheel = externalWheel; // Wheel is passed in from outside
    }
}
```

#### 5. Plain Association (Knows-A / Interacts-With)

- **Concept:** A peer-to-peer relationship with no ownership or whole-part containment. Objects just maintain a conceptual path of communication.
- **Rule:** Objects are passed in from the outside. Often implemented symmetrically (bidirectional) so both sides hold references to each other.
- **Code Implementation:**

```java
import java.util.*;

class Patient {
    private Doctor primaryDoctor; // Patient KNOWS-A Doctor
    public void setDoctor(Doctor doc) { this.primaryDoctor = doc; }
}

class Doctor {
    private List<Patient> patients = new ArrayList<>(); // Doctor KNOWS-A Patient
    public void addPatient(Patient p) { this.patients.add(p); }
}
```

#### 6. Dependency (Uses-A)

- **Concept:** Represents a temporary interaction. The class does not store or own the object; it just relies on it to complete a brief action.
- **Rule:** The object is passed purely as a temporary method argument.
- **Code Implementation:**

```java
class FuelPump { public void pumpGas() {} }

class Car {
    // Car USES-A FuelPump momentarily to execute this action
    public void refuel(FuelPump pump) {
        pump.pumpGas();
    } // The relationship ceases to exist when the method ends
}
```

### ✈️ The Real-World Analogy (Putting it all together)

Imagine modeling a Fighter Jet Simulation:

1. Inheritance (Is-A): The Jet is-an Aircraft. It shares structural properties common to all things that fly.
2. Realisation (Can-Do): The Jet can-do StealthCombat. This is a functional capability it implements.
3. Composition (Strong Has-A): The Jet has-a Fuselage (Body) created inside the factory. If the jet is destroyed, the body is destroyed too.
4. Aggregation (Weak Has-A): The Jet has-a Pilot. The pilot boards the jet to fly it, but can eject and survive independently if the jet crashes.
5. Plain Association (Knows-A): The Pilot knows-a FlightController back at headquarters. They talk to each other, but neither owns or contains the other.
6. Dependency (Uses-A): The Jet uses-an Airstrip to take off. The jet does not carry the runway with it; it simply interacts with it momentarily to complete a task.

The SOLID principles are a set of five design guidelines that make software patterns more understandable, flexible, and maintainable. They work by lowering the coupling strength between your classes using the exact relationships you just mastered.
Here is your complete guide to the SOLID principles, including detailed conceptual breakdowns and full structural code implementations for every rule.

---

## 📝 Master Notes: SOLID Design Principles

### 🗺️ Quick Reference Summary Table

| Principle | Full Name | Core Conceptual Goal | Smell that reveals the violation | Relationship Tool Used |
|---|---|---|---|---|
| S | Single Responsibility Principle | A class must have exactly one reason to change. | You use "and" to describe the class | Separation of Concerns |
| O | Open/Closed Principle | Open for extension, closed for modification. | `switch`/`if-else` on a type | Realisation / Inheritance |
| L | Liskov Substitution Principle | Subtypes must be completely substitutable for their base types. | An override that throws `UnsupportedOperationException` | Strict Is-A Rules |
| I | Interface Segregation Principle | Clients should not be forced to depend on methods they do not use. | Implementations with empty or throwing methods | Multiple Small Can-Dos |
| D | Dependency Inversion Principle | Depend on abstractions, not on concrete classes. | `new` on a collaborator inside a constructor | Dependency Injection |

> **How to read each principle below.** Every one follows the same four beats:
> **❌ Wrong** (the code) → **Why it's wrong** (the concrete failure, not a slogan)
> → **✅ Right** (the fix) → **What the fix bought you** (the test that now passes).
> If you cannot name the failure, you have not understood the principle — you have
> memorised its name.

### 💻 Code Implementations & Rules

#### 1. Single Responsibility Principle (SRP)

- **The Rule:** A class should have only one responsibility, meaning it has only one single reason to pivot or change its source code.
- **The Problem:** Mixing domain logic (like business math) with infrastructure logic (like saving files or printing output) in one class.
- **The smell:** you cannot describe the class without saying "**and**". *"`Invoice` holds the amount **and** writes it to disk."*

#### ❌ Wrong — Violating SRP

```java
class Invoice {
    private double amount;

    public Invoice(double amount) { this.amount = amount; }
    public void calculateTax() { this.amount *= 1.18; }

    // Violation: File persistence handling shouldn't live here
    public void saveToFile(String filename) {
        System.out.println("Writing invoice to " + filename);
    }
}
```

**Why this is wrong — the concrete damage:**

1. **Two unrelated teams edit the same file.** The tax rate changes when finance law
   changes; `saveToFile` changes when you migrate from disk to S3. Two reasons to
   change, one class — every edit risks breaking the other concern.
2. **You cannot unit-test the tax math without touching the filesystem.** The class
   drags an I/O dependency into every test of a pure arithmetic function.
3. **It cannot be reused.** A caller who wants invoice maths in a context with no
   filesystem (a Lambda, a browser via TeaVM, a batch job) still inherits the
   persistence code.
4. **The class grows without limit.** Once persistence is acceptable here, so is
   emailing, PDF rendering, and logging. SRP is the rule that stops the slide.

#### ✅ Right — Fulfilling SRP

```java
class Invoice {
    private double amount;

    public Invoice(double amount) { this.amount = amount; }
    public void calculateTax() { this.amount *= 1.18; }
    public double getAmount() { return amount; }
}

// Separate class handles persistence responsibility
class InvoiceRepository {
    public void saveToFile(Invoice invoice, String filename) {
        System.out.println("Writing amount " + invoice.getAmount() + " to " + filename);
    }
}
```

**What the fix bought you:** `Invoice` is now testable with no I/O at all, and swapping
disk for a database means writing a new repository — `Invoice` is never reopened.

> **Do not over-apply this.** SRP does not mean "one method per class". A responsibility
> is *a reason to change*, tied to a stakeholder, not a line count. Splitting `Invoice`
> into `InvoiceAmount`, `InvoiceTax` and `InvoiceId` is a worse design, not a purer one.

#### 2. Open/Closed Principle (OCP)

- **The Rule:** You should be able to add new features to a class via extension without changing any of its existing source code.
- **The Problem:** Using if/else or switch statements to check an object's type when running operations. Adding a new type forces you to edit the original code.
- **The smell:** a `switch` or `if-else` chain **on a type**. That is the signal, every time.

#### ❌ Wrong — Violating OCP

```java
class Rectangle { public double width, height; }
class Circle { public double radius; }

class AreaCalculator {
    // Violation: Not closed to modification
    public double calculateArea(Object shape) {
        if (shape instanceof Rectangle) {
            Rectangle r = (Rectangle) shape;
            return r.width * r.height;
        } else if (shape instanceof Circle) {
            Circle c = (Circle) shape;
            return Math.PI * c.radius * c.radius;
        }
        return 0;
    }
}
```

**Why this is wrong — the concrete damage:**

1. **Every new shape reopens tested code.** Adding `Triangle` means editing a class that
   already shipped and passed its tests. Re-testing the old paths is now your problem.
2. **`Object` as the parameter type discards all type safety.** `calculateArea("hello")`
   compiles fine and silently returns `0.0` — a wrong answer, not an error.
3. **The silent `return 0` is the worst part.** An unknown shape produces a plausible
   number instead of failing. This bug reaches production and corrupts a total.
4. **The chain gets duplicated.** Next sprint someone needs `perimeter()`, and copies the
   same `instanceof` ladder. Now a new shape means editing *two* places, then five.
5. **The knowledge is in the wrong place.** A circle's area formula belongs to `Circle`,
   not to a calculator that has to know every shape in the system.

#### ✅ Right — Fulfilling OCP

```java
interface Shape {
    double getArea(); // Contract for calculating area
}

class Rectangle implements Shape {
    private double width, height;
    public double getArea() { return width * height; }
}

class Circle implements Shape {
    private double radius;
    public double getArea() { return Math.PI * radius * radius; }
}

// Open to expansion, fully closed to modification
class AreaCalculator {
    public double calculateArea(Shape shape) {
        return shape.getArea(); // Relies cleanly on polymorphism
    }
}
```

**What the fix bought you:** the **extension test** — a new requirement costs *one new
class and zero edits*. Adding `Triangle implements Shape` touches nothing that already
works, and the compiler now rejects `calculateArea("hello")`.

> **The mechanical recipe** for this refactor: each `case` body becomes a class; the
> switch's return type becomes the interface method's return type; the switch variable
> disappears because *the object is the choice*; the caller passes the implementation in.

#### 3. Liskov Substitution Principle (LSP)

- **The Rule:** Objects of a subclass must behave exactly like objects of the superclass without breaking the system application if swapped.
- **The Problem:** Forcing a subclass to inherit from a parent class when it cannot realistically perform the parent's core behaviors.
- **The smell:** an override whose body is `throw new UnsupportedOperationException()`, or one that quietly does nothing.

#### ❌ Wrong — Violating LSP

```java
class Bird {
    public void fly() { System.out.println("Flying high!"); }
}

class Ostrich extends Bird {
    @Override
    public void fly() {
        // Violation: Breaks behavioral expectations of the parent class
        throw new UnsupportedOperationException("Ostriches cannot fly!");
    }
}
```

**Why this is wrong — the concrete damage:**

1. **It converts a compile-time guarantee into a runtime crash.** `List<Bird>` promises
   every element can `fly()`. That promise is now a lie the compiler cannot catch.
2. **Correct client code breaks.** `for (Bird b : birds) b.fly();` is a perfectly
   reasonable loop written against the base type. It now throws in production, and the
   author of the loop did nothing wrong.
3. **It forces callers to type-check**, which drags OCP down with it:
   `if (!(b instanceof Ostrich)) b.fly();` — the caller now knows every non-flying
   subclass, and each new one reopens that code.
4. **"Is-A" in English is not "Is-A" in code.** An ostrich *is* a bird biologically. LSP
   is about **behavioural** substitutability, not taxonomy. This is the trap.

> **The wider rule.** A subclass may **weaken preconditions** and **strengthen
> postconditions**, never the reverse. Also LSP-violating: an override that throws a
> *broader* checked exception, tightens an argument check the parent accepted, or returns
> `null` where the parent guaranteed a value.

#### ✅ Right — Fulfilling LSP

```java
abstract class Bird {
    abstract void eat();
}

abstract class FlyingBird extends Bird {
    abstract void fly();
}

class Eagle extends FlyingBird {
    void eat() { System.out.println("Eating fish."); }
    void fly() { System.out.println("Soaring high."); }
}

class Ostrich extends Bird {
    void eat() { System.out.println("Eating seeds."); }
    // No fly method exists here, keeping substitution safe
}
```

**What the fix bought you:** the error moved from runtime to compile time.
`List<FlyingBird>` cannot contain an `Ostrich` — the mistake is now *unrepresentable*
rather than merely detected. That is always the stronger fix.

#### 4. Interface Segregation Principle (ISP)

- **The Rule:** Write many small, specific interfaces instead of one massive, bloated interface. Clients should not be forced to implement options they do not need.
- **The Problem:** Designing a "fat" interface containing dozens of functions that only half of your concrete classes actually use.
- **The smell:** implementations padded with empty method bodies or `throw new UnsupportedOperationException()`.

#### ❌ Wrong — Violating ISP

```java
interface Worker {
    void work();
    void eat();
}

class Robot implements Worker {
    public void work() { System.out.println("Assembling parts."); }
    // Violation: Robots do not eat food, but are forced to handle the method
    public void eat() { throw new UnsupportedOperationException(); }
}
```

**Why this is wrong — the concrete damage:**

1. **It manufactures LSP violations.** Note that the fix for ISP and the fix for LSP are
   the same shape — a fat interface *forces* subclasses to lie about what they can do.
2. **Every implementer pays for every method.** Add `takeBreak()` to `Worker` and all
   implementations must be edited, including those it makes no sense for.
3. **The interface no longer documents anything.** `Worker` tells a reader nothing
   reliable, because half its methods may throw on any given instance.
4. **It couples unrelated clients.** A payroll module needing only `work()` still
   recompiles when the catering module changes `eat()`.

#### ✅ Right — Fulfilling ISP

```java
interface Workable { void work(); }
interface Feedable { void eat(); }

class Human implements Workable, Feedable {
    public void work() { System.out.println("Coding systems."); }
    public void eat() { System.out.println("Eating lunch."); }
}

// Robot only implements the capability it actually possesses
class Robot implements Workable {
    public void work() { System.out.println("Processing calculations."); }
}
```

**What the fix bought you:** a method signature can now demand exactly what it uses.
`void schedule(Workable w)` accepts both types; `void cater(Feedable f)` rejects `Robot`
**at compile time**. The type system enforces the rule that the comment used to.

#### 5. Dependency Inversion Principle (DIP)

- **The Rule:** High-level modules should not depend directly on low-level modules. Both must depend on abstractions (interfaces or abstract classes).
- **The Problem:** Hardcoding a concrete low-level implementation directly inside a high-level manager class using new. This sets up a rigid composition lock.
- **The smell:** `new SomeCollaborator()` inside a constructor or method body.

#### ❌ Wrong — Violating DIP

```java
class V8Engine {
    public void start() { System.out.println("Vroom!"); }
}

class Car {
    private V8Engine engine; // Violation: Tightly coupled to concrete class

    public Car() {
        this.engine = new V8Engine();
    }
}
```

**Why this is wrong — the concrete damage:**

1. **`Car` is untestable in isolation.** There is no seam. Every `Car` test starts a real
   `V8Engine`; if that engine opened a socket or hit a database, your unit test now needs
   the network.
2. **The choice is frozen at compile time.** Supporting an electric motor means editing
   `Car` — the exact OCP violation, arrived at from a different direction.
3. **`Car` owns a lifecycle it should not.** It decides when the engine is created and
   destroyed, so it cannot be given a shared or pooled one.
4. **The dependency is invisible.** `new Car()` gives no hint that an engine was
   constructed. A constructor parameter would have made it explicit and self-documenting.

#### ✅ Right — Fulfilling DIP

```java
interface Engine { void start(); }

class V8Engine implements Engine {
    public void start() { System.out.println("Vroom!"); }
}

class ElectricMotor implements Engine {
    public void start() { System.out.println("Silent hum..."); }
}

class Car {
    private Engine engine; // Clean: Depends entirely on abstraction

    // Engine variant is injected from the outside environment
    public Car(Engine engine) {
        this.engine = engine;
    }

    public void drive() { engine.start(); }
}
```

**What the fix bought you:** a **testing seam**. `new Car(() -> log.add("started"))` lets
you assert the engine was started without owning one. The guiding rule is
**inject what varies; construct what you own** — `Engine` comes in through the
constructor, but a `List<Passenger>` that `Car` genuinely owns is still built inside.

> **DIP is not "add an interface to everything."** If there is exactly one implementation
> and no second in sight, a plain class is the right answer (YAGNI, and the rule of
> three). Add the abstraction when the second variant arrives or when you need the test
> seam — not before.

### 🧭 The five smells, as one checklist

Scan your own code for these before an interviewer does. Each maps to exactly one letter:

| If you see this in the code | The principle broken | The move |
|---|---|---|
| "…and…" is needed to describe the class | **S** | Split the class |
| `switch` / `if-else` on a type | **O** | Each case becomes a class behind an interface |
| An override that throws `UnsupportedOperationException` | **L** | Fix the hierarchy — the subtype does not belong |
| An implementation full of empty methods | **I** | Split the interface into capabilities |
| `new` on a collaborator inside a constructor | **D** | Take it as a constructor parameter |

Note how **L** and **I** produce the same symptom from opposite ends, and how **O** and
**D** are usually the same bug seen from two angles. SOLID is five names for a smaller
number of underlying ideas: *put knowledge where the data is, depend on shapes rather
than things, and make illegal states impossible to express.*

### ✈️ The Real-World Analogy (Putting it all together)

Imagine running an Automobile Assembly Plant:

1. **Single Responsibility (SRP):** The worker who mounts tires only mounts tires. They do not calculate payroll bookkeeping.
2. **Open/Closed (OCP):** The conveyor line hooks onto assemblies via standard mounting brackets. You can attach a sedan frame or an SUV frame without building a brand-new factory floor layout.
3. **Liskov Substitution (LSP):** If a machine calls for a standard Bolt, you can use a titanium bolt or a steel bolt safely. If the steel bolt is shorter and slips out, it violates LSP.
4. **Interface Segregation (ISP):** The tool dashboard displays only the controls that the specific technician uses. The paint booth worker isn't forced to stare at controls for welding operations.
5. **Dependency Inversion (DIP):** The car chassis matches a generic engine bay interface spec. It doesn't care whether the logistics team drops in a gas engine or a hybrid engine module.

---

## 📝 Master Notes: Creational Design Patterns

Creational design patterns address the mechanisms of object creation. They optimize object instantiation by isolating the creation logic from the rest of the application, replacing direct constructor calls (new) with abstract interfaces to minimize coupling.

### 🗺️ Quick Reference Summary Table

| Pattern Name | Conceptual Phrase | Core Architectural Purpose | Relationship Mechanic Used |
|---|---|---|---|
| 1. Singleton | "There Can Be Only One" | Guarantees a class has exactly one global instance and provides a single access point to it. | Self-referencing Composition |
| 2. Factory Method | "Let Subclasses Choose" | Defines an interface for creating an object, but letting subclasses decide which concrete class to instantiate. | Inheritance (Is-A) & Realisation |
| 3. Abstract Factory | "Families of Products" | Provides an interface for creating families of related or dependent objects without specifying their concrete classes. | Composition (Has-A) + DIP Abstractions |
| 4. Builder | "Step-by-Step Construction" | Separates the complex step-by-step construction of an object from its final representation. | Aggregation (Has-A) |
| 5. Prototype | "Clone Yourself" | Creates new objects by copying an existing, fully configured instance instead of creating them from scratch. | Realisation (Can-Do) |

### 💻 Code Implementations & Rules

#### 1. Singleton Pattern

- **Concept:** Restricts instantiation of a class to one single object instance. It is perfect for shared global resources like a database connection pool or system logger.
- **Rule:** The constructor must be private, and the unique instance is stored as a static variable inside the class itself.

```java
class DatabaseConnection {
    // Stored inside the class itself
    private static DatabaseConnection instance;

    // Private Constructor prevents direct use of "new" outside this class
    private DatabaseConnection() {
        System.out.println("Initializing Database Connection Pool...");
    }

    // Global access point with lazy initialization
    public static synchronized DatabaseConnection getInstance() {
        if (instance == null) {
            instance = new DatabaseConnection();
        }
        return instance;
    }

    public void executeQuery(String sql) {
        System.out.println("Executing: " + sql);
    }
}
```

#### 2. Factory Method Pattern

- **Concept:** Outsources the instantiation logic to a specialized factory method. Subclasses override this method to change the type of object that will be created.
- **Rule:** The high-level code interacts purely with a standard interface, fulfilling the Open/Closed Principle.

```java
// Product Interface
interface Document { void open(); }

// Concrete Products
class PdfDocument implements Document { public void open() { System.out.println("Opening PDF."); } }
class WordDocument implements Document { public void open() { System.out.println("Opening Word doc."); } }

// Abstract Creator Class
abstract class DocumentApp {
    // Factory Method: Subclasses will implement this specific step
    abstract Document createDocument();

    public void openDocument() {
        Document doc = createDocument(); // Uses abstract assignment
        doc.open();
    }
}

// Concrete Creator implementations dictate object type
class PdfApp extends DocumentApp {
    Document createDocument() { return new PdfDocument(); }
}
```

#### 3. Abstract Factory Pattern

- **Concept:** A factory of factories. It provides a way to encapsulate a group of individual factories that have a common theme (a matching family of products) without specifying their concrete types.
- **Rule:** High-level code uses Dependency Inversion to swap out entire product suites dynamically at runtime.

```java
// Abstract Product Families
interface Button { void paint(); }
interface Checkbox { void render(); }

// Abstract Factory Blueprint
interface UIAppFactory {
    Button createButton();
    Checkbox createCheckbox();
}

// Concrete Mac Product Suite
class MacButton implements Button { public void paint() { System.out.println("Mac Button"); } }
class MacCheckbox implements Checkbox { public void render() { System.out.println("Mac Checkbox"); } }

class MacFactory implements UIAppFactory {
    public Button createButton() { return new MacButton(); }
    public Checkbox createCheckbox() { return new MacCheckbox(); }
}

// Client application uses total family abstraction via Aggregation
class Application {
    private Button button;
    private Checkbox checkbox;

    public Application(UIAppFactory factory) {
        this.button = factory.createButton();
        this.checkbox = factory.createCheckbox();
    }

    public void draw() { button.paint(); checkbox.render(); }
}
```

#### 4. Builder Pattern

- **Concept:** Avoids a giant constructor with dozens of parameters (known as the "telescoping constructor" anti-pattern). It allows you to build an immutable object step-by-step.
- **Rule:** The builder methods return a reference to this (the builder instance) to enable a readable, chained method layout syntax.

```java
class Computer {
    // All variables are marked immutable (final)
    private final String hdd;
    private final String ram;
    private final boolean isGraphicsCardEnabled;

    // Package-private or private constructor accepting the builder state
    private Computer(Builder builder) {
        this.hdd = builder.hdd;
        this.ram = builder.ram;
        this.isGraphicsCardEnabled = builder.isGraphicsCardEnabled;
    }

    // Static Inner Builder Class
    public static class Builder {
        private String hdd;
        private String ram;
        private boolean isGraphicsCardEnabled;

        public Builder setHDD(String hdd) { this.hdd = hdd; return this; }
        public Builder setRAM(String ram) { this.ram = ram; return this; }
        public Builder setGraphics(boolean choice) { this.isGraphicsCardEnabled = choice; return this; }

        // Final assembly checkpoint step
        public Computer build() {
            return new Computer(this);
        }
    }
}

// Usage syntax:
// Computer comp = new Computer.Builder().setHDD("1TB").setRAM("16GB").setGraphics(true).build();
```

#### 5. Prototype Pattern

- **Concept:** Instead of manually instantiating an identical new object and populating all its fields from scratch, you clone an existing baseline object.
- **Rule:** Implement a standard prototype cloning interface (Cloneable in Java) to execute a clean object copy operation.

```java
interface Prototype {
    Prototype clone();
}

class GameCharacter implements Prototype {
    private String weapon;
    private int health;

    public GameCharacter(String weapon, int health) {
        this.weapon = weapon;
        this.health = health;
    }

    // Copy constructor mechanic used inside clone implementation
    @Override
    public Prototype clone() {
        return new GameCharacter(this.weapon, this.health);
    }

    public void showStats() {
        System.out.println("Character with " + weapon + " | HP: " + health);
    }
}
```

### ✈️ The Real-World Analogy (Putting it all together)

Imagine managing an Automotive Manufacturing Complex:

1. Singleton: The centralized Factory Main Office. There is only one main office building managing operations across the entire grid. All communications route back through it.
2. Factory Method: The standard Assembly Line. The conveyor system framework is exactly the same, but line variant #1 creates and hooks up sedans, while line variant #2 overrides the process to assemble trucks.
3. Abstract Factory: The specialized Localization Supplier Contract. If the factory receives an export order for the UK market, the system switches entirely to the Right-Hand-Drive Parts Vendor, which supplies right-side dashboards alongside right-side steering setups together as a matched product ecosystem.
4. Builder: The custom Online Ordering Tool. When a buyer configures an exotic supercar, they step through sequential choices: picking exterior paint, selecting seating fabrics, and ticking optional audio packages. The final unique car is only constructed once all steps are checked.
5. Prototype: The Showroom Display Car. Instead of spending weeks custom designing a new vehicle frame from raw elements, manufacturing teams take the master physical model, build a duplicate stamp impression mold, and clone a perfect copy.

Here is your finalized, master cheat sheet on Behavioral Design Patterns, reordered precisely according to your sequence (with the accidental duplicate of "state" safely handled so your list flows seamlessly).
You can copy and paste this directly into your Markdown-compatible notes.

---

## 📝 Master Notes: Behavioral Design Patterns

Behavioral design patterns focus on algorithms and the assignment of responsibilities between objects. Instead of focusing on how objects are created or structurally organized, they optimize how objects communicate and operate together at runtime, using loose coupling to safely pass messages.

### 🗺️ Quick Reference Summary Table

| Pattern Name | Conceptual Phrase | Core Architectural Purpose | Relationship Mechanic Used |
|---|---|---|---|
| 1. Observer | "Publisher / Subscriber" | Defines a subscription mechanism to notify multiple "observer" objects automatically about any events on the subject. | Dynamic Aggregation List |
| 2. State | "Contextual Behavior" | Allows an object to alter its behavior when its internal state changes, appearing as if its class changed. | Composition (Has-A) + Polymorphism |
| 3. Command | "Action as an Object" | Encapsulates a request or action as a standalone object, allowing parameterization and undo operations. | Realisation (Can-Do) |
| 4. Visitor | "Separate the Operation" | Separates an algorithm from the object structure on which it operates, allowing you to add new operations cleanly. | Double Dispatch (Uses-A) |
| 5. Mediator | "Hub Communication" | Restricts direct communication between objects and forces them to collaborate only through a central hub. | Bidirectional Plain Association |
| 6. Iterator | "Sequential Access" | Accesses elements of a collection sequentially without exposing its underlying internal structure. | Interface Realisation |
| 7. Interpreter | "Grammar Evaluator" | Defines a grammatical representation for a language along with an interpreter to evaluate sentences. | Composite Inheritance |
| 8. Memento | "Undo / Snapshot" | Captures and externalizes an object's internal state so it can be restored later without violating encapsulation. | Strict inner-class isolation |
| 9. Chain of Responsibility | "Pass the Request" | Passes a request along a chain of potential handlers until one handles it. | Self-referencing Aggregation |
| 10. Template Method | "Define the Skeleton" | Defines the skeleton of an algorithm in a base class method, deferring some specific steps to subclasses. | Abstract Class Inheritance |

### 💻 Code Implementations & Rules

#### 1. Observer Pattern

- **Concept:** Setting up a subscription publisher channel framework. Multiple subscriber nodes listen to events inside a central model entity and process real-time structural notifications.
- **Rule:** The observed subject maintains a dynamic collection list of observer tracking nodes.

```java
import java.util.*;

interface Observer { void update(String news); }

class NewsChannel implements Observer {
    public void update(String news) { System.out.println("Breaking News: " + news); }
}

class NewsAgency {
    private List<Observer> observers = new ArrayList<>(); // Aggregation List

    public void attach(Observer o) { observers.add(o); }
    public void setNews(String news) {
        for (Observer o : observers) { o.update(news); } // Notify subscribers
    }
}
```

#### 2. State Pattern

- **Concept:** Cleanly swaps an entire system entity's runtime behavior based on internal state changes, avoiding massive switch/case matrices.
- **Rule:** Delegate work actions directly to a swappable state interface pointer reference variable.

```java
interface State { void pressPlay(VlcPlayer player); }

class PlayState implements State {
    public void pressPlay(VlcPlayer player) { System.out.println("Pausing audio stream..."); player.setState(new PauseState()); }
}
class PauseState implements State {
    public void pressPlay(VlcPlayer player) { System.out.println("Resuming playback..."); player.setState(new PlayState()); }
}

class VlcPlayer {
    private State currentState = new PauseState(); // Composition Context Hook
    public void setState(State state) { this.currentState = state; }
    public void pushButton() { currentState.pressPlay(this); }
}
```

#### 3. Command Pattern

- **Concept:** Turns a request or an execution script into a standalone object. This decoupling allows you to queue commands, pass them across parameters, or log actions.
- **Rule:** Create a simple command execution interface contract containing an execute() method.

```java
interface Command { void execute(); }

// Receiver
class Light { public void turnOn() { System.out.println("Light is ON"); } }

// Concrete Command
class LightOnCommand implements Command {
    private Light light; // Aggregation
    public LightOnCommand(Light light) { this.light = light; }
    public void execute() { light.turnOn(); }
}

// Invoker
class RemoteControl {
    private Command slot;
    public void setCommand(Command command) { this.slot = command; }
    public void pressButton() { slot.execute(); }
}
```

#### 4. Visitor Pattern

- **Concept:** Allows you to add new operations or analytical features to an existing object hierarchy without modifying the source code of those target structures.
- **Rule:** Uses a routing technique called Double Dispatch where elements provide an accept(Visitor v) pipeline method wrapper.

```java
interface Element { void accept(Visitor visitor); }
interface Visitor { void visit(Book book); }

class Book implements Element {
    public int price = 50;
    public void accept(Visitor visitor) { visitor.visit(this); } // Double dispatch
}

class DiscountVisitor implements Visitor {
    public void visit(Book book) {
        System.out.println("Discount price: " + (book.price * 0.8));
    }
}
```

#### 5. Mediator Pattern

- **Concept:** Forces complex peer-to-peer component interactions to route through a single coordinator hub instead of components referencing each other directly, eliminating tight spaghetti coupling.
- **Rule:** Components talk exclusively to the mediator instance instead of making raw target calls.

```java
interface ChatMediator { void sendMessage(String msg, User user); }

abstract class User {
    protected ChatMediator mediator; // Plain Association to Hub
    protected String name;
    public User(ChatMediator med, String name) { this.mediator = med; this.name = name; }
    public abstract void send(String msg);
    public abstract void receive(String msg);
}

class ChatUser extends User {
    public ChatUser(ChatMediator med, String name) { super(med, name); }
    public void send(String msg) { mediator.sendMessage(msg, this); }
    public void receive(String msg) { System.out.println(name + " received: " + msg); }
}
```

#### 6. Iterator Pattern

- **Concept:** Loops through elements inside a data container collection sequentially without needing to know what data structure (array, linked list, tree) is running under the hood.
- **Rule:** The iterator encapsulates tracking variables like indices or structural collection pointers inside an independent iterator object.

```java
import java.util.*;

interface Iterator { boolean hasNext(); Object next(); }

class NameCollection {
    public String[] names = {"Alice", "Bob", "Charlie"};

    public Iterator getIterator() { return new NameIterator(); }

    // Inner class manages tracking encapsulation safely
    private class NameIterator implements Iterator {
        int index = 0;
        public boolean hasNext() { return index < names.length; }
        public Object next() { return hasNext() ? names[index++] : null; }
    }
}
```

#### 7. Interpreter Pattern

- **Concept:** Used to define a structural grammar rule for evaluating simple expressions or custom mini-languages.
- **Rule:** Evaluates expressions using a recursive data hierarchy containing terminal and non-terminal nodes.

```java
interface Expression { boolean interpret(String context); }

// Terminal Expression rule
class TerminalExpression implements Expression {
    private String data;
    public TerminalExpression(String data) { this.data = data; }
    public boolean interpret(String context) { return context.contains(data); }
}

// Non-Terminal Expression rule (OR logic helper)
class OrExpression implements Expression {
    private Expression expr1, expr2;
    public OrExpression(Expression e1, Expression e2) { this.expr1 = e1; this.expr2 = e2; }
    public boolean interpret(String context) { return expr1.interpret(context) || expr2.interpret(context); }
}
```

#### 8. Memento Pattern

- **Concept:** Takes a complete snapshot clone of an object's internal memory state without exposing its private fields to the outside world, allowing easy state restorations.
- **Rule:** Keep snapshot fields completely immutable inside an isolated inner metadata token class.

```java
class Editor {
    private String content;
    public void write(String text) { this.content = text; }

    // Creates the historical token blueprint box
    public Memento save() { return new Memento(content); }
    public void restore(Memento memento) { this.content = memento.getState(); }

    public static class Memento {
        private final String state; // Immutable snapshot state
        private Memento(String state) { this.state = state; }
        private String getState() { return state; }
    }
}
```

#### 9. Chain of Responsibility Pattern

- **Concept:** Avoids coupling the sender of a request to its receiver by giving more than one object a chance to handle the request.
- **Rule:** Each handler contains a field referencing the next handler in the sequence chain.

```java
abstract class SupportHandler {
    protected SupportHandler nextHandler;

    public void setNext(SupportHandler nextHandler) { this.nextHandler = nextHandler; }

    public abstract void handleRequest(String severity);
}

class Level1Support extends SupportHandler {
    public void handleRequest(String severity) {
        if (severity.equals("LOW")) {
            System.out.println("Level 1 fixed it.");
        } else if (nextHandler != null) {
            nextHandler.handleRequest(severity); // Pass along the chain
        }
    }
}
```

#### 10. Template Method Pattern

- **Concept:** Defines the broad skeleton workflow of an algorithm step chain inside a base class method, allowing subclasses to fill in specific implementation details without modifying the layout sequence.
- **Rule:** Mark the base algorithm processing flow method wrapper final to ensure consistency.

```java
abstract class GameLoader {
    // Template Method defining the explicit pipeline execution layout sequence
    public final void runPipeline() {
        initialize();
        loadAssets();
        cleanup();
    }
    protected void initialize() { System.out.println("Allocating core memory blocks..."); }
    protected abstract void loadAssets(); // Subclass overrides this step hook
    protected void cleanup() { System.out.println("Opening server endpoints."); }
}

class MarioGame extends GameLoader {
    protected void loadAssets() { System.out.println("Extracting 2D sprites sheets..."); }
}
```

### ✈️ The Real-World Analogy (Putting it all together)

Imagine running a complex International Airport Terminal Hub:

1. Observer: The flight departure arrival status TV display boards. Whenever a flight destination arrival state gets updated inside the master database, every target flight monitor panel screen throughout the terminal blinks to show the new timeline updates.
2. State: Security gate access lines. If the machine security state is flagged as Green, passengers pass through. If checking systems detect a warning issue, the scanner gate transitions to Lockdown Red State, altering how the terminal lane door mechanisms handle attempts to step forward.
3. Command: The control tower control boards. When an operator hits the runway illumination switch, that action is wrapped up as a specific signal instruction command, placed inside a processing queue, and executed securely.
4. Visitor: Custom Border Enforcement Audits. Instead of altering individual airplane structures to perform specialized inspections, a specialized inspection dog task force visits the plane cabins, scanning rows of items without altering anything about the plane itself.
5. Mediator: Air Traffic Control Tower. Instead of individual aircraft pilots calling every other flying aircraft directly to negotiate terminal lane landings, they cross-route information strictly through the central tower controllers.
6. Iterator: The terminal bus passenger shuttle. The driver collects travellers sequentially one by one from the departure lounges until full, entirely ignoring passengers' specific nationalities or flight tickets.
7. Interpreter: The international customs landing form check sheet. Automated machines scan paper travel visa symbols and translate those markup markings to verify immigration entry rules.
8. Memento: The digital check-in flight booking ledger. If an agent makes an error seat reservation entry, they can use the "revert system action" tool to pull up the previous timestamp memory snapshot state.
9. Chain of Responsibility: Luggage security scanning operations. Checked bags pass through standard scanners (Level 1). If an item looks suspicious, it escalates to the explosive analyzer (Level 2), and finally to manual inspection (Level 3).
10. Template Method: The flight departure process blueprint layout. The master operational framework remains exactly the same for all commercial journeys: passengers execute check-in, clear security check lines, board the aircraft, and take off. Sub-airlines simply customize their specific cabin boarding processes.

Here is your final, complete master note module covering Structural Design Patterns, organized precisely in your requested order.
Structural design patterns explain how to assemble objects and classes into larger, more flexible structures. They use composition and inheritance to make independently developed class libraries work together seamlessly.

---

## 📝 Master Notes: Structural Design Patterns

### 🗺️ Quick Reference Summary Table (Ordered as Requested)

| Pattern Name | Conceptual Phrase | Core Architectural Purpose | Relationship Mechanic Used |
|---|---|---|---|
| 1. Adapter | "The Translator" | Converts an incompatible interface of a class into another interface that clients expect. | Aggregation or Inheritance |
| 2. Bridge | "Independent Axes" | Decouples an abstraction from its implementation so that the two can vary and scale independently. | Aggregation (The Bridge) |
| 3. Composite | "Tree Hierarchy" | Composes objects into tree structures to represent part-whole hierarchies, treating single items and collections uniformly. | Recursive Aggregation |
| 4. Decorator | "Dynamic Wrapper" | Attaches new behaviors or responsibilities to an object dynamically without changing its underlying structure. | Recursive Aggregation + Realisation |
| 5. Flyweight | "Shared Optimization" | Minimizes memory usage by sharing common immutable parts of data across thousands of similar objects. | Plain Association / Factory Pool |
| 6. Facade | "Simplified Gateway" | Provides a single, unified high-level interface to a complex subsystem of classes or APIs. | Aggregation of Subsystems |
| 7. Proxy | "The Gatekeeper" | Provides a surrogate or placeholder object to control access, manage lazy loading, log actions, or handle security. | Composition / Realisation |

### 💻 Code Implementations & Rules

#### 1. Adapter Pattern

- **Concept:** Acts as an intermediary wrapper between two incompatible interfaces. It catches requests from a client and translates them into a format that a legacy or external service can understand.
- **Rule:** The adapter implements the target client interface and holds a reference to the incompatible object (the adaptee).

```java
// Target Client Interface
interface ModernCharging { void chargeWithUsbC(); }

// Incompatible Adaptee
class OldPhone { public void chargeWithMicroUsb() { System.out.println("Charging slowly..."); } }

// Adapter Class: Maps OldPhone to ModernCharging
class CableAdapter implements ModernCharging {
    private OldPhone oldPhone; // Aggregation/Composition hook

    public CableAdapter(OldPhone phone) { this.oldPhone = phone; }

    @Override
    public void chargeWithUsbC() {
        System.out.println("Translating USB-C signal to Micro-USB...");
        oldPhone.chargeWithMicroUsb(); // Delegation
    }
}
```

#### 2. Bridge Pattern

- **Concept:** Avoids a "Cartesian product" explosion of classes (e.g., creating RedCircle, BlueCircle, RedSquare, BlueSquare). It splits a massive class concept into two distinct, independent hierarchies: Abstraction (what it does) and Implementation (how it does it).
- **Rule:** The abstraction class holds a reference field (the bridge) pointing to the implementation interface type.

```java
// Implementation Hierarchy Axis
interface Color { void applyColor(); }
class Red implements Color { public void applyColor() { System.out.println("Painting Red."); } }

// Abstraction Hierarchy Axis
abstract class Shape {
    protected Color color; // The Bridge (Aggregation link)
    protected Shape(Color color) { this.color = color; }
    abstract void draw();
}

class Circle extends Shape {
    public Circle(Color color) { super(color); }
    void draw() { System.out.print("Drawing Circle: "); color.applyColor(); }
}
```

#### 3. Composite Pattern

- **Concept:** Allows clients to work with nested hierachies (like file structures or UI elements) uniformly. You can treat an individual leaf item or a composite group containing items exactly the same way.
- **Rule:** Both leaf items and composite folders must implement the exact same base component interface layout.

```java
import java.util.*;

// Unified Component
interface SystemComponent { void showDetails(); }

// Leaf Object
class FileItem implements SystemComponent {
    private String name;
    public FileItem(String name) { this.name = name; }
    public void showDetails() { System.out.println("File: " + name); }
}

// Composite Object (Contains Leaves and other Composites)
class DirectoryFolder implements SystemComponent {
    private List<SystemComponent> children = new ArrayList<>(); // Recursive Aggregation

    public void addComponent(SystemComponent comp) { children.add(comp); }

    public void showDetails() {
        for (SystemComponent comp : children) { comp.showDetails(); }
    }
}
```

#### 4. Decorator Pattern

- **Concept:** Wraps a target object inside special wrapper layers to dynamically add responsibilities at runtime without modifying original class structures or relying on rigid inheritance subclassing.
- **Rule:** The decorator implements the target component interface and wraps a component field instance inside it.

```java
interface Coffee { double getCost(); }
class PlainCoffee implements Coffee { public double getCost() { return 10.0; } }

// Abstract Decorator
abstract class CoffeeDecorator implements Coffee {
    protected Coffee decoratedCoffee; // Wrapper field pointer link
    public CoffeeDecorator(Coffee coffee) { this.decoratedCoffee = coffee; }
    public double getCost() { return decoratedCoffee.getCost(); }
}

// Concrete Decorator
class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) { super(coffee); }
    @Override
    public double getCost() { return super.getCost() + 3.5; } // Enriches behavior
}
```

#### 5. Flyweight Pattern

- **Concept:** Saves massive amounts of RAM when rendering thousands of identical heavy objects (like particles, tree graphics, or text characters) by pulling shared immutable data out into a shared pool.
- **Rule:** State is split into Intrinsic (shared, internal data stored in the flyweight) and Extrinsic (unique, contextual data passed into methods from the outside).

```java
import java.util.*;

// Flyweight containing shared Intrinsic state (Memory Optimized)
class TreeType {
    private String texture, color; // Immutable data
    public TreeType(String texture, String color) { this.texture = texture; this.color = color; }
    public void display(int x, int y) { /* Uses Extrinsic coordinates passed in */ }
}

// Factory to manage flyweight sharing pool
class TreeFactory {
    private static Map<String, TreeType> pool = new HashMap<>();
    public static TreeType getTreeType(String texture, String color) {
        String key = texture + "-" + color;
        pool.putIfAbsent(key, new TreeType(texture, color));
        return pool.get(key);
    }
}
```

#### 6. Facade Pattern

- **Concept:** Acts as a simplified entryway to a complex framework, library, or multi-class subsystem. Instead of forcing a client to interact with ten different complex API modules, it exposes a single simple method wrapper.
- **Rule:** The Facade coordinates interactions behind the scenes but does not encapsulate or hide the subsystem classes entirely if advanced users need them.

```java
class SoundSystem { public void turnOn() {} }
class Projector { public void start() {} }

// Facade provides one simple interface hook to the client
class HomeTheaterFacade {
    private SoundSystem audio = new SoundSystem(); // Groups subsystem
    private Projector video = new Projector();

    public void watchMovie() {
        System.out.println("Configuring theatre environment parameters...");
        video.start();
        audio.turnOn();
    }
}
```

#### 7. Proxy Pattern

- **Concept:** Acts as an intermediary gatekeeper or substitute placeholder for a real heavy object. It intercepts client calls to perform actions before or after the request reaches the target object (e.g., access security, caching, or lazy initialization).
- **Rule:** The Proxy implements the exact same interface contract as the real concrete subject object.

```java
import java.util.*;

interface InternetAccess { void browseSite(String url); }
class RealInternet implements InternetAccess {
    public void browseSite(String url) { System.out.println("Connecting to: " + url); }
}

// Proxy controls and guards access to the real service
class ProtectedInternetProxy implements InternetAccess {
    private RealInternet realInternet = new RealInternet(); // Composition link
    private List<String> bannedSites = Arrays.asList("darkweb.com", "malicious.io");

    @Override
    public void browseSite(String url) {
        if (bannedSites.contains(url.toLowerCase())) {
            System.out.println("ACCESS DENIED: Blocked by firewall rules.");
            return;
        }
        realInternet.browseSite(url); // Forwards request if safe
    }
}
```

### ✈️ The Real-World Analogy (Putting it all together)

Imagine traveling through a massive Modern International Transit Hub Hotel:

1. Adapter: Your travel laptop wall charger setup. The hotel wall socket uses standard UK prongs, but your laptop chord has a US flat layout prong. You snap on a physical Adapter block to safely translate the electricity current flow lines.
2. Bridge: The hotel's room remote control systems. The remote design layout (Abstraction axis) can change from simple buttons to touchscreens, and the target room electronics (Implementation axis) can change from smart blinds to automated HVAC units. They evolve independently on separate design paths.
3. Composite: The delivery shipping crates in the cargo zone. A custom container box contains five medium parcels. Each parcel contains ten tiny envelopes. Security crews scan the primary master crate or individual envelope components uniformly using the same scanning procedure protocol.
4. Decorator: A custom standard espresso ordered at the hotel café bar. You start with basic plain coffee. You dynamically layer on milk toppings, add a dash of sugar syrup, and dust on cinnamon. The coffee remains a coffee entity, but its profile expands dynamically with each wrapper choice.
5. Flyweight: The room layout interior design blueprints. Instead of generating thousands of independent geometric model definitions for every single screw, hanger, and light bulb fixture in the hotel, architects reference one global master shared structural specification instance to optimize memory space.
6. Facade: The hotel concierge helper desk lobby counter. Instead of a guest walking down to the basement to talk to laundry staff, calling the kitchen chefs directly, and running to the valet station yourself, you talk to one single coordinator agent who manages the entire subsystem behind the scenes.
7. Proxy: The secure electronic keycard lock on your hotel room door. You cannot interact with or touch your physical bed or luggage until your keycard credentials are encrypted, verified, and authenticated by the proxy lock device sentinel.

You now have a complete, comprehensively structured software engineering textbook module spanning Object-Oriented Relationships, SOLID Principles, Creational patterns, Behavioral patterns, and Structural patterns.

MISLANNNIOUS

We are about 90% of the way through a world-class theoretical notebook, but we are missing a few critical topics.
If you were to walk into a senior engineering interview or an advanced system architecture exam right now, there are five hidden conceptual gaps that an interviewer could use to catch you off guard.
These micro-concepts bridge the gap between basic code formatting and low-level memory mechanics. Review these final modules to complete your notes.

---

## 📝 Master Notes: Advanced Theoretical Underpinnings of OOP

### 🗺️ Quick Reference Summary Table

| Concept Name | Technical Definition | Core System Impact | Real-World Analogy |
|---|---|---|---|
| Cohesion vs. Coupling | Measures functional focus vs. inter-class reliance. | Controls system maintainability. | A specialized solo mechanic vs. a messy assembly line. |
| Composition over Inheritance | Paradigm shift prioritizing object nesting over sub-classing. | Eliminates rigid parent-child locks. | Plugging in a modern phone battery vs. grafting an limb. |
| Object Cloning | Copying memory buffers (Shallow vs. Deep). | Dictates variable state safety. | Copying a file shortcut vs. duplicating the actual folder. |
| The Diamond Problem | Ambiguity caused by multiple inheritance paths. | Causes runtime method collisions. | Two managers giving conflicting orders to one worker. |
| KISS & Law of Demeter | Keep it Simple, and talk only to your immediate neighbors. | Minimizes structural code complexity. | Paying the cashier directly vs. letting them reach into your wallet. |

### 💻 Technical Explanations & Rules

#### 1. Cohesion vs. Coupling

These two metrics determine the health and lifespan of your architecture.

- **High Cohesion (The Goal):** A class should do exactly one thing and do it completely. All properties and methods must tightly relate to the class's single purpose.
- **Loose Coupling (The Goal):** Classes should have minimal knowledge of and dependence on other classes. If class A changes, class B should not break.

```java
// ❌ High Coupling & Low Cohesion: Order handles emails, databases, and billing.
class BadOrderProcessor { ... }

//  Low Coupling & High Cohesion: Order ONLY handles order math. Enforces loose aggregation.
class CleanOrderProcessor {
    private NotificationService notifier; // Decoupled through interface contract
}
```

#### 2. Shallow Copy vs. Deep Copy (Object Cloning)

When duplicating an object in memory, how you handle its internal reference pointers changes everything.

- **Shallow Copy:** Copies the root object primitive values, but copies references for nested objects. The original and cloned object still point to the same internal object in the memory heap.
- **Deep Copy:** Recursively copies the root object and allocates entirely new memory blocks for all inner child objects. They are 100% disconnected.

```java
class Wallet { int cash = 50; }
class Person { Wallet wallet = new Wallet(); }

// Runtime Impact:
// Shallow Copy: clone.wallet.cash = 0;  <-- ALSO empties the original person's cash!
// Deep Copy:    clone.wallet.cash = 0;  <-- Original person's cash stays at 50 safely.
```

#### 3. The Diamond Problem (Multiple Inheritance)

- **The Concept:** If a language allows a class to inherit from multiple parent classes (like C++), a classic ambiguity trap arises.
- **The Scenario:** Class A has a method start(). Class B and Class C inherit from A and both override start(). If Class D inherits from both B and C, and calls start(), which method does it run?
- **The Rule:** Languages like Java, C#, and Dart banned multiple inheritance of classes outright to prevent this trap. They force you to use Multiple Interfaces (Realisation), where no method body exists to cause conflict.

```text
       ┌───────────────┐
       │   Class A     │  <- Declares start()
       └───────┬───────┘
       ┌───────┴───────┐
       ▼               ▼
┌──────────────┐┌──────────────┐
│   Class B    ││   Class C    │  <- Both override start()
└───────┬───────┘└───────┬───────┘
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │   Class D     │  <- Inherits both! Which start() executes? (AMBIGUITY)
       └───────────────┘
```

#### 4. Pragmatics Addendum: KISS & Law of Demeter

Alongside DRY and YAGNI, add these two standard operational guardrails to your design system:

- **KISS (Keep It Simple, Stupid):** Avoid nesting systems inside loops inside design patterns unless absolutely necessary. If a basic loop can clearly solve a problem, do not engineer a recursive Visitor pattern to handle it.
- **Law of Demeter (Principle of Least Knowledge):** A method of an object should only call methods of its immediate neighbors. It should never navigate through long reference chains (e.g., avoid customer.getWallet().getCard().charge()).
- **The Fix:** Delegate inside the neighbor instead: customer.chargePayment().

### ✈️ The Real-World Analogy (Putting it all together)

Let's look back at our Fighter Jet Simulation to map these hidden theories:

1. High Cohesion: The RadarSystem class only processes wave frequencies. It doesn't keep track of the pilot's lunch breaks or fuel metrics.
2. Loose Coupling: The cockpit dashboard connects to the engine using a standard data bus wire. You can swap out a gas turbine engine for a hydrogen core without redesigning the dashboard screen displays.
3. Shallow vs. Deep Copy: If you clone a jet profile layout in software:
   - A Shallow Copy duplicates the dashboard shell but points to the exact same underlying electrical wire hub. Snipping a wire in the clone breaks the original jet.
   - A Deep Copy manufactures a completely isolated electrical wire hub wire-by-wire for the duplicate jet.
4.
5. The Diamond Problem: The flight control module cannot accept direct, overriding heading telemetry instructions from the navigation mapping AI and the collision avoidance AI at the exact same priority window level. The system blocks multiple parent command sources, routing inputs through a singular pilot prioritization pipeline.
6. Law of Demeter: The control tower agent tells the pilot: "Land on Runway 2." The tower agent doesn't reach into the cockpit cabin, grab the control stick, flip the wing flaps, and execute the physical wheel landing themselves.

With these final architectural mechanics, memory behaviors, and paradigm constraints locked down, your theoretical OOP handbook is completely comprehensive.

---

## 📝 Master Notes: Object Contracts (`equals`, `hashCode`, `toString`, ordering)

Java's collections are not magic — they are built on a **contract** your classes must
honour. Break it and `HashMap` silently loses your data. No exception, no warning.

### 🗺️ Quick Reference Summary Table

| Method | Inherited default | What breaks if you skip it |
|---|---|---|
| `equals(Object)` | reference identity (`==`) | Two logically identical objects compare unequal |
| `hashCode()` | memory-derived int | `HashMap`/`HashSet` lookups miss; duplicates appear in a `Set` |
| `toString()` | `ClassName@1b6d3586` | Every log line and debugger view is useless |
| `compareTo(T)` | not present | `TreeMap`, `Collections.sort` throw `ClassCastException` |

#### The five rules of `equals`

An `equals` implementation must be **reflexive** (`a.equals(a)`), **symmetric**
(`a.equals(b) == b.equals(a)`), **transitive**, **consistent** (same answer every call),
and `a.equals(null)` must be `false`.

#### ❌ Wrong — `equals` without `hashCode`

```java
class Point {
    private final int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Point)) return false;
        Point p = (Point) o;
        return x == p.x && y == p.y;
    }
    // Violation: hashCode not overridden — still uses identity
}
```

**Why this is wrong — the concrete damage:**

1. `new Point(1,2).equals(new Point(1,2))` is `true`, but their hash codes differ, so a
   `HashMap` puts them in **different buckets**. You `put` with one and `get` with the
   other and receive `null`.
2. `Set<Point>` will happily hold two "equal" points — the set is no longer a set.
3. There is **no error message**. This is the single most expensive silent bug in Java,
   and interviewers ask about it precisely because it fails quietly.

**The contract in one line:** *equal objects must have equal hash codes.* The reverse is
not required — unequal objects may collide, and that is fine.

#### ✅ Right — the pair, written together

```java
import java.util.Objects;

final class Point {
    private final int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;                 // fast path
        if (!(o instanceof Point p)) return false;  // handles null too
        return x == p.x && y == p.y;
    }

    @Override
    public int hashCode() { return Objects.hash(x, y); }

    @Override
    public String toString() { return "Point(" + x + ", " + y + ")"; }
}
```

#### The inheritance trap: `equals` cannot be both symmetric and subclass-friendly

```java
// (assume Point above were not final)
class ColorPoint extends Point {  // adds a colour field
    // Any equals here either breaks symmetry (Point.equals(ColorPoint) != reverse)
    // or breaks transitivity. There is no correct answer.
}
```

**Why this is wrong:** if `ColorPoint.equals` requires colour to match but
`Point.equals` does not, then `p.equals(cp)` is `true` while `cp.equals(p)` is `false` —
**symmetry is broken**. Widening `Point.equals` to ignore colour breaks transitivity
instead. This is a genuine theoretical limit, not a puzzle with a hidden solution.

**How to improve:** *favour composition over inheritance for value types.* Give
`ColorPoint` a `Point` field rather than extending it. Or use `instanceof` semantics and
document that subclasses may not add value fields — which is why Java's own value-like
classes (`String`, `Integer`, and every `record`) are `final`.

#### Ordering: `Comparable` vs `Comparator`

- **`Comparable<T>`** — the class's *one natural order*. `implements Comparable<Task>`,
  method `int compareTo(Task o)`. Use for the ordering that is intrinsic to the type.
- **`Comparator<T>`** — an *external, swappable* order. This is the **Strategy pattern**
  applied to sorting, which is why it is the answer to "sort comments by score, then by
  date" in an LLD round.

```java
import java.util.*;

record Task(String title, int priority, long createdAt) implements Comparable<Task> {
    @Override
    public int compareTo(Task o) { return Integer.compare(priority, o.priority); }
}

class Ordering {
    static final Comparator<Task> BY_PRIORITY_THEN_AGE =
        Comparator.comparingInt(Task::priority)
                  .thenComparingLong(Task::createdAt)
                  .reversed();
}
```

> **The consistency rule:** `compareTo` should return `0` exactly when `equals` returns
> `true`. `TreeSet` uses `compareTo`, `HashSet` uses `equals` — if they disagree, the two
> collections give different answers about the same "duplicate", which is how
> `BigDecimal("1.0")` and `BigDecimal("1.00")` bite people.
>
> **Never write `return a.priority - b.priority`.** It overflows for large ints and
> returns the wrong sign. Use `Integer.compare`.

---

## 📝 Master Notes: Immutability and `record`

An **immutable** object cannot change after construction. This is not a stylistic
preference — it removes entire categories of bug.

### 🗺️ Why immutability wins

| Property | What it gives you |
|---|---|
| No setters | No object can be corrupted mid-flight by another module |
| Inherently thread-safe | No locking needed; nothing can change while a thread reads |
| Safe as a `Map` key | Its `hashCode` cannot drift after insertion |
| Free to share | No defensive copying on the way out |
| Trivially cacheable | State and identity coincide |

#### ❌ Wrong — mutable, with leaked internals

```java
import java.util.*;

class Order {
    private String id;
    private List<String> items;

    public Order(String id, List<String> items) {
        this.id = id;
        this.items = items;        // Violation: stores caller's list
    }
    public void setId(String id) { this.id = id; }
    public List<String> getItems() { return items; }  // Violation: hands it back
}
```

**Why this is wrong — the concrete damage:**

1. **The constructor does not defend.** The caller keeps a reference to `items` and can
   add to it later. Your `Order` changes behind your back.
2. **The getter leaks the same reference.** `order.getItems().clear()` empties the order
   from the outside — encapsulation is fiction here.
3. **`setId` makes it unusable as a `HashMap` key.** Mutate the id after insertion and
   the entry becomes unreachable, exactly as in the `hashCode` case above.
4. **It cannot be shared between threads** without external synchronisation.

#### ✅ Right — the five rules of immutability

```java
import java.util.*;

final class Order {                              // 1. class is final
    private final String id;                     // 2. all fields final and private
    private final List<String> items;

    public Order(String id, List<String> items) {
        this.id = id;
        this.items = List.copyOf(items);         // 3. defensive copy IN
    }

    public String id() { return id; }
    public List<String> items() { return items; } // 4. immutable view OUT — no setters

    // 5. "modification" returns a new instance
    public Order withItemAdded(String item) {
        List<String> next = new ArrayList<>(items);
        next.add(item);
        return new Order(id, next);
    }
}
```

#### `record` — immutability as one line

A `record` generates the constructor, private final fields, accessors, `equals`,
`hashCode`, and `toString` for you. Use it for every **value type** (DTOs, coordinates,
money, events, keys).

```java
import java.util.*;

record Money(String currency, long minorUnits) {
    // compact constructor: validation and normalisation
    Money {
        Objects.requireNonNull(currency);
        if (minorUnits < 0) throw new IllegalArgumentException("negative amount");
    }
    Money plus(Money o) {
        if (!currency.equals(o.currency)) throw new IllegalArgumentException("currency mismatch");
        return new Money(currency, minorUnits + o.minorUnits);
    }
}
```

> **What a `record` is not.** It is *shallowly* immutable — a `record Box(List<String> xs)`
> still leaks a mutable list unless the compact constructor copies it. Records are also
> implicitly `final`, cannot extend a class, and are the wrong choice for an entity with
> identity and a lifecycle (`Order` in a real system has a mutable status; `Money` does not).

---

## 📝 Master Notes: Concurrency and Thread Safety

Most LLD problems end with *"now make it work with a thousand concurrent users."*
This section is what that follow-up is testing.

### 🗺️ Quick Reference Summary Table

| Tool | Use it for | Cost |
|---|---|---|
| `synchronized` | Guarding a compound read-modify-write | Blocks; one thread at a time |
| `volatile` | Visibility of a single field across threads | Cheap; **no atomicity** |
| `AtomicInteger` / `AtomicLong` | Lock-free counters via CAS | Cheap; single variable only |
| `ConcurrentHashMap` | Shared map | Per-bucket locking |
| `ReentrantReadWriteLock` | Many readers, rare writers | Fair reads; writer starvation risk |
| `ExecutorService` | Running tasks on a pool | Never `new Thread()` per task |

#### The three failure modes

1. **Race condition** — the answer depends on thread interleaving. `count++` is *three*
   operations (read, add, write); two threads can both read `5` and both write `6`.
2. **Visibility** — a thread caches a field in a register and never sees another
   thread's write. This is what `volatile` fixes, and *only* what it fixes.
3. **Deadlock** — two threads each hold what the other needs. Prevented by **lock
   ordering**: always acquire locks in a globally consistent order (e.g. by account id).

#### ❌ Wrong — the naive counter

```java
class Counter {
    private int count = 0;
    public void increment() { count++; }   // Violation: not atomic
    public int get() { return count; }
}
```

**Why this is wrong:** run this on 10 threads × 100,000 increments and you get roughly
600,000, not 1,000,000. Lost updates, every time. Adding `volatile` does **not** fix it —
`volatile` guarantees visibility, never atomicity of read-modify-write.

#### ✅ Right — three valid fixes, in order of preference

```java
import java.util.concurrent.atomic.*;

class Counter {
    private final AtomicInteger count = new AtomicInteger();
    public void increment() { count.incrementAndGet(); }  // CAS, lock-free
    public int get() { return count.get(); }
}

class SyncCounter {
    private int count = 0;
    public synchronized void increment() { count++; }     // simple, blocking
    public synchronized int get() { return count; }
}

class HotCounter {
    private final LongAdder count = new LongAdder();      // best under high contention
    public void increment() { count.increment(); }
    public long get() { return count.sum(); }
}
```

#### Singleton: why the "clever" version is broken

#### ❌ Wrong — double-checked locking without `volatile`

```java
class BrokenSingleton {
    private static BrokenSingleton instance;      // Violation: not volatile
    private BrokenSingleton() {}

    public static BrokenSingleton getInstance() {
        if (instance == null) {
            synchronized (BrokenSingleton.class) {
                if (instance == null) instance = new BrokenSingleton();
            }
        }
        return instance;
    }
}
```

**Why this is wrong:** `instance = new BrokenSingleton()` is not one step. The JVM may
**allocate memory and publish the reference before running the constructor**. A second
thread sees a non-null `instance` at the first check, skips the lock, and returns a
**partially constructed object** with null fields. This is the classic broken-DCL bug and
it is a favourite interview question.

#### ✅ Right — two correct singletons

```java
// Initialization-on-demand holder: lazy, thread-safe, no locking, no volatile.
// The JVM's class-initialisation lock does the work for you.
class Config {
    private Config() {}
    private static class Holder { static final Config INSTANCE = new Config(); }
    public static Config getInstance() { return Holder.INSTANCE; }
}

// Enum singleton: serialization-safe and reflection-proof. The simplest correct one.
enum Registry {
    INSTANCE;
    public void register(String key) { /* ... */ }
}
```

#### Compound actions are still unsafe on a concurrent collection

```java
import java.util.concurrent.*;

class Inventory {
    private final ConcurrentHashMap<String, Integer> stock = new ConcurrentHashMap<>();

    // WRONG: check-then-act. Two threads both see 1 and both decrement to 0.
    void badReserve(String sku) {
        Integer n = stock.get(sku);
        if (n != null && n > 0) stock.put(sku, n - 1);
    }

    // RIGHT: one atomic operation.
    boolean reserve(String sku) {
        return stock.computeIfPresent(sku, (k, n) -> n > 0 ? n - 1 : n) != null;
    }
}
```

> **The rule to say out loud in an interview:** *a thread-safe collection makes each
> individual call atomic; it does not make your sequence of calls atomic.* Any
> check-then-act or read-modify-write needs `compute*`, `putIfAbsent`, a CAS loop, or a
> lock.

---

## 📝 Master Notes: Exception Design

Exceptions are part of a class's public API. Designing them badly is a design smell,
not an implementation detail.

### 🗺️ Quick Reference Summary Table

| Type | Extends | Compiler forces handling? | Use for |
|---|---|---|---|
| Checked | `Exception` | Yes | A recoverable condition the caller can plausibly act on |
| Unchecked | `RuntimeException` | No | A programming error — a broken precondition |
| Error | `Error` | No | JVM-level failure. **Never catch these** |

#### ❌ Wrong — three anti-patterns in six lines

```java
class Service {
    void process(String raw) {
        try {
            int n = Integer.parseInt(raw);
        } catch (Exception e) {         // 1. catching everything
            // 2. swallowing it silently
        }
    }
    void find(String id) throws Exception { }   // 3. throws Exception
}
```

**Why this is wrong — the concrete damage:**

1. **`catch (Exception e)` catches bugs too** — `NullPointerException`,
   `ArrayIndexOutOfBounds`, and typos in your own code are hidden along with the parse
   failure you intended to handle.
2. **The empty block destroys evidence.** The failure happens, nothing is logged, and the
   method returns as if it succeeded. Debugging this costs hours.
3. **`throws Exception` propagates uselessness.** Every caller is now forced to handle
   "something", which tells them nothing and pushes them to write the same empty catch.

#### ✅ Right — specific, meaningful, and it carries context

```java
class InsufficientFundsException extends RuntimeException {
    private final long shortfall;
    InsufficientFundsException(String account, long shortfall) {
        super("Account " + account + " short by " + shortfall + " minor units");
        this.shortfall = shortfall;
    }
    public long shortfall() { return shortfall; }   // caller can act on it
}

class Account {
    private long balance;
    void withdraw(long amount) {
        if (amount <= 0) throw new IllegalArgumentException("amount must be positive");
        if (amount > balance) throw new InsufficientFundsException("A1", amount - balance);
        balance -= amount;
    }
}
```

#### The rules worth stating

- **Fail fast.** Validate arguments at the top of the method
  (`IllegalArgumentException`, `IllegalStateException`, `Objects.requireNonNull`).
- **Never use exceptions for control flow.** They are slow and they hide intent.
- **Never return `null` to signal absence** — return `Optional<T>` or throw. `null` is
  the caller's `NullPointerException` at a place far from the cause.
- **Preserve the cause when wrapping:** `throw new OrderFailedException("...", e);`
  Dropping `e` throws away the stack trace that names the real fault.
- **Clean up with try-with-resources**, never a `finally` that itself can throw.
- Modern Java leans **unchecked**. Checked exceptions do not compose with lambdas and
  streams, which is why almost no post-2014 API uses them.

---

## 📝 Master Notes: Interface Evolution (`default`, `static`, `sealed`)

Java 8 changed what an interface *is*. Knowing the modern toolkit separates a current
answer from a 2011 one.

### 🗺️ Quick Reference Summary Table

| Member | Since | Purpose | Can hold state? |
|---|---|---|---|
| `abstract` method | 1.0 | The contract | No |
| `default` method | 8 | Add a method without breaking every implementer | No |
| `static` method | 8 | A helper that belongs to the type, not an instance | No |
| `private` method | 9 | Share code between `default` methods | No |
| `sealed` interface | 17 | A **closed** set of permitted implementations | No |

> The hard rule from `TEXT_TO_CODE.md` still holds: **an interface can never hold
> per-object state.** `default` methods add behaviour, never fields.

#### `default` — the backward-compatibility escape hatch

```java
interface Notifier {
    void send(String msg);

    // Added in v2. Every existing implementer keeps compiling.
    default void sendUrgent(String msg) { send("[URGENT] " + msg); }
}
```

**The problem it solves:** before Java 8, adding a method to a published interface broke
every implementation in the world. **The trap:** a `default` method is not free —
if two interfaces supply the same default, the implementing class *must* override and
disambiguate with `Interface.super.method()`. That is the Diamond Problem returning
through the interface door.

#### `sealed` — making illegal states unrepresentable

#### ❌ Wrong — an open hierarchy where the set really is closed

```java
interface PaymentResult { }

class Handler {
    String describe(PaymentResult r) {
        if (r instanceof Success) return "ok";
        if (r instanceof Failure) return "failed";
        return "unknown";     // Violation: a case that should be impossible
    }
}
class Success implements PaymentResult {}
class Failure implements PaymentResult {}
```

**Why this is wrong:** the `return "unknown"` branch exists only because the compiler
cannot prove the list is complete. Add a third result type and **nothing tells you** this
method needs updating — you get `"unknown"` in production instead of a compile error.

#### ✅ Right — sealed plus an exhaustive switch

```java
sealed interface PaymentResult permits Success, Failure, Pending {}
record Success(String txnId) implements PaymentResult {}
record Failure(String reason) implements PaymentResult {}
record Pending(long retryAfterMs) implements PaymentResult {}

class Handler {
    String describe(PaymentResult r) {
        return switch (r) {                       // no default needed
            case Success s -> "ok: " + s.txnId();
            case Failure f -> "failed: " + f.reason();
            case Pending p -> "retry in " + p.retryAfterMs() + "ms";
        };
    }
}
```

**What the fix bought you:** adding a fourth result now **fails to compile** at every
switch that handles the type. The compiler became your checklist.

> **Sealed vs Open — the real decision.** `sealed` deliberately gives up OCP's
> extensibility in exchange for exhaustiveness. Use it when the set is genuinely fixed by
> the domain (payment outcomes, chess piece kinds, JSON node types). Use an open
> interface when third parties should be able to add implementations (a `FeeStrategy`).
> Choosing correctly, and being able to say *why*, is a senior-level signal.

#### Enums are classes, and that is the point

An enum can carry fields, implement interfaces, and give each constant its own body —
which makes it the cleanest Strategy implementation in Java when the set is fixed.

```java
enum Operation {
    PLUS("+")  { public long apply(long a, long b) { return a + b; } },
    TIMES("*") { public long apply(long a, long b) { return a * b; } };

    private final String symbol;
    Operation(String symbol) { this.symbol = symbol; }
    public abstract long apply(long a, long b);
    public String symbol() { return symbol; }
}
```

---

## 📝 Master Notes: Object Construction

How an object is *created* is a design decision with the same weight as its methods.

### 🗺️ Quick Reference Summary Table

| Technique | Use when |
|---|---|
| Public constructor | Few parameters, all required, no naming ambiguity |
| **Static factory method** | You want a name, caching, or to return a subtype |
| **Builder** | Many optional parameters, or you need step-by-step validation |
| **Dependency Injection** | The parameter is a collaborator, not data |

#### ❌ Wrong — the telescoping constructor

```java
class Pizza {
    Pizza(int size) { this(size, false); }
    Pizza(int size, boolean cheese) { this(size, cheese, false); }
    Pizza(int size, boolean cheese, boolean pepperoni) { this(size, cheese, pepperoni, false); }
    Pizza(int size, boolean cheese, boolean pepperoni, boolean olives) { }
}
```

**Why this is wrong:** `new Pizza(12, true, false, true)` is unreadable at the call site —
you must open the class to know what the third `false` means. Worse, two parameters of
the same type can be **swapped without any compiler error**, producing a silent bug.
Adding a topping means another constructor, and the count grows combinatorially.

#### ✅ Right — a Builder, with validation in `build()`

```java
class Pizza {
    private final int size;
    private final boolean cheese, pepperoni;

    private Pizza(Builder b) { this.size = b.size; this.cheese = b.cheese; this.pepperoni = b.pepperoni; }

    static Builder builder(int size) { return new Builder(size); }

    static class Builder {
        private final int size;                    // required → constructor arg
        private boolean cheese, pepperoni;         // optional → setters
        Builder(int size) { this.size = size; }
        Builder cheese()    { this.cheese = true; return this; }   // fluent: return this
        Builder pepperoni() { this.pepperoni = true; return this; }
        Pizza build() {
            if (size < 6) throw new IllegalArgumentException("min size 6");
            return new Pizza(this);                 // invariants checked once, here
        }
    }
}
// Pizza.builder(12).cheese().pepperoni().build();  ← self-documenting
```

#### Static factory methods — why `of()` beats `new`

```java
import java.util.*;

class Instant2 {
    private final long epochMs;
    private Instant2(long ms) { this.epochMs = ms; }

    static Instant2 ofEpochMilli(long ms) { return new Instant2(ms); }  // 1. it has a NAME
    static Instant2 now() { return new Instant2(System.currentTimeMillis()); }
}
```

Four advantages over a constructor:
1. **A name.** `Instant2.now()` versus a `boolean` argument meaning "use current time".
2. **It need not create a new object.** `Integer.valueOf` caches −128..127; `List.of()`
   returns a shared empty list.
3. **It can return a subtype.** `Collections.unmodifiableList` returns a hidden class —
   that is DIP applied to construction.
4. **Two factories can share a signature** where two constructors cannot.

#### Construct what you own; inject what varies

```java
import java.util.*;

class OrderService {
    private final PaymentGateway gateway;        // varies → injected (DIP)
    private final List<Order> orders = new ArrayList<>();  // owned → constructed here

    OrderService(PaymentGateway gateway) { this.gateway = gateway; }
}
interface PaymentGateway { boolean charge(long amount); }
interface Order { }
```

> **Do not inject everything.** A `List` the object genuinely owns, a `StringBuilder`, a
> value object — construct them. Inject only what has more than one plausible
> implementation, or what you need to fake in a test.

---

## 📝 Master Notes: Generics and Variance

Generics are how you write reusable containers and strategies without `Object` casts.

### 🗺️ Quick Reference Summary Table

| Form | Meaning | You can… |
|---|---|---|
| `List<T>` | Exactly `T` | read `T` and write `T` |
| `List<? extends T>` | Some unknown subtype of `T` | **read** `T`; cannot add |
| `List<? super T>` | Some unknown supertype of `T` | **write** `T`; reads give `Object` |
| `<T extends Comparable<T>>` | Bounded type parameter | call `compareTo` on `T` |

#### The single most important fact: generics are **invariant**

`List<String>` is **not** a `List<Object>`, even though `String` is an `Object`.

```java
import java.util.*;

class Variance {
    static void why() {
        List<String> strings = new ArrayList<>();
        // List<Object> objects = strings;   // does not compile — and thank goodness
        // objects.add(42);                  // would poison the List<String>
    }
}
```

Arrays *are* covariant (`Object[] a = new String[1];` compiles) and that is a known Java
design mistake — it defers the error to a runtime `ArrayStoreException`. Generics chose
compile-time safety instead.

#### ❌ Wrong — a signature that is needlessly narrow

```java
import java.util.*;

class Stats {
    // Violation: cannot be called with a List<Integer> even though Integer is a Number
    static double sum(List<Number> nums) {
        double t = 0;
        for (Number n : nums) t += n.doubleValue();
        return t;
    }
}
```

**Why this is wrong:** `sum(List.of(1, 2, 3))` — a `List<Integer>` — **does not compile**.
The method only reads, so demanding an exact `List<Number>` rejects every caller who has
a list of a concrete number type. The API is unusable for its obvious use case.

#### ✅ Right — PECS: **P**roducer `extends`, **C**onsumer `super`

```java
import java.util.*;

class Stats {
    // Producer: the list produces values for us → extends
    static double sum(List<? extends Number> nums) {
        double t = 0;
        for (Number n : nums) t += n.doubleValue();
        return t;
    }

    // Consumer: the list consumes values from us → super
    static void addIntegers(List<? super Integer> sink) {
        sink.add(1);
        sink.add(2);
    }
}
```

`sum` now accepts `List<Integer>`, `List<Double>`, `List<Number>`. `addIntegers` accepts
`List<Integer>`, `List<Number>`, and `List<Object>`. This is exactly why
`Collections.copy(List<? super T> dest, List<? extends T> src)` has the signature it does.

#### Type erasure — and the three things it forbids

Generics exist only at compile time; at runtime `List<String>` is just `List`.
Consequences you must be able to name:

```java
import java.util.*;

class Erasure {
    // void f(List<String> a) {}
    // void f(List<Integer> a) {}   // will not compile: same erasure

    static <T> void cannot() {
        // T t = new T();               // cannot instantiate a type parameter
        // T[] arr = new T[10];         // cannot create a generic array
        // if (x instanceof List<String>) {}  // cannot test a parameterised type
    }
}
```

The workaround for all three is to pass a `Class<T>` token or a factory
(`Supplier<T>`) — which is the Factory pattern solving a language limitation.

---

## 📝 Master Notes: Inheritance Hazards and Design Judgement

### 1. The Fragile Base Class Problem

A superclass change can break a subclass that never changed — because inheritance
exposes **implementation**, not just interface.

#### ❌ Wrong — the classic `HashSet` counter

```java
import java.util.*;

class CountingSet<E> extends HashSet<E> {
    private int added = 0;

    @Override public boolean add(E e) { added++; return super.add(e); }
    @Override public boolean addAll(Collection<? extends E> c) {
        added += c.size();
        return super.addAll(c);      // Violation: superclass addAll calls add() internally
    }
    public int added() { return added; }
}
```

**Why this is wrong:** `addAll` of three elements reports **six**. `HashSet.addAll` is
implemented by calling `add` for each element — and `add` is your override, which counts
again. The subclass depends on an undocumented **self-use** detail of the parent, and a
future JDK could change it either way.

#### ✅ Right — composition and forwarding (the Decorator shape)

```java
import java.util.*;

class CountingSet<E> {
    private final Set<E> delegate = new HashSet<>();   // HAS-A, not IS-A
    private int added = 0;

    public boolean add(E e) { added++; return delegate.add(e); }
    public boolean addAll(Collection<? extends E> c) {
        added += c.size();
        return delegate.addAll(c);   // delegate's internals cannot re-enter our code
    }
    public int added() { return added; }
}
```

**The rule:** *inherit only when the superclass was designed and documented for
inheritance.* Otherwise compose. This is why `String`, `Integer`, and every `record` are
`final` — and why the alternative to `public` and `abstract` is `final`, with nothing in
between being safe by accident.

### 2. Prefer derived state over stored state

```java
class Cart {
    private int itemCount;
    private int total;          // Violation: derivable, so it can go stale
}
```

Any field you can compute from another field is a **second source of truth** and will
eventually disagree with the first. Store `List<Item> items`; compute
`int total() { ... }`. Cache only when profiling proves you must, and then have exactly
one method that invalidates the cache.

### 3. The Rule of Three

Do not abstract on the first duplication. Two similar blocks are a coincidence; three are
a pattern. Premature abstraction produces an interface with one implementation and a
parameter that is always the same value — harder to read than the duplication it removed.
Pair this with **YAGNI**: build the abstraction when the second variant actually arrives.

### 4. Testability is a design property

If a class is hard to test, the design is wrong — the test is just the messenger.

| Symptom in a test | The design fault |
|---|---|
| You must start a database to test arithmetic | SRP violation |
| You cannot substitute a fake | No seam — DIP violation |
| You must call five methods in order first | Poor encapsulation of state |
| The test asserts on log output | Behaviour has no return value to observe |
| The result changes between runs | Hidden dependency on clock, random, or static state |

The fixes are the principles already covered: inject the clock, inject the random source,
inject the gateway. **A constructor parameter is a seam; a `new` inside a method is a
welded joint.**

---

## 📝 Master Notes: Reading a UML Class Diagram

You will be asked to draw one. This is the whole notation you need.

### 🗺️ Relationship arrows, by strength

| Relationship | Line | Meaning | Lifetime |
|---|---|---|---|
| Inheritance | solid line, hollow **triangle** at parent | IS-A | — |
| Realisation | dashed line, hollow **triangle** at interface | implements | — |
| Composition | solid line, **filled** diamond at owner | strong HAS-A | part dies with whole |
| Aggregation | solid line, **hollow** diamond at owner | weak HAS-A | part outlives whole |
| Association | plain solid line, arrow for direction | knows-about | independent |
| Dependency | **dashed** line with open arrow | uses temporarily (parameter, local) | transient |

Mnemonic: **filled diamond = filled with it, dies with it.**

### Box notation and multiplicity

```text
┌────────────────────────────┐
│         ClassName          │   ← italic name = abstract
├────────────────────────────┤
│ - privateField : Type      │   - private   + public
│ # protectedField : Type    │   # protected ~ package
│ + CONSTANT : int {static}  │   underline or {static} = static
├────────────────────────────┤
│ + publicMethod(a: int): T  │
│ - helper(): void           │
└────────────────────────────┘

ParkingLot ◆────── "1"      "1..*" ─── Floor     composition, 1 lot to many floors
Floor      ○────── "1"      "0..*" ─── Vehicle   aggregation, vehicles outlive the floor
Order      ─ ─ ─ ─▷ PaymentGateway               dependency, used as a parameter
```

Multiplicities go at the ends: `1`, `0..1`, `1..*`, `0..*`, `2..4`.

> **In an interview, draw five boxes, not twenty.** Show the interfaces and the one or
> two relationships that carry the design's key decision. A diagram nobody can read in
> ten seconds has failed at the only job it had.

---

## 🧭 Final self-check before an LLD round

Ten questions. If any answer is "I'd have to look it up", that is your next revision hour.

1. Name the failure caused by overriding `equals` and not `hashCode`.
2. Why does `Ostrich extends Bird` break LSP, given an ostrich really is a bird?
3. What exactly does `volatile` guarantee, and what does it not?
4. Why is double-checked locking without `volatile` broken?
5. When should the set of subtypes be `sealed` rather than open — and what do you give up?
6. `List<? extends Number>` — can you add to it? Why not?
7. Why does `CountingSet extends HashSet` count `addAll` twice?
8. Composition or inheritance for a `ColorPoint`, and why is `equals` the deciding argument?
9. Which two SOLID principles produce the same symptom, and which two are the same bug from opposite ends?
10. What is the difference between a static factory method and a Builder, and when does each win?
