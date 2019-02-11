# -*- coding: utf-8 -*-
'''
* Water and steam properties according to IAPWS IF-97
* By Magnus Holmgren, www.x-eng.com
* The steam tables are free and provided as is.
* We take no responsibilities for any errors in the code or damage thereby.
* You are free to use, modify and distribute the code as long as authorship is properly acknowledged.
* Please notify me at magnus@x-eng.com if the code is used in commercial applications
'''
import os
import sys
import unittest
import pprint
file_directory = os.path.dirname(__file__)
src_path = os.path.join(os.path.abspath(file_directory), "..", "XSteamPython")
sys.path.append(src_path)
import numpy as np

import Data
import XSteamPython as stm

class Test_tcL_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_tcL_p(self):
        pressure, conductivityCompare = Data.getOneDimensionalTestData('SIUnits_tcL_p.npz')
        conductivity = Data.calculatePropertyFromOneDimension(stm.tcL_p, pressure)
        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=2)

    def test_tcL_p_English(self):
        stm.englishUnits = True
        pressure, conductivityCompare = Data.getOneDimensionalTestData('EnglishUnits_tcL_p.npz')
        conductivity = Data.calculatePropertyFromOneDimension(stm.tcL_p, pressure)
        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=2)

    def test_tcL_p_error(self):
        self.assertAlmostEqual(stm.tcL_p(-1.0), 2015.0, places=1)

class Test_tcV_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_tcV_p(self):
        pressure, conductivityCompare = Data.getOneDimensionalTestData('SIUnits_tcV_p.npz')
        conductivity = Data.calculatePropertyFromOneDimension(stm.tcV_p, pressure)
        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=2)

    def test_tcV_p_English(self):
        stm.englishUnits = True
        pressure, conductivityCompare = Data.getOneDimensionalTestData('EnglishUnits_tcV_p.npz')
        conductivity = Data.calculatePropertyFromOneDimension(stm.tcV_p, pressure)
        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=2)

    def test_tcV_p_error(self):
        self.assertAlmostEqual(stm.tcV_p(-1.0), 2015.0, places=1)

class Test_tcL_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_tcL_T(self):
        temperature, conductivityCompare = Data.getOneDimensionalTestData('SIUnits_tcL_T.npz')
        conductivity = Data.calculatePropertyFromOneDimension(stm.tcL_T, temperature)
        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=2)

    def test_tcL_T_English(self):
        stm.englishUnits = True
        temperature, conductivityCompare = Data.getOneDimensionalTestData('EnglishUnits_tcL_T.npz')
        conductivity = Data.calculatePropertyFromOneDimension(stm.tcL_T, temperature)

        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=2)

    def test_tcL_T_error(self):
        self.assertAlmostEqual(stm.tcL_T(-1.0), 2015.0, places=1)

class Test_tc_pT(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_tc_pT(self):
        pressure, temperature, conductivityCompare = Data.getTwoDimensionalTestData('SIUnits_tc_pT.npz')
        conductivity = Data.calculatePropertyFromTwoDimensions(stm.tc_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=2)

    def test_tc_pT_English(self):
        stm.englishUnits = True
        pressure, temperature,  conductivityCompare = Data.getTwoDimensionalTestData('EnglishUnits_tc_pT.npz')
        conductivity = Data.calculatePropertyFromTwoDimensions(stm.tc_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(conductivity, conductivityCompare, decimal=2)

    def test_tc_pT_error(self):
        self.assertAlmostEqual(stm.tc_pT(-1.0, -1.0), 2015.0, places=2)

if __name__ == '__main__':
    unittest.main()
