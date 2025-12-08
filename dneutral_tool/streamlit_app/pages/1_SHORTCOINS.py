#New section about shortable coins with high risk of dump
import streamlit as st
import pandas as pd

st.markdown("---")
st.subheader("🚨 Altcoins con Fundamentales Débiles / Riesgo Alto")

try:
    with open("short_coins.json", "r", encoding="utf-8") as f:
        short_data = json.load(f)
    df_short = pd.DataFrame(short_data)

    # Mostrar tabla ordenada por riesgo y volatilidad
    df_short["Volatilidad"] = pd.to_numeric(df_short["Volatilidad"], errors="coerce")
    df_short = df_short.sort_values(by=["Riesgo", "Volatilidad"], ascending=[True, False])

    st.dataframe(df_short)

except: 
    pass
