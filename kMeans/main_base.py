from KmeansObjetos import*
import pandas as pd
from analisis_kmeans import*
from sklearn.preprocessing import MinMaxScaler


min_max_scaler = MinMaxScaler()
# DATOS DE ENTRENAMIENTO Y MUESTRA
# Leer los archivos CSV
ruta_datos_entrenamiento = r'D:\Usuarios\martin\documents\FACULTAD\Inteligencia Artificial\EXÁMEN FINAL\Procesamiento_de_imagenes\caracteristicas_imagenes.csv'
ruta_datos_muestra = r'D:\Usuarios\martin\documents\FACULTAD\Inteligencia Artificial\EXÁMEN FINAL\Procesamiento_de_imagenes\caracteristicas_muestras.csv'

datos_entrenamiento = pd.read_csv(ruta_datos_entrenamiento, delimiter=';', decimal='.')
datos_muestra = pd.read_csv(ruta_datos_muestra, delimiter=';', decimal='.')
etiquetas_entrenamiento = datos_entrenamiento['nombre']

datos_entrenamiento = datos_entrenamiento.drop('nombre', axis=1)                       # elimino la columna nombre
datos_muestra = datos_muestra.drop('nombre', axis=1)                                   # elimino la columna nombre
columnas_eliminar = ['momento1', 'momento3', 'momento4', 'momento5', 'momento6', 'momento7', 'momento2']  # elimino columnas irrelevantes
datos_entrenamiento = datos_entrenamiento.drop(columnas_eliminar, axis=1)
datos_muestra = datos_muestra.drop(columnas_eliminar, axis=1)



# Datos normalizados, da mejor precisión
datos_entrenamiento = pd.DataFrame(min_max_scaler.fit_transform(datos_entrenamiento), columns=datos_entrenamiento.columns) # normalizo los datos
datos_muestra = pd.DataFrame(min_max_scaler.fit_transform(datos_muestra), columns=datos_muestra.columns)


#print("Datos de entrenamiento:\n", datos_entrenamiento)
print("Datos de muestra:\n", datos_muestra)
for p in range(1):
    datos_muestra = pd.read_csv(ruta_datos_muestra, delimiter=';', decimal='.')
    datos_muestra = datos_muestra.drop('nombre', axis=1)
    datos_muestra = datos_muestra.drop(columnas_eliminar, axis=1)
    datos_muestra = pd.DataFrame(min_max_scaler.transform(datos_muestra), columns=datos_muestra.columns)

    # KMEANS
    kmeans = Kmeans(n_clusters=4, iteraciones=300, datos=datos_entrenamiento)
    kmeans.Kmeans(datos_entrenamiento)
    clusters = kmeans.clusters

    # ANÁLISIS
    analizador = Analizador_kmeans()
    clusters2= analizador.nombres_cluster2(clusters, datos_entrenamiento, etiquetas_entrenamiento)
    for cluster in clusters2:
        print("Cluster:", cluster['name'])

    #precisión
    precision = analizador.calcular_precision(datos_entrenamiento, clusters2, etiquetas_entrenamiento)
    print("Precisión del algoritmo K-means:", precision)


    # predicción de la muestra

    numeros_cl_muestra = kmeans.predecir_cluster(datos_muestra)
    #print("Los números de cluster de las muestras son:", numeros_cl_muestra)
    #asigno el nombre del cluster correspondiente a cada muestra
    for i in range(len(datos_muestra)):
        datos_muestra.loc[i, 'nombre'] = clusters2[numeros_cl_muestra[i]-1]['name']
        print("La imagen", i, "de muestra es:", datos_muestra.loc[i, 'nombre'])


    # GRÁFICA
    graficadora = Graficadora_kmeans(kmeans, datos_entrenamiento)
    graficadora.graficar_kmeans(componentes_principales=3)


