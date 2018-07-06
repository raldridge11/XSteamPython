# -*- coding: utf-8 -*-
'''
* Water and steam properties according to IAPWS IF-97
* By Magnus Holmgren, www.x-eng.com
* The steam tables are free and provided as is.
* We take no responsibilities for any errors in the code or damage thereby.
* You are free to use, modify and distribute the code as long as authorship is properly acknowledged.
* Please notify me at magnus@x-eng.com if the code is used in commercial applications
'''
import argparse

import numpy as np
import pandas as pd

def getOneDimensionalTestData(excelData):
    dataAsMatrix = excelData.as_matrix()
    return dataAsMatrix[0, 1:], dataAsMatrix[1, 1:]

def getTwoDimensionalTestData(excelData):
    dataAsMatrix = excelData.as_matrix()
    return dataAsMatrix[0, 1:], dataAsMatrix[1:, 0], dataAsMatrix[1:, 1:]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Spreadsheet data file to read in', required=True)
    parser.add_argument('-s', help='Sheet in spreadsheet to read in', required=True)
    args = parser.parse_args()

    data = pd.read_excel(args.f, args.s)

    units = args.f.split('_')[0]

    if data.shape[0] == 2:
        independentXVariable, dependentVariable = getOneDimensionalTestData(data)
        np.savez_compressed('{}_{}'.format(units, args.s), x=independentXVariable, f=dependentVariable)
    elif data.shape[0] > 2:
        independentXVariable, independentYVariable, dependentVariable = getTwoDimensionalTestData(data)
        np.savez_compressed('{}_{}'.format(units, args.s), x=independentXVariable, y=independentYVariable, f=dependentVariable)
    else:
        raise(ValueError)

if __name__ == "__main__":
    main()