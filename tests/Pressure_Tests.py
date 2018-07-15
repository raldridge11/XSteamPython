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
