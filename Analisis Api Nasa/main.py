from dbConnec import establecer_conexion, crear_tabla_dinamica, insertar_datos, verificar_tabla_existente
from apiData import obtener_datos


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
    conn = establecer_conexion()

    if conn is not None:
        # Verifico si la tabla existe sino la creo
        tabla = 'tabla_asteroides'
        keys = ['id', 'name', 'nasa_jpl_url', 'absolute_magnitude_h', 'close_approach_date', 'relative_velocity', 'miss_distance', 'estimated_diameter_min_kilometers', 'estimated_diameter_max_kilometers']
        if not verificar_tabla_existente(conn, tabla):
            crear_tabla_dinamica(conn, tabla)

        # Obtengo los datos de la api
        data = obtener_datos()

        # Inserto los datos en la db
        if data:
            values_list = analizar_json_neo(data)
            insertar_datos(conn, tabla, values_list)
            print("Datos insertados correctamente.")
        else:
            print("No se pudieron obtener datos de la API NEO de la NASA.")

if __name__ == "__main__":
    main()

