from lab_intento_pygame import Maze, Node
import pygame


#Defino el laberinto
longitud = 12
while True:
    start_coords = input("Ingrese las coordenadas de inicio separadas por coma (ejemplo: 0,0): ")
    start_coords = start_coords.strip().split(",")
    if len(start_coords) != 2:
        print("Coordenadas de inicio inválidas. Por favor ingrese dos números separados por coma.")
        continue
    try:
        start_x, start_y = int(start_coords[0]), int(start_coords[1])
    except ValueError:
        print("Coordenadas de inicio inválidas. Por favor ingrese dos números separados por coma.")
        continue
    if start_x > (longitud-1) or start_y > (longitud-1):
        print("Coordenadas de inicio inválidas. Por favor ingrese dos números entre 0 y " + str(longitud-1) + ".")
        continue
    break

while True:
    end_coords = input("Ingrese las coordenadas de fin separadas por coma (ejemplo: 4,4): ")
    end_coords = end_coords.strip().split(",")
    if len(end_coords) != 2:
        print("Coordenadas de fin inválidas. Por favor ingrese dos números separados por coma.")
        continue
    try:
        end_x, end_y = int(end_coords[0]), int(end_coords[1])
    except ValueError:
        print("Coordenadas de fin inválidas. Por favor ingrese dos números separados por coma.")
        continue
    if end_x > (longitud-1) or end_y > (longitud-1):
        print("Coordenadas de fin inválidas. Por favor ingrese dos números entre 0 y " + str(longitud-1) + ".")
        continue
    if (start_x, start_y) == (end_x, end_y):
        print("Coordenadas de fin iguales a las de inicio. Por favor ingrese coordenadas diferentes.")
        continue
    break

# Dimensiones de la pantalla
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700

# Inicializamos pygame
pygame.init()

# Creamos la pantalla
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Laberinto")

# Creamos el laberinto
maze = Maze((start_x, start_y), (end_x, end_y), longitud, 0.3)
# Encontramos el camino más corto
shortest_path = maze.find_shortest_path()

# Ciclo principal del juego
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibujamos el laberinto
    screen.fill((255, 255, 255))
    maze.draw_maze(screen, shortest_path)

    # Actualizamos la pantalla
    pygame.display.update()

# Cerramos pygame
pygame.quit()
