/**
 * PatternSkeleton.java - Learn ONE skeleton, derive ELEVEN patterns.
 *
 * ===========================================================================
 * WHAT THIS FILE IS
 * ===========================================================================
 * A teaching file, not production code. It makes one claim:
 *
 * Eleven of the design patterns you are asked about in interviews are
 * the same small piece of Java, with exactly one thing changed each time.
 *
 * So do not memorize eleven patterns. Memorize these four lines:
 *
 * interface Thing { void doIt(); } // 1. CONTRACT
 * class RealThing implements Thing { } // 2. IMPLEMENTATION
 * class Context {
 * private Thing field; // 3. HOLD
 * void action() { field.doIt(); } // 4. DELEGATE
 * }
 *
 * Every section below is those four lines with ONE thing changed. Each section
 * marks that change with <== THE ONLY DIFFERENCE.
 *
 * The sections are ordered by FAMILY (creational, then structural, then
 * behavioural), which is the order interviewers expect. They are NOT ordered
 * by difficulty, so you may read them in any order - each section stands on
 * its own, and where one refers to another it names the section number.
 *
 * ---------------------------------------------------------------------------
 * A NOTE ON THE WORD "CONTEXT"
 * ---------------------------------------------------------------------------
 * In pattern books, "the Context" is the NAME OF A ROLE. It means: the class
 * that HOLDS the field. In the skeleton above, `Context` is literally the
 * class name. In section 11 the context is `Checkout`; in section 8 it is
 * `Door`.
 *
 * "Context" does NOT mean "extra information" or "the situation". When this
 * file says a method "receives the context", it means one specific thing:
 * the method receives a REFERENCE TO THE OBJECT THAT HOLDS IT. That is very
 * different from receiving a number or a string.
 *
 * ---------------------------------------------------------------------------
 * HOW TO READ THIS FILE
 * ---------------------------------------------------------------------------
 * The outer class holds a `static class` block per section (Skeleton,
 * AsStrategy, AsState, ...). Those blocks are only NAMESPACES. They exist so
 * that every section can reuse the names `field` and `action` without the
 * names clashing. They carry no design meaning - do not copy that nesting
 * into real code.
 *
 * Reusing the names `field` and `action` in every section is deliberate. It
 * keeps the SHAPE identical from section to section, so the one real change
 * is easy to see.
 *
 * Sections 1-11 are the patterns, grouped the way the Gang of Four book
 * groups them:
 *
 * CREATIONAL  (1-3)  how an object gets MADE
 *                    Singleton, Factory Method, Abstract Factory
 * STRUCTURAL  (4-6)  how objects are PUT TOGETHER
 *                    Adapter, Composite, Decorator
 * BEHAVIOURAL (7-11) how objects SHARE WORK at run time
 *                    Observer, State, Command, Chain of Responsibility,
 *                    Strategy
 *
 * That grouping is worth memorising on its own: being asked to "name a
 * structural pattern" is a real interview question, and the three family
 * names are the cheapest marks in the subject.
 *
 * Section 12 is a separate topic: the six
 * relationships between classes that UML class diagrams draw, which you will
 * be asked to name in an interview. Section 13 is SOLID - the five design
 * principles that explain WHY the twelve sections above are shaped the way
 * they are. Read it last: every rule there points back at code you have
 * already seen.
 *
 * main() runs every section in order.
 *
 * Run: java PatternSkeleton.java
 */
public class PatternSkeleton {

     // =========================================================================
     // 0. THE SKELETON (not a pattern - just the shape everything else reuses)
     // =========================================================================
     //
     // Four moves. Everything after this changes exactly one of them.
     //
     // THE MOST IMPORTANT LINE is:
     //
     // private final Thing field;
     //
     // The declared type is `Thing`, the INTERFACE. It is not `RealThing`, the
     // concrete class. This matters because of what `Context` now CANNOT do:
     // it cannot know which implementation it holds, and the compiler enforces
     // that. It has no instanceof check, no type flag, no switch.
     //
     // That restriction is the benefit. A class that does not know what it is
     // talking to cannot break when that thing changes. You can hand `Context`
     // an implementation written years later, by someone who never read
     // `Context`, and `Context` still works without being edited.
     //
     // The fourth move, `field.doIt()`, is called DELEGATION: `Context` does
     // not do the work itself, it forwards the work to the field. `Context`
     // decides WHEN the work happens; the field decides HOW.
     //
     static class Skeleton {
          interface Thing { // 1. CONTRACT - the set of things that can be done
               void doIt();
          }

          static class RealThing implements Thing { // 2. IMPLEMENTATION - one way to do them
               public void doIt() {
                    System.out.println("    did the thing");
               }
          }

          static class Context {
               private final Thing field; // 3. HOLD - the type is the INTERFACE, never the class

               Context(Thing field) {
                    this.field = field;
               }

               void action() {
                    field.doIt();
               } // 4. DELEGATE - forward the work to the field
          }

          static void demo() {
               say("0. SKELETON");
               new Context(new RealThing()).action();
          }
     }

     // #########################################################################
     // CREATIONAL PATTERNS (1-3) - they answer: HOW DOES THIS OBJECT GET MADE?
     // #########################################################################
     //
     // Creational patterns take the `new` keyword away from the caller. The
     // caller says WHAT it wants, not HOW to build it, so the construction
     // rule can change later without touching a single call site.
     //
     // =========================================================================
     // 1. SINGLETON = the skeleton where the field is STATIC and of the
     // class's own type
     // =========================================================================
     //
     // Three mechanisms, each doing real work.
     //
     // 1. `private Config()` - a private constructor. No code outside the class
     // can write `new Config()`; the compiler blocks it. The only way to get
     // an instance is get(). Without this, everything else is decoration.
     //
     // 2. The `Holder` inner class - this is the INITIALIZATION-ON-DEMAND
     // HOLDER idiom, and it relies on two guarantees from the JVM:
     //
     // (a) A class is not initialized until it is first used. `Holder` is
     // untouched until someone reads `Holder.field`, which happens on
     // the first get() call. So the object is created LAZILY - no work
     // at program startup.
     //
     // (b) Class initialization is THREAD-SAFE. The JVM holds an internal
     // lock while it runs. If fifty threads call get() at the same
     // moment, exactly one Config is built and every thread sees a
     // fully constructed object.
     //
     // So you get laziness and thread safety with NO `synchronized` and NO
     // double-checked locking. The correctness comes from the language.
     //
     // WHY THIS MATTERS IN AN INTERVIEW: if you write double-checked
     // locking from memory and forget `volatile` on the instance field, the
     // singleton is subtly broken - instruction reordering can publish a
     // half-built object to another thread. The holder idiom avoids that
     // problem entirely. If asked for an alternative, `enum Config
     // { INSTANCE; }` is the other accepted answer, and it also survives
     // serialization and reflection attacks.
     //
     // 3. `static final` - created once, never reassigned.
     //
     // WHY THE DEMO USES `==` AND NOT .equals: `==` compares REFERENCES - it
     // asks whether these are literally the same object in memory, which is
     // exactly what Singleton claims. `.equals` would only say they look alike.
     //
     // THE CRITICISM YOU SHOULD KNOW: Singleton is the most overused pattern in
     // the catalogue. It is global mutable state, it makes unit testing awkward
     // because you cannot substitute a fake, and it hides dependencies - a
     // class that calls Config.get() does not declare that it needs Config. Use
     // it for genuinely single resources: a config registry, a connection pool,
     // a logger. If an interviewer pushes back, the strong reply is that
     // dependency injection gives the same single-instance guarantee without a
     // global access point.
     //
     // EXAMPLES YOU CAN PICTURE
     //
     // (a) THE PRINTER SPOOLER IN AN OFFICE. Many people print; there is one
     //     queue. Two queues would mean two documents fighting for one printer.
     //
     // (b) APP CONFIGURATION. config.yml is parsed once at startup. Every
     //     class that asks gets the same loaded object rather than re-reading
     //     the file a thousand times.
     //
     // (c) DATABASE CONNECTION POOL. The pool object must be unique, because
     //     the whole point is a shared, counted set of connections. Two pools
     //     would silently double your connection limit.
     //
     // (d) THE LOGGER. Everyone writes to one file handle. Two logger objects
     //     means two handles to the same file and interleaved, corrupted lines.
     //
     // (e) java.lang.Runtime.getRuntime() - the JVM ships a Singleton.
     //
     // THE COUNTER-EXAMPLE, WHICH MATTERS AS MUCH: a UserSession is NOT a
     // Singleton. It feels like "the current user", but the moment you run two
     // requests at once, one global session is a bug. Ask "is there physically
     // only one of these?" before reaching for this pattern.
     //
     static class AsSingleton {
          static final class Config {
               private static class Holder {
                    static final Config field = new Config();
               } // <== STATIC, and of the class's own type

               private Config() { // private: the only way in is get()
                    System.out.println("    built once");
               }

               static Config get() {
                    return Holder.field;
               } // the first call triggers lazy, thread-safe creation

               void action() {
                    System.out.println("    serving config");
               }
          }

          static void demo() {
               say("1. SINGLETON  (a static field of the class's own type)");
               Config.get().action();
               // "built once" prints once even though get() is called three times.
               System.out.println("    same object? " + (Config.get() == Config.get()));
          }
     }

     // =========================================================================
     // 2. FACTORY METHOD = the skeleton that RETURNS the interface instead of
     // holding it
     // =========================================================================
     //
     // THE CHANGE: `App` has no `field` at all. Instead of holding a Doc, it
     // declares a method that PRODUCES one.
     //
     // protected abstract Doc create();
     //
     // Because create() is abstract, `App` is saying: "a Doc will exist, and I
     // am not going to say which kind." Subclasses answer that question.
     //
     // WHAT IT BUYS YOU: action() - the real logic - is written ONCE, in the
     // parent, and works for every subclass forever. Imagine action() were
     // forty lines of document workflow: open, validate, render, cache, log.
     // You write those forty lines one time; each new document type adds three
     // lines. The workflow and the object creation change independently.
     //
     // NAMING, WHICH INTERVIEWERS DO CHECK:
     // FACTORY METHOD (this section) - a subclass overrides one creation
     // method. One product type per subclass.
     // SIMPLE FACTORY - a static method with a switch on an enum. Common in
     // real code, but not one of the 23 GoF patterns.
     // ABSTRACT FACTORY (section 3) - one object that creates a whole FAMILY
     // of related products that must match each other.
     //
     // WHERE THIS SHOWS UP: chess piece creation, notification channels, hotel
     // room types, vehicle types, board game setup.
     //
     // EXAMPLES YOU CAN PICTURE
     //
     // (a) LOGISTICS APP. `RoadLogistics.createTransport()` returns a Truck;
     //     `SeaLogistics.createTransport()` returns a Ship. The shared planRoute()
     //     code in the parent works with either, because it only ever calls
     //     Transport.deliver().
     //
     // (b) CHESS BOARD SETUP. `setUpBoard()` walks the squares and calls the
     //     abstract makePiece(square). ClassicChess makes a Bishop on c1;
     //     Chess960 makes something else. The setup loop is written once.
     //
     // (c) NOTIFICATION SERVICE. EmailNotifierFactory, SmsNotifierFactory,
     //     PushNotifierFactory. Business code calls send() and never sees a
     //     `new SmtpClient(...)` anywhere.
     //
     // (d) DOCUMENT EDITOR (the classic). "File > New" runs the same open,
     //     save and close code for a spreadsheet or a slide deck; only
     //     createDocument() differs per editor subclass.
     //
     // THE TELL IN ALL FOUR: a parent class already knows the WORKFLOW but not
     // the exact object, so it leaves one creation method for the subclass.
     //
     static class AsFactory {
          interface Doc {
               void open();
          }

          static class Pdf implements Doc {
               public void open() {
                    System.out.println("    opening pdf");
               }
          }

          static class Word implements Doc {
               public void open() {
                    System.out.println("    opening word");
               }
          }

          static abstract class App {
               protected abstract Doc create(); // <== RETURN a Doc, do not hold one

               void action() {
                    create().open();
               } // written once, works for every subclass
          }

          static class PdfApp extends App {
               protected Doc create() {
                    return new Pdf();
               }
          }

          static class WordApp extends App {
               protected Doc create() {
                    return new Word();
               }
          }

          static void demo() {
               say("2. FACTORY METHOD  (the method returns the interface)");
               new PdfApp().action();
               new WordApp().action();
          }
     }

     // =========================================================================
     // 3. ABSTRACT FACTORY = a factory with SEVERAL create methods, so that a
     // whole family of products is guaranteed to match
     // =========================================================================
     //
     // THE CHANGE FROM SECTION 2: Factory Method has ONE create method.
     // Abstract Factory has SEVERAL, and one implementation supplies all of
     // them.
     //
     // THE PROBLEM IT SOLVES: some objects only work correctly together. A
     // dark-theme button next to a light-theme checkbox is a bug. With two
     // separate factories nothing stops you from mixing them. With one factory
     // object per family, mixing is impossible - you pick `DarkKit` once, and
     // every widget it hands you is dark.
     //
     // NOTE WHAT `Screen` KNOWS: only the `Kit` interface. It never names
     // DarkKit or LightKit. Switching the entire application theme is a
     // one-line change at the point where the Kit is chosen.
     //
     // THE TRADE-OFF: adding a new PRODUCT (say, a Slider) means adding a
     // method to `Kit` and implementing it in every kit. Abstract Factory
     // makes new FAMILIES cheap and new PRODUCT TYPES expensive.
     //
     // WHERE THIS SHOWS UP: UI theme kits, cross-platform widget sets,
     // database driver sets (connection + command + reader must match), test
     // doubles vs real service sets.
     //
     // EXAMPLES YOU CAN PICTURE
     //
     // (a) DARK MODE. DarkKit makes a dark button, dark checkbox and dark text
     //     field. LightKit makes the light versions. You cannot end up with a
     //     dark button next to a light checkbox, because one kit made both.
     //     THAT GUARANTEE IS THE WHOLE POINT.
     //
     // (b) DATABASE DRIVERS. MySqlFactory returns a MySQL connection, command
     //     and result reader. PostgresFactory returns the Postgres trio. A
     //     MySQL connection with a Postgres command would be nonsense, and the
     //     factory makes that combination impossible to construct.
     //
     // (c) FURNITURE SHOP. VictorianFactory makes a Victorian chair, sofa and
     //     table. ModernFactory makes the modern set. Buying a matching living
     //     room is one factory choice.
     //
     // (d) TEST vs PROD WIRING. TestFactory hands out a fake payment gateway,
     //     fake mailer and in-memory database. ProdFactory hands out the real
     //     three. Switching environments is one line at startup.
     //
     // THE TELL IN ALL FOUR: several products must MATCH EACH OTHER, and
     // letting a caller mix them would be a bug.
     //
     static class AsAbstractFactory {
          interface Button {
               void draw();
          }

          interface Checkbox {
               void draw();
          }

          static class DarkButton implements Button {
               public void draw() {
                    System.out.println("    dark button");
               }
          }

          static class DarkCheckbox implements Checkbox {
               public void draw() {
                    System.out.println("    dark checkbox");
               }
          }

          static class LightButton implements Button {
               public void draw() {
                    System.out.println("    light button");
               }
          }

          static class LightCheckbox implements Checkbox {
               public void draw() {
                    System.out.println("    light checkbox");
               }
          }

          interface Kit { // <== SEVERAL create methods, not one
               Button createButton();

               Checkbox createCheckbox();
          }

          static class DarkKit implements Kit { // one implementation supplies the whole family
               public Button createButton() {
                    return new DarkButton();
               }

               public Checkbox createCheckbox() {
                    return new DarkCheckbox();
               }
          }

          static class LightKit implements Kit {
               public Button createButton() {
                    return new LightButton();
               }

               public Checkbox createCheckbox() {
                    return new LightCheckbox();
               }
          }

          static class Screen {
               private final Kit field; // knows only the interface, never DarkKit or LightKit

               Screen(Kit field) {
                    this.field = field;
               }

               void action() {
                    field.createButton().draw();
                    field.createCheckbox().draw(); // guaranteed to match the button above
               }
          }

          static void demo() {
               say("3. ABSTRACT FACTORY  (one factory per family, so parts always match)");
               new Screen(new DarkKit()).action();
               new Screen(new LightKit()).action();
          }
     }

     // #########################################################################
     // STRUCTURAL PATTERNS (4-6) - they answer: HOW ARE OBJECTS PUT TOGETHER?
     // #########################################################################
     //
     // Structural patterns are all about one object HOLDING another and
     // presenting a particular face to the outside. Adapter changes the face,
     // Decorator adds to it, Composite makes many objects share one face.
     //
     // =========================================================================
     // 4. ADAPTER = the skeleton where the field is a class you CANNOT change,
     // and the adapter translates between the two shapes
     // =========================================================================
     //
     // THE SITUATION: your code expects an interface. Some existing class does
     // exactly the job you need but has the wrong method names or parameters -
     // it is third-party code, or legacy code, or generated code. You cannot
     // edit it.
     //
     // THE CHANGE: `CelsiusAdapter` implements YOUR interface and holds the
     // class you cannot change. Its method body does the translation.
     //
     // THE ONE LINE THAT IS THE ENTIRE PATTERN:
     //
     // return (field.getF() - 32) * 5 / 9;
     //
     // Every adapter is a class whose methods are conversions like that.
     //
     // ADAPTER VS DECORATOR (section 6): both wrap another object, so people
     // confuse them. Adapter CHANGES THE INTERFACE and keeps behaviour the
     // same. Decorator KEEPS THE INTERFACE and adds behaviour.
     //
     // WHERE THIS SHOWS UP: wrapping a payment gateway SDK behind your own
     // PaymentProvider interface, making a legacy logger satisfy a new logging
     // interface, converting between two teams' data formats.
     //
     // EXAMPLES YOU CAN PICTURE
     //
     // (a) TRAVEL PLUG. Your Indian charger has round pins, the UK socket has
     //     flat ones. The adapter changes the SHAPE of the connection and
     //     delivers exactly the same electricity. That is the definition.
     //
     // (b) PAYMENT GATEWAYS. Your code calls PaymentProvider.charge(amount).
     //     Razorpay's SDK wants createOrder(paise, currency, receiptId).
     //     RazorpayAdapter converts rupees to paise, invents a receipt id, and
     //     calls their method. Swapping to Stripe means writing a second
     //     adapter, not editing your checkout.
     //
     // (c) OLD XML, NEW JSON. A legacy analytics library only accepts XML;
     //     your new service emits JSON. The adapter converts on the way in.
     //
     // (d) java.util.Arrays.asList(array). An array is not a List, but this
     //     hands you a List-shaped view of it. Standard-library Adapter.
     //
     // THE TELL IN ALL FOUR: the other side ALREADY WORKS and you cannot (or
     // must not) edit it. You only translate the vocabulary.
     //
     static class AsAdapter {
          // What your code wants to talk to.
          interface Thermometer {
               double celsius();
          }

          // What actually exists. Wrong units, wrong method name, and assume
          // you cannot edit this file.
          static class FahrenheitSensor {
               double getF() {
                    return 98.6;
               }
          }

          static class CelsiusAdapter implements Thermometer { // <== implements YOURS, holds THEIRS
               private final FahrenheitSensor field;

               CelsiusAdapter(FahrenheitSensor field) {
                    this.field = field;
               }

               public double celsius() {
                    return (field.getF() - 32) * 5 / 9; // the translation IS the pattern
               }
          }

          static class Display {
               private final Thermometer field; // knows only the interface it wanted

               Display(Thermometer field) {
                    this.field = field;
               }

               void action() {
                    System.out.printf("    %.1f C%n", field.celsius());
               }
          }

          static void demo() {
               say("4. ADAPTER  (translate an interface you cannot change)");
               new Display(new CelsiusAdapter(new FahrenheitSensor())).action();
          }
     }

     // =========================================================================
     // 5. COMPOSITE = the skeleton where ONE implementation holds a LIST of
     // the same interface, so trees and leaves are used identically
     // =========================================================================
     //
     // THE CHANGE: `Folder` implements `Node` AND holds a List<Node>. That one
     // sentence is the whole pattern.
     //
     // Because a Folder is itself a Node, a Folder can contain Folders, with
     // no depth limit. That is what makes it a TREE.
     //
     // THE POINT: the caller cannot tell a leaf from a branch and does not
     // need to. `size()` on a File and `size()` on a Folder are the same call.
     // No code anywhere asks "is this a folder or a file?" before acting.
     //
     // HOW Folder.size() WORKS: it loops over its children and calls size() on
     // each. Some of those children are Files (which just return a number) and
     // some are Folders (which loop again). The recursion terminates at the
     // leaves. You did not write a tree traversal - the structure does it.
     //
     // COMPARE WITH CHAIN (section 10): Chain's field is ONE object of its own
     // interface, forming a line. Composite's field is a LIST of its own
     // interface, forming a tree.
     //
     // WHERE THIS SHOWS UP: nested comments/replies, file systems and S3
     // prefixes, organisation charts, UI component trees, coupon rules made of
     // groups of rules, menus with submenus.
     //
     // EXAMPLES YOU CAN PICTURE
     //
     // (a) FILE EXPLORER. Right-click any item and ask its size. A file
     //     answers with its own bytes; a folder adds up its children, some of
     //     which are folders that do the same. You wrote no recursion loop -
     //     the shape of the tree ran it.
     //
     // (b) COMPANY HIERARCHY. countPeople() on an individual returns 1; on a
     //     department returns 1 plus the count of everyone under it. Works
     //     whether the org is 2 levels deep or 9.
     //
     // (c) REDDIT COMMENT THREADS. A comment may have replies, which may have
     //     replies. "Collapse this thread" and "count all comments" are single
     //     calls on the top node.
     //
     // (d) RESTAURANT MENU WITH SUB-MENUS. Desserts is a menu inside the
     //     dinner menu. print() on the root prints the entire card.
     //
     // (e) SHOPPING BASKET WITH COMBO OFFERS. A combo is a "product" made of
     //     products; price() on the basket totals both kinds identically.
     //
     // THE TELL IN ALL FIVE: the client wants to say "do X to this thing" and
     // NOT care whether the thing is one item or a whole subtree.
     //
     static class AsComposite {
          interface Node {
               int size();

               String name();
          }

          static class File implements Node { // a LEAF - no children
               private final String n;
               private final int bytes;

               File(String n, int bytes) {
                    this.n = n;
                    this.bytes = bytes;
               }

               public int size() {
                    return bytes;
               }

               public String name() {
                    return n;
               }
          }

          static class Folder implements Node { // a BRANCH - implements Node AND holds Nodes
               private final String n;
               private final java.util.List<Node> field = new java.util.ArrayList<>(); // <== A LIST OF ITS OWN
                                                                                       // INTERFACE

               Folder(String n) {
                    this.n = n;
               }

               Folder add(Node child) {
                    field.add(child);
                    return this;
               }

               public int size() { // children may be Files or Folders; this code does not care
                    int total = 0;
                    for (Node c : field)
                         total += c.size();
                    return total;
               }

               public String name() {
                    return n;
               }
          }

          static void demo() {
               say("5. COMPOSITE  (a branch implements the interface AND holds a list of it)");
               Node tree = new Folder("root")
                         .add(new File("a.txt", 100))
                         .add(new Folder("sub")
                                   .add(new File("b.txt", 250))
                                   .add(new File("c.txt", 150)));
               // Identical call shape for a leaf and for a whole tree.
               System.out.println("    single file : " + new File("a.txt", 100).size());
               System.out.println("    whole tree  : " + tree.size());
          }
     }

     // =========================================================================
     // 6. DECORATOR = the skeleton where the wrapper implements THE SAME
     // interface it holds, so wrappers can stack
     // =========================================================================
     //
     // THE CHANGE: `Deco` both IMPLEMENTS `Coffee` and HOLDS a `Coffee`.
     //
     // Because a decorator is itself the interface, a decorator can wrap
     // another decorator, as deep as you like. Each layer calls the layer
     // beneath it and adds a little:
     //
     // field.cost() + 20
     //
     // WHAT IT REPLACES: a subclass for every combination. Without Decorator
     // you end up writing CoffeeWithMilk, CoffeeWithSugar,
     // CoffeeWithMilkAndSugar, CoffeeWithMilkAndSugarAndCream - the class
     // count doubles with every new option. With Decorator, N options means N
     // classes and any combination is built at runtime.
     //
     // DECORATOR VS COMPOSITE: Composite holds a LIST of the interface (a tree
     // with many children). Decorator holds exactly ONE (a stack of layers).
     //
     // DECORATOR VS ADAPTER: Adapter changes the interface and keeps the
     // behaviour. Decorator keeps the interface and changes the behaviour.
     //
     // DECORATOR VS INHERITANCE: subclassing fixes the combination when you
     // compile. Decorator picks it while the program runs.
     //
     // WHERE THIS SHOWS UP: java.io streams (BufferedInputStream wrapping
     // FileInputStream is exactly this), pizza and coffee pricing, HTTP
     // middleware adding auth then logging then compression, adding retry or
     // caching to a service call.
     //
     // EXAMPLES YOU CAN PICTURE
     //
     // (a) STARBUCKS ORDER. Espresso, wrapped in Milk, wrapped in Caramel,
     //     wrapped in ExtraShot. Each wrapper adds its own price to whatever
     //     it wraps. Without this you would need an EspressoMilkCaramelShot
     //     class - and one for every other combination.
     //
     // (b) PIZZA TOPPINGS. Same idea: a Margherita wrapped in ExtraCheese
     //     wrapped in Olives. The customer chooses the stack at ORDER TIME,
     //     which is exactly why subclassing cannot do this job.
     //
     // (c) java.io. new BufferedReader(new InputStreamReader(new
     //     FileInputStream(f))). Three wrappers, each keeping the same "read"
     //     interface and adding one capability. You have been using Decorator
     //     since your first Java program.
     //
     // (d) HTTP MIDDLEWARE. The real handler wrapped in Logging wrapped in
     //     Auth wrapped in Compression. Reorder the wrapping and you reorder
     //     the behaviour, with no class edited.
     //
     // (e) RETRY + CACHE ON A SERVICE CALL. CachingClient wraps RetryingClient
     //     wraps the real client. All three satisfy the same interface, so
     //     calling code cannot tell how deep the stack is.
     //
     // THE TELL IN ALL FIVE: N optional features would mean 2^N subclasses, so
     // you stack them at runtime instead.
     //
     static class AsDecorator {
          interface Coffee {
               int cost();

               String desc();
          }

          static class Plain implements Coffee { // the innermost object
               public int cost() {
                    return 100;
               }

               public String desc() {
                    return "coffee";
               }
          }

          static abstract class Deco implements Coffee { // <== IMPLEMENTS Coffee AND HOLDS a Coffee
               protected final Coffee field;

               Deco(Coffee field) {
                    this.field = field;
               }
          }

          static class Milk extends Deco {
               Milk(Coffee c) {
                    super(c);
               }

               public int cost() {
                    return field.cost() + 20;
               } // ask the layer below, then add

               public String desc() {
                    return field.desc() + " + milk";
               }
          }

          static class Sugar extends Deco {
               Sugar(Coffee c) {
                    super(c);
               }

               public int cost() {
                    return field.cost() + 5;
               }

               public String desc() {
                    return field.desc() + " + sugar";
               }
          }

          static void demo() {
               say("6. DECORATOR  (the wrapper implements the same interface it holds)");
               Coffee c = new Sugar(new Milk(new Plain())); // layers stack at runtime
               System.out.println("    " + c.desc() + " = " + c.cost());
          }
     }

     // #########################################################################
     // BEHAVIOURAL PATTERNS (7-11) - they answer: HOW DO OBJECTS SHARE WORK?
     // #########################################################################
     //
     // Behavioural patterns are about which object decides what, and when.
     // The held field is no longer a part or a disguise - it is a piece of
     // decision-making that has been moved out of the holder.
     //
     // =========================================================================
     // 7. OBSERVER = the skeleton where `field` is a LIST and action() loops
     // =========================================================================
     //
     // THE CHANGE: same contract, same hold, same delegate - but ONE-TO-MANY
     // instead of one-to-one.
     //
     // add() plays the same role here that setField() played in STRATEGY. It
     // is the place where the field is filled in. It just appends instead of
     // replacing.
     //
     // WHAT IT BUYS YOU: `Board` does not know how many listeners exist, what
     // they do, or whether there are any at all. Register a logger, an audit
     // trail and a metrics collector tomorrow - `Board` is unchanged in every
     // case. This separates WHO CAUSES AN EVENT from WHO CARES ABOUT IT, and
     // it is the basis of every event-driven system: pub/sub, message queues,
     // UI event handlers, Kafka topics.
     //
     // THE FOLLOW-UP QUESTION TO EXPECT: if a listener calls add() or remove()
     // while action() is looping, you get ConcurrentModificationException. The
     // standard fixes are CopyOnWriteArrayList, or looping over a copy of the
     // list.
     //
     // WHERE THIS SHOWS UP: notification systems, order-status updates, social
     // feeds, stock price ticks, inventory alerts.
     //
     // EXAMPLES YOU CAN PICTURE
     //
     // (a) YOUTUBE SUBSCRIBE. The channel keeps a list of subscribers. Upload
     //     one video, everyone is pinged. The channel does not know or care
     //     whether a subscriber is a phone, a TV or an email digest.
     //
     // (b) AMAZON "NOTIFY ME WHEN IN STOCK". Each waiting customer is a
     //     listener on that product. Restock fires update() on the whole list.
     //     Unsubscribing is just removing yourself from the list.
     //
     // (c) EXCEL FORMULA CELLS. Cell C1 = A1 + B1 registers itself as a
     //     listener on A1 and B1. Type a new number into A1 and C1 recomputes
     //     itself. You never wrote "when A1 changes, update C1" anywhere.
     //
     // (d) ORDER PLACED. One event, four listeners: send SMS, email the
     //     invoice, decrement inventory, log to analytics. Adding a fifth
     //     (loyalty points) does not touch the order code at all.
     //
     // THE TELL IN ALL FOUR: one thing happens, an unknown number of parties
     // need to hear about it, and the announcer must not be edited when a new
     // listener appears.
     //
     static class AsObserver {
          interface Listener {
               void update(String msg);
          }

          static class Screen implements Listener {
               private final String id;

               Screen(String id) {
                    this.id = id;
               }

               public void update(String m) {
                    System.out.println("    " + id + " -> " + m);
               }
          }

          static class Board {
               private final java.util.List<Listener> field = new java.util.ArrayList<>(); // <== A LIST

               void add(Listener l) {
                    field.add(l);
               } // same role as setField(), but it appends

               void action(String msg) {
                    for (Listener l : field)
                         l.update(msg);
               } // <== A LOOP
          }

          static void demo() {
               say("7. OBSERVER  (the field is a List, action() loops over it)");
               Board b = new Board();
               b.add(new Screen("gate-A"));
               b.add(new Screen("gate-B"));
               b.action("flight delayed"); // one call, both gates print
          }
     }

     // =========================================================================
     // 8. STATE = the skeleton where the FIELD REPLACES ITSELF
     // =========================================================================
     //
     // THE CHANGE: the field is swappable, exactly as in Strategy - but the
     // only code that ever swaps it is the object CURRENTLY SITTING IN IT. An
     // object's last act is to install its successor.
     //
     // A READING NOTE: State and Strategy (section 11) are THE SAME STRUCTURE -
     // same field, same setter, same delegating action(). They are the classic
     // interview pair, so this section spells out the comparison in full even
     // though Strategy comes later in the file. If you want the pair read
     // together, read section 11 first and come straight back here; nothing
     // else in the file depends on that order. Two things differ.
     //
     // CHANGE (a) - THE PARAMETER TYPE:
     //
     // STRATEGY: void pay(double amt) <- receives a number
     // STATE: void push(Door d) <- receives the Door that holds it
     //
     // Strategy's method also has a parameter, so the change is NOT "a
     // parameter was added". The change is WHAT THE PARAMETER IS.
     //
     // `amt` is a double. `Card` can read it, add to it, print it - and
     // that is all. When pay() returns, `Card` has had no effect on
     // `Checkout`. It never had a reference to a `Checkout` to begin with.
     //
     // `d` is a Door - the actual object whose field currently points at
     // this state. Not information about the door. The door itself.
     //
     // CHANGE (b) - WHAT THAT MAKES POSSIBLE:
     //
     // Because `Open` holds a real Door reference, it can call methods on
     // it:
     // d.setField(new Closed());
     //
     // `Card` cannot do the equivalent. `a.setField(...)` does not compile,
     // because `a` is a double and there is nothing to call a method on.
     // `Card` has no path back to `Checkout`; the compiler cut that wire.
     //
     // SO THE FLOW REVERSES. Strategy goes one way and stops:
     //
     // caller -> Checkout.action() -> Card.pay(100) [done]
     //
     // State goes down and then calls back up:
     //
     // caller -> Door.action() -> field.push(this)
     // -> d.setField(new Closed()) [back up]
     //
     // That last arrow is a CALLBACK: the Door passes itself down, and the
     // state calls back into the Door.
     //
     // STRATEGY VS STATE IN ONE SENTENCE:
     // The structure is identical. The only question is who calls
     // setField(). Code outside the class -> STRATEGY.
     // The field itself -> STATE.
     //
     // A TEST THAT MAKES IT CONCRETE:
     // Does `new Card().pay(100)` work with no Checkout anywhere? Yes -
     // Card only ever needed a number.
     // Does `new Open().push(???)` work with no Door? No - there is
     // nothing to pass. A state is bound to its holder by that parameter.
     //
     // WHERE THE TRANSITION TABLE LIVES: nowhere central. It is spread across
     // the state classes. `Closed` knows the next state is `Open`; `Open`
     // knows the next state is `Closed`. Each class holds one row of the
     // state machine.
     //
     // WHY NOT if/else? (vending machine and ATM problems both ask this.)
     // With a status enum and conditionals, adding a `Locked` state means
     // finding and editing EVERY conditional in the class, and missing one is
     // a bug. With State you add one class and adjust which states point at
     // it. The change stays local.
     //
     // THE HONEST COST: more classes, and the state machine is no longer
     // readable in one place. For a two-state toggle, if/else really is
     // better. State earns its place when there are many transitions and the
     // behaviour per state differs a lot.
     //
     // WHERE THIS SHOWS UP: vending machine, ATM, elevator, order lifecycle,
     // booking flow - anything with a lifecycle.
     //
     // EXAMPLES YOU CAN PICTURE
     //
     // (a) OLA RIDE. A ride moves Requested -> DriverAssigned -> InTrip ->
     //     Completed. Calling cancel() on a Requested ride refunds fully;
     //     calling it during InTrip charges a fee; calling it on Completed is
     //     rejected. Same method name, three different answers, and each state
     //     object decides which state comes next.
     //
     // (b) TRAFFIC LIGHT. Red's tick() installs Green. Green's tick() installs
     //     Yellow. Yellow's tick() installs Red. The light never contains the
     //     sequence - the sequence lives distributed across three tiny classes.
     //     Adding a blinking-amber night mode adds one class.
     //
     // (c) VENDING MACHINE. Idle -> CoinInserted -> Dispensing -> Idle.
     //     Pressing "select item" while Idle prints "insert coin first". The
     //     same button, wired to the same method, behaves differently purely
     //     because a different object is sitting in the field.
     //
     // (d) ATM. NoCard / HasCard / PinEntered / OutOfCash. The OutOfCash state
     //     is why this beats an if-chain: it silently disables four operations
     //     at once, without touching any of their code.
     //
     // THE TELL IN ALL FOUR: nobody outside ever calls the setter. The object
     // currently in the field is the only thing that replaces it.
     //
     static class AsState {
          interface DoorState {
               // The parameter is the HOLDER ITSELF, not data about it.
               void push(Door d); // <== THE ONLY DIFFERENCE
          }

          static class Open implements DoorState {
               public void push(Door d) {
                    System.out.println("    closing");
                    d.setField(new Closed()); // this state chooses the next state
               }
          }

          static class Closed implements DoorState {
               public void push(Door d) {
                    System.out.println("    opening");
                    d.setField(new Open()); // this state chooses the next state
               }
          }

          static class Door {
               private DoorState field = new Closed();

               void setField(DoorState f) {
                    this.field = f;
               } // identical to Strategy's setter...

               void action() {
                    field.push(this);
               } // ...but `this` is handed over, so the FIELD can call it
          }

          static void demo() {
               say("8. STATE  (the field replaces itself - compare with STRATEGY)");
               Door d = new Door();
               // The caller calls the SAME method three times and passes
               // nothing. The output still alternates.
               d.action();
               d.action();
               d.action(); // the caller never chose a state
          }
     }

     // =========================================================================
     // 9. COMMAND = the skeleton where the field stores a REQUEST as an object,
     // and keeps a history of them so they can be undone
     // =========================================================================
     //
     // THE CHANGE: the contract gains a second method, undo(), and each
     // implementation stores the data it needs to reverse itself.
     //
     // THE IDEA: normally calling a method is an event that happens and is
     // gone. Command turns "please do X" into an OBJECT. Once a request is an
     // object you can put it in a list, keep it for later, send it over a
     // network, retry it, or run it backwards.
     //
     // WHY THE HISTORY LIST IS A STACK (last in, first out): undo must reverse
     // the MOST RECENT action first. Typing "a" then "b" and pressing undo
     // must remove "b".
     //
     // NOTE WHAT `Editor` DOES NOT KNOW: it never learns whether a command is
     // an insert, a delete or a paste. It calls run() and pushes; it calls
     // undo() and pops. Adding a new command type does not change `Editor`.
     //
     // COMMAND VS STRATEGY: both hold an interface and call one method on it.
     // The difference is intent and lifetime. A strategy is a way of doing a
     // job, held for as long as it is needed. A command is a single request,
     // recorded so it can be replayed or reversed.
     //
     // WHERE THIS SHOWS UP: undo/redo in a text editor, Tetris moves, task
     // boards, version control, job queues, transaction logs.
     //
     // EXAMPLES YOU CAN PICTURE
     //
     // (a) CTRL+Z IN GOOGLE DOCS. Every keystroke, delete and paste becomes an
     //     object pushed onto a stack. Undo pops one and calls undo() on it.
     //     The editor stores your history as a LIST OF OBJECTS, not text.
     //
     // (b) TV REMOTE. Each button holds a command object. Pointing the same
     //     physical remote at an AC instead of a TV means loading different
     //     command objects into the buttons - the buttons themselves never
     //     change.
     //
     // (c) SWIGGY ORDER QUEUE. "Prepare order #412" is created in the app,
     //     serialised, sent over the network, and executed in the restaurant
     //     kitchen minutes later. That delay is only possible because the
     //     request was turned into an object.
     //
     // (d) BANK TRANSACTION LOG. A transfer is recorded as an object so it can
     //     be replayed after a crash, or reversed as a chargeback.
     //
     // THE TELL IN ALL FOUR: the request is stored, queued, replayed or
     // reversed - which you cannot do with a plain method call.
     //
     static class AsCommand {
          interface Cmd {
               void run();

               void undo(); // <== THE ONLY DIFFERENCE: every request can reverse itself
          }

          static class Type implements Cmd {
               private final Editor target;
               private final String text; // the data needed to reverse this exact command

               Type(Editor target, String text) {
                    this.target = target;
                    this.text = text;
               }

               public void run() {
                    target.buffer.append(text);
               }

               public void undo() {
                    target.buffer.setLength(target.buffer.length() - text.length());
               }
          }

          static class Editor {
               final StringBuilder buffer = new StringBuilder();
               // A stack, because undo must reverse the most recent command first.
               private final java.util.Deque<Cmd> field = new java.util.ArrayDeque<>();

               void action(Cmd c) {
                    c.run();
                    field.push(c);
               } // do it, then remember it

               void undo() {
                    if (!field.isEmpty())
                         field.pop().undo();
               }

               public String toString() {
                    return buffer.toString();
               }
          }

          static void demo() {
               say("9. COMMAND  (a request stored as an object, so it can be undone)");
               Editor e = new Editor();
               e.action(new Type(e, "hello "));
               e.action(new Type(e, "world"));
               System.out.println("    after two commands: " + e);
               e.undo();
               System.out.println("    after undo:         " + e);
          }
     }

     // =========================================================================
     // 10. CHAIN OF RESPONSIBILITY = the skeleton where the field is the SAME
     // TYPE as the class holding it
     // =========================================================================
     //
     // THE CHANGE: one word - the TYPE of `field`. A Handler holds a Handler.
     //
     // An object holding another object of its own type is a LINKED LIST. That
     // is why this is called a chain. You have built this shape before to hold
     // data; here the same shape holds behaviour.
     //
     // WHY setField RETURNS `f` INSTEAD OF void: so chains can be built in one
     // expression - a.setField(b).setField(c) wires three links together.
     //
     // THE POINT OF THE PATTERN: the caller does not know which handler dealt
     // with the request, or whether any handler did. You can insert a handler
     // in the middle, reorder them, or delete one, and no calling code changes.
     //
     // NOTE THE THIRD DEMO CALL. A chain must define what happens when NOBODY
     // handles the request. Forgetting that case is a common bug, so the
     // "COSMIC" call exists to show it.
     //
     // WHERE THIS SHOWS UP: validation pipelines, coupon rule evaluation, ATM
     // cash dispensing (2000-note handler -> 500 -> 100), log-level filters,
     // web middleware, approval escalation.
     //
     // EXAMPLES YOU CAN PICTURE
     //
     // (a) LEAVE APPROVAL. 1 day -> your manager approves. 5 days -> manager
     //     passes it up to the director. 30 days -> it reaches HR. You submit
     //     to ONE place and never learn who actually signed it.
     //
     // (b) ATM DISPENSING 3700. The 2000-handler gives one note and forwards
     //     1700. The 500-handler gives three and forwards 200. The 100-handler
     //     gives two and finishes. Each link knows only its own denomination.
     //
     // (c) SUPPORT TICKET ESCALATION. Bot -> L1 agent -> L2 engineer ->
     //     on-call lead. Anyone can resolve and stop the chain.
     //
     // (d) LOGIN REQUEST FILTERS. Authentication -> authorization -> rate
     //     limit -> input validation -> the actual handler. Any filter can
     //     reject and the rest never run. Every web framework's middleware
     //     stack is literally this pattern.
     //
     // THE TELL IN ALL FOUR: a request travels down a line, each link asks
     // only "is this mine?", and the sender never knows who stopped it.
     //
     static class AsChain {
          static abstract class Handler {
               protected Handler field; // <== the field's type is Handler, its own type

               Handler setField(Handler f) {
                    this.field = f;
                    return f; // returning f lets chains be built in one expression
               }

               abstract void action(String req);

               protected void forward(String req) { // DELEGATE, plus an end-of-chain case
                    if (field != null)
                         field.action(req);
                    else
                         System.out.println("    nobody handled: " + req);
               }
          }

          // Each handler answers one question - "is this mine?" - and passes
          // on everything else.
          static class L1 extends Handler {
               void action(String r) {
                    if (r.equals("LOW"))
                         System.out.println("    L1 handled");
                    else
                         forward(r);
               }
          }

          static class L2 extends Handler {
               void action(String r) {
                    if (r.equals("HIGH"))
                         System.out.println("    L2 handled");
                    else
                         forward(r);
               }
          }

          static void demo() {
               say("10. CHAIN OF RESPONSIBILITY  (the field's type is its own type)");
               Handler h = new L1();
               h.setField(new L2());
               h.action("LOW"); // handled by the first link
               h.action("HIGH"); // handled by the second link
               h.action("COSMIC"); // reaches the end unhandled
          }
     }

     // =========================================================================
     // 11. STRATEGY = the skeleton, plus a setter that THE CLIENT calls
     // =========================================================================
     //
     // THE CHANGE: the field is no longer `final`, and there is a setField()
     // method. That is the whole pattern.
     //
     // WHO SWAPS THE FIELD: code outside the class. Remember this. It is the
     // only thing that separates STRATEGY from STATE in section 8.
     //
     // WHAT IT BUYS YOU: `Checkout` contains no `if (type == CARD)` anywhere.
     // Compare with the version you would write without the pattern:
     //
     // void action(double amt, String type) {
     // if (type.equals("CARD")) { ...card logic... }
     // else if (type.equals("UPI")) { ...upi logic... }
     // }
     //
     // In that version, adding ApplePay means EDITING `Checkout` - editing a
     // class that is already written, tested and deployed. Over time every
     // payment method that ever exists gets spliced into that one method.
     //
     // With Strategy, adding ApplePay means writing ONE new class. `Checkout`
     // is never reopened. This is the OPEN/CLOSED PRINCIPLE: open for
     // extension (new classes), closed for modification (no edits).
     //
     // WHERE THIS SHOWS UP: parking-lot fees per vehicle type, Splitwise split
     // rules (equal / exact / percentage), rate-limiter algorithms, cache
     // eviction policies, ride matching. It is the most common pattern in
     // interview LLD problems by a wide margin.
     //
     // EXAMPLES YOU CAN PICTURE
     //
     // (a) SWIGGY DELIVERY FEE. `Order` holds a FeeRule field. The rules are
     //     NormalFee, RainSurgeFee and FreeForGoldFee. The pricing service
     //     decides which one to install before the bill is computed. Nothing
     //     inside `Order` knows monsoon season exists.
     //
     // (b) GOOGLE MAPS ROUTE BUTTON. `Trip` holds a RouteFinder field. Tapping
     //     the car / bike / walk / train icon calls setField(...) with a
     //     different finder. Same Trip object, same "find the route" call, four
     //     completely different algorithms.
     //
     // (c) SORTING A TABLE COLUMN. Java's Collections.sort(list, comparator)
     //     IS Strategy, already in the standard library. The list is the
     //     holder, the Comparator is the swappable field, and YOU - the caller
     //     - decide which comparator goes in.
     //
     // (d) PARKING LOT FEE. `Ticket` holds a FeeStrategy. BikeFee charges 10/hr,
     //     CarFee 20/hr, TruckFee 50/hr. Adding an ElectricCarFee tomorrow is
     //     one new class; `Ticket` is not touched.
     //
     // THE TELL IN ALL FOUR: somebody OUTSIDE picks the behaviour, and the
     // picked object never picks its own replacement.
     //
     static class AsStrategy {
          interface PayMethod {
               void pay(double amt); // receives DATA ONLY - a number. Contrast with section 8.
          }

          static class Card implements PayMethod {
               public void pay(double a) {
                    System.out.println("    card: " + a);
               }
          }

          static class Upi implements PayMethod {
               public void pay(double a) {
                    System.out.println("    upi: " + a);
               }
          }

          static class Checkout {
               private PayMethod field; // dropped `final` so it can be swapped

               void setField(PayMethod f) {
                    this.field = f;
               } // <== THE ONLY DIFFERENCE

               void action(double amt) {
                    field.pay(amt);
               }
          }

          static void demo() {
               say("11. STRATEGY  (code outside the class swaps the field)");
               Checkout c = new Checkout();
               c.setField(new Card());
               c.action(100); // the CALLER chose Card
               c.setField(new Upi());
               c.action(250); // the CALLER chose Upi
          }
     }

     // =========================================================================
     // 12. THE SIX RELATIONSHIPS BETWEEN CLASSES
     // =========================================================================
     //
     // This section is NOT a pattern. It is the vocabulary underneath all of
     // them: the six ways two classes can be connected, and the arrow UML draws
     // for each. Interviewers ask you to name these directly, and they ask you
     // to justify a choice ("why aggregation and not composition here?").
     //
     // The six, ordered from weakest link to strongest:
     //
     // 1. DEPENDENCY ("uses-a") dashed arrow ----->
     // Class A mentions B somewhere in a method - as a parameter, a local
     // variable, or a return type - but stores nothing. Delete the method
     // and the link is gone. Weakest possible relationship.
     //
     // 2. ASSOCIATION ("knows-a") solid line ------
     // A keeps a long-term reference to B as a FIELD. Neither one owns the
     // other and their lifetimes are unrelated. A Student has a Teacher;
     // both exist independently.
     //
     // 3. AGGREGATION ("has-a", hollow diamond <>-----
     // shared)
     // A holds B, but B is passed IN from outside and outlives A. The
     // classic test: if A is destroyed, does B still make sense? For
     // aggregation the answer is yes. A Team holds Players; disband the
     // team and the players still exist.
     //
     // 4. COMPOSITION ("owns-a", filled diamond <#>-----
     // exclusive)
     // A CREATES B internally and B dies with A. Same test, opposite
     // answer: destroy the House and its Rooms are meaningless. The giveaway
     // in code is `new` inside the owner plus a private field never handed
     // out.
     //
     // AGGREGATION VS COMPOSITION IS THE ONE THEY PROBE. Both are "has-a"
     // and both look like a field. The question is always ownership and
     // lifetime: was the object passed in (aggregation) or created inside
     // (composition)?
     //
     // 5. REALIZATION ("implements") dashed arrow, hollow triangle ----|>
     // A class implements an interface. It promises to supply the methods
     // but inherits no code. This is the arrow behind EVERY pattern above -
     // "program to an interface" means "prefer realization".
     //
     // 6. INHERITANCE ("is-a") solid arrow, hollow triangle ----|>
     // A class extends another and inherits its code. The strongest and
     // most rigid link: a change in the parent reaches every child.
     //
     // THE RULE INTERVIEWERS WANT: prefer composition over inheritance.
     // Inheritance is fixed at compile time and locks a subclass to its
     // parent forever; a held field can be swapped while the program runs.
     // Section 6 (Decorator) is that rule in action - it replaces a
     // combinatorial explosion of subclasses with wrapping.
     //
     // The code below is the smallest example of each, in the same order.
     //
     static class Relationships {

          // MORE DEPENDENCY EXAMPLES (Uses-A - the loosest link):
          // - A Chef USES a knife during cook(). He does not own that knife
          //   and nothing about him remembers it after the dish is served.
          // - OrderService.checkout(PaymentGateway g) - the gateway arrives as
          //   a parameter, is used, and is gone when the method returns.
          // - A method that creates a `new SimpleDateFormat(...)` as a local
          //   variable, formats one date, and lets it be garbage collected.
          // THE TEST: it appears in a parameter, a local variable or a return
          // type - NEVER as a field. Change the used class and the user class
          // may need recompiling; that is the only tie between them.
          //
          // 1. DEPENDENCY - Printer USES a Report. It stores nothing.
          static class Report {
               String text() {
                    return "quarterly numbers";
               }
          }

          static class Printer {
               void print(Report r) { // mentioned only as a parameter
                    System.out.println("    dependency  : printing " + r.text());
               }
          }

          // MORE ASSOCIATION EXAMPLES (Knows-A - a lasting link, no ownership):
          // - Doctor and Patient. Each has a reference to the other, both
          //   existed before the appointment and both continue after it.
          // - Driver and Car. The driver knows their car; deleting the driver
          //   does not delete the car, and vice versa.
          // - Customer and Address (when the address is shared or reusable).
          // - MANY-TO-MANY: Students and Courses. Held on both sides as lists.
          //   When the link itself needs attributes - enrolment date, grade -
          //   promote the link to its own class (`Enrolment`). That new class
          //   is called an ASSOCIATION CLASS and is a normal interview follow-up.
          // THE TEST: it IS a field (unlike dependency), but neither side
          // creates or destroys the other (unlike composition).
          //
          // 2. ASSOCIATION - Student KNOWS a Teacher. Separate lifetimes,
          // neither owns the other.
          static class Teacher {
               final String name;

               Teacher(String name) {
                    this.name = name;
               }
          }

          static class Student {
               private final Teacher tutor; // a long-lived field, but no ownership

               Student(Teacher tutor) {
                    this.tutor = tutor;
               }

               void show() {
                    System.out.println("    association : tutor is " + tutor.name);
               }
          }

          // MORE AGGREGATION EXAMPLES (Has-A, borrowed):
          // - A Playlist HAS Songs. Delete the playlist; the songs remain in
          //   your library and in other playlists.
          // - A University department HAS Professors. Shut the department and
          //   the professors are reassigned, not deleted.
          // - A Library HAS Books that were acquired elsewhere and can be
          //   transferred to another branch.
          // - A ParkingLot HAS Cars parked in it - very obviously borrowed.
          // THE TEST - WHERE DOES `new` HAPPEN? The parts are CREATED OUTSIDE
          // and handed in through the constructor or an add() method. That is
          // the single reliable difference from composition below.
          //
          // 3. AGGREGATION - Team HAS Players, passed in from outside. Disband
          // the team and the players are unaffected.
          static class Player {
               final String name;

               Player(String name) {
                    this.name = name;
               }
          }

          static class Team {
               private final java.util.List<Player> players; // handed IN, not created here

               Team(java.util.List<Player> players) {
                    this.players = players;
               }

               void show() {
                    System.out.println("    aggregation : " + players.size() + " players, they outlive the team");
               }
          }

          // MORE COMPOSITION EXAMPLES (Has-A, owned - the strong Has-A):
          // - A Car OWNS its Engine. The engine is built with the car and is
          //   scrapped with it; it has no independent life in your model.
          // - An Order OWNS its OrderLines. Delete the order and the lines are
          //   meaningless - nobody keeps a stray line item around.
          // - A Human OWNS a Heart. An Invoice OWNS its line items. A Window
          //   OWNS its title bar and scroll bars.
          // - A Book OWNS its Chapters (a chapter does not migrate to another
          //   book).
          // THE TEST - WHERE DOES `new` HAPPEN? Inside the owner, usually in
          // its constructor, and the parts are never handed out to anyone
          // else. Destroy the whole and the parts die with it.
          //
          // THE SAME PAIR CAN BE EITHER, DEPENDING ON THE MODEL: rooms inside
          // a house are composition; desks inside an office are aggregation if
          // the company moves desks between offices. Lifetime decides, not the
          // nouns.
          //
          // 4. COMPOSITION - House OWNS its Rooms. It creates them, never hands
          // them out, and they are meaningless without it.
          static class Room {
               final String label;

               Room(String label) {
                    this.label = label;
               }
          }

          static class House {
               private final java.util.List<Room> rooms = new java.util.ArrayList<>();

               House() {
                    rooms.add(new Room("kitchen")); // created INSIDE the constructor - this is the giveaway
                    rooms.add(new Room("bedroom"));
               }

               void show() {
                    System.out.println("    composition : " + rooms.size() + " rooms, they die with the house");
               }
          }

          // MORE REALIZATION EXAMPLES (Can-Do - a promise with no inherited code):
          // - ArrayList CAN-DO List. HashMap CAN-DO Map. Every collection you
          //   use is a realization of an interface.
          // - A Duck CAN-DO Flyable and CAN-DO Swimmable at the same time. A
          //   class may realize many interfaces but extend only one class -
          //   which is exactly why interfaces exist in Java.
          // - Comparable: "I promise I can be ordered", which is what lets
          //   Collections.sort() work on your class without knowing about it.
          // - Runnable: "I promise I have a run() method", which is what lets
          //   a Thread accept your object.
          // THE TEST: it says WHAT the class can do and nothing about HOW.
          // No behaviour is inherited - the class supplies all of it.
          //
          // 5. REALIZATION - Sms IMPLEMENTS an interface. Promises methods,
          // inherits no code.
          interface Channel {
               void send(String m);
          }

          static class Sms implements Channel {
               public void send(String m) {
                    System.out.println("    realization : sms -> " + m);
               }
          }

          // MORE INHERITANCE EXAMPLES (Is-A - the tightest link):
          // - A Car IS-A Vehicle. A SavingsAccount IS-A Account. A Manager
          //   IS-A Employee. Note the direction: always specific -> general.
          //   `class Vehicle extends Car` is backwards and is a real mistake
          //   people make in interviews.
          // - IOException IS-A Exception, which is how one catch block can
          //   handle a whole family.
          //
          // THE SUBSTITUTION TEST: say the sentence out loud with "is a kind
          // of". "A Car is a kind of Vehicle" - true, so inherit. "A Car is a
          // kind of Engine" - false, so that is composition, not inheritance.
          //
          // THE CLASSIC TRAP: Square extends Rectangle. Mathematically true,
          // but setWidth(5) on a Square must also change the height, which
          // breaks every caller written against Rectangle. That is a LISKOV
          // SUBSTITUTION violation, and it is why "prefer composition over
          // inheritance" is the standing advice.
          //
          // 6. INHERITANCE - PriorityQueueTask EXTENDS Task and inherits its
          // code, then overrides part of it.
          static class Task {
               void run() {
                    System.out.println("    inheritance : running a plain task");
               }
          }

          static class PriorityTask extends Task {
               @Override
               void run() {
                    System.out.println("    inheritance : running a priority task (overrode the parent)");
               }
          }

          static void demo() {
               say("12. THE SIX RELATIONSHIPS  (the vocabulary under every pattern)");
               new Printer().print(new Report());
               new Student(new Teacher("Rao")).show();
               new Team(new java.util.ArrayList<>(java.util.List.of(new Player("A"), new Player("B")))).show();
               new House().show();
               new Sms().send("hello");
               new PriorityTask().run();
          }
     }

     // =========================================================================
     // 13. SOLID - the five rules the twelve sections above are obeying
     // =========================================================================
     //
     // Sections 1-12 showed WHAT to build. SOLID is WHY those shapes are the
     // right ones. Every pattern above is one or more of these five rules made
     // concrete, so learn them last, not first - now each rule has code you
     // have already read attached to it.
     //
     // The name is an acronym of the five principle names:
     //
     // S - SINGLE RESPONSIBILITY   one reason to change
     // O - OPEN/CLOSED             extend by adding, not by editing
     // L - LISKOV SUBSTITUTION     a subtype must be usable as its parent
     // I - INTERFACE SEGREGATION   no client forced to depend on unused methods
     // D - DEPENDENCY INVERSION    depend on interfaces, not concrete classes
     //
     // WHAT THEY ARE FOR, IN ONE SENTENCE: code changes constantly, and these
     // five rules keep a change LOCAL - confined to new code, or to one class -
     // instead of rippling through files that had nothing to do with it.
     //
     // THEY ARE GUIDELINES, NOT LAWS. Applied blindly they produce a hundred
     // one-method interfaces for a program that will never change. The honest
     // interview answer is "I apply these where the code is likely to change,
     // and I keep it simple where it is not."
     //
     static class SolidPrinciples {

          // =====================================================================
          // S - SINGLE RESPONSIBILITY PRINCIPLE
          // =====================================================================
          //
          // A class should have ONE REASON TO CHANGE.
          //
          // "Reason to change" means a PERSON or DEPARTMENT who can ask for
          // something different. Not "one method" and not "one job" loosely -
          // one source of change requests.
          //
          // Take a single Employee class that calculates pay, saves itself to
          // the database and prints a report. Three different people can force
          // an edit to that one file: Finance changes the tax formula, the DBA
          // changes the schema, and Marketing changes the report layout. Three
          // reasons to change means three responsibilities, so it should be
          // three classes.
          //
          // WHY IT ACTUALLY BITES: when Finance asks for a tax change, you edit
          // a file that also contains the report code, and now the report has
          // to be re-tested too. Responsibilities that share a file share
          // blame, share merge conflicts, and share regressions.
          //
          // EXAMPLES YOU CAN PICTURE
          //
          // (a) A RESTAURANT. The chef cooks, the waiter serves, the cashier
          //     bills. One person doing all three is how a busy evening
          //     collapses. Nobody designs a restaurant as one role.
          //
          // (b) INVOICE. Calculating the total, rendering the PDF, and emailing
          //     it are three responsibilities. Switching from PDF to HTML
          //     should not risk breaking the arithmetic.
          //
          // (c) A "UserManager" CLASS that validates passwords, writes to the
          //     database, sends welcome emails and generates reports. The name
          //     "Manager" or "Helper" or "Util" is usually the smell itself -
          //     it is a name that admits the class has no single job.
          //
          // (d) ORDER PROCESSING. OrderValidator, OrderRepository,
          //     PaymentProcessor, NotificationSender. Four classes, four
          //     reasons to change, four independently testable pieces.
          //
          // THE TELL: describe the class in one sentence. If you need the word
          // "and" - "it calculates pay AND saves it" - you have found a second
          // responsibility.
          //
          // RELATED PATTERNS: Command gives each request its own class.
          // Strategy pulls one varying calculation out into its own class.
          //
          static class Srp {
               // BAD (shown as text only, so it cannot be copied by accident):
               //
               // class Employee {
               //      double calculatePay() { ... }   // Finance changes this
               //      void save() { ... }             // the DBA changes this
               //      String report() { ... }         // Marketing changes this
               // }
               //
               // GOOD - one reason to change per class:

               static class Employee { // just the data
                    final String name;
                    final double hours;

                    Employee(String name, double hours) {
                         this.name = name;
                         this.hours = hours;
                    }
               }

               static class PayCalculator { // changes only when Finance asks
                    double pay(Employee e) {
                         return e.hours * 500;
                    }
               }

               static class EmployeeRepository { // changes only when the schema changes
                    void save(Employee e) {
                         System.out.println("    SRP : saved " + e.name + " to the database");
                    }
               }

               static class EmployeeReport { // changes only when the layout changes
                    void print(Employee e, double pay) {
                         System.out.println("    SRP : report -> " + e.name + " earned " + pay);
                    }
               }
          }

          // =====================================================================
          // O - OPEN/CLOSED PRINCIPLE
          // =====================================================================
          //
          // A class should be OPEN FOR EXTENSION but CLOSED FOR MODIFICATION.
          //
          // In plain words: you should be able to add new behaviour by writing
          // a NEW class, without opening and editing a class that already
          // works, is already tested and is already in production.
          //
          // THE SIGNATURE VIOLATION is a switch or if-else chain over a type:
          //
          // if (shape.equals("CIRCLE")) { ... }
          // else if (shape.equals("SQUARE")) { ... }
          //
          // Every new shape reopens that method. The method grows forever, and
          // each edit risks the shapes that already worked.
          //
          // WHY EDITING WORKING CODE IS THE PROBLEM: the tested code and the
          // untested new code now live in the same method, so your regression
          // risk is the whole method, not just the new part.
          //
          // EXAMPLES YOU CAN PICTURE
          //
          // (a) A PHONE WITH A USB-C PORT. Adding a keyboard, a mic or a hub
          //     does not require opening the phone. The port is the extension
          //     point; the sealed body is "closed for modification".
          //
          // (b) DISCOUNT RULES. Christmas, Diwali, first-order, student. As an
          //     if-chain, marketing edits your pricing engine four times a
          //     year. As a Discount interface, each campaign is a new file.
          //
          // (c) BROWSER EXTENSIONS. Chrome ships sealed; the whole extension
          //     store is new behaviour added without Google editing Chrome.
          //
          // (d) PAYMENT METHODS. Card, UPI, wallet, EMI, ApplePay. This is why
          //     section 11 (Strategy) exists - it is Open/Closed with a name.
          //
          // THE TELL: ask "to add the next variant, do I write a new file or
          // edit an old one?" If you must edit, the design is not closed.
          //
          // THE HONEST CAVEAT: you cannot make code open to every possible
          // future change. Choose the ONE axis that actually varies - here,
          // the shape type - and leave the rest simple.
          //
          // RELATED PATTERNS: Strategy, Decorator, Factory Method, Chain of
          // Responsibility, Visitor. Almost every pattern is a way of paying
          // for this rule.
          //
          static class Ocp {
               // BAD:
               //
               // double area(String type, double a) {
               //      if (type.equals("CIRCLE")) return 3.14 * a * a;
               //      else if (type.equals("SQUARE")) return a * a;
               //      // ...and this method is edited again for every new shape
               // }
               //
               // GOOD - a new shape is a new class, and area() is never reopened:

               interface Shape {
                    double area();
               }

               static class Circle implements Shape {
                    private final double r;

                    Circle(double r) {
                         this.r = r;
                    }

                    public double area() {
                         return 3.14 * r * r;
                    }
               }

               static class Square implements Shape {
                    private final double s;

                    Square(double s) {
                         this.s = s;
                    }

                    public double area() {
                         return s * s;
                    }
               }

               // Triangle was added LATER. Nothing above or below was edited.
               static class Triangle implements Shape {
                    private final double b, h;

                    Triangle(double b, double h) {
                         this.b = b;
                         this.h = h;
                    }

                    public double area() {
                         return 0.5 * b * h;
                    }
               }

               static double total(java.util.List<Shape> shapes) { // written once, forever
                    double sum = 0;
                    for (Shape s : shapes)
                         sum += s.area();
                    return sum;
               }
          }

          // =====================================================================
          // L - LISKOV SUBSTITUTION PRINCIPLE
          // =====================================================================
          //
          // Anywhere the parent type is expected, ANY subtype must work without
          // the caller noticing or being told.
          //
          // The compiler already lets you pass a Square where a Rectangle is
          // expected - that part is free. Liskov is about BEHAVIOUR: the
          // substitution must not surprise the caller. A subclass may not
          // throw a new exception the parent never threw, may not refuse to do
          // what the parent promised, and may not need the caller to check its
          // type first.
          //
          // THE CANONICAL COUNTER-EXAMPLE - SQUARE EXTENDS RECTANGLE:
          //
          // A square IS a rectangle in mathematics, so it feels correct. But
          // Rectangle promises "setWidth changes only the width". A Square
          // must change the height too, or stop being a square. So this test
          // passes for Rectangle and fails for Square:
          //
          // r.setWidth(5); r.setHeight(4); assert r.area() == 20;
          //
          // A Square returns 16. The caller did nothing wrong - the hierarchy
          // lied. The fix is that they are siblings, not parent and child:
          // both implement a Shape interface, neither extends the other.
          //
          // EXAMPLES YOU CAN PICTURE
          //
          // (a) BIRD.FLY(). Ostrich extends Bird and throws
          //     UnsupportedOperationException from fly(). Every loop over
          //     birds now needs a special case. The fix: separate Bird from
          //     Flyable, and let the ostrich simply not implement Flyable.
          //
          // (b) SQUARE / RECTANGLE, above. The most-asked version.
          //
          // (c) READ-ONLY LIST. A subclass of List whose add() throws breaks
          //     every method written against List. This is exactly why
          //     Collections.unmodifiableList is documented as a view with
          //     restrictions - the JDK has this scar.
          //
          // (d) FILE STORAGE. LocalStorage and S3Storage both implement
          //     Storage.save(). If S3Storage silently truncates filenames
          //     over 100 characters, it is not substitutable, even though it
          //     compiles perfectly.
          //
          // THE TELL: if calling code needs `if (x instanceof Ostrich)` to
          // stay correct, substitution has already failed.
          //
          // PRACTICAL SUMMARY: inheritance is a promise about behaviour, not
          // a way to reuse a few methods. When the subtype cannot keep the
          // promise, use composition or a sibling interface instead.
          //
          static class Lsp {
               // BAD:
               //
               // class Rectangle { void setWidth(int w); void setHeight(int h); }
               // class Square extends Rectangle {
               //      void setWidth(int w) { this.w = w; this.h = w; }   // surprises the caller
               // }
               //
               // GOOD - siblings under one interface, so neither inherits a
               // promise it cannot keep:

               interface Shape {
                    int area();
               }

               static class Rectangle implements Shape {
                    private final int w, h;

                    Rectangle(int w, int h) {
                         this.w = w;
                         this.h = h;
                    }

                    public int area() {
                         return w * h;
                    }
               }

               static class Square implements Shape {
                    private final int side;

                    Square(int side) {
                         this.side = side;
                    }

                    public int area() {
                         return side * side;
                    }
               }

               // Works for every Shape, now and later, with no type checks.
               static void report(Shape s) {
                    System.out.println("    LSP : area is " + s.area() + ", caller never asked what shape it is");
               }
          }

          // =====================================================================
          // I - INTERFACE SEGREGATION PRINCIPLE
          // =====================================================================
          //
          // No class should be forced to implement methods it does not use.
          //
          // Prefer several small, focused interfaces over one large one. The
          // symptom of breaking this rule is an implementation full of empty
          // method bodies or `throw new UnsupportedOperationException()`.
          //
          // Take one Worker interface with work(), eat() and sleep(). A human
          // employee implements all three happily. Then a RobotWorker arrives:
          // it works, but it does not eat or sleep, so two of its three
          // methods are lies. Split the interface into Workable, Eatable and
          // Sleepable, and the robot implements only Workable.
          //
          // HOW IT RELATES TO LISKOV: an empty method body is usually a Liskov
          // violation waiting to happen. Interface Segregation prevents it at
          // the source, by never handing the class a promise it cannot keep.
          //
          // EXAMPLES YOU CAN PICTURE
          //
          // (a) AN ALL-IN-ONE PRINTER INTERFACE with print(), scan(), fax()
          //     and staple(). A cheap home printer must implement fax() and
          //     staple() as no-ops. Split into Printer, Scanner and Fax, and
          //     each device implements only what it really does.
          //
          // (b) A RESTAURANT MENU. Vegetarians should not have to read past
          //     forty meat dishes. Separate menu cards are Interface
          //     Segregation applied to paper.
          //
          // (c) READ vs WRITE. Splitting a Repository into ReadRepository and
          //     WriteRepository means a reporting service can be handed read
          //     access ONLY - the type system now prevents an accidental
          //     write. Segregation is a security tool as well as a tidiness
          //     one.
          //
          // (d) java.lang.Runnable HAS ONE METHOD. That is why it fits
          //     threads, executors, lambdas and event handlers. Small
          //     interfaces get reused; big ones do not.
          //
          // THE TELL: an implementing class with an empty method body, a
          // `return null`, or an UnsupportedOperationException. Each one is
          // the class saying it was handed the wrong contract.
          //
          static class Isp {
               // BAD:
               //
               // interface Worker { void work(); void eat(); void sleep(); }
               // class Robot implements Worker {
               //      public void work()  { ... }
               //      public void eat()   { }   // empty - the smell
               //      public void sleep() { }   // empty - the smell
               // }
               //
               // GOOD - one capability per interface, mixed as needed:

               interface Workable {
                    void work();
               }

               interface Eatable {
                    void eat();
               }

               static class Human implements Workable, Eatable { // takes both
                    public void work() {
                         System.out.println("    ISP : human works");
                    }

                    public void eat() {
                         System.out.println("    ISP : human eats");
                    }
               }

               static class Robot implements Workable { // takes only what is true
                    public void work() {
                         System.out.println("    ISP : robot works, and is never asked to eat");
                    }
               }
          }

          // =====================================================================
          // D - DEPENDENCY INVERSION PRINCIPLE
          // =====================================================================
          //
          // High-level code should not depend on low-level code. Both should
          // depend on an interface.
          //
          // HIGH-LEVEL means the code that expresses the business rule -
          // "notify the customer". LOW-LEVEL means the mechanism - "open an
          // SMTP socket". Normally the rule reaches down and names the
          // mechanism. Dependency Inversion turns that arrow around: the rule
          // names an INTERFACE, and the mechanism implements it. The
          // dependency now points UP, from detail to abstraction, which is
          // what "inversion" means.
          //
          // THE ONE-LINE TEST: does the word `new` appear inside your business
          // class, naming a concrete service? If OrderService contains
          // `new SmtpMailer()`, it is welded to SMTP. Take it as a constructor
          // parameter instead and the weld is gone.
          //
          // WHAT THAT BUYS YOU: in a unit test you pass a fake mailer and
          // assert it was called, with no mail server anywhere. That single
          // benefit is why this principle is the one interviewers push on.
          //
          // Passing dependencies in from outside has a name you should use:
          // DEPENDENCY INJECTION. Spring, Guice and Dagger are frameworks that
          // do the passing for you; the principle works identically without
          // them, as the code below shows.
          //
          // EXAMPLES YOU CAN PICTURE
          //
          // (a) A WALL SOCKET. Your laptop does not depend on the power
          //     station. Both depend on the socket standard. The station can
          //     switch from coal to solar and your laptop never notices.
          //
          // (b) NOTIFICATIONS. OrderService depends on a Notifier interface.
          //     Today it is email, tomorrow SMS, next month WhatsApp - and
          //     OrderService is never edited for any of them.
          //
          // (c) THE DATABASE. Business logic depends on UserRepository, an
          //     interface. MySqlUserRepository, MongoUserRepository and
          //     InMemoryUserRepository implement it. The last one makes your
          //     tests run in milliseconds.
          //
          // (d) THE TV REMOTE. It depends on "a device that accepts commands",
          //     not on Sony. The same remote drives a different brand.
          //
          // THE TELL: `new SomeConcreteService()` inside a class that is
          // supposed to hold business rules. Move that `new` outward, to
          // main() or to a factory, and take the interface as a parameter.
          //
          // RELATED SECTIONS: this is why the skeleton at section 0 declares
          // its field as the INTERFACE type. Dependency Inversion is the
          // principle; the whole file is the demonstration.
          //
          static class Dip {
               // BAD:
               //
               // class OrderService {
               //      private final SmtpMailer mailer = new SmtpMailer(); // welded shut
               //      void place() { mailer.sendEmail("..."); }           // cannot be tested offline
               // }
               //
               // GOOD - depend on the abstraction, receive the detail:

               interface Notifier { // owned by the high-level side
                    void notify(String message);
               }

               static class EmailNotifier implements Notifier { // a swappable detail
                    public void notify(String m) {
                         System.out.println("    DIP : email -> " + m);
                    }
               }

               static class SmsNotifier implements Notifier { // another detail, added later
                    public void notify(String m) {
                         System.out.println("    DIP : sms   -> " + m);
                    }
               }

               static class OrderService { // the business rule
                    private final Notifier notifier; // the INTERFACE, never a concrete class

                    OrderService(Notifier notifier) { // injected from outside
                         this.notifier = notifier;
                    }

                    void placeOrder(String item) {
                         System.out.println("    DIP : order placed for " + item);
                         notifier.notify("your " + item + " is confirmed");
                    }
               }
          }

          static void demo() {
               say("13. SOLID  (the five rules the twelve sections above obey)");

               Srp.Employee e = new Srp.Employee("Asha", 8);
               double pay = new Srp.PayCalculator().pay(e);
               new Srp.EmployeeRepository().save(e);
               new Srp.EmployeeReport().print(e, pay);

               System.out.println("    OCP : total area is " + Ocp.total(java.util.List.of(
                         new Ocp.Circle(1), new Ocp.Square(2), new Ocp.Triangle(3, 4))));

               Lsp.report(new Lsp.Rectangle(5, 4)); // both are Shapes, and the
               Lsp.report(new Lsp.Square(4)); // caller treats them identically

               new Isp.Human().work();
               new Isp.Human().eat();
               new Isp.Robot().work();

               new Dip.OrderService(new Dip.EmailNotifier()).placeOrder("book");
               new Dip.OrderService(new Dip.SmsNotifier()).placeOrder("phone"); // one word changed
          }
     }

     static void say(String s) {
          System.out.println("\n" + s + "\n" + "-".repeat(64));
     }

     public static void main(String[] args) {
          System.out.println("ONE SKELETON, ELEVEN PATTERNS, SIX RELATIONSHIPS, FIVE PRINCIPLES");
          Skeleton.demo();

          // CREATIONAL - how objects get made
          AsSingleton.demo();
          AsFactory.demo();
          AsAbstractFactory.demo();

          // STRUCTURAL - how objects are composed into bigger shapes
          AsAdapter.demo();
          AsComposite.demo();
          AsDecorator.demo();

          // BEHAVIOURAL - how objects share work at run time
          AsObserver.demo();
          AsState.demo();
          AsCommand.demo();
          AsChain.demo();
          AsStrategy.demo();
          Relationships.demo();
          SolidPrinciples.demo();

          // ------------------------------------------------------------------
          // THIS TABLE IS THE POINT OF THE FILE.
          //
          // In an interview nobody asks "what is Strategy?". You are given a
          // REQUIREMENT and have to recognise the shape it needs. If you
          // studied pattern-name -> definition, you are practising the lookup
          // in the wrong direction, and it fails under pressure.
          //
          // Practise it in this direction instead. The MIDDLE COLUMN is what
          // you actually type; the pattern name is only the label you say out
          // loud.
          // ------------------------------------------------------------------
          System.out.println("""

                    ----------------------------------------------------------------
                    RECALL DRILL - go left to right, never "what is Strategy?"
                    ----------------------------------------------------------------
                    CREATIONAL
                    "Exactly one, application-wide"     -> STATIC field of self   -> SINGLETON
                    "Create the right subtype"          -> RETURN the interface   -> FACTORY METHOD
                    "All the parts must match"          -> one factory per family -> ABSTRACT FACTORY

                    STRUCTURAL
                    "Library has the wrong methods"     -> wrap + translate       -> ADAPTER
                    "Folders inside folders"            -> implement it, hold a
                                                           LIST of it             -> COMPOSITE
                    "Add milk, then sugar, at runtime"  -> implement it, hold ONE
                                                           of it                  -> DECORATOR

                    BEHAVIOURAL
                    "Notify every display on change"    -> hold a LIST + loop     -> OBSERVER
                    "Behaves differently when idle
                     vs dispensing"                     -> hold + field sets self -> STATE
                    "Undo the last action"              -> store requests, stack  -> COMMAND
                    "Escalate until someone handles"    -> field of its OWN type  -> CHAIN
                    "Fee changes by vehicle type"       -> hold + caller sets     -> STRATEGY
                    ----------------------------------------------------------------
                    RELATIONSHIPS - weakest link to strongest
                    ----------------------------------------------------------------
                    uses-a, stores nothing              -> method parameter only  -> DEPENDENCY
                    knows-a, separate lifetimes         -> plain field            -> ASSOCIATION
                    has-a, passed in, outlives owner    -> field set in ctor      -> AGGREGATION
                    owns-a, created inside, dies with   -> `new` inside the owner -> COMPOSITION
                    implements, inherits no code        -> implements Interface   -> REALIZATION
                    is-a, inherits code                 -> extends Parent         -> INHERITANCE
                    ----------------------------------------------------------------
                    SOLID - the reason all of the above are shaped that way
                    ----------------------------------------------------------------
                    "this class changes for 3 reasons"   -> split it up            -> SINGLE RESPONSIBILITY
                    "another if-else for a new type"     -> interface + new class  -> OPEN/CLOSED
                    "the subclass throws Unsupported"    -> make them siblings     -> LISKOV SUBSTITUTION
                    "half the methods are empty"         -> split the interface    -> INTERFACE SEGREGATION
                    "`new SmtpMailer()` in my service"   -> take it as a parameter -> DEPENDENCY INVERSION
                    ----------------------------------------------------------------""");
     }
}
