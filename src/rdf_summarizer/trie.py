
array = [] 
class TrieNode:
    def __init__(self):
        self.children = {}

        # isEndOfWord is True if node represent the end of the word
        self.isEndOfWord = False
        self.numLeafs = 0

class Trie:
    def __init__(self):
        self.root = self.getNode()

    # returns new trie node
    def getNode(self):
        return TrieNode()

    # insert key in trie if not present
    def insert(self,key):
        node = self.root
        for char in key:
            if not char in node.children:
                node.children[char] = self.getNode()
            node = node.children[char]

        node.isEndOfWord = True
    
    # search key in the trie
    def search(self, key):
        node = self.root
        prefix_acc = ""
        longest_prefix = ""
        for char in key:
            prefix_acc = prefix_acc + char
            if not char in node.children:
                return longest_prefix
            node = node.children[char]
            if node.isEndOfWord:
                longest_prefix = prefix_acc

        return longest_prefix


