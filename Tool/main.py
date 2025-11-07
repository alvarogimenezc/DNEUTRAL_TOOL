import yaml
import time

from hyperliquid import hyperliquid
from lighter import lighter
from paradex import paradex
from plotter import plotter
from analyzer import analyzer
from dashboard import dashboard

# Guarda el tiempo de inicio
tiempo_inicio = time.time()

# Cargamos configuración del yml
with open("Config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

monedas = config["monedas"]
granularidad = config["granularidad"]
dataset_resultante=[]

# Iteramos sobre los datos de configuración. 
for moneda in monedas: 
    
    try:
      fundings_hyperliquid, fechas_hyperliquid= hyperliquid(moneda, granularidad)
    except: 
      fundings_hyperliquid, fechas_hyperliquid=[], []

    try:
      fundings_lighter, fechas_lighter= lighter(moneda, granularidad)
    except:
        fundings_lighter, fechas_lighter=[], []

    try:
        fundings_paradex, fechas_paradex= paradex(moneda, granularidad)
    except:
        fundings_paradex, fechas_paradex=[], []
    
    #Ejecutamos el analizador de estrategias
    resultados=analyzer(moneda, fundings_lighter, fundings_paradex, fundings_hyperliquid)

    # Juntamos todos los resultados en una lista y la ordenamos por APR
    for r in resultados:
        dataset_resultante.append(r)

    dataset_resultante.sort(key=lambda x: x[2], reverse=True)

dashboard(dataset_resultante)

# Calcula y muestra el tiempo de ejecución
tiempo_fin = time.time()
print(f"El código tardó: {(tiempo_fin - tiempo_inicio)/60} minutos")
