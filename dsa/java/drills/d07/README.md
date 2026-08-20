# Drill 07 — Exceptions

Python: everything is unchecked. You catch what you remember to catch.
Java: some exceptions are CHECKED — the compiler forces you to either
catch them or declare `throws`. That is why file I/O looks so noisy.

  RuntimeException family (unchecked): your bugs. NPE, IllegalArgument,
      IndexOutOfBounds. Don't catch these — fix them.
  Checked (IOException, etc.): the world failing, not you. Handle them.

Rule of thumb: throw IllegalArgumentException when the CALLER passed
something invalid. Throw IllegalStateException when the OBJECT is in the
wrong state for that call.

    javac Exceptions.java && java Exceptions
