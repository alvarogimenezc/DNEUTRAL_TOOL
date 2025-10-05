import requests
import time
from datetime import datetime
import matplotlib.pyplot as plt

#https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals

# Endpoint oficial, usaremos POST por diseño de hyperliquid, se devuelve en horas
url = "https://api.hyperliquid.xyz/info"
headers = {"Content-Type": "application/json"}

#Insertamos los parámetros de búsqueda
moneda="BTC"
rango_dias=1
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

#Creamos los ejes de la gráfica
fundings=[]
for posicion in data: 
    print(posicion)
    fundings.append(float(posicion["fundingRate"])* 24 * 365 *100) #Lo pasamos a APR

fechas=[]
for posicion in data: 
    fechas.append(datetime.fromtimestamp(posicion["time"] / 1000))

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