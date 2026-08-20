import java.util.*;

interface Shape {
    double area();      // no body. implementors MUST provide one.
    String name();
}

// TODO: make Circle implement Shape.
// field: radius. area = Math.PI * r * r. name = "circle"
class Circle {
}

// TODO: make Rectangle implement Shape.
// fields: width, height. area = w*h. name = "rectangle"
class Rectangle {
}

// TODO: make Square REUSE Rectangle via `extends Rectangle`.
// A square is a rectangle with equal sides. Call super(side, side).
// name = "square"  <- override it
class Square {
}

public class Shapes {

    // Note: this method never mentions Circle, Rectangle, or Square.
    // It works for shapes that do not exist yet. THAT is the payoff.
    static double totalArea(List<Shape> shapes) {
        double sum = 0;
        for (Shape s : shapes) sum += s.area();
        return sum;
    }

    public static void main(String[] args) {
        // Uncomment once your classes compile:
        //
        // List<Shape> shapes = List.of(
        //     new Circle(1),
        //     new Rectangle(2, 3),
        //     new Square(4)
        // );
        //
        // for (Shape s : shapes) {
        //     System.out.printf("%-10s %.2f%n", s.name(), s.area());
        // }
        //
        // double t = totalArea(shapes);
        // System.out.printf("total %.2f%n", t);
        // System.out.println(Math.abs(t - 25.14159) < 0.001 ? "PASS" : "FAIL");

        System.out.println("Implement the three classes, then uncomment main.");
    }
}
