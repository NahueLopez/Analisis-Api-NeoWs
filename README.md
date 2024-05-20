# Proyecto de Análisis de la API de la NASA - NeoWs

## URL base de la API de la NASA
url base = 'https://api.nasa.gov/'

## Descripción de la API de asteroides NeoWs
Descripcion de la api = NeoWs (Near Earth Object Web Service) es un servicio web RESTful para información de asteroides cercanos a la Tierra.

Parámetros de consulta:

- fecha de inicio: AAAA-MM-DD (ninguno por defecto) - Fecha de inicio de la búsqueda de asteroides.
- fecha final: AAAA-MM-DD (7 días después de la fecha_inicio por defecto) - Fecha de finalización de la búsqueda de asteroides.
- Clave API: cadena (DEMO_KEY por defecto) - Clave api.nasa.gov para uso ampliado.

## Descripcion

El proyecto se plantea para recopilar los datos de la API, analizarlos y guardarlos en una base de datos y un archivo Excel. Se busca obtener solo los datos relevantes para el proyecto y evitar duplicados, utilizando la fecha de emisión y el ID de cada dato para verificar su unicidad. Se realiza una consulta a la API cada 7 días para asegurarse de no omitir ningún dato, ya que el programa se ejecuta los días lunes y al analizar los datos se evitan duplicados. Se utiliza el mismo ID que proporciona la API para mantener consistencia y evitar confusiones, ya que cada ID corresponde a un asteroide único.

La creación del archivo Excel también se verifica para evitar duplicados, de manera similar a la base de datos. Además, se cuenta con un respaldo en caso de algún problema.

Se verifica la integridad de los datos para asegurarse de que estén completos y que la información más importante esté presente. La decisión de no sobrescribir los datos se basa en la idea de generar un seguimiento de los asteroides y determinar cuándo están más cerca de la Tierra. Al cambiar cada día, se busca establecer un patrón de cercanía y seguimiento de los mismos, lo cual motiva el desarrollo en esta dirección.

## Funcionalidades del Proyecto:

1- Obtención de Datos: Se accede a la API para obtener los datos necesarios.  
2- Conexión con Redshift: Se establece una conexión con la base de datos Redshift.  
3- Análisis y Guardado de Datos: Se analizan los datos JSON de la API y se guardan los campos relevantes.  
4- Verificación y Creación de Tabla: Se verifica si la tabla de datos ya está creada; de lo contrario, se crea una nueva tabla.  
5- Almacenamiento de Datos: Los datos procesados se insertan en la base de datos  
6- Verificación y Creación del Excel: Se verifica si el excel de datos ya está creado; de lo contrario, se crea un nuevo excel.
7- Gestión de Errores: Se implementa un manejo adecuado de errores y excepciones para garantizar que el programa pueda recuperarse de situaciones inesperadas y continuar su ejecución de manera segura.

## Consideraciones Importantes

### Archivos faltantes:

1- Archivo apiKey.py: Este archivo debe contener la variable API_KEY, que es la llave proporcionada por la API de la NASA.  
2- Archivo dbKey.py: Este archivo debe contener las variables DB_NAME, HOST, PORT, USER y PASSWORD, que corresponden a los datos de la base de datos.  
