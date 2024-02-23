import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import subprocess


from kMeans import KmeansObjetos
from kMeans import analisis_kmeans
from Knn import KnnObjetos
from Procesamiento_de_Imagenes import procesamiento_imagen
from Planificacion import Planificador
from LABERINTO import laberintoFINAL

class Agente:
    def __init__(self, ruta_datos_entrenamiento, ruta_datos_muestra, ruta_datos_cajas):
        self.ruta_datos_entrenamiento = ruta_datos_entrenamiento
        self.ruta_datos_muestra = ruta_datos_muestra
        self.ruta_datos_cajas = ruta_datos_cajas

        self.datos_entrenamiento = pd.read_csv(ruta_datos_entrenamiento, delimiter=';', decimal='.')
        self.datos_muestra = pd.read_csv(ruta_datos_muestra, delimiter=';', decimal='.')
        self.datos_cajas = pd.read_csv(ruta_datos_cajas, delimiter=';', decimal='.')
        self.orden_inicial = []

    def generar_archivo_caracteristicas(self, nombre_archivo, carpeta_imagenes, modo):
        procesamiento = procesamiento_imagen.ProcesamientoImagen()
        procesamiento.leer_imagenes(carpeta_imagenes)
        procesamiento.caracteristicas(modo=1, nombre_archivo=nombre_archivo)
        if modo == 1:
            procesamiento.guardar_imagenes_procesadas("Procesamiento_de_Imagenes/imagenes_procesadas")
            self.datos_entrenamiento = pd.read_csv(self.ruta_datos_entrenamiento, delimiter=';', decimal='.')
        elif modo == 2:
            self.datos_muestra = pd.read_csv(self.ruta_datos_muestra, delimiter=';', decimal='.')
        else:
            self.datos_cajas = pd.read_csv(self.ruta_datos_cajas, delimiter=';', decimal='.')


    def kMeans_agente(self, datos_entrenamiento, datos_muestra):
        # PREPROCESAMIENTO DE DATOS PARA KMEANS
        etiquetas_entrenamiento = datos_entrenamiento['nombre']
        datos_entrenamiento = datos_entrenamiento.drop('nombre', axis=1)                       # elimino la columna nombre
        datos_muestra = datos_muestra.drop('nombre', axis=1)                                   # elimino la columna nombre
        columnas_eliminar = ['momento1', 'momento3', 'momento4', 'momento5', 'momento6', 'momento7', 'momento2']  # elimino columnas irrelevantes
        datos_entrenamiento = datos_entrenamiento.drop(columnas_eliminar, axis=1)
        datos_muestra = datos_muestra.drop(columnas_eliminar, axis=1)
        
        # Datos normalizados, da mejor precisión
        min_max_scaler = MinMaxScaler()
        datos_entrenamiento = pd.DataFrame(min_max_scaler.fit_transform(datos_entrenamiento), columns=datos_entrenamiento.columns) # normalizo los datos
        datos_muestra = pd.DataFrame(min_max_scaler.fit_transform(datos_muestra), columns=datos_muestra.columns)
        
        # KMEANS
        kmeans = KmeansObjetos.Kmeans(n_clusters=4, iteraciones=300, datos=datos_entrenamiento)
        kmeans.Kmeans(datos_entrenamiento)
        clusters = kmeans.clusters
        
        # ANÁLISIS
        analizador = analisis_kmeans.Analizador_kmeans()
        clusters2= analizador.nombres_cluster2(clusters, datos_entrenamiento, etiquetas_entrenamiento)
        numeros_cl_cajas = kmeans.predecir_cluster(datos_muestra)
        for i in range(len(datos_muestra)):
            datos_muestra.loc[i, 'nombre'] = clusters2[numeros_cl_cajas[i]-1]["name"]
            #print("Muestra", i, ":", datos_muestra.loc[i, 'nombre'])
        muestras_clasificadas = datos_muestra.loc[:, 'nombre']      # obtengo la clase de cada muestra
        #transformo a lista
        muestras_clasificadas = muestras_clasificadas.values.tolist()
        return muestras_clasificadas

    def knn_agente(self, datos_entrenamiento, datos_muestra):
        # Obtener las características y las etiquetas
        caracteristicas = datos_entrenamiento.drop('nombre', axis=1)
        etiquetas = datos_entrenamiento['nombre']


        #caracteristicas RELEVANTES
        columnas_eliminar = ['momento1', 'momento3', 'momento4', 'momento5', 'momento6', 'momento7', 'momento2']
        caracteristicas = caracteristicas.drop(columnas_eliminar, axis=1)
        datos_muestra = datos_muestra.drop(columnas_eliminar, axis=1)

        muestras_clasificadas = []
        knn = KnnObjetos.Knn(caracteristicas, etiquetas, k=5)

        for i in range(len(datos_muestra)):
            etiqueta_predicha = knn.predecir(datos_muestra.iloc[i, :])
            muestras_clasificadas.append(etiqueta_predicha)
            #print(f"La etiqueta predicha para la muestra es: {muestras_clasificadas[i]}")

        return muestras_clasificadas
    
    def planificacion_strips(self, muestras_clasificadas, objetivo):
        # Rutas de los archivos de dominio y problema
        dominio_file = r'D:\Usuarios\martin\documents\FACULTAD\Inteligencia Artificial\EXÁMEN FINAL\Dominio.pddl'
        problema_file = r'D:\Usuarios\martin\documents\FACULTAD\Inteligencia Artificial\EXÁMEN FINAL\Problema.pddl'
        plan = Planificador(dominio_file, problema_file)
        plan.generar_archivo_problema(muestras_clasificadas, objetivo)
        exito = plan.ejecutar_planificacion()
        if exito:
            print("Planificación realizada con éxito")
            muestras_clasificadas = objetivo
        else:
            print("Error en la planificación")
            return muestras_clasificadas

        return objetivo
    
    def obtener_orden_objetivo(self):
        caja_objetivo = []
        nombres_cajas = ["arandela", "clavo", "tornillo", "tuerca"]
        print("Ingrese el lugar de cada caja en el orden deseado (de arriba hacia abajo).")
        for i, nombre in enumerate(nombres_cajas, start=1):
            while True:
                lugar = input(f"Lugar de {nombre}? ")
                if not lugar.isdigit():
                    print("Error: El lugar debe ser un número.")
                    continue
                lugar = int(lugar)
                if lugar <= 0:
                    print("Error: El lugar debe ser un número positivo.")
                    continue
                if lugar in caja_objetivo:
                    print("Error: El lugar ingresado ya está ocupado.")
                    continue
                if lugar > len(nombres_cajas):
                    print("Error: El lugar ingresado no existe.")
                    continue
                caja_objetivo.append((nombre, lugar))
                break
        caja_objetivo.sort(key=lambda x: x[1])
        
        return [nombre for nombre, _ in caja_objetivo]

    def transportar_cajas(self, tamaño):
        tamaño = 10
        laberinto = laberintoFINAL.Laberinto(tamaño)
        laberinto.iniciar_laberinto()
        while True:
            print("¿Desea reiniciar el laberinto? (s/n)")
            respuesta = input()
            if respuesta == "s":
                laberinto = laberintoFINAL.Laberinto(tamaño)
                laberinto.iniciar_laberinto()
            else:
                break

    def INICIAR_agente(self):
        nombre_archivo_cajas = 'caracteristicas_cajas.csv'
        carpeta_cajas = "Procesamiento_de_Imagenes/imagenes_cajas"
        self.generar_archivo_caracteristicas(nombre_archivo_cajas, carpeta_cajas, modo=3)
        
        print("-------------------------------------------------------------------------------------")
        print("                          INICIALIZACIÓN DEL AGENTE")
        print("-------------------------------------------------------------------------------------")
        print("Identificando cajas...\n"
              "Seleccione el método de clasificación:\n"
                "1. Knn\n"
                "2. Kmeans")
        metodo = input()

        if metodo == "1":
            muestras = self.knn_agente(self.datos_entrenamiento, self.datos_cajas)
            print("Clasificación efectuada mediante el algoritmo Knn")
            self.orden_inicial = muestras

        elif metodo == "2":
            muestras = self.kMeans_agente(self.datos_entrenamiento, self.datos_cajas)
            print("Clasificación efectuada mediante el algoritmo kMeans")
            self.orden_inicial = muestras

        
        print("El orden de las cajas (de arriba a abajo) es:")
        for i in range(len(muestras)):
            print(i + 1, ":", muestras[i])
        print("")

        objetivo = self.obtener_orden_objetivo()
        print("El objetivo es: ", objetivo)

        self.planificacion_strips(muestras, objetivo)

        tamaño_laberinto = 12
        self.transportar_cajas(tamaño_laberinto)


    def menu_opciones(self):
            while True:
                print("------------------------------------------------------------------------------")
                print("                       MENÚ PRINCIPAL")
                print("------------------------------------------------------------------------------")
                print("Seleccione una opción:")
                print("1. Clasificar imágenes")
                print("2. Planificar")
                print("3. Transportar cajas")
                print("4. Modificar datos")
                print("5. Salir")
                opcion = input()
                print("")

                if opcion == "1":
                    print("Seleccione el método de clasificación:")
                    print("1. Knn")
                    print("2. Kmeans")
                    metodo = input()
                    if metodo == "1":
                        muestras = self.knn_agente(self.datos_entrenamiento, self.datos_muestra)
                        print("Clasificación efectuada mediante el algoritmo Knn")

                    elif metodo == "2":
                        muestras = self.kMeans_agente(self.datos_entrenamiento, self.datos_muestra)
                        print("Clasificación efectuada mediante el algoritmo kMeans")
                    for i in range(len(muestras)):
                        print("La imagen", i + 1, "es: ", muestras[i])

                elif opcion == "2":
                    objetivo = self.obtener_orden_objetivo()
                    print("El objetivo es:", objetivo)
                    self.planificacion_strips(self.orden_inicial, objetivo)

                elif opcion == "3":
                    tamaño_laberinto = 12
                    self.transportar_cajas(tamaño_laberinto)

                elif opcion == "4":
                    print("Seleccione la base de datos a modificar:")
                    print("1. Datos de entrenamiento")
                    print("2. Datos de muestra")
                    print("3. Datos de cajas")
                    datos = input()

                    if datos == "1":
                        print("Modificando datos de entrenamiento...")
                        carpeta = "Procesamiento_de_Imagenes/imagenes"
                        nombre_archivo = 'caracteristicas_imagenes.csv'
                        modo = 1
                        

                    elif datos == "2":
                        print("Modificando datos de muestra...")
                        nombre_archivo = 'caracteristicas_muestras.csv'
                        carpeta = "Procesamiento_de_Imagenes/imagenes_muestra"
                        modo = 2

                    elif datos == "3":
                        print("Modificando datos de cajas...")
                        nombre_archivo = 'caracteristicas_cajas.csv'
                        carpeta = "Procesamiento_de_Imagenes/imagenes_cajas"
                        modo = 3
                    
                    self.generar_archivo_caracteristicas(nombre_archivo, carpeta, modo=modo)

                elif opcion == "5":
                    print("Saliendo del programa...")
                    break

                else:
                    print("Opción inválida. Intente nuevamente.")




agente1 = Agente(
    r'D:\Usuarios\martin\documents\FACULTAD\Inteligencia Artificial\EXÁMEN FINAL\Procesamiento_de_imagenes\caracteristicas_imagenes.csv',
    r'D:\Usuarios\martin\documents\FACULTAD\Inteligencia Artificial\EXÁMEN FINAL\Procesamiento_de_imagenes\caracteristicas_muestras.csv',
    r'D:\Usuarios\martin\documents\FACULTAD\Inteligencia Artificial\EXÁMEN FINAL\Procesamiento_de_imagenes\caracteristicas_cajas.csv'
)

agente1.INICIAR_agente()
print("Finalizó la inicialización del agente")
agente1.menu_opciones()
print("Finalizó el programa")

"""
SIN USAR EL METODO INICIAR_AGENTE:

nombre_archivo_cajas = 'caracteristicas_cajas.csv'
carpeta_cajas = "Procesamiento_de_Imagenes/imagenes_cajas"
agente1.generar_archivo_caracteristicas(nombre_archivo_cajas, carpeta_cajas, modo=3) #Sobreescribe el archivo de características de cajas


muestras_Kmeans = agente1.kMeans_agente(agente1.datos_entrenamiento, agente1.datos_muestra)
print("Clasificación por kMeans: ", muestras_Kmeans)

muestras_Knn = agente1.knn_agente(agente1.datos_entrenamiento, agente1.datos_cajas)
print("Clasificación por Knn: ", muestras_Knn)

#ORDEN DE LAS CAJAS
print("El orden de las cajas (de arriba a abajo) es:")
for i in range(len(muestras_Knn)):
    print(i+1, ":", muestras_Knn[i])

#PLANIFICACIÓN DE STRIPS
objetivo = agente1.obtener_orden_objetivo()
print("El objetivo es: ", objetivo)

agente1.planificacion_strips(muestras_Knn, objetivo)

#TRANSPORTAR CAJAS
agente1.transportar_cajas(12)
"""