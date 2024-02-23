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

    def print_maze(self, path):
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == (self.start.x, self.start.y):
                    print("S", end=" ")
                elif (i, j) == (self.end.x, self.end.y):
                    print("E", end=" ")
                elif path is not None and (i, j) in path:
                    print("*", end=" ")
                elif self.grid[i][j] == 1:
                    print("X", end=" ")
                else:
                    print("_", end=" ")
            print()

    
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
