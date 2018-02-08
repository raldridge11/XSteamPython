import unittest

import XSteamPython as stm

class Test_Conversions(unittest.TestCase):

    def tearDown(self):

        stm.englishUnits = False

    def test_toSIUnit_pressure(self):

        self.assertEqual(stm.toSIUnit_pressure(100.0), 0.1)

    def test_toSIUnit_pressure_English(self):

        stm.englishUnits = True
        self.assertAlmostEqual(stm.toSIUnit_pressure(14.7), 0.1013529, 7)

    def test_fromSIUnit_pressure(self):

        self.assertEqual(stm.fromSIUnit_pressure(0.1), 100.0)

    def test_fromSIUnit_pressure_English(self):

        stm.englishUnits = True
        self.assertAlmostEqual(stm.fromSIUnit_pressure(0.1013529), 14.7, 1)

    def test_toSIUnit_temperature(self):

        self.assertEqual(stm.toSIUnit_temperature(100.0), 373.15)

    def test_toSIUnit_temperature_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.toSIUnit_temperature(212.0), 373.15)

    def test_fromSIUnit_temperature(self):

        self.assertEqual(stm.fromSIUnit_temperature(373.15), 100.0)

    def test_fromSIUnit_temperature_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.fromSIUnit_temperature(373.15), 212.0)

    def test_toSIUnit_entropy_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.toSIUnit_entropy(1.0), 1.0/0.238845896627)

    def test_fromSIUnit_entropy_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.fromSIUnit_entropy(1.0), 0.238845896627)

    def test_toSIUnit_enthalpy_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.toSIUnit_enthalpy(1.0), 2.326)

    def test_fromSIUnit_enthalpy_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.fromSIUnit_enthalpy(1.0), 1.0/2.326)

    def test_toSIUnit_specificVolume_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.toSIUnit_specificVolume(1.0), 0.0624279606)

    def test_fromSIUnit_specificVolume_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.fromSIUnit_specificVolume(1.0), 1.0/0.0624279606)

    def test_toSIUnit_velocity_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.toSIUnit_velocity(1.0), 0.3048)

    def test_fromSIUnit_velocity_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.fromSIUnit_velocity(1.0), 1.0/0.3048)

    def test_toSIUnit_thermalConductivity_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.toSIUnit_thermalConductivity(1.0), 1.0/0.577789)

    def test_fromSIUnit_thermalConductivity_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.fromSIUnit_thermalConductivity(1.0), 0.577789)

    def test_toSIUnit_surfaceTension_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.toSIUnit_surfaceTension(1.0), 1.0/0.068521766)

    def test_fromSIUnit_surfaceTension_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.fromSIUnit_surfaceTension(1.0), 0.068521766)

    def test_toSIUnit_dynamicViscosity_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.toSIUnit_dynamicViscosity(1.0), 1.0/2419.088311)

    def test_fromSIUnit_dynamicViscosity_English(self):

        stm.englishUnits = True
        self.assertEqual(stm.fromSIUnit_dynamicViscosity(1.0), 2419.088311)

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

if __name__ == '__main__':
    unittest.main()
