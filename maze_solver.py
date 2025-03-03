import sys
from algorithms import breadth_first_search, depth_first_search, greedy_best_first_search, a_star_search
from algorithms import heuristica_manhattan, heuristica_euclidiana

class MazeSolver:
    def __init__(self, maze_file):
        self.maze = self.load_maze(maze_file)
        self.width = len(self.maze[0])
        self.height = len(self.maze)
        self.punto_partida = self.find_positions('2')
        self.punto_salida = self.find_positions('3')
        
        if not self.punto_partida:
            raise ValueError("No se encontró punto partida ")
        if not self.punto_salida:
            raise ValueError("No se encontró punto salida")
        
        self.start_pos = self.punto_partida[0]  
        self.goal_pos = self.punto_salida[0]    
        
    def load_maze(self, filename):
        with open(filename, 'r') as file:
            return [list(line.strip()) for line in file if line.strip()]

    def find_positions(self, char):
        positions = []
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == char:
                    positions.append((x, y))
        return positions
    
    def get_neighbors(self, state):
        x, y = state
        neighbors = []
        
        directions = [
            (0, -1, "arriba"),
            (1, 0, "derecha"),
            (0, 1, "abajo"),
            (-1, 0, "izquierda")
        ]
        
        for dx, dy, action in directions:
            nx, ny = x + dx, y + dy
            
            # se revisa si no hay pared para mover
            if (0 <= nx < self.width and 0 <= ny < self.height and 
                self.maze[ny][nx] != '1'):
                neighbors.append(((nx, ny), action, 1))  # Costo 1 por movimiento
                
        return neighbors
    
    def solve(self, algorithm, heuristic=None):
        if algorithm == "bfs":
            return breadth_first_search(self.start_pos, self.goal_pos, self.get_neighbors)
        elif algorithm == "dfs":
            return depth_first_search(self.start_pos, self.goal_pos, self.get_neighbors)
        elif algorithm == "greedy":
            if not heuristic:
                raise ValueError("Escoga Heuristica para greedy")
            return greedy_best_first_search(self.start_pos, self.goal_pos, self.get_neighbors, heuristic)
        elif algorithm == "astar":
            if not heuristic:
                raise ValueError("Escoga Heuristica para A*")
            return a_star_search(self.start_pos, self.goal_pos, self.get_neighbors, heuristic)
        else:
            raise ValueError(f"Escoga uno de los algoritmos implementados: {algorithm}")
    def run_benchmark(self, num_random_starts=5):
        ##se corren todos los algoritmos con 5 posiciones aleatorias establecidas en los archivos de laberinto
        ##toma el promedio de sus pruebas
        "correr todos los algoritmos"
        algorithms = {
            "BFS": ("bfs", None),
            "DFS": ("dfs", None),
            "Greedy (Manhattan)": ("greedy", heuristica_manhattan),
            "Greedy (Euclidean)": ("greedy", heuristica_euclidiana),
            "A* (Manhattan)": ("astar", heuristica_manhattan),
            "A* (Euclidean)": ("astar", heuristica_euclidiana)
    }
    ##usar start positions disponibles
        if len(self.punto_partida) > 1:
            benchmark_starts = self.punto_partida[:min(num_random_starts, len(self.punto_partida))]
        else:
            benchmark_starts = [self.punto_partida[0]] * num_random_starts
    
        results = {}
    
        for name, (algo, heuristic) in algorithms.items():
            results[name] = {
                "path_lengths": [],
                "nodes_explored": [],
                "execution_times": [],
                "branching_factors": []
            }
        
            for start_pos in benchmark_starts:
                self.start_pos = start_pos
            
                try:
                    if heuristic:
                        solution = self.solve(algo, heuristic)
                    else:
                        solution = self.solve(algo)
                
                    if solution:
                    # Métricas
                        largo_path = len(solution["solucion"]) - 1  
                        nodo_explorado = solution["nodos_explorados"]
                        tiempo_ejecutado = solution.get("tiempo_ejecucion", 0)
                        branching_factor = solution.get("factor_ramificacion", 0)
                    
                    # Almacenar
                        results[name]["path_lengths"].append(largo_path)
                        results[name]["nodes_explored"].append(nodo_explorado)
                        results[name]["execution_times"].append(tiempo_ejecutado)
                        results[name]["branching_factors"].append(branching_factor)
                except Exception as e:
                    print(f"Error running {name} from {start_pos}: {e}")
    
        for name in algorithms:
            for metric in ["path_lengths", "nodes_explored", "execution_times", "branching_factors"]:
                values = results[name][metric]
                if values:
                    results[name][f"avg_{metric}"] = sum(values) / len(values)
                else:
                    results[name][f"avg_{metric}"] = 0
    
        print("\n===== Resultados prueba completa =====")
        print(f"Numero de posiciones iniciales probadas: {len(benchmark_starts)}")
        print("\nAlgoritmo | Promedio de largo de camino solución | Promedio de nodos visitados | Tiempo promedio de ejecución (s) | Branching Factor Promedio")
        print("-" * 90)
    
        for name in algorithms:
            avg_path = results[name]["avg_path_lengths"]
            avg_nodes = results[name]["avg_nodes_explored"]
            avg_time = results[name]["avg_execution_times"]
            avg_branch = results[name]["avg_branching_factors"]
        
            print(f"{name.ljust(20)} | {avg_path:.2f} | {avg_nodes:.2f} | {avg_time:.6f} | {avg_branch:.2f}")
    
        return results

def main():
    if len(sys.argv) < 2:
        print("Uso: python maze_solver.py <maze_file> [algorithm] [heuristic]")
        print("Algoritmos disponibles: bfs, dfs, greedy, astar, benchmark")
        print("Heuristicas: manhattan, euclidean")
        sys.exit(1)
    
    maze_file = sys.argv[1]
    
    algorithm = "bfs"
    heuristic_name = None
    
    if len(sys.argv) > 2:
        algorithm = sys.argv[2].lower()
    
    if len(sys.argv) > 3:
        heuristic_name = sys.argv[3].lower()
    
    # Validación algoritmo
    valid_algorithms = ["bfs", "dfs", "greedy", "astar", "benchmark"]
    if algorithm not in valid_algorithms:
        print(f"Algorithm no valido: {algorithm}")
        print(f"Algorithms disponibles: {', '.join(valid_algorithms)}")
        sys.exit(1)
    
    try:
        solver = MazeSolver(maze_file)
    except Exception as e:
        print(f"Error cargando laberinto: {e}")
        sys.exit(1)
    
    if algorithm == "benchmark":
        solver.run_benchmark()
    else:
        heuristic = None
        if algorithm in ["greedy", "astar"]:
            if heuristic_name == "manhattan":
                heuristic = heuristica_manhattan
            elif heuristic_name == "euclidean":
                heuristic = heuristica_euclidiana
            else:
                print(f"Escoga Heuristica correcta para {algorithm}. Se utilizó Manhattan.")
                heuristic = heuristica_manhattan
                heuristic_name = "manhattan"
        
        # Correr
        try:
            if heuristic:
                solution = solver.solve(algorithm, heuristic)
            else:
                solution = solver.solve(algorithm)
            
            if solution:
                path_length = len(solution["solucion"]) - 1  ##numero de pasos
                nodes_explored = solution["nodos_explorados"]
                execution_time = solution.get("tiempo_ejecucion", 0)
                branching_factor = solution.get("factor_ramificacion", 0)
                
                print("\n===== Solución Encontrada =====")
                print(f"Algorithmo: {algorithm.upper()}")
                if heuristic_name:
                    print(f"Heuristica: {heuristic_name.capitalize()}")
                print(f"Largo Camino: {path_length} pasos")
                print(f"Nodos visitados: {nodes_explored}")
                print(f"Tiempo de ejecución: {execution_time:.6f} segundos")
                print(f"Branching Factor: {branching_factor:.4f}")
                
                print(f"Punto de partida: {solver.start_pos}")
                print(f"Punto de salida: {solver.goal_pos}")
            else:
                print(f"No se encontró solución con {algorithm}")
        except Exception as e:
            print(f"Error resolviendo: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()