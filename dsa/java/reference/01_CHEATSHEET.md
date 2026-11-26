# Java Cheatsheet — the 90% you actually use

## Run it
    javac Foo.java && java Foo          # compile then run
    java Foo.java                       # single-file: compile+run in one step (JDK 11+)
    javac -d out *.java && java -cp out Main    # multi-file into an out/ dir

## Skeleton
    public class Foo {
        public static void main(String[] args) {
        }
    }
File name MUST match the public class name. Foo.java holds `public class Foo`.

## Types
    int    long    double    boolean    char        // primitives, lowercase
    String  Integer  Double  Boolean                // references, Capitalized
    var x = 5;                  // inferred; still statically typed. Local vars only.
    final int y = 5;            // cannot be reassigned

## Strings
    s.length()          s.charAt(0)        s.substring(1, 4)
    s.equals(t)         s.equalsIgnoreCase(t)     s.contains("x")
    s.split(",")        s.trim()           s.toUpperCase()
    s.isEmpty()         s.isBlank()        String.join(",", list)
    "a %s and %d".formatted(x, n)          String.valueOf(n)
    Integer.parseInt("42")                 // String -> int

Building strings in a loop: use StringBuilder, not `+=`.
    StringBuilder sb = new StringBuilder();
    sb.append("x"); sb.append(1);
    String out = sb.toString();

## Collections
    List<String> list = new ArrayList<>();
    list.add("a");  list.get(0);  list.size();  list.remove(0);
    list.contains("a");  list.isEmpty();  list.set(0, "b");

    Map<String,Integer> map = new HashMap<>();
    map.put("k", 1);  map.get("k");  map.getOrDefault("k", 0);
    map.containsKey("k");  map.remove("k");  map.keySet();  map.values();
    map.merge("k", 1, Integer::sum);        // count things in one line

    Set<String> set = new HashSet<>();
    set.add("a");  set.contains("a");

    Deque<Integer> stack = new ArrayDeque<>();   // push/pop/peek
    Queue<Integer> q = new LinkedList<>();       // offer/poll/peek
    PriorityQueue<Integer> pq = new PriorityQueue<>();   // min-heap by default
    PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());

    List.of(1,2,3)      // IMMUTABLE. .add() throws. Wrap: new ArrayList<>(List.of(..))

## Iterating
    for (String s : list) { }
    for (int i = 0; i < n; i++) { }
    for (Map.Entry<String,Integer> e : map.entrySet()) {
        e.getKey(); e.getValue();
    }
    map.forEach((k, v) -> System.out.println(k + "=" + v));

## Arrays (different from List — fixed size, `.length` not `.size()`)
    int[] a = new int[5];
    int[] b = {1, 2, 3};
    a.length            Arrays.sort(a)     Arrays.toString(a)
    Arrays.fill(a, 0)   Arrays.asList(b)

## Sorting
    Collections.sort(list);
    list.sort(Comparator.comparing(Person::name));
    list.sort(Comparator.comparingInt(Person::age).reversed());
    list.sort(Comparator.comparing(Person::city).thenComparing(Person::name));

## Streams
    xs.stream().filter(x -> x > 3).map(x -> x * 2).toList()
    xs.stream().mapToInt(Integer::intValue).sum()
    xs.stream().anyMatch(x -> x > 3)     .allMatch(..)   .noneMatch(..)
    xs.stream().collect(Collectors.groupingBy(Person::city))
    xs.stream().collect(Collectors.toMap(Person::name, Person::age))
    xs.stream().sorted().distinct().limit(5).toList()
    xs.stream().findFirst().orElse(null)
    IntStream.range(0, n).boxed().toList()

## Classes
    public class Dog extends Animal implements Pet {
        private final String name;
        private static int count = 0;        // shared by ALL instances

        public Dog(String name) {
            super(name);                     // parent constructor first
            this.name = name;
            count++;
        }

        @Override public String speak() { return "woof"; }
        public String getName() { return name; }
    }

    record Point(int x, int y) {}            // immutable data holder, free everything
    interface Pet { String speak(); }        // contract
    abstract class Animal {                  // partial implementation, cannot instantiate
        abstract String speak();
        void breathe() { }                   // shared concrete behavior
    }
    enum Color { RED, GREEN, BLUE }

**interface vs abstract class:** interface = "can do" (a capability; a class
can implement many). abstract class = "is a" (shared state and code; only one
parent allowed). When unsure, pick the interface.

## Exceptions
    try {
        risky();
    } catch (IOException | SQLException e) {
        System.out.println(e.getMessage());
    } finally {
        cleanup();                           // always runs
    }

    try (var reader = Files.newBufferedReader(path)) { }   // auto-closes

    throw new IllegalArgumentException("bad input");
    void f() throws IOException { }           // checked: caller must handle

## Files
    Path p = Path.of("data.txt");
    String all = Files.readString(p);
    List<String> lines = Files.readAllLines(p);
    Files.writeString(p, "content");

## Null-safety
    Objects.requireNonNull(x, "x must not be null");
    Optional<String> o = Optional.ofNullable(maybe);
    o.orElse("default");   o.isPresent();   o.map(String::toUpperCase);

## Gotchas that will cost you an hour each
    "a" == "b"              // compares references. use .equals()
    Integer 128 == 128      // FALSE. cache only covers -128..127
    List.of(..).add(x)      // UnsupportedOperationException; it's immutable
    int / int               // 5/2 == 2. cast: (double) 5 / 2
    0.1 + 0.2 != 0.3        // never use double for money. BigDecimal or long cents
    array.length            // no parens. String.length() HAS parens. size() for List
    modifying a list while for-each looping it   // ConcurrentModificationException
                                                 // use an Iterator, or removeIf()
