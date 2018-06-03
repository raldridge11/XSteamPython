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

import Region2

class Test_Region2(unittest.TestCase):

    def test_h2_pt(self):
        self.assertAlmostEqual(Region2.h2_pt(15.0, 1073.15), 4091.326, places=3)

    def test_t2_ph(self):
        self.assertAlmostEqual(Region2.t2_ph(10.0, 4000.0), 1026.313, places=3)

    def test_v2_pt(self):
        self.assertAlmostEqual(Region2.v2_pt(10.0, 600.0), 0.020093, places=6)

    def test_u2_pt(self):
        self.assertAlmostEqual(Region2.u2_pt(10.0, 600.0), 2618.897, places=3)

    def test_s2_pt(self):
        self.assertAlmostEqual(Region2.s2_pt(10.0, 600.0), 5.775, places=3)

    def test_cp2_pt(self):
        self.assertAlmostEqual(Region2.cp2_pt(10.0, 600.0), 5.141, places=3)

    def test_cv2_pt(self):
        self.assertAlmostEqual(Region2.cv2_pt(10.0, 600.0), 2.626, places=3)

    def test_w2_pt(self):
        self.assertAlmostEqual(Region2.w2_pt(10.0, 600.0), 503.347, places=3)

    def test_t2_ps_region1(self):
        self.assertAlmostEqual(Region2.t2_ps(3.9, 1.0), 82.311, places=3)

    def test_t2_ps_region3(self):
        self.assertAlmostEqual(Region2.t2_ps(5.0, 2.0), 555.359, places=3)

    def test_t2_ps_region2(self):
        self.assertAlmostEqual(Region2.t2_ps(5.0, 5.86), 525.436, places=3)

    def test_p2_hs_region1(self):
        self.assertAlmostEqual(Region2.p2_hs(1700.0, 4.0), 175.162, places=3)

    def test_p2_hs_region2(self):
        self.assertAlmostEqual(Region2.p2_hs(2800.0, 5.86), 7.070, places=3)

    def test_p2_hs_region3(self):
        self.assertAlmostEqual(Region2.p2_hs(2800.0, 5.8), 8.415, places=3)

    def test_t2_prho(self):
        self.assertAlmostEqual(Region2.t2_prho(1.01, 5.0), 466.334, places=3)

if __name__ == '__main__':
    unittest.main()
