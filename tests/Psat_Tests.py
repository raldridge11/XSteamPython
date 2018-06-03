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

class Test_Psat_T(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_Psat_T(self):
        temperature, PsatCompare = Data.getOneDimensionalTestData(Data.siData, 'Psat_T')
        Psat = Data.calculatePropertyFromOneDimension(stm.Psat_T, temperature)
        np.testing.assert_array_almost_equal(Psat, PsatCompare, decimal=3)

    def test_Psat_T_English(self):
        stm.englishUnits = True
        temperature, PsatCompare = Data.getOneDimensionalTestData(Data.englishData, 'Psat_T')
        Psat = Data.calculatePropertyFromOneDimension(stm.Psat_T, temperature)
        np.testing.assert_array_almost_equal(Psat, PsatCompare, decimal=3)

    def test_Psat_T_error(self):
        self.assertAlmostEqual(stm.Psat_T(0.0), 2015.0, places=2)

if __name__ == '__main__':
    unittest.main()
