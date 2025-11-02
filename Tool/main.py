import yaml
from hyperliquid import hyperliquid
from lighter import lighter
from paradex import paradex

# Cargamos configuracion del yml
with open("Config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

monedas = config["monedas"]
granularidad = config["granularidad"]

# Iteramos sobre los datos de configuaración
for moneda in monedas: 
    print(f"\n", moneda,f"\n")

    print(f"\n", hyperliquid(moneda, granularidad), f"\n")
    print(f"\n", lighter(moneda, granularidad), f"\n")
    print(f"\n", paradex(moneda, granularidad), f"\n")

