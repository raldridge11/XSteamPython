# -*- coding: utf-8 -*-
import unittest

import numpy as np

import Data
import XSteamPython as stm

class Test_Transport_Properties(unittest.TestCase):

    def test_surfaceTension_T(self):
        self.assertAlmostEqual(stm.surfaceTension_T(100.0), 0.09006, places=5)

    def test_surfaceTension_T_Excetpion(self):
        self.assertRaises(ArithmeticError, stm.surfaceTension_T, 0.0)

if __name__ == '__main__':
    unittest.main()
