import requests
import time
from datetime import datetime

def lighter(moneda, granularidad):

    #We get the relation between market_id and token name
    url_nombres = "https://mainnet.zklighter.elliot.ai/api/v1/orderBookDetails"
    headers_nombres = {"accept": "application/json"}
    response_nombres = requests.get(url_nombres, headers=headers_nombres)
    data_nombres=response_nombres.json()

    #Create a dictionary key-id
    diccionario_id_moneda={}
    for values in data_nombres["order_book_details"]:
        diccionario_id_moneda[str(values["symbol"])]=values["market_id"]

    #Define the searching params
    moneda = diccionario_id_moneda[moneda]
    rango_dias=granularidad
    granularidad = rango_dias * 24 * 60 * 60 * 1000
    T1 = int(time.time() * 1000)
    T2 = T1 - granularidad
    C_Back=0                             #Number of subdivisions, 0 for hourly

    #Make the funding request hourly
    url_funding = f"https://mainnet.zklighter.elliot.ai/api/v1/fundings?market_id={moneda}&resolution=1h&start_timestamp={T2}&end_timestamp={T1}&count_back={C_Back}"
    headers_funding = {"accept": "application/json"}
    response_funding = requests.get(url_funding, headers=headers_funding)
    data_funding = response_funding.json()

    #Create the output lists, the api returns + funding with short / long direction, we switch it into + or - apr for long direction always 
    fundings_lighter=[]
    for posicion in data_funding["fundings"]: 
        if posicion['direction']=="long":
         fundings_lighter.append(float(posicion["rate"])*24*365)  #APR conversion
        else: 
         fundings_lighter.append(-float(posicion["rate"])*24*365) #APR conversion

    fechas_lighter=[]
    for posicion in data_funding["fundings"]:
        fechas_lighter.append(datetime.fromtimestamp(posicion["timestamp"]))

    return(fundings_lighter, fechas_lighter)