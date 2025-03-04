## Definimos la estructura nodo con su estado, parent, action y costo acumulado
class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state  
        self.parent = parent  
        self.action = action 
        self.cost = cost  
        self.node_id = id(self)  
    
    def __str__(self):
        return f"Node(state={self.state}, action={self.action}, cost={self.cost})"
    
    def __lt__(self, other):
        return self.node_id < other.node_id
    
    def __eq__(self, other):
        return self.node_id == other.node_id

# Implementación de estructuras de cola
class FIFO:
    def __init__(self):
        self.queue = []
    
    def isEmpty(self):
        return len(self.queue) == 0
    
    def top(self):
        if not self.isEmpty():
            return self.queue[0]
        return None
    
    def pop(self):
        if not self.isEmpty():
            return self.queue.pop(0)
        return None
    
    def add(self, item):
        self.queue.append(item)

class LIFO:
    def __init__(self):
        self.stack = []
    
    def isEmpty(self):
        return len(self.stack) == 0
    
    def top(self):
        if not self.isEmpty():
            return self.stack[-1]
        return None
    
    def pop(self):
        if not self.isEmpty():
            return self.stack.pop()
        return None
    
    def add(self, item):
        self.stack.append(item)