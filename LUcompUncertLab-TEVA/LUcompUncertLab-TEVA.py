#mcandrew

import sys
import numpy as np
import pandas as pd

from interface import interface
from epitime import epitime
from model import model

import datetime

def getHHS():
        return { 1:["09","23","25","33","44","50"]
                ,2:["34","36","72","78"]
                ,3:["10","11","24","42","51","54"]
                ,4:["01","12","13","21","28","37","45","47"]
                ,5:["17","18","26","27","39","55"]
                ,6:["05","22","35","40","48"]
                ,7:["19","20","29","31"]
                ,8:["08","30","38","46","49","56"]
                ,9:["04","06","15","32"] # no american samoa, no mariana, no microni, no guam,nomarshall,nopa
                ,10:["02","16","41","53"]}

def getStates(HHS):
    return [state for (hhs,states) in HHS.items() for state in states]


def prepareData(f):
    fluhosp = pd.read_csv(f)   
    fluhosp = fluhosp.loc[fluhosp.ew>202101] #ONLY CONSIDERING 2021 and later

    fluhosp = fluhosp.set_index(["ew","mw","date"])
    return fluhosp

if __name__ == "__main__":

    #PREPARE DATA
    fluhosp   = prepareData("confirmedFluHosps__wide.csv")
    covidhosp = prepareData("confirmedCOVIDHosps__wide.csv")

    etim = epitime()
    thisweek,lastweek = etim.thisweek()

    forecast_date = (thisweek.startdate()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    io = interface(forecast_date)
    
    TEVA = model(io)
    io.writeData(writeout=1, dataPredictions = TEVA.TEVApredictions, dataQuantiles = TEVA.TEVAQuantiles )

    fromLocation2Probs = TEVA.fromLocation2Probs
    print(fromLocation2Probs)
    
    dataQuantiles = TEVA.TEVAQuantiles

    # HHS = getHHS()
    # states = getStates(HHS)
    # for n,includedstates in enumerate(states):
    #     visual = viz(dataQuantiles,fluhosp,covidhosp,[includedstates],[])
    #     visual.forecastVizLOCS()
    # visual = viz(dataQuantiles,fluhosp,covidhosp,["US"],[])
    # visual.forecastVizLOCS()
