# -*- coding: utf-8 -*-
'''
Unit tests for Speed of Sound functions
'''
import unittest

import numpy as np

import Data
import XSteamPython as stm

class Test_wV_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_wV_p(self):
        pressure, speedOfSoundCompare = Data.getOneDimensionalTestData('SIUnits_wV_p.npz')
        speedOfSound = Data.calculatePropertyFromOneDimension(stm.wV_p, pressure)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_wV_p_English(self):
        stm.englishUnits = True
        pressure, speedOfSoundCompare = Data.getOneDimensionalTestData('EnglishUnits_wV_p.npz')
        speedOfSound = Data.calculatePropertyFromOneDimension(stm.wV_p, pressure)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_wV_p_error(self):
        self.assertAlmostEqual(stm.wV_p(-1.0), 2015.0, places=2)

class Test_wL_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_wL_p(self):
        pressure, speedOfSoundCompare = Data.getOneDimensionalTestData('SIUnits_wL_p.npz')
        speedOfSound = Data.calculatePropertyFromOneDimension(stm.wL_p, pressure)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_wL_p_English(self):
        stm.englishUnits = True
        pressure, speedOfSoundCompare = Data.getOneDimensionalTestData('EnglishUnits_wL_p.npz')
        speedOfSound = Data.calculatePropertyFromOneDimension(stm.wL_p, pressure)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_wL_p_error(self):
        self.assertAlmostEqual(stm.wL_p(-1.0), 2015.0, places=2)

class Test_wV_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_wV_T(self):
        temperature, speedOfSoundCompare = Data.getOneDimensionalTestData('SIUnits_wV_T.npz')
        speedOfSound = Data.calculatePropertyFromOneDimension(stm.wV_T, temperature)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_wV_T_English(self):
        stm.englishUnits = True
        temperature, speedOfSoundCompare = Data.getOneDimensionalTestData('EnglishUnits_wV_T.npz')
        speedOfSound = Data.calculatePropertyFromOneDimension(stm.wV_T, temperature)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_wV_T_error(self):
        self.assertAlmostEqual(stm.wV_T(-1.0), 2015.0, places=2)

class Test_wL_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_wL_T(self):
        temperature, speedOfSoundCompare = Data.getOneDimensionalTestData('SIUnits_wL_T.npz')
        speedOfSound = Data.calculatePropertyFromOneDimension(stm.wL_T, temperature)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_wL_T_English(self):
        stm.englishUnits = True
        temperature, speedOfSoundCompare = Data.getOneDimensionalTestData('EnglishUnits_wL_T.npz')
        speedOfSound = Data.calculatePropertyFromOneDimension(stm.wL_T, temperature)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_wL_T_error(self):
        self.assertAlmostEqual(stm.wL_T(-1.0), 2015.0, places=2)

class Test_w_pT(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_w_pT(self):
        pressure, temperature, speedOfSoundCompare = Data.getTwoDimensionalTestData('SIUnits_w_pT.npz')
        speedOfSound = Data.calculatePropertyFromTwoDimensions(stm.w_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_w_pT_English(self):
        stm.englishUnits = True
        pressure, temperature, speedOfSoundCompare = Data.getTwoDimensionalTestData('EnglishUnits_w_pT.npz')
        speedOfSound = Data.calculatePropertyFromTwoDimensions(stm.w_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_w_pT_error(self):
        self.assertAlmostEqual(stm.w_pT(1.0, -1.0), 2015.0, places=2)

class Test_w_ph(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_w_ph(self):
        pressure, enthalpy, speedOfSoundCompare = Data.getTwoDimensionalTestData('SIUnits_w_ph.npz')
        speedOfSound = Data.calculatePropertyFromTwoDimensions(stm.w_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=0)

    def test_w_ph_English(self):
        stm.englishUnits = True
        pressure, enthalpy, speedOfSoundCompare = Data.getTwoDimensionalTestData('EnglishUnits_w_ph.npz')
        speedOfSound = Data.calculatePropertyFromTwoDimensions(stm.w_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_w_ph_error(self):
        self.assertAlmostEqual(stm.w_ph(1.0, -1.0), 2015.0, places=2)

class Test_w_ps(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_w_ps(self):
        pressure, entropy, speedOfSoundCompare = Data.getTwoDimensionalTestData('SIUnits_w_ps.npz')
        speedOfSound = Data.calculatePropertyFromTwoDimensions(stm.w_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=0)

    def test_w_ps_English(self):
        stm.englishUnits = True
        pressure, entropy, speedOfSoundCompare = Data.getTwoDimensionalTestData('EnglishUnits_w_ps.npz')
        speedOfSound = Data.calculatePropertyFromTwoDimensions(stm.w_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_w_ps_error(self):
        self.assertAlmostEqual(stm.w_ps(1.0, -1.0), 2015.0, places=2)

if __name__ == '__main__':
    unittest.main()
