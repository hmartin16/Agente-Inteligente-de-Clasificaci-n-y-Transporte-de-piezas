import pandas as pd
import numpy as np
#from KmeansObjetos import* #para ejecutar EL AGENTE descomentar esta linea y comentar la siguiente
from kMeans import KmeansObjetos    # para hacer pruebas desde Kmeans_main.py descomentar esta linea y comentar la anterior
class Analizador_kmeans:
    def __init__(self):
        pass

    def nombres_cluster1(self, clusters, datos_entrenamiento, etiquetas_entrenamiento):
        etiquetas_cluster = []  # Lista de etiquetas de cada cluster

        # Recorrer cada cluster en la lista de clusters
        for i, cluster in enumerate(clusters):
            etiquetas_cluster.append([])  # Agregar una lista vacía para las etiquetas de cada cluster
            
            # Recorrer cada punto del cluster
            for punto in cluster['puntos']:
                # Obtener el índice del punto en el DataFrame original
                indice = datos_entrenamiento.index[datos_entrenamiento.apply(lambda x: x.tolist() == punto, axis=1)].tolist()[0]
                etiqueta = etiquetas_entrenamiento[indice]    # Obtener la etiqueta correspondiente al índice
                etiquetas_cluster[i].append(etiqueta)         # Agregar la etiqueta a la lista del cluster actual

        etiquetas_cluster_representativas = []  # Lista con la etiqueta representativa de cada cluster

        # Recorrer cada cluster en la lista de etiquetas_cluster
        for cluster_etiquetas in etiquetas_cluster:
            # Contar la cantidad de veces que aparece cada etiqueta en el cluster
            conteo_etiquetas = {}
            for etiqueta in cluster_etiquetas:
                if etiqueta in conteo_etiquetas:
                    conteo_etiquetas[etiqueta] += 1
                else:
                    conteo_etiquetas[etiqueta] = 1
            
            # Obtener la etiqueta más común (la de mayor conteo)
            etiqueta_mas_comun = max(conteo_etiquetas, key=conteo_etiquetas.get)
            
            # Agregar la etiqueta representativa a la lista de etiquetas_cluster_representativas
            etiquetas_cluster_representativas.append(etiqueta_mas_comun)

        # Asignar las etiquetas_cluster_representativas a la lista de clusters
        for i, cluster in enumerate(clusters):
            cluster['name'] = etiquetas_cluster_representativas[i]

        return clusters

    # Asignar nombres a los clusters a partir de los nombres de los puntos más cercanos al centroide
    def nombres_cluster2(self, clusters, datos_entrenamiento, etiquetas_entrenamiento):
        etiquetas_cluster_representativas = []

        for cluster in clusters:
            centroide = cluster['centroide']
            distancias = []

            for punto in cluster['puntos']:
                distancia = np.sqrt(np.sum((centroide - punto)**2))
                distancias.append((punto, distancia))

            # Ordenar las distancias de manera ascendente
            distancias.sort(key=lambda x: x[1])

            etiquetas_puntos_cercanos = []
            for punto, _ in distancias[:5]:  # Seleccionar los tres puntos más cercanos
                indice = datos_entrenamiento.index[datos_entrenamiento.apply(lambda x: x.tolist() == punto, axis=1)].tolist()[0]
                etiqueta = etiquetas_entrenamiento[indice]
                etiquetas_puntos_cercanos.append(etiqueta)

            # Obtener la etiqueta más repetida
            etiqueta_representativa = max(etiquetas_puntos_cercanos, key=etiquetas_puntos_cercanos.count)
            etiquetas_cluster_representativas.append(etiqueta_representativa)
            #print("Etiquetas de puntos cercanos:", etiquetas_puntos_cercanos)
            #print()
            #print("Etiqueta representativa:", etiqueta_representativa)
            #print()

        for i, cluster in enumerate(clusters):
            cluster['name'] = etiquetas_cluster_representativas[i]

        return clusters



    def calcular_precision(self, datos_entrenamiento, clusters, etiquetas_entrenamiento):

        #mapear los puntos de datos con sus etiquetas
        indice_etiqueta = {}
        for cluster in clusters:
            etiqueta_cluster = cluster['name']
            puntos_cluster = cluster['puntos']
            for i, punto in enumerate(puntos_cluster):
                indice = datos_entrenamiento.index[datos_entrenamiento.eq(punto).all(axis=1)]
                indice_etiqueta[indice[0]] = etiqueta_cluster

        datos_con_etiqueta = datos_entrenamiento.copy()
        datos_con_etiqueta['etiqueta_cluster'] = [indice_etiqueta.get(i) for i in range(len(datos_entrenamiento))]

        # Cálculo de la precisión
        precision = sum(etiquetas_entrenamiento[i] == indice_etiqueta.get(i) for i in range(len(datos_entrenamiento)))
        precision /= len(datos_entrenamiento)

        return precision


