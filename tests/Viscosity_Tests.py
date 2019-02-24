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

file_directory = os.path.dirname(__file__)
src_path = os.path.join(os.path.abspath(file_directory), "..", "XSteamPython")
sys.path.append(src_path)
import Viscosity

class Test_my_AllRegions_pT(unittest.TestCase):

    def test_my_pT_region1(self):
        self.assertAlmostEqual(Viscosity.my_allregions_pT(1.0, 300.0),0.0008535, places=7)

    def test_my_pT_region2(self):
        self.assertAlmostEqual(Viscosity.my_allregions_pT(1.0, 500.0), 1.71e-5, places=7)

    def test_my_pT_region3(self):
        self.assertAlmostEqual(Viscosity.my_allregions_pT(19.0, 640.0), 2.54e-5, places=7)

    def test_my_pT_region4(self):
        self.assertAlmostEqual(Viscosity.my_allregions_pT(2.63890, 500.0), 0.0, places=7)

    def test_my_pT_region5(self):
        self.assertAlmostEqual(Viscosity.my_allregions_pT(9.0, 1100.0), 4.18e-5, places=7)

    def test_my_pT_invalid_area(self):
        self.assertEqual(Viscosity.my_allregions_pT(9.0, 2000.0), 2015.0)
        self.assertEqual(Viscosity.my_allregions_pT(350.0, 900.0), 2015.0)
        self.assertEqual(Viscosity.my_allregions_pT(400.0, 500.0), 2015.0)
        self.assertEqual(Viscosity.my_allregions_pT(600.0, 300.0), 2015.0)

if __name__ == '__main__':
    unittest.main()
