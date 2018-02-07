import unittest

import XSteamPython as stm

class Test_tests(unittest.TestCase):

    def test_toSIUnit_pressure(self):

        self.assertEqual(stm.toSIUnit_pressure(100.0), 0.1)

    def test_fromSIUnit_pressure(self):

        self.assertEqual(stm.fromSIUnit_pressure(0.1), 100.0)

    def test_toSIUnit_temperature(self):

        self.assertEqual(stm.toSIUnit_temperature(100.0), 373.15)

    def test_fromSIUnit_temperature(self):

        self.assertEqual(stm.fromSIUnit_temperature(373.15), 100.0)

    def test_Tsat_p(self):

        self.assertAlmostEqual(stm.Tsat_p(101.0), 99.88, places=2)

    def test_Tsat_p_errer(self):

        self.assertRaises(ArithmeticError, stm.Tsat_p, 0.0)

if __name__ == '__main__':
    unittest.main()
