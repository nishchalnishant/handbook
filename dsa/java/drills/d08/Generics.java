import java.util.*;

// TODO: make Pair generic in two types, A and B: `class Pair<A, B>`
// fields first/second, a constructor, getters, and a toString of "(a, b)"
class Pair {
}

enum Status {
    ACTIVE("running"),
    PAUSED("on hold"),
    CLOSED("done");

    private final String label;
    Status(String label) { this.label = label; }
    public String label() { return label; }
}

public class Generics {

    // TODO: return the largest element.
    // `<T extends Comparable<T>>` = "any T that knows how to compare itself"
    static <T extends Comparable<T>> T largest(List<T> xs) {
        return null;
    }

    public static void main(String[] args) {
        for (Status s : Status.values()) {
            System.out.println(s + " -> " + s.label() + "  (ordinal " + s.ordinal() + ")");
        }

        Status s = Status.PAUSED;
        switch (s) {                         // switch on enum: exhaustive, typo-proof
            case ACTIVE -> System.out.println("it runs");
            case PAUSED -> System.out.println("it waits");
            case CLOSED -> System.out.println("it ended");
        }

        // Uncomment as you implement:
        // Pair<String, Integer> p = new Pair<>("age", 30);
        // System.out.println(p);
        // System.out.println(p.toString().equals("(age, 30)") ? "PASS pair" : "FAIL pair");
        //
        // System.out.println(largest(List.of(3, 9, 2)) == 9 ? "PASS int" : "FAIL int");
        // System.out.println(largest(List.of("a","z","m")).equals("z") ? "PASS str" : "FAIL str");
    }
}
