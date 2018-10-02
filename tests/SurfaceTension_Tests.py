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

class Test_st_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_st_p(self):
        pressure, surfaceTensionCompare = Data.getOneDimensionalTestData('SIUnits_st_p.npz')
        surfaceTension = Data.calculatePropertyFromOneDimension(stm.st_p, pressure)
        np.testing.assert_array_almost_equal(surfaceTension, surfaceTensionCompare, decimal=2)

    def test_st_p_English(self):
        stm.englishUnits = True
        pressure, surfaceTensionCompare = Data.getOneDimensionalTestData('EnglishUnits_st_p.npz')
        surfaceTension = Data.calculatePropertyFromOneDimension(stm.st_p, pressure)
        np.testing.assert_array_almost_equal(surfaceTension, surfaceTensionCompare, decimal=2)

    def test_st_p_error(self):
        self.assertAlmostEqual(stm.st_p(-1.0), 2015.0, places=1)

class Test_st_t(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_st_t(self):
        pressure, surfaceTensionCompare = Data.getOneDimensionalTestData('SIUnits_st_t.npz')
        surfaceTension = Data.calculatePropertyFromOneDimension(stm.st_t, pressure)
        np.testing.assert_array_almost_equal(surfaceTension, surfaceTensionCompare, decimal=2)

    def test_st_t_English(self):
        stm.englishUnits = True
        pressure, surfaceTensionCompare = Data.getOneDimensionalTestData('EnglishUnits_st_t.npz')
        surfaceTension = Data.calculatePropertyFromOneDimension(stm.st_t, pressure)
        np.testing.assert_array_almost_equal(surfaceTension, surfaceTensionCompare, decimal=2)

    def test_st_t_error(self):
        self.assertAlmostEqual(stm.st_t(-300.0), 2015.0, places=1)

if __name__ == '__main__':
    unittest.main()
