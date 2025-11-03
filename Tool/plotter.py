import plotly.graph_objects as go

def plotter(nombre_serie1, nombre_serie2, fechas1, fechas2, fundings1, fundings2): 

    # Crear la figura
    fig = go.Figure()

    # Primera serie
    fig.add_trace(go.Scatter(
        x=fechas1,
        y=fundings1,
        mode='lines',
        name=nombre_serie1
    ))

    # Segunda serie 
    fig.add_trace(go.Scatter(
        x=fechas2,
        y=fundings2,
        mode='lines',
        name=nombre_serie2
    ))

    # Mostramos por pantalla
    fig.show()
        