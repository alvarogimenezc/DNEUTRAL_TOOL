import streamlit as st

st.title("About the Delta-Neutral Tool")

st.markdown("""
This tool is designed to monitor and analyze funding rate differences across three decentralized exchanges: **Hyperliquid**, **Lighter**, and **Paradex**.

---

## Funding Rates and Delta-Neutral Strategies

Funding rates are peer-to-peer fees that traders pay to keep perpetual contract prices aligned with the underlying spot price.

When a market becomes over-leveraged on the **long side**, long traders pay a funding fee to short traders.  
Conversely, when the market is over-leveraged on the **short side**, short traders pay the funding fee to long traders.

This mechanism helps maintain balanced leverage and keeps prices close to the oracle reference.

A delta-neutral strategy exploits funding rate inefficiencies by opening:
- a **long position** on one exchange, and  
- a **short position** on another exchange,  

while maintaining zero net price exposure.  
This approach is commonly known as **funding rate arbitrage**.

---

## About the Tool Architecture

The project is structured using two Docker containers:

- **api_calculator**  
  Acts as the processing layer. It retrieves funding rate data from public exchange endpoints, analyzes potential delta-neutral opportunities, and executes once per hour. The processed data is stored in a shared volume as a JSON file.

- **streamlit_app**  
  Handles data visualization. It reads the generated JSON file and provides an interactive web interface, allowing users to filter and explore the data efficiently.

This separation avoids unnecessary recomputation caused by Streamlit’s reactive execution model. Without it, every user interaction would trigger all API calls again, blocking the application for several minutes without providing new data.

---

The project is still under active development.
""")
