# -*- coding: utf-8 -*-
'''
Unit tests for Boundaries
'''
import unittest

import Boundaries

class Test_Boundaries(unittest.TestCase):

    def test_b23t_p(self):

        self.assertAlmostEqual(Boundaries.b23t_p(15.0), 605.11, places=2)

    def test_b23p_t(self):

        self.assertAlmostEqual(Boundaries.b23p_t(100.0), 241.526, places=3)

    def test_hb13_s(self):

        self.assertAlmostEqual(Boundaries.hB13_s(3.0), 1612.0467, places=3)

    def test_tB23_hs(self):

        self.assertAlmostEqual(Boundaries.tB23_hs(1000.0, 3.0), 1611.524, places=3)

if __name__ == '__main__':
    unittest.main()
