# Drill 10 — Build one thing from an empty file

No stubs. No scaffolding. This is the exam for drills 01-09, and the
moment you find out whether it stuck.

Delete Inventory.java and write it yourself from nothing:

  - `record Item(String sku, String name, double price)`
  - class `Inventory` with a private Map<String, Integer> of sku -> quantity
      add(Item item, int qty)
      remove(String sku, int qty)   -> throw if not enough stock
      totalValue()                  -> sum of price * qty
      lowStock(int threshold)       -> List<Item> below threshold, by name
  - a main that exercises all of it and prints PASS/FAIL

Rules:
  - do not copy from earlier drills; retype from memory
  - compile every 5 lines
  - when stuck longer than 10 minutes, THEN look back

If you can do this unaided, you can write Java. That's the whole bar.
