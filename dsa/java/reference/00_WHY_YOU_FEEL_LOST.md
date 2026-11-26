# Why Java Feels Impossible When Python Doesn't

You are not bad at Java. You are missing exactly four mental models that
Python let you skip. Once you have them, Java becomes ordinary.

---

## Model 1: The compiler runs before your program does

Python:  you write code -> you run it -> it breaks at line 40 while running.
Java:    you write code -> `javac` reads ALL of it -> it refuses to build.

This is the single biggest shock. In Python your feedback comes from
*running*. In Java most of your feedback comes from *compiling*, before
anything has run at all.

Consequence: a Java error message is usually not a bug report. It's the
compiler telling you your mental model of the types is wrong. Read it as
information, not as failure. `javac` is a tutor that answers instantly.

**Practice habit:** compile after every 5 lines. Not every 50. You want the
error while you still remember what you were thinking.

---

## Model 2: Every value has a declared type, and the type is a promise

Python:
    x = 5
    x = "hello"     # fine, x is just a name pointing at things

Java:
    int x = 5;
    x = "hello";    // ERROR. x is a box that only holds ints. Forever.

In Python a variable is a *label*. In Java a variable is a *typed box*.

This is why Java feels verbose: you must declare the shape of the box
before you put anything in it. But that declaration is what lets the
compiler catch your mistakes before runtime — that's the trade.

Two families of types:

  primitives:  int, long, double, boolean, char
               hold the value directly. lowercase. no methods.
  references:  String, List, ArrayList, your own classes
               hold an ARROW to an object living elsewhere. Capitalized.

`int x = 5` -> the box contains 5.
`String s = "hi"` -> the box contains an arrow pointing to "hi".

Everything confusing about Java later (null, ==, passing to methods)
comes from this one distinction. Learn it now and you skip months of pain.

---

## Model 3: null is the arrow that points nowhere

A reference variable can hold an arrow to nothing:

    String s = null;
    s.length();     // NullPointerException at RUNTIME

Python has None, but Python code rarely explodes on it because Python
checks so much at runtime anyway. In Java, NPE is THE most common runtime
crash. When you see it, the question is always the same:

    "Which arrow was pointing nowhere, and who forgot to set it?"

---

## Model 4: Code lives inside classes. There is no loose code.

Python lets you write a statement in a file and run it. Java does not.
Every line of executable code sits inside a method, inside a class.

    public class Hello {                 // the file MUST be Hello.java
        public static void main(String[] args) {
            System.out.println("hi");
        }
    }

Decoding `public static void main(String[] args)` — memorize it once:

    public       anyone can call it
    static       belongs to the CLASS, not to an object of the class
    void         returns nothing
    main         the name the JVM looks for to start your program
    String[] args  command-line arguments, as an array of strings

That line is not deep. It is a magic incantation. Type it 50 times this
week and it stops being noise.

---

## The translation table you actually need

| Python                  | Java                                      |
|-------------------------|-------------------------------------------|
| `x = 5`                 | `int x = 5;`                              |
| `s = "hi"`              | `String s = "hi";`                        |
| `xs = []`               | `List<String> xs = new ArrayList<>();`    |
| `xs.append(v)`          | `xs.add(v);`                              |
| `len(xs)`               | `xs.size()`   (`.length` on arrays, `.length()` on String) |
| `d = {}`                | `Map<String,Integer> d = new HashMap<>();`|
| `d[k] = v`              | `d.put(k, v);`                            |
| `d[k]`                  | `d.get(k)`                                |
| `k in d`                | `d.containsKey(k)`                        |
| `for x in xs:`          | `for (String x : xs) {`                   |
| `for i in range(n):`    | `for (int i = 0; i < n; i++) {`           |
| `def f(a, b):`          | `int f(int a, int b) {`                   |
| `None`                  | `null`                                    |
| `print(x)`              | `System.out.println(x);`                  |
| `a == b` (strings)      | `a.equals(b)`  <-- NOT `==`               |
| `class A:`              | `public class A {`                        |
| `def __init__(self):`   | `public A() {`                            |
| `self.x`                | `this.x`                                  |

## The one that will bite you first

    String a = "hello";
    String b = "hello";
    a == b          // compares ARROWS. unreliable. sometimes true by accident.
    a.equals(b)     // compares CONTENTS. this is what you meant.

For objects, `==` asks "same object?" and `.equals()` asks "same value?".
Python's `==` calls `__eq__` for you. Java makes you say it out loud.

Rule: for `int`/`char`/`boolean` use `==`. For everything else use `.equals()`.
