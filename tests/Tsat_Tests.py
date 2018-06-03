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

class Test_Tsat_p(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_Tsat_p(self):
        pressure, TsatCompare = Data.getOneDimensionalTestData(Data.siData, 'Tsat_p')
        Tsat = Data.calculatePropertyFromOneDimension(stm.Tsat_p, pressure)
        np.testing.assert_array_almost_equal(Tsat, TsatCompare, decimal=3)

    def test_Tsat_p_English(self):
        stm.englishUnits = True
        pressure, TsatCompare = Data.getOneDimensionalTestData(Data.englishData, 'Tsat_p')
        Tsat = Data.calculatePropertyFromOneDimension(stm.Tsat_p, pressure)
        np.testing.assert_array_almost_equal(Tsat, TsatCompare, decimal=3)

    def test_Tsat_p_error(self):
        self.assertAlmostEqual(stm.Tsat_p(23000.0), 2015.0, places=2)

class Test_Tsat_s(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_Tsat_s(self):
        entropy, TsatCompare = Data.getOneDimensionalTestData(Data.siData, 'Tsat_s')
        Tsat = Data.calculatePropertyFromOneDimension(stm.Tsat_s, entropy)
        np.testing.assert_array_almost_equal(Tsat, TsatCompare, decimal=3)

    def test_Tsat_s_English(self):
        stm.englishUnits = True
        entropy, TsatCompare = Data.getOneDimensionalTestData(Data.englishData, 'Tsat_s')
        Tsat = Data.calculatePropertyFromOneDimension(stm.Tsat_s, entropy)
        np.testing.assert_array_almost_equal(Tsat, TsatCompare, decimal=3)

    def test_Tsat_s_error(self):
        self.assertAlmostEqual(stm.Tsat_s(10.0), 2015.0, places=2)

if __name__ == '__main__':
    unittest.main()
