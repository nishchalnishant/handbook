# Drill 05 — Interfaces: the idea that unlocks LLD

An interface is a CONTRACT: "anything claiming to be a Shape must be able
to give me an area and a name." It says nothing about how.

In Python you lean on duck typing — if it has .area() it works, and you
find out at runtime when it doesn't. Java makes the duck sign a contract
first, and the compiler checks the signature before the program runs.

Why this matters for design: code written against an INTERFACE keeps
working when you add new implementations. `totalArea(List<Shape>)` below
never changes, no matter how many shapes you invent. That is the entire
point of every design pattern you will meet later.

    javac Shapes.java && java Shapes
