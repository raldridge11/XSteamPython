# -*- coding: utf-8 -*-
'''
Unit tests for Kappa functions
'''
import unittest

import numpy as np

import Data
import XSteamPython as stm

class Test_kappa_pT(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_kappa_pT(self):
        pressure, temperature, kappaCompare = Data.getTwoDimensionalTestData('SIUnits_kappa_pT.npz')
        kappa = Data.calculatePropertyFromTwoDimensions(stm.kappa_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(kappa, kappaCompare, decimal=2)

    def test_kappa_pT_English(self):
        stm.englishUnits = True
        pressure, temperature, kappaCompare = Data.getTwoDimensionalTestData('EnglishUnits_kappa_pT.npz')
        kappa = Data.calculatePropertyFromTwoDimensions(stm.kappa_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(kappa, kappaCompare, decimal=2)

    def test_kappa_pT_error(self):
        self.assertAlmostEqual(stm.kappa_pT(1.0, -1.0), 1.0, places=2)

class Test_kappa_ph(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_kappa_ph(self):
        pressure, temperature, kappaCompare = Data.getTwoDimensionalTestData('SIUnits_kappa_ph.npz')
        kappa = Data.calculatePropertyFromTwoDimensions(stm.kappa_ph, pressure, temperature)
        np.testing.assert_array_almost_equal(kappa, kappaCompare, decimal=2)

    def test_kappa_ph_English(self):
        stm.englishUnits = True
        pressure, temperature, kappaCompare = Data.getTwoDimensionalTestData('EnglishUnits_kappa_ph.npz')
        kappa = Data.calculatePropertyFromTwoDimensions(stm.kappa_ph, pressure, temperature)
        np.testing.assert_array_almost_equal(kappa, kappaCompare, decimal=2)

    def test_kappa_ph_error(self):
        self.assertAlmostEqual(stm.kappa_ph(1.0, -1.0), 1.0, places=2)

if __name__ == '__main__':
    unittest.main()
