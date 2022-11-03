class Node:
    def __init__(self, weight, height):
        self.weight = weight
        self.height = height
        self.parent = None
    
    

class Internal(Node):
    def __init__(self, left, right, weight, height):
        super().__init__(weight, height)
        self.left = left
        self.right = right
    
    def __str__(self):
        return f"Internal - Weight: {self.weight} - Parent: {self.parent.id if self.parent else None}"

class External(Node):
    def __init__(self, symbol, weight, id, height):
        super().__init__(weight, height)
        self.symbol = symbol
        self.id = id
    
    def __str__(self):
        return f"Id {self.id} - Weight: {self.weight} - Parent: {self.parent.id if self.parent else None}"