# ========================================================
# ✅ 1. CLASS & OBJECT
# ========================================================
# A class is a blueprint for creating objects.
# An object is an instance of a class with its own attributes and methods.
# Example: An Animal class with name and species attributes.
class Animal:
    """A base class to represent an Animal"""

    def __init__(self, name, species):
        self.name = name  # Public Attribute
        self.species = species  # Public Attribute

    def make_sound(self):
        """A general method to make a sound"""
        return "Some generic sound"

    def __str__(self):
        """Magic Method to return a string representation"""
        return f"{self.name} is a {self.species}"

# ========================================================
# ✅ 2. ENCAPSULATION (DATA HIDING)
# ========================================================
# Encapsulation restricts direct access to some data,
# allowing controlled access through methods (getters/setters).
# Example: A BankAccount class where balance is private.
class BankAccount:
    """A class demonstrating Encapsulation"""

    def __init__(self, account_holder, balance):
        self.account_holder = account_holder  # Public attribute
        self.__balance = balance  # Private attribute (Encapsulation)

    def deposit(self, amount):
        """Public method to deposit money"""
        if amount > 0:
            self.__balance += amount
            return f"Deposited {amount}, New Balance: {self.__balance}"
        return "Invalid deposit amount"

    def withdraw(self, amount):
        """Public method to withdraw money"""
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return f"Withdrew {amount}, Remaining Balance: {self.__balance}"
        return "Insufficient funds"

    def get_balance(self):
        """Getter method to access private attribute"""
        return self.__balance

# ========================================================
# ✅ 3. ABSTRACTION (HIDING IMPLEMENTATION DETAILS)
# ========================================================
# Abstraction hides complex details and exposes only necessary functionality.
# Abstract classes cannot be instantiated and force subclasses to implement required methods.
from abc import ABC, abstractmethod

class Vehicle(ABC):
    """Abstract class forcing subclasses to implement methods"""

    @abstractmethod
    def start_engine(self):
        pass
    
    @abstractmethod
    def stop_engine(self):
        pass

class Car(Vehicle):
    """Concrete class implementing abstract methods"""

    def start_engine(self):
        return "Car engine started"

    def stop_engine(self):
        return "Car engine stopped"

# ========================================================
# ✅ 4. INHERITANCE (IS-A RELATIONSHIP)
# ========================================================
# Inheritance allows a class (child) to acquire properties and behaviors of another class (parent).
# This promotes code reuse. Example: Dog IS-A Animal.
class Dog(Animal):
    """Dog IS-A Animal (Inheritance)"""

    def __init__(self, name, breed):
        super().__init__(name, "Dog")  # Calling parent class constructor
        self.breed = breed  # Additional attribute

    def make_sound(self):
        """Method Overriding (Polymorphism)"""
        return "Bark!"

# ========================================================
# ✅ 5. MULTIPLE INHERITANCE
# ========================================================
# A class can inherit from multiple base classes.
# Example: Bird IS-A Animal and also CAN Fly.
class Flying:
    """A class to add flying capability"""

    def fly(self):
        return "I can fly!"

class Bird(Animal, Flying):
    """Bird IS-A Animal and it also CAN Fly"""

    def __init__(self, name, species):
        super().__init__(name, species)

    def make_sound(self):
        return "Chirp!"

# ========================================================
# ✅ 6. MULTILEVEL INHERITANCE
# ========================================================
# A class is derived from another derived class.
# Example: Puppy → Dog → Animal
class Puppy(Dog):
    """Puppy IS-A Dog, which IS-A Animal"""

    def __init__(self, name, breed, age):
        super().__init__(name, breed)
        self.age = age

    def is_cute(self):
        return f"{self.name} is a cute {self.age}-month-old puppy!"

# ========================================================
# ✅ 7. POLYMORPHISM (METHOD OVERRIDING & OVERLOADING)
# ========================================================
# Polymorphism allows different classes to have the same method name but different behaviors.
# Example: make_sound() is overridden in Dog, Cat, and Lion.
class Cat(Animal):
    """Cat IS-A Animal"""

    def make_sound(self):
        return "Meow!"

class Lion(Animal):
    """Lion IS-A Animal"""

    def make_sound(self):
        return "Roar!"

# Polymorphism in action
def animal_sound(animal):
    """Function to demonstrate polymorphism"""
    return animal.make_sound()

# ========================================================
# ✅ 8. COMPOSITION (HAS-A RELATIONSHIP)
# ========================================================
# Instead of inheritance, we can use composition where a class contains another class as an attribute.
# Example: A Car HAS-A Engine.
class Engine:
    """Engine class"""

    def start(self):
        return "Engine started"

    def stop(self):
        return "Engine stopped"

class CarWithEngine:
    """Car HAS-A Engine (Composition)"""

    def __init__(self, model):
        self.model = model
        self.engine = Engine()  # Composition

    def start_car(self):
        return f"{self.model}: {self.engine.start()}"

    def stop_car(self):
        return f"{self.model}: {self.engine.stop()}"

# ========================================================
# ✅ 9. STATIC & CLASS METHODS
# ========================================================
# Static methods don't use instance attributes and can be called without an instance.
# Class methods operate on the class itself rather than on an instance.
class Utility:
    """A class with static and class methods"""

    @staticmethod
    def greet():
        return "Hello, welcome to OOP in Python!"
    
    @classmethod
    def describe_class(cls):
        return f"This is {cls.__name__} class."

# ========================================================
# ✅ 10. DEMONSTRATION OF ALL CONCEPTS
# ========================================================
if __name__ == "__main__":
    # Objects
    dog = Dog("Buddy", "Golden Retriever")
    cat = Cat("Whiskers")
    lion = Lion("Simba")

    # Polymorphism
    print(animal_sound(dog))  # Bark!
    print(animal_sound(cat))  # Meow!
    print(animal_sound(lion))  # Roar!

    # Encapsulation
    account = BankAccount("Alice", 1000)
    print(account.deposit(500))
    print(account.withdraw(300))
    print(f"Balance: {account.get_balance()}")

    # Abstraction
    car = Car()
    print(car.start_engine())
    print(car.stop_engine())

    # Composition
    my_car = CarWithEngine("Tesla Model X")
    print(my_car.start_car())
    print(my_car.stop_car())

    # Static and Class Methods
    print(Utility.greet())  
    print(Utility.describe_class())  

    # Multilevel Inheritance
    puppy = Puppy("Max", "Labrador", 3)
    print(puppy.is_cute())
