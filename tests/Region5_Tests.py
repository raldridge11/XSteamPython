import unittest

import Region5

class Test_Region5(unittest.TestCase):

    def test_h5_pt(self):
        self.assertAlmostEqual(Region5.h5_pt(10.0,2273.15), 7374.752, places=3)

    def test_t5_ph(self):
        self.assertAlmostEqual(Region5.t5_ph(10.0, 4500.0), 1228.268, places=3)

    def test_v5_pt(self):
        self.assertAlmostEqual(Region5.v5_pt(15.0, 600.0), 0.010378, places=6)

    def test_u5_pt(self):
        self.assertAlmostEqual(Region5.u5_pt(15.0, 600.0), 2479.857, places=3)

    def test_s5_pt(self):
        self.assertAlmostEqual(Region5.s5_pt(15.0, 600.0), 5.343, places=3)

    def test_cp5_pt(self):
        self.assertAlmostEqual(Region5.cp5_pt(15.0, 600.0), 6.058, places=3)

    def test_cv5_pt(self):
        self.assertAlmostEqual(Region5.cv5_pt(15.0, 600.0), 2.390, places=3)

    def test_w5_pt(self):
        self.assertAlmostEqual(Region5.w5_pt(15.0, 600.0), 436.314, places=3)

    def test_t5_ps(self):
        self.assertAlmostEqual(Region5.t5_ps(9.0, 7.5), 1090.51, places=2)

    def test_t5_prho(self):
        self.assertAlmostEqual(Region5.t5_prho(9.0, 10.0), 1943.669, places=3)

if __name__ == '__main__':
    unittest.main()
