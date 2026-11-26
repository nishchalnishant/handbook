package practice;

/*
public	Anywhere in the application
private	Only inside the same class
protected	The same package and child classes
*/

public class User {
    String name;
    String email;

    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }

    void login() {
        System.out.println("User has logged in");
    }
}

enum InnerUser {
    first_user, seconduser, thirduser    
}

// Example usage
class Main {
    public static void main(String[] args) {
        User user1 = new User("abc", "abc@gmail.com");
        user1.login();
    }
}