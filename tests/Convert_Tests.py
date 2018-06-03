import unittest

import Convert

class Test_Conversions(unittest.TestCase):

    def test_toSIUnit_pressure(self):
        self.assertEqual(Convert.toSIUnit(100.0, 'pressure'), 0.1)

    def test_toSIUnit_pressure_English(self):
        self.assertAlmostEqual(Convert.toSIUnit(14.7, 'pressure', englishUnits=True), 0.1013529, 7)

    def test_fromSIUnit_pressure(self):
        self.assertEqual(Convert.fromSIUnit(0.1, 'pressure'), 100.0)

    def test_fromSIUnit_pressure_English(self):
        self.assertAlmostEqual(Convert.fromSIUnit(0.1013529, 'pressure', englishUnits=True), 14.7, 1)

    def test_toSIUnit_temperature(self):
        self.assertEqual(Convert.toSIUnit(100.0, 'temperature'), 373.15)

    def test_toSIUnit_temperature_English(self):
        self.assertEqual(Convert.toSIUnit(212.0, 'temperature', englishUnits=True), 373.15)

    def test_fromSIUnit_temperature(self):
        self.assertEqual(Convert.fromSIUnit(373.15, 'temperature'), 100.0)

    def test_fromSIUnit_temperature_English(self):
        self.assertEqual(Convert.fromSIUnit(373.15, 'temperature', englishUnits=True), 212.0)

    def test_toSIUnit_entropy_English(self):
        self.assertEqual(Convert.toSIUnit(1.0, 'entropy', englishUnits=True), 1.0/0.238845896627)

    def test_fromSIUnit_entropy_English(self):
        self.assertEqual(Convert.fromSIUnit(1.0, 'entropy', englishUnits=True), 0.238845896627)

    def test_toSIUnit_enthalpy_English(self):
        self.assertEqual(Convert.toSIUnit(1.0, 'enthalpy', englishUnits=True), 2.326)

    def test_fromSIUnit_enthalpy_English(self):
        self.assertEqual(Convert.fromSIUnit(1.0, 'enthalpy', englishUnits=True), 1.0/2.326)

    def test_toSIUnit_specificVolume_English(self):
        self.assertEqual(Convert.toSIUnit(1.0, 'specific volume', englishUnits=True), 0.0624279606)

    def test_fromSIUnit_specificVolume_English(self):
        self.assertEqual(Convert.fromSIUnit(1.0, 'specific volume', englishUnits=True), 1.0/0.0624279606)

    def test_toSIUnit_velocity_English(self):
        self.assertEqual(Convert.toSIUnit(1.0, 'velocity', englishUnits=True), 0.3048)

    def test_fromSIUnit_velocity_English(self):
        self.assertEqual(Convert.fromSIUnit(1.0, 'velocity', englishUnits=True), 1.0/0.3048)

    def test_toSIUnit_thermalConductivity_English(self):
        self.assertEqual(Convert.toSIUnit(1.0, 'thermal conductivity', englishUnits=True), 1.0/0.577789)

    def test_fromSIUnit_thermalConductivity_English(self):
        self.assertEqual(Convert.fromSIUnit(1.0, 'thermal conductivity', englishUnits=True), 0.577789)

    def test_toSIUnit_surfaceTension_English(self):
        self.assertEqual(Convert.toSIUnit(1.0, 'surface tension', englishUnits=True), 1.0/0.068521766)

    def test_fromSIUnit_surfaceTension_English(self):
        self.assertEqual(Convert.fromSIUnit(1.0, 'surface tension', englishUnits=True), 0.068521766)

    def test_toSIUnit_dynamicViscosity_English(self):
        self.assertEqual(Convert.toSIUnit(1.0, 'viscosity', englishUnits=True), 1.0/2419.088311)

    def test_fromSIUnit_dynamicViscosity_English(self):
        self.assertEqual(Convert.fromSIUnit(1.0, 'viscosity', englishUnits=True), 2419.088311)

if __name__ == '__main__':
    unittest.main()