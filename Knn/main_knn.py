import os
import pandas as pd
from KnnObjetos import*



# Rutas completas de los archivos CSV
ruta_datos_entrenamiento = r'D:\Usuarios\martin\documents\FACULTAD\Inteligencia Artificial\Aprender OpenCV\Procesamiento de Imagenes\caracteristicas_imagenes.csv'
ruta_datos_muestra = r'D:\Usuarios\martin\documents\FACULTAD\Inteligencia Artificial\Aprender OpenCV\Procesamiento de Imagenes\caracteristicas_muestras.csv'

# Cargar los datos_entrenamiento desde el archivo CSV
datos_entrenamiento = pd.read_csv(ruta_datos_entrenamiento, delimiter=';', decimal='.')
# Obtener las características y las etiquetas
caracteristicas = datos_entrenamiento.drop('nombre', axis=1)
etiquetas = datos_entrenamiento['nombre']

datos_muestra = pd.read_csv(ruta_datos_muestra, delimiter=';', decimal='.')
print("muestra:\n", datos_muestra)


#caracteristicas RELEVANTES
columnas_eliminar = ['momento1', 'momento3', 'momento4', 'momento5', 'momento6', 'momento7', 'momento2']
caracteristicas = caracteristicas.drop(columnas_eliminar, axis=1)
datos_muestra = datos_muestra.drop(columnas_eliminar, axis=1)
print("caracteristicas:\n", caracteristicas)

etiquetas_muestra = []
knn = Knn(caracteristicas, etiquetas, k=5)

for i in range(len(datos_muestra)):
    etiqueta_predicha = knn.predecir(datos_muestra.iloc[i, :])
    etiquetas_muestra.append(etiqueta_predicha)
    print(f"La etiqueta predicha para la muestra es: {etiquetas_muestra[i]}")

# Actualizar el dataframe reemplazando los valores de la columna nombre por los valores de etiquetas_muestra
datos_muestra['nombre'] = etiquetas_muestra
print("muestra_clasificada:\n", datos_muestra)

# Crear una instancia de la clase Graficadora
graficadora = Graficadora(caracteristicas, etiquetas, muestra=datos_muestra, etiquetas_muestra=etiquetas_muestra)
# Graficar los datos en 2D o 3D según corresponda
#graficadora.graficar_datos(componentes_principales=3)


