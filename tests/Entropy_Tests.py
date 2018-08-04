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

class Test_sV_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_sV_p(self):
        pressure, entropyCompare = Data.getOneDimensionalTestData('SIUnits_sV_p.npz')
        entropy = Data.calculatePropertyFromOneDimension(stm.sV_p, pressure)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_sV_p_English(self):
        stm.englishUnits = True
        pressure, entropyCompare = Data.getOneDimensionalTestData('EnglishUnits_sV_p.npz')
        entropy = Data.calculatePropertyFromOneDimension(stm.sV_p, pressure)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_sV_p_error(self):
        self.assertAlmostEqual(stm.sV_p(-1.0), 2015.0, places=1)

class Test_sL_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_sL_p(self):
        pressure, entropyCompare = Data.getOneDimensionalTestData('SIUnits_sL_p.npz')
        entropy = Data.calculatePropertyFromOneDimension(stm.sL_p, pressure)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_sL_p_English(self):
        stm.englishUnits = True
        pressure, entropyCompare = Data.getOneDimensionalTestData('EnglishUnits_sL_p.npz')
        entropy = Data.calculatePropertyFromOneDimension(stm.sL_p, pressure)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_sL_p_error(self):
        self.assertAlmostEqual(stm.sL_p(-1.0), 2015.0, places=1)

class Test_sV_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_sV_T(self):
        pressure, entropyCompare = Data.getOneDimensionalTestData('SIUnits_sV_T.npz')
        entropy = Data.calculatePropertyFromOneDimension(stm.sV_T, pressure)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_sV_T_English(self):
        stm.englishUnits = True
        pressure, entropyCompare = Data.getOneDimensionalTestData('EnglishUnits_sV_T.npz')
        entropy = Data.calculatePropertyFromOneDimension(stm.sV_T, pressure)
        np.testing.assert_array_almost_equal(entropy, entropyCompare, decimal=2)

    def test_sV_T_error(self):
        self.assertAlmostEqual(stm.sV_T(-1.0), 2015.0, places=1)

if __name__ == '__main__':
    unittest.main()
