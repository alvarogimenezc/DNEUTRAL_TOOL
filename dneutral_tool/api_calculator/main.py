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
cuenta_monedas=len(config["monedas"])     #Sacamos la cuenta de las monedas para ver el progreso del análisis
granularidad = config["granularidad"]
dataset_resultante=[]
dict_series={}
cuenta_analisis=0

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
    
    #Necesitamos persistencia en las series devueltas de la api para los gráficos, guardamos en un diccionario
    if fundings_hyperliquid:
        dict_series[f"{moneda}_Hyperliquid"] = {
            "Exchange": "Hyperliquid",
            "Moneda": moneda,
            "Fundings": fundings_hyperliquid,
            "Fechas": fechas_hyperliquid
        }

    if fundings_paradex:
        dict_series[f"{moneda}_Paradex"] = {
            "Exchange": "Paradex",
            "Moneda": moneda,
            "Fundings": fundings_paradex,
            "Fechas": fechas_paradex
        }

    if fundings_lighter:
        dict_series[f"{moneda}_Lighter"] = {
            "Exchange": "Lighter",
            "Moneda": moneda,
            "Fundings": fundings_lighter,
            "Fechas": fechas_lighter
        }

    #Ejecutamos el analizador de estrategias
    resultados=analyzer(moneda, fundings_lighter, fundings_paradex, fundings_hyperliquid)

    # Juntamos todos los resultados en una lista y la ordenamos por APR, no adjuntamos si no hay resultados del analisis
    for r in resultados:
        if r!=[]:
           dataset_resultante.append(r)

    cuenta_analisis+=1
   
    #Mostramos el progreso por cada 4 monedas analizadas
    if cuenta_analisis % 4 == 0 or cuenta_analisis==1 or cuenta_analisis==cuenta_monedas:
       print(f"{round((cuenta_analisis/cuenta_monedas)*100, 2)} % completado...")

    dataset_resultante.sort(key=lambda x: x[2], reverse=True)

dashboard(dataset_resultante, dict_series)

# Calcula y muestra el tiempo de ejecución
tiempo_fin = time.time()
print(f"El código tardó: {round((tiempo_fin - tiempo_inicio)/60, 1)} minutos")
