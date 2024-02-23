import os
import pandas as pd
from KnnObjetos import*
import time
from sklearn.metrics import confusion_matrix



# Rutas completas de los archivos CSV
ruta_datos_entrenamiento = r'D:\Usuarios\martin\documents\FACULTAD\Inteligencia Artificial\EXÁMEN FINAL\Procesamiento_de_imagenes\caracteristicas_imagenes.csv'
ruta_datos_muestra = r'D:\Usuarios\martin\documents\FACULTAD\Inteligencia Artificial\EXÁMEN FINAL\Procesamiento_de_imagenes\caracteristicas_muestras.csv'

# Cargar los datos_entrenamiento desde el archivo CSV
datos_entrenamiento = pd.read_csv(ruta_datos_entrenamiento, delimiter=';', decimal='.')
# Obtener las características y las etiquetas
caracteristicas = datos_entrenamiento.drop('nombre', axis=1)
etiquetas = datos_entrenamiento['nombre']

datos_muestra = pd.read_csv(ruta_datos_muestra, delimiter=';', decimal='.')
#print("muestra:\n", datos_muestra)


#caracteristicas RELEVANTES
columnas_eliminar = ['momento1', 'momento3', 'momento4', 'momento5', 'momento6', 'momento7', 'momento2']
caracteristicas = caracteristicas.drop(columnas_eliminar, axis=1)
datos_muestra = datos_muestra.drop(columnas_eliminar, axis=1)
#print("caracteristicas:\n", caracteristicas)

etiquetas_muestra = []
knn = Knn(caracteristicas, etiquetas, k=5)
inicio = time.time()

for i in range(len(datos_muestra)):
    etiqueta_predicha = knn.predecir(datos_muestra.iloc[i, :])
    etiquetas_muestra.append(etiqueta_predicha)
    print(f"La etiqueta predicha para la muestra es: {etiquetas_muestra[i]}")

# Actualizar el dataframe reemplazando los valores de la columna nombre por los valores de etiquetas_muestra
datos_muestra['nombre'] = etiquetas_muestra
print("muestra_clasificada:\n", datos_muestra)

fin = time.time()
tiempo_total = fin - inicio

etiquetas_esperadas =["clavo", "arandela", "tuerca", "clavo", "tuerca", "tornillo"]
esperadas_esperadas = pd.DataFrame(etiquetas_esperadas, columns=['nombre'])


# Cálculo de la matriz de confusión
matriz_confusion = confusion_matrix(esperadas_esperadas, etiquetas_muestra)

# Cálculo de la Precisión Global (Accuracy)
precision_global = np.diagonal(matriz_confusion).sum() / matriz_confusion.sum()

# Cálculo de la Precisión por Categoría
precision_arandela = matriz_confusion[0, 0] / matriz_confusion[0, :].sum()
precision_tornillo = matriz_confusion[1, 1] / matriz_confusion[1, :].sum()
precision_clavo = matriz_confusion[2, 2] / matriz_confusion[2, :].sum()
precision_tuerca = matriz_confusion[3, 3] / matriz_confusion[3, :].sum()

# Resultados
print("Matriz de Confusión:")
print(matriz_confusion)
print("Precision Global (Accuracy): {:.2f}".format(precision_global))
print("Precision arandela: {:.2f}".format(precision_arandela))
print("Precision tornillo: {:.2f}".format(precision_tornillo))
print("Precision clavo: {:.2f}".format(precision_clavo))
print("Precision tuerca: {:.2f}".format(precision_tuerca))
print("Tiempo de ejecucion: {:.6f} segundos".format(tiempo_total))

