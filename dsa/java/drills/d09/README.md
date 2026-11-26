# Drill 09 — Streams and lambdas (Java's comprehensions)

    Python: [x*2 for x in xs if x > 3]
    Java:   xs.stream().filter(x -> x > 3).map(x -> x * 2).toList()

Once this clicks, Java stops feeling twice as long as Python.
Three stages: a source, zero or more intermediate ops, one terminal op.

    javac Streams.java && java Streams
