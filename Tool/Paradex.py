import requests
import time
import sys
from datetime import datetime
import matplotlib.pyplot as plt

# Parámetros
moneda = "BTC"
rango_dias = 1
granularidad = rango_dias * 24 * 60 * 60 * 1000  # ms en X días
tiempo_actual = int(time.time() * 1000)

# Obtener símbolos PERP
diccionario_mercados = {}
headers = {'Accept': 'application/json'}
respuesta_mercados = requests.get('https://api.testnet.paradex.trade/v1/markets', headers=headers).json()
for values in respuesta_mercados["results"]:
    if values["asset_kind"] == "PERP":
        diccionario_mercados[values["base_currency"]] = values["symbol"]

# Consulta inicial
params = {
    "market": diccionario_mercados[moneda],
    "start_at": tiempo_actual - granularidad,
    "end_at": tiempo_actual,
    "page_size": 5000
}

response = requests.get('https://api.testnet.paradex.trade/v1/funding/data', params=params, headers=headers)
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
    response = requests.get('https://api.testnet.paradex.trade/v1/funding/data', params=params, headers=headers)
    data_json = response.json()
    data_funding.extend(data_json.get("results", []))  # Añadimos los nuevos registros a la lista resultados

#Ordenamos el resultado, la paginación ppuede ir desordenada
data_funding = sorted(data_funding, key=lambda x: x["created_at"])

#El json resultante tiene una granularidad de 5 segundos, lo convertimos a APR y granularidad horaria (average)
fundings=[]
for posicion in data_funding: 
    fundings.append(float(posicion["funding_rate"])*24*365) #Lo pasamos a APR

fechas=[]
for posicion in data_funding:
    fechas.append(posicion["created_at"])

i=0
sumador=0
cuentalocal=0
fundings_horarios=[]
fechas_horarios=[]

#Output buscado: lista de promedio de funding horario en apr y lista de timestamps de ultimo registro del set horario
while i < len(fundings):
    try:
       while datetime.fromtimestamp(fechas[i] / 1000).hour==datetime.fromtimestamp(fechas[i+1] / 1000).hour: 
         sumador= sumador+fundings[i]
         cuentalocal+= 1                      
         i+=1
    except:

       break

    fundings_horarios.append((sumador/cuentalocal))      #Promedio de valores para el rango horario iterado con el while, en APR
    fechas_horarios.append(fechas[i]/1000)               #Nos quedamos con el último registro del rango horarioen milisegundos
    i+=1
    sumador=0
    cuentalocal=0

print(fechas_horarios)

#Graficamos
plt.figure(figsize=(12,6))
plt.plot(fechas_horarios, fundings_horarios, marker="o", linestyle="-", color="blue", label="Funding rate")
plt.axhline(0, color="red", linestyle="--", linewidth=1)
plt.title(f"Funding rate {moneda} (últimos {rango_dias} días)")
plt.xlabel("Fecha")
plt.ylabel("Funding rate")
plt.legend()
plt.grid(True)
plt.show()