import os 
import cv2
import math
import pandas as pd
import numpy as np

class ProcesamientoImagen:
    
    def __init__(self, dimensiones=(300, 400)):
        self.dimensiones = dimensiones
        self.imagenes = []
        self.tabla_datos = pd.DataFrame()
        self.name = []
    
    def crear_csv(self, nombre_archivo): # Guarda el DataFrame en un archivo CSV sin índices
        carpeta_destino = os.path.join(os.getcwd(), "Procesamiento_de_imagenes") # Ruta completa de la carpeta "Procesamiento de imagenes"
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)
        ruta_archivo = os.path.join(carpeta_destino, nombre_archivo) # Ruta completa del archivo CSV
        self.tabla_datos.to_csv(ruta_archivo, sep=';', index=False)

    
    def leer_imagenes(self, carpeta): # Lee las imágenes de una carpeta y las almacena en self.imagenes
        name_im = os.listdir(carpeta) # Lista con los nombres de las imágenes, obtenidos desde la carpeta donde se encuentran
        for i in name_im:
            path = os.path.join(carpeta, i) # Ruta completa de la imagen
            self.imagenes.append(cv2.imread(path))
            indice = i.index('(')
            nombre = i[0:indice]
            self.name.append(nombre)
        
    def leer_imagen(self, path):   # Lee una única imagen desde la ruta especificada y la almacena en self.imagenes
        self.imagenes = cv2.imread(path)
        
    def procesarImagen(self, modo):
        # Dimensiones de redimensionamiento
        n_col = self.dimensiones[0]
        n_fil = self.dimensiones[1]
        
        if modo == 1:                   # Procesa todas las imágenes de la lista
            imagenes = self.imagenes[:]
            self.imagenes = []
            for i in imagenes:
                i = cv2.resize(i, (n_col, n_fil))  # Redimensiona la imagen
                im = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)  # Convierte la imagen a escala de grises
                im = cv2.GaussianBlur(im, (5, 5), 0) # Aplica el filtro gaussiano
                im = cv2.Canny(im, 50, 150)  # Detecta los bordes en la imagen utilizando el algoritmo de Canny
                im = cv2.dilate(im, None, iterations=1)  # Dilata los bordes
                im = cv2.erode(im, None, iterations=1)# Erosion de los bordes
                self.imagenes.append(im)
        
        else:                           # Procesa una única imagen
            self.imagenes = cv2.resize(self.imagenes, (n_col, n_fil))
            self.imagenes = cv2.cvtColor(self.imagenes, cv2.COLOR_BGR2GRAY)
            self.imagenes = cv2.GaussianBlur(self.imagenes, (5, 5), 0)
            self.imagenes = cv2.Canny(self.imagenes, 50, 150)
            self.imagenes = cv2.dilate(self.imagenes, None, iterations=1)
            self.imagenes = cv2.erode(self.imagenes, None, iterations=1)

    def hu_momentos(self, i):        # Calcula los momentos Hu de una imagen y los normaliza
        momentos = cv2.HuMoments(cv2.moments(i)) 
        for j in range(7):
            momentos[j] = round(-1 * math.copysign(1.0, momentos[j]) * math.log10(abs(momentos[j])), 2) # Normaliza los momentos Hu
        return momentos

    def rasgos_geometricos(self, i):
        # Encuentra los contornos en la imagen
        (contornos, _) = cv2.findContours(i.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        area = 0
        perimetro = 0
        draw = np.zeros((i.shape[0], i.shape[1], 3), dtype=np.uint8)
        im4 = cv2.drawContours(draw, contornos, -1, (255, 255, 0), 5)

        esbeltez_max = 0  # Variable para almacenar la máxima esbeltez encontrada

        for cnt in contornos:
            # Calcula el área y el perímetro de cada contorno
            area += cv2.contourArea(cnt)
            perimetro += cv2.arcLength(cnt, True)

            # Calcula la esbeltez del contorno actual
            rectangulo = cv2.minAreaRect(cnt)
            (x, y), (ancho, alto), angulo = rectangulo
            if ancho > alto:
                esbeltez = ancho / alto
            else:
                esbeltez = alto / ancho

            if esbeltez > esbeltez_max:
                esbeltez_max = esbeltez


        # Calcula la circularidad
        circularidad = 4 * math.pi * area / (perimetro ** 2)

        # Calcula la convexidad
        hull = cv2.convexHull(cnt)
        area_hull = cv2.contourArea(hull)
        convexidad = area / area_hull

        return circularidad, convexidad, esbeltez_max


    def caracteristicas(self, modo, nombre_archivo):  # Extrae las características de las imágenes y las almacena en self.tabla_datos
        self.procesarImagen(modo)
        if modo == 1:
            for i, img in enumerate(self.imagenes):
                momento = self.hu_momentos(img)
                circularidad, convexidad, esbeltez = self.rasgos_geometricos(img)
                caracteristicas = {
                    'momento1': momento[0],
                    'momento2': momento[1],
                    'momento3': momento[2],
                    'momento4': momento[3],
                    'momento5': momento[4],
                    'momento6': momento[5],
                    'momento7': momento[6],
                    'circularidad': circularidad,
                    'convexidad': convexidad,
                    'esbeltez': esbeltez,
                    'nombre': self.name[i]
                }
                self.tabla_datos = pd.concat([self.tabla_datos, pd.DataFrame(caracteristicas)], ignore_index=True)

        else:
            momento = self.hu_momentos(self.imagenes)
            circularidad, convexidad, esbeltez = self.rasgos_geometricos(self.imagenes)
            caracteristicas = {
                'momento1': momento[0],
                'momento2': momento[1],
                'momento3': momento[2],
                'momento4': momento[3],
                'momento5': momento[4],
                'momento6': momento[5],
                'momento7': momento[6],
                'circularidad': circularidad,
                'convexidad': convexidad,
                'esbeltez': esbeltez,
                'nombre': self.name
            }
            self.tabla_datos = pd.concat([self.tabla_datos, pd.DataFrame(caracteristicas)], ignore_index=True)

        # Crea el archivo CSV con las características
        self.crear_csv(nombre_archivo)

    def guardar_imagenes_procesadas(self, carpeta_destino):
        # Crea la carpeta de destino si no existe
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        # Guarda las imágenes procesadas en la carpeta de destino
        for i, img in enumerate(self.imagenes):
            nombre_imagen = f"imagen_{i}.jpg"  # Nombre de archivo para la imagen procesada
            ruta_destino = os.path.join(carpeta_destino, nombre_imagen)
            cv2.imwrite(ruta_destino, img)

        print(f"Imágenes procesadas guardadas en la carpeta: {carpeta_destino}")





if __name__ == '__main__':
    carpeta_imagenes = "Procesamiento_de_Imagenes/imagenes"
    procesamiento = ProcesamientoImagen()
    procesamiento.leer_imagenes(carpeta_imagenes)
    procesamiento.caracteristicas(modo=1, nombre_archivo ='caracteristicas_imagenes.csv')
    print(procesamiento.tabla_datos)
    procesamiento.guardar_imagenes_procesadas("Procesamiento de Imagenes/imagenes_procesadas")

    carpeta_muestra = "Procesamiento_de_Imagenes/imagenes_muestra"
    procesamiento_muestra = ProcesamientoImagen()
    procesamiento_muestra.leer_imagenes(carpeta_muestra)
    procesamiento_muestra.caracteristicas(modo=1, nombre_archivo='caracteristicas_muestras.csv')
    print(procesamiento_muestra.tabla_datos, "\n")

    carpeta_cajas = "Procesamiento_de_Imagenes/imagenes_cajas"
    procesamiento_cajas = ProcesamientoImagen()
    procesamiento_cajas.leer_imagenes(carpeta_cajas)
    procesamiento_cajas.caracteristicas(modo=1, nombre_archivo='caracteristicas_cajas.csv')
    print(procesamiento_cajas.tabla_datos)


