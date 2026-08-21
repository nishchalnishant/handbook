import java.util.*;

/*
 * Proofs for notes/TEXT_TO_CODE.md
 *   javac TextToCodeProofs.java && java TextToCodeProofs
 *
 * A. the same sentence -> four different correct shapes, depending on HOW variants differ
 * B. why an interface cannot hold state (the rule that decides Q2)
 * C. switch -> interface, the refactor you use most
 * D. the food-delivery worked example, actually running
 */

// ===============================================================
// A. "There should be a vehicle. There could be different types."
// ===============================================================

// A1. differ only by DATA -> enum
enum VehicleType {
    BIKE(1, 10.0), CAR(2, 20.0), TRUCK(4, 40.0);
    private final int size; private final double rate;
    VehicleType(int s, double r){ size = s; rate = r; }
    int size(){ return size; }
    double rate(){ return rate; }
}
record SimpleVehicle(String plate, VehicleType type) {}

// A2. differ by BEHAVIOUR, share no state -> interface
interface Parkable {
    int size();
    default String describe(){ return "takes " + size() + " spot(s)"; }
}
record Bike(String plate) implements Parkable { public int size(){ return 1; } }
record Car (String plate) implements Parkable { public int size(){ return 2; } }

// A3. share STATE -> abstract class
abstract class Vehicle {
    protected final String plate;                 // interface cannot hold this
    protected Vehicle(String plate){ this.plate = plate; }
    String plate(){ return plate; }               // written once, inherited
    abstract int size();                          // each subclass must differ
}
class Truck extends Vehicle { Truck(String p){ super(p); } int size(){ return 4; } }

// A4. state + an extra capability -> BOTH
interface Chargeable { double kwh(); }
class ElectricCar extends Vehicle implements Chargeable {
    ElectricCar(String p){ super(p); }
    int size(){ return 2; }
    public double kwh(){ return 75.0; }
}

// ===============================================================
// C. switch -> interface
// ===============================================================
class NotifierBefore {
    String send(String kind, String msg) {
        switch (kind) {                            // the smell: switch on a TYPE
            case "email": return "email: " + msg;
            case "sms":   return "sms: "   + msg;
            default: throw new IllegalArgumentException(kind);
        }
    }
}
interface Channel { String send(String msg); }
class Email implements Channel { public String send(String m){ return "email: " + m; } }
class Sms   implements Channel { public String send(String m){ return "sms: "   + m; } }
class Push  implements Channel { public String send(String m){ return "push: "  + m; } }
class NotifierAfter {
    private final Channel channel;
    NotifierAfter(Channel c){ channel = c; }       // injected
    String send(String msg){ return channel.send(msg); }
}

// ===============================================================
// D. Food delivery — the worked example, running
// ===============================================================
record Item(String name, double price) {}                     // value -> record
enum Status { PLACED, PREPARING, OUT_FOR_DELIVERY, DELIVERED } // fixed list -> enum
class Restaurant {
    private final String name;
    Restaurant(String n){ name = n; }
    String name(){ return name; }
}
interface PaymentMethod { boolean pay(double amount); }        // varies -> interface
class CardPayment   implements PaymentMethod { public boolean pay(double a){ System.out.println("        card charged "   + a); return true; } }
class UpiPayment    implements PaymentMethod { public boolean pay(double a){ System.out.println("        upi charged "    + a); return true; } }
class WalletPayment implements PaymentMethod {
    private double balance;
    WalletPayment(double b){ balance = b; }
    public boolean pay(double a){
        if (a > balance) { System.out.println("        wallet declined, balance " + balance); return false; }
        balance -= a; System.out.println("        wallet charged " + a); return true;
    }
}
interface OrderListener { void onStatusChange(Order o, Status s); }   // observer

class Order {
    private final List<Item> items;                    // aggregation: items pre-exist
    private final Restaurant restaurant;               // aggregation
    private Status status = Status.PLACED;             // changes -> class, not record
    private final List<OrderListener> listeners = new ArrayList<>();  // composition

    Order(Restaurant r, List<Item> items) {
        if (items.isEmpty()) throw new IllegalArgumentException("order needs items"); // invariant
        this.restaurant = r;
        this.items = List.copyOf(items);
    }
    double total(){ return items.stream().mapToDouble(Item::price).sum(); }
    Status status(){ return status; }
    Restaurant restaurant(){ return restaurant; }
    void addListener(OrderListener l){ listeners.add(l); }
    boolean checkout(PaymentMethod method){ return method.pay(total()); }   // DIP
    void advanceTo(Status next){
        this.status = next;
        for (OrderListener l : listeners) l.onStatusChange(this, next);
    }
}

public class TextToCodeProofs {
    public static void main(String[] args) {
        System.out.println("A. one sentence, four correct shapes");
        System.out.println("   enum      : truck occupies " + new SimpleVehicle("KA01", VehicleType.TRUCK).type().size());
        System.out.println("   interface : car " + new Car("KA02").describe());
        Vehicle v = new Truck("KA03");
        System.out.println("   abstract  : " + v.plate() + " size " + v.size() + "  (plate stored in parent)");
        ElectricCar e = new ElectricCar("KA04");
        System.out.println("   both      : " + e.plate() + " size " + e.size() + " kwh " + e.kwh());
        System.out.println("               is-a Vehicle " + (e instanceof Vehicle)
                         + ", can-do Chargeable " + (e instanceof Chargeable));

        System.out.println("\nB. why interfaces cannot decide Q2");
        System.out.println("   `interface X { private int c; }`  -> compile error");
        System.out.println("   `interface X { int c = 5; }`      -> silently public static final (a CONSTANT)");
        System.out.println("   => per-object state forces an abstract class");

        System.out.println("\nC. switch -> interface");
        System.out.println("   before: " + new NotifierBefore().send("email", "hi"));
        for (Channel c : List.of(new Email(), new Sms(), new Push()))
            System.out.println("   after : " + new NotifierAfter(c).send("hi"));
        System.out.println("   => Push added with zero edits to Notifier or Channel");

        System.out.println("\nD. food delivery, from the spec");
        Restaurant r = new Restaurant("Biryani House");
        Order o = new Order(r, List.of(new Item("biryani", 250.0), new Item("coke", 50.0)));
        o.addListener((ord, s) -> System.out.println("        [sms] your order is now " + s));
        System.out.println("   restaurant: " + o.restaurant().name() + ", total: " + o.total());
        System.out.println("   pay by wallet with too little balance:");
        System.out.println("        succeeded? " + o.checkout(new WalletPayment(100.0)));
        System.out.println("   pay by card:");
        System.out.println("        succeeded? " + o.checkout(new CardPayment()));
        System.out.println("   advance through statuses:");
        o.advanceTo(Status.PREPARING);
        o.advanceTo(Status.OUT_FOR_DELIVERY);
        o.advanceTo(Status.DELIVERED);
        System.out.println("   final status: " + o.status());

        System.out.print("   invariant enforced? ");
        try { new Order(r, List.of()); System.out.println("NO"); }
        catch (IllegalArgumentException ex) { System.out.println("yes -> " + ex.getMessage()); }
    }
}
