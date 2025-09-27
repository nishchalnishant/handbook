# ============================
# 🔹 Question 1: Class & Object
# ============================
# Create a class `Car` with attributes `brand`, `model`, and `year`.
# Create an object of `Car` and print its details.


class Car:
    """Car class"""

    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

# ============================
# 🔹 Question 2: Encapsulation
# ============================
# Create a class `BankAccount` with a private attribute `__balance`.
# Implement `deposit()` and `withdraw()` methods.
# Use a `get_balance()` method to access the private balance.
# Make sure we give account no in an incremental manner


class BankAccount:

    account_no = 0
    """BankAccount class"""

    def __init__(self, account_holder, balance):
        self.account_holder = account_holder
        self.__balance = balance
        BankAccount.account_no += 1

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return f"Deposited {amount}, New Balance: {self.__balance}"
        return "Invalid deposit amount"
    
    
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return f"Withdrew {amount}, Remaining Balance: {self.__balance}"
        return "Insufficient funds"
    
    def get_balance(self):
        return self.__balance
    
    def __str__(self):
        return f"{self.account_holder}'s Account Balance: {self.__balance}"
    


# ============================
# 🔹 Question 3: Abstraction
# ============================
# Create an abstract class `Shape` with an abstract method `area()`.
# Implement `area()` in subclasses `Circle` and `Rectangle`.

from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract class Shape"""

    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    """Circle class"""

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2
    
    def __str__(self):
        return f"Circle with radius {self.radius}"
    
class Rectangle(Shape):
    """Rectangle class"""

    def __init__(self, length, breadth):
        self.length = length
        self.breadth = breadth

    def area(self):
        return self.length * self.breadth
    
    def __str__(self):
        return f"Rectangle with length {self.length} and breadth {self.breadth}"
    



# ============================
# 🔹 Question 4: Single Inheritance (IS-A Relationship)
# ============================
# Create a parent class `Animal` with `make_sound()` method.
# Create a child class `Dog` that overrides `make_sound()` to return "Bark!"

class Animal:
    """Animal class"""

    def __init__(self, name, species):
        self.name = name
        self.species = species

    def make_sound(self):
        return "Sound!"
    
    def __str__(self):
        return f"{self.name} ({self.species})"
    
class Dog(Animal):
    """Dog class"""

    def make_sound(self):
        return "Bark!"
    
    def __str__(self):
        return f"{self.name} ({self.species}) - {self.make_sound()}"
    



# ============================
# 🔹 Question 5: Multiple Inheritance
# ============================
# Create two classes: `Person` (with `get_name()`) and `Employee` (with `get_salary()`).
# Create a `Manager` class that inherits from both and has a `get_details()` method.


class Person:
    """Person class"""

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name
    
    def __str__(self):
        return f"Name: {self.name}"
    
class Employee:
    """Employee class"""

    def __init__(self, salary):
        self.salary = salary

    def get_salary(self):
        return self.salary
    
    def __str__(self):
        return f"Salary: {self.salary}"
    
class Manager(Person, Employee):
    """Manager class"""

    def __init__(self, name, salary):
        Person.__init__(self, name)
        Employee.__init__(self, salary)

    def get_details(self):
        return f"{self.get_name()}, Salary: {self.get_salary()}"
    
    def __str__(self):
        return f"Manager: {self.get_details()}"
    


# ============================
# 🔹 Question 6: Multilevel Inheritance
# ============================
# Implement a class hierarchy: `Vehicle` → `Car` → `ElectricCar`
# The `ElectricCar` should have a `battery_capacity` attribute.

class Vehicle:
    """Vehicle class"""

    def __init__(self, make, model):
        self.make = make
        self.model = model

    def __str__(self):
        return f"{self.make} {self.model}"
    
class Car(Vehicle):
    """Car class"""

    def __init__(self, make, model, fuel_type):
        super().__init__(make, model)
        self.fuel_type = fuel_type

    def __str__(self):
        return f"{super().__str__()} ({self.fuel_type})"
    
class ElectricCar(Car):
    """ElectricCar class"""

    def __init__(self, make, model, battery_capacity):
        super().__init__(make, model, "Electric")
        self.battery_capacity = battery_capacity

    def __str__(self):
        return f"{super().__str__()}, Battery: {self.battery_capacity} kWh"
    


# ============================
# 🔹 Question 7: Polymorphism (Method Overriding)
# ============================
# Create a base class `Bird` with `fly()` method returning "I can fly!"
# Override it in `Penguin` class to return "I can't fly!"

class Bird:
    """Bird class"""

    def fly(self):
        return "I can fly!"
    
    def __str__(self):
        return self.fly()
    
class Penguin(Bird):
    """Penguin class"""

    def fly(self):
        return "I can't fly!"
    
    def __str__(self):
        return self.fly()
    



# ============================
# 🔹 Question 8: Polymorphism (Method Overloading using default arguments)
# ============================
# Create a class `MathOperations` with a method `add()`
# The `add()` method should work for 2 or 3 numbers.

class MathOperations:
    """MathOperations class"""

    def add(self, a, b, c=0):
        return a + b + c
    
    def __str__(self):
        return "MathOperations class"
    


# ============================
# 🔹 Question 9: Composition (HAS-A Relationship)
# ============================
# Create an `Engine` class with `start()` method.
# Create a `Car` class that has an `Engine` object.

class Engine:
    """Engine class"""

    def start(self):
        return "Engine started!"
    
    def __str__(self):
        return "Engine"
    
class Car:
    """Car class"""

    def __init__(self):
        self.engine = Engine()

    def start(self):
        return self.engine.start()
    
    def __str__(self):
        return f"Car with {self.engine}"
    


# ============================
# 🔹 Question 10: Static & Class Methods
# ============================
# Create a class `Utility` with:
# - A static method `greet()` that returns "Hello!"
# - A class method `describe_class()` that returns the class name.

class Utility:
    """Utility class"""

    @staticmethod
    def greet():
        return "Hello!"
    
    @classmethod
    def describe_class(cls):
        return cls.__name__
    
    def __str__(self):
        return "Utility class"
    
    