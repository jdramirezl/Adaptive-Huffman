import tarfile
from Node import Internal, External

class Tree:
    def __init__(self, ):
        self.MAX_VAL = 107
        self.root = External("NYT", 0, self.MAX_VAL, 1)
        self.counter = self.MAX_VAL 
        self.by_sym = {"NYT": self.root}
        self.by_id = {}
        self.blocks = {0: set()}
        self.by_id[self.MAX_VAL] = self.root
        
    
    def update(self, node):
        #print("New iter")
        #print(self.blocks)
        # if type(node) == External:
        #     print("Updating", node.symbol, node.id)
        if not node.parent:
            self.root.weight += 1
        else:
            curr = node
            
            node.weight += 1
            
            # dir = self.direction(curr)
            
            # if not dir:
            #     curr.parent.left.weight += 1
            # else:
            #     curr.parent.right.weight += 1
            
            if type(curr) == External:
                index = curr.id
                
                self.blocks[curr.weight - 1].remove(index)
                
                if curr.weight not in self.blocks:
                    self.blocks[curr.weight] = set()
                self.blocks[curr.weight].add(index)
                
                biggest = min(self.blocks[curr.weight - 1], key=lambda x: self.by_id[x].height, default=None)
                
                if biggest:
                    self.swap(self.by_id[index].parent, self.by_id[biggest])
            
            self.update(curr.parent)
    
    def add(self, symbol):
        print("Adding", symbol)
        if symbol not in self.by_sym:
            print("Symbol not in tree")
            
            # Get old NYT
            node = self.by_sym["NYT"]
            
            # Create new NYT
            
            new_left = External("NYT", "", 107, node.height + 1)
            
            # Add NYT to lookup
            self.by_sym["NYT"] = new_left
            
            # Create symbol
            self.counter -= 1
            new_right = External(symbol, 0, self.counter, node.height + 1)
            
            
            # Add symbol to lookups
            self.by_id[self.counter] = new_right
            self.by_sym[symbol] = new_right
            
            # Add to block
            self.blocks[0].add(self.counter)
            
            # Create decision node
            new_node = Internal(new_left, new_right, 0, node.height)
            
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
        else:
            print("Symbol in tree")
        
        target = self.by_sym[symbol]
        
        self.update(target)
    
    def direction(self, node):
        if node is node.parent.left: # 0 is left
            return 0
        return 1 # 1 is right
    
    def swap(self, n1, n2):
        n1_dir = self.direction(n1)
        n2_dir = self.direction(n2)
        
        # Swap children
        if not n1_dir:
            n1.parent.left = n2
        else:
            n1.parent.right = n2
        
        if not n2_dir:
            n2.parent.left = n1
        else:
            n2.parent.right = n1
        
        # Swap parents
        n1.parent, n2.parent = n2.parent, n1.parent
        
        # swap heights
        self.propagate_height(n1, n2.height)
        self.propagate_height(n2, n1.height)
    
    def propagate_height(self, node, height):
        if not node:
            return
        
        node.height = height
        
        if type(node) == External:
            return
        
        self.propagate_height(node.left, height + 1)
        self.propagate_height(node.right, height + 1)
    
    def printTree(self):
        self.printTreeAux(self.root)
    
    def printTreeAux(self, node, level=0, l = '-'):
        if node != None:
            if type(node) == Internal:
                self.printTreeAux(node.right, level + 1, '1')
                print('-' * 4 * level + '-> ', l, '[', node.weight, ']')
                self.printTreeAux(node.left, level + 1, '0')
            else:
                print('-' * 4 * level + '-> ', l,'[', node.symbol, node.weight, node.id, ']')

    def printInorder(self):
        self.printInorderAux(self.root)
    
    def printInorderAux(self, node):
        if type(node) == Internal:
            self.printInorderAux(node.left)
            print(f"[,{node.weight},]")
            self.printInorderAux(node.right)
        else:
            print(f"[{node.symbol},{node.weight},{node.id}]")


def main():
    tree = Tree()
    #string = "aardvark"
    string = "abccde"
    
    for symbol in string:
        tree.printTree()
        tree.add(symbol)
    tree.printTree()
    tree.printInorder()

main()