import yaml
import time
import plotly.graph_objects as go
from hyperliquid import hyperliquid
from lighter import lighter
from paradex import paradex

# Iniciamos cronómetro
inicio = time.time()

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

#Graficamos los resultados
# Crear la figura
fig = go.Figure()

# Primera serie (por ejemplo Hyperliquid)
fig.add_trace(go.Scatter(
    x=fechas_hyperliquid,
    y=fundings_hyperliquid,
    mode='lines',
    name='Hyperliquid'
))

# Segunda serie (por ejemplo Paradex)
fig.add_trace(go.Scatter(
    x=fechas_paradex,
    y=fundings_paradex,
    mode='lines',
    name='Paradex'
))

# Configuración del gráfico
fig.update_layout(
    title="Comparativa de Funding Rates",
    xaxis_title="Fecha",
    yaxis_title="Funding APR (%)",
    hovermode="x unified",
    template="plotly_dark",
    height=500
)

# Mostrar
fig.show()

# Fin del cronómetro
fin = time.time()
print(f"\n🕒 Tiempo total de ejecución: {round(fin - inicio, 2)/60} minutos\n")


