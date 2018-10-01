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

class Test_x_ps(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_x_ps(self):
        pressure, entropy, qualityCompare = Data.getTwoDimensionalTestData('SIUnits_x_ps.npz')
        quality = Data.calculatePropertyFromTwoDimensions(stm.x_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(quality, qualityCompare, decimal=2)

    def test_x_ps_English(self):
        stm.englishUnits = True
        pressure, entropy, qualityCompare = Data.getTwoDimensionalTestData('EnglishUnits_x_ps.npz')
        quality = Data.calculatePropertyFromTwoDimensions(stm.x_ps, pressure, entropy)
        np.testing.assert_array_almost_equal(quality, qualityCompare, decimal=2)

    def test_x_ps_error(self):
        self.assertAlmostEqual(stm.x_ps(-1.0, -1.0), 2015.0, places=2)

if __name__ == '__main__':
    unittest.main()
