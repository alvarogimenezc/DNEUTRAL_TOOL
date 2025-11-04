import yaml
import time

from hyperliquid import hyperliquid
from lighter import lighter
from paradex import paradex
from plotter import plotter
from analyzer import analyzer

# Guarda el tiempo de inicio
tiempo_inicio = time.time()

# Cargamos configuración del yml
with open("Config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

monedas = config["monedas"]
granularidad = config["granularidad"]

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

    #Aquí habria que meter un ID de la estrategia y mostrarlo en formato de lista recursivamente, ordenado de mayor a menor APR
    output1, output2, output3=analyzer(moneda, fundings_lighter, fundings_paradex, fundings_hyperliquid)
    if output1!=[]:
        print(output1)
    if output2!=[]:
        print(output2)
    if output3!=[]:
        print(output3)

# Calcula y muestra el tiempo de ejecución
tiempo_fin = time.time()
print(f"El código tardó: {(tiempo_fin - tiempo_inicio)/60} minutos")
