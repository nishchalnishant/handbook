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


NOW that we are sure of what we have on the OOPS concept lets mode to OOPS principles 
- SOLID
- - Single responsibility principle
  - A calss should be reponsible for a singe task , if there are multiple reponsibility within a class we shoudl create a new class and move that extra reponsibiltiy to that calss
- - Open close principle
  - A class should be open for extension but closed for modifiction, we should be having interface which extends the functionality of the classes intead of modifying the existing implementation as it might break the existing structure of the code.
- - Liskov substition principle 
  - It means the 
- - Interface segrigation principle
  - two objects must be segregated by the interface , the subclasses 
- - Dependency inversion principle 
  - 
- KISS
- - Keep it simple stupid, instead of creating so many interfaces and abstract classes we should keep the logic simple and concise so that the things are streamlined and things works as per the need and usage instead of overcomplicating things
- YAGNI
- - You are not gonna need it. this talks about implmenting anything which is not the need of an hour and assuing we might need that in future and implementing that or adjusting our code accoring to something which not required as of now. we should not do it instead we should make our code so flexible so that we can extend it based on the needs of the future
- DRY - Dont repeat your self
- - this talks about in oops paradigm we should avoid repeating our code and make sure that the code is reused instead of rewritten

how the relationship works between the classes and how closly binded they are

Association - USES-A
Aggregation - HAS-A (Weak)
composition - HAS-A (Strong)
Inheritnce  - IS-A
Abstraction - IS-A
Realization   - CAN-DO

How are these implemented 

association 
- it can be implemented in code using  
aggregation 
- it can be implmented using an interface
composition 
- using an interface
inheritance 
- it can be implementing using a superclass and a subclass or using a abstrsact class
realization 
- using an interface 


Design patterns --

Creation -- deals with object creation 
- singleton - makes sure there is only one instance of a class available
- factory - gives the responsibility of creating the concerete objects to the subclasses
- abstract factory
- builder - builds a complex objet step by step
- prototye - duplicates an existing object to save time and space for repeatable objects

behavioural - deals with the behaviour of the object
- Observer - 
- strategy
- command
- state
- visitor
- mediatior
- iterator
- chain or reponsibility 
- template

structural - deals with the structure of the object 
- Adapter
- bridge
- composite
- decorator
- flywheel
- facade
- proxy