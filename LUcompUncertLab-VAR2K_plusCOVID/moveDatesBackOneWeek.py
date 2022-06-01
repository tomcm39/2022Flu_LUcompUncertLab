#mcandrew

import sys
import numpy as np
import pandas as pd

from epiweeks import Week

if __name__ == "__main__":

    infile  = "2022-06-06-LUcompUncertLab-VAR2K_plusCOVID.csv"
    outfile = "2022-05-30-LUcompUncertLab-VAR2K_plusCOVID.csv"

    data = pd.read_csv(infile)

    teds = []
    for week in data.target_end_date:
        week = Week.fromdate(pd.to_datetime(week)) 
        week = week - 1
        teds.append(week.enddate().strftime("%Y-%m-%d"))
    data["target_end_date"] = teds
        
    data["forecast_date"] = "2022-05-30"

    data.to_csv(outfile,index=False)
