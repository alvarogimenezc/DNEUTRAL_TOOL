import requests
import time
from datetime import datetime

def lighter(moneda, granularidad):

    # Nos traemos la relación entre market_id y nombre del token
    url_nombres = "https://mainnet.zklighter.elliot.ai/api/v1/orderBookDetails"
    headers_nombres = {"accept": "application/json"}
    response_nombres = requests.get(url_nombres, headers=headers_nombres)
    data_nombres=response_nombres.json()

    # Creamos un diccionario de clave-id 
    diccionario_id_moneda={}
    for values in data_nombres["order_book_details"]:
        diccionario_id_moneda[str(values["symbol"])]=values["market_id"]

    # Definimos los parámetros de búsqueda
    moneda = diccionario_id_moneda[moneda]
    rango_dias=granularidad
    granularidad = rango_dias * 24 * 60 * 60 * 1000
    T1 = int(time.time() * 1000)
    T2 = T1 - granularidad
    C_Back=0                             # Número de subdivisiones del resultado, 0 para horario

    # Hacemos la petición de funding a la API por horas
    url_funding = f"https://mainnet.zklighter.elliot.ai/api/v1/fundings?market_id={moneda}&resolution=1h&start_timestamp={T2}&end_timestamp={T1}&count_back={C_Back}"
    headers_funding = {"accept": "application/json"}
    response_funding = requests.get(url_funding, headers=headers_funding)
    data_funding = response_funding.json()

    # Creamos los ejes de la gráfica, mucho ojo, la rate es siempre +, el signo short o long da el signo del funding
    fundings_lighter=[]
    for posicion in data_funding["fundings"]: 
        if posicion['direction']=="long":
         fundings_lighter.append(float(posicion["rate"])*24*365)  # Lo pasamos a APR
        else: 
         fundings_lighter.append(-float(posicion["rate"])*24*365) # Lo pasamos a APR

    fechas_lighter=[]
    for posicion in data_funding["fundings"]:
        fechas_lighter.append(datetime.fromtimestamp(posicion["timestamp"] / 1000))

    return(fundings_lighter)