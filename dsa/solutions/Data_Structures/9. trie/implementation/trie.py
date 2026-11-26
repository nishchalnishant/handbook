class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            # If character not present, add a new node
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True  # Mark end of word

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False  # Character path does not exist
            node = node.children[char]
        return node.is_end_of_word  # Return True if end of word is reached

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False  # Character path does not exist
            node = node.children[char]
        return True  # If all characters in prefix are found

    def delete(self, word):
        # Helper function for deleting a word
        def _delete(node, word, depth):
            if depth == len(word):
                if not node.is_end_of_word:
                    return False  # Word not found
                node.is_end_of_word = False
                return len(node.children) == 0  # If no children, node can be deleted

            char = word[depth]
            if char not in node.children:
                return False  # Word not found
            
            # Recursively delete the child node
            should_delete = _delete(node.children[char], word, depth + 1)

            if should_delete:
                del node.children[char]
                return len(node.children) == 0  # Check if node can be deleted

            return False
        
        _delete(self.root, word, 0)

# Example usage
trie = Trie()
trie.insert("apple")
trie.insert("app")
print(trie.search("apple"))    # True
print(trie.search("app"))      # True
print(trie.search("ap"))       # False
print(trie.starts_with("app")) # True
trie.delete("apple")
print(trie.search("apple"))    # False
print(trie.search("app"))      # True
