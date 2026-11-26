import java.util.*;

class Point {
    int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }

    // TODO (part 2): implement equals and hashCode so two Points with the
    // same x,y are treated as equal. Rule: if a.equals(b) then their
    // hashCodes MUST match, or HashMap/HashSet quietly misbehave.
    //
    // @Override public boolean equals(Object o) {
    //     if (this == o) return true;
    //     if (!(o instanceof Point)) return false;
    //     Point p = (Point) o;
    //     return x == p.x && y == p.y;
    // }
    // @Override public int hashCode() { return Objects.hash(x, y); }
}

public class Equality {
    public static void main(String[] args) {
        // --- part 1: predict each line, then run ---
        String a = "hello";
        String b = "hello";
        String c = new String("hello");

        System.out.println(a == b);        // predict:
        System.out.println(a == c);        // predict:
        System.out.println(a.equals(c));   // predict:

        Integer i = 127, j = 127;
        Integer m = 128, n = 128;
        System.out.println(i == j);        // predict:
        System.out.println(m == n);        // predict: (this one is infamous)

        // --- part 2: uncomment equals/hashCode above, rerun, watch these flip ---
        Point p1 = new Point(1, 2);
        Point p2 = new Point(1, 2);
        System.out.println(p1.equals(p2));           // predict:

        Set<Point> set = new HashSet<>();
        set.add(p1);
        System.out.println(set.contains(p2));        // predict:

        // --- part 3: the NPE ---
        Map<String, Integer> scores = new HashMap<>();
        Integer score = scores.get("missing");       // no key -> null
        System.out.println(score);                   // predict:
        // System.out.println(score + 1);            // uncomment: what happens & WHY?
        // Fix it two ways: an if-check, and scores.getOrDefault("missing", 0)
    }
}
