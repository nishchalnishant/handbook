class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        """Add a node at the end of the list"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.head.next = self.head
            return
        temp = self.head
        while temp.next != self.head:
            temp = temp.next
        temp.next = new_node
        new_node.next = self.head

    def prepend(self, data):
        """Add a node at the beginning of the list"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.head.next = self.head
            return
        new_node.next = self.head
        temp = self.head
        while temp.next != self.head:
            temp = temp.next
        temp.next = new_node
        self.head = new_node

    def delete(self, key):
        """Delete the first node with the given key"""
        if not self.head:
            return
        temp = self.head
        prev = None
        if self.head.data == key:
            while temp.next != self.head:
                temp = temp.next
            if self.head.next == self.head:  # only one node
                self.head = None
            else:
                temp.next = self.head.next
                self.head = self.head.next
            return
        while temp.next != self.head:
            prev = temp
            temp = temp.next
            if temp.data == key:
                prev.next = temp.next
                return

    def delete_at_position(self, position):
        """Delete a node at a specific position"""
        if not self.head or position < 0:
            return
        temp = self.head
        if position == 0:
            if self.head.next == self.head:  # only one node
                self.head = None
            else:
                while temp.next != self.head:
                    temp = temp.next
                temp.next = self.head.next
                self.head = self.head.next
            return
        for _ in range(position - 1):
            temp = temp.next
            if temp.next == self.head:
                return
        temp.next = temp.next.next

    def display(self):
        """Display the list"""
        elements = []
        if not self.head:
            return elements
        temp = self.head
        while True:
            elements.append(temp.data)
            temp = temp.next
            if temp == self.head:
                break
        return elements

    def insert_after(self, prev_node_data, data):
        """Insert a node after a given node data"""
        temp = self.head
        while temp:
            if temp.data == prev_node_data:
                new_node = Node(data)
                new_node.next = temp.next
                temp.next = new_node
                return
            temp = temp.next
            if temp == self.head:
                break

    def insert_before(self, next_node_data, data):
        """Insert a node before a given node data"""
        if not self.head:
            return
        if self.head.data == next_node_data:  # Insert before head
            self.prepend(data)
            return
        temp = self.head
        prev = None
        while True:
            if temp.data == next_node_data:
                new_node = Node(data)
                new_node.next = temp
                prev.next = new_node
                return
            prev = temp
            temp = temp.next
            if temp == self.head:
                break

# Usage Example
cll = CircularLinkedList()
cll.append(10)
cll.append(20)
cll.prepend(5)
cll.insert_after(10, 15)
cll.insert_before(20, 17)
print("List:", cll.display())  # Output: [5, 10, 15, 17, 20]
cll.delete(15)
print("After deleting 15:", cll.display())  # Output: [5, 10, 17, 20]
cll.delete_at_position(1)
print("After deleting at position 1:", cll.display())  # Output: [5, 17, 20]