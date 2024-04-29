from apiKey import API_KEY
import requests
from datetime import datetime, timedelta

def obtener_datos():
    fecha_final = datetime.utcnow().strftime('%Y-%m-%d')
    fecha_actual = (datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%d')

    url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={fecha_actual}&end_date={fecha_final}&api_key={API_KEY}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            return json_data
        else:
            return None
    except Exception as e:
        print(f"Error al hacer la solicitud a la API: {e}")
        return None

data = obtener_datos()
print(data)
