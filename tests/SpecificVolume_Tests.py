# -*- coding: utf-8 -*-
'''
Unit tests for Specific Volume functions
'''
import unittest

import numpy as np

import Data
import XSteamPython as stm

class Test_vV_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_vV_p(self):
        pressure, specificVolumeCompare = Data.getOneDimensionalTestData('SIUnits_vV_p.npz')
        specificVolume = Data.calculatePropertyFromOneDimension(stm.vV_p, pressure)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_vV_p_English(self):
        stm.englishUnits = True
        pressure, specificVolumeCompare = Data.getOneDimensionalTestData('EnglishUnits_vV_p.npz')
        specificVolume = Data.calculatePropertyFromOneDimension(stm.vV_p, pressure)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_vV_p_error(self):
        self.assertAlmostEqual(stm.vV_p(-1.0), 2015.0, places=2)

class Test_vL_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_vL_p(self):
        pressure, specificVolumeCompare = Data.getOneDimensionalTestData('SIUnits_vL_p.npz')
        specificVolume = Data.calculatePropertyFromOneDimension(stm.vL_p, pressure)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_vL_p_English(self):
        stm.englishUnits = True
        pressure, specificVolumeCompare = Data.getOneDimensionalTestData('EnglishUnits_vL_p.npz')
        specificVolume = Data.calculatePropertyFromOneDimension(stm.vL_p, pressure)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_vL_p_error(self):
        self.assertAlmostEqual(stm.vL_p(-1.0), 2015.0, places=2)

class Test_vV_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_vV_T(self):
        temperature, specificVolumeCompare = Data.getOneDimensionalTestData('SIUnits_vV_T.npz')
        specificVolume = Data.calculatePropertyFromOneDimension(stm.vV_T, temperature)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_vV_T_English(self):
        stm.englishUnits = True
        temperature, specificVolumeCompare = Data.getOneDimensionalTestData('EnglishUnits_vV_T.npz')
        specificVolume = Data.calculatePropertyFromOneDimension(stm.vV_T, temperature)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_vV_T_error(self):
        self.assertAlmostEqual(stm.vV_T(-1.0), 2015.0, places=2)

class Test_vL_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_vL_T(self):
        temperature, specificVolumeCompare = Data.getOneDimensionalTestData('SIUnits_vL_T.npz')
        specificVolume = Data.calculatePropertyFromOneDimension(stm.vL_T, temperature)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_vL_T_English(self):
        stm.englishUnits = True
        temperature, specificVolumeCompare = Data.getOneDimensionalTestData('EnglishUnits_vL_T.npz')
        specificVolume = Data.calculatePropertyFromOneDimension(stm.vL_T, temperature)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_vL_T_error(self):
        self.assertAlmostEqual(stm.vL_T(-1.0), 2015.0, places=2)

class Test_v_pT(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_v_pT(self):
        pressure, temperature, specificVolumeCompare = Data.getTwoDimensionalTestData('SIUnits_v_pT.npz')
        specificVolume = Data.calculatePropertyFromTwoDimensions(stm.v_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_v_pT_English(self):
        stm.englishUnits = True
        pressure, temperature, specificVolumeCompare = Data.getTwoDimensionalTestData('EnglishUnits_v_pT.npz')
        specificVolume = Data.calculatePropertyFromTwoDimensions(stm.v_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_v_pT_error(self):
        self.assertAlmostEqual(stm.v_pT(-1.0, -1.0), 2015.0, places=2)

class Test_v_ph(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_v_ph(self):
        pressure, enthalpy, specificVolumeCompare = Data.getTwoDimensionalTestData('SIUnits_v_ph.npz')
        specificVolume = Data.calculatePropertyFromTwoDimensions(stm.v_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_v_ph_English(self):
        stm.englishUnits = True
        pressure, enthalpy, specificVolumeCompare = Data.getTwoDimensionalTestData('EnglishUnits_v_ph.npz')
        specificVolume = Data.calculatePropertyFromTwoDimensions(stm.v_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_v_ph_error(self):
        self.assertAlmostEqual(stm.v_ph(-1.0, -1.0), 2015.0, places=2)

class Test_v_ps(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_v_ps(self):
        pressure, entropy, specificVolumeCompare = Data.getTwoDimensionalTestData('SIUnits_v_ps.npz')
        specificVolume = Data.calculatePropertyFromTwoDimensions(stm.v_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_v_ps_English(self):
        stm.englishUnits = True
        pressure, entropy, specificVolumeCompare = Data.getTwoDimensionalTestData('EnglishUnits_v_ps.npz')
        specificVolume = Data.calculatePropertyFromTwoDimensions(stm.v_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_v_ps_error(self):
        self.assertAlmostEqual(stm.v_ps(-1.0, -1.0), 2015.0, places=2)

if __name__ == '__main__':
    unittest.main()
