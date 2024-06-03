import os
from dbConnec import establecer_conexion, crear_tabla_dinamica, insertar_datos, verificar_tabla_existente
from apiData import obtener_datos
from datosExcel import Verificacion_Excel, insertar_datos_csv
from analisisDatosApi import analizar_json_api

def crear_tabla_si_no_existe():
    conn = establecer_conexion()
    if conn is not None:
        try:
            tabla = 'tabla_asteroides'
            if not verificar_tabla_existente(conn, tabla):
                crear_tabla_dinamica(conn, tabla)
        finally:
            conn.close()

def procesar_datos_api():
    data = obtener_datos()
    print(data)  # Para depuración
    if data:
        values_list = analizar_json_api(data)
        return values_list
    return []

def verificar_y_crear_excel():
    Verificacion_Excel()

def insertar_datos_en_db(values_list):
    conn = establecer_conexion()
    if conn is not None:
        try:
            crear_tabla_si_no_existe()
            insertar_datos(conn, 'Asteroides', values_list)
        finally:
            conn.close()

def insertar_datos_en_excel(values_list):
    if values_list:
        nombre_archivo = os.path.join('src', 'Asteroides.csv')
        insertar_datos_csv(nombre_archivo, values_list)


def main():
    values_list = procesar_datos_api()
    if values_list:
        insertar_datos_en_db(values_list)
        verificar_y_crear_excel()
        insertar_datos_en_excel(values_list)

