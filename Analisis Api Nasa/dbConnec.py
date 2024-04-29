import psycopg2
from psycopg2 import OperationalError
from dbKey import DB_NAME, HOST, PORT, USER, PASSWORD

def establecer_conexion():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD
        )
        print("Conectado a Redshift con éxito!")
        return conn

    except OperationalError as e:
        print(f'Error al establecer la conexión: {e}')
        return None

def verificar_tabla_existente(conn, table_name):
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');")
            exists = cur.fetchone()[0]
            return exists
    except Exception as e:
        print(f"Error al verificar la existencia de la tabla {table_name}: {e}")
        return False

def crear_tabla_dinamica(conn, tabla):
    try:
        cur = conn.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {tabla} ("
                    f"id VARCHAR(255) PRIMARY KEY,"
                    f"fecha_emision DATE,"
                    f"name VARCHAR(255),"
                    f"nasa_jpl_url VARCHAR(255),"
                    f"absolute_magnitude_h FLOAT,"
                    f"relative_velocity FLOAT,"
                    f"miss_distance FLOAT,"
                    f"estimated_diameter_min_kilometers FLOAT,"
                    f"estimated_diameter_max_kilometers FLOAT"
                    ");")
        conn.commit()
        print(f"Tabla '{tabla}' creada correctamente.")
    except Exception as e:
        print(f"Error al crear la tabla: {e}")



def insertar_datos(conn, tabla, values_list):
    try:
        with conn.cursor() as cur:
            for asteroid in values_list:
                keys = list(asteroid.keys())
                placeholders = ', '.join(['%s' for _ in range(len(keys))])
                query = f"INSERT INTO {tabla} ({', '.join(keys)}) VALUES ({placeholders});"
                values = [asteroid[key] for key in keys]
                cur.execute(query, values)
        conn.commit()
        print("Datos insertados correctamente.")
    except Exception as e:
        print(f"Error al insertar datos en la tabla {tabla}: {e}")




