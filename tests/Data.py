# -*- coding: utf-8 -*-
'''
Helper functions for working with test data
'''
import os

import numpy as np

def loadnpz(npzfile):

    if os.path.isfile(os.path.join('TestData', npzfile)):
        return np.load(os.path.join('TestData', npzfile))
    elif os.path.isfile(os.path.join('tests', 'TestData', npzfile)):
        return np.load(os.path.join('tests', 'TestData', npzfile))
    else:
        raise Exception('npz file not found')

def getOneDimensionalTestData(npzfile):
    data = loadnpz(npzfile)
    return data['x'], data['f']

def getTwoDimensionalTestData(npzfile):
    data = loadnpz(npzfile)
    return data['x'], data['y'], data['f']

def calculatePropertyFromOneDimension(function, independentVariable):
    thProperty = np.fromiter((function(x) for x in independentVariable), float)
    return thProperty

def calculatePropertyFromTwoDimensions(function, independentVariable1, independentVariable2):
    thProperty = np.empty(shape=(len(independentVariable1), len(independentVariable2)))
    for i, x in enumerate(independentVariable1):
        for j, y in enumerate(independentVariable2):
            thProperty[i, j] = function(x, y)
    return thProperty.T