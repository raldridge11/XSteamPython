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

class Test_T_ph(unittest.TestCase):

    def tearDown(self):

        stm.englishUnits = False

    def test_T_ph(self):
        pressure, enthalpy, temperatureCompare = Data.getTwoDimensionalTestData(Data.siData, 'T_ph')
        temperature = Data.calculatePropertyFromTwoDimensions(stm.T_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_ph_English(self):
        stm.englishUnits = True
        pressure, enthalpy, temperatureCompare = Data.getTwoDimensionalTestData(Data.englishData, 'T_ph')
        temperature = Data.calculatePropertyFromTwoDimensions(stm.T_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_ph_error(self):
        self.assertAlmostEqual(stm.T_ph(-1, -1), 2015.0, places=2)

class Test_T_ps(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_T_ps(self):
        pressure, entropy, temperatureCompare = Data.getTwoDimensionalTestData(Data.siData, 'T_ps')
        temperature = Data.calculatePropertyFromTwoDimensions(stm.T_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_ps_English(self):
        stm.englishUnits = True
        pressure, entropy, temperatureCompare = Data.getTwoDimensionalTestData(Data.englishData, 'T_ps')
        temperature = Data.calculatePropertyFromTwoDimensions(stm.T_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_ps_error(self):
        self.assertAlmostEqual(stm.T_ps(1.0, -1.0), 2015.0, places=2)

class Test_T_hs(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_T_hs(self):
        enthalpy, entropy, temperatureCompare = Data.getTwoDimensionalTestData(Data.siData, 'T_hs')
        temperature = Data.calculatePropertyFromTwoDimensions(stm.T_hs, enthalpy, entropy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_English(self):
        stm.englishUnits = True
        enthalpy, entropy, temperatureCompare = Data.getTwoDimensionalTestData(Data.englishData, 'T_hs')
        temperature = Data.calculatePropertyFromTwoDimensions(stm.T_hs, enthalpy, entropy)
        np.testing.assert_array_almost_equal(temperature, temperatureCompare, decimal=2)

    def test_T_hs_error(self):
        self.assertAlmostEqual(stm.T_hs(1.0, 1.0), 2015.0, places=2)

if __name__ == '__main__':
    unittest.main()
