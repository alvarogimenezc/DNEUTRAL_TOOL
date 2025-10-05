import requests
import time
from datetime import datetime
import matplotlib.pyplot as plt

#Public endpoint for Paradex frate API https://docs.paradex.trade/api/testnet/markets/get-funding-data

#Definimos parametros de la consulta
moneda="ETH"
rango_dias=1
granularidad = rango_dias * 24 * 60 * 60 * 1000
tiempo_actual = int(time.time() * 1000)

#Creamos diccionario de clave-id
diccionario_mercados={}
headers = {
  'Accept': 'application/json'
}
respuesta_mercados = requests.get('https://api.testnet.paradex.trade/v1/markets', headers = headers).json()
for values in respuesta_mercados["results"]:
    if values["asset_kind"]=="PERP":
        diccionario_mercados[values["base_currency"]]=values["symbol"]

#Ejecutamos la consulta
headers = {
  'Accept': 'application/json'}

params = {
    "market": diccionario_mercados[moneda],
    "start_at": int(time.time() * 1000) - granularidad,
    "end_at": int(time.time() * 1000)}

response = requests.get('https://api.testnet.paradex.trade/v1/funding/data', params=params, headers = headers)
data_funding=response.json()["results"]

print(data_funding)

#Creamos los ejes de la gráfica
fundings=[]
for posicion in data_funding: 
    print(posicion)
    fundings.append(float(posicion["funding_rate"])*24*365) #Lo pasamos a APR

fechas=[]
for posicion in data_funding:
    fechas.append(datetime.fromtimestamp(posicion["created_at"] / 1000))

#Graficamos
plt.figure(figsize=(12,6))
plt.plot(fechas, fundings, marker="o", linestyle="-", color="blue", label="Funding rate")
plt.axhline(0, color="red", linestyle="--", linewidth=1)
plt.title(f"Funding rate {moneda} (últimos {rango_dias} días)")
plt.xlabel("Fecha")
plt.ylabel("Funding rate")
plt.legend()
plt.grid(True)
plt.show()