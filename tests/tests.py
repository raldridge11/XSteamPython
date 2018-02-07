import unittest

import XSteamPython as stm

class Test_Pressure_Conversion(unittest.TestCase):

    def test_toSIUnit_pressure(self):

        self.assertEqual(stm.toSIUnit_pressure(100.0), 0.1)

    def test_toSIUnit_pressure_English(self):

        self.assertAlmostEqual(stm.toSIUnit_pressure(14.7, units='English'), 0.1013529, 7)

    def test_toSIUnit_pressure_Error(self):

        self.assertRaises(ValueError, stm.toSIUnit_pressure, 14.7, units='dumb')

    def test_fromSIUnit_pressure(self):

        self.assertEqual(stm.fromSIUnit_pressure(0.1), 100.0)

    def test_fromSIUnit_pressure_English(self):

        self.assertAlmostEqual(stm.fromSIUnit_pressure(0.1013529, units='English'), 14.7, 1)

    def test_fromSIUnit_pressure_Error(self):

        self.assertRaises(ValueError, stm.fromSIUnit_pressure, 0.1013529, units='dumb')

class Test_Temperature_Conversion(unittest.TestCase):

    def test_toSIUnit_temperature(self):

        self.assertEqual(stm.toSIUnit_temperature(100.0), 373.15)

    def test_toSIUnit_temperature_English(self):

        self.assertEqual(stm.toSIUnit_temperature(212.0, units='English'), 373.15)

    def test_toSIUnit_temperature_Error(self):

        self.assertRaises(ValueError, stm.toSIUnit_temperature, 212.0, units='dumb')

    def test_fromSIUnit_temperature(self):

        self.assertEqual(stm.fromSIUnit_temperature(373.15), 100.0)

    def test_fromSIUnit_temperature_English(self):

        self.assertEqual(stm.fromSIUnit_temperature(373.15, units='English'), 212.0)

    def test_fromSIUnit_temperature_English_Error(self):

        self.assertRaises(ValueError, stm.fromSIUnit_temperature, 373.15, units='dumb')

class Test_Entropy_Conversion(unittest.TestCase):

    def test_toSIUnit_entropy(self):

        self.assertEqual(stm.toSIUnit_entropy(1.0), 1.0)

    def test_toSIUnit_entropy_English(self):

        self.assertEqual(stm.toSIUnit_entropy(1.0, units='English'), 1.0/0.238845896627)

    def test_toSIUnit_entropy_Error(self):

        self.assertRaises(ValueError, stm.toSIUnit_entropy, 1.0, units='dumb')

    def test_fromSIUnit_entropy(self):

        self.assertEqual(stm.fromSIUnit_entropy(1.0), 1.0)

    def test_fromSIUnit_entropy_English(self):

        self.assertEqual(stm.fromSIUnit_entropy(1.0, units='English'), 0.238845896627)

    def test_fromSIUnit_entropy_Error(self):

        self.assertRaises(ValueError, stm.fromSIUnit_entropy, 1.0, units='dumb')

class Test_Tsat_p(unittest.TestCase):

    def test_Tsat_p(self):

        self.assertAlmostEqual(stm.Tsat_p(101.0), 99.88, places=2)

    def test_Tsat_p_English(self):

        self.assertAlmostEqual(stm.Tsat_p(14.7, units='English'), 212.0, 1)

    def test_Tsat_p_error(self):

        self.assertRaises(ArithmeticError, stm.Tsat_p, 0.0)

if __name__ == '__main__':
    unittest.main()
