# -*- coding: utf-8 -*-
'''
* Water and steam properties according to IAPWS IF-97
* By Magnus Holmgren, www.x-eng.com
* The steam tables are free and provided as is.
* We take no responsibilities for any errors in the code or damage thereby.
* You are free to use, modify and distribute the code as long as authorship is properly acknowledged.
* Please notify me at magnus@x-eng.com if the code is used in commercial applications
'''
import os
import sys
import unittest

import numpy as np

file_directory = os.path.dirname(__file__)
src_path = os.path.join(os.path.abspath(file_directory), "..", "XSteamPython")
sys.path.append(src_path)
import Data
import Viscosity
import XSteamPython as stm

class Test_my_AllRegions_pT(unittest.TestCase):

    def test_my_allregions_pT_region1(self):
        self.assertAlmostEqual(Viscosity.my_allregions_pT(1.0, 300.0),0.0008535, places=7)

    def test_my_allregions_pT_region2(self):
        self.assertAlmostEqual(Viscosity.my_allregions_pT(1.0, 500.0), 1.71e-5, places=7)

    def test_my_allregions_pT_region3(self):
        self.assertAlmostEqual(Viscosity.my_allregions_pT(19.0, 640.0), 2.54e-5, places=7)

    def test_my_allregions_pT_region4(self):
        self.assertAlmostEqual(Viscosity.my_allregions_pT(2.63890, 500.0), 0.0, places=7)

    def test_my_allregions_pT_region5(self):
        self.assertAlmostEqual(Viscosity.my_allregions_pT(9.0, 1100.0), 4.18e-5, places=7)

    def test_my_allregions_pT_invalid_area(self):
        self.assertEqual(Viscosity.my_allregions_pT(9.0, 2000.0), 2015.0)
        self.assertEqual(Viscosity.my_allregions_pT(350.0, 900.0), 2015.0)
        self.assertEqual(Viscosity.my_allregions_pT(400.0, 500.0), 2015.0)
        self.assertEqual(Viscosity.my_allregions_pT(600.0, 300.0), 2015.0)

class Test_my_AllRegions_ph(unittest.TestCase):

    def test_my_allregions_ph_region1(self):
        self.assertAlmostEqual(Viscosity.my_allregions_ph(1.0, 100.0), 0.000918, places=6)

    def test_my_allregions_ph_region2(self):
        self.assertAlmostEqual(Viscosity.my_allregions_ph(1.0, 4000.0), 3.79e-5, places=7)
    
    def test_my_allregions_ph_region3(self):
        self.assertAlmostEqual(Viscosity.my_allregions_ph(19.0, 2500.0), 2.58e-5, places=7)
    
    def test_my_allregions_ph_region4(self):
        self.assertAlmostEqual(Viscosity.my_allregions_ph(1.0, 1000.0), 1.33e-5, places=7)

    def test_my_allregions_ph_region5(self):
        self.assertAlmostEqual(Viscosity.my_allregions_ph(1.0, 4250.0), 4.19e-5, places=7)

    def test_my_ph_invalid_area(self):
        self.assertEqual(Viscosity.my_allregions_ph(9.0, 6590.0), 2015.0)
        self.assertEqual(Viscosity.my_allregions_ph(350.0, 3490.0), 2015.0)
        self.assertEqual(Viscosity.my_allregions_ph(400.0, 990.0), 2015.0)
        self.assertEqual(Viscosity.my_allregions_ph(600.0, 170.0), 2015.0)

class Test_Check_Valid_Area(unittest.TestCase):

    def test_Invalid_Value_Returns_False(self):
        self.assertFalse(Viscosity.check_valid_area(9.0, 2000.0))
        self.assertFalse(Viscosity.check_valid_area(350.0, 900.0))
        self.assertFalse(Viscosity.check_valid_area(400.0, 500.0))
        self.assertFalse(Viscosity.check_valid_area(600.0, 300.0))

    def test_Valid_Value_Returns_True(self):
        self.assertTrue(Viscosity.check_valid_area(1.0, 100.0))

class Test_my_rhot(unittest.TestCase):

    def test_my_rhot(self):
        self.assertAlmostEqual(Viscosity.my_rhot(997.793, 300.0),0.000853, places=6)

class Test_my_pT(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_my_pT(self):
        pressure, temperature, viscosityCompare = Data.getTwoDimensionalTestData('SIUnits_my_pT.npz')
        viscosity = Data.calculatePropertyFromTwoDimensions(stm.my_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(viscosity, viscosityCompare, decimal=2)

    def test_my_pT_English(self):
        stm.englishUnits = True
        pressure, temperature, viscosityCompare = Data.getTwoDimensionalTestData('EnglishUnits_my_pT.npz')
        viscosity = Data.calculatePropertyFromTwoDimensions(stm.my_pT, pressure, temperature)
        np.testing.assert_array_almost_equal(viscosity, viscosityCompare, decimal=2)

    def test_my_pT_error(self):
        self.assertAlmostEqual(stm.my_pT(-1.0, -1.0), 2015.0, places=2)

class Test_my_ph(unittest.TestCase):

    def tearDown(self):
        stm.englishUnits = False

    def test_my_ph(self):
        pressure, enthalpy, viscosityCompare = Data.getTwoDimensionalTestData('SIUnits_my_ph.npz')
        viscosity = Data.calculatePropertyFromTwoDimensions(stm.my_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(viscosity, viscosityCompare, decimal=2)

    def test_my_ph_English(self):
        stm.englishUnits = True
        pressure, enthalpy, viscosityCompare = Data.getTwoDimensionalTestData('EnglishUnits_my_ph.npz')
        viscosity = Data.calculatePropertyFromTwoDimensions(stm.my_ph, pressure, enthalpy)
        np.testing.assert_array_almost_equal(viscosity, viscosityCompare, decimal=2)

    def test_my_ph_error(self):
        self.assertAlmostEqual(stm.my_ph(-1.0, -1.0), 2015.0, places=2)


if __name__ == '__main__':
    unittest.main()
