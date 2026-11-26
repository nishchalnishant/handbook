import java.util.*;

public class Collections1 {

    // TODO: return a List containing the numbers 1..n
    static List<Integer> range(int n) {
        return new ArrayList<>();
    }

    // TODO: return only the even numbers from xs, in order
    static List<Integer> evens(List<Integer> xs) {
        return new ArrayList<>();
    }

    // TODO: count how many times each word appears.
    //   ["a","b","a"] -> {a=2, b=1}
    // Hint: map.getOrDefault(key, 0) is your friend.
    static Map<String, Integer> wordCount(List<String> words) {
        return new HashMap<>();
    }

    // TODO: return the key with the highest count. Ties: any is fine.
    // Hint: for (Map.Entry<String,Integer> e : m.entrySet())
    static String mostCommon(Map<String, Integer> m) {
        return null;
    }

    // TODO: return xs reversed, as a NEW list (leave xs untouched)
    static List<Integer> reversed(List<Integer> xs) {
        return new ArrayList<>();
    }

    // ---- harness ----
    static int passed = 0, failed = 0;
    static void check(String label, Object got, Object want) {
        boolean ok = (got == null) ? want == null : got.equals(want);
        System.out.println((ok ? "PASS  " : "FAIL  ") + label
            + (ok ? "" : "  got=" + got + " want=" + want));
        if (ok) passed++; else failed++;
    }

    public static void main(String[] args) {
        check("range(5)", range(5), List.of(1,2,3,4,5));
        check("range(0)", range(0), List.of());
        check("evens", evens(List.of(1,2,3,4,5,6)), List.of(2,4,6));

        Map<String,Integer> want = new HashMap<>();
        want.put("a",2); want.put("b",1);
        check("wordCount", wordCount(List.of("a","b","a")), want);

        Map<String,Integer> m = new HashMap<>();
        m.put("x",1); m.put("y",9); m.put("z",3);
        check("mostCommon", mostCommon(m), "y");

        List<Integer> orig = new ArrayList<>(List.of(1,2,3));
        check("reversed", reversed(orig), List.of(3,2,1));
        check("original untouched", orig, List.of(1,2,3));

        System.out.println("\n" + passed + " passed, " + failed + " failed");
    }
}
