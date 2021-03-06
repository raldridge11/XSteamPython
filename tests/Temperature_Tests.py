# -*- coding: utf-8 -*-
'''
Unit tests for Temperature functions
'''
import unittest

import numpy as np

import Data
import XSteamPython as stm

class Test_T_ph(unittest.TestCase):

    def tearDown(self):

        stm.englishUnits = False

    def test_T_ph(self):
        pressure, enthalpy, temperatureCompare = Data.getTwoDimensionalTestData('SIUnits_T_ph.npz')
        temperature = Data.calculatePropertyFromTwoDimensions(stm.T_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_ph_English(self):
        stm.englishUnits = True
        pressure, enthalpy, temperatureCompare = Data.getTwoDimensionalTestData('EnglishUnits_T_ph.npz')
        temperature = Data.calculatePropertyFromTwoDimensions(stm.T_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_ph_error(self):
        self.assertAlmostEqual(stm.T_ph(-1, -1), 2015.0, places=2)

class Test_T_ps(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_T_ps(self):
        pressure, entropy, temperatureCompare = Data.getTwoDimensionalTestData('SIUnits_T_ps.npz')
        temperature = Data.calculatePropertyFromTwoDimensions(stm.T_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_ps_English(self):
        stm.englishUnits = True
        pressure, entropy, temperatureCompare = Data.getTwoDimensionalTestData('EnglishUnits_T_ps.npz')
        temperature = Data.calculatePropertyFromTwoDimensions(stm.T_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_ps_error(self):
        self.assertAlmostEqual(stm.T_ps(1.0, -1.0), 2015.0, places=2)

class Test_T_hs(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_T_hs(self):
        enthalpy, entropy, temperatureCompare = Data.getTwoDimensionalTestData('SIUnits_T_hs.npz')
        temperature = Data.calculatePropertyFromTwoDimensions(stm.T_hs, enthalpy, entropy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_hs_English(self):
        stm.englishUnits = True
        enthalpy, entropy, temperatureCompare = Data.getTwoDimensionalTestData('EnglishUnits_T_hs.npz')
        temperature = Data.calculatePropertyFromTwoDimensions(stm.T_hs, enthalpy, entropy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_hs_error(self):
        self.assertAlmostEqual(stm.T_hs(1.0, 1.0), 2015.0, places=2)

if __name__ == '__main__':
    unittest.main()
