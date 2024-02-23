import pygame
import heapq


class Laberinto:
    def __init__(self, tamaño):
        self.inicio = None
        self.fin = None
        self.tamaño = tamaño
        self.grid = [[0 for _ in range(self.tamaño)] for _ in range(self.tamaño)]
        self.color_obstaculo = (0, 0, 0)
        self.color_vacio = (255, 255, 255)
        self.color_inicio = (0, 255, 0)
        self.color_fin = (255, 0, 0)
        self.color_camino = (192, 192, 192)
        self.ancho_celda = 0
        self.alto_celda = 0
        self.modo_obstáculo = False  # False = vacio, True = obstáculo
        self.camino = None
        self.inicio_establecido = False
        self.fin_establecido = False
        self.cursor = None

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Botón izquierdo del ratón
                self.toggle_obstáculo(evento.pos)
            elif evento.button == 3:  # Botón derecho del ratón
                self.iniciar_búsqueda_camino()

    def toggle_obstáculo(self, posición):
        if not self.camino:
            celda_x = posición[0] // self.ancho_celda
            celda_y = posición[1] // self.alto_celda
            if self.inicio_establecido and self.fin_establecido:
                self.grid[celda_y][celda_x] = 1 - self.grid[celda_y][celda_x]
            elif not self.inicio_establecido:
                self.inicio = Nodo(celda_y, celda_x)
                self.inicio_establecido = True
            elif not self.fin_establecido:
                self.fin = Nodo(celda_y, celda_x)
                self.fin_establecido = True

    def iniciar_búsqueda_camino(self):
        if self.inicio_establecido and self.fin_establecido:
            self.camino = self.encontrar_camino_más_corto()
            if self.camino:
                self.cursor = Cursor(self.camino)

    def obtener_vecinos(self, nodo):
        vecinos = []
        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x = nodo.x + i
            y = nodo.y + j
            if (
                x >= 0
                and y >= 0
                and x < len(self.grid)
                and y < len(self.grid[0])
                and self.grid[x][y] == 0
            ):
                vecinos.append(Nodo(x, y))
        return vecinos

    def encontrar_camino_más_corto(self):
        lista_abierta = []
        lista_cerrada = []
        heapq.heappush(lista_abierta, self.inicio)
        while lista_abierta:
            nodo_actual = heapq.heappop(lista_abierta)
            lista_cerrada.append(nodo_actual)
            if nodo_actual == self.fin:
                camino = []
                while nodo_actual is not None:
                    camino.append((nodo_actual.x, nodo_actual.y))
                    nodo_actual = nodo_actual.padre
                return camino[::-1]
            for vecino in self.obtener_vecinos(nodo_actual):
                if vecino in lista_cerrada:
                    continue
                vecino.g = nodo_actual.g + 1
                vecino.h = abs(vecino.x - self.fin.x) + abs(vecino.y - self.fin.y)
                vecino.f = vecino.g + vecino.h
                vecino.padre = nodo_actual
                if vecino not in lista_abierta:
                    heapq.heappush(lista_abierta, vecino)
        print("El laberinto no tiene solución.")  # Mensaje cuando no hay solución
        return None


    def dibujar_laberinto(self, pantalla):
        # Dimensiones de la ventana
        ancho_ventana = pantalla.get_width()
        alto_ventana = pantalla.get_height()

        # Dimensiones de la celda
        self.ancho_celda = ancho_ventana // self.tamaño
        self.alto_celda = alto_ventana // self.tamaño

        # Dibujar la cuadrícula
        for i in range(self.tamaño):
            for j in range(self.tamaño):
                celda_x = j * self.ancho_celda
                celda_y = i * self.alto_celda

                # Dibujar el cuadrado
                if self.grid[i][j] == 0:
                    pygame.draw.rect(
                        pantalla,
                        self.color_vacio,
                        (celda_x, celda_y, self.ancho_celda, self.alto_celda),
                    )
                else:
                    pygame.draw.rect(
                        pantalla,
                        self.color_obstaculo,
                        (celda_x, celda_y, self.ancho_celda, self.alto_celda),
                    )

                # Si es la celda de inicio:
                if (
                    self.inicio_establecido
                    and (i, j) == (self.inicio.x, self.inicio.y)
                ):
                    pygame.draw.rect(
                        pantalla,
                        self.color_inicio,
                        (celda_x, celda_y, self.ancho_celda, self.alto_celda),
                    )

                # Si es la celda de fin:
                elif self.fin_establecido and (i, j) == (self.fin.x, self.fin.y):
                    pygame.draw.rect(
                        pantalla,
                        self.color_fin,
                        (celda_x, celda_y, self.ancho_celda, self.alto_celda),
                    )

                # Si es parte del camino:
                #elif self.camino is not None and (i, j) in self.camino:
                 #   pygame.draw.rect(
                 #       pantalla,
                    #      self.color_camino,
                    #    (celda_x, celda_y, self.ancho_celda, self.alto_celda),
                    #)

        # Dibujar el cursor
        if self.cursor:
            self.cursor.dibujar(pantalla, self.ancho_celda, self.alto_celda)

        # Actualizar la pantalla
        pygame.display.flip()


    def iniciar_laberinto(self):
        # Dimensiones de la ventana
        ancho_ventana = 500
        alto_ventana = 500

        # Inicializar pygame y la ventana
        pygame.init()
        pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
        pygame.display.set_caption("Laberinto")

        ejecutando = True
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                else:
                    self.manejar_evento(evento)

            pantalla.fill((255, 255, 255))
            self.dibujar_laberinto(pantalla)

            # Avanzar el cursor si hay un camino
            if self.cursor:
                self.cursor.avanzar()

            pygame.time.wait(200)  # Retardo de 200 milisegundos entre avances del cursor

            pygame.display.flip()

        pygame.quit()

class Nodo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.padre = None

    def __lt__(self, otro):
        return self.f < otro.f

    def __eq__(self, otro):
        return self.x == otro.x and self.y == otro.y


class Cursor:
    def __init__(self, camino):
        camino.pop(0)  # Borrar el inicio
        camino.pop(-1)  # Borrar el fin
        self.camino = camino
        self.posición_actual = 0
        self.celdas_recorridas = []

    def dibujar(self, pantalla, ancho_celda, alto_celda):
        for posición in self.celdas_recorridas:
            celda_x = posición[1] * ancho_celda
            celda_y = posición[0] * alto_celda
            pygame.draw.rect(
                pantalla,
                (192, 192, 192),
                (celda_x, celda_y, ancho_celda, alto_celda),
            )

    def avanzar(self):
        if self.posición_actual < len(self.camino):
            nueva_posición = self.camino[self.posición_actual]
            if nueva_posición not in self.celdas_recorridas:
                self.celdas_recorridas.append(nueva_posición)
            self.posición_actual += 1





if __name__ == "__main__":
    tamaño = 12
    laberinto = Laberinto(tamaño)
    laberinto.iniciar_laberinto()
    while True:
        print("¿Desea reiniciar el laberinto? (s/n)")
        respuesta = input()
        if respuesta == "s":
            laberinto = Laberinto(tamaño)
            laberinto.iniciar_laberinto()
        else:
            break



