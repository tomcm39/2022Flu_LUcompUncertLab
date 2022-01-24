#mcandrew

import sys
import numpy as np
import pandas as pd
import pickle

from interface import interface


class buildWeightMatrix(object):
    def __init__(self):
        self.locations = self.grabLocations()

    def grabLocations(self):
        import pandas as pd
        return pd.read_csv("communityquantiles__interpolated.csv").location_name.unique()

    def add_data(self,X,Y):
        self.X=X
        self.Y=Y
    
    def fitmodel(self):
        import stan
        modeldesc = '''
        data {
            int locs;
            int sublocs;
            int T;
            matrix [T,sublocs]    X;
            matrix [T,locs] Y;
        }
        parameters {
           vector <lower=0> [locs] sigmas ;
           simplex [sublocs] alpha [locs];
           simplex [sublocs] W [locs]; 
        }
        model {
           for (l in 1: locs){
              sigmas[l]~exponential(1.);
              W[l]~dirichlet(alpha[l]);
              Y[:,l]~normal( X*W[l],sigmas[l]);
           }
        }
        '''
        data = {"locs": Y.shape[-1], "T":Y.shape[0], "sublocs":X.shape[-1],"X":X,"Y":Y}
        posterior = stan.build(modeldesc, data=data)
        fit = posterior.sample()

        self.fit = fit
        return fit

   
if __name__ == "__main__":

    inter = interface()
    flu = inter.fluDataBy100

    W = buildWeightMatrix()

    location_names = W.grabLocations()
                      
    
    fluwide = pd.pivot_table(index="date", columns="location_name",values="value",data=flu)
    fluwide = fluwide.dropna(0)

    fluwide = fluwide.loc[fluwide.index>'2021-01-01']
    timepoints = fluwide.shape[0]

    X = fluwide[location_names].values
    Y = fluwide.values

    W.add_data(X,Y)
    W.fitmodel()

    W = W.fit["W"].mean(2)
    pickle.dump(W,open("W.pkl","wb"))
    
    quantiles = inter.grabInterpolatedQuantiles()

    quantilesByValues = pd.pivot_table(index= ["target_end_date","quantile"], columns = ["location_name"], values = ["value"],data = quantiles)
    quantilesByValues.columns = [column  for (_,column) in quantilesByValues.columns]
    quantilesByValues = quantilesByValues.dropna(1)

    allQuantiles = pd.DataFrame(quantilesByValues.values.dot(W.T),columns=fluwide.columns,index=quantilesByValues.index)
    allQuantiles = allQuantiles.reset_index()
    
    prediction2submit = allQuantiles.melt( id_vars=["target_end_date","quantile"]  )
    prediction2submit = inter.addFIPS(prediction2submit)
    prediction2submit = inter.addForecastDate(prediction2submit)

    inter.quantilesOut(prediction2submit)
    
