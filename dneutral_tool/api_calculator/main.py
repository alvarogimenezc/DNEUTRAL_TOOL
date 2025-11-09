import yaml
import time

from dneutral_tool.api_calculator.hyperliquid import hyperliquid
from dneutral_tool.api_calculator.lighter import lighter
from dneutral_tool.api_calculator.paradex import paradex
from dneutral_tool.api_calculator.analyzer import analyzer
from dneutral_tool.streamlit_app.dashboard import dashboard

#Save the initial time
tiempo_inicio = time.time()

#Load the configuration params
with open("dneutral_tool/config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

monedas = config["monedas"]
cuenta_monedas=len(config["monedas"])     #To track the execution
granularidad = config["granularidad"]
dataset_resultante=[]
dict_series={}
cuenta_analisis=0

#Iterate over the configuration data
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

    #We need persistency on the series returned by the api for the charts, saved in a dict
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

    #Execute the analyzer
    resultados=analyzer(moneda, fundings_lighter, fundings_paradex, fundings_hyperliquid)

    #Join the results in one list and order by apr, avoid empty results
    for r in resultados:
        if r!=[]:
           dataset_resultante.append(r)

    cuenta_analisis+=1
   
    #Show the progress for each 4 token group
    if cuenta_analisis % 4 == 0 or cuenta_analisis==1 or cuenta_analisis==cuenta_monedas:
       print(f"{round((cuenta_analisis/cuenta_monedas)*100, 2)} % completado...")

    dataset_resultante.sort(key=lambda x: x[2], reverse=True)

dashboard(dataset_resultante, dict_series)

#Show the execution time
tiempo_fin = time.time()
print(f"El código tardó: {round((tiempo_fin - tiempo_inicio)/60, 1)} minutos")
