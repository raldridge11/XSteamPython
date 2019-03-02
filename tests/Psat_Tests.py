# -*- coding: utf-8 -*-
'''
Unit tests for Psat functions
'''
import unittest

import numpy as np

import Data
import XSteamPython as stm

class Test_Psat_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_Psat_T(self):
        temperature, PsatCompare = Data.getOneDimensionalTestData('SIUnits_Psat_T.npz')
        Psat = Data.calculatePropertyFromOneDimension(stm.Psat_T, temperature)
        np.testing.assert_array_almost_equal(Psat, PsatCompare, decimal=3)

    def test_Psat_T_English(self):
        stm.englishUnits = True
        temperature, PsatCompare = Data.getOneDimensionalTestData('EnglishUnits_Psat_T.npz')
        Psat = Data.calculatePropertyFromOneDimension(stm.Psat_T, temperature)
        np.testing.assert_array_almost_equal(Psat, PsatCompare, decimal=3)

    def test_Psat_T_error(self):
        self.assertAlmostEqual(stm.Psat_T(0.0), 2015.0, places=2)

    def test_Psat_s(self):
        entropy, PsatCompare = Data.getOneDimensionalTestData('SIUnits_Psat_s.npz')
        Psat = Data.calculatePropertyFromOneDimension(stm.Psat_s, entropy)
        np.testing.assert_array_almost_equal(Psat, PsatCompare, decimal=3)

    def test_Psat_s_English(self):
        stm.englishUnits = True
        entropy, PsatCompare = Data.getOneDimensionalTestData('EnglishUnits_Psat_s.npz')
        Psat = Data.calculatePropertyFromOneDimension(stm.Psat_s, entropy)
        np.testing.assert_array_almost_equal(Psat, PsatCompare, decimal=3)

    def test_Psat_s_error(self):
        self.assertAlmostEqual(stm.Psat_s(-100.0), 2015.0, places=2)

if __name__ == '__main__':
    unittest.main()
