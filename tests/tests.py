import unittest

import XSteamPython as stm

unitSystem = 'English'
unitWrong = 'dumb'

class Test_Pressure_Conversion(unittest.TestCase):

    def test_toSIUnit_pressure(self):

        self.assertEqual(stm.toSIUnit_pressure(100.0), 0.1)

    def test_toSIUnit_pressure_English(self):

        self.assertAlmostEqual(stm.toSIUnit_pressure(14.7, unitSystem), 0.1013529, 7)

    def test_toSIUnit_pressure_Error(self):

        self.assertRaises(ValueError, stm.toSIUnit_pressure, 14.7, unitWrong)

    def test_fromSIUnit_pressure(self):

        self.assertEqual(stm.fromSIUnit_pressure(0.1), 100.0)

    def test_fromSIUnit_pressure_English(self):

        self.assertAlmostEqual(stm.fromSIUnit_pressure(0.1013529, unitSystem), 14.7, 1)

    def test_fromSIUnit_pressure_Error(self):

        self.assertRaises(ValueError, stm.fromSIUnit_pressure, 0.1013529, unitWrong)

class Test_Temperature_Conversion(unittest.TestCase):

    def test_toSIUnit_temperature(self):

        self.assertEqual(stm.toSIUnit_temperature(100.0), 373.15)

    def test_toSIUnit_temperature_English(self):

        self.assertEqual(stm.toSIUnit_temperature(212.0, unitSystem), 373.15)

    def test_toSIUnit_temperature_Error(self):

        self.assertRaises(ValueError, stm.toSIUnit_temperature, 212.0, unitWrong)

    def test_fromSIUnit_temperature(self):

        self.assertEqual(stm.fromSIUnit_temperature(373.15), 100.0)

    def test_fromSIUnit_temperature_English(self):

        self.assertEqual(stm.fromSIUnit_temperature(373.15, unitSystem), 212.0)

    def test_fromSIUnit_temperature_English_Error(self):

        self.assertRaises(ValueError, stm.fromSIUnit_temperature, 373.15, unitWrong)

class Test_Entropy_Conversion(unittest.TestCase):

    def test_toSIUnit_entropy(self):

        self.assertEqual(stm.toSIUnit_entropy(1.0), 1.0)

    def test_toSIUnit_entropy_English(self):

        self.assertEqual(stm.toSIUnit_entropy(1.0, unitSystem), 1.0/0.238845896627)

    def test_toSIUnit_entropy_Error(self):

        self.assertRaises(ValueError, stm.toSIUnit_entropy, 1.0, unitWrong)

    def test_fromSIUnit_entropy(self):

        self.assertEqual(stm.fromSIUnit_entropy(1.0), 1.0)

    def test_fromSIUnit_entropy_English(self):

        self.assertEqual(stm.fromSIUnit_entropy(1.0, unitSystem), 0.238845896627)

    def test_fromSIUnit_entropy_Error(self):

        self.assertRaises(ValueError, stm.fromSIUnit_entropy, 1.0, unitWrong)

class Test_Enthalpy_Conversion(unittest.TestCase):

    def test_toSIUnit_enthalpy(self):

        self.assertEqual(stm.toSIUnit_enthalpy(1.0), 1.0)

    def test_toSIUnit_enthalpy_English(self):

        self.assertEqual(stm.toSIUnit_enthalpy(1.0, unitSystem), 2.326)

    def test_toSIUnit_enthalpy_Error(self):

        self.assertRaises(ValueError, stm.toSIUnit_enthalpy, 1, unitWrong)

    def test_fromSIUnit_enthalpy(self):

        self.assertEqual(stm.fromSIUnit_enthalpy(1.0), 1.0)

    def test_fromSIUnit_enthalpy_English(self):

        self.assertEqual(stm.fromSIUnit_enthalpy(1.0, unitSystem), 1.0/2.326)

    def test_fromSIUnit_enthalpy_Error(self):

        self.assertRaises(ValueError, stm.fromSIUnit_enthalpy, 1, unitWrong)

class Test_SpecificVolume_Conversion(unittest.TestCase):

    def test_toSIUnit_specificVolume(self):

        self.assertEqual(stm.toSIUnit_specificVolume(1.0), 1.0)

    def test_toSIUnit_specificVolume_English(self):

        self.assertEqual(stm.toSIUnit_specificVolume(1.0, unitSystem), 0.0624279606)

    def test_toSIUnit_specificVolume_Error(self):

        self.assertRaises(ValueError, stm.toSIUnit_specificVolume, 1, unitWrong)

    def test_fromSIUnit_specificVolume(self):

        self.assertEqual(stm.fromSIUnit_specificVolume(1.0), 1.0)

    def test_fromSIUnit_specificVolume_English(self):

        self.assertEqual(stm.fromSIUnit_specificVolume(1.0, unitSystem), 1.0/0.0624279606)

    def test_fromSIUnit_specificVolume_Error(self):

        self.assertRaises(ValueError, stm.fromSIUnit_specificVolume, 1, unitWrong)

class Test_Velocity_Conversion(unittest.TestCase):

    def test_toSIUnit_velocity(self):

        self.assertEqual(stm.toSIUnit_velocity(1.0), 1.0)

    def test_toSIUnit_velocity_English(self):

        self.assertEqual(stm.toSIUnit_velocity(1.0, unitSystem), 0.3048)

    def test_toSIUnit_velocity_Error(self):

        self.assertRaises(ValueError, stm.toSIUnit_velocity, 1, unitWrong)

    def test_fromSIUnit_velocity(self):

        self.assertEqual(stm.fromSIUnit_velocity(1.0), 1.0)

    def test_fromSIUnit_velocity_English(self):

        self.assertEqual(stm.fromSIUnit_velocity(1.0, unitSystem), 1.0/0.3048)

    def test_fromSIUnit_velocity_Error(self):

        self.assertRaises(ValueError, stm.fromSIUnit_velocity, 1, unitWrong)

class Test_ThermalConductivity_Conversion(unittest.TestCase):

    def test_toSIUnit_thermalConductivity(self):

        self.assertEqual(stm.toSIUnit_thermalConductivity(1.0), 1.0)

    def test_toSIUnit_thermalConductivity_English(self):

        self.assertEqual(stm.toSIUnit_thermalConductivity(1.0, unitSystem), 1.0/0.577789)

    def test_toSIUnit_thermalConductivity_Error(self):

        self.assertRaises(ValueError, stm.toSIUnit_thermalConductivity, 1, unitWrong)

    def test_fromSIUnit_thermalConductivity(self):

        self.assertEqual(stm.fromSIUnit_thermalConductivity(1.0), 1.0)

    def test_fromSIUnit_thermalConductivity_English(self):

        self.assertEqual(stm.fromSIUnit_thermalConductivity(1.0, unitSystem), 0.577789)

    def test_fromSIUnit_thermalConductivity_Error(self):

        self.assertRaises(ValueError, stm.fromSIUnit_thermalConductivity, 1, unitWrong)

class Test_SurfaceTension_Conversion(unittest.TestCase):

    def test_toSIUnit_surfaceTension(self):

        self.assertEqual(stm.toSIUnit_surfaceTension(1.0), 1.0)

    def test_toSIUnit_surfaceTension_English(self):

        self.assertEqual(stm.toSIUnit_surfaceTension(1.0, unitSystem), 1.0/0.068521766)

    def test_toSIUnit_surfaceTension_Error(self):

        self.assertRaises(ValueError, stm.toSIUnit_surfaceTension, 1, unitWrong)

    def test_fromSIUnit_surfaceTension(self):

        self.assertEqual(stm.fromSIUnit_surfaceTension(1.0), 1.0)

    def test_fromSIUnit_surfaceTension_English(self):

        self.assertEqual(stm.fromSIUnit_surfaceTension(1.0, unitSystem), 0.068521766)

    def test_fromSIUnit_surfaceTension_Error(self):

        self.assertRaises(ValueError, stm.fromSIUnit_surfaceTension, 1, unitWrong)

class Test_DynamicViscosity_Conversion(unittest.TestCase):

    def test_toSIUnit_dynamicViscosity(self):

        self.assertEqual(stm.toSIUnit_dynamicViscosity(1.0), 1.0)

    def test_toSIUnit_dynamicViscosity_English(self):

        self.assertEqual(stm.toSIUnit_dynamicViscosity(1.0, unitSystem), 1.0/2419.088311)

    def test_toSIUnit_dynamicViscosity_Error(self):

        self.assertRaises(ValueError, stm.toSIUnit_dynamicViscosity, 1, unitWrong)

    def test_fromSIUnit_dynamicViscosity(self):

        self.assertEqual(stm.fromSIUnit_dynamicViscosity(1.0), 1.0)

    def test_fromSIUnit_dynamicViscosity_English(self):

        self.assertEqual(stm.fromSIUnit_dynamicViscosity(1.0, unitSystem), 2419.088311)

    def test_fromSIUnit_dynamicViscosity_Error(self):

        self.assertRaises(ValueError, stm.fromSIUnit_dynamicViscosity, 1, unitWrong)

class Test_Tsat_p(unittest.TestCase):

    def test_Tsat_p(self):

        self.assertAlmostEqual(stm.Tsat_p(101.0), 99.88, places=2)

    def test_Tsat_p_English(self):

        self.assertAlmostEqual(stm.Tsat_p(14.7, unitSystem), 212.0, 1)

    def test_Tsat_p_error(self):

        self.assertRaises(ArithmeticError, stm.Tsat_p, 0.0)

if __name__ == '__main__':
    unittest.main()
