#mcandrew

import sys
import numpy as np
import pandas as pd

class interface(object):
    def __init__(self,forecast_date):
        self.forecast_date = forecast_date
        self.predictions = self.mergePastPredictions(1)
        self.quantiles   = self.mergePastPredictions(0)

    def grabTrueFluHosps(self):
        truth = pd.read_csv("../../data-truth/truth-Incident Hospitalizations.csv")
        self.truth=truth
        return truth

    def merge(self,models=1):
        from glob import glob
        import os

        predictions = []
        filesAndDirs = glob("../*")
        for _ in filesAndDirs:
            if os.path.isdir(_):
                if "TEVA" in _:
                    continue
                if "LUcompUncertLab" not in _:
                    continue
                if models:
                    filpath = os.path.join(_,"{:s}-allPredictions.csv.gz".format(self.forecast_date))
                else:
                    filpath = os.path.join(_,"{:s}-{:s}-preprocess.csv".format(self.forecast_date,_[3:]))
                predictions.append(pd.read_csv(filpath))
        return predictions

    def mergePastPredictions(self,models=1):
        from glob import glob
        import os
        import re

        predictions = []
        filesAndDirs = glob("../*")
        for _ in filesAndDirs:
            if os.path.isdir(_):
                if "TEVA" in _:
                    continue
                if "LUcompUncertLab" not in _:
                    continue
                if models:
                    end="allPredictions"
                else:
                    end="preprocess"

                for fil in glob("{:s}/*".format(_)):
                    if ".py" in fil:
                         continue
                    
                    if end not in fil:
                        continue
                    model = _
                    filpath = os.path.join(_,fil)
                    d = pd.read_csv(filpath)
                    d["model"] = model
                    predictions.append(d)
        return predictions

    def writeData(self,writeout,dataPredictions,dataQuantiles):
        if dataPredictions is not None:
            predictString = "{:s}-allPredictions.csv".format(self.forecast_date)
            quantileString = "{:s}-LUcompUncertLab-TEVA-preprocess.csv".format(self.forecast_date)
        
            if writeout==0:
                dataPredictions.to_csv(predictString,header=False,mode="a",index=False)
                dataQuantiles.to_csv(quantileString,header=False ,mode="a",index=False)

            else:
                dataPredictions.to_csv(predictString,header=True,mode="w",index=False)
                dataQuantiles.to_csv(quantileString ,header=True,mode="w",index=False)
        else:
            quantileString = "{:s}-LUcompUncertLab-TEVA-preprocess.csv".format(self.forecast_date)
        
            if writeout==0:
                dataQuantiles.to_csv(quantileString,header=False ,mode="a",index=False)

            else:
                dataQuantiles.to_csv(quantileString ,header=True,mode="w",index=False)

    def accessPredictionsAndQuantiles(self):
        import pandas as pd
        from glob import glob

        mostRecentFile = sorted(glob("*TEVA*.csv"))[-1]
        quantiles = pd.read_csv(mostRecentFile)

        mostRecentFile = sorted(glob("*allPredictions*.csv"))[-1]
        predictions = pd.read_csv(mostRecentFile)

        self.quantiles,self.predictions = quantiles,predictions
        return quantiles,predictions


    
if __name__ == "__main__":

    pass


