# -*- coding: utf-8 -*-
'''
Unit tests for Transport Property functions
'''
import unittest

import XSteamPython as stm

class Test_Transport_Properties(unittest.TestCase):

    def test_surfaceTension_T(self):
        self.assertAlmostEqual(stm.surfaceTension_T(100.0), 0.09006, places=5)

    def test_tcpTrho(self):
        self.assertAlmostEqual(stm.tc_pTrho(1.0, 293.0, 998.0), 0.599, places=3)

if __name__ == '__main__':
    unittest.main()
