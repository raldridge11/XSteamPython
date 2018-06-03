# -*- coding: utf-8 -*-
'''
* Water and steam properties according to IAPWS IF-97
* By Magnus Holmgren, www.x-eng.com
* The steam tables are free and provided as is.
* We take no responsibilities for any errors in the code or damage thereby.
* You are free to use, modify and distribute the code as long as authorship is properly acknowledged.
* Please notify me at magnus@x-eng.com if the code is used in commercial applications
'''
import numpy as np
import pandas as pd

try:
    siData = pd.ExcelFile('SIUnits_testCompare.xlsm')
    englishData = pd.ExcelFile('EnglishUnits_testCompare.xlsm')
except Exception:
    siData = pd.ExcelFile('tests/SIUnits_testCompare.xlsm')
    englishData = pd.ExcelFile('tests/EnglishUnits_testCompare.xlsm')

def getOneDimensionalTestData(excelFile, excelPage):

    data = pd.read_excel(excelFile, excelPage)
    dataAsMatrix = data.as_matrix()
    return dataAsMatrix[0, 1:], dataAsMatrix[1, 1:]

def getTwoDimensionalTestData(excelFile, excelPage):
    data = pd.read_excel(excelFile, excelPage)
    dataAsMatrix = data.as_matrix()
    return dataAsMatrix[0, 1:], dataAsMatrix[1:, 0], dataAsMatrix[1:, 1:]

def calculatePropertyFromOneDimension(function, independentVariable):
    thProperty = np.fromiter((function(x) for x in independentVariable), float)
    return thProperty

def calculatePropertyFromTwoDimensions(function, independentVariable1, independentVariable2):
    thProperty = np.empty(shape=(len(independentVariable1), len(independentVariable2)))
    for i, x in enumerate(independentVariable1):
        for j, y in enumerate(independentVariable2):
            thProperty[i, j] = function(x, y)
    return thProperty.T