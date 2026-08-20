# Drill 04 — Your first real class

Stop writing static methods. This is the shift into object thinking,
and it is the foundation of every LLD interview you will ever sit.

A class answers two questions:
  1. What do I KNOW?  -> fields
  2. What can I DO?   -> methods

Fields are `private`. Always. Outsiders touch them only through methods
you chose to expose. That is encapsulation, and it is not bureaucracy:
it means you can change the inside later without breaking every caller.

    javac BankAccount.java && java BankAccount
