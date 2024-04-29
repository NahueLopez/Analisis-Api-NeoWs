# Proyecto de Análisis de la API de la NASA - NeoWs

## URL base de la API de la NASA
url base = 'https://api.nasa.gov/'

## Descripción de la API de asteroides NeoWs
Descripcion de la api = NeoWs (Near Earth Object Web Service) es un servicio web RESTful para información de asteroides cercanos a la Tierra.

Parámetros de consulta:

- fecha de inicio: AAAA-MM-DD (ninguno por defecto) - Fecha de inicio de la búsqueda de asteroides.
- fecha final: AAAA-MM-DD (7 días después de la fecha_inicio por defecto) - Fecha de finalización de la búsqueda de asteroides.
- Clave API: cadena (DEMO_KEY por defecto) - Clave api.nasa.gov para uso ampliado.

## Funcionalidades del Proyecto:

1- Obtención de Datos: Se accede a la API para obtener los datos necesarios.  
2- Conexión con Redshift: Se establece una conexión con la base de datos Redshift.  
3- Análisis y Guardado de Datos: Se analizan los datos JSON de la API y se guardan los campos relevantes.  
4- Verificación y Creación de Tabla: Se verifica si la tabla de datos ya está creada; de lo contrario, se crea una nueva tabla.  
5- Almacenamiento de Datos: Los datos procesados se insertan en la base de datos.

## Consideraciones Importantes

### Archivos faltantes:

1- Archivo apiKey.py: Este archivo debe contener la variable API_KEY, que es la llave proporcionada por la API de la NASA.  
2- Archivo dbKey.py: Este archivo debe contener las variables DB_NAME, HOST, PORT, USER y PASSWORD, que corresponden a los datos de la base de datos.  
