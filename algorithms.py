import time
from estructuras import Node, FIFO, LIFO
import heapq


def heuristica_manhattan(actual, meta):
    x1, y1 = actual
    x2, y2 = meta
    return abs(x1 - x2) + abs(y1 - y2)

def heuristica_euclidiana(actual, meta):
    x1, y1 = actual
    x2, y2 = meta
    return (x1 - x2) ** 2 + (y1 - y2) ** 2
##implementación Squared para optimización

def breadth_first_search(estado_inicial, estado_meta, get_vecinos):
    start_time = time.time()
    frontera = FIFO()
    explorado = set()
    nodos_generados = 0

    nodo_inicial = Node(estado_inicial)
    frontera.add(nodo_inicial)
    frontier_states = {estado_inicial} 

    while not frontera.isEmpty():
        current = frontera.pop()
        frontier_states.remove(current.state)
        
        if current.state == estado_meta:
            end_time = time.time()
            path = get_path(current)
            return {
                "solucion": path,
                "nodos_explorados": len(explorado),
                "tiempo_ejecucion": end_time - start_time,
                "factor_ramificacion": nodos_generados / len(explorado) if explorado else 0
            }

        explorado.add(current.state)

        for vecino, action, cost in get_vecinos(current.state):
            if vecino not in explorado and vecino not in frontier_states:
                hijo = Node(vecino, current, action, current.cost + cost)
                frontera.add(hijo)
                frontier_states.add(vecino)
                nodos_generados += 1

    return None

def depth_first_search(estado_inicial, estado_meta, get_vecinos):
    start_time = time.time()
    frontera = LIFO()
    explorado = set()
    nodos_generados = 0
    
    nodo_inicial = Node(estado_inicial)
    frontera.add(nodo_inicial)
    frontier_states = {estado_inicial}
    
    while not frontera.isEmpty():
        current = frontera.pop()
        frontier_states.remove(current.state)
        
        if current.state == estado_meta:
            end_time = time.time()
            path = get_path(current)
            return {
                "solucion": path,
                "nodos_explorados": len(explorado),
                "tiempo_ejecucion": end_time - start_time,
                "factor_ramificacion": nodos_generados / len(explorado) if explorado else 0
            }
            
        explorado.add(current.state)
        
        for vecino, action, cost in get_vecinos(current.state):
            if vecino not in explorado and vecino not in frontier_states:
                hijo = Node(vecino, current, action, current.cost + cost)
                frontera.add(hijo)
                frontier_states.add(vecino)
                nodos_generados += 1
                
    return None
def greedy_best_first_search(estado_inicial, estado_meta, get_vecinos, heuristica):
    start_time = time.time()
    frontera = []
    explorado = set()
    nodos_generados = 0
    
    nodo_inicial = Node(estado_inicial)
    frontier_states = {estado_inicial}
    heapq.heappush(frontera, (heuristica(estado_inicial, estado_meta), nodo_inicial))
    
    while frontera:
        _, current = heapq.heappop(frontera)
        
        if current.state == estado_meta:
            end_time = time.time()
            path = get_path(current)
            return {
                "algoritmo": "Greedy Best-First Search",
                "solucion": path,
                "nodos_explorados": len(explorado),
                "tiempo_ejecucion": end_time - start_time,
                "factor_ramificacion": nodos_generados / len(explorado) if explorado else 0
            }
            
        explorado.add(current.state)
        
        for vecino, action, step_cost in get_vecinos(current.state):
            if vecino not in explorado and vecino not in frontier_states:
                hijo = Node(vecino, current, action, current.cost + step_cost)
                heapq.heappush(frontera, (heuristica(vecino, estado_meta), hijo))
                frontier_states.add(vecino)
                nodos_generados += 1
    
    return None


def a_star_search(estado_inicial, estado_meta, get_vecinos, heuristica):
    start_time = time.time()
    frontera = []  
    explorado = set()
    nodos_generados = 0
    frontier_states = {estado_inicial} 
    
    nodo_inicial = Node(estado_inicial)
    heapq.heappush(frontera, (heuristica(estado_inicial, estado_meta), nodo_inicial))

    while frontera:
        _, current = heapq.heappop(frontera)
        frontier_states.remove(current.state)  
        
        if current.state == estado_meta:
            end_time = time.time()  
            path = get_path(current)
            return {
                "algoritmo": "A* Search",
                "solucion": path,
                "nodos_explorados": len(explorado),
                "tiempo_ejecucion": end_time - start_time,  
                "factor_ramificacion": nodos_generados / len(explorado) if explorado else 0  
            }
            
        explorado.add(current.state)
        
        for vecino, action, step_cost in get_vecinos(current.state):
            if vecino not in explorado and vecino not in frontier_states:  
                hijo = Node(vecino, current, action, current.cost + step_cost)
                f_value = hijo.cost + heuristica(vecino, estado_meta)
                heapq.heappush(frontera, (f_value, hijo))
                frontier_states.add(vecino)  
                nodos_generados += 1  
    
    return None

def get_path(node):
    path = []
    current = node
    while current:
        path.append((current.state, current.action, current.cost))
        current = current.parent
    return list(reversed(path))
