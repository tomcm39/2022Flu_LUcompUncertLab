#mcandrew

class interface(object):
    def __init__(self):
        import pandas as pd
        self.predictions = pd.read_csv("communitypredictions.csv")
        self.quantiles   = pd.read_csv("communityquantiles.csv")

        self.getForecastDate()
        self.getFluData()

    def today(self):
        from datetime import date
        return date.today().strftime("%Y-%m-%d")
        
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

    def getFluData(self):
        import pandas as pd
        fludata = pd.read_csv("../../data-truth/truth-Incident Hospitalizations.csv")
        census  = pd.read_csv("../../data-locations/locations.csv")

        fluDataBy100 = fludata.merge(census,on=["location_name","location"])
        fluDataBy100["value"] = fluDataBy100.value/fluDataBy100.population
        
        self.fludata = fludata
        self.census  = census 
        self.fluDataBy100 = fluDataBy100

    def computeEndDatesBetween2Others(self,x,y):
        import numpy as np
        dts = [x]
        while x<y:
            x+=np.timedelta64(7,'D')
            dts.append(x)
        return np.array(dts,"datetime64[ns]")

    def grabInterpolatedQuantiles(self):
        import pandas as pd
        self.quantiles__interpolated = pd.read_csv("communityquantiles__interpolated.csv")
        return self.quantiles__interpolated

    def addFIPS(self, d):
        return d.merge(self.census[["location_name","location"]], on = ["location_name"])

    def addForecastDate(self,d):
        d["forecast_date"] = self.forecast_date
        return d
   
    def quantilesOut(self,x):
        import os

        if os.path.isdir("datalog"):
            pass
        else:
            os.mkdir("datalog")
        x.to_csv("./allcommunityquantiles.csv",index=False)
        x.to_csv("datalog/{:s}--allcommunityquantiles.csv".format(self.today()) ,index=False)
 
      

   

if __name__ == "__main__":

    pass

    

