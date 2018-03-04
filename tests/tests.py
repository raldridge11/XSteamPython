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

class Test_Tx_p(unittest.TestCase):

    def test_t4_p(self):

        self.assertAlmostEqual(stm.t4_p(10.0), 584.149, places=3)

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

    def test_t1_ph(self):

        self.assertAlmostEqual(stm.t1_ph(10.0, 100.0), 294.775, places=3)

    def test_t2_ph(self):

        self.assertAlmostEqual(stm.t2_ph(10.0, 4000.0), 1026.313, places=3)

    def test_t3_ph(self):

        self.assertAlmostEqual(stm.t3_ph(19.0, 2500.0), 635.926, places=3)

    def test_t5_ph(self):

        self.assertAlmostEqual(stm.t5_ph(10.0, 4500.0), 1228.268, places=3)

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

class Test_hX_pt(unittest.TestCase):

    def test_h1_pt(self):

        self.assertAlmostEqual(stm.h1_pt(17.0, 623.15), 1666.589, places=3)

    def test_h2_pt(self):

        self.assertAlmostEqual(stm.h2_pt(15.0, 1073.15), 4091.326, places=3)

    def test_h5_pt(self):

        self.assertAlmostEqual(stm.h5_pt(10.0,2273.15), 7374.752, places=3)

class Test_pXsat_h(unittest.TestCase):

    def test_p3sat_h(self):

        self.assertAlmostEqual(stm.p3sat_h(2674.95), 11.62, places=2)

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

class Test_vX_pt(unittest.TestCase):

    def test_v1_pt(self):

        self.assertAlmostEqual(stm.v1_pt(100.0, 400.0), 0.0010185, places=7)

class Test_uX_pt(unittest.TestCase):

    def test_u1_pt(self):

        self.assertAlmostEqual(stm.u1_pt(100.0, 400.0), 501.925, places=3)

class Test_sX_pt(unittest.TestCase):

    def test_s1_pt(self):
        self.assertAlmostEqual(stm.s1_pt(100.0, 400.0), 1.519, places=3)

class Test_cpX_pt(unittest.TestCase):

    def test_cp1_pt(self):

        self.assertAlmostEqual(stm.cp1_pt(100.0, 400.0), 4.0604, places=4)

class Test_cvX_pt(unittest.TestCase):

    def test_cv1_pt(self):
        self.assertAlmostEqual(stm.cv1_pt(100.0, 400.0), 3.533, places=3)

class Test_wx_pt(unittest.TestCase):

    def test_w1_pt(self):
        self.assertAlmostEqual(stm.w1_pt(100.0, 400.0), 1717.663, places=3)

class Test_tX_ps(unittest.TestCase):

    def test_t1_ps(self):
        self.assertAlmostEqual(stm.t1_ps(100.0, 2.0), 450.051, places=3)

if __name__ == '__main__':
    unittest.main()
