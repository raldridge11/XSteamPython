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
