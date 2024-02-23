import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches


class Knn:
    def __init__(self, datos, etiquetas, k):
        self.datos = datos
        self.k = k
        self.distancias = []
        self.etiquetas = etiquetas

    def distancia_euclidiana(self, x1, x2):
        distancia = np.sqrt(np.sum((x2 - x1)**2))  # Distancia euclidiana
        return distancia

    def calcular_distancias(self, x):
        self.distancias = []
        for i in range(len(self.datos)):
            dist = self.distancia_euclidiana(x, self.datos.iloc[i, :-1])  # Distancia entre x y cada punto de datos
            self.distancias.append((dist, i))  # Guardar distancia y el índice del punto de datos
        self.distancias.sort()  # Ordenar las distancias de menor a mayor
        return self.distancias

    def votacion(self):
        etiquetas = []
        for i in range(self.k):
            etiquetas.append(self.etiquetas[self.distancias[i][1]])  # Obtener la etiqueta del vecino más cercano
        etiqueta_votada = max(set(etiquetas), key=etiquetas.count)  # Etiqueta más frecuente en los k vecinos
        return etiqueta_votada
    
    def predecir(self, x):
        self.calcular_distancias(x)
        etiqueta = self.votacion()
        return etiqueta




class Graficadora:
    def __init__(self, datos, etiquetas, muestra=None, etiquetas_muestra=None):
        self.datos = datos
        self.etiquetas = etiquetas
        self.muestra = muestra
        self.etiquetas_muestra = etiquetas_muestra

    def reducir_dimensiones(self, datos, componentes_principales):
        datos_numericos = datos.select_dtypes(include=[np.number]) # Seleccionar solo las columnas numéricas
        pca = PCA(componentes_principales)
        datos_reducidos = pca.fit_transform(datos_numericos)
        return datos_reducidos

    def graficar_datos(self, componentes_principales=2):
        if self.datos.shape[1] == 2:
            self.graficar_2d()
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

        etiquetas_unicas = list(set(self.etiquetas))
        colores = {etiquetas_unicas[0]: 'blue', etiquetas_unicas[1]: 'green',
                   etiquetas_unicas[2]: 'red', etiquetas_unicas[3]: 'yellow'}
        custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', list(colores.values()))
        etiquetas_colores = [colores[etiqueta] for etiqueta in self.etiquetas]

        scatter = plt.scatter(datos_reducidos[:, 0], datos_reducidos[:, 1], c=etiquetas_colores, cmap=custom_cmap)

        if muestra_reducida is not None:
            for i, muestra in enumerate(muestra_reducida):
                etiqueta_muestra = self.etiquetas_muestra[i]
                etiqueta_color = colores[etiqueta_muestra]
                plt.scatter(
                    muestra[0], muestra[1], marker='x', s=100,
                    c=etiqueta_color, label=f"Muestra {i+1} ({etiqueta_muestra})"
                )

            plt.scatter([], [], marker='x', s=100, color='black', label='Punto de muestra')

        plt.xlabel("Componente Principal 1")
        plt.ylabel("Componente Principal 2")
        plt.title("Visualización en 2D")

        handles = [mpatches.Patch(color=color, label=etiqueta) for etiqueta, color in colores.items()]
        etiquetas_legend = [etiqueta for etiqueta in etiquetas_unicas]

        handles = [handle for etiqueta in etiquetas_legend for handle in handles if handle.get_label() == etiqueta]
        etiquetas_legend = [etiqueta for etiqueta in etiquetas_legend if etiqueta in [handle.get_label() for handle in handles]]

        plt.legend(handles, etiquetas_legend, facecolor='white', labelcolor='black')
        plt.show()

    def graficar_3d(self, datos_reducidos=None, muestra_reducida=None):
        if datos_reducidos is None:
            datos_reducidos = self.datos.values
        if muestra_reducida is None:
            muestra_reducida = self.muestra.values if self.muestra is not None else None

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        etiquetas_unicas = list(set(self.etiquetas))
        colores = { etiquetas_unicas[0]: 'blue', etiquetas_unicas[1]: 'green',
                   etiquetas_unicas[2]: 'red', etiquetas_unicas[3]: 'yellow'}
        custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', list(colores.values()))
        etiquetas_colores = [colores[etiqueta] for etiqueta in self.etiquetas]

        scatter = ax.scatter(datos_reducidos[:, 0], datos_reducidos[:, 1], datos_reducidos[:, 2], c=etiquetas_colores, cmap=custom_cmap)

        if muestra_reducida is not None:
            for i, muestra in enumerate(muestra_reducida):
                etiqueta_muestra = self.etiquetas_muestra[i]
                etiqueta_color = colores[etiqueta_muestra]
                ax.scatter(
                    muestra[0], muestra[1], muestra[2], marker='x', s=100,
                    c=etiqueta_color, label=f"Muestra {i+1} ({etiqueta_muestra})"
                )

            ax.scatter([], [], [], marker='x', s=100, color='black', label='Punto de muestra')

        ax.set_xlabel("Componente Principal 1")
        ax.set_ylabel("Componente Principal 2")
        ax.set_zlabel("Componente Principal 3")
        ax.set_title("Visualización en 3D")

        handles = [mpatches.Patch(color=color, label=etiqueta) for etiqueta, color in colores.items()]
        etiquetas_legend = [etiqueta for etiqueta in etiquetas_unicas]

        handles = [handle for etiqueta in etiquetas_legend for handle in handles if handle.get_label() == etiqueta]
        etiquetas_legend = [etiqueta for etiqueta in etiquetas_legend if etiqueta in [handle.get_label() for handle in handles]]

        ax.legend(handles, etiquetas_legend)
        plt.show()







if __name__ == '__main__':
    # Datos de entrenamiento
    Goles = [0, 4, 12, 58, 49, 70, 14, 68, 55, 0, 15, 0, 0, 1, 4, 7, 8, 40]
    Asistencias = [0, 4, 38, 10,  6,  7, 41,  9,  3, 9, 50, 0, 1, 0, 8, 12, 15, 9]
    Robos = [11, 73,  15,  1,  1,  0,  15,  1,  0, 62,  25, 16, 12, 20, 60, 70, 56,  0]
    Despejes = [60,  11,  4,  0,  0,  3,  0,  0,  0,  9,  4,  55,  48,  72,  10,  7,  5,  0]
    Jugadores = ['Marquinhos', 'Casemiro', 'Paquetá', 'Neymar', 'Richarlison', 'Kane', 'Foden', 'Mbappé', 'Lewandowski', 
    'Busquets', 'De Bruyne', 'Pepe', 'Alaba', 'Koulibaly', 'Brozovic', 'Kante', 'Jorginho', 'Gareth Bale']
    datos_entrenamiento = pd.DataFrame({'Goles': Goles, 'Asistencias': Asistencias, 'Robos': Robos, 'Despejes': Despejes}, index=Jugadores)
    etiquetas = ["Defensor", "Mediocampista defensivo", "Mediocampista ofensivo", "Delantero", "Delantero", "Delantero", "Mediocampista ofensivo", "Delantero", "Delantero", "Mediocampista defensivo", "Mediocampista ofensivo", "Defensor", "Defensor", "Defensor", "Mediocampista defensivo", "Mediocampista defensivo", "Mediocampista defensivo", "Delantero"]
    datos_entrenamiento['Etiquetas'] = etiquetas

    # Datos de muestra
    datos_muestra = [[82, 2,  3, 70, 22, 18, 0], [ 3, 1, 10, 11, 42, 34, 3], [0, 17, 67,  0,  7, 10, 56], [0, 62,  9,  0,  1, 0,  12]]
    datos_muestra = np.transpose(datos_muestra)
    nombres_muestra = ['Haaland', 'Ruben Dias', 'Kimmich', 'Benzema', 'Lo Celso', 'Modric', 'Amrabat']
    encabezados_muestra = ['Goles', 'Asistencias', 'Robos', 'Despejes']
    muestra = pd.DataFrame(datos_muestra, index=nombres_muestra, columns=encabezados_muestra)

    # Crear objeto Knn con los datos de entrenamiento y etiquetas
    k = 3
    knn = Knn(datos_entrenamiento, datos_entrenamiento['Etiquetas'], k)
    print("Datos muestra:\n", muestra)
    # Clasificar los datos de muestra
    etiquetas_muestra = []
    for i in range(len(muestra)):
        dato = muestra.iloc[i, :]
        etiqueta_predicha = knn.predecir(dato)
        etiquetas_muestra += [etiqueta_predicha]
        print("", nombres_muestra[i], "es:", etiquetas_muestra[i])

    # Graficar datos de entrenamiento
    graficadora = Graficadora(datos_entrenamiento, datos_entrenamiento['Etiquetas'], muestra, etiquetas_muestra)
    graficadora.graficar_datos(componentes_principales=3)  # Visualización en 2D
    print("fin")