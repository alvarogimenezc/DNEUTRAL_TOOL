# Funding Rate Tool  
This tool is designed to show and track differences between funding rates across 3 different decentralized exchanges: Hyperliquid, Lighter and Paradex.

## About Funding Rates and Delta-Neutral Strategies
Funding rates are peer to peer fees that traders pay to mantain price stability. If a market is over-laveraged in the long direction, long traders will pay the funding fee to short traders. If the market is over-laveraged in the short direction, long traders will pay the funding fee to short traders. 

This mechanism ensures that the laverage remains smooth, and the price keeps stable compared to the oracle price. 

The strategy is based on opening a long position in the exchange a and a short position in the exchange b, remaining delta neutral and profiting from the differences of funding rates. This is also called funding rate arbitrage. 

## The Tool  
This project contains a Python module for each exchange, designed to:  
- Connect to the public funding history endpoint.  
- Retrieve funding rate data.  
- Standarize the output so results are consistent across all three exchanges.  

The main script orchestrates the three API requests, aggregates the data, and runs analyses on possible delta-neutral strategies.  
Finally, the results are presented to the user.

The project is still in development, stay tuned for further updates. 

