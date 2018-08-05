# -*- coding: utf-8 -*-
'''
* Water and steam properties according to IAPWS IF-97
* By Magnus Holmgren, www.x-eng.com
* The steam tables are free and provided as is.
* We take no responsibilities for any errors in the code or damage thereby.
* You are free to use, modify and distribute the code as long as authorship is properly acknowledged.
* Please notify me at magnus@x-eng.com if the code is used in commercial applications
'''
import unittest

import numpy as np

import Data
import XSteamPython as stm

class Test_cpV_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_cpV_p(self):
        pressure, specificHeatCompare = Data.getOneDimensionalTestData('SIUnits_cpV_p.npz')
        specificHeat = Data.calculatePropertyFromOneDimension(stm.cpV_p, pressure)
        np.testing.assert_array_almost_equal(specificHeat, specificHeatCompare, decimal=2)

    def test_cpV_p_English(self):
        stm.englishUnits = True
        pressure, specificHeatCompare = Data.getOneDimensionalTestData('EnglishUnits_cpV_p.npz')
        specificHeat = Data.calculatePropertyFromOneDimension(stm.cpV_p, pressure)
        np.testing.assert_array_almost_equal(specificHeat, specificHeatCompare, decimal=2)

    def test_cpV_p_error(self):
        self.assertAlmostEqual(stm.cpV_p(-1.0), 2015.0, places=1)

class Test_cpL_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_cpL_p(self):
        pressure, specificHeatCompare = Data.getOneDimensionalTestData('SIUnits_cpL_p.npz')
        specificHeat = Data.calculatePropertyFromOneDimension(stm.cpL_p, pressure)
        np.testing.assert_array_almost_equal(specificHeat, specificHeatCompare, decimal=2)

    def test_cpL_p_English(self):
        stm.englishUnits = True
        pressure, specificHeatCompare = Data.getOneDimensionalTestData('EnglishUnits_cpL_p.npz')
        specificHeat = Data.calculatePropertyFromOneDimension(stm.cpL_p, pressure)
        np.testing.assert_array_almost_equal(specificHeat, specificHeatCompare, decimal=2)

    def test_cpL_p_error(self):
        self.assertAlmostEqual(stm.cpL_p(-1.0), 2015.0, places=1)

class Test_cpV_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_cpV_T(self):
        temperature, specificHeatCompare = Data.getOneDimensionalTestData('SIUnits_cpV_T.npz')
        specificHeat = Data.calculatePropertyFromOneDimension(stm.cpV_T, temperature)
        np.testing.assert_array_almost_equal(specificHeat, specificHeatCompare, decimal=2)

    def test_cpV_T_English(self):
        stm.englishUnits = True
        temperature, specificHeatCompare = Data.getOneDimensionalTestData('EnglishUnits_cpV_T.npz')
        specificHeat = Data.calculatePropertyFromOneDimension(stm.cpV_T, temperature)
        np.testing.assert_array_almost_equal(specificHeat, specificHeatCompare, decimal=2)

    def test_cpV_T_error(self):
        self.assertAlmostEqual(stm.cpV_T(-1.0), 2015.0, places=1)

class Test_cpL_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_cpL_T(self):
        temperature, specificHeatCompare = Data.getOneDimensionalTestData('SIUnits_cpL_T.npz')
        specificHeat = Data.calculatePropertyFromOneDimension(stm.cpL_T, temperature)
        np.testing.assert_array_almost_equal(specificHeat, specificHeatCompare, decimal=2)

    def test_cpL_T_English(self):
        stm.englishUnits = True
        temperature, specificHeatCompare = Data.getOneDimensionalTestData('EnglishUnits_cpL_T.npz')
        specificHeat = Data.calculatePropertyFromOneDimension(stm.cpL_T, temperature)
        np.testing.assert_array_almost_equal(specificHeat, specificHeatCompare, decimal=2)

    def test_cpL_T_error(self):
        self.assertAlmostEqual(stm.cpL_T(-1.0), 2015.0, places=1)

class Test_cp_pT(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_cp_pT(self):
        pressure, temperature, specificHeatCompare = Data.getTwoDimensionalTestData('SIUnits_cp_pT.npz')
        specificHeat = Data.calculatePropertyFromTwoDimensions(stm.cp_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(specificHeat, specificHeatCompare, decimal=2)

    def test_cp_pT_English(self):
        stm.englishUnits = True
        pressure, temperature, specificHeatCompare = Data.getTwoDimensionalTestData('EnglishUnits_cp_pT.npz')
        specificHeat = Data.calculatePropertyFromTwoDimensions(stm.cp_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(specificHeat, specificHeatCompare, decimal=2)

    def test_cp_pT_error(self):
        self.assertAlmostEqual(stm.cp_pT(1.0, -1.0), 2015.0, places=2)

@unittest.skip('Speeding up')
class Test_cp_ph(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_cp_ph(self):
        pressure, enthalpy, specificHeatCompare = Data.getTwoDimensionalTestData('SIUnits_cp_ph.npz')
        specificHeat = Data.calculatePropertyFromTwoDimensions(stm.cp_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(specificHeat, specificHeatCompare, decimal=2)

    def test_cp_ph_English(self):
        stm.englishUnits = True
        pressure, enthalpy, specificHeatCompare = Data.getTwoDimensionalTestData('EnglishUnits_cp_ph.npz')
        specificHeat = Data.calculatePropertyFromTwoDimensions(stm.cp_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(specificHeat, specificHeatCompare, decimal=2)

    def test_cp_ph_error(self):
        self.assertAlmostEqual(stm.cp_ph(1.0, -1.0), 2015.0, places=2)

class Test_cp_ps(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_cp_ps(self):
        pressure, entropy, specificHeatCompare = Data.getTwoDimensionalTestData('SIUnits_cp_ps.npz')
        specificHeat = Data.calculatePropertyFromTwoDimensions(stm.cp_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(specificHeat, specificHeatCompare, decimal=2)

    def test_cp_ps_English(self):
        stm.englishUnits = True
        pressure, entropy, specificHeatCompare = Data.getTwoDimensionalTestData('EnglishUnits_cp_ps.npz')
        specificHeat = Data.calculatePropertyFromTwoDimensions(stm.cp_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(specificHeat, specificHeatCompare, decimal=2)

    def test_cp_ps_error(self):
        self.assertAlmostEqual(stm.cp_ps(1.0, -1.0), 2015.0, places=2)

class Test_cvV_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_cvV_p(self):
        pressure, specificHeatCompare = Data.getOneDimensionalTestData('SIUnits_cvV_p.npz')
        specificHeat = Data.calculatePropertyFromOneDimension(stm.cvV_p, pressure)
        np.testing.assert_array_almost_equal(specificHeat, specificHeatCompare, decimal=2)

    def test_cvV_p_English(self):
        stm.englishUnits = True
        pressure, specificHeatCompare = Data.getOneDimensionalTestData('EnglishUnits_cvV_p.npz')
        specificHeat = Data.calculatePropertyFromOneDimension(stm.cvV_p, pressure)
        np.set_printoptions(threshold=np.nan)
        np.testing.assert_array_almost_equal(specificHeat, specificHeatCompare, decimal=2)

    def test_cvV_p_error(self):
        self.assertAlmostEqual(stm.cvV_p(-1.0), 2015.0, places=1)

if __name__ == '__main__':
    unittest.main()
