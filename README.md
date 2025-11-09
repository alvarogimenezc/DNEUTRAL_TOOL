## Funding Rate Tool  
This tool is designed to show and track differences between funding rates across 3 different decentralized exchanges: Hyperliquid, Lighter and Paradex.

## Funding Rates and Delta-Neutral Strategies
Funding rates are peer to peer fees that traders pay to maintain price stability. If a market is over-laveraged in the long direction, long traders will pay the funding fee to short traders. If the market is over-laveraged in the short direction, short traders will pay the funding fee to long traders. 

This mechanism ensures that the laverage remains balanced, and the price keeps stable compared to the oracle price. 

The strategy is based on opening a long position in the exchange a and a short position in the exchange b, remaining delta neutral and profiting from the differences of funding rates. This is also called funding rate arbitrage. 

## About The Tool  
The project is structured in two docker containers:

- The api_calculator container serves as the brain, it retrieves the data from the public funding endpoint of each exchange and analyzes potential delta neutral strategies. This container executes the requests once an hour. Data is then stored in a shared volume with a json dictionary. 
- The streamlit_app container takes the json file to make the web view and allow the user filter the data smoothly. 

With this architecture we are able to avoid the problem of recalculation that streamlit library has. If this separation wasn't designed, for each user interaction all the api requests would be made, adding no updates at all and blocking the app for many minutes until finished. 

The project is still under active development.

