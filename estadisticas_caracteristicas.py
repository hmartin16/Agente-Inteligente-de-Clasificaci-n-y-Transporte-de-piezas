import pandas as pd
from scipy.stats import f_oneway
from itertools import combinations

# Cargar el archivo CSV
ruta_datos_entrenamiento = r'D:\Usuarios\martin\documents\FACULTAD\Inteligencia Artificial\Aprender OpenCV\Procesamiento de Imagenes\caracteristicas_imagenes.csv'
data = pd.read_csv(ruta_datos_entrenamiento, delimiter=';', decimal='.')

# Obtener las etiquetas únicas
etiquetas = data['nombre'].unique()

# Crear un DataFrame para almacenar los resultados de las combinaciones específicas
resultados_combinaciones = {}

# Calcular el estadístico y el valor p para todas las combinaciones específicas
for r in range(2, len(etiquetas)+1):
    combinaciones = list(combinations(etiquetas, r))
    for combinacion in combinaciones:
        resultados_combinacion = pd.DataFrame(columns=['Caracteristica', 'Estadistica', 'Valor p'])
        for columna in data.columns:
            if columna != 'nombre':
                grupos = [data[data['nombre'] == etiqueta][columna] for etiqueta in combinacion]
                estadistico, valor_p = f_oneway(*grupos)
                resultados_combinacion = pd.concat([resultados_combinacion, pd.DataFrame({'Caracteristica': [columna], 'Estadistica': [estadistico], 'Valor p': [valor_p]})], ignore_index=True)

        # Ordenar los resultados de la combinación por estadístico y valor p
        resultados_combinacion = resultados_combinacion.sort_values(by=['Estadistica'], ascending=False)

        # Agregar los resultados de la combinación al diccionario
        resultados_combinaciones['-'.join(combinacion)] = resultados_combinacion

# Mostrar resultados para la combinacion de todas las etiquetas
print(f"Para todas las etiquetas:")
print(resultados_combinaciones['-'.join(etiquetas)])
print()

# Mostrar resultados para la combinacion clavo-tornillo
print(f"Para la combinacion clavo-tornillo:")
print(resultados_combinaciones['clavo-tornillo'])
print()

# Mostrar resultados para la combinacion arandela-tuerca
print(f"Para la combinacion arandela-tuerca:")
print(resultados_combinaciones['arandela-tuerca'])
print()

# Mostrar resultados para la combinacion arandela-tornillo
print(f"Para la combinacion arandela-tornillo:")
print(resultados_combinaciones['arandela-tornillo'])
print()

