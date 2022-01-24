#mcandrew

import sys
import numpy as np
import pandas as pd

from interface import interface
from model     import VAR
from visualize import viz

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

def prepareFluHospData():
    fluhosp = pd.read_csv("confirmedFluHosps__wide.csv")   
    fluhosp = fluhosp.loc[fluhosp.ew>202101] #ONLY CONSIDERING 2021 and later

    fluhosp = fluhosp.set_index(["ew","mw","date"])
    return fluhosp
       
if __name__ == "__main__":

    #PREPARE DATA
    fluhosp = prepareFluHospData()

    # SELECT STATES
    writeout=1
    HHS = getHHS()
    for n,(hhsregion,includedstates) in enumerate(HHS.items()):

        # BUILD INTERFACE
        interface_local = interface(fluhosp,includedstates)

        #TRAIN
        model = VAR(data = interface_local.y,L=5,F=4)
        model.fit()

        #FORMAT SAMPLES
        dataPredictions = model.formatSamples(interface_local)
        dataQuantiles   = model.fromSamples2Quantiles()

        interface_local.writeData(writeout,dataPredictions,dataQuantiles)
        if n==0:
            writeout=0
       
    #BUILD US FORECAST
    USquantiles = model.createUnitedStatesForecast()
    interface_local.writeData(writeout=0,dataPredictions=None,dataQuantiles = USquantiles)
