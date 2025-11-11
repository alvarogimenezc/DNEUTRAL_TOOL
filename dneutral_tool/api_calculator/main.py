import yaml
import json
from datetime import datetime
import time

from hyperliquid import hyperliquid
from lighter import lighter
from paradex import paradex
from analyzer import analyzer

while True: 
        #Load the configuration params
        with open("config.yaml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        monedas = config["monedas"]     
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

            #Join the results in one list, avoid empty results
            for r in resultados:
                if r!=[]:
                   dataset_resultante.append(r)

        #Order by apr,
        dataset_resultante.sort(key=lambda x: x[2], reverse=True)

        #Save and consolidate the results on the shared volume to feed the streamlit app
        output_json={
            "timestamp": datetime.now(),
            "dict_series": dict_series,
            "dataset_resultante": dataset_resultante
        }

        #Datetime format is not recognized by json, we need to transform it into iso text
        output_json["timestamp"] = output_json["timestamp"].isoformat()

        #Convert all datetimes inside dict_series and dataset_resultante manually
        for key, value in output_json["dict_series"].items():
            if "Fechas" in value:
                value["Fechas"] = [fecha.isoformat() for fecha in value["Fechas"]]

        with open("shared_vol/data.json", "w", encoding="utf-8") as f:
            json.dump(output_json, f, ensure_ascii=False, indent=2)

        print(f"Data updated. Timestamp: {datetime.now()}")

        #Stop the code 1 hour until next update 3600s
        time.sleep(60)