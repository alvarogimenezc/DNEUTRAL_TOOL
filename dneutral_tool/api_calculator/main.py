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
        dataset_resultante_1=[]
        dataset_resultante_2=[]
        dataset_resultante_3=[]
        dataset_resultante_4=[]
        dataset_resultante_5=[]
        dataset_resultante_6=[]
        dataset_resultante_7=[]
        dataset_resultante_8=[]
        dataset_resultante_9=[]
        dataset_resultante_10=[]
        dataset_resultante_11=[]
        dataset_resultante_12=[]
        dataset_resultante_13=[]
        dataset_resultante_14=[]


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

            
            #Execute the analyzer for the 14 periods possible
            for n in range(1, 15): 

                periodos=(n)*24
                resultados=analyzer(moneda, fundings_lighter[:periodos], fundings_paradex[:periodos], fundings_hyperliquid[:periodos])

                #Join the results in one list, avoid empty results
                for r in resultados:
                    if r!=[] and n==1:
                      dataset_resultante_1.append(r)
                    if r!=[] and n==2:
                      dataset_resultante_2.append(r)
                    if r!=[] and n==3:
                      dataset_resultante_3.append(r)
                    if r!=[] and n==4:
                      dataset_resultante_4.append(r)
                    if r!=[] and n==5:
                      dataset_resultante_5.append(r)
                    if r!=[] and n==6:
                      dataset_resultante_6.append(r)
                    if r!=[] and n==7:
                      dataset_resultante_7.append(r)
                    if r!=[] and n==8:
                      dataset_resultante_8.append(r)
                    if r!=[] and n==9:
                      dataset_resultante_9.append(r)
                    if r!=[] and n==10:
                      dataset_resultante_10.append(r)
                    if r!=[] and n==11:
                      dataset_resultante_11.append(r)
                    if r!=[] and n==12:
                      dataset_resultante_12.append(r)
                    if r!=[] and n==13:
                      dataset_resultante_13.append(r)
                    if r!=[] and n==14:
                      dataset_resultante_14.append(r)

        #Order by apr,
        dataset_resultante_1.sort(key=lambda x: x[2], reverse=True)
        dataset_resultante_2.sort(key=lambda x: x[2], reverse=True)
        dataset_resultante_3.sort(key=lambda x: x[2], reverse=True)
        dataset_resultante_4.sort(key=lambda x: x[2], reverse=True)
        dataset_resultante_5.sort(key=lambda x: x[2], reverse=True)
        dataset_resultante_6.sort(key=lambda x: x[2], reverse=True)
        dataset_resultante_7.sort(key=lambda x: x[2], reverse=True)
        dataset_resultante_8.sort(key=lambda x: x[2], reverse=True)
        dataset_resultante_9.sort(key=lambda x: x[2], reverse=True)
        dataset_resultante_10.sort(key=lambda x: x[2], reverse=True)
        dataset_resultante_11.sort(key=lambda x: x[2], reverse=True)
        dataset_resultante_12.sort(key=lambda x: x[2], reverse=True)
        dataset_resultante_13.sort(key=lambda x: x[2], reverse=True)
        dataset_resultante_14.sort(key=lambda x: x[2], reverse=True)

        #Save and consolidate the results on the shared volume to feed the streamlit app
        output_json={
            "timestamp": datetime.now(),
            "dict_series": dict_series,
            "dataset_resultante_1": dataset_resultante_1,
            "dataset_resultante_2": dataset_resultante_2,
            "dataset_resultante_3": dataset_resultante_3,
            "dataset_resultante_4": dataset_resultante_4,
            "dataset_resultante_5": dataset_resultante_5,
            "dataset_resultante_6": dataset_resultante_6,
            "dataset_resultante_7": dataset_resultante_7,
            "dataset_resultante_8": dataset_resultante_8,
            "dataset_resultante_9": dataset_resultante_9,
            "dataset_resultante_10": dataset_resultante_10,
            "dataset_resultante_11": dataset_resultante_11,
            "dataset_resultante_12": dataset_resultante_12,
            "dataset_resultante_13": dataset_resultante_13,
            "dataset_resultante_14": dataset_resultante_14
        }

        #Datetime format is not recognized by json, we need to transform it into iso text
        output_json["timestamp"] = output_json["timestamp"].isoformat()

        #Convert all datetimes inside dict_series and dataset_resultante manually
        for key, value in output_json["dict_series"].items():
            if "Fechas" in value:
                value["Fechas"] = [fecha.isoformat() for fecha in value["Fechas"]]

        #Save the results in a shared volume
        with open("/shared_data/data_api.json", "w", encoding="utf-8") as f:
            json.dump(output_json, f, ensure_ascii=False, indent=2)

        print(f"Data updated. Timestamp: {datetime.now()}")

        #Stop the code 10 minutes until next update 600 seconds
        time.sleep(600)