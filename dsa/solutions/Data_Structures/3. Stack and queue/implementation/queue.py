class Queue:
    def __init__(self):
        self.queue = []

    def is_empty(self):
        """Check if the queue is empty"""
        return len(self.queue) == 0

    def enqueue(self, data):
        """Add an element to the end of the queue"""
        self.queue.append(data)

    def dequeue(self):
        """Remove and return the front element of the queue"""
        if self.is_empty():
            return "Queue is empty"
        return self.queue.pop(0)

    def front(self):
        """Return the front element of the queue without removing it"""
        if self.is_empty():
            return "Queue is empty"
        return self.queue[0]

    def rear(self):
        """Return the last element of the queue without removing it"""
        if self.is_empty():
            return "Queue is empty"
        return self.queue[-1]

    def size(self):
        """Return the size of the queue"""
        return len(self.queue)

    def display(self):
        """Display all elements in the queue"""
        return self.queue  # Display in FIFO order

# Usage Example
queue = Queue()
queue.enqueue(10)
queue.enqueue(20)
queue.enqueue(30)
print("Queue:", queue.display())  # Output: [10, 20, 30]
print("Front element:", queue.front())  # Output: 10
print("Rear element:", queue.rear())  # Output: 30
print("Dequeued element:", queue.dequeue())  # Output: 10
print("Queue after dequeue:", queue.display())  # Output: [20, 30]
print("Queue size:", queue.size())  # Output: 2