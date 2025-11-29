#Run the funding alaysis for a given coin
#Returns a list of the shape ["moneda", "dex1", "dex2", funding delta apr for the given period] the direction is long->short

def analyzer (moneda, fundings_lighter, fundings_paradex, fundings_hyperliquid):
    
    #Define the output dicts
    delta_para_hype=[]
    delta__para_lig=[]
    delta_lig_hype=[]
    sumador=0

    #Calculate the mean apr value for the period
    try:
        for funding in fundings_hyperliquid:
            sumador+=funding
        hyper_apr=sumador/len(fundings_hyperliquid)
        sumador=0
    except: 
        pass

    try:   
        for funding in fundings_paradex:
            sumador+=funding
        paradex_apr=sumador/len(fundings_paradex)
        sumador=0
    except: 
        pass

    try: 
        for funding in fundings_lighter:
            sumador+=funding
        lighter_apr=sumador/len(fundings_lighter)
    except: 
        pass

    #Lets run the simulations paradex-hyperliquid, after checking both coins are available
    if fundings_hyperliquid!=[] and fundings_paradex!=[]:

        if hyper_apr > 0 and paradex_apr > 0: 
            if hyper_apr < paradex_apr:
                delta_para_hype=["Hyperliquid", "Paradex", round(paradex_apr - hyper_apr,2)]
            else:
                delta_para_hype=["Paradex", "Hyperliquid", round(hyper_apr - paradex_apr,2)]
        
        elif hyper_apr < 0 and paradex_apr < 0: 
            if hyper_apr < paradex_apr:
                delta_para_hype=["Hyperliquid", "Paradex", round(paradex_apr - hyper_apr,2)]
            else:
                delta_para_hype=["Paradex", "Hyperliquid", round(hyper_apr - paradex_apr,2)]

        else:
            if hyper_apr > 0: 
               delta_para_hype=["Paradex", "Hyperliquid", round(hyper_apr - paradex_apr,2)]
            else: 
               delta_para_hype=["Hyperliquid", "Paradex", round(-hyper_apr + paradex_apr,2)]
        delta_para_hype.append(moneda)


    #Lets run the simulations paradex-lighter, after checking both coins are available
    if fundings_lighter!=[] and fundings_paradex!=[]:

        if lighter_apr > 0 and paradex_apr > 0: 
            if lighter_apr < paradex_apr:
                delta__para_lig=["Lighter", "Paradex", round(paradex_apr - lighter_apr,2)]
            else:
                delta__para_lig=["Paradex", "Lighter", round(lighter_apr - paradex_apr,2)]
        
        elif lighter_apr < 0 and paradex_apr < 0: 
            if lighter_apr < paradex_apr:
                delta__para_lig=["Lighter", "Paradex", round(paradex_apr - lighter_apr,2)]
            else:
                delta__para_lig=["Paradex", "Lighter", round(lighter_apr - paradex_apr,2)]

        else:
            if lighter_apr > 0: 
               delta__para_lig=["Paradex", "Lighter", round(lighter_apr - paradex_apr,2)]
            else: 
               delta__para_lig=["Lighter", "Paradex", round(-lighter_apr + paradex_apr,2)]
        delta__para_lig.append(moneda)
 
    #Lets run the simulations hyperliquid-lighter, after checking both coins are available
    if fundings_lighter!=[] and fundings_hyperliquid!=[]:
   
        if lighter_apr > 0 and hyper_apr > 0: 
            if lighter_apr < hyper_apr:
                delta_lig_hype=["Lighter", "Hyperliquid", round(hyper_apr - lighter_apr,2)]
            else:
                delta_lig_hype=["Hyperliquid", "Lighter", round(lighter_apr - hyper_apr,2)]
        
        elif lighter_apr < 0 and hyper_apr < 0: 
            if lighter_apr < hyper_apr:
                delta_lig_hype=["Lighter", "Hyperliquid", round(hyper_apr - lighter_apr,2)]
            else:
                delta_lig_hype=["Hyperliquid", "Lighter", round(lighter_apr - hyper_apr,2)]

        else:
            if lighter_apr > 0: 
               delta_lig_hype=["Hyperliquid", "Lighter", round(lighter_apr - hyper_apr,2)]
            else: 
               delta_lig_hype=["Lighter", "Hyperliquid", round(-lighter_apr + hyper_apr,2)]
        delta_lig_hype.append(moneda)
    
    return(delta_para_hype, delta__para_lig, delta_lig_hype)
    