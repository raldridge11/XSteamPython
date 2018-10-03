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

if __name__ == '__main__':
    unittest.main()
