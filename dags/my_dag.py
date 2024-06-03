import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from src.main import (
    crear_tabla_si_no_existe,
    procesar_datos_api,
    verificar_y_crear_excel,
    insertar_datos_en_db,
    insertar_datos_en_excel
)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email': ['tu_email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'mi_dag',
    default_args=default_args,
    description='Un DAG para ejecutar el script principal',
    schedule_interval=timedelta(days=1),
)

crear_tabla_task = PythonOperator(
    task_id='crear_tabla_si_no_existe',
    python_callable=crear_tabla_si_no_existe,
    dag=dag,
)

def procesar_datos_api_y_guardar(**kwargs):
    values_list = procesar_datos_api()
    kwargs['ti'].xcom_push(key='values_list', value=values_list)

procesar_datos_task = PythonOperator(
    task_id='procesar_datos_api_y_guardar',
    python_callable=procesar_datos_api_y_guardar,
    provide_context=True,
    dag=dag,
)

def insertar_datos_en_db_wrapper(**kwargs):
    values_list = kwargs['ti'].xcom_pull(key='values_list', task_ids='procesar_datos_api_y_guardar')
    insertar_datos_en_db(values_list)

insertar_datos_db_task = PythonOperator(
    task_id='insertar_datos_en_db',
    python_callable=insertar_datos_en_db_wrapper,
    provide_context=True,
    dag=dag,
)

def verificar_y_crear_excel_wrapper(**kwargs):
    verificar_y_crear_excel()

verificar_excel_task = PythonOperator(
    task_id='verificar_y_crear_excel',
    python_callable=verificar_y_crear_excel_wrapper,
    dag=dag,
)


def insertar_datos_en_excel_wrapper(**kwargs):
    values_list = kwargs['ti'].xcom_pull(key='values_list', task_ids='procesar_datos_api_y_guardar')
    insertar_datos_en_excel(values_list)

insertar_datos_excel_task = PythonOperator(
    task_id='insertar_datos_en_excel',
    python_callable=insertar_datos_en_excel_wrapper,
    provide_context=True,
    dag=dag,
)





crear_tabla_task >> procesar_datos_task >> insertar_datos_db_task >> verificar_excel_task >> insertar_datos_excel_task
