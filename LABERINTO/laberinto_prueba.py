import pygame
import math
import heapq

# Define los colores que se utilizarán en el laberinto
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define las dimensiones del laberinto
WIDTH = 480
HEIGHT = 480
MARGIN = 40
CELL_SIZE = 40

# Define la clase del nodo del laberinto
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.g = 0
        self.h = 0
        self.f = 0
        self.neighbors = []
        self.previous = None
        self.wall = False
        
    def __lt__(self, other):
        return self.f < other.f
        
    def add_neighbors(self, grid):
        if self.row > 0 and not grid[self.row - 1][self.col].wall:
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.row < len(grid) - 1 and not grid[self.row + 1][self.col].wall:
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].wall:
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < len(grid[self.row]) - 1 and not grid[self.row][self.col + 1].wall:
            self.neighbors.append(grid[self.row][self.col + 1])

# Define la función para crear el laberinto
def create_maze(grid, obstacles):
    for row in range(1, len(grid) - 1):
        for col in range(1, len(grid[row]) - 1):
            if (row, col) not in obstacles:
                grid[row][col].wall = True
    start = grid[1][1]
    end = grid[len(grid) - 2][len(grid[0]) - 2]
    return start, end

# Define la función para dibujar el laberinto
def draw_grid(screen, grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            color = BLACK
            if grid[row][col].wall:
                color = WHITE
            pygame.draw.rect(screen, color, [(MARGIN + CELL_SIZE) * col + MARGIN,
                                             (MARGIN + CELL_SIZE) * row + MARGIN,
                                             CELL_SIZE,
                                             CELL_SIZE])

# Define la función para encontrar la solución utilizando el algoritmo A estrella
def a_star(start, end):
    open_list = []
    closed_list = []
    heapq.heappush(open_list, start)
    
    while len(open_list) > 0:
        current = heapq.heappop(open_list)
        closed_list.append(current)
        
        if current == end:
            path = []
            while current.previous:
                path.append(current)
                current = current.previous
            return path
        
        for neighbor in current.neighbors:
            if neighbor in closed_list:
                continue
            tentative_g_score = current.g + 1
            if neighbor not in open_list:
                heapq.heappush(open_list, neighbor)
            elif tentative_g_score >= neighbor.g:
                continue
                
            neighbor.previous = current
            neighbor.g = tentative_g_score
            neighbor.h = math.sqrt((neighbor.row - end.row)**2 + (neighbor.col - end.col)**2)
            neighbor.f = neighbor.g + neighbor.h
            
    return None

# Define la función para dibujar el camino encontrado por el algoritmo A estrella
def draw_path(screen, path):
    for node in path:
        pygame.draw.circle(screen, GREEN, ((MARGIN + CELL_SIZE) * node.col + MARGIN + CELL_SIZE//2,
                                           (MARGIN + CELL_SIZE) * node.row + MARGIN + CELL_SIZE//2), CELL_SIZE//4)

# Define la función principal
def main():
    # Inicializa pygame
    pygame.init()
    
    # Crea la pantalla del laberinto
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Laberinto")
    
    # Crea el laberinto
    grid = [[Node(row, col) for col in range(WIDTH // (CELL_SIZE + MARGIN))] for row in range(HEIGHT // (CELL_SIZE + MARGIN))]
    obstacles = [(3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8),
                 (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8)]
    start, end = create_maze(grid, obstacles)
    
    # Encuentra la solución utilizando el algoritmo A estrella
    path = a_star(start, end)
    
    # Dibuja el laberinto y el camino encontrado
    screen.fill(BLACK)
    draw_grid(screen, grid)
    if path is not None:
        draw_path(screen, path)
    
    # Actualiza la pantalla
    pygame.display.flip()
    
    # Espera a que se cierre la ventana
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

# Ejecuta la función principal
if __name__ == '__main__':
    main()
