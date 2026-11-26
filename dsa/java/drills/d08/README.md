# Drill 08 — Generics and enums

`<T>` is not scary. It means "I will tell you the type later."
A `Box<String>` is a box the compiler knows holds Strings.

Enums are a fixed set of named values — and in Java they are full objects
that can hold fields and methods. Use them anywhere Python would use a
string constant. The compiler then catches your typos.

    javac Generics.java && java Generics
