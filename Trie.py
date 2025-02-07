class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        
    def search_valid_permutations(self, fromIdx: str, toIdx: str, node=None, path="", results=None) -> list:
        if results is None:
            results = []
        if node is None:
            node = self.root
            
        if node.is_end:
            if fromIdx in path and toIdx in path and path.index(fromIdx) < path.index(toIdx):
                results.append(path)
        # DFS search
        for char in sorted(node.children.keys()):
            self.search_valid_permutations(fromIdx, toIdx, node.children[char], path + char,results)
        return results
                