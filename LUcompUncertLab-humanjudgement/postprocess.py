#mcandrew

import sys
import numpy as np
import pandas as pd

from interface_post import interface_post

if __name__ == "__main__":

    forecasts = pd.read_csv("./allcommunityquantiles.csv")
    forecasts["target_end_date"] = pd.to_datetime(forecasts.target_end_date)
    forecasts["forecast_date"]   = pd.to_datetime(forecasts.forecast_date)

    forecasts["horizon"] = forecasts.target_end_date - forecasts.forecast_date

    forecasts = forecasts.loc[forecasts.horizon>pd.Timedelta(0,'D')]

    enddates = sorted(list(forecasts.target_end_date.unique()))
    enddates2num  = {}
    for num,enddate in enumerate(enddates):
        enddate = pd.to_datetime(enddate)
        enddates2num[enddate] = num+1

    targets = []
    for idx,row in forecasts.iterrows():
        ted = row.target_end_date
        num = enddates2num[ted]
        targets.append( "{:d} wk ahead inc flu hosp".format(num) )
    forecasts["target"] = targets
    


    forecasts = forecasts[ ["forecast_date","target_end_date","location","target","quantile","value"] ]
    forecasts["type"] = "quantile"

    forecast_date = forecasts.iloc[0]["forecast_date"]
    forecasts.to_csv("{:s}-LUcompUncertLab-humanjudgment.csv".format(forecast_date.strftime("%Y-%m-%d")))
