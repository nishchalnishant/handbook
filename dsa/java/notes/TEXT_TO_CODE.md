# From English sentence to Java code

The missing link between "I know what aggregation is" and "I can write this".

You already know the vocabulary. This file is the **decision procedure** that turns a
problem statement into class declarations. Follow it top to bottom. Every rule here has
a yes/no test — you should never be *guessing* whether something is an interface.

Runnable proof: `notes/oop_proofs/TextToCodeProofs.java`

---

## The one-page flowchart

```
PROBLEM STATEMENT (English)
         |
[1] underline NOUNS ------------------> candidate classes
[2] underline VERBS ------------------> candidate methods
[3] underline ADJECTIVES / "types of"-> candidate variation points
         |
         v
   for each NOUN:
         |
         +-- is it just a value, no behaviour, never changes?
         |        YES -> record          (Ticket, Money, Point)
         |
         +-- is it a fixed, known-at-compile-time list of options?
         |        YES -> enum            (VehicleType, Status, Direction)
         |
         +-- does it have state that CHANGES over time?
         |        YES -> class           (Spot, Account, Elevator)
         |
         +-- is it a "kind of" something else?
                  YES -> go to THE BIG DECISION below
         |
         v
   for each VERB:
         put it on the class that OWNS THE DATA it needs
         (if the method reaches into another object's fields, it's on the wrong class)
         |
         v
   for each "different types of X" / "multiple ways to Y":
         -> THE BIG DECISION
```

---

## THE BIG DECISION: class, abstract class, or interface?

This is the question you asked. Here is the test. Ask these **in order** and stop at the
first YES.

```
Q1. Do the variants differ ONLY by data (a number, a label, a rate)?
    and is the list of variants FIXED and known now?
        YES -> enum with fields.        <-- most people miss this one
        NO  -> Q2

Q2. Do the variants need to SHARE MUTABLE STATE or shared constructor logic?
        YES -> abstract class
        NO  -> Q3

Q3. Is this a CAPABILITY that unrelated classes might also have?
    (test: does the name end in -able, or read as "can do X"?)
        YES -> interface
        NO  -> Q4

Q4. Is there exactly one variant right now, with no second one in sight?
        YES -> plain class. Stop. (YAGNI — do not invent a hierarchy for one thing.)
        NO  -> interface (default answer)
```

**Default to interface.** If Q1 and Q2 both say no, interface is almost always right.
Abstract class is the exception, not the norm.

### The hard rule that decides Q2

An interface **cannot hold per-object state**. This is not style — the compiler enforces it:

```java
interface Bad { private int counter; }   // error: = expected
interface Silent { int x = 5; }          // legal, but silently becomes
                                         // public static final — a shared CONSTANT
```

Verified: reflection reports `public static final` on that field. So the moment each
variant needs its own `plate`, `id`, or `balance` **stored in the parent**, an interface
is off the table and you need an abstract class.

That single fact resolves most interface-vs-abstract arguments.

---

## Your vehicle example, worked all four ways

> "There should be a vehicle. There could be different types of vehicles."

That sentence alone is **not enough to decide**. You need one more answer: *how do the
types differ?* Each answer gives a different correct shape.

### If they differ only by data → `enum`

> "A bike takes 1 spot, a car 2, a truck 4."

```java
enum VehicleType {
    BIKE(1, 10.0), CAR(2, 20.0), TRUCK(4, 40.0);
    private final int size; private final double rate;
    VehicleType(int s, double r){ size = s; rate = r; }
    int size(){ return size; }
    double rate(){ return rate; }
}
record Vehicle(String plate, VehicleType type) {}
```

Two declarations, no hierarchy. **This is what the parking lot uses.** Reach for this
first — candidates who build a five-class hierarchy for this look worse, not better.

### If they differ by behaviour but share no state → `interface`

> "Different vehicles are parked differently and charged differently."

```java
interface Parkable {
    int size();
    default String describe(){ return "takes " + size() + " spots"; }
}
record Bike(String plate) implements Parkable { public int size(){ return 1; } }
record Car (String plate) implements Parkable { public int size(){ return 2; } }
```

### If they share state → `abstract class`

> "Every vehicle has a plate and a registration date, but each computes its own fee."

```java
abstract class Vehicle {
    protected final String plate;          // shared STATE — interface cannot do this
    protected Vehicle(String plate){ this.plate = plate; }
    String plate(){ return plate; }        // written once, inherited
    abstract int size();                   // each subclass MUST differ here
}
class Bike  extends Vehicle { Bike(String p){ super(p); }  int size(){ return 1; } }
class Truck extends Vehicle { Truck(String p){ super(p); } int size(){ return 4; } }
```

### If some vehicles have an extra capability → `both`

> "Some vehicles are electric and can be charged."

```java
interface Chargeable { double kwh(); }

class ElectricCar extends Vehicle implements Chargeable {
    ElectricCar(String p){ super(p); }
    int size(){ return 2; }
    public double kwh(){ return 75.0; }
}
```

`extends` for **what it is** (one parent, carries state).
`implements` for **what it can do** (many, capability only).

Say that sentence out loud in an interview and you've answered the question.

---

## Trigger phrases → code shapes

Train yourself to hear these. This table is the actual translation layer.

| English in the problem | What it means | Code |
|---|---|---|
| "a X has a Y" (Y dies with X) | composition | field `new`ed in constructor, never returned |
| "a X has a Y" (Y exists independently) | aggregation | field passed into constructor |
| "a X is a Y" | inheritance | `class X extends Y` |
| "a X can be Y-ed" / "-able" | capability | `interface Yable` |
| "different types of X" (data only) | fixed variants | `enum` |
| "different types of X" (behaviour) | variation point | `interface` + impls |
| "different **strategies/policies/rules** for" | strategy pattern | `interface` injected via constructor |
| "X notifies Y when..." | observer | `List<Listener>` + `notifyAll()` |
| "only one X in the system" | singleton | `enum INSTANCE` or holder idiom |
| "X is created based on..." | factory | a `create(...)` method |
| "X has many optional fields" | builder | `Builder` inner class |
| "at most / at least / must be" | an **invariant** | validate in constructor, throw |
| "for each / all of the" | a collection | `List<X>` / `Map<K,X>` |
| "at the same time" / "concurrent" | thread safety | `synchronized` / `ConcurrentHashMap` |

---

## The refactor you will use most: switch → interface

Whenever you write a `switch` or `if-else` chain **on a type**, that's the signal.

**Before** — every new channel edits this method (OCP violation):

```java
String send(String kind, String msg) {
    switch (kind) {
        case "email": return "email: " + msg;
        case "sms":   return "sms: " + msg;
        default: throw new IllegalArgumentException(kind);
    }
}
```

**After** — each `case` became a class:

```java
interface Channel { String send(String msg); }
class Email implements Channel { public String send(String m){ return "email: " + m; } }
class Sms   implements Channel { public String send(String m){ return "sms: " + m; } }
class Push  implements Channel { public String send(String m){ return "push: " + m; } }

class Notifier {
    private final Channel channel;
    Notifier(Channel c){ channel = c; }     // injected = swappable = testable
    String send(String msg){ return channel.send(msg); }
}
```

Verified: `Push` was added without editing `Notifier` or `Channel`. Mechanical recipe:

1. each `case` body → one class
2. the switch's return type → the interface method's return type
3. the switch variable → gone; the object *is* the choice
4. the caller passes the implementation in

---

## Worked example: read a spec, produce declarations

> "Design a food delivery system. A customer places an order containing several items
> from one restaurant. Orders can be paid by card, UPI, or wallet. An order moves
> through placed, preparing, out-for-delivery, delivered. Notify the customer on every
> status change."

**Step 1 — nouns:** customer, order, item, restaurant, payment, status, notification.

**Step 2 — verbs:** place, pay, move-through, notify.

**Step 3 — apply the decision tree to each noun:**

| Noun | Test | Answer |
|---|---|---|
| Item | value, never changes | `record Item(String name, double price)` |
| Customer | has identity + state | `class Customer` |
| Restaurant | has identity + state | `class Restaurant` |
| Status | fixed known list | `enum Status { PLACED, PREPARING, OUT_FOR_DELIVERY, DELIVERED }` |
| Payment | "paid **by** card, UPI, wallet" = different ways to do one thing | `interface PaymentMethod` |
| Order | state that changes over time | `class Order` |
| Notification | "notify **on** every change" | `interface OrderListener` (observer) |

**Step 4 — verbs onto owners:** `place()` needs the items → `Order`. `pay()` needs the
amount → `PaymentMethod`, called by `Order`. `notify()` needs the listener list → `Order`.

**Step 5 — the API, signatures only:**

```java
record Item(String name, double price) {}

enum Status { PLACED, PREPARING, OUT_FOR_DELIVERY, DELIVERED }

interface PaymentMethod { boolean pay(double amount); }      // varies -> interface
interface OrderListener { void onStatusChange(Order o, Status s); }

class Order {
    private final List<Item> items;          // aggregation: items pre-exist
    private final Restaurant restaurant;     // aggregation
    private Status status;                   // changes -> class, not record
    private final List<OrderListener> listeners = new ArrayList<>();  // composition

    Order(Restaurant r, List<Item> items) { ... }
    double total() { ... }
    boolean checkout(PaymentMethod method) { ... }   // injected -> DIP
    void advanceTo(Status next) { ... }              // fires listeners
    void addListener(OrderListener l) { ... }
}
```

Notice: **no inheritance anywhere.** Two interfaces, both because the spec said "different
ways to do X". That's the normal shape of a good answer.

---

## Say this out loud in the interview

The procedure only scores if the interviewer hears it. Narrate:

> "The nouns are customer, order, item, restaurant, payment. Item never changes, so it's
> a record. Status is a fixed list, so it's an enum. Payment has three variants that
> differ in behaviour, so that's an interface with three implementations, injected into
> checkout so I'm not editing Order to add a fourth. Order owns the status, so advance()
> lives there."

That paragraph *is* the answer. The code just writes it down.

---

## Five rules that prevent most bad designs

1. **Don't create a hierarchy for one thing.** One implementation = plain class.
   Add the interface when the second variant arrives (rule of three).
2. **Prefer enum over subclasses when only data differs.** Cheaper, exhaustive in
   `switch`, impossible to get wrong.
3. **If a method doesn't use its own class's fields, it's on the wrong class.**
   The single most reliable smell test.
4. **Inject what varies; construct what you own.** `FeeStrategy` comes in through the
   constructor; `List<Spot>` is built inside.
5. **`extends` at most once, deliberately. `implements` freely.** If you ever want two
   parents, you wanted interfaces.

---

## Practice loop

Don't read this file again. Use it:

1. Open `lld/02_elevator/README.md`.
2. On paper: underline nouns, verbs, "different types of".
3. Run each noun through the decision tree. Write only declarations — no bodies.
4. Check yourself against `lld/01_parking_lot/ParkingLot.java`, which follows this
   procedure exactly.
5. Then fill in the bodies and make it run.

If you can produce the declarations in under 10 minutes, you've closed the gap you
described. That is the whole skill.
