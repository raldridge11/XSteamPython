# -*- coding: utf-8 -*-
'''
Unit tests for Specific Energy functions
'''
import unittest

import numpy as np

import Data
import XSteamPython as stm

class Test_uV_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_uV_p(self):
        pressure, energyCompare = Data.getOneDimensionalTestData('SIUnits_uV_p.npz')
        energy = Data.calculatePropertyFromOneDimension(stm.uV_p, pressure)
        np.testing.assert_array_almost_equal(energy, energyCompare, decimal=2)

    def test_uV_p_English(self):
        stm.englishUnits = True
        pressure, energyCompare = Data.getOneDimensionalTestData('EnglishUnits_uV_p.npz')
        energy = Data.calculatePropertyFromOneDimension(stm.uV_p, pressure)
        np.testing.assert_array_almost_equal(energy, energyCompare, decimal=2)

    def test_uV_p_error(self):
        self.assertAlmostEqual(stm.uV_p(-1.0), 2015.0, places=1)

class Test_uL_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_uL_p(self):
        pressure, energyCompare = Data.getOneDimensionalTestData('SIUnits_uL_p.npz')
        energy = Data.calculatePropertyFromOneDimension(stm.uL_p, pressure)
        np.testing.assert_array_almost_equal(energy, energyCompare, decimal=2)

    def test_uL_p_English(self):
        stm.englishUnits = True
        pressure, energyCompare = Data.getOneDimensionalTestData('EnglishUnits_uL_p.npz')
        energy = Data.calculatePropertyFromOneDimension(stm.uL_p, pressure)
        np.testing.assert_array_almost_equal(energy, energyCompare, decimal=2)

    def test_uL_p_error(self):
        self.assertAlmostEqual(stm.uL_p(-1.0), 2015.0, places=1)

class Test_uV_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_uV_T(self):
        temperature, energyCompare = Data.getOneDimensionalTestData('SIUnits_uV_T.npz')
        energy = Data.calculatePropertyFromOneDimension(stm.uV_T, temperature)
        np.testing.assert_array_almost_equal(energy, energyCompare, decimal=2)

    def test_uV_T_English(self):
        stm.englishUnits = True
        temperature, energyCompare = Data.getOneDimensionalTestData('EnglishUnits_uV_T.npz')
        energy = Data.calculatePropertyFromOneDimension(stm.uV_T, temperature)
        np.testing.assert_array_almost_equal(energy, energyCompare, decimal=2)

    def test_uV_T_error(self):
        self.assertAlmostEqual(stm.uV_T(-1.0), 2015.0, places=1)

class Test_uL_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_uL_T(self):
        temperature, energyCompare = Data.getOneDimensionalTestData('SIUnits_uL_T.npz')
        energy = Data.calculatePropertyFromOneDimension(stm.uL_T, temperature)
        np.testing.assert_array_almost_equal(energy, energyCompare, decimal=2)

    def test_uL_T_English(self):
        stm.englishUnits = True
        temperature, energyCompare = Data.getOneDimensionalTestData('EnglishUnits_uL_T.npz')
        energy = Data.calculatePropertyFromOneDimension(stm.uL_T, temperature)
        np.testing.assert_array_almost_equal(energy, energyCompare, decimal=2)

    def test_uL_T_error(self):
        self.assertAlmostEqual(stm.uL_T(-1.0), 2015.0, places=1)

class Test_u_pT(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_u_pT(self):
        pressure, temperature, energyCompare = Data.getTwoDimensionalTestData('SIUnits_u_pT.npz')
        energy = Data.calculatePropertyFromTwoDimensions(stm.u_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(energy, energyCompare, decimal=2)

    def test_u_pT_English(self):
        stm.englishUnits = True
        pressure, temperature, energyCompare = Data.getTwoDimensionalTestData('EnglishUnits_u_pT.npz')
        energy = Data.calculatePropertyFromTwoDimensions(stm.u_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(energy, energyCompare, decimal=2)

    def test_u_pT_error(self):
        self.assertAlmostEqual(stm.u_pT(1.0, -1.0), 2015.0, places=2)

class Test_u_ph(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_u_ph(self):
        pressure, enthalpy, energyCompare = Data.getTwoDimensionalTestData('SIUnits_u_ph.npz')
        energy = Data.calculatePropertyFromTwoDimensions(stm.u_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(energy, energyCompare, decimal=2)

    def test_u_ph_English(self):
        stm.englishUnits = True
        pressure, enthalpy, energyCompare = Data.getTwoDimensionalTestData('EnglishUnits_u_ph.npz')
        energy = Data.calculatePropertyFromTwoDimensions(stm.u_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(energy, energyCompare, decimal=2)

    def test_u_ph_error(self):
        self.assertAlmostEqual(stm.u_ph(1.0, -1.0), 2015.0, places=2)

class Test_u_ps(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_u_ps(self):
        pressure, entropy, energyCompare = Data.getTwoDimensionalTestData('SIUnits_u_ps.npz')
        energy = Data.calculatePropertyFromTwoDimensions(stm.u_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(energy, energyCompare, decimal=1)

    def test_u_ps_English(self):
        stm.englishUnits = True
        pressure, entropy, energyCompare = Data.getTwoDimensionalTestData('EnglishUnits_u_ps.npz')
        energy = Data.calculatePropertyFromTwoDimensions(stm.u_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(energy, energyCompare, decimal=1)

    def test_u_ps_error(self):
        self.assertAlmostEqual(stm.u_ps(1.0, -1.0), 2015.0, places=1)

if __name__ == '__main__':
    unittest.main()