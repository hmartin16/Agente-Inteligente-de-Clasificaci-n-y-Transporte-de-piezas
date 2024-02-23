import random

# Control
print("El programa corre")

# Dimensiones del laberinto
n = 4

# Matriz para representar el laberinto
maze = [[0 for i in range(n)] for j in range(n)]

# Celda actual
current_cell = (0, 0)

# Lista de celdas visitadas
visited_cells = [current_cell]

# Lista de celdas no visitadas
unvisited_cells = [(i, j) for i in range(n) for j in range(n) if (i, j) != current_cell]

# Mientras haya celdas no visitadas
while unvisited_cells:
    print("entró al while")
    # Buscar vecinos no visitados de la celda actual
    neighbors = []
    if current_cell[0] > 0 and (current_cell[0]-1, current_cell[1]) in unvisited_cells:
        neighbors.append((current_cell[0]-1, current_cell[1]))
    if current_cell[0] < n-1 and (current_cell[0]+1, current_cell[1]) in unvisited_cells:
        neighbors.append((current_cell[0]+1, current_cell[1]))
    if current_cell[1] > 0 and (current_cell[0], current_cell[1]-1) in unvisited_cells:
        neighbors.append((current_cell[0], current_cell[1]-1))
    if current_cell[1] < n-1 and (current_cell[0], current_cell[1]+1) in unvisited_cells:
        neighbors.append((current_cell[0], current_cell[1]+1))

    if neighbors:
        # Elegir aleatoriamente uno de los vecinos
        next_cell = random.choice(neighbors)

        # Eliminar la pared entre la celda actual y la siguiente celda
        if next_cell[0] < current_cell[0]:
            maze[current_cell[0]][current_cell[1]] |= 1
            maze[next_cell[0]][next_cell[1]] |= 4
        elif next_cell[0] > current_cell[0]:
            maze[current_cell[0]][current_cell[1]] |= 4
            maze[next_cell[0]][next_cell[1]] |= 1
        elif next_cell[1] < current_cell[1]:
            maze[current_cell[0]][current_cell[1]] |= 2
            maze[next_cell[0]][next_cell[1]] |= 8
        elif next_cell[1] > current_cell[1]:
            maze[current_cell[0]][current_cell[1]] |= 8

        # Actualizar la celda actual y marcarla como visitada
        current_cell = next_cell
        visited_cells.append(current_cell)
        unvisited_cells.remove(current_cell)
    else:
        # Retroceder a la celda anterior si no hay vecinos no visitados
        if len(visited_cells) < 2:
            break
        current_cell = visited_cells[-2]

print("salió del while")
"""

# Generar entradas y salidas adicionales
exits = []
for i in range(n):
    if maze[0][i] == 0:
        exits.append((0, i))
    if maze[n-1][i] == 0:
        exits.append((n-1, i))
    if maze[i][0] == 0:
        exits.append((i, 0))
    if maze[i][n-1] == 0:
        exits.append((i, n-1))

# Elegir aleatoriamente una entrada y una salida
entry, exit = random.sample(exits, 2)

# Agregar entradas y salidas al laberinto
maze[entry[0]][entry[1]] |= 1
maze[exit[0]][exit[1]] |= 2
"""


# Imprimir el laberinto
for row in maze:
    print("+", end="")
    for i in range(n):
        if row[i] & 1:
            print("   +", end="")
        else:
            print("---+", end="")
    print()
    print("|", end="")
    for i in range(n):
        if row[i] & 2:
            print("   |", end="")
        else:
            print("    ", end="")
        if i == n-1:
            print("|", end="")
    print()
print("+---"*n + "+")



# REVISAR PORQUE FUNCIONA A VECES
# Evaluar si vale la pena usar el algoritmo de backtracking para generar el laberinto
#consultar para decidir si usar backtracking o no