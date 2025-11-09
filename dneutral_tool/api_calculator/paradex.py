import requests
import time
from datetime import datetime

def paradex(moneda, granularidad):
    #Parameters
    moneda = moneda
    rango_dias = granularidad
    granularidad = rango_dias * 24 * 60 * 60 * 1000  # ms in X days
    tiempo_actual = int(time.time() * 1000)

    #Obtain PERP symbols
    diccionario_mercados = {}
    headers = {'Accept': 'application/json'}
    respuesta_mercados = requests.get('https://api.prod.paradex.trade/v1/markets', headers=headers).json()
    for values in respuesta_mercados["results"]:
        if values["asset_kind"] == "PERP":
            diccionario_mercados[values["base_currency"]] = values["symbol"]

    #Now we obtain the funding period for the specific coin
    for values in respuesta_mercados["results"]:
        if values["base_currency"]==moneda and values["asset_kind"]=="PERP": 
            periodo_funding=values["funding_period_hours"]

    #Initial query
    params = {
        "market": diccionario_mercados[moneda],
        "start_at": int(tiempo_actual - granularidad),
        "end_at": tiempo_actual,
        "page_size": 5000
    }

    response = requests.get('https://api.prod.paradex.trade/v1/funding/data', params=params, headers=headers)
    data_json = response.json()
    data_funding = data_json["results"]

    #We keep sending queries until all data is received
    while "next" in data_json and data_json["next"]:
        next_cursor = data_json["next"]
        params = {
            "cursor": next_cursor,
            "market": diccionario_mercados[moneda],
            "page_size": 5000
        }
        response = requests.get('https://api.prod.paradex.trade/v1/funding/data', params=params, headers=headers)
        data_json = response.json()
        data_funding.extend(data_json.get("results", []))  #Add the new registers to the results list

    #Order the result, the page may be disordered
    data_funding = sorted(data_funding, key=lambda x: x["created_at"])

    #The output json shows the funding paid for 5 seconds, we need to integrate
    fundings=[]
    for posicion in data_funding: 
        fundings.append(float(posicion["funding_rate"])) #APR conversion

    fechas=[]
    for posicion in data_funding:
        fechas.append(posicion["created_at"])

    i=0
    sumador=0
    cuentalocal=0
    fundings_paradex=[]
    fechas_paradex=[]

    #Average hourly funding list in apr and timestamp list with the last register of the hourly set
    while i < len(fundings):
        try:
         while datetime.fromtimestamp(fechas[i] / 1000).hour==datetime.fromtimestamp(fechas[i+1] / 1000).hour: 
            sumador = sumador + fundings[i]
            cuentalocal+= 1                      
            i+=1
        except:
         break

        fundings_paradex.append((sumador / cuentalocal) * 24 * 365 *100 / periodo_funding)  #Sum of raw funding paid in 1 hour
        fechas_paradex.append(datetime.fromtimestamp(fechas[i]/1000))     #We keep the last register of the set
        i+=1
        sumador=0
        cuentalocal=0
        
    return(fundings_paradex, fechas_paradex)
