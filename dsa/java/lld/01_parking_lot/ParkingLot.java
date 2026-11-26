import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.*;

// ---------- what varies #1: a FIXED, known set -> enum ----------
enum VehicleType {
    BIKE(1), CAR(2), TRUCK(4);        // the int is how many spot-units it needs

    private final int size;
    VehicleType(int size) { this.size = size; }
    public int size() { return size; }
}

// ---------- immutable data -> record ----------
record Vehicle(String plate, VehicleType type) {}

class Spot {
    private final String id;
    private final VehicleType fits;
    private Vehicle occupant;         // null = free. The arrow pointing nowhere.

    Spot(String id, VehicleType fits) {
        this.id = id;
        this.fits = fits;
    }

    boolean isFree() { return occupant == null; }
    boolean canFit(VehicleType t) { return isFree() && fits.size() >= t.size(); }

    void occupy(Vehicle v) {
        if (!isFree()) throw new IllegalStateException("spot " + id + " taken");
        this.occupant = v;
    }

    void release() { this.occupant = null; }
    String id() { return id; }
}

record Ticket(String id, Vehicle vehicle, Spot spot, LocalDateTime entryTime) {}

// ---------- what varies #2: OPEN-ENDED behavior -> interface ----------
interface FeeStrategy {
    double calculate(Ticket ticket, LocalDateTime exit);
}

class HourlyFee implements FeeStrategy {
    private final Map<VehicleType, Double> ratePerHour;

    HourlyFee(Map<VehicleType, Double> ratePerHour) {
        this.ratePerHour = ratePerHour;
    }

    @Override
    public double calculate(Ticket t, LocalDateTime exit) {
        long hours = Math.max(1, ChronoUnit.HOURS.between(t.entryTime(), exit));
        return hours * ratePerHour.getOrDefault(t.vehicle().type(), 10.0);
    }
}

class FlatFee implements FeeStrategy {
    private final double amount;
    FlatFee(double amount) { this.amount = amount; }

    @Override
    public double calculate(Ticket t, LocalDateTime exit) { return amount; }
}

// ---------- the coordinator ----------
class Lot {
    private final List<Spot> spots;
    private final Map<String, Ticket> active = new HashMap<>();
    private final FeeStrategy feeStrategy;   // injected, not constructed here.
                                             // THAT is dependency inversion.

    Lot(List<Spot> spots, FeeStrategy feeStrategy) {
        this.spots = spots;
        this.feeStrategy = feeStrategy;
    }

    boolean hasSpace(VehicleType type) {
        return spots.stream().anyMatch(s -> s.canFit(type));
    }

    Ticket park(Vehicle v) {
        Spot spot = spots.stream()
                         .filter(s -> s.canFit(v.type()))
                         .findFirst()
                         .orElseThrow(() -> new IllegalStateException("lot full for " + v.type()));
        spot.occupy(v);
        Ticket t = new Ticket(UUID.randomUUID().toString().substring(0, 8),
                              v, spot, LocalDateTime.now());
        active.put(t.id(), t);
        return t;
    }

    double unpark(String ticketId, LocalDateTime exit) {
        Ticket t = active.remove(ticketId);
        if (t == null) throw new IllegalArgumentException("unknown ticket " + ticketId);
        t.spot().release();
        return feeStrategy.calculate(t, exit);
    }
}

public class ParkingLot {
    public static void main(String[] args) {
        List<Spot> spots = List.of(
            new Spot("B1", VehicleType.BIKE),
            new Spot("C1", VehicleType.CAR),
            new Spot("C2", VehicleType.CAR),
            new Spot("T1", VehicleType.TRUCK)
        );

        FeeStrategy hourly = new HourlyFee(Map.of(
            VehicleType.BIKE, 10.0,
            VehicleType.CAR,  20.0,
            VehicleType.TRUCK, 50.0
        ));

        Lot lot = new Lot(new ArrayList<>(spots), hourly);

        Vehicle car = new Vehicle("MH12AB1234", VehicleType.CAR);
        Ticket t = lot.park(car);
        System.out.println("parked " + car.plate() + " at " + t.spot().id());

        double fee = lot.unpark(t.id(), t.entryTime().plusHours(3));
        System.out.println("3 hours -> " + fee);
        System.out.println(fee == 60.0 ? "PASS  hourly fee" : "FAIL  hourly fee");

        // Swapping the ENTIRE pricing model: one line. No edits to Lot.
        Lot flatLot = new Lot(new ArrayList<>(spots), new FlatFee(99));
        Ticket t2 = flatLot.park(new Vehicle("KA01XY", VehicleType.BIKE));
        double flat = flatLot.unpark(t2.id(), t2.entryTime().plusHours(9));
        System.out.println("flat -> " + flat);
        System.out.println(flat == 99.0 ? "PASS  flat fee" : "FAIL  flat fee");

        // fill the truck spot, then confirm the lot reports itself full
        Lot small = new Lot(new ArrayList<>(List.of(new Spot("T1", VehicleType.TRUCK))), hourly);
        small.park(new Vehicle("T-1", VehicleType.TRUCK));
        System.out.println(!small.hasSpace(VehicleType.TRUCK)
            ? "PASS  full detection" : "FAIL  full detection");

        try {
            small.park(new Vehicle("T-2", VehicleType.TRUCK));
            System.out.println("FAIL  should have refused");
        } catch (IllegalStateException e) {
            System.out.println("PASS  refused when full: " + e.getMessage());
        }
    }
}
