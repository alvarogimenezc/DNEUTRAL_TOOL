#This dashboard uses stremalit to show the results 
import streamlit as st

def dashboard(dataset_resultante): 
    st.title("Dashbord estrategias delta neutral")

    st.header("Comparador de estrategias de delta neutral")

    # Create a table to display the results
    st.subheader("Tabla comprarativa resultados")
    
    # Convert dataset_resultante to a DataFrame for better display
    import pandas as pd

    df = pd.DataFrame(dataset_resultante, columns=["Dex lagro", "Dex corto 2", "APR", "Moneda"])
    st.dataframe(df)