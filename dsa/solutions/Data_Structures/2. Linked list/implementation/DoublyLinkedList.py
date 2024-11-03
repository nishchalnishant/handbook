class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        """Add a node at the end of the list"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
        new_node.prev = last

    def prepend(self, data):
        """Add a node at the beginning of the list"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node

    def delete(self, key):
        """Delete the first node with the given key"""
        temp = self.head
        if temp is not None and temp.data == key:
            self.head = temp.next
            if self.head:
                self.head.prev = None
            return
        while temp is not None:
            if temp.data == key:
                if temp.next:
                    temp.next.prev = temp.prev
                if temp.prev:
                    temp.prev.next = temp.next
                return
            temp = temp.next

    def delete_at_position(self, position):
        """Delete a node at a specific position"""
        if self.head is None or position < 0:
            return
        temp = self.head
        for _ in range(position):
            temp = temp.next
            if temp is None:
                return
        if temp.prev:
            temp.prev.next = temp.next
        if temp.next:
            temp.next.prev = temp.prev
        if temp == self.head:  # If head is to be deleted
            self.head = temp.next

    def display_forward(self):
        """Display the list in a forward direction"""
        elements = []
        temp = self.head
        while temp:
            elements.append(temp.data)
            temp = temp.next
        return elements

    def display_backward(self):
        """Display the list in a backward direction"""
        elements = []
        temp = self.head
        while temp and temp.next:
            temp = temp.next
        while temp:
            elements.append(temp.data)
            temp = temp.prev
        return elements

    def insert_after(self, prev_node_data, data):
        """Insert a node after a given node data"""
        temp = self.head
        while temp:
            if temp.data == prev_node_data:
                new_node = Node(data)
                new_node.next = temp.next
                temp.next = new_node
                new_node.prev = temp
                if new_node.next:
                    new_node.next.prev = new_node
                return
            temp = temp.next

    def insert_before(self, next_node_data, data):
        """Insert a node before a given node data"""
        temp = self.head
        while temp:
            if temp.data == next_node_data:
                new_node = Node(data)
                new_node.next = temp
                new_node.prev = temp.prev
                if temp.prev:
                    temp.prev.next = new_node
                temp.prev = new_node
                if temp == self.head:
                    self.head = new_node
                return
            temp = temp.next

# Usage Example
dll = DoublyLinkedList()
dll.append(10)
dll.append(20)
dll.prepend(5)
dll.insert_after(10, 15)
dll.insert_before(20, 17)
print("Forward:", dll.display_forward())  # Output: [5, 10, 15, 17, 20]
print("Backward:", dll.display_backward()) # Output: [20, 17, 15, 10, 5]
dll.delete(15)
print("After deleting 15:", dll.display_forward())  # Output: [5, 10, 17, 20]
dll.delete_at_position(1)
print("After deleting at position 1:", dll.display_forward())  # Output: [5, 17, 20]