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
            # Verifica si la tabla ya existe en la base de datos
            cur.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');")
            exists = cur.fetchone()[0]
            return exists
    except Exception as e:
        print(f"Error al verificar la existencia de la tabla {table_name}: {e}")
        return False

def crear_tabla_dinamica(conn, tabla):
    try:
        # Define las columnas de la tabla
        columnas = {
            'id': 'VARCHAR(255) PRIMARY KEY',
            'fecha_creacion': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            'fecha_emision': 'DATE',
            'name': 'VARCHAR(255)',
            'nasa_jpl_url': 'VARCHAR(255)',
            'absolute_magnitude_h': 'FLOAT',
            'relative_velocity': 'FLOAT',
            'miss_distance': 'FLOAT',
            'estimated_diameter_min_kilometers': 'FLOAT',
            'estimated_diameter_max_kilometers': 'FLOAT'
        }

        # Construir la definición de las columnas
        definicion_columnas = ", ".join([f"{nombre} {tipo}" for nombre, tipo in columnas.items()])

        with conn.cursor() as cur:
            # Crea la tabla si no existe
            cur.execute(f"CREATE TABLE IF NOT EXISTS {tabla} ({definicion_columnas});")
            conn.commit()
            print(f"Tabla '{tabla}' creada correctamente.")
    except Exception as e:
        print(f"Error al crear la tabla: {e}")

def insertar_datos(conn, tabla, values_list):
    fechas_existentes = set()
    datos_insertados = False
    try:
        with conn.cursor() as cur:
            for asteroid in values_list:
                fecha_emision = asteroid['fecha_emision']
                id_asteroide = asteroid['id']
                # Verifica si existen registros con la misma fecha de emisión y ID
                cur.execute(f"SELECT COUNT(*) FROM {tabla} WHERE fecha_emision = %s AND id = %s", (fecha_emision, id_asteroide))
                if cur.fetchone()[0] == 0:
                    keys = list(asteroid.keys())
                    placeholders = ', '.join(['%s' for _ in range(len(keys))])
                    query = f"INSERT INTO {tabla} ({', '.join(keys)}) VALUES ({placeholders})"
                    values = [asteroid[key] for key in keys]
                    cur.execute(query, values)
                    datos_insertados = True
                else:
                    fechas_existentes.add(fecha_emision)
        conn.commit()
        if datos_insertados:
            print("Datos insertados correctamente.")
        if fechas_existentes:
            print(f"Las siguientes fechas de emisión ya tenían el ID registrado y no se agregaron nuevos registros para esos IDs: {', '.join(fechas_existentes)}")
        if not datos_insertados and not fechas_existentes:
            print("No se insertaron nuevos datos.")
    except Exception as e:
        print(f"Error al insertar datos en la tabla {tabla}: {e}")








