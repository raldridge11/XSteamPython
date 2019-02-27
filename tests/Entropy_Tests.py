# -*- coding: utf-8 -*-
'''
Unit tests for Entropy functions
'''
import unittest

import numpy as np

import Data
import XSteamPython as stm

class Test_sV_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_sV_p(self):
        pressure, entropyCompare = Data.getOneDimensionalTestData('SIUnits_sV_p.npz')
        entropy = Data.calculatePropertyFromOneDimension(stm.sV_p, pressure)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_sV_p_English(self):
        stm.englishUnits = True
        pressure, entropyCompare = Data.getOneDimensionalTestData('EnglishUnits_sV_p.npz')
        entropy = Data.calculatePropertyFromOneDimension(stm.sV_p, pressure)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_sV_p_error(self):
        self.assertAlmostEqual(stm.sV_p(-1.0), 2015.0, places=1)

class Test_sL_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_sL_p(self):
        pressure, entropyCompare = Data.getOneDimensionalTestData('SIUnits_sL_p.npz')
        entropy = Data.calculatePropertyFromOneDimension(stm.sL_p, pressure)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_sL_p_English(self):
        stm.englishUnits = True
        pressure, entropyCompare = Data.getOneDimensionalTestData('EnglishUnits_sL_p.npz')
        entropy = Data.calculatePropertyFromOneDimension(stm.sL_p, pressure)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_sL_p_error(self):
        self.assertAlmostEqual(stm.sL_p(-1.0), 2015.0, places=1)

class Test_sV_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_sV_T(self):
        temperature, entropyCompare = Data.getOneDimensionalTestData('SIUnits_sV_T.npz')
        entropy = Data.calculatePropertyFromOneDimension(stm.sV_T, temperature)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_sV_T_English(self):
        stm.englishUnits = True
        temperature, entropyCompare = Data.getOneDimensionalTestData('EnglishUnits_sV_T.npz')
        entropy = Data.calculatePropertyFromOneDimension(stm.sV_T, temperature)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_sV_T_error(self):
        self.assertAlmostEqual(stm.sV_T(-1.0), 2015.0, places=1)

class Test_sL_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_sL_T(self):
        temperature, entropyCompare = Data.getOneDimensionalTestData('SIUnits_sL_T.npz')
        entropy = Data.calculatePropertyFromOneDimension(stm.sL_T, temperature)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_sL_T_English(self):
        stm.englishUnits = True
        temperature, entropyCompare = Data.getOneDimensionalTestData('EnglishUnits_sL_T.npz')
        entropy = Data.calculatePropertyFromOneDimension(stm.sL_T, temperature)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_sL_T_error(self):
        self.assertAlmostEqual(stm.sL_T(-1.0), 2015.0, places=1)

class Test_s_pT(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_s_pT(self):
        pressure, temperature, entropyCompare = Data.getTwoDimensionalTestData('SIUnits_s_pT.npz')
        entropy = Data.calculatePropertyFromTwoDimensions(stm.s_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_s_pT_English(self):
        stm.englishUnits = True
        pressure, temperature, entropyCompare = Data.getTwoDimensionalTestData('EnglishUnits_s_pT.npz')
        entropy = Data.calculatePropertyFromTwoDimensions(stm.s_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_s_pT_error(self):
        self.assertAlmostEqual(stm.s_pT(1.0, -1.0), 2015.0, places=2)

class Test_s_ph(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_s_ph(self):
        pressure, enthalpy, entropyCompare = Data.getTwoDimensionalTestData('SIUnits_s_ph.npz')
        entropy = Data.calculatePropertyFromTwoDimensions(stm.s_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_s_ph_English(self):
        stm.englishUnits = True
        pressure, enthalpy, entropyCompare = Data.getTwoDimensionalTestData('EnglishUnits_s_ph.npz')
        entropy = Data.calculatePropertyFromTwoDimensions(stm.s_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_s_ph_error(self):
        self.assertAlmostEqual(stm.s_ph(1.0, -1.0), 2015.0, places=2)

if __name__ == '__main__':
    unittest.main()
