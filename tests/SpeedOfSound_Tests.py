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

class Test_wV_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_wV_p(self):
        pressure, speedOfSoundCompare = Data.getOneDimensionalTestData('SIUnits_wV_p.npz')
        speedOfSound = Data.calculatePropertyFromOneDimension(stm.wV_p, pressure)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_wV_p_English(self):
        stm.englishUnits = True
        pressure, speedOfSoundCompare = Data.getOneDimensionalTestData('EnglishUnits_wV_p.npz')
        speedOfSound = Data.calculatePropertyFromOneDimension(stm.wV_p, pressure)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_wV_p_error(self):
        self.assertAlmostEqual(stm.wV_p(-1.0), 2015.0, places=2)

class Test_wL_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_wL_p(self):
        pressure, speedOfSoundCompare = Data.getOneDimensionalTestData('SIUnits_wL_p.npz')
        speedOfSound = Data.calculatePropertyFromOneDimension(stm.wL_p, pressure)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_wL_p_English(self):
        stm.englishUnits = True
        pressure, speedOfSoundCompare = Data.getOneDimensionalTestData('EnglishUnits_wL_p.npz')
        speedOfSound = Data.calculatePropertyFromOneDimension(stm.wL_p, pressure)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_wL_p_error(self):
        self.assertAlmostEqual(stm.wL_p(-1.0), 2015.0, places=2)

class Test_wV_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_wV_T(self):
        temperature, speedOfSoundCompare = Data.getOneDimensionalTestData('SIUnits_wV_T.npz')
        speedOfSound = Data.calculatePropertyFromOneDimension(stm.wV_T, temperature)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_wV_T_English(self):
        stm.englishUnits = True
        temperature, speedOfSoundCompare = Data.getOneDimensionalTestData('EnglishUnits_wV_T.npz')
        speedOfSound = Data.calculatePropertyFromOneDimension(stm.wV_T, temperature)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_wV_T_error(self):
        self.assertAlmostEqual(stm.wV_T(-1.0), 2015.0, places=2)

class Test_wL_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_wL_T(self):
        temperature, speedOfSoundCompare = Data.getOneDimensionalTestData('SIUnits_wL_T.npz')
        speedOfSound = Data.calculatePropertyFromOneDimension(stm.wL_T, temperature)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_wL_T_English(self):
        stm.englishUnits = True
        temperature, speedOfSoundCompare = Data.getOneDimensionalTestData('EnglishUnits_wL_T.npz')
        speedOfSound = Data.calculatePropertyFromOneDimension(stm.wL_T, temperature)
        np.testing.assert_array_almost_equal(speedOfSound, speedOfSoundCompare, decimal=2)

    def test_wL_T_error(self):
        self.assertAlmostEqual(stm.wL_T(-1.0), 2015.0, places=2)

if __name__ == '__main__':
    unittest.main()
