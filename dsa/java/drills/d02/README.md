# Drill 01 — Compile, run, and read an error on purpose

Goal: make `javac` your friend instead of your enemy in 15 minutes.

## Step 1
    javac Hello.java
    java Hello

## Step 2 — break it deliberately, five times
After each break: compile, READ the message, write the message down in
notes/error_log.md in your own words, then fix it.

  1. delete a semicolon
  2. change `String[] args` to `String args`
  3. rename the class to `Goodbye` but keep the file `Hello.java`
  4. write `int x = "hello";`
  5. call `sayHi()` before it is defined  (surprise: this one WORKS. why?)

Point of this drill: after today, a red error message should raise your
pulse zero. It is the fastest tutor you will ever have.
