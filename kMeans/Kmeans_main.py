from KmeansObjetos import*
import pandas as pd
from analisis_kmeans import*
from sklearn.preprocessing import MinMaxScaler
import time
from sklearn.metrics import confusion_matrix

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

lista_global =[]
lista_arandela = []
lista_tornillo = []
lista_clavo = []
lista_tuerca = []
lista_tiempo = []

#print("Datos de entrenamiento:\n", datos_entrenamiento)
print("Datos de muestra:\n", datos_muestra)
for p in range(1):
    inicio = time.time()
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
    #precision = analizador.calcular_precision(datos_entrenamiento, clusters2, etiquetas_entrenamiento)
    #print("Precisión del algoritmo K-means:", precision)


    # predicción de la muestra

    numeros_cl_muestra = kmeans.predecir_cluster(datos_muestra)
    #print("Los números de cluster de las muestras son:", numeros_cl_muestra)
    #asigno el nombre del cluster correspondiente a cada muestra
    for i in range(len(datos_muestra)):
        datos_muestra.loc[i, 'nombre'] = clusters2[numeros_cl_muestra[i]-1]['name']
        print("La imagen", i, "de muestra es:", datos_muestra.loc[i, 'nombre'])

    fin = time.time()
    t_ejecucion =round(fin - inicio, 2)
    print("Tiempo de ejecución:", t_ejecucion)

    etiquetas_esperadas =["clavo", "arandela", "tuerca", "clavo", "tuerca", "tornillo"]
    esperadas_esperadas = pd.DataFrame(etiquetas_esperadas, columns=['nombre'])

    # GRÁFICA
    graficadora = Graficadora_kmeans(kmeans, datos_entrenamiento)
    graficadora.graficar_kmeans(componentes_principales=3)


    matriz_confusion = confusion_matrix(etiquetas_esperadas, datos_muestra['nombre'])

    # Cálculo de la Precisión Global (Accuracy)
    precision_global = (matriz_confusion[0, 0] + matriz_confusion[1, 1] + matriz_confusion[2, 2] + matriz_confusion[3, 3]) / matriz_confusion.sum()

    # Cálculo de la Precisión por Categoría
    precision_arandela = matriz_confusion[0, 0] / matriz_confusion[0, :].sum()
    precision_tornillo = matriz_confusion[1, 1] / matriz_confusion[1, :].sum()
    precision_clavo = matriz_confusion[2, 2] / matriz_confusion[2, :].sum()
    precision_tuerca = matriz_confusion[3, 3] / matriz_confusion[3, :].sum()

    # Resultados
    print("Matriz de Confusión:")
    print(matriz_confusion)
    print("Precision Global (Accuracy): {:.2f}".format(precision_global))
#    print("Precisión por Categoría:")
    print("Arandela: {:.2f}".format(precision_arandela))
    print("Tornillo: {:.2f}".format(precision_tornillo))
    print("Clavo: {:.2f}".format(precision_clavo))
    print("Tuerca: {:.2f}".format(precision_tuerca))
    print("")
    print("")

    lista_global.append(precision_global)
    lista_arandela.append(precision_arandela)
    lista_tornillo.append(precision_tornillo)
    lista_clavo.append(precision_clavo)
    lista_tuerca.append(precision_tuerca)
    lista_tiempo.append(t_ejecucion)

    

#Calculo de precisiones promedio
promedio_global = sum(lista_global)/len(lista_global)
promedio_arandela = sum(lista_arandela)/len(lista_arandela)
promedio_tornillo = sum(lista_tornillo)/len(lista_tornillo)
promedio_clavo = sum(lista_clavo)/len(lista_clavo)
promedio_tuerca = sum(lista_tuerca)/len(lista_tuerca)
promedio_tiempo = sum(lista_tiempo)/len(lista_tiempo)

data = {
    'Precision arandela': lista_arandela,
    'Precision tornillo': lista_tornillo,
    'Precision clavo': lista_clavo,
    'Precision tuerca': lista_tuerca,
    'Precision global': lista_global,
    'Tiempo de ejecucion': lista_tiempo,
}
#Agrego los promedios como última fila
data['Precision arandela'].append(promedio_arandela)
data['Precision tornillo'].append(promedio_tornillo)
data['Precision clavo'].append(promedio_clavo)
data['Precision tuerca'].append(promedio_tuerca)
data['Precision global'].append(promedio_global)
data['Tiempo de ejecucion'].append(promedio_tiempo)


df = pd.DataFrame(data)
print(df)

#gurado el archivo csv
print("¿Qué lote es?")
lote = input("Ingrese el número de lote: ")
df.to_csv('resultados_lote_'+ lote, index=False, sep=';')



