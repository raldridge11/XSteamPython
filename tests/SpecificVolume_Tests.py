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
import pprint

import numpy as np

import Data
import XSteamPython as stm

class Test_SpecificVolume(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_vV_p(self):
        pressure, specificVolumeCompare = Data.getOneDimensionalTestData('SIUnits_vV_p.npz')
        specificVolume = Data.calculatePropertyFromOneDimension(stm.vV_p, pressure)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_vV_p_English(self):
        stm.englishUnits = True
        pressure, specificVolumeCompare = Data.getOneDimensionalTestData('EnglishUnits_vV_p.npz')
        specificVolume = Data.calculatePropertyFromOneDimension(stm.vV_p, pressure)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_vV_p_error(self):
        self.assertAlmostEqual(stm.vV_p(-1.0), 2015.0, places=2)

    def test_vL_p(self):
        pressure, specificVolumeCompare = Data.getOneDimensionalTestData('SIUnits_vL_p.npz')
        specificVolume = Data.calculatePropertyFromOneDimension(stm.vL_p, pressure)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_vL_p_English(self):
        stm.englishUnits = True
        pressure, specificVolumeCompare = Data.getOneDimensionalTestData('EnglishUnits_vL_p.npz')
        specificVolume = Data.calculatePropertyFromOneDimension(stm.vL_p, pressure)
        np.testing.assert_array_almost_equal(specificVolume, specificVolumeCompare, decimal=2)

    def test_vL_p_error(self):
        self.assertAlmostEqual(stm.vL_p(-1.0), 2015.0, places=2)

if __name__ == '__main__':
    unittest.main()
