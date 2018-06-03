# -*- coding: utf-8 -*-
import unittest

import numpy as np
import pandas as pd

import XSteamPython as stm

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

class Test_Tsat_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_Tsat_p(self):
        pressure, TsatCompare = getOneDimensionalTestData(siData, 'Tsat_p')
        Tsat = calculatePropertyFromOneDimension(stm.Tsat_p, pressure)
        np.testing.assert_array_almost_equal(Tsat, TsatCompare, decimal=3)

    def test_Tsat_p_English(self):
        stm.englishUnits = True
        pressure, TsatCompare = getOneDimensionalTestData(englishData, 'Tsat_p')
        Tsat = calculatePropertyFromOneDimension(stm.Tsat_p, pressure)
        np.testing.assert_array_almost_equal(Tsat, TsatCompare, decimal=3)

    def test_Tsat_p_error(self):
        self.assertAlmostEqual(stm.Tsat_p(23000.0), 2015.0, places=2)

class Test_Tsat_s(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_Tsat_s(self):
        entropy, TsatCompare = getOneDimensionalTestData(siData, 'Tsat_s')
        Tsat = calculatePropertyFromOneDimension(stm.Tsat_s, entropy)
        np.testing.assert_array_almost_equal(Tsat, TsatCompare, decimal=3)

    def test_Tsat_s_English(self):
        stm.englishUnits = True
        entropy, TsatCompare = getOneDimensionalTestData(englishData, 'Tsat_s')
        Tsat = calculatePropertyFromOneDimension(stm.Tsat_s, entropy)
        np.testing.assert_array_almost_equal(Tsat, TsatCompare, decimal=3)

    def test_Tsat_s_error(self):
        self.assertAlmostEqual(stm.Tsat_s(10.0), 2015.0, places=2)

class Test_T_ph(unittest.TestCase):

    def tearDown(self):

        stm.englishUnits = False

    def test_T_ph(self):
        pressure, enthalpy, temperatureCompare = getTwoDimensionalTestData(siData, 'T_ph')
        temperature = calculatePropertyFromTwoDimensions(stm.T_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_ph_English(self):
        stm.englishUnits = True
        pressure, enthalpy, temperatureCompare = getTwoDimensionalTestData(englishData, 'T_ph')
        temperature = calculatePropertyFromTwoDimensions(stm.T_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_ph_error(self):
        self.assertAlmostEqual(stm.T_ph(-1, -1), 2015.0, places=2)

class Test_T_ps(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_T_ps(self):
        pressure, entropy, temperatureCompare = getTwoDimensionalTestData(siData, 'T_ps')
        temperature = calculatePropertyFromTwoDimensions(stm.T_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_ps_English(self):
        stm.englishUnits = True
        pressure, entropy, temperatureCompare = getTwoDimensionalTestData(englishData, 'T_ps')
        temperature = calculatePropertyFromTwoDimensions(stm.T_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_ps_error(self):
        self.assertAlmostEqual(stm.T_ps(1.0, -1.0), 2015.0, places=2)

class Test_T_hs(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_T_hs(self):
        enthalpy, entropy, temperatureCompare = getTwoDimensionalTestData(siData, 'T_hs')
        temperature = calculatePropertyFromTwoDimensions(stm.T_hs, enthalpy, entropy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_English(self):
        stm.englishUnits = True
        enthalpy, entropy, temperatureCompare = getTwoDimensionalTestData(englishData, 'T_hs')
        temperature = calculatePropertyFromTwoDimensions(stm.T_hs, enthalpy, entropy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_hs_error(self):
        self.assertAlmostEqual(stm.T_hs(1.0, 1.0), 2015.0, places=2)

class Test_Psat_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_Psat_T(self):
        temperature, PsatCompare = getOneDimensionalTestData(siData, 'Psat_T')
        Psat = calculatePropertyFromOneDimension(stm.Psat_T, temperature)
        np.testing.assert_array_almost_equal(Psat, PsatCompare, decimal=3)

    def test_Psat_T_English(self):
        stm.englishUnits = True
        temperature, PsatCompare = getOneDimensionalTestData(englishData, 'Psat_T')
        Psat = calculatePropertyFromOneDimension(stm.Psat_T, temperature)
        np.testing.assert_array_almost_equal(Psat, PsatCompare, decimal=3)

    def test_Psat_T_error(self):
        self.assertAlmostEqual(stm.Psat_T(0.0), 2015.0, places=2)

class Test_Transport_Properties(unittest.TestCase):

    def test_surfaceTension_T(self):
        self.assertAlmostEqual(stm.surfaceTension_T(100.0),0.09006, places=5)

    def test_surfaceTension_T_Excetpion(self):
        self.assertRaises(ArithmeticError, stm.surfaceTension_T, 0.0)

if __name__ == '__main__':
    unittest.main()
