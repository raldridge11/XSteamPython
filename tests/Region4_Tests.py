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

import Region4

class Test_Region4(unittest.TestCase):

    def test_t4_p(self):
        self.assertAlmostEqual(Region4.t4_p(10.0), 584.149, places=3)

    def test_p4_t(self):
        self.assertAlmostEqual(Region4.p4_t(550.0), 6.117, places=3)

    def test_h4_s_regionhl1_s(self):
        self.assertAlmostEqual(Region4.h4_s(1.0), 308.551, places=3)

    def test_h4_s_regionhl3_s(self):
        self.assertAlmostEqual(Region4.h4_s(4.0), 1816.891, places=3)

    def test_h4_s_regionhv2c3b_s(self):
        self.assertAlmostEqual(Region4.h4_s(5.0), 2451.624, places=3)

    def test_h4_s_region4(self):
        self.assertAlmostEqual(Region4.h4_s(6.0), 2796.509, places=3)

    def test_h4_s_exception(self):
        self.assertRaises(ArithmeticError, Region4.h4_s, 100.0)

    def test_p4_s_region1(self):
        self.assertAlmostEqual(Region4.p4_s(1.0), 0.037, places=3)

    def test_p4_s_region2(self):
        self.assertAlmostEqual(Region4.p4_s(4.0), 19.809, places=3)

    def test_p4_s_region3(self):
        self.assertAlmostEqual(Region4.p4_s(6.0), 4.710, places=3)

    def test_p4_s_exception(self):
        self.assertRaises(ArithmeticError, Region4.p4_s, 100.0)

    def test_h4_p_phaseException(self):
        self.assertRaises(AttributeError, Region4.h4_p, 22.0, 'dumb')

    def test_h4_p_liq_region1(self):
        self.assertAlmostEqual(Region4.h4_p(15.0, 'liq'), 1610.152, places=3)

    def test_h4_p_liq_region2(self):
        self.assertAlmostEqual(Region4.h4_p(17.0, 'liq'), 1690.036, places=3)

    def test_h4_p_liq_exception(self):
        self.assertRaises(ArithmeticError, Region4.h4_p, 23.0, 'liq')

    def test_h4_p_vap_region1(self):
        self.assertAlmostEqual(Region4.h4_p(15.0, 'vap'), 2610.865, places=3)

    def test_h4_p_vap_region2(self):
        self.assertAlmostEqual(Region4.h4_p(17.0, 'vap'), 2547.413, places=3)

    def test_h4_p_vap_exception(self):
        self.assertRaises(ArithmeticError, Region4.h4_p, 23.0, 'vap')

    def test_t4_hs_region1(self):
        self.assertAlmostEqual(Region4.t4_hs(2000.0, 6.0), 338.379, places=3)

    def test_t4_hs_region2(self):
        self.assertAlmostEqual(Region4.t4_hs(1000.0, 1.0), 505.232, places=3)

    def test_t4_hs_region3(self):
        self.assertAlmostEqual(Region4.t4_hs(1500.0, 4.0), 403.155, places=3)

    def test_t4_hs_exception(self):
        self.assertRaises(ArithmeticError, Region4.t4_hs, 100.0, 100.0)

    def test_x4_ph_liquid(self):
        self.assertEqual(Region4.x4_ph(15.0, 1000.0), 0.0)

    def test_x4_ph_vapor(self):
        self.assertEqual(Region4.x4_ph(15.0, 3000.0), 1.0)

    def test_x4_ph_mix(self):
        self.assertAlmostEqual(Region4.x4_ph(15.0, 2000.0), 0.390, places=3)

    def test_x4_ps_region1_liquid(self):
        self.assertEqual(Region4.x4_ps(15.0, 1.0), 0.0)

    def test_x4_ps_region1_vapor(self):
        self.assertEqual(Region4.x4_ps(15.0, 6.0), 1.0)

    def test_x4_ps_region1_mix(self):
        self.assertAlmostEqual(Region4.x4_ps(15.0, 4.0), 0.194, places=3)

    def test_x4_ps_region2_liquid(self):
        self.assertEqual(Region4.x4_ps(17.0, 1.0), 0.0)

    def test_x4_ps_region2_vapor(self):
        self.assertEqual(Region4.x4_ps(17.0, 6.0), 1.0)

    def test_x4_ps_region2_mix(self):
        self.assertAlmostEqual(Region4.x4_ps(17.0, 4.0), 0.140, places=3)

if __name__ == '__main__':
    unittest.main()
