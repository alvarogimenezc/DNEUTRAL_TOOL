import yaml
import time

from hyperliquid import hyperliquid
from lighter import lighter
from paradex import paradex
from plotter import plotter
from analyzer import analyzer

# Cargamos configuración del yml
with open("Config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

monedas = config["monedas"]
granularidad = config["granularidad"]

# Iteramos sobre los datos de configuración. Deberemos meter un try except a cada llamada por si la moneda no está disponible
for moneda in monedas: 
    print(f"\n{moneda}\n")
    
    fundings_hyperliquid, fechas_hyperliquid= hyperliquid(moneda, granularidad)
    fundings_lighter, fechas_lighter= lighter(moneda, granularidad)
    fundings_paradex, fechas_paradex= paradex(moneda, granularidad)

    #Aquí habria que meter un ID de la estrategia y mostrarlo en formato de lista recursivamente, ordenado de mayor a menor APR
    print(analyzer(moneda, fundings_lighter, fundings_paradex, fundings_hyperliquid))