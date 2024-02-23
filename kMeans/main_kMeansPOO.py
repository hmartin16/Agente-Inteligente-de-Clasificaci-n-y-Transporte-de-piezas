from kMeansPOO import*
import pandas as pd
from analisis_kmeans import*
from sklearn.preprocessing import MinMaxScaler, StandardScaler


np.random.seed(1) # Semilla para reproducibilidad
# DATOS DE ENTRENAMIENTO Y MUESTRA
# Crear una instancia de MinMaxScaler
min_max_scaler = MinMaxScaler()
# Leer los archivos CSV
ruta_datos_entrenamiento = r'D:\Usuarios\martin\documents\FACULTAD\Inteligencia Artificial\Aprender OpenCV\Procesamiento de Imagenes\caracteristicas_imagenes.csv'
ruta_datos_muestra = r'D:\Usuarios\martin\documents\FACULTAD\Inteligencia Artificial\Aprender OpenCV\Procesamiento de Imagenes\caracteristicas_muestras.csv'

datos_entrenamiento = pd.read_csv(ruta_datos_entrenamiento, delimiter=';', decimal='.')
datos_muestra = pd.read_csv(ruta_datos_muestra, delimiter=';', decimal='.')
etiquetas_entrenamiento = datos_entrenamiento['nombre']

datos_entrenamiento = datos_entrenamiento.drop('nombre', axis=1) # elimino la columna nombre
datos_muestra = datos_muestra.drop('nombre', axis=1)
#datos_entrenamiento = pd.DataFrame(min_max_scaler.fit_transform(datos_entrenamiento), columns=datos_entrenamiento.columns) # normalizo los datos
#datos_muestra = pd.DataFrame(min_max_scaler.fit_transform(datos_muestra), columns=datos_muestra.columns)
columnas_eliminar = ['momento1','momento3', 'momento4', 'momento5', 'momento6', 'momento7', 'momento2']  # elimino columnas irrelevantes
datos_entrenamiento = datos_entrenamiento.drop(columnas_eliminar, axis=1)
datos_muestra = datos_muestra.drop(columnas_eliminar, axis=1)
print("datos_entrenamiento:\n", datos_entrenamiento)
print("datos_muestra:\n", datos_muestra)
print("etiquetas_entrenamiento:\n", etiquetas_entrenamiento)

# KMEANS
kmeans = Kmeans(n_clusters=4, iteraciones=10, datos=datos_entrenamiento)
kmeans.Kmeans(datos_entrenamiento)
clusters = kmeans.clusters

for i, cluster in enumerate(clusters):
    print("Puntos del Cluster:", i+1)
    for punto in cluster['puntos']:
        print(punto)

print("\n")

#imprimir los centroides del diccionario clusters
for cluster in clusters:
    print("Cluster:", cluster['centroide'])


# ANÁLISIS
analizador = Analizador_kmeans()

# Llamar al método analizar_clusters para asignar nombres a los clusters
clusters1 = analizador.nombres_cluster1(clusters, datos_entrenamiento, etiquetas_entrenamiento)

# Imprimir los nombres de los clusters
for cluster in clusters1:
    print("Cluster1:", cluster['name'])

print("\n")


clusters2= analizador.nombres_cluster2(clusters, datos_entrenamiento, etiquetas_entrenamiento)
for cluster in clusters2:
    print("Cluster2:", cluster['name'])

# GRÁFICA
graficadora = Graficadora_kmeans(kmeans, datos_entrenamiento)
graficadora.graficar_kmeans(componentes_principales=3)
