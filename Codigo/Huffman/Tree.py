class Node:
    def __init__(self, weight, id):
        self.weight = weight
        self.id = id
        self.parent = None
    
    def __str__(self):
        return f"Node: {self.id} - Weight: {self.weight} - Parent: {self.parent.id if self.parent else None}"

class Internal(Node):
    def __init__(self, left, right, weight, id):
        super().__init__(weight, id)
        self.left = left
        self.right = right

class External(Node):
    def __init__(self, symbol, weight, id):
        super().__init__(weight, id)
        self.symbol = symbol


class Tree:
    def __init__(self, ):
        self.root = External("NYT", 0, 213)
        self.NYT = 213
        self.by_sym = {}
        self.by_id = {}
        self.by_id[213] = self.root
    
    def update(self, index):
        #print("Updating", index)
        if index == 213:
            self.root.weight += 1
        else:
            curr = self.by_id[index]
            
            dir = self.direction(curr)
            
            if not dir:
                curr.parent.left.weight += 1
                curr = curr.parent.left
                sibling = curr.parent.right
            else:
                curr.parent.right.weight += 1
                curr = curr.parent.right
                sibling = curr.parent.left
            
            #print('before dad!', '\n',curr.parent.left, '\n',curr.parent.right)
            self.by_id[index] = curr
            #print("weights", curr.weight, sibling.weight)
            #print("ids", curr.id, sibling.id)
            if curr.weight > sibling.weight and not dir:
                #print("are we even here?")
                self.swap(curr)
            #print('after dad!', curr.parent.left.id, curr.parent.right.id)
            
            self.update(curr.parent.id)
    
    def direction(self, node):
        if node.id == node.parent.left.id:
            return 0
        return 1
    
    def swap(self, node):
        node.parent.left, node.parent.right = node.parent.right, node.parent.left
    
    def add(self, symbol):
        print("Adding", symbol)
        if symbol not in self.by_sym:
            print("Symbol not in tree")
            
            # Get old NYT
            node = self.by_id[self.NYT]
            
            #print("Old NYT","type", type(node))
            
            # Create new NYT
            new_left = External("NYT", 0, self.NYT - 2)
            
            # Add NYT to lookup
            self.by_id[self.NYT - 2] = new_left
            
            # Create symbol
            new_right = External(symbol, 0, self.NYT - 1)
            
            # Add symbol to lookups
            self.by_id[self.NYT - 1] = new_right
            self.by_sym[symbol] = self.NYT - 1
            
            # Create decision node
            new_node = Internal(new_left, new_right, 0, self.NYT)
            
            # Update parent
            if not node.parent:
                self.root = new_node
            else:
                dir = self.direction(node)
                if not dir:
                    node.parent.left = new_node  
                else:
                    node.parent.right = new_node 
                
                new_node.parent = node.parent
            
            # Assign parent
            new_left.parent = new_node  # type: ignore
            new_right.parent = new_node  # type: ignore
            
            self.by_id[self.NYT] = node
            
            # Update NYT
            self.NYT -= 2
        
        target = self.by_sym[symbol]
        
        print(target)
        
        self.update(target)


def printTree(node, level=0, l = '-'):
    if node != None:
        if type(node) == Internal:
            printTree(node.right, level + 1, '1')
            print('-' * 4 * level + '-> ', l, '[', node.weight, node.id, ']')
            printTree(node.left, level + 1, '0')
        else:
            print('-' * 4 * level + '-> ', l,'[', node.symbol, node.weight, node.id, ']')
        

def main():
    tree = Tree()
    string = "aardvark"
    #string = "aabbbcccc"
    
    for symbol in string:
        printTree(tree.root)
        tree.add(symbol)
    printTree(tree.root)

main()