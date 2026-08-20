public class Hello {

    // static = belongs to the class, callable without making a Hello object
    static void sayHi(String name) {
        System.out.println("hi " + name);
    }

    public static void main(String[] args) {
        sayHi("nishchal");

        int x = 5;              // primitive: the box holds 5 itself
        String s = "five";      // reference: the box holds an arrow to "five"

        System.out.println(x + " and " + s);

        // string + anything = string. Java quietly converts. Predict this:
        System.out.println(1 + 2 + "3");     // ?
        System.out.println("1" + 2 + 3);     // ?
        // Write your prediction down BEFORE you run it.
    }
}
