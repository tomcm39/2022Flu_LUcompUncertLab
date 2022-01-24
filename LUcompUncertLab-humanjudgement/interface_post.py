#mcandrew

class interface_post(object):
    def __init__(self,fluhosp,includedstates):
        self.fluhosp = fluhosp
        
        self.includedstates = includedstates
        self.timeseriesName = includedstates
        self.getForecastDate()
        self.generateTargetEndDates()

    def getForecastDate(self):
        import datetime
        from epiweeks import Week

        from datetime import datetime as dt

        today = dt.today()
        dayofweek = today.weekday()

        thisWeek = Week.thisweek()
        if dayofweek in {6,0}: # a SUNDAY or MONDAY
            thisWeek = thisWeek-1
        else:
            pass
        self.thisWeek = thisWeek
        
        forecastDate = ((thisWeek+1).startdate() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        self.forecast_date = forecastDate
        return forecastDate

    def generateTargetEndDates(self):
        import numpy as np
        
        target_end_dates = []
        for f in np.arange(1,4+1): # four weeks ahead
            ted = ((self.thisWeek+int(f)).enddate()).strftime("%Y-%m-%d")
            target_end_dates.append(ted)
        self.target_end_dates = target_end_dates
        return target_end_dates


    def accessPredictionsAndQuantiles(self):
        import pandas as pd
        from glob import glob

        quantiles = pd.read_csv("allcommunityquantiles.csv")
        self.quantiles = quantiles
        return quantiles
        

if __name__ == "__main__":
    pass

