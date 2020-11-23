import math
import numpy as np
import scipy
from scipy.stats import binom, hypergeom
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

'''
- 1) **Compute propensity scores**. 
- 2) Then we need to separate the treated and controls again (preserve original indexing) in order to match them.
'''
propensity = LogisticRegression()
propensity = propensity.fit(DT_m[colnames[1:-1]], DT_m['group'])

pscore = propensity.predict_proba(DT_m[colnames[1:-1]])[:,1] 
    #-- The predicted propensities by the model
print(pscore[:5])

DT_m['Propensity'] = pscore

'''
**Implement one-to-one matching, caliper without replacement**

Variants of the method are examined in the following paper. This is something to explore further. </br> Austin, P. C. (2014), A comparison of 12 algorithms for matching on the propensity score. Statist. Med., 33: 1057–1069. doi: 10.1002/sim.6004

The following "Match" function is from "https://nbviewer.jupyter.org/github/kellieotto/StatMoments/blob/master/PSM.ipynb"
'''



def Match(groups, propensity, caliper = 0.05):
    ''' 
    Inputs:
    groups = Treatment assignments.  Must be 2 groups
    propensity = Propensity scores for each observation. Propensity and groups should be in the same order (matching indices)
    caliper = Maximum difference in matched propensity scores. For now, this is a caliper on the raw
            propensity; Austin reccommends using a caliper on the logit propensity.
    
    Output:
    A series containing the individuals in the control group matched to the treatment group.
    Note that with caliper matching, not every treated individual may have a match.
    '''

    # Check inputs
    if any(propensity <=0) or any(propensity >=1):
        raise ValueError('Propensity scores must be between 0 and 1')
    elif not(0<caliper<1):
        raise ValueError('Caliper must be between 0 and 1')
    elif len(groups)!= len(propensity):
        raise ValueError('groups and propensity scores must be same dimension')
    elif len(groups.unique()) != 2:
        raise ValueError('wrong number of groups')
        
        
    # Code groups as 0 and 1
    groups = groups == groups.unique()[0]
    N = len(groups)
    N1 = groups.sum(); N2 = N-N1
    g1, g2 = propensity[groups == 1], (propensity[groups == 0])
    # Check if treatment groups got flipped - treatment (coded 1) should be the smaller
    if N1 > N2:
        N1, N2, g1, g2 = N2, N1, g2, g1 
        
        
    # Randomly permute the smaller group to get order for matching
    morder = np.random.permutation(N1)
    matches = pd.Series(np.empty(N1))
    matches[:] = np.NAN
    

    g1 = list(g1)
    # g2 = list(g2)
    
    for m in morder:
#         dist = abs(g1[m] - g2)
        dist = pd.Series( [abs(g1[m] - x) for x in g2] )
        if dist.min() <= caliper:
            matches[m] = dist.argmin()
            g2 = g2.drop(matches[m])
    return (matches)



stuff = Match( DT_m.group, DT_m.Propensity )
g1, g2 = DT_m['Propensity'][DT_m['group']==1], DT_m['Propensity'][DT_m['group']==0]
# test ValueError
#badtreat = data.Treated + data.Hispanic
#Match(badtreat, pscore)


plt.plot( DT_m['Propensity'][DT_m['group']==1] )