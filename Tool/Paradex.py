import requests
import time
from datetime import datetime

def paradex(moneda, granularidad):
    # Parámetros
    moneda = moneda
    rango_dias = granularidad
    granularidad = rango_dias * 24 * 60 * 60 * 1000  # ms en X días
    tiempo_actual = int(time.time() * 1000)

    # Obtener símbolos PERP
    diccionario_mercados = {}
    headers = {'Accept': 'application/json'}
    respuesta_mercados = requests.get('https://api.prod.paradex.trade/v1/markets', headers=headers).json()
    for values in respuesta_mercados["results"]:
        if values["asset_kind"] == "PERP":
            diccionario_mercados[values["base_currency"]] = values["symbol"]

    # Consulta inicial
    params = {
        "market": diccionario_mercados[moneda],
        "start_at": int(tiempo_actual - granularidad),
        "end_at": tiempo_actual,
        "page_size": 5000
    }

    response = requests.get('https://api.prod.paradex.trade/v1/funding/data', params=params, headers=headers)
    data_json = response.json()
    data_funding = data_json["results"]

    # Seguimos pidiendo paginas y añadimos al resultado
    while "next" in data_json and data_json["next"]:
        next_cursor = data_json["next"]
        params = {
            "cursor": next_cursor,
            "market": diccionario_mercados[moneda],
            "page_size": 5000
        }
        response = requests.get('https://api.prod.paradex.trade/v1/funding/data', params=params, headers=headers)
        data_json = response.json()
        data_funding.extend(data_json.get("results", []))  # Añadimos los nuevos registros a la lista resultados

    #Ordenamos el resultado, la paginación puede ir desordenada
    data_funding = sorted(data_funding, key=lambda x: x["created_at"])

    #El json de salida muestra el funding pagado cada 5 segundos, integramos. 
    fundings=[]
    for posicion in data_funding: 
        fundings.append(float(posicion["funding_rate"])) #Lo tenemos que pasar a APR

    fechas=[]
    for posicion in data_funding:
        fechas.append(posicion["created_at"])

    i=0
    sumador=0
    cuentalocal=0
    fundings_paradex=[]
    fechas_paradex=[]

    #Output buscado: lista de promedio de funding horario en apr y lista de timestamps de ultimo registro del set horario
    while i < len(fundings):
        try:
         while datetime.fromtimestamp(fechas[i] / 1000).hour==datetime.fromtimestamp(fechas[i+1] / 1000).hour: 
            sumador = sumador + fundings[i]
            cuentalocal+= 1                      
            i+=1
        except:
         break

        fundings_paradex.append((sumador / cuentalocal) * 24 * 365 *100)  #Suma de fundings pagados en una hora
        fechas_paradex.append(datetime.fromtimestamp(fechas[i]/1000))     #Nos quedamos con el último registro del rango horario en milisegundos
        i+=1
        sumador=0
        cuentalocal=0

    return(fundings_paradex, fechas_paradex)
