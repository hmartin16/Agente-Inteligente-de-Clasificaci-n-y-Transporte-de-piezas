import pygame
import random

# Dimensiones del laberinto
width, height = 600, 600
n = 12  # Tamaño del laberinto

# Inicializar pygame
pygame.init()

# Crear ventana
screen = pygame.display.set_mode((width, height))

# Colores
white = (255, 255, 255)
black = (0, 0, 0)

# Tamaño de los bloques
block_size = width // n

# Matriz para representar el laberinto
maze = [[0 for i in range(n)] for j in range(n)]

# Generar laberinto aleatorio
pygame.draw.rect(screen, white, (0, 0, width, height))
for i in range(n):
    for j in range(n):
        if random.random() < 0.4:
            maze[i][j] = 1
            pygame.draw.rect(screen, black, (i*block_size, j*block_size, block_size, block_size))

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
if len(exits) >= 2:
    start = random.choice(exits)
    exits.remove(start)
    end = random.choice(exits)
    pygame.draw.rect(screen, (0, 255, 0), (start[0]*block_size, start[1]*block_size, block_size, block_size))
    pygame.draw.rect(screen, (255, 0, 0), (end[0]*block_size, end[1]*block_size, block_size, block_size))

# Actualizar pantalla
pygame.display.update()

# Esperar a que se cierre la ventana
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
