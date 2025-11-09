import requests
import time
from datetime import datetime

def hyperliquid(moneda, granularidad):

    #Official endopt, PUT by hyperliquid design
    url = "https://api.hyperliquid.xyz/info"
    headers = {"Content-Type": "application/json"}

    #Insert searching params
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

    #Request
    response = requests.post(url, headers=headers, json=params)
    data = response.json()

    #Create output lists
    fundings_hyperliquid=[]
    for posicion in data: 
        fundings_hyperliquid.append(float(posicion["fundingRate"])* 24 * 365 *100) # Lo pasamos a APR

    fechas_hyperliquid=[]
    for posicion in data: 
        fechas_hyperliquid.append(datetime.fromtimestamp(posicion["time"] / 1000))

    return(fundings_hyperliquid, fechas_hyperliquid)

