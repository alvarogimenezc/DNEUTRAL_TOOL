
import requests
import time
from datetime import datetime
import matplotlib.pyplot as plt

#https://apidocs.lighter.xyz/reference/fundings

#Nos traemos la relación entre market_id y nombre del token
url_nombres = "https://mainnet.zklighter.elliot.ai/api/v1/orderBookDetails"
headers_nombres = {"accept": "application/json"}
response_nombres = requests.get(url_nombres, headers=headers_nombres)
data_nombres=response_nombres.json()

#Creamos un diccionario de clave-id 
diccionario_id_moneda={}
for values in data_nombres["order_book_details"]:
    diccionario_id_moneda[str(values["symbol"])]=values["market_id"]

#Definimos los parámetros de búsqueda
moneda = diccionario_id_moneda["HYPE"]
rango_dias=1
granularidad = rango_dias * 24 * 60 * 60 * 1000
T1 = int(time.time() * 1000)
T2 = T1 - granularidad
C_Back=0                             #Número de subdivisiones del resultado, 0 para horario

#Hacemos la petición de funding a la API por horas
url_funding = f"https://mainnet.zklighter.elliot.ai/api/v1/fundings?market_id={moneda}&resolution=1h&start_timestamp={T2}&end_timestamp={T1}&count_back={C_Back}"
headers_funding = {"accept": "application/json"}
response_funding = requests.get(url_funding, headers=headers_funding)
data_funding = response_funding.json()

#Creamos los ejes de la gráfica
fundings=[]
for posicion in data_funding["fundings"]: 
    print(posicion)
    fundings.append(float(posicion["rate"])*24*365) #Lo pasamos a APR

fechas=[]
for posicion in data_funding["fundings"]:
    fechas.append(datetime.fromtimestamp(posicion["timestamp"] / 1000))

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