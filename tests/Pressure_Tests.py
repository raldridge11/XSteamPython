# -*- coding: utf-8 -*-
'''
Unit tests for Pressure functions
'''
import unittest

import numpy as np

import Data
import XSteamPython as stm

class Test_P_hs(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_P_hs(self):
        entropy, enthalpy, pressureCompare = Data.getTwoDimensionalTestData('SIUnits_P_hs.npz')
        pressure = Data.calculatePropertyFromTwoDimensions(stm.P_hs, enthalpy, entropy)
        np.testing.assert_array_almost_equal(pressure.T, pressureCompare, decimal=2)

    def test_P_hs_English(self):
        stm.englishUnits = True
        entropy, enthalpy, pressureCompare = Data.getTwoDimensionalTestData('EnglishUnits_P_hs.npz')
        pressure = Data.calculatePropertyFromTwoDimensions(stm.P_hs, enthalpy, entropy)
        np.testing.assert_array_almost_equal(pressure.T, pressureCompare, decimal=2)

    def test_P_hs_error(self):
        self.assertAlmostEqual(stm.P_hs(1.0, -1.0), 2015.0, places=2)

if __name__ == '__main__':
    unittest.main()
