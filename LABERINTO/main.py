from lab_basico import Maze, Node

# Creamos una instancia del laberinto con tamaño 10x10, punto de inicio (0,0) y punto final (9,9)
start = (0,0)
end = (9,9)
size = 12
maze = Maze(start, end, size, 0.2)

# Encontramos el camino más corto desde el punto de inicio al final
shortest_path = maze.find_shortest_path()

# Imprimimos el laberinto y el camino más corto encontrado
maze.print_maze(shortest_path)
