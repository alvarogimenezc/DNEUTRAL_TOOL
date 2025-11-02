import requests
import time
from datetime import datetime

def hyperliquid(moneda, granularidad):

    # Endpoint oficial, usaremos POST por diseño de hyperliquid, se devuelve en horas
    url = "https://api.hyperliquid.xyz/info"
    headers = {"Content-Type": "application/json"}

    # Insertamos los parámetros de búsqueda
    moneda=moneda
    rango_dias=granularidad
    granularidad = rango_dias * 24 * 60 * 60 * 1000
    tiempo_actual = int(time.time() * 1000)

    params = {
        "type": "fundingHistory",
        "coin": moneda,
        "startTime": tiempo_actual - granularidad,
        "endTime": tiempo_actual
    }

    # Petición
    response = requests.post(url, headers=headers, json=params)
    data = response.json()

    # Creamos los ejes de la gráfica
    fundings_hyperliquid=[]
    for posicion in data: 
        fundings_hyperliquid.append(float(posicion["fundingRate"])* 24 * 365 *100) # Lo pasamos a APR

    fechas_hyperliquid=[]
    for posicion in data: 
        fechas_hyperliquid.append(datetime.fromtimestamp(posicion["time"] / 1000))

    return(fundings_hyperliquid, fechas_hyperliquid)

