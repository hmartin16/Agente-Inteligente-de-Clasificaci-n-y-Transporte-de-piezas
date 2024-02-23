import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches
from sklearn.decomposition import PCA



#-------------------------------------------------------------------------------------------------------------------------------------------
#                                                      CLASE PARA ALGORITMO KMEANS
#-------------------------------------------------------------------------------------------------------------------------------------------

class Kmeans:
    def __init__(self, n_clusters, iteraciones, datos):
        if n_clusters <= 0:
            raise ValueError('El número de clusters debe ser mayor que cero')
        if iteraciones <= 0:
            raise ValueError('El número de iteraciones debe ser mayor que cero')
        if datos.empty:
            raise ValueError('Los datos de entrada están vacíos')
        self.n_clusters = n_clusters
        self.iteraciones = iteraciones
        self.cant_carac = datos.shape[1]
        self.centroides = []
        self.clusters = [{'centroide': np.zeros(self.cant_carac), 'puntos': []} for i in range(self.n_clusters)]
        self.mejores_resultados = []

    
    def get_centroides(self):
        return self.centroides
    
    def get_clusters(self):
        return self.clusters
    
    #definir los metodos de la clase
    def distancia_euclidiana(self, centroide, punto):
        distancia = np.sqrt(np.sum((centroide - punto)**2)) #distancia euclidiana
        #distancia = np.sum(np.abs(centroide - punto)) #distancia manhattan
        return distancia
    
    def asignar_cluster(self, punto):
        distancias = []
        for centroide in self.centroides:
            distancias.append(self.distancia_euclidiana(centroide, punto))
        cluster = np.argmin(distancias) + 1
        return cluster
    
    def actualizar_centroides(self):
        for i in range(len(self.centroides)):
            puntos = np.array(self.clusters[i]['puntos'])
            if len(puntos) > 0:
                self.centroides[i] = np.mean(puntos, axis=0)
            else:
                pass                                              # si el cluster no tiene puntos asignados, no se actualiza su centroide
    

    def algoritmo_kmeans(self, datos):
        self.centroides_anteriores = np.zeros((self.n_clusters, self.cant_carac))
        self.centroides_actuales = np.array(self.centroides, dtype=object)
        while not np.array_equal(self.centroides_anteriores, self.centroides_actuales):
            self.centroides_anteriores = self.centroides_actuales
            for i in range(len(self.clusters)):
                self.clusters[i]['puntos'] = []
            for i in range(len(datos)):
                punto = datos.iloc[i].to_numpy()
                num_cluster = self.asignar_cluster(punto)
                punto_list = punto.tolist()                              #convierte el punto en una lista para poder agregarlo al cluster
                self.clusters[num_cluster-1]['puntos'].append(punto_list)
            self.actualizar_centroides()
            self.centroides_actuales = np.array(self.centroides)
    

    def predecir_cluster(self, muestra):
        cluster_m = []
        for i in range(len(muestra)):
            cluster_m.append(self.asignar_cluster(muestra.iloc[i].to_numpy()))
        return cluster_m

    
    def Kmeans(self, datos):        
        self.centroides.append(datos.sample(n=1).to_numpy()) #Genero el primer centroide, solo para que no sea vacio
        for i in range(self.iteraciones):
            # Inicializar el primer centroide de manera aleatoria
            self.centroides[0] = datos.sample(n=1).to_numpy()  # Ahora si le asigno un valor para cada iteracion
            
            # Inicializar el resto de los centroides utilizando el método "k-means++"
            distancias = []
            for punto in datos.to_numpy():
                distancias.append(self.distancia_euclidiana(self.centroides[np.argmin([self.distancia_euclidiana(centroide, punto) for centroide in self.centroides])], punto))
            distancias = np.array(distancias)
            distancias = distancias / distancias.sum()
            while len(self.centroides) < self.n_clusters:
                self.centroides.append(datos.to_numpy()[np.random.choice(range(len(datos)), p=distancias)])

            # Ejecutar el algoritmo k-means
            self.algoritmo_kmeans(datos)
            
            # Calcular la suma de las distancias al cuadrado de los puntos a sus centroides
            suma_distancias = 0
            for i in range(len(self.clusters)):
                suma_distancias += sum([self.distancia_euclidiana(self.centroides[i], punto)**2 for punto in self.clusters[i]['puntos']])
            
            # Guardar los mejores resultados
            if len(self.mejores_resultados) == 0:
                self.mejores_resultados = [self.centroides, self.clusters, suma_distancias]
            elif suma_distancias < self.mejores_resultados[2]:
                self.mejores_resultados = [self.centroides, self.clusters, suma_distancias]
            else:
                pass
        
        # Asignar los mejores resultados
        self.centroides = self.mejores_resultados[0]
        self.clusters = self.mejores_resultados[1]
        
        for i in range(len(self.clusters)): #asigna los centroides a los diccionarios de los clusters
            self.clusters[i]['centroide'] = self.centroides[i]




#-------------------------------------------------------------------------------------------------------------------------------------------------
#                                                          CLASE GRAFICADORA KMEANS
#-------------------------------------------------------------------------------------------------------------------------------------------------

class Graficadora_kmeans:
    def __init__(self, kmeans, datos, muestra=None):
        self.kmeans = kmeans
        self.datos = datos
        self.muestra = muestra

    def reducir_dimensiones(self, datos, componentes_principales):
        pca = PCA(componentes_principales)
        datos_reducidos = pca.fit_transform(datos)
        return datos_reducidos

    def graficar_kmeans(self, componentes_principales=2):
        if self.datos.shape[1] == 2:
            self.graficar_2d(self.datos.values)
        elif self.datos.shape[1] == 3:
            if componentes_principales == 2:
                self.graficar_2d(self.datos.values)
            elif componentes_principales == 3:
                self.graficar_3d(self.datos.values)
            else:
                raise ValueError("El número de componentes debe ser 2 o 3.")
        else:
            datos_reducidos = self.reducir_dimensiones(self.datos, componentes_principales)
            muestra_reducida = self.reducir_dimensiones(self.muestra, componentes_principales) if self.muestra is not None else None

            if componentes_principales == 2:
                self.graficar_2d(datos_reducidos, muestra_reducida)
            elif componentes_principales == 3:
                self.graficar_3d(datos_reducidos, muestra_reducida)
            else:
                raise ValueError("El número de componentes debe ser 2 o 3.")

    def graficar_2d(self, datos_reducidos=None, muestra_reducida=None):
        if datos_reducidos is None:
            datos_reducidos = self.datos.values
        if muestra_reducida is None:
            muestra_reducida = self.muestra.values if self.muestra is not None else None

        etiquetas_clusters = self.kmeans.predecir_cluster(self.datos)
        colores = ['red', 'blue', 'green', 'yellow']
        custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colores)

        # Visualizar los datos en el plano
        plt.scatter(datos_reducidos[:, 0], datos_reducidos[:, 1], c=etiquetas_clusters, s=50, cmap=custom_cmap)

        if muestra_reducida is not None:
            etiquetas_muestra = self.kmeans.predecir_cluster(self.muestra)
            print("Etiquetas muestra: ", etiquetas_muestra)
            plt.scatter(muestra_reducida[:, 0], muestra_reducida[:, 1], c=etiquetas_muestra, s=100, cmap=custom_cmap, marker='X')

        # Dibujar cada centroide
        centroides = self.kmeans.centroides
        if self.datos.shape[1] == 2:
            centroides_reducidos = np.array(centroides)
        else:
            centroides_reducidos = self.reducir_dimensiones(pd.DataFrame(centroides), 2)
        plt.scatter(centroides_reducidos[:, 0], centroides_reducidos[:, 1], marker='X', c='black', s=100, label='Centroides')

        plt.xlabel("Componente Principal 1")
        plt.ylabel("Componente Principal 2")
        plt.title("Visualización K-means en 2D")
        plt.legend()
        plt.show()

    def graficar_3d(self, datos_reducidos=None, muestra_reducida=None):
        if datos_reducidos is None:
            datos_reducidos = self.datos.values
        if muestra_reducida is None:
            muestra_reducida = self.muestra.values if self.muestra is not None else None

        etiquetas_clusters = self.kmeans.predecir_cluster(self.datos)
        colores = ['red', 'blue', 'green', 'yellow']
        custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colores)

        # Visualizar los datos en el espacio 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(datos_reducidos[:, 0], datos_reducidos[:, 1], datos_reducidos[:, 2], c=etiquetas_clusters, s=50, cmap=custom_cmap)

        if muestra_reducida is not None:
            etiquetas_muestra = self.kmeans.predecir_cluster(self.muestra)
            ax.scatter(muestra_reducida[:, 0], muestra_reducida[:, 1], muestra_reducida[:, 2], c=etiquetas_muestra, s=100, cmap=custom_cmap, marker='X')

        # Dibujar cada centroide
        centroides = self.kmeans.centroides
        if self.datos.shape[1] == 3:
            centroides_reducidos = np.array(centroides)
        else:
            centroides_reducidos = self.reducir_dimensiones(pd.DataFrame(centroides), 3)
        ax.scatter(centroides_reducidos[:, 0], centroides_reducidos[:, 1], centroides_reducidos[:, 2], marker='X', c='black', s=100, label='Centroides')

        ax.set_xlabel("Componente Principal 1")
        ax.set_ylabel("Componente Principal 2")
        ax.set_zlabel("Componente Principal 3")
        ax.set_title("Visualización K-means en 3D")
        ax.legend()
        plt.show()




#------------------------------------------------------------------------------------------------------------------------------
                                        # MAIN DE PRUEBA CON DATOS DE FUTBOL
#------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
        #DATAFRAME
    Goles = [0, 4, 12, 58, 49, 70, 14, 68, 55, 0, 15, 0, 0, 1, 4, 7, 8, 40]
    Asistencias = [0, 4, 38, 10,  6,  7, 41,  9,  3, 9, 50, 0, 1, 0, 8, 12, 15, 9]
    Robos = [11, 73,  15,  1,  1,  0,  15,  1,  0, 62,  25, 16, 12, 20, 60, 70, 56,  0]
    Despejes = [60,  11,  4,  0,  0,  3,  0,  0,  0,  9,  4,  55,  48,  72,  10,  7,  5,  0]
    Jugadores = ['Marquinhos', 'Casemiro', 'Paquetá', 'Neymar', 'Richarlison', 'Kane', 'Foden', 'Mbappé', 'Lewandowski', 
    'Busquets', 'De Bruyne', 'Pepe', 'Alaba', 'Koulibaly', 'Brozovic', 'Kante', 'Jorginho', 'Gareth Bale']
    datos = pd.DataFrame({'Goles': Goles, 'Asistencias': Asistencias, 'Robos': Robos, 'Despejes': Despejes}, index=Jugadores)
    print("DATAFRAME de datos: \n", datos)  

    #DATAFRAME muestra
    datos_muestra = [[82, 2,  3, 70, 22, 18, 0], [ 3, 1, 10, 11, 42, 34, 8], [0, 17, 67,  0,  7, 10, 65], [0, 62,  9,  0,  1, 0,  10]]
    datos_muestra = np.transpose(datos_muestra)
    nombres_muestra = ['Haaland', 'Ruben Dias', 'Kimmich', 'Benzema', 'Lo Celso', 'Modric', 'Amrabat']
    encabezados_muestra = ['Goles', 'Asistencias', 'Robos', 'Despejes']
    muestra = pd.DataFrame(datos_muestra, index=nombres_muestra, columns=encabezados_muestra)
    print("\nDATAFRAME de muestra", muestra)


    mikmeans = Kmeans(n_clusters=4, iteraciones=150, datos=datos)
    mikmeans.Kmeans(datos)
    micentroides = mikmeans.centroides
    miclusters = mikmeans.clusters

    graficadora = Graficadora_kmeans(mikmeans, datos, muestra)
    graficadora.graficar_kmeans(componentes_principales=3)  # Graficar en 2D

