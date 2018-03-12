# -*- coding: utf-8 -*-
import unittest

import XSteamPython as stm

class Test_Conversions(unittest.TestCase):

    def tearDown(self):

        stm.englishUnits = False

    def test_toSIUnit_pressure(self):

        self.assertEqual(stm.toSIUnit(100.0, 'pressure'), 0.1)

    def test_toSIUnit_pressure_English(self):

        stm.englishUnits = True
        self.assertAlmostEqual(stm.toSIUnit(14.7, 'pressure'), 0.1013529, 7)

    def test_fromSIUnit_pressure(self):

        self.assertEqual(stm.fromSIUnit(0.1, 'pressure'), 100.0)

    def test_fromSIUnit_pressure_English(self):

        stm.englishUnits = True
        self.assertAlmostEqual(stm.fromSIUnit(0.1013529, 'pressure'), 14.7, 1)

    def test_toSIUnit_temperature(self):

        self.assertEqual(stm.toSIUnit(100.0, 'temperature'), 373.15)

    def test_toSIUnit_temperature_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.toSIUnit(212.0, 'temperature'), 373.15)

    def test_fromSIUnit_temperature(self):

        self.assertEqual(stm.fromSIUnit(373.15, 'temperature'), 100.0)

    def test_fromSIUnit_temperature_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.fromSIUnit(373.15, 'temperature'), 212.0)

    def test_toSIUnit_entropy_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.toSIUnit(1.0, 'entropy'), 1.0/0.238845896627)

    def test_fromSIUnit_entropy_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.fromSIUnit(1.0, 'entropy'), 0.238845896627)

    def test_toSIUnit_enthalpy_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.toSIUnit(1.0, 'enthalpy'), 2.326)

    def test_fromSIUnit_enthalpy_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.fromSIUnit(1.0, 'enthalpy'), 1.0/2.326)

    def test_toSIUnit_specificVolume_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.toSIUnit(1.0, 'specific volume'), 0.0624279606)

    def test_fromSIUnit_specificVolume_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.fromSIUnit(1.0, 'specific volume'), 1.0/0.0624279606)

    def test_toSIUnit_velocity_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.toSIUnit(1.0, 'velocity'), 0.3048)

    def test_fromSIUnit_velocity_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.fromSIUnit(1.0, 'velocity'), 1.0/0.3048)

    def test_toSIUnit_thermalConductivity_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.toSIUnit(1.0, 'thermal conductivity'), 1.0/0.577789)

    def test_fromSIUnit_thermalConductivity_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.fromSIUnit(1.0, 'thermal conductivity'), 0.577789)

    def test_toSIUnit_surfaceTension_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.toSIUnit(1.0, 'surface tension'), 1.0/0.068521766)

    def test_fromSIUnit_surfaceTension_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.fromSIUnit(1.0, 'surface tension'), 0.068521766)

    def test_toSIUnit_dynamicViscosity_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.toSIUnit(1.0, 'viscosity'), 1.0/2419.088311)

    def test_fromSIUnit_dynamicViscosity_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.fromSIUnit(1.0, 'viscosity'), 2419.088311)

class Test_Tsat_p(unittest.TestCase):

    def tearDown(self):

        stm.englishUnits = False

    def test_Tsat_p(self):

        self.assertAlmostEqual(stm.Tsat_p(101.0), 99.88, places=2)

    def test_Tsat_p_English(self):

        stm.englishUnits = True
        self.assertAlmostEqual(stm.Tsat_p(14.7), 212.0, 1)

    def test_Tsat_p_error(self):

        self.assertRaises(ArithmeticError, stm.Tsat_p, 0.0)

class Test_T_ph(unittest.TestCase):

    def tearDown(self):

        stm.englishUnits = False

    def test_T_ph(self):

        self.assertAlmostEqual(stm.T_ph(100.0, 100.0), 23.84, places=2)

    def test_T_ph_English(self):

        stm.englishUnits = True
        self.assertAlmostEqual(stm.T_ph(1.0, 100.0), 101.69, places=2)

    def test_T_ph_error(self):

        self.assertRaises(ArithmeticError, stm.T_ph, -1, -1)

class Test_region_ph(unittest.TestCase):

    def test_region_ph_pressureOutOfBounds(self):

        self.assertRaises(ArithmeticError, stm.region_ph, 0, 4.0)

    def test_region_ph_enthalpyOutOfBounds(self):

        self.assertRaises(ArithmeticError, stm.region_ph, 1, -1)

    def test_region_ph_region1_bellow3(self):

        self.assertEqual(stm.region_ph(1.0, 100.0), 1)

    def test_region_ph_region1_above3(self):

        self.assertEqual(stm.region_ph(17.0, 1000.0), 1)

    def test_region_ph_region2_bellow3(self):

        self.assertEqual(stm.region_ph(1.0, 4000.0), 2)

    def test_region_ph_region2_above3(self):

        self.assertEqual(stm.region_ph(17.0, 3000.0), 2)

    def test_region_ph_region4_bellow3(self):

        self.assertEqual(stm.region_ph(1.0, 1000.0), 4)

    def test_region_ph_region4_above3(self):

        self.assertEqual(stm.region_ph(17.0, 2000.0), 4)

    def test_region_ph_region5_bellow3(self):

        self.assertEqual(stm.region_ph(1.0, 5000.0), 5)

    def test_region_ph_region3(self):

        self.assertEqual(stm.region_ph(19.0, 2500.0), 3)

class Test_BoundaryFunctions(unittest.TestCase):

    def test_b23t_p(self):

        self.assertAlmostEqual(stm.b23t_p(15.0), 605.11, places=2)

    def test_b23p_t(self):

        self.assertAlmostEqual(stm.b23p_t(100.0), 241.526, places=3)

    def test_hb13_s(self):

        self.assertAlmostEqual(stm.hB13_s(3.0), 1612.0467, places=3)

    def test_tB23_hs(self):

        self.assertAlmostEqual(stm.tB23_hs(1000.0, 3.0), 1611.524, places=3)

class Test_Transport_Properties(unittest.TestCase):

    def test_surfaceTension_T(self):
        self.assertAlmostEqual(stm.surfaceTension_T(100.0),0.09006, places=5)

    def test_surfaceTension_T_Excetpion(self):
        self.assertRaises(ArithmeticError, stm.surfaceTension_T, 0.0)

class Test_tX_p(unittest.TestCase):

    def test_t4_p(self):

        self.assertAlmostEqual(stm.t4_p(10.0), 584.149, places=3)

class Test_pX_t(unittest.TestCase):

    def test_p4_t(self):
        self.assertAlmostEqual(stm.p4_t(550.0), 6.117, places=3)

class Test_hX_s(unittest.TestCase):

    def test_h4_s_regionhl1_s(self):
        self.assertAlmostEqual(stm.h4_s(1.0), 308.551, places=3)

    def test_h4_s_regionhl3_s(self):
        self.assertAlmostEqual(stm.h4_s(4.0), 1816.891, places=3)

    def test_h4_s_regionhv2c3b_s(self):
        self.assertAlmostEqual(stm.h4_s(5.0), 2451.624, places=3)

    def test_h4_s_region4(self):
        self.assertAlmostEqual(stm.h4_s(6.0), 2796.509, places=3)

    def test_h4_s_exception(self):
        self.assertRaises(ArithmeticError, stm.h4_s, 100.0)

class Test_hX_p(unittest.TestCase):

    def test_h4_p_phaseException(self):
        self.assertRaises(AttributeError, stm.h4_p, 22.0, 'dumb')

    def test_h4_p_liq_region1(self):
        self.assertAlmostEqual(stm.h4_p(15.0, 'liq'), 1610.152, places=3)

    def test_h4_p_liq_region2(self):
        self.assertAlmostEqual(stm.h4_p(17.0, 'liq'), 1690.036, places=3)

    def test_h4_p_liq_exception(self):
        self.assertRaises(ArithmeticError, stm.h4_p, 23.0, 'liq')

    def test_h4_p_vap_region1(self):
        self.assertAlmostEqual(stm.h4_p(15.0, 'vap'), 2610.865, places=3)

    def test_h4_p_vap_region2(self):
        self.assertAlmostEqual(stm.h4_p(17.0, 'vap'), 2547.413, places=3)

    def test_h4_p_vap_exception(self):
        self.assertRaises(ArithmeticError, stm.h4_p, 23.0, 'vap')

class Test_hX_pt(unittest.TestCase):

    def test_h1_pt(self):

        self.assertAlmostEqual(stm.h1_pt(17.0, 623.15), 1666.589, places=3)

    def test_h2_pt(self):

        self.assertAlmostEqual(stm.h2_pt(15.0, 1073.15), 4091.326, places=3)

    def test_h3_pt(self):
        self.assertAlmostEqual(stm.h3_pt(21.0, 650.0), 2545.682, places=3)

    def test_h5_pt(self):

        self.assertAlmostEqual(stm.h5_pt(10.0,2273.15), 7374.752, places=3)

class Test_pXsat_h(unittest.TestCase):

    def test_p3sat_h(self):

        self.assertAlmostEqual(stm.p3sat_h(2674.95), 11.62, places=2)

class Test_pXsat_s(unittest.TestCase):

    def test_p3sat_s(self):
        self.assertAlmostEqual(stm.p3sat_s(4.0), 19.809, places=3)

class Test_tX_ph(unittest.TestCase):

    def test_t1_ph(self):

        self.assertAlmostEqual(stm.t1_ph(10.0, 100.0), 294.775, places=3)

    def test_t2_ph(self):

        self.assertAlmostEqual(stm.t2_ph(10.0, 4000.0), 1026.313, places=3)

    def test_t3_ph(self):

        self.assertAlmostEqual(stm.t3_ph(19.0, 2500.0), 635.926, places=3)

    def test_t5_ph(self):

        self.assertAlmostEqual(stm.t5_ph(10.0, 4500.0), 1228.268, places=3)

class Test_vX_ph(unittest.TestCase):

    def test_v3_ph_region3a(self):
        self.assertAlmostEqual(stm.v3_ph(22.0, 2000.0), 0.002638, places=6)

    def test_v3_ph_region3b(self):
        self.assertAlmostEqual(stm.v3_ph(22.5, 2089.0), 0.003065, places=6)

class Test_vX_pt(unittest.TestCase):

    def test_v1_pt(self):

        self.assertAlmostEqual(stm.v1_pt(100.0, 400.0), 0.0010185, places=7)

    def test_v2_pt(self):

        self.assertAlmostEqual(stm.v2_pt(10.0, 600.0), 0.020093, places=6)

class Test_uX_pt(unittest.TestCase):

    def test_u1_pt(self):

        self.assertAlmostEqual(stm.u1_pt(100.0, 400.0), 501.925, places=3)

    def test_u2_pt(self):

        self.assertAlmostEqual(stm.u2_pT(10.0, 600.0), 2618.897, places=3)

class Test_sX_pt(unittest.TestCase):

    def test_s1_pt(self):
        self.assertAlmostEqual(stm.s1_pt(100.0, 400.0), 1.519, places=3)

    def test_s2_pt(self):
        self.assertAlmostEqual(stm.s2_pt(10.0, 600.0), 5.775, places=3)

class Test_cpX_pt(unittest.TestCase):

    def test_cp1_pt(self):

        self.assertAlmostEqual(stm.cp1_pt(100.0, 400.0), 4.0604, places=4)

    def test_cp2_pt(self):

        self.assertAlmostEqual(stm.cp2_pt(10.0, 600.0), 5.141, places=3)

class Test_cvX_pt(unittest.TestCase):

    def test_cv1_pt(self):
        self.assertAlmostEqual(stm.cv1_pt(100.0, 400.0), 3.533, places=3)

    def test_cv2_pt(self):
        self.assertAlmostEqual(stm.cv2_pt(10.0, 600.0), 2.626, places=3)

class Test_wX_pt(unittest.TestCase):

    def test_w1_pt(self):
        self.assertAlmostEqual(stm.w1_pt(100.0, 400.0), 1717.663, places=3)

    def test_w2_pt(self):
        self.assertAlmostEqual(stm.w2_pt(10.0, 600.0), 503.347, places=3)

class Test_tX_ps(unittest.TestCase):

    def test_t1_ps(self):
        self.assertAlmostEqual(stm.t1_ps(100.0, 2.0), 450.051, places=3)

    def test_t2_ps_region1(self):
        self.assertAlmostEqual(stm.t2_ps(3.9, 1.0), 82.311, places=3)

    def test_t2_ps_region3(self):
        self.assertAlmostEqual(stm.t2_ps(5.0, 2.0), 555.359, places=3)

    def test_t2_ps_region2(self):
        self.assertAlmostEqual(stm.t2_ps(5.0, 5.86), 525.436, places=3)

    def test_t3_ps_region3a(self):
        self.assertAlmostEqual(stm.t3_ps(20.0, 4.0), 638.449, places=3)

    def test_t3_ps_region3b(self):
        self.assertAlmostEqual(stm.t3_ps(20.0, 5.0), 640.118, places=3)

class Test_pX_hs(unittest.TestCase):

    def test_p1_hs(self):
        self.assertAlmostEqual(stm.p1_hs(100.0, 0.2), 44.451, places=3)

    def test_p2_hs_region1(self):
        self.assertAlmostEqual(stm.p2_hs(1700.0, 4.0), 175.162, places=3)

    def test_p2_hs_region2(self):
        self.assertAlmostEqual(stm.p2_hs(2800.0, 5.86), 7.070, places=3)

    def test_p2_hs_region3(self):
        self.assertAlmostEqual(stm.p2_hs(2800.0, 5.8), 8.415, places=3)

    def test_p3_hs_region3a(self):
        self.assertAlmostEqual(stm.p3_hs(1900.0, 4.0), 66.314, places=3)

    def test_p3_hs_region3b(self):
        self.assertAlmostEqual(stm.p3_hs(2200.0, 4.42), 67.465, places=3)

class Test_vX_ps(unittest.TestCase):

    def test_v3_ps_region3a(self):
        self.assertAlmostEqual(stm.v3_ps(20.0, 4.0), 0.002010, places=6)

    def test_v3_ps_region3b(self):
        self.assertAlmostEqual(stm.v3_ps(20.0, 5.0), 0.006262, places=6)

class Test_tX_prho(unittest.TestCase):

    def test_t1_prho(self):
        self.assertAlmostEqual(stm.t1_prho(100.0, 990.0), 388.110, places=3)

    def test_t2_prho(self):
        self.assertAlmostEqual(stm.t2_prho(1.01, 5.0), 466.334, places=3)

    def test_t3_prho(self):
        self.assertAlmostEqual(stm.t3_prho(21.0, 148.0), 649.829, places=3)

class Test_pX_rhot(unittest.TestCase):

    def test_p3_rhot(self):
        self.assertAlmostEqual(stm.p3_rhot(500.0, 644.0), 22.689, places=3)

class Test_uX_rhot(unittest.TestCase):

    def test_u3_rhot(self):
        self.assertAlmostEqual(stm.u3_rhot(500.0, 644.0), 1792.867, places=3)

class Test_hX_rhot(unittest.TestCase):

    def test_h3_rhot(self):
        self.assertAlmostEqual(stm.h3_rhot(500.0, 644.0), 1838.244, places=3)

class Test_sX_rhot(unittest.TestCase):

    def test_s3_pt(self):
        self.assertAlmostEqual(stm.s3_rhot(500.0, 644.0), 4.024, places=3)

class Test_cpX_rhot(unittest.TestCase):

    def test_cp3_rhot(self):
        self.assertAlmostEqual(stm.cp3_rhot(500.0, 644.0), 16.128, places=3)

class Test_cvX_rhot(unittest.TestCase):

    def test_cv3_rhot(self):
        self.assertAlmostEqual(stm.cv3_rhot(500.0, 644.0), 3.278, places=3)

class Test_wX_rhot(unittest.TestCase):

    def test_w3_rhot(self):
        self.assertAlmostEqual(stm.w3_rhot(500.0, 644.0), 473.134, places=3)

class Test_xX_ph(unittest.TestCase):

    def test_x4_ph_liquid(self):
        self.assertEqual(stm.x4_ph(15.0, 1000.0), 0.0)

    def test_x4_ph_vapor(self):
        self.assertEqual(stm.x4_ph(15.0, 3000.0), 1.0)

    def test_x4_ph_mix(self):
        self.assertAlmostEqual(stm.x4_ph(15.0, 2000.0), 0.390, places=3)

if __name__ == '__main__':
    unittest.main()
