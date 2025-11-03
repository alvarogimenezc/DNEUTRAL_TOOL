
#Run the funding alaysis for a given coin
#Returns a list of the shape ["moneda", "dex1", "dex2", funding delta apr for the given period] the direction is long->short

def analyzer (moneda, fundings_lighter, fundings_paradex, fundings_hyperliquid):
    
    #Define the output dicts
    delta_para_hype=[]
    delta__para_lig=[]
    delta_lig_hype=[]
    sumador=0

    #Calculate the mean apr value for the period
    for funding in fundings_hyperliquid:
        sumador+=funding
    hyper_apr=sumador/len(fundings_hyperliquid)
    sumador=0

    for funding in fundings_paradex:
        sumador+=funding
    paradex_apr=sumador/len(fundings_paradex)
    sumador=0

    for funding in fundings_lighter:
        sumador+=funding
    lighter_apr=sumador/len(fundings_lighter)

    #Lets run the simulations paradex-hyperliquid
    if hyper_apr > 0 and paradex_apr > 0: 
        if hyper_apr < paradex_apr:
            delta_para_hype=["Hyperliquid", "Paradex", paradex_apr - hyper_apr]
        else:
            delta_para_hype=["Paradex", "Hyperliquid", hyper_apr - paradex_apr]
    
    elif hyper_apr < 0 and paradex_apr < 0: 
        if hyper_apr < paradex_apr:
            delta_para_hype=["Hyperliquid", "Paradex", paradex_apr - hyper_apr]
        else:
            delta_para_hype=["Paradex", "Hyperliquid", hyper_apr - paradex_apr]

    else:
        if hyper_apr > 0: 
           delta_para_hype=["Paradex", "Hyperliquid", hyper_apr - paradex_apr]
        else: 
           delta_para_hype=["Hyperliquid", "Paradex", hyper_apr - paradex_apr]

    #Lets run the simulations paradex-lighter
    if lighter_apr > 0 and paradex_apr > 0: 
        if lighter_apr < paradex_apr:
            delta__para_lig=["Lighter", "Paradex", paradex_apr - lighter_apr]
        else:
            delta__para_lig=["Paradex", "Lighter", lighter_apr - paradex_apr]
    
    elif lighter_apr < 0 and paradex_apr < 0: 
        if lighter_apr < paradex_apr:
            delta__para_lig=["Lighter", "Paradex", paradex_apr - lighter_apr]
        else:
            delta__para_lig=["Paradex", "Lighter", lighter_apr - paradex_apr]

    else:
        if lighter_apr > 0: 
           delta__para_lig=["Paradex", "Lighter", lighter_apr - paradex_apr]
        else: 
           delta__para_lig=["Lighter", "Paradex", lighter_apr - paradex_apr]

    #Lets run the simulations hyperliquid-lighter
    if lighter_apr > 0 and hyper_apr > 0: 
        if lighter_apr < hyper_apr:
            delta_lig_hype=["Lighter", "Hyperliquid", hyper_apr - lighter_apr]
        else:
            delta_lig_hype=["Hyperliquid", "Lighter", lighter_apr - hyper_apr]
    
    elif lighter_apr < 0 and hyper_apr < 0: 
        if lighter_apr < hyper_apr:
            delta_lig_hype=["Lighter", "Hyperliquid", hyper_apr - lighter_apr]
        else:
            delta_lig_hype=["Hyperliquid", "Lighter", lighter_apr - hyper_apr]

    else:
        if lighter_apr > 0: 
           delta_lig_hype=["Hyperliquid", "Lighter", lighter_apr - hyper_apr]
        else: 
           delta_lig_hype=["Lighter", "Hyperliquid", lighter_apr - hyper_apr]

    delta_para_hype.append(moneda)
    delta__para_lig.append(moneda)
    delta_lig_hype.append(moneda)

    return(delta_para_hype, delta__para_lig, delta_lig_hype)