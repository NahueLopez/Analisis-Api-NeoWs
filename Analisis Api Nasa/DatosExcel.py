import os
import pandas as pd
from datetime import date

def Verificacion_Excel(nombre_archivo):
    if not os.path.isfile(nombre_archivo):
        # Definir las columnas
        columnas = [
            'id', 'fecha_creacion', 'fecha_emision', 'name',
            'nasa_jpl_url', 'absolute_magnitude_h',
            'relative_velocity', 'miss_distance',
            'estimated_diameter_min_kilometers', 'estimated_diameter_max_kilometers'
        ]
        # Crea un DataFrame con las columnas
        df = pd.DataFrame(columns=columnas)
        # Guardar el DataFrame en un archivo CSV con el delimitador
        df.to_csv(nombre_archivo, index=False, sep=';')
        print(f"Archivo '{nombre_archivo}' creado exitosamente con títulos de columnas.")
    else:
        print(f"El archivo '{nombre_archivo}' ya existe.")

def insertar_datos_csv(nombre_archivo, values_list):
    # Leer el archivo CSV existente
    df_existente = pd.read_csv(nombre_archivo, sep=';')

    # Verificar que la columna 'fecha_emision' existe en el DataFrame
    if 'fecha_emision' not in df_existente.columns:
        raise ValueError("La columna 'fecha_emision' no existe en el archivo CSV.")

    # Agregar la fecha actual al campo 'fecha_creacion' para cada nuevo dato
    for row in values_list:
        row['fecha_creacion'] = date.today().strftime('%Y-%m-%d')

    # Filtrar los datos que no están en el archivo existente
    nuevos_datos = [row for row in values_list if row['fecha_emision'] not in df_existente['fecha_emision'].values]

    if nuevos_datos:
        # Convertir la lista de nuevas filas en un DataFrame
        nuevos_datos = pd.DataFrame(nuevos_datos, columns=df_existente.columns)
        # Concatenar el DataFrame existente con las nuevas filas
        df_actualizado = pd.concat([df_existente, nuevos_datos], ignore_index=True)
        # Guardar el DataFrame actualizado en el archivo CSV con el delimitador
        df_actualizado.to_csv(nombre_archivo, index=False, sep=';')
        print(f"Nuevos datos agregados al archivo '{nombre_archivo}'.")
    else:
        print("No hay datos nuevos que agregar.")
