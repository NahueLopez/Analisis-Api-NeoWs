from dbConnec import establecer_conexion, crear_tabla_dinamica, insertar_datos, verificar_tabla_existente
from apiData import obtener_datos
from DatosExcel import Verificacion_Excel, insertar_datos_csv

def analizar_json_neo(data):
    # Analizo el JSON de datos de asteroides de la api y guardo los valores relevantes para cada asteroide
    all_values = []
    near_earth_objects = data.get('near_earth_objects', {})

    for fecha, asteroids in near_earth_objects.items():
        for asteroid in asteroids:
            close_approach_data = asteroid.get('close_approach_data', [])
            if close_approach_data:
                values = {
                    'id': asteroid.get('neo_reference_id', None),
                    'name': asteroid.get('name', None),
                    'nasa_jpl_url': asteroid.get('nasa_jpl_url', None),
                    'absolute_magnitude_h': asteroid.get('absolute_magnitude_h', None),
                    'relative_velocity': close_approach_data[0]['relative_velocity'].get('kilometers_per_hour', None),
                    'miss_distance': close_approach_data[0]['miss_distance'].get('kilometers', None),
                    'estimated_diameter_min_kilometers': asteroid['estimated_diameter']['kilometers'].get(
                        'estimated_diameter_min', None),
                    'estimated_diameter_max_kilometers': asteroid['estimated_diameter']['kilometers'].get(
                        'estimated_diameter_max', None),
                    'fecha_emision': fecha
                }
                all_values.append(values)
    return all_values

def main():
    # Establecer la conexión
    conn = establecer_conexion()

    if conn is not None:
        try:
            # Verificar si la tabla existe sino la creo
            tabla = 'tabla_asteroides'
            if not verificar_tabla_existente(conn, tabla):
                crear_tabla_dinamica(conn, tabla)

            # Obtener los datos de la API
            data = obtener_datos()

            # Insertar los datos en la base de datos
            if data:
                values_list = analizar_json_neo(data)
                insertar_datos(conn, tabla, values_list)

                # Verifica si el archivo Excel Esta creado,sino lo crea
                Verificacion_Excel("Asteroides.csv")
                # Inserta los datos en el Excel
                insertar_datos_csv("Asteroides.csv", values_list)

            else:
                print("No se pudieron obtener datos de la API NEO de la NASA.")
        finally:
            # Cerrar la conexión
            conn.close()

if __name__ == "__main__":
    main()

