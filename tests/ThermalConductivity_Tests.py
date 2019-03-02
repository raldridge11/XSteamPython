# -*- coding: utf-8 -*-
'''
Unit tests for Thermal Conductivity functions
'''
import unittest

import numpy as np

import Data
import XSteamPython as stm

class Test_tcL_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_tcL_p(self):
        pressure, conductivityCompare = Data.getOneDimensionalTestData('SIUnits_tcL_p.npz')
        conductivity = Data.calculatePropertyFromOneDimension(stm.tcL_p, pressure)
        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=2)

    def test_tcL_p_English(self):
        stm.englishUnits = True
        pressure, conductivityCompare = Data.getOneDimensionalTestData('EnglishUnits_tcL_p.npz')
        conductivity = Data.calculatePropertyFromOneDimension(stm.tcL_p, pressure)
        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=2)

    def test_tcL_p_error(self):
        self.assertAlmostEqual(stm.tcL_p(-1.0), 2015.0, places=1)

class Test_tcV_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_tcV_p(self):
        pressure, conductivityCompare = Data.getOneDimensionalTestData('SIUnits_tcV_p.npz')
        conductivity = Data.calculatePropertyFromOneDimension(stm.tcV_p, pressure)
        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=2)

    def test_tcV_p_English(self):
        stm.englishUnits = True
        pressure, conductivityCompare = Data.getOneDimensionalTestData('EnglishUnits_tcV_p.npz')
        conductivity = Data.calculatePropertyFromOneDimension(stm.tcV_p, pressure)
        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=2)

    def test_tcV_p_error(self):
        self.assertAlmostEqual(stm.tcV_p(-1.0), 2015.0, places=1)

class Test_tcL_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_tcL_T(self):
        temperature, conductivityCompare = Data.getOneDimensionalTestData('SIUnits_tcL_T.npz')
        conductivity = Data.calculatePropertyFromOneDimension(stm.tcL_T, temperature)
        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=2)

    def test_tcL_T_English(self):
        stm.englishUnits = True
        temperature, conductivityCompare = Data.getOneDimensionalTestData('EnglishUnits_tcL_T.npz')
        conductivity = Data.calculatePropertyFromOneDimension(stm.tcL_T, temperature)

        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=2)

    def test_tcL_T_error(self):
        self.assertAlmostEqual(stm.tcL_T(-1.0), 2015.0, places=1)

class Test_tc_pT(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_tc_pT(self):
        pressure, temperature, conductivityCompare = Data.getTwoDimensionalTestData('SIUnits_tc_pT.npz')
        conductivity = Data.calculatePropertyFromTwoDimensions(stm.tc_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=2)

    def test_tc_pT_English(self):
        stm.englishUnits = True
        pressure, temperature, conductivityCompare = Data.getTwoDimensionalTestData('EnglishUnits_tc_pT.npz')
        conductivity = Data.calculatePropertyFromTwoDimensions(stm.tc_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=2)

    def test_tc_pT_error(self):
        self.assertAlmostEqual(stm.tc_pT(-1.0, -1.0), 2015.0, places=2)

class Test_tc_ph(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_tc_ph(self):
        pressure, enthalpy, conductivityCompare = Data.getTwoDimensionalTestData('SIUnits_tc_ph.npz')
        conductivity = Data.calculatePropertyFromTwoDimensions(stm.tc_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=1)

    def test_tc_ph_English(self):
        stm.englishUnits = True
        pressure, enthalpy, conductivityCompare = Data.getTwoDimensionalTestData('EnglishUnits_tc_ph.npz')
        conductivity = Data.calculatePropertyFromTwoDimensions(stm.tc_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=1)

    def test_tc_ph_error(self):
        self.assertAlmostEqual(stm.tc_ph(-1.0, -1.0), 2015.0, places=2)

class Test_tc_hs(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_tc_hs(self):
        entropy, enthalpy, conductivityCompare = Data.getTwoDimensionalTestData('SIUnits_tc_hs.npz')
        conductivity = Data.calculatePropertyFromTwoDimensions(stm.tc_hs, enthalpy, entropy)
        np.testing.assert_array_almost_equal(conductivity.T, conductivityCompare, decimal=1)

    def test_tc_hs_English(self):
        stm.englishUnits = True
        entropy, enthalpy, conductivityCompare = Data.getTwoDimensionalTestData('EnglishUnits_tc_hs.npz')
        conductivity = Data.calculatePropertyFromTwoDimensions(stm.tc_hs, enthalpy, entropy)
        np.testing.assert_array_almost_equal(conductivity.T, conductivityCompare, decimal=1)

    def test_tc_hs_error(self):
        self.assertAlmostEqual(stm.tc_hs(-1.0, -1.0), 2015.0, places=2)

if __name__ == '__main__':
    unittest.main()
