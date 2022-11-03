class Node:
    def __init__(self, weight, height, id):
        self.weight = weight
        self.height = height
        self.parent = None
        self.id = id
    
    def __str__(self):
        return f"ID: {self.id} - Weight: {self.weight} - Height: {self.height}" #  - Parent - {self.parent.id if self.parent else None}



class Internal(Node):
    def __init__(self, left, right, id, weight, height):
        super().__init__(weight, height, id)
        self.left = left
        self.right = right

class External(Node):
    def __init__(self, symbol, id, weight, height):
        super().__init__(weight, height, id)
        self.symbol = symbol
    
    def __str__(self):
        return f'Symbol: {self.symbol} - ' + super().__str__()


