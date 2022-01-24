#mcandrew

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from interface import interface
from scipy.interpolate import interp1d

if __name__ == "__main__":

    inter  = interface()

    d = inter.quantiles
    d["target_end_date"] = pd.to_datetime(d.target_end_date)
    
    interpolatedData = {"location_name":[],"quantile":[],"target_end_date":[],"value":[]}
    for (location_name,quantile),subset in d.groupby(["location_name","quantile"]):

        if len(subset)<2:
            continue
        
        measured_target_end_dates = np.array( subset.target_end_date.unique(), "datetime64[ns]")
        startdate = min(measured_target_end_dates)
        enddate   = max(measured_target_end_dates)

        datesFromStart2End = inter.computeEndDatesBetween2Others(startdate,enddate)
        missingDates = set(datesFromStart2End) - set(measured_target_end_dates)

        measured_dates_ref_start     = np.array(measured_target_end_dates - startdate, "float64")
        datesFromStart2End_ref_start = np.array(datesFromStart2End - startdate       , "float64")
        
        f = interp1d(measured_dates_ref_start , subset.value )
        interpolated_predictions = f( datesFromStart2End_ref_start )

        N = len(interpolated_predictions)
        interpolatedData["location_name"].extend([location_name]*N)
        interpolatedData["quantile"].extend([quantile]*N)
        interpolatedData["target_end_date"].extend(datesFromStart2End)
        interpolatedData["value"].extend(interpolated_predictions)
    interpolatedData = pd.DataFrame(interpolatedData)
    interpolatedData.to_csv("communityquantiles__interpolated.csv",index=False)
