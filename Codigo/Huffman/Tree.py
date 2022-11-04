from .Node import Internal, External


class Tree:
    def __init__(self):
        self.MAX_VAL = 213
        self.root = External("NYT", self.MAX_VAL, 0, 1)
        self.counter = self.MAX_VAL
        self.by_sym = {"NYT": self.root}
        self.by_id = {}
        self.blocks = {0: set()}
        self.by_id[self.MAX_VAL] = self.root

    def update(self, node):
        if not node.parent:
            self.root.weight += 1
        else:
            curr = node

            node.weight += 1

            if type(curr) == External:
                index = curr.id

                if curr.weight not in self.blocks:
                    self.blocks[curr.weight] = set()
                self.blocks[curr.weight].add(index)

                self.blocks[curr.weight - 1].remove(index)
                biggest = min(self.blocks[curr.weight - 1], key=lambda x: self.by_id[x].height, default=None)

                
                print("biggest", biggest, "curr", curr.id)
                if biggest:
                    print("biggest height", self.by_id[biggest].height, "curr height", curr.height)
                if biggest and self.by_id[biggest].height < curr.height:
                    self.swap(self.by_id[index].parent, self.by_id[biggest])

            self.update(curr.parent)

    def inTree(self, symbol):
        return symbol in self.by_sym

    def getPath(self, symbol):
        node = self.by_sym[symbol]
        return self.getPathAux(node, "")

    def getPathAux(self, node, path):
        if not node.parent:
            return path

        if self.direction(node):
            path = '1' + path
        else:
            path = '0' + path

        return self.getPathAux(node.parent, path)

    def add(self, symbol):
        if symbol not in self.by_sym:

            # Get old NYT
            node = self.by_sym["NYT"]

            # Create new NYT

            new_left = External("NYT", self.counter - 2, 0, node.height + 1)

            # Add NYT to lookup
            self.by_sym["NYT"] = new_left

            # Create symbol
            new_right = External(symbol, self.counter - 1, 0, node.height + 1)

            # Add symbol to lookups
            self.by_id[self.counter - 1] = new_right
            self.by_sym[symbol] = new_right

            # Add to block
            self.blocks[0].add(self.counter - 1)
            
            # Create decision node
            new_node = Internal(new_left, new_right, self.counter, 0, node.height)

            self.counter -= 2
            
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

        target = self.by_sym[symbol]

        self.update(target)

    def direction(self, node):
        if node is node.parent.left:  # 0 is left
            return 0
        return 1  # 1 is right

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
        self.propagate_height(n2, n1.height + 1)

    def propagate_height(self, node, height):
        if not node:
            return

        node.height = height

        if type(node) == External:
            return

        self.propagate_height(node.left, height + 1)
        self.propagate_height(node.right, height + 1)
        
        self.propagate_quantity(self.root)

    def propagate_quantity(self, node):
        if type(node) == External:
            return node.weight
        
        l, r = self.propagate_quantity(node.left), self.propagate_quantity(node.right)
        
        
        
        node.weight = l + r
        
        return node.weight
        
    
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
            print(f"[,{node.weight},]")
            self.__printInorderAux(node.right)
        else:
            print(f"[{node.symbol},{node.weight},{node.id}]")
    
