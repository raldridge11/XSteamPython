import unittest

import Regions

class Test_Regions(unittest.TestCase):

    def test_region_ph_pressureOutOfBounds(self):
        self.assertEqual(Regions.region_ph(0,4.0), None)

    def test_region_ph_enthalpyOutOfBounds(self):
        self.assertEqual(Regions.region_ph(1,-1), None)

    def test_region_ph_region1_bellow3(self):
        self.assertEqual(Regions.region_ph(1.0, 100.0), 1)

    def test_region_ph_region1_above3(self):
        self.assertEqual(Regions.region_ph(17.0, 1000.0), 1)

    def test_region_ph_region2_bellow3(self):
        self.assertEqual(Regions.region_ph(1.0, 4000.0), 2)

    def test_region_ph_region2_above3(self):
        self.assertEqual(Regions.region_ph(17.0, 3000.0), 2)

    def test_region_ph_region4_bellow3(self):
        self.assertEqual(Regions.region_ph(1.0, 1000.0), 4)

    def test_region_ph_region4_above3(self):
        self.assertEqual(Regions.region_ph(17.0, 2000.0), 4)

    def test_region_ph_region5_bellow3(self):
        self.assertEqual(Regions.region_ph(1.0, 5000.0), 5)

    def test_region_ph_region3(self):
        self.assertEqual(Regions.region_ph(19.0, 2500.0), 3)

    def test_region_pt_region5(self):
        self.assertEqual(Regions.region_pt(9.0, 2000.0), 5)

    def test_region_pt_region3_highT(self):
        self.assertEqual(Regions.region_pt(19.0, 640.0), 3)

    def test_region_pt_region4_highT(self):
        self.assertEqual(Regions.region_pt(20.26594,640.0), 4)

    def test_region_pt_region2_highT(self):
        self.assertEqual(Regions.region_pt(18.0, 640.0), 2)

    def test_region_pt_region4_lowT(self):
        self.assertEqual(Regions.region_pt(2.63890, 500.0), 4)

    def test_region_pt_region1_lowT(self):
        self.assertEqual(Regions.region_pt(3.0, 500.0), 1)

    def test_region_pt_region2_lowT(self):
        self.assertEqual(Regions.region_pt(2.0, 500.0), 2)

    def test_region_pt_region_pt_exception(self):
        self.assertRaises(ArithmeticError, Regions.region_pt, 200, 3000.0)

    def test_region_ps_exception(self):
        self.assertEqual(Regions.region_ps(200.0, 100.0), None)

    def test_region_ps_exception_region5(self):
        self.assertEqual(Regions.region_ps(11.0, 7.5), None)

    def test_region_ps_region5(self):
        self.assertEqual(Regions.region_ps(9, 7.5), 5)

    def test_region_ps_region2_highPressure(self):
        self.assertEqual(Regions.region_ps(17.0, 5.4), 2)

    def test_region_ps_region2_lowPressure(self):
        self.assertEqual(Regions.region_ps(15.0, 5.4), 2)

    def test_region_ps_region3(self):
        self.assertEqual(Regions.region_ps(17.0, 3.8), 3)

    def test_region_ps_region4inside3(self):
        self.assertEqual(Regions.region_ps(17.0, 4.0), 4)

    def test_region_ps_region4(self):
        self.assertEqual(Regions.region_ps(10.0, 4.0), 4)

    def test_region_ps_region1(self):
        self.assertEqual(Regions.region_ps(10.0, 1.0), 1)

    def test_region_hs_exception(self):
        self.assertEqual(Regions.region_hs(-1.0, -1.0), None)

    def test_region_hs_region4_bitoverb13(self):
        self.assertEqual(Regions.region_hs(274.0, 1.0), 4)

    def test_region_hs_region1_bitoverb13_100Mpa_limit(self):
        self.assertEqual(Regions.region_hs(309.0, 1.0), 1)

    def test_region_hs_region1_b23(self):
        self.assertEqual(Regions.region_hs(1500.0, 3.4), 1)

    def test_region_hs_region3_b23(self):
        self.assertEqual(Regions.region_hs(1747.0, 3.7), 3)

    def test_region_hs_exception_bitoverb13(self):
        self.assertEqual(Regions.region_hs(1800.0, 3.7), None)

    def test_region_hs_region2_upperB23(self):
        self.assertEqual(Regions.region_hs(3000.0, 9.2), 2)

    def test_region_hs_region4_upperB23(self):
        self.assertEqual(Regions.region_hs(2700.0, 7.0), 4)

    def test_region_hs_region2_upperB23_lowEntropy(self):
        self.assertEqual(Regions.region_hs(3000.0, 6.03), 2)

    def test_region_hs_region2_upperB23_highEntropy(self):
        self.assertEqual(Regions.region_hs(3000.0, 6.05), 2)

    def test_region_hs_exception_upperB23(self):
        self.assertEqual(Regions.region_hs(4000.0, 6.05), None)

    def test_region_hs_region4_underCritical(self):
        self.assertEqual(Regions.region_hs(1800.0, 4.0), 4)

    def test_region_hs_region3_underCritical(self):
        self.assertEqual(Regions.region_hs(1900.0, 4.0), 3)

    def test_region_hs_excpetion_underCritical(self):
        self.assertEqual(Regions.region_hs(2000.0, 4.0), None)

    def test_region_hs_region4_aboveCritical(self):
        self.assertEqual(Regions.region_hs(1900.0, 4.5), 4)

    def test_region_hs_region3_aboveCritical_underb23(self):
        self.assertEqual(Regions.region_hs(2200.0, 4.5), 3)

    def test_region_hs_region2_aboveCritical_underb23(self):
        self.assertEqual(Regions.region_hs(2813.0, 5.1), 2)

    def test_region_hs_region3_aboveCritical_underb23_check2(self):
        self.assertEqual(Regions.region_hs(2600.0, 5.1), 3)

    def test_region_hs_region3_aboveCritical_underb23_check3(self):
        self.assertEqual(Regions.region_hs(2600.0, 5.2), 3)

    def test_region_hs_region2_aboveCritical_aboveb23(self):
        self.assertEqual(Regions.region_hs(2700.0, 5.2), 2)

    def test_region_hs_exception_regionnotdetermined(self):
        self.assertEqual(Regions.region_hs(3000.0, 5.2), None)

    def test_region_prho_exceptionOnPressure(self):
        self.assertRaises(ArithmeticError, Regions.region_prho, 0.0, 700.0)

    def test_region_prho_exceptionOnDensity(self):
        self.assertRaises(ArithmeticError, Regions.region_prho, 10.0, 1005.0)

    def test_region_prho_region1_lowPressure(self):
        self.assertEqual(Regions.region_prho(15.0, 700.0), 1)

    def test_region_prho_region4_lowPressure(self):
        self.assertEqual(Regions.region_prho(15.0, 96.72), 4)

    def test_region_prho_lowPressure_exception(self):
        self.assertRaises(ArithmeticError, Regions.region_prho, 15.0, 31.0)

    def test_region_prho_region2_lowPressure(self):
        self.assertEqual(Regions.region_prho(10.0, 21.0), 2)

    def test_region_prho_region5_lowPressure(self):
        self.assertEqual(Regions.region_prho(10.0, 11.0), 5)

    def test_region_prho_region1_highPressure(self):
        self.assertEqual(Regions.region_prho(17.0, 580.0), 1)

    def test_region_prho_region3_superCritical(self):
        self.assertEqual(Regions.region_prho(23.0, 145.0), 3)

    def test_region_prho_region3_highPressure(self):
        self.assertEqual(Regions.region_prho(17.0, 115.0), 3)

    def test_region_prho_region4_highPressure(self):
        self.assertEqual(Regions.region_prho(17.0, 145.0), 4)

    def test_region_prho_region2_highPressure(self):
        self.assertEqual(Regions.region_prho(17.0, 36.0), 2)

if __name__ == '__main__':
    unittest.main()
