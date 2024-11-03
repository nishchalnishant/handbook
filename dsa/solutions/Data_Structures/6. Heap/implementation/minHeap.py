class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, data):
        """Insert a new element into the heap"""
        self.heap.append(data)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        """Maintain the heap property by bubbling up the element at index"""
        parent_index = (index - 1) // 2
        if index > 0 and self.heap[index] < self.heap[parent_index]:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._heapify_up(parent_index)

    def extract_min(self):
        """Remove and return the smallest element from the heap"""
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return min_val

    def _heapify_down(self, index):
        """Maintain the heap property by bubbling down the element at index"""
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        smallest = index

        if left_child < len(self.heap) and self.heap[left_child] < self.heap[smallest]:
            smallest = left_child
        if right_child < len(self.heap) and self.heap[right_child] < self.heap[smallest]:
            smallest = right_child

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def get_min(self):
        """Return the smallest element without removing it"""
        return self.heap[0] if self.heap else None

    def display(self):
        """Display the heap"""
        return self.heap

# Usage Example for Min-Heap
min_heap = MinHeap()
min_heap.insert(10)
min_heap.insert(5)
min_heap.insert(3)
min_heap.insert(2)
min_heap.insert(8)

print("Min-Heap:", min_heap.display())  # Output: [2, 5, 3, 10, 8]
print("Extract Min:", min_heap.extract_min())  # Output: 2
print("Min-Heap after extraction:", min_heap.display())  # Output: [3, 5, 8, 10]
print("Minimum Element:", min_heap.get_min())  # Output: 3