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

class Test_Pr_pT(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_Pr_pT(self):
        pressure, temperature, prandtlCompare = Data.getTwoDimensionalTestData('SIUnits_Pr_pT.npz')
        prandtl = Data.calculatePropertyFromTwoDimensions(stm.Pr_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(prandtl, prandtlCompare, decimal=1)

    def test_Pr_pT_English(self):
        stm.englishUnits = True
        pressure, temperature, prandtlCompare = Data.getTwoDimensionalTestData('EnglishUnits_Pr_pT.npz')
        prandtl = Data.calculatePropertyFromTwoDimensions(stm.Pr_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(prandtl, prandtlCompare, decimal=1)

    def test_Pr_pT_error(self):
        self.assertAlmostEqual(stm.Pr_pT(-1.0, -1.0), 2015.0, places=2)

class Test_Pr_ph(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_Pr_ph(self):
        pressure, enthalpy, prandtlCompare = Data.getTwoDimensionalTestData('SIUnits_Pr_ph.npz')
        prandtl = Data.calculatePropertyFromTwoDimensions(stm.Pr_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(prandtl, prandtlCompare, decimal=0)

    def test_Pr_ph_English(self):
        stm.englishUnits = True
        pressure, enthalpy, prandtlCompare = Data.getTwoDimensionalTestData('EnglishUnits_Pr_ph.npz')
        prandtl = Data.calculatePropertyFromTwoDimensions(stm.Pr_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(prandtl, prandtlCompare, decimal=0)

    def test_Pr_ph_error(self):
        self.assertAlmostEqual(stm.Pr_ph(-1.0, -1.0), 2015.0, places=2)

if __name__ == '__main__':
    unittest.main()