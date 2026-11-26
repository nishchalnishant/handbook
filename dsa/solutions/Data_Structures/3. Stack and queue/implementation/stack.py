class Stack:
    def __init__(self):
        self.stack = []

    def is_empty(self):
        """Check if the stack is empty"""
        return len(self.stack) == 0

    def push(self, data):
        """Push an element onto the stack"""
        self.stack.append(data)

    def pop(self):
        """Remove and return the top element of the stack"""
        if self.is_empty():
            return "Stack is empty"
        return self.stack.pop()

    def peek(self):
        """Return the top element of the stack without removing it"""
        if self.is_empty():
            return "Stack is empty"
        return self.stack[-1]

    def size(self):
        """Return the size of the stack"""
        return len(self.stack)

    def display(self):
        """Display all elements in the stack"""
        return self.stack[::-1]  # Display in LIFO order

# Usage Example
stack = Stack()
stack.push(10)
stack.push(20)
stack.push(30)
print("Stack:", stack.display())  # Output: [30, 20, 10]
print("Top element:", stack.peek())  # Output: 30
print("Popped element:", stack.pop())  # Output: 30
print("Stack after pop:", stack.display())  # Output: [20, 10]
print("Stack size:", stack.size())  # Output: 2