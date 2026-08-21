OOPS -- object oriented programming 

it deals with objects and classes

classes are blueprint of anything while objects are the instances of those classes 
oops has these building blocks, we have 4 major principles that are followed in OOPS those are

Abstraction 
- Hinding the implementation details of the methods from the users are known as abstraction
- these are acheived by using Abstract classes and interface
- abstract classes (IS-A)
- - these are classes which has some methods described , when a subclasses is created out of those abstract classes it is forecd to implement all the methods mentioned in the abastract classes. In this way the subclass methods logic is hidden from the end user and they dont know how that mentod are implemented
- - a class can have only one abstract class while an abastract class can be used to create multiple subclasses

- interface (CAN DO)
- - these are contracts between two classes where they have to implement the methods mentioned in these interfaces , the interfaces can have thier own implementation which the classes implementing them can override
  
ENcapsulation
- Bundling together the methods and attribute and methods in a class is called as encapsulation, here we hide the atrributes from the end users and we make sure that they are modified using the getters and setters , instead of directly exposing them to the endusers
  
inheritance (IS-A)
- This mean creating subclasses from the superclasses where the the subclasses inherits all the behaviours from the superlcasses they can modify the behaviour but they would have to implement those behaviours.

polymorphism 
- THis means the same functionality can vary based on how it is used.
- we have two ways to implement this using
- - methods overloading
- - in this case the methods are called with different parameters and based on the parameters different methods are called which leads to different methods being called
- method overriding 
- - in this case the method is implemented by the superclass and it is also implemented by the sub class, when the subclass invokes the same method the the implementation fo the method in the sub class takes predent and when the super class invokes the same method then the implemntation of the method from the super class thakes precent. Note that in this case the method name as well as the parameter and the return types are same for both the sub calss and the super class