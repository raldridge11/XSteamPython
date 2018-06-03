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

import Region1

class Test_Region1(unittest.TestCase):

    def test_h1_pt(self):
        self.assertAlmostEqual(Region1.h1_pt(17.0, 623.15), 1666.589, places=3)

    def test_t1_ph(self):
        self.assertAlmostEqual(Region1.t1_ph(10.0, 100.0), 294.775, places=3)

    def test_v1_pt(self):
        self.assertAlmostEqual(Region1.v1_pt(100.0, 400.0), 0.0010185, places=7)

    def test_u1_pt(self):
        self.assertAlmostEqual(Region1.u1_pt(100.0, 400.0), 501.925, places=3)

    def test_s1_pt(self):
        self.assertAlmostEqual(Region1.s1_pt(100.0, 400.0), 1.519, places=3)

    def test_cp1_pt(self):
        self.assertAlmostEqual(Region1.cp1_pt(100.0, 400.0), 4.0604, places=4)

    def test_cv1_pt(self):
        self.assertAlmostEqual(Region1.cv1_pt(100.0, 400.0), 3.533, places=3)

    def test_w1_pt(self):
        self.assertAlmostEqual(Region1.w1_pt(100.0, 400.0), 1717.663, places=3)

    def test_t1_ps(self):
        self.assertAlmostEqual(Region1.t1_ps(100.0, 2.0), 450.051, places=3)

    def test_p1_hs(self):
        self.assertAlmostEqual(Region1.p1_hs(100.0, 0.2), 44.451, places=3)

    def test_t1_prho(self):
        self.assertAlmostEqual(Region1.t1_prho(100.0, 990.0), 388.110, places=3)

if __name__ == '__main__':
    unittest.main()
