class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def hash_function(self, key):
        # Simple hash function using modulo
        return hash(key) % self.size

    def insert(self, key, value):
        hash_key = self.hash_function(key)
        # Check if key already exists, and if so, update it
        for i, kv in enumerate(self.table[hash_key]):
            if kv[0] == key:
                self.table[hash_key][i] = (key, value)
                return
        # Otherwise, add a new key-value pair
        self.table[hash_key].append((key, value))

    def search(self, key):
        hash_key = self.hash_function(key)
        # Search for the key in the chain at hash_key
        for kv in self.table[hash_key]:
            if kv[0] == key:
                return kv[1]  # Return value if found
        return None  # Return None if key is not found

    def delete(self, key):
        hash_key = self.hash_function(key)
        # Search for the key and delete if found
        for i, kv in enumerate(self.table[hash_key]):
            if kv[0] == key:
                del self.table[hash_key][i]
                return True  # Return True if deletion was successful
        return False  # Return False if key was not found

    def display(self):
        # Display the hash table structure
        for i, chain in enumerate(self.table):
            print(f"Bucket {i}: {chain}")

# Example usage
hash_table = HashTable(10)
hash_table.insert("apple", 100)
hash_table.insert("banana", 200)
hash_table.insert("grape", 300)
hash_table.display()

# Search for values
print("Search apple:", hash_table.search("apple"))
print("Search banana:", hash_table.search("banana"))

# Delete a key
hash_table.delete("banana")
hash_table.display()
