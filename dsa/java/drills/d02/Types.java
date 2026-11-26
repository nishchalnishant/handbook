public class Types {

    // TODO: return the sum of a and b
    static int add(int a, int b) {
        return 0;
    }

    // TODO: return true if n is even
    static boolean isEven(int n) {
        return false;
    }

    // TODO: return the larger of a and b. Do not use Math.max.
    static int max(int a, int b) {
        return 0;
    }

    // TODO: return s repeated n times. "ab", 3 -> "ababab"
    // Hint: build it in a loop with +=, or discover StringBuilder.
    static String repeat(String s, int n) {
        return "";
    }

    // TODO: return the number of vowels in s (aeiou, lowercase only)
    // Hint: s.charAt(i) gives you a char. Compare chars with ==.
    static int countVowels(String s) {
        return 0;
    }

    // ---- test harness: do not edit below ----
    static int passed = 0, failed = 0;

    static void check(String label, Object got, Object want) {
        if (got.equals(want)) {
            System.out.println("PASS  " + label);
            passed++;
        } else {
            System.out.println("FAIL  " + label + "  got=" + got + " want=" + want);
            failed++;
        }
    }

    public static void main(String[] args) {
        check("add(2,3)", add(2, 3), 5);
        check("add(-1,1)", add(-1, 1), 0);
        check("isEven(4)", isEven(4), true);
        check("isEven(7)", isEven(7), false);
        check("max(3,9)", max(3, 9), 9);
        check("max(9,3)", max(9, 3), 9);
        check("repeat(ab,3)", repeat("ab", 3), "ababab");
        check("repeat(x,0)", repeat("x", 0), "");
        check("countVowels(hello)", countVowels("hello"), 2);
        check("countVowels(xyz)", countVowels("xyz"), 0);
        System.out.println("\n" + passed + " passed, " + failed + " failed");
    }
}
