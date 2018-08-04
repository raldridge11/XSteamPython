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

if __name__ == '__main__':
    unittest.main()