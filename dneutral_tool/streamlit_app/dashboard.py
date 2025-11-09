#This dashboard uses stremalit library to show the results 
import streamlit as st
import pandas as pd
import plotly.express as px

def dashboard(dataset_resultante, dict_series): 

    #Insert the web title
    st.title("Dashboard estrategias delta neutral")

    #Create the table to show the results, we need pandas lib 
    st.subheader("Tabla comprarativa resultados")
    df = pd.DataFrame(dataset_resultante, columns=["LARGO 📈", "CORTO 📉", "APR % 🔼", "MONEDA 🪙"])
    st.dataframe(df)

     #Lets create the chart for a given coin/dex
    st.subheader("📈 Evolución de Fundings por Exchange y Moneda")

    if not dict_series:
        st.warning("No hay datos disponibles para graficar.")
        return

    # Obtenemos listas únicas de exchanges y monedas
    exchanges = sorted({v["Exchange"] for v in dict_series.values()})
    monedas = sorted({v["Moneda"] for v in dict_series.values()})

    col1, col2 = st.columns(2)
    selected_exchange = col1.selectbox("Selecciona Exchange", exchanges)
    selected_moneda = col2.selectbox("Selecciona Moneda", monedas)

    key = f"{selected_moneda}_{selected_exchange}"
    if key in dict_series:
        data = dict_series[key]
        df_plot = pd.DataFrame({
            "Fecha": data["Fechas"],
            "Funding": data["Fundings"]
        })

        fig = px.line(
            df_plot,
            x="Fecha",
            y="Funding",
            title=f"Funding Rate - {selected_moneda} ({selected_exchange})",
            template="plotly_dark",
        )
        fig.update_traces(line=dict(width=2))
        fig.update_layout(
            title_font=dict(size=20),
            hovermode="x unified",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40, r=40, t=60, b=40)
        )

        st.plotly_chart(fig, width=True)
    else:
        pass