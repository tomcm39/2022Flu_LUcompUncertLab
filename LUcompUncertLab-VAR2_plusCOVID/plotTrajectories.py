#mcandrew

import sys
import numpy as np
import pandas as pd

from interface import interface
from visualize import viz

def prepareData(f):
    fluhosp = pd.read_csv(f)   
    fluhosp = fluhosp.loc[fluhosp.ew>202101] #ONLY CONSIDERING 2021 and later

    fluhosp = fluhosp.set_index(["ew","mw","date"])
    #fluhosp = fluhosp.loc[:, fluhosp.sum(0)!=0] # REMOVE locations with all zeros
    return fluhosp
 

if __name__ == "__main__":

    #PREPARE DATA
    fluhosp   = prepareData("confirmedFluHosps__wide.csv")
    covidhosp = prepareData("confirmedCOVIDHosps__wide.csv")

    interface_local = interface(fluhosp,covidhosp,includedstates=[])

    interface_local.getForecastDate()
    quantiles, predictions = interface_local.accessPredictionsAndQuantiles()

    for state, quantiles in quantiles.groupby(["location"]):
        visual = viz(quantiles,fluhosp,covidhosp,[state],hhsregion=[])
        visual.forecastVizLOCS()
