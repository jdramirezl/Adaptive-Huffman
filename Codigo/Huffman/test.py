import heapq

class obj:
    def __init__(self, weight, id):
        self.weight = weight
        self.id = id
    
    def __repr__(self):
        return f"ID: {self.id} - Weight: {self.weight}"
    
    def __lt__(self, other):
        return self.weight < other.weight

a, b, c, d = obj(1, 'a'), obj(2, 'b'), obj(3, 'c'), obj(4, 'd')

l = [a, b, c, d]


heapq.heapify(l)

print(l)
print(list(l))

a.weight = 5  

print(l)
print(list(l))