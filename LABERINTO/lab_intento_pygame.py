import pygame
import random
import heapq

class Maze:
    def __init__(self, start, end, size, density):
        self.start = Node(start[0], start[1])
        self.end = Node(end[0], end[1])
        self.size = size
        self.density = density
        self.grid = self.generate_maze()

    def generate_maze(self):
        grid = [[0 for j in range(self.size)] for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == (self.start.x, self.start.y) or (i, j) == (self.end.x, self.end.y):
                    grid[i][j] = 0
                else:
                    grid[i][j] = 1 if random.random() < self.density else 0
        return grid

    def get_neighbors(self, node):
        neighbors = []
        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x = node.x + i
            y = node.y + j
            if x >= 0 and y >= 0 and x < len(self.grid) and y < len(self.grid[0]) and self.grid[x][y] == 0:
                neighbors.append(Node(x, y))
        return neighbors

    def find_shortest_path(self):
        open_list = []
        closed_list = []
        heapq.heappush(open_list, self.start)
        while open_list:
            current_node = heapq.heappop(open_list)
            closed_list.append(current_node)
            if current_node == self.end:
                path = []
                while current_node is not None:
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent
                return path[::-1]
            for neighbor in self.get_neighbors(current_node):
                if neighbor in closed_list:
                    continue
                neighbor.g = current_node.g + 1
                neighbor.h = abs(neighbor.x - self.end.x) + abs(neighbor.y - self.end.y)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current_node
                if neighbor not in open_list:
                    heapq.heappush(open_list, neighbor)
        return None

    def draw_maze(self, screen, path):
        # Dimensiones de la ventana
        window_width = screen.get_width()
        window_height = screen.get_height()

        # Dimensiones de la celda
        cell_width = window_width // self.size
        cell_height = window_height // self.size

        # Dibujar la cuadrícula
        for i in range(self.size):
            for j in range(self.size):
                cell_x = j * cell_width
                cell_y = i * cell_height

                # Dibujar el cuadrado
                pygame.draw.rect(screen, (255, 255, 255), (cell_x, cell_y, cell_width, cell_height), 1)

                # Si es la celda de inicio, dibujar un rectángulo verde
                if (i, j) == (self.start.x, self.start.y):
                    pygame.draw.rect(screen, (0, 255, 0), (cell_x, cell_y, cell_width, cell_height))

                # Si es la celda de fin, dibujar un rectángulo rojo
                elif (i, j) == (self.end.x, self.end.y):
                    pygame.draw.rect(screen, (255, 0, 0), (cell_x, cell_y, cell_width, cell_height))

                # Si es parte del camino, dibujar un círculo azul
                elif path is not None and (i, j) in path:
                    pygame.draw.circle(screen, (0, 0, 255), (cell_x + cell_width // 2, cell_y + cell_height // 2), 10)

                # Si la celda está bloqueada, dibujar un cuadrado negro
                elif self.grid[i][j] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (cell_x + 2, cell_y + 2, cell_width - 4, cell_height - 4))

        # Actualizar la pantalla
        pygame.display.flip()

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y