# -*- coding: utf-8 -*-
'''
Unit tests for Density functions
'''
import unittest

import numpy as np

import Data
import XSteamPython as stm

class Test_rhoV_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_rhoV_p(self):
        pressure, specificVolumeCompare = Data.getOneDimensionalTestData('SIUnits_vV_p.npz')
        density = Data.calculatePropertyFromOneDimension(stm.rhoV_p, pressure)
        np.testing.assert_array_almost_equal(density, 1.0/specificVolumeCompare, decimal=2)

    def test_rhoV_p_English(self):
        stm.englishUnits = True
        pressure, specificVolumeCompare = Data.getOneDimensionalTestData('EnglishUnits_vV_p.npz')
        density = Data.calculatePropertyFromOneDimension(stm.rhoV_p, pressure)
        np.testing.assert_array_almost_equal(density, 1.0/specificVolumeCompare, decimal=2)

    def test_rhoV_p_error(self):
        self.assertAlmostEqual(stm.rhoV_p(-1.0), 1.0/2015.0, places=2)

class Test_rhoL_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_rhoL_p(self):
        pressure, specificVolumeCompare = Data.getOneDimensionalTestData('SIUnits_vL_p.npz')
        density = Data.calculatePropertyFromOneDimension(stm.rhoL_p, pressure)
        np.testing.assert_array_almost_equal(density, 1.0/specificVolumeCompare, decimal=2)

    def test_rhoL_p_English(self):
        stm.englishUnits = True
        pressure, specificVolumeCompare = Data.getOneDimensionalTestData('EnglishUnits_vL_p.npz')
        density = Data.calculatePropertyFromOneDimension(stm.rhoL_p, pressure)
        np.testing.assert_array_almost_equal(density, 1.0/specificVolumeCompare, decimal=2)

    def test_rhoL_p_error(self):
        self.assertAlmostEqual(stm.rhoL_p(-1.0), 1.0/2015.0, places=2)

class Test_rhoV_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_rhoV_T(self):
        temperature, specificVolumeCompare = Data.getOneDimensionalTestData('SIUnits_vV_T.npz')
        density = Data.calculatePropertyFromOneDimension(stm.rhoV_T, temperature)
        np.testing.assert_array_almost_equal(density, 1.0/specificVolumeCompare, decimal=2)

    def test_rhoV_T_English(self):
        stm.englishUnits = True
        temperature, specificVolumeCompare = Data.getOneDimensionalTestData('EnglishUnits_vV_T.npz')
        density = Data.calculatePropertyFromOneDimension(stm.rhoV_T, temperature)
        np.testing.assert_array_almost_equal(density, 1.0/specificVolumeCompare, decimal=2)

    def test_rhoV_T_error(self):
        self.assertAlmostEqual(stm.rhoV_T(-1.0), 1.0/2015.0, places=2)

class Test_rhoL_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_rhoL_T(self):
        temperature, specificVolumeCompare = Data.getOneDimensionalTestData('SIUnits_vL_T.npz')
        density = Data.calculatePropertyFromOneDimension(stm.rhoL_T, temperature)
        np.testing.assert_array_almost_equal(density, 1.0/specificVolumeCompare, decimal=2)

    def test_rhoL_T_English(self):
        stm.englishUnits = True
        temperature, specificVolumeCompare = Data.getOneDimensionalTestData('EnglishUnits_vL_T.npz')
        density = Data.calculatePropertyFromOneDimension(stm.rhoL_T, temperature)
        np.testing.assert_array_almost_equal(density, 1.0/specificVolumeCompare, decimal=2)

    def test_rhoL_T_error(self):
        self.assertAlmostEqual(stm.rhoL_T(-1.0), 1.0/2015.0, places=2)

class Test_rho_pT(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_rho_pT(self):
        pressure, temperature, specificVolumeCompare = Data.getTwoDimensionalTestData('SIUnits_v_pT.npz')
        density = Data.calculatePropertyFromTwoDimensions(stm.rho_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(density, 1.0/specificVolumeCompare, decimal=2)

    def test_rho_pT_English(self):
        stm.englishUnits = True
        pressure, temperature, specificVolumeCompare = Data.getTwoDimensionalTestData('EnglishUnits_v_pT.npz')
        density = Data.calculatePropertyFromTwoDimensions(stm.rho_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(density, 1.0/specificVolumeCompare, decimal=2)

    def test_rho_pT_error(self):
        self.assertAlmostEqual(stm.rho_pT(-1.0, -1.0), 1.0/2015.0, places=2)

class Test_rho_ph(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_rho_ph(self):
        pressure, enthalpy, specificVolumeCompare = Data.getTwoDimensionalTestData('SIUnits_v_ph.npz')
        density = Data.calculatePropertyFromTwoDimensions(stm.rho_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(density, 1.0/specificVolumeCompare, decimal=2)

    def test_rho_ph_English(self):
        stm.englishUnits = True
        pressure, enthalpy, specificVolumeCompare = Data.getTwoDimensionalTestData('EnglishUnits_v_ph.npz')
        density = Data.calculatePropertyFromTwoDimensions(stm.rho_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(density, 1.0/specificVolumeCompare, decimal=2)

    def test_rho_ph_error(self):
        self.assertAlmostEqual(stm.rho_ph(-1.0, -1.0), 1.0/2015.0, places=2)

class Test_rho_ps(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_rho_ps(self):
        pressure, entropy, specificVolumeCompare = Data.getTwoDimensionalTestData('SIUnits_v_ps.npz')
        density = Data.calculatePropertyFromTwoDimensions(stm.rho_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(density, 1.0/specificVolumeCompare, decimal=1)

    def test_rho_ps_English(self):
        stm.englishUnits = True
        pressure, entropy, specificVolumeCompare = Data.getTwoDimensionalTestData('EnglishUnits_v_ps.npz')
        density = Data.calculatePropertyFromTwoDimensions(stm.rho_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(density, 1.0/specificVolumeCompare, decimal=2)

    def test_rho_ps_error(self):
        self.assertAlmostEqual(stm.rho_ps(-1.0, -1.0), 1.0/2015.0, places=2)

if __name__ == '__main__':
    unittest.main()
