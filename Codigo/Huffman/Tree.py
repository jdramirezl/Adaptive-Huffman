from .Node import Internal, External


class Tree:
    def __init__(self):
        self.MAX_VAL = 213
        self.root = External("NYT", self.MAX_VAL, 0, 1)
        self.counter = self.MAX_VAL
        self.by_sym = {"NYT": self.root}
        self.blocks = {0: set()}

    def add(self, symbol):
        if symbol not in self.by_sym:
            if self.counter == 1:
                last_NYT = self.by_sym["NYT"]
                self.by_sym["NYT"] = None  # type: ignore
                
                last_node = External(symbol, 1, 0, last_NYT.height)
                self.by_sym[symbol] = last_node
                
                node = last_NYT
                new_node = last_node
                self.blocks[0].add(symbol)
            else:
                # Get old NYT
                node = self.by_sym["NYT"]

                # Create new NYT node
                new_left = External("NYT", self.counter - 2, 0, node.height + 1)
                self.by_sym["NYT"] = new_left

                # Create symbol node
                new_right = External(symbol, self.counter - 1, 0, node.height + 1)
                self.by_sym[symbol] = new_right
                self.blocks[0].add(symbol)
                
                # Create decision node
                new_node = Internal(new_left, new_right, self.counter, 0, node.height)
                
                # Update counter
                self.counter -= 2
                
                # Assign parent
                new_left.parent = new_node  # type: ignore
                new_right.parent = new_node  # type: ignore

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
        
        target = self.by_sym[symbol]
        self.update(target)

    
    def update(self, node):
        swapped = False
        
        # Update weight
        node.weight += 1
        
        # If node is root, return
        if not node.parent:
            return
    
        if type(node) == External:
            # Set variables for node
            w, s, h = node.weight, node.symbol, node.height
            
            # Look if new weight exists
            if w not in self.blocks:
                self.blocks[w] = set()
            
            # Move blocks
            self.blocks[w].add(s)
            self.blocks[w - 1].remove(s)
            
            # Look for node to swap
            big_sym = min(self.blocks[w - 1], key=lambda x: self.by_sym[x].height, default=None)
            biggest = self.by_sym[big_sym] if big_sym else None
            
            
            # If block is empty or node is the highest in the block, dont swap
            
            if swapped := (biggest and biggest.height < h):
                self.swap(node.parent, biggest)
        
        # Update Tree
        self.update(node.parent)
        if swapped:
            self.clean_tree()

    
    def swap(self, n1, n2):
        dir1 = self.direction(n1)
        dir2 = self.direction(n2)

        # Swap children
        if not dir1:
            n1.parent.left  = n2
        else:
            n1.parent.right = n2
        
        if not dir2:
            n2.parent.left  = n1
        else:
            n2.parent.right = n1
        
        # Swap parents
        n1.parent, n2.parent = n2.parent, n1.parent

    def clean_tree(self):
        self._clean_tree_aux(self.root, 1)

    def _clean_tree_aux(self, node, height):
        node.height = height
        
        if type(node) is External:
            return node.weight
        
        l = self._clean_tree_aux(node.left, height + 1)
        r = self._clean_tree_aux(node.right, height + 1)
        
        total = l + r
        
        node.weight = total
        
        return total
    
    def inTree(self, symbol):
        return symbol in self.by_sym

    def getPath(self, symbol):
        node = self.by_sym[symbol]
        if not node:
            return ""
        return self.getPathAux(node, "")

    def getPathAux(self, node, path):
        if not node.parent:
            return path
        
        if self.direction(node):
            path = '1' + path
        else:
            path = '0' + path

        return self.getPathAux(node.parent, path)

    def direction(self, node):
        if node is node.parent.left:  # 0 is left
            return 0
        return 1  # 1 is right

    def printTree(self):
        self.printTreeAux(self.root)

    def printTreeAux(self, node, level=0, l='-'):
        if node is not None:
            if type(node) == Internal:
                self.printTreeAux(node.right, level + 1, '1')
                print('-' * 4 * level + '-> ', l, '[', node.weight, node.id, ']')
                self.printTreeAux(node.left, level + 1, '0')
            else:
                print('-' * 4 * level + '-> ', l, '[', node.symbol, node.weight, node.id, ']')

    
    def printInorder(self):
        self.__printInorderAux(self.root)

    def __printInorderAux(self, node):
        if type(node) == Internal:
            self.__printInorderAux(node.left)
            print(f"(,{node.weight},{node.id})")
            self.__printInorderAux(node.right)
        else:
            print(f"[{node.symbol},{node.weight},{node.id}]")
    
