# -*- coding: utf-8 -*-
'''
Unit tests for Tsat functions
'''
import unittest

import numpy as np

import Data
import XSteamPython as stm

class Test_Tsat_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_Tsat_p(self):
        pressure, TsatCompare = Data.getOneDimensionalTestData('SIUnits_Tsat_p.npz')
        Tsat = Data.calculatePropertyFromOneDimension(stm.Tsat_p, pressure)
        np.testing.assert_array_almost_equal(Tsat, TsatCompare, decimal=3)

    def test_Tsat_p_English(self):
        stm.englishUnits = True
        pressure, TsatCompare = Data.getOneDimensionalTestData('EnglishUnits_Tsat_p.npz')
        Tsat = Data.calculatePropertyFromOneDimension(stm.Tsat_p, pressure)
        np.testing.assert_array_almost_equal(Tsat, TsatCompare, decimal=3)

    def test_Tsat_p_error(self):
        self.assertAlmostEqual(stm.Tsat_p(23000.0), 2015.0, places=2)

class Test_Tsat_s(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_Tsat_s(self):
        entropy, TsatCompare = Data.getOneDimensionalTestData('SIUnits_Tsat_s.npz')
        Tsat = Data.calculatePropertyFromOneDimension(stm.Tsat_s, entropy)
        np.testing.assert_array_almost_equal(Tsat, TsatCompare, decimal=3)

    def test_Tsat_s_English(self):
        stm.englishUnits = True
        entropy, TsatCompare = Data.getOneDimensionalTestData('EnglishUnits_Tsat_s.npz')
        Tsat = Data.calculatePropertyFromOneDimension(stm.Tsat_s, entropy)
        np.testing.assert_array_almost_equal(Tsat, TsatCompare, decimal=3)

    def test_Tsat_s_error(self):
        self.assertAlmostEqual(stm.Tsat_s(10.0), 2015.0, places=2)

if __name__ == '__main__':
    unittest.main()
