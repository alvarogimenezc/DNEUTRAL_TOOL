## Funding Rate Tool  
This tool is designed to help users identify delta-neutral trading opportunities across three decentralized exchanges: Hyperliquid, Lighter, and Paradex.  

---

## About Funding Rates and Delta-Neutral Strategies  
Funding rates are periodic payments exchanged between traders in perpetual futures markets.  
They exist to keep the contract price close to the spot price by balancing long and short positions:  

- If the market is heavily long-biased, longs pay shorts the funding rate.  
- If the market is heavily short-biased, shorts pay longs the funding rate.  

This mechanism ensures that leverage is distributed smoothly and helps maintain price stability.  

---

## The Tool  
This project contains a Python module for each exchange pipeline, designed to:  
- Connect to the public funding history endpoint.  
- Retrieve funding rate data.  
- Standarize the output so results are consistent across all three exchanges.  

The main script orchestrates the three API requests, aggregates the data, and runs analyses on possible delta-neutral strategies.  
Finally, the results are presented to the user.
The project is still in development, stay tuned for further updates. 

