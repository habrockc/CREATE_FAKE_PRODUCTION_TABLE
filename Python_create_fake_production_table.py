# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 21:53:08 2020

@author: cdhabro
"""

import pandas as pd
import numpy as np

                       
"""
numPeriods = 365
freqInterval = "d"
startDate = "6/1/2019"
highestValue = 1000
lowestValue = 2
"""

def createProdTable(nPeriods=365, interval="d", firstDate="6/1/2019", maxOilValue=1000.57, minOilValue=2.5, GOR=1.45, roundDigits=2):
    """
    nPeriods: integer (ex: 365)
    interval: string (ex: "d")
    firstDate: string (ex: "6/1/2019")
    maxOilValue: float (ex: 1000.00)
    minOilValue: float (ex: 2.00)
    gasPct: float (ex: 10.5) # for 10.5% enter 10.5, not 0.105
    roundDigits: integer (ex: 0)

    """
    numPeriods = nPeriods
    inter = interval
    sd = firstDate
    maxOV = maxOilValue
    minOV = minOilValue
    gasPercentage = GOR
    rd = roundDigits
    gasPercentage = GOR
    np.random.seed(seed=1)
    randomValueToVaryCurve = round(np.random.random(1)[0], 2)
    dfName = pd.DataFrame({"DATE":pd.date_range(start=sd, periods=numPeriods, freq=inter)})
    firstPeriod = dfName["DATE"].min()
    lastPeriod = dfName["DATE"].max()
    pd.to_datetime(firstPeriod)
    dfName["rand"] = float(randomValueToVaryCurve)
    dfName["BO"] = None
    # dfName["BO"] = np.real(dfName["BO"])
    dfName["BO"] = dfName["BO"].astype(float)
    dfName["BO"] = np.where(dfName["DATE"] == sd,maxOV,None)
    dfName["BO"] = np.where(dfName["DATE"] == lastPeriod,minOV,dfName["BO"])
    dfName["BO"] = dfName["BO"].astype(float)
    dfName["BO"] = dfName["BO"].interpolate()
    dfName["BO"] = dfName["BO"].values * randomValueToVaryCurve
    dfName["BO"] = round(dfName["BO"],rd)

    
    dfName["MCF"] = dfName["BO"].values * gasPercentage
    dfName["MCF"] = round(dfName["MCF"],rd)
    
    dfName["BOE"] = sum([dfName["BO"], (dfName["MCF"]/6)])
    dfName["BOE"] = round(dfName["BOE"],2)
    dfName["calc_fake_join_column"] = "FAKE JOIN COLUMN"
    print("Random value:", randomValueToVaryCurve)
    return dfName
    return randomValueToVaryCurve



    
df = createProdTable()
print(df)


### create sample dataframe from dictionary
wellNamesDict = {"ABC":[20, "d", "6/1/2019", 777.77, 5.1, 1.50, 2],
                 "XYZ":[50, "d", "5/1/2019", 999.99, 10.3, 1.25, 2],
                 "LOL":[9, "d", "6/11/2019", 499.73, 30.1, 1.61, 2]
                 }


sampleDfList = []

for k, v in wellNamesDict.items():
    tempDf = createProdTable(*v)
    tempDf["WELLNAME"] = k
    print(tempDf)
    sampleDfList.append(tempDf)

sampleDf = pd.concat(sampleDfList, axis=0)
sampleDf.sort_values(by=["DATE", "WELLNAME"], ascending=[True, True], inplace=True)
sampleDf.reset_index(drop=True, inplace=True)
print()
print(sampleDf)
print()

outfile = r"\\hotce15\p\l48esri\per\working\c_habrock\AICOE\FLARE_POC\fake prod table.csv"
sampleDf.to_csv(outfile, index=False)
print()
print(f"DONE, saved to: \n {outfile}")
