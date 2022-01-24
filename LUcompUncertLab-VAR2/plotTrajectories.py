#mcandrew

import sys
import numpy as np
import pandas as pd

from interface import interface
from visualize import viz

def prepareFluHospData():
    fluhosp = pd.read_csv("confirmedFluHosps__wide.csv")   
    fluhosp = fluhosp.loc[fluhosp.ew>202101] #ONLY CONSIDERING 2021 and later

    fluhosp = fluhosp.set_index(["ew","mw","date"])
    return fluhosp
       
if __name__ == "__main__":

    #PREPARE DATA
    fluhosp = prepareFluHospData()

    interface_local = interface(fluhosp,includedstates=[])

    interface_local.getForecastDate()
    quantiles, predictions = interface_local.accessPredictionsAndQuantiles()

    for state, quantiles in quantiles.groupby(["location"]):
        visual = viz(quantiles,fluhosp,[state],hhsregion=[])
        visual.forecastVizLOCS()
