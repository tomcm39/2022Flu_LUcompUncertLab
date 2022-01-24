#mcandrew

import sys
import numpy as np
import pandas as pd

class model(object):
    def __init__(self,io):
        self.io = io

        self.createUSsamples()

        self.combineModelPredictions(1)
        self.combineModelPredictions(0)
        
        self.mergedModels    = self.buildMergedModelOfValues(1)
        self.mergedQuantiles = self.buildMergedModelOfValues(0)

        self.addTruth2AppendedModels()

        self.scoreQuantiles()
        self.fromWISScores2Tokens()

        self.fromTokens2ProbsByLocation()

        self.sampleValues()

        self.fromSamples2Quantiles()

        self.subset2MostRecentForecastDate()

    def createUSsamples(self):
        def sumSamples(x):
            return pd.Series({"location":"US","value":x["value"].sum()})
        
        for n,data in enumerate(self.io.predictions):
            data = data.groupby(["forecast_date","target_end_date","target","sample"]).apply(sumSamples).reset_index()
            self.io.predictions[n] = self.io.predictions[n].append(data)
            
    def combineModelPredictions(self,modelpreds=1):
        if modelpreds:
            predictions = self.io.predictions
        else:
            predictions = self.io.quantiles
        
        fromModel2Predictions = {}
        for data in predictions:
            model = data.iloc[0]["model"]

            try:
                fromModel2Predictions[model] = fromModel2Predictions[model].append(data) # odd pandas layout here
            except KeyError:
                fromModel2Predictions[model] = data

        if modelpreds:
            self.predictions = [ data for model,data in fromModel2Predictions.items() ]
            return self.predictions
        else:
            self.quantiles   = [ data for model,data in fromModel2Predictions.items() ]
            return self.quantiles
       
    def buildMergedModelOfValues(self,models=1,varname = "value"):
        if models: # sampled predictions
            data = self.predictions
            key = ['forecast_date','target_end_date','location','target','sample']
        else: # quantiles
            data = self.quantiles
            key = ['forecast_date','target_end_date','location','target','quantile','type']
            
        for n,model in enumerate(data):
            if n>0:
                model = model.rename(columns={varname:"{:s}{:d}".format(varname,n)})
                mergedModels = mergedModels.merge(model,on=key)
            else:
                mergedModels = model.rename(columns={varname:"{:s}0".format(varname)})

        mergedModels = self.turnColumnsIntoList(mergedModels,"value")

        locations = []
        for location in mergedModels.location:
            try:
                locations.append("{:02d}".format(int(location)))
            except:
                locations.append(location)
        mergedModels["location"] = locations
        mergedModels["target_end_date"] = pd.to_datetime(mergedModels.target_end_date)
        
        return mergedModels
    
    def turnColumnsIntoList(self,d,colname):
        valueColumns = d.columns.str.match(colname)
        values = d.loc[:,valueColumns].to_numpy()

        d = d.loc[:,~valueColumns]
        d[colname] = list(values)

        return d

    def addTruth2AppendedModels(self):

        for n,data in enumerate(self.quantiles):
            if n>0:
                data["model"] = n
                allQuantiles = allQuantiles.append(data)
            else:
                allQuantiles = data
                allQuantiles["model"] = 0
        allQuantiles["location"] = allQuantiles.location.astype("str")
        allQuantiles["target_end_date"] = pd.to_datetime(allQuantiles.target_end_date)
 
                 
        truth = self.io.grabTrueFluHosps()
        truth["date"] = pd.to_datetime(truth.date) 
        
        truth = truth.rename(columns={"value":"truth"})

        allQuantiles = allQuantiles.merge(truth,left_on=["target_end_date","location"]
                                               ,right_on=["date","location"], how="left")
        self.appendedQuantiles = allQuantiles
        return allQuantiles

    def scoreQuantiles(self):
        
        def score(x,numodels):
            import sys
            sys.path.append("../../../interval-scoring/")
            from scoring import weighted_interval_score_fast

            TRUTH = float(x.truth.unique())
            if np.isnan(TRUTH):
                return pd.Series({"wis":1/numodels})
            else:
                quantile2value = {row["quantile"]:[row.value] for idx,row in x.iterrows()}
                alphas = [2*x for x in quantile2value if x<0.5]

                ttl,sharpness,calibration = weighted_interval_score_fast( [TRUTH], alphas=alphas, q_dict=quantile2value)
                return pd.Series({"wis":float(ttl)})

        numodels = self.appendedQuantiles.model.max()+1
        key = ["forecast_date","target_end_date","location","target","model"]
        appendedQuantiles = self.appendedQuantiles.groupby(key).apply(lambda x: score(x,numodels)).reset_index()

        appendedQuantiles_wide = pd.pivot_table(index= key[:-1], columns = key[-1], values = "wis", data = appendedQuantiles).add_prefix("wis")
        appendedQuantiles_wide = appendedQuantiles_wide.reset_index()

        self.appendedQuantiles_wide = self.turnColumnsIntoList(appendedQuantiles_wide,"wis")
        
    def fromWISScores2Tokens(self):
        def oneHotMaxEncoding(lst):
            import numpy as np
            mn = np.min(lst)
            return [1 if x==mn else 0 for x in lst]
            
        self.appendedQuantiles_wide["tokens"] = [ oneHotMaxEncoding(wiss) for wiss in self.appendedQuantiles_wide.wis ]

    def fromTokens2ProbsByLocation(self):
        numodels = self.appendedQuantiles.model.max()+1
        def tallyTokens(x,N):
            tally = np.zeros((N,))
        
            for token in x["tokens"]:
                tally = tally+np.array(token)
            return pd.Series({"tally":list(tally)})
        
        key = ["location"]
        fromLocation2Probs = self.appendedQuantiles_wide.groupby(key).apply( lambda x: tallyTokens(x,numodels)).reset_index()
        
        self.fromLocation2Probs = fromLocation2Probs
        return fromLocation2Probs

    def sampleValues(self):
        key = ["location"]
        TEVA = self.mergedModels.merge( self.fromLocation2Probs, on = key )

        def sample(x):
            probs   = np.random.dirichlet( x.tally )
            index = np.where( np.random.multinomial(1,probs) == 1) # which model was selected
            return float(x.value[index])

        TEVA["value"] = TEVA.apply(sample,1)
        self.TEVApredictions = TEVA
        return TEVA

    def createQuantiles(self,x):
        import numpy as np
        import pandas as pd
 
        quantiles = np.array([0.010, 0.025, 0.050, 0.100, 0.150, 0.200, 0.250, 0.300, 0.350, 0.400, 0.450, 0.500
                              ,0.550, 0.600, 0.650, 0.700, 0.750, 0.800, 0.850, 0.900, 0.950, 0.975, 0.990])
        quantileValues = np.percentile( x["value"], q=100*quantiles)     
        return pd.DataFrame({"quantile":list(quantiles),"value":list(quantileValues)})

    def fromSamples2Quantiles(self):
        dataQuantiles = self.TEVApredictions.groupby(["forecast_date","target_end_date","location","target"]).apply(lambda x: self.createQuantiles(x)).reset_index().drop(columns="level_4")
        dataQuantiles["type"] = "quantile"
        dataQuantiles["target_end_date"] = dataQuantiles.target_end_date.dt.strftime("%Y-%m-%d")
        self.TEVAQuantiles = dataQuantiles
        return dataQuantiles

    def subset2MostRecentForecastDate(self):
        forecast_date = max(self.TEVApredictions["forecast_date"])
        self.TEVApredictions = self.TEVApredictions.loc[ self.TEVApredictions.forecast_date == forecast_date ]
        self.TEVAQuantiles = self.TEVAQuantiles.loc[ self.TEVAQuantiles.forecast_date == forecast_date ]
 
if __name__ == "__main__":

    pass
