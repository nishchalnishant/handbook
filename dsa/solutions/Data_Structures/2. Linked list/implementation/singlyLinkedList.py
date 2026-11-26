class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    # Method to add a node at the beginning of the list
    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    # Method to add a node at the end of the list
    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    # Method to insert a node after a specific position
    def insert_at_position(self, data, position):
        if position < 0:
            print("Position must be a non-negative integer.")
            return
        new_node = Node(data)
        if position == 0:
            self.insert_at_beginning(data)
            return
        current = self.head
        for _ in range(position - 1):
            if current is None:
                print("Position out of bounds.")
                return
            current = current.next
        new_node.next = current.next
        current.next = new_node

    # Method to delete a node by value
    def delete_by_value(self, value):
        if self.head is None:
            print("List is empty.")
            return
        if self.head.data == value:
            self.head = self.head.next
            return
        current = self.head
        while current.next and current.next.data != value:
            current = current.next
        if current.next is None:
            print(f"Value {value} not found in the list.")
            return
        current.next = current.next.next

    # Method to delete a node at a specific position
    def delete_at_position(self, position):
        if self.head is None:
            print("List is empty.")
            return
        if position == 0:
            self.head = self.head.next
            return
        current = self.head
        for _ in range(position - 1):
            if current.next is None:
                print("Position out of bounds.")
                return
            current = current.next
        if current.next is None:
            print("Position out of bounds.")
            return
        current.next = current.next.next

    # Method to search for a value in the list
    def search(self, value):
        current = self.head
        position = 0
        while current:
            if current.data == value:
                return position
            current = current.next
            position += 1
        return -1

    # Method to display the linked list
    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")