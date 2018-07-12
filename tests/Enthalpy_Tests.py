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

class Test_Enthalpy(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_hV_p(self):
        pressure, enthalpyCompare = Data.getOneDimensionalTestData('SIUnits_hV_p.npz')
        enthalpy = Data.calculatePropertyFromOneDimension(stm.hV_p, pressure)
        np.testing.assert_array_almost_equal(enthalpy, enthalpyCompare, decimal=2)

    def test_hV_p_English(self):
        stm.englishUnits = True
        pressure, enthalpyCompare = Data.getOneDimensionalTestData('EnglishUnits_hV_p.npz')
        enthalpy = Data.calculatePropertyFromOneDimension(stm.hV_p, pressure)
        np.testing.assert_array_almost_equal(enthalpy, enthalpyCompare, decimal=2)

    def test_hV_p_error(self):
        self.assertAlmostEqual(stm.hV_p(-1.0), 2015.0, places=1)

    def test_hL_p(self):
        pressure, enthalpyCompare = Data.getOneDimensionalTestData('SIUnits_hL_p.npz')
        enthalpy = Data.calculatePropertyFromOneDimension(stm.hL_p, pressure)
        np.testing.assert_array_almost_equal(enthalpy, enthalpyCompare, decimal=2)

    def test_hL_p_English(self):
        stm.englishUnits = True
        pressure, enthalpyCompare = Data.getOneDimensionalTestData('EnglishUnits_hL_p.npz')
        enthalpy = Data.calculatePropertyFromOneDimension(stm.hL_p, pressure)
        np.testing.assert_array_almost_equal(enthalpy, enthalpyCompare, decimal=1)

    def test_hL_p_error(self):
        self.assertAlmostEqual(stm.hL_p(-1.0), 2015.0, places=1)

    def test_hV_T(self):
        temperature, enthalpyCompare = Data.getOneDimensionalTestData('SIUnits_hV_T.npz')
        enthalpy = Data.calculatePropertyFromOneDimension(stm.hV_T, temperature)
        np.testing.assert_array_almost_equal(enthalpy, enthalpyCompare, decimal=2)

    def test_hV_T_English(self):
        stm.englishUnits = True
        temperature, enthalpyCompare = Data.getOneDimensionalTestData('EnglishUnits_hV_T.npz')
        enthalpy = Data.calculatePropertyFromOneDimension(stm.hV_T, temperature)
        np.testing.assert_array_almost_equal(enthalpy, enthalpyCompare, decimal=2)

    def test_hV_T_error(self):
        self.assertAlmostEqual(stm.hV_T(-1.0), 2015.0, places=1)



if __name__ == '__main__':
    unittest.main()