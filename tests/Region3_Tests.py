# -*- coding: utf-8 -*-
'''
Unit tests for Region 3 functions
'''
import unittest

import Region3

class Test_Region3_Tests(unittest.TestCase):

    def test_h3_pt(self):
        self.assertAlmostEqual(Region3.h3_pt(21.0, 650.0), 2545.682, places=3)

    def test_t3_ph(self):

        self.assertAlmostEqual(Region3.t3_ph(19.0, 2500.0), 635.926, places=3)

    def test_v3_ph_region3a(self):
        self.assertAlmostEqual(Region3.v3_ph(22.0, 2000.0), 0.002638, places=6)

    def test_v3_ph_region3b(self):
        self.assertAlmostEqual(Region3.v3_ph(22.5, 2089.0), 0.003065, places=6)

    def test_t3_ps_region3a(self):
        self.assertAlmostEqual(Region3.t3_ps(20.0, 4.0), 638.449, places=3)

    def test_t3_ps_region3b(self):
        self.assertAlmostEqual(Region3.t3_ps(20.0, 5.0), 640.118, places=3)

    def test_p3_hs_region3a(self):
        self.assertAlmostEqual(Region3.p3_hs(1900.0, 4.0), 66.314, places=3)

    def test_p3_hs_region3b(self):
        self.assertAlmostEqual(Region3.p3_hs(2200.0, 4.42), 67.465, places=3)

    def test_v3_ps_region3a(self):
        self.assertAlmostEqual(Region3.v3_ps(20.0, 4.0), 0.002010, places=6)

    def test_v3_ps_region3b(self):
        self.assertAlmostEqual(Region3.v3_ps(20.0, 5.0), 0.006262, places=6)

    def test_t3_prho(self):
        self.assertAlmostEqual(Region3.t3_prho(21.0, 148.0), 649.829, places=3)

    def test_p3_rhot(self):
        self.assertAlmostEqual(Region3.p3_rhot(500.0, 644.0), 22.689, places=3)

    def test_u3_rhot(self):
        self.assertAlmostEqual(Region3.u3_rhot(500.0, 644.0), 1792.867, places=3)

    def test_h3_rhot(self):
        self.assertAlmostEqual(Region3.h3_rhot(500.0, 644.0), 1838.244, places=3)

    def test_s3_pt(self):
        self.assertAlmostEqual(Region3.s3_rhot(500.0, 644.0), 4.024, places=3)

    def test_cp3_rhot(self):
        self.assertAlmostEqual(Region3.cp3_rhot(500.0, 644.0), 16.128, places=3)

    def test_cv3_rhot(self):
        self.assertAlmostEqual(Region3.cv3_rhot(500.0, 644.0), 3.278, places=3)

    def test_w3_rhot(self):
        self.assertAlmostEqual(Region3.w3_rhot(500.0, 644.0), 473.134, places=3)

    def test_p3sat_h(self):
        self.assertAlmostEqual(Region3.p3sat_h(2674.95), 11.62, places=2)

    def test_p3sat_s(self):
        self.assertAlmostEqual(Region3.p3sat_s(4.0), 19.809, places=3)

if __name__ == '__main__':
    unittest.main()
