# Decoding Java errors

Java error messages are long but formulaic. Learn the six you'll actually
hit and the fear goes away.

## Compile errors (javac refuses; nothing ran)

**`cannot find symbol`**
You used a name Java doesn't know. Causes, in order of likelihood:
typo; missing `import`; variable declared inside a different `{}` block;
method doesn't exist on that type. The line below the message points with
a `^` at the exact symbol.

**`incompatible types: String cannot be converted to int`**
You put the wrong shape in the box. Either change the declared type or
convert the value (`Integer.parseInt`, `String.valueOf`).

**`class X is public, should be declared in a file named X.java`**
Filename must match the public class name. Exactly, including case.

**`missing return statement`**
Some path through your method returns nothing. Usually an `if` without
an `else`, or a loop the compiler can't prove executes.

**`unreported exception IOException; must be caught or declared to be thrown`**
A checked exception. Wrap in try/catch, or add `throws IOException` to your
method signature and let the caller deal with it.

**`non-static method cannot be referenced from a static context`**
You called an instance method from `main` (which is static) without an
object. You need `new Thing().method()`, not `Thing.method()`.
This one confuses every Python developer exactly once.

## Runtime errors (it compiled; it died while running)

**`NullPointerException`**
An arrow pointed nowhere. Modern Java tells you precisely which one —
read the "because ... is null" clause; it names the variable.

**`ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 5`**
Valid indices are 0..length-1. An off-by-one, nearly always in a loop condition.

**`ConcurrentModificationException`**
You added or removed from a collection while for-each looping over it.
Use `list.removeIf(pred)`, or an explicit `Iterator` with `it.remove()`.

**`NumberFormatException`**
`Integer.parseInt` got something that isn't a number. Check for null and
empty string first.

**`ClassCastException`**
You cast an object to a type it isn't. Guard with `instanceof` first.

## Reading a stack trace

    Exception in thread "main" java.lang.NullPointerException
        at Foo.helper(Foo.java:42)      <- WHERE IT BROKE. start here.
        at Foo.process(Foo.java:20)     <- who called that
        at Foo.main(Foo.java:8)         <- who called that

Top frame = where it blew up. Read downward to see how you got there.
Ignore frames from java.* packages; your bug is in YOUR files.
