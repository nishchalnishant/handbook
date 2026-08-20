# How to actually do Low-Level Design

LLD is not memorizing 23 design patterns. It is a repeatable procedure.
Interviewers are watching the procedure, not the answer.

## The 6 steps, every single time

1. **Clarify + scope.** Ask 3-5 questions. Say out loud what you are NOT
   building. ("Single machine, in-memory, no persistence, no payments.")
   Candidates who skip this fail before writing a line.

2. **Nouns -> classes.** Read the problem statement and underline nouns.
   Parking lot, spot, vehicle, ticket, floor. Those are your candidates.

3. **Verbs -> methods.** Park, unpark, calculate fee. Put each verb on the
   class that OWNS the data it needs. That single habit is 80% of good design.

4. **Find what varies -> interface.** Anything the problem says "different
   types of" or "multiple strategies for" becomes an interface with several
   implementations. Fee rules. Vehicle types. Eviction policies.

5. **Write the API before the bodies.** Method signatures only. Ask
   yourself: could someone USE this without reading the implementation?
   If the signature is confusing, the design is wrong. Fix it now, not later.

6. **Then implement, compile, and run a main() that proves it.**
   Working code beats a whiteboard drawing every time.

## The design principles, in plain words

- **SRP** — one class, one reason to change. If you say "and" describing a
  class, split it. `Ticket` stores ticket data; `FeeCalculator` prices it.
- **Open/Closed** — adding a feature should mean adding a class, not editing
  a switch statement in five places. See the strategy pattern below.
- **Liskov** — a subclass must be usable anywhere its parent is, without
  surprises. If overriding forces you to throw "not supported", don't inherit.
- **Interface Segregation** — many small interfaces beat one fat one.
  Don't force a class to implement methods it has no use for.
- **Dependency Inversion** — depend on interfaces, not concrete classes.
  Take `FeeStrategy` as a constructor parameter; don't `new FlatFee()` inside.

## The 5 patterns that cover most interviews

- **Strategy** — swap an algorithm at runtime. An interface + implementations,
  passed in. THE most useful one. Fee rules, sorting, eviction, pricing.
- **Factory** — one place decides which concrete class to build. Keeps
  `new Truck()` out of your business logic.
- **Singleton** — exactly one instance. Use an `enum` or a static holder.
  Interviewers ask for it; real systems mostly regret it.
- **Observer** — one thing changes, many things react. Notifications, events.
- **Builder** — construct objects with many optional fields readably,
  instead of a constructor with nine arguments.

## The trap you must avoid

Do not start by drawing a giant class diagram. Start with the smallest
thing that RUNS, then grow it. A design you have compiled and executed
teaches you more in 20 minutes than a diagram teaches you in a week.
