from .Tree import Tree


class Huffman:
    def __init__(self, alphabet):
        self.alphabet = {}

        count = 1
        for char in alphabet:
            self.alphabet[char] = count
            count += 1

        self.tree = Tree()
        self.E = 6
        self.R = 43

    def valid(self, char):
        char = ord(char)
        return char in self.alphabet

    def getFixedCode(self, char):
        K = self.alphabet[ord(char)]

        if 1 <= K <= 2 * self.R:
            binary = bin(K - 1)[2:]
            val = self.E + 1
        else:
            binary = bin(K - self.R - 1)[2:]
            val = self.E

        if len(binary) < val:
            binary = '0' * (val - len(binary)) + binary

        return binary

    def getCode(self, char):
        if not self.tree.inTree(char):
            NYT_code = self.tree.getPath("NYT")
            fixed = self.getFixedCode(char)
            code = NYT_code + fixed
        else:
            code = self.tree.getPath(char)

        self.tree.add(char)

        return code

    def encode(self, text):
        result = ""
        for char in text:
            if not self.valid(char):
                print("Símbolo encontrado genera error de compresión")
                return None
            self.tree.printTree()
            result += self.getCode(char)
        self.tree.printTree()
        self.tree.printInorder()
        return result
