public class BankAccount {

    // what it KNOWS. private = nobody outside can reach in and scribble on these.
    private final String owner;   // final = set once in the constructor, never again
    private double balance;

    // the constructor: same name as the class, no return type
    public BankAccount(String owner, double initialBalance) {
        this.owner = owner;              // `this.owner` = the field
        this.balance = initialBalance;   // `owner` alone = the parameter
    }

    // TODO: add amount to balance.
    // If amount <= 0, throw new IllegalArgumentException("deposit must be positive")
    public void deposit(double amount) {
    }

    // TODO: subtract amount. Throw IllegalArgumentException if amount <= 0
    // or if amount > balance ("insufficient funds").
    public void withdraw(double amount) {
    }

    // TODO: return the balance
    public double getBalance() {
        return 0;
    }

    // TODO: return e.g. "nishchal: 250.0"
    // @Override tells the compiler "I mean to replace the inherited version".
    // If you typo the name, it errors instead of silently doing nothing.
    @Override
    public String toString() {
        return "";
    }

    // ---- harness ----
    public static void main(String[] args) {
        BankAccount a = new BankAccount("nishchal", 100);

        a.deposit(150);
        System.out.println(a.getBalance() == 250.0 ? "PASS  deposit" : "FAIL  deposit");

        a.withdraw(50);
        System.out.println(a.getBalance() == 200.0 ? "PASS  withdraw" : "FAIL  withdraw");

        System.out.println(a.toString().equals("nishchal: 200.0")
            ? "PASS  toString" : "FAIL  toString  got=" + a);

        try {
            a.withdraw(999999);
            System.out.println("FAIL  overdraft was allowed");
        } catch (IllegalArgumentException e) {
            System.out.println("PASS  overdraft blocked: " + e.getMessage());
        }

        try {
            a.deposit(-5);
            System.out.println("FAIL  negative deposit was allowed");
        } catch (IllegalArgumentException e) {
            System.out.println("PASS  negative deposit blocked");
        }
    }
}
