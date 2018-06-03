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

class Test_region_ph(unittest.TestCase):

    def test_region_ph_pressureOutOfBounds(self):

        self.assertEqual(stm.region_ph(0,4.0), None)

    def test_region_ph_enthalpyOutOfBounds(self):

        self.assertEqual(stm.region_ph(1,-1), None)

    def test_region_ph_region1_bellow3(self):

        self.assertEqual(stm.region_ph(1.0, 100.0), 1)

    def test_region_ph_region1_above3(self):

        self.assertEqual(stm.region_ph(17.0, 1000.0), 1)

    def test_region_ph_region2_bellow3(self):

        self.assertEqual(stm.region_ph(1.0, 4000.0), 2)

    def test_region_ph_region2_above3(self):

        self.assertEqual(stm.region_ph(17.0, 3000.0), 2)

    def test_region_ph_region4_bellow3(self):

        self.assertEqual(stm.region_ph(1.0, 1000.0), 4)

    def test_region_ph_region4_above3(self):

        self.assertEqual(stm.region_ph(17.0, 2000.0), 4)

    def test_region_ph_region5_bellow3(self):

        self.assertEqual(stm.region_ph(1.0, 5000.0), 5)

    def test_region_ph_region3(self):

        self.assertEqual(stm.region_ph(19.0, 2500.0), 3)

class Test_region_pt(unittest.TestCase):

    def test_region_pt_region5(self):
        self.assertEqual(stm.region_pt(9.0, 2000.0), 5)

    def test_region_pt_region3_highT(self):
        self.assertEqual(stm.region_pt(19.0, 640.0), 3)

    def test_region_pt_region4_highT(self):
        self.assertEqual(stm.region_pt(20.26594,640.0), 4)

    def test_region_pt_region2_highT(self):
        self.assertEqual(stm.region_pt(18.0, 640.0), 2)

    def test_region_pt_region4_lowT(self):
        self.assertEqual(stm.region_pt(2.63890, 500.0), 4)

    def test_region_pt_region1_lowT(self):
        self.assertEqual(stm.region_pt(3.0, 500.0), 1)

    def test_region_pt_region2_lowT(self):
        self.assertEqual(stm.region_pt(2.0, 500.0), 2)

    def test_region_pt_region_pt_exception(self):
        self.assertRaises(ArithmeticError, stm.region_pt, 200, 3000.0)

class Test_region_ps(unittest.TestCase):

    def test_region_ps_exception(self):
        self.assertEqual(stm.region_ps(200.0, 100.0), None)

    def test_region_ps_exception_region5(self):
        self.assertEqual(stm.region_ps(11.0, 7.5), None)

    def test_region_ps_region5(self):
        self.assertEqual(stm.region_ps(9, 7.5), 5)

    def test_region_ps_region2_highPressure(self):
        self.assertEqual(stm.region_ps(17.0, 5.4), 2)

    def test_region_ps_region2_lowPressure(self):
        self.assertEqual(stm.region_ps(15.0, 5.4), 2)

    def test_region_ps_region3(self):
        self.assertEqual(stm.region_ps(17.0, 3.8), 3)

    def test_region_ps_region4inside3(self):
        self.assertEqual(stm.region_ps(17.0, 4.0), 4)

    def test_region_ps_region4(self):
        self.assertEqual(stm.region_ps(10.0, 4.0), 4)

    def test_region_ps_region1(self):
        self.assertEqual(stm.region_ps(10.0, 1.0), 1)

class Test_region_hs(unittest.TestCase):

    def test_region_hs_exception(self):
        self.assertEqual(stm.region_hs(-1.0, -1.0), None)

    def test_region_hs_region4_bitoverb13(self):
        self.assertEqual(stm.region_hs(274.0, 1.0), 4)

    def test_region_hs_region1_bitoverb13_100Mpa_limit(self):
        self.assertEqual(stm.region_hs(309.0, 1.0), 1)

    def test_region_hs_region1_b23(self):
        self.assertEqual(stm.region_hs(1500.0, 3.4), 1)

    def test_region_hs_region3_b23(self):
        self.assertEqual(stm.region_hs(1747.0, 3.7), 3)

    def test_region_hs_exception_bitoverb13(self):
        self.assertEqual(stm.region_hs(1800.0, 3.7), None)

    def test_region_hs_region2_upperB23(self):
        self.assertEqual(stm.region_hs(3000.0, 9.2), 2)

    def test_region_hs_region4_upperB23(self):
        self.assertEqual(stm.region_hs(2700.0, 7.0), 4)

    def test_region_hs_region2_upperB23_lowEntropy(self):
        self.assertEqual(stm.region_hs(3000.0, 6.03), 2)

    def test_region_hs_region2_upperB23_highEntropy(self):
        self.assertEqual(stm.region_hs(3000.0, 6.05), 2)

    def test_region_hs_exception_upperB23(self):
        self.assertEqual(stm.region_hs(4000.0, 6.05), None)

    def test_region_hs_region4_underCritical(self):
        self.assertEqual(stm.region_hs(1800.0, 4.0), 4)

    def test_region_hs_region3_underCritical(self):
        self.assertEqual(stm.region_hs(1900.0, 4.0), 3)

    def test_region_hs_excpetion_underCritical(self):
        self.assertEqual(stm.region_hs(2000.0, 4.0), None)

    def test_region_hs_region4_aboveCritical(self):
        self.assertEqual(stm.region_hs(1900.0, 4.5), 4)

    def test_region_hs_region3_aboveCritical_underb23(self):
        self.assertEqual(stm.region_hs(2200.0, 4.5), 3)

    def test_region_hs_region2_aboveCritical_underb23(self):
        self.assertEqual(stm.region_hs(2813.0, 5.1), 2)

    def test_region_hs_region3_aboveCritical_underb23_check2(self):
        self.assertEqual(stm.region_hs(2600.0, 5.1), 3)

    def test_region_hs_region3_aboveCritical_underb23_check3(self):
        self.assertEqual(stm.region_hs(2600.0, 5.2), 3)

    def test_region_hs_region2_aboveCritical_aboveb23(self):
        self.assertEqual(stm.region_hs(2700.0, 5.2), 2)

    def test_region_hs_exception_regionnotdetermined(self):
        self.assertEqual(stm.region_hs(3000.0, 5.2), None)

class Test_region_prho(unittest.TestCase):

    def test_region_prho_exceptionOnPressure(self):
        self.assertRaises(ArithmeticError, stm.region_prho, 0.0, 700.0)

    def test_region_prho_exceptionOnDensity(self):
        self.assertRaises(ArithmeticError, stm.region_prho, 10.0, 1005.0)

    def test_region_prho_region1_lowPressure(self):
        self.assertEqual(stm.region_prho(15.0, 700.0), 1)

    def test_region_prho_region4_lowPressure(self):
        self.assertEqual(stm.region_prho(15.0, 96.72), 4)

    def test_region_prho_lowPressure_exception(self):
        self.assertRaises(ArithmeticError, stm.region_prho, 15.0, 31.0)

    def test_region_prho_region2_lowPressure(self):
        self.assertEqual(stm.region_prho(10.0, 21.0), 2)

    def test_region_prho_region5_lowPressure(self):
        self.assertEqual(stm.region_prho(10.0, 11.0), 5)

    def test_region_prho_region1_highPressure(self):
        self.assertEqual(stm.region_prho(17.0, 580.0), 1)

    def test_region_prho_region3_superCritical(self):
        self.assertEqual(stm.region_prho(23.0, 145.0), 3)

    def test_region_prho_region3_highPressure(self):
        self.assertEqual(stm.region_prho(17.0, 115.0), 3)

    def test_region_prho_region4_highPressure(self):
        self.assertEqual(stm.region_prho(17.0, 145.0), 4)

    def test_region_prho_region2_highPressure(self):
        self.assertEqual(stm.region_prho(17.0, 36.0), 2)

class Test_BoundaryFunctions(unittest.TestCase):

    def test_b23t_p(self):

        self.assertAlmostEqual(stm.b23t_p(15.0), 605.11, places=2)

    def test_b23p_t(self):

        self.assertAlmostEqual(stm.b23p_t(100.0), 241.526, places=3)

    def test_hb13_s(self):

        self.assertAlmostEqual(stm.hB13_s(3.0), 1612.0467, places=3)

    def test_tB23_hs(self):

        self.assertAlmostEqual(stm.tB23_hs(1000.0, 3.0), 1611.524, places=3)

class Test_Transport_Properties(unittest.TestCase):

    def test_surfaceTension_T(self):
        self.assertAlmostEqual(stm.surfaceTension_T(100.0),0.09006, places=5)

    def test_surfaceTension_T_Excetpion(self):
        self.assertRaises(ArithmeticError, stm.surfaceTension_T, 0.0)

class Test_hX_pt(unittest.TestCase):





    def test_h5_pt(self):

        self.assertAlmostEqual(stm.h5_pt(10.0,2273.15), 7374.752, places=3)

class Test_tX_ph(unittest.TestCase):





    def test_t5_ph(self):

        self.assertAlmostEqual(stm.t5_ph(10.0, 4500.0), 1228.268, places=3)

class Test_vX_pt(unittest.TestCase):





    def test_v5_pt(self):
        self.assertAlmostEqual(stm.v5_pt(15.0, 600.0), 0.010378, places=6)

class Test_uX_pt(unittest.TestCase):





    def test_u5_pt(self):
        self.assertAlmostEqual(stm.u5_pt(15.0, 600.0), 2479.857, places=3)

class Test_sX_pt(unittest.TestCase):





    def test_s5_pt(self):
        self.assertAlmostEqual(stm.s5_pt(15.0, 600.0), 5.343, places=3)

class Test_cpX_pt(unittest.TestCase):



    def test_cp5_pt(self):
        self.assertAlmostEqual(stm.cp5_pt(15.0, 600.0), 6.058, places=3)

class Test_cvX_pt(unittest.TestCase):





    def test_cv5_pt(self):
        self.assertAlmostEqual(stm.cv5_pt(15.0, 600.0), 2.390, places=3)

class Test_wX_pt(unittest.TestCase):





    def test_w5_pt(self):
        self.assertAlmostEqual(stm.w5_pt(15.0, 600.0), 436.314, places=3)

class Test_tX_ps(unittest.TestCase):







    def test_t5_ps(self):
        self.assertAlmostEqual(stm.t5_ps(9.0, 7.5), 1090.51, places=2)

class Test_tX_prho(unittest.TestCase):







    def test_t5_prho(self):
        self.assertAlmostEqual(stm.t5_prho(9.0, 10.0), 1943.669, places=3)

if __name__ == '__main__':
    unittest.main()
