class MaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, data):
        """Insert a new element into the heap"""
        self.heap.append(data)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        """Maintain the heap property by bubbling up the element at index"""
        parent_index = (index - 1) // 2
        if index > 0 and self.heap[index] > self.heap[parent_index]:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._heapify_up(parent_index)

    def extract_max(self):
        """Remove and return the largest element from the heap"""
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        max_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return max_val

    def _heapify_down(self, index):
        """Maintain the heap property by bubbling down the element at index"""
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        largest = index

        if left_child < len(self.heap) and self.heap[left_child] > self.heap[largest]:
            largest = left_child
        if right_child < len(self.heap) and self.heap[right_child] > self.heap[largest]:
            largest = right_child

        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self._heapify_down(largest)

    def get_max(self):
        """Return the largest element without removing it"""
        return self.heap[0] if self.heap else None

    def display(self):
        """Display the heap"""
        return self.heap

# Usage Example for Max-Heap
max_heap = MaxHeap()
max_heap.insert(10)
max_heap.insert(5)
max_heap.insert(3)
max_heap.insert(2)
max_heap.insert(8)

print("Max-Heap:", max_heap.display())  # Output: [10, 8, 3, 2, 5]
print("Extract Max:", max_heap.extract_max())  # Output: 10
print("Max-Heap after extraction:", max_heap.display())  # Output: [8, 5, 3, 2]
print("Maximum Element:", max_heap.get_max())  # Output: 8