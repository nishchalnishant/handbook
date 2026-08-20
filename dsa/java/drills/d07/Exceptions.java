import java.util.*;

// TODO: make this a proper checked exception by extending Exception.
// Give it a constructor taking a message that calls super(message).
class InsufficientFundsException {
}

class Vault {
    private double balance = 100;

    // TODO: declare `throws InsufficientFundsException` and throw it
    // when amount > balance. Otherwise subtract.
    void withdraw(double amount) {
    }

    double balance() { return balance; }
}

public class Exceptions {

    // TODO: parse s to an int. If it is not a number, return fallback.
    // Hint: Integer.parseInt throws NumberFormatException (unchecked).
    static int parseOr(String s, int fallback) {
        return 0;
    }

    public static void main(String[] args) {
        System.out.println(parseOr("42", -1) == 42 ? "PASS  parse ok" : "FAIL  parse ok");
        System.out.println(parseOr("abc", -1) == -1 ? "PASS  parse bad" : "FAIL  parse bad");
        System.out.println(parseOr(null, -1) == -1 ? "PASS  parse null" : "FAIL  parse null");

        Vault v = new Vault();
        // Once InsufficientFundsException is checked, this WON'T COMPILE
        // until you wrap it in try/catch. That is the compiler doing its job.
        //
        // try {
        //     v.withdraw(500);
        //     System.out.println("FAIL  should have thrown");
        // } catch (InsufficientFundsException e) {
        //     System.out.println("PASS  caught: " + e.getMessage());
        // } finally {
        //     System.out.println("finally always runs. balance=" + v.balance());
        // }
    }
}
