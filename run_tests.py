# -*- coding: utf-8 -*-
'''
Unit test runner
'''
import os
import sys
import unittest

file_directory = os.path.dirname(__file__)
src_path = os.path.join(os.path.abspath(file_directory), "XSteamPython")
test_path = os.path.join(os.path.abspath(file_directory), "tests")
sys.path.append(src_path)
sys.path.append(test_path)

import Boundaries_Tests
import Convert_Tests
import Region1_Tests
import Region2_Tests
import Region3_Tests
import Region4_Tests
import Region5_Tests
import Regions_Tests

import Density_Tests
import Enthalpy_Tests
import Entropy_Tests
import Kappa_Tests
import Prandtl_Tests
import Pressure_Tests
import Psat_Tests
import SpecificEnergy_Tests
import SpecificHeat_Tests
import SpecificVolume_Tests
import SpeedOfSound_Tests
import SurfaceTension_Tests
import Tsat_Tests
import Temperature_Tests
import ThermalConductivity_Tests
import TransportProperties_Tests
import VaporFraction_Tests
import Viscosity_Tests


def main():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTest(loader.loadTestsFromModule(Convert_Tests))
    suite.addTest(loader.loadTestsFromModule(Region1_Tests))
    suite.addTest(loader.loadTestsFromModule(Region2_Tests))
    suite.addTest(loader.loadTestsFromModule(Region3_Tests))
    suite.addTest(loader.loadTestsFromModule(Region4_Tests))
    suite.addTest(loader.loadTestsFromModule(Region5_Tests))
    suite.addTest(loader.loadTestsFromModule(Regions_Tests))
    suite.addTest(loader.loadTestsFromModule(Boundaries_Tests))

    suite.addTest(loader.loadTestsFromModule(Psat_Tests))
    suite.addTest(loader.loadTestsFromModule(Tsat_Tests))
    suite.addTest(loader.loadTestsFromModule(Temperature_Tests))
    suite.addTest(loader.loadTestsFromModule(TransportProperties_Tests))
    suite.addTest(loader.loadTestsFromModule(Pressure_Tests))
    suite.addTest(loader.loadTestsFromModule(Enthalpy_Tests))
    suite.addTest(loader.loadTestsFromModule(SpecificVolume_Tests))
    suite.addTest(loader.loadTestsFromModule(Density_Tests))
    suite.addTest(loader.loadTestsFromModule(Entropy_Tests))
    suite.addTest(loader.loadTestsFromModule(SpecificEnergy_Tests))
    suite.addTest(loader.loadTestsFromModule(SpecificHeat_Tests))
    suite.addTest(loader.loadTestsFromModule(SpeedOfSound_Tests))
    suite.addTest(loader.loadTestsFromModule(VaporFraction_Tests))
    suite.addTest(loader.loadTestsFromModule(SurfaceTension_Tests))
    suite.addTest(loader.loadTestsFromModule(Kappa_Tests))
    suite.addTest(loader.loadTestsFromModule(ThermalConductivity_Tests))
    suite.addTest(loader.loadTestsFromModule(Viscosity_Tests))
    suite.addTest(loader.loadTestsFromModule(Prandtl_Tests))

    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    main()
