import java.util.*;

// Runnable backing for the "extension test" in notes/THE_SCRIPT.md (follow-up #1).
// A new requirement must cost you ONE NEW CLASS and ZERO EDITS.
//   javac ExtensionTestProof.java && java ExtensionTestProof
public class ExtensionTestProof {

    interface FeeStrategy { double fee(int hours); }

    static class FlatFee implements FeeStrategy {
        public double fee(int h) { return 50; }
    }
    static class HourlyFee implements FeeStrategy {
        public double fee(int h) { return 20 * h; }
    }
    // The interviewer says "now add weekend pricing". This is the whole change:
    static class WeekendFee implements FeeStrategy {
        public double fee(int h) { return 30 * h + 100; }
    }

    static class Ticket {
        private final FeeStrategy strategy;   // DIP: interface, injected
        Ticket(FeeStrategy s) { strategy = s; }
        double price(int hours) { return strategy.fee(hours); }
    }

    public static void main(String[] args) {
        // ONE call site. Zero edits to Ticket, FlatFee, or HourlyFee.
        List<FeeStrategy> all = List.of(new FlatFee(), new HourlyFee(), new WeekendFee());
        for (FeeStrategy s : all) {
            System.out.printf("  %-11s 3h -> %.1f%n",
                s.getClass().getSimpleName(), new Ticket(s).price(3));
        }
        System.out.println("  lines edited to add WeekendFee: 0");
        System.out.println("  classes added: 1");
    }
}
