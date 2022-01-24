#mcandrew

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import scipy.stats

from scipy.stats import entropy as KL
from scipy.stats import norm as N
from scipy.stats import multivariate_normal as MVN
from scipy.interpolate import Rbf

if __name__ == "__main__":

    min,max=-3,3
    predictionone   = scipy.stats.norm(0,1)
    predictiontwo   = scipy.stats.norm(3,2.5)
    predictionthree = scipy.stats.norm(6,3.5)

    timePoints = [0,2,6]
    medians    = [0,3,6]
    
    rbfi = Rbf(timePoints, medians)
    domain = np.linspace(0,6,100)

    interps = rbfi(domain)
    
    fig,ax = plt.subplots()
    ax.scatter(timePoints,medians,s=10,color="black")
    ax.plot(domain,interps, color="blue" )
    
    plt.show()
    
    
    domain = np.linspace(min,max,200)

    probsOne   = [ predictionone.cdf(y) - predictionone.cdf(x) for (x,y) in zip(domain,domain[1:])]
    probsTwo   = [ predictiontwo.cdf(y) - predictiontwo.cdf(x) for (x,y) in zip(domain,domain[1:])]
    probsThree = [ predictionthree.cdf(y) - predictionthree.cdf(x) for (x,y) in zip(domain,domain[1:])] 

    data = np.zeros( (199,3) )
    data[:,0] = probsOne
    data[:,1] = probsTwo
    data[:,2] = probsThree
    
    def objectiveFunction(params,datadomain,data,start=0,stop=4,spacing=2):
        #params = s,l,m
        s,l = params[:1+1]
        m   = params[2:]
        
        def radialbasis(x,y,s,l):
            return s*np.exp( -1.*( ((x-y)**2)/(2*l**2) ) )

        domain = np.arange(start,stop+spacing,spacing)
        T = len(domain)
        X = len(datadomain)
      
        def buildProbs(datadomain,MVN):
             probs = MVN.cdf(datadomain[1:]) - MVN.cdf(datadomain[:-1])
             return probs

        P = np.zeros( (X-1,T) )
        KLS = []
        for col in range(P.shape[-1]):
            marginal = N( m[col], covmatrix[col,col] )
            P[:,col] = buildProbs( datadomain, marginal  )
            KLS.append(KL( data[:,col], P[:,col]  ))
        return sum(KLS)
         

    from scipy.optimize import minimize
    rslts = minimize( lambda x: objectiveFunction(x,datadomain=domain, data = data, start=0,stop=4,spacing=2), x0 = [1,0.5,0,0,0])

    s,l = rslts["x"][:1+1]
    m   = rslts["x"][2:]

    
    L = 100
    ts = np.linspace(start,stop,L)

    covmatrix = np.zeros( (L,L) )
    for r,x in enumerate(ts):
        for c,y in enumerate(ts):
            covmatrix[r,c] = radialbasis(x,y,s,l)
    testMVN = MVN(m,covmatrix,allow_singular=True)

    samples = np.random.multivariate_normal(,covmatrix,5000)
            
    
    
        
        

    

    
    
    
    


    

