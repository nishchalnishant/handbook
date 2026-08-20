import java.util.*;
import java.util.stream.*;

public class Streams {

    record Person(String name, int age, String city) {}
    // `record` = an immutable data class. Java generates the constructor,
    // getters (person.name()), equals, hashCode and toString for you.
    // This is Python's @dataclass. Use it constantly.

    static List<Person> people() {
        return List.of(
            new Person("asha", 30, "pune"),
            new Person("ben", 25, "delhi"),
            new Person("chai", 35, "pune"),
            new Person("dev", 28, "delhi"),
            new Person("eli", 41, "pune")
        );
    }

    // TODO: names of everyone older than 29, sorted alphabetically
    static List<String> namesOver29(List<Person> ps) {
        return List.of();
    }

    // TODO: average age. Hint: mapToInt(...).average().orElse(0)
    static double averageAge(List<Person> ps) {
        return 0;
    }

    // TODO: group people by city -> Map<String, List<Person>>
    // Hint: Collectors.groupingBy(Person::city)
    static Map<String, List<Person>> byCity(List<Person> ps) {
        return Map.of();
    }

    // TODO: count of people per city -> {pune=3, delhi=2}
    // Hint: groupingBy(..., Collectors.counting())  -- gives Long, not Integer
    static Map<String, Long> countByCity(List<Person> ps) {
        return Map.of();
    }

    public static void main(String[] args) {
        List<Person> ps = people();

        // worked example — study this one, then do the TODOs
        List<String> loud = ps.stream()
                              .map(Person::name)
                              .map(String::toUpperCase)
                              .sorted()
                              .toList();
        System.out.println(loud);

        System.out.println(namesOver29(ps).equals(List.of("asha","chai","eli"))
            ? "PASS  over29" : "FAIL  over29  got=" + namesOver29(ps));
        System.out.println(Math.abs(averageAge(ps) - 31.8) < 0.001
            ? "PASS  avg" : "FAIL  avg  got=" + averageAge(ps));
        System.out.println(byCity(ps).get("pune") != null && byCity(ps).get("pune").size() == 3
            ? "PASS  byCity" : "FAIL  byCity");
        System.out.println(countByCity(ps).equals(Map.of("pune",3L,"delhi",2L))
            ? "PASS  countByCity" : "FAIL  countByCity  got=" + countByCity(ps));
    }
}
