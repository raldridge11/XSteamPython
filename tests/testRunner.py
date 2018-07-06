# -*- coding: utf-8 -*-
'''
* Water and steam properties according to IAPWS IF-97
* By Magnus Holmgren, www.x-eng.com
* The steam tables are free and provided as is.
* We take no responsibilities for any errors in the code or damage thereby.
* You are free to use, modify and distribute the code as long as authorship is properly acknowledged.
* Please notify me at magnus@x-eng.com if the code is used in commercial applications
'''
import unittest

import Convert_Tests
import Region1_Tests
import Region2_Tests
import Region3_Tests
import Region4_Tests
import Region5_Tests
import Regions_Tests
import Boundaries_Tests

import Psat_Tests
import Tsat_Tests
import Temperature_Tests
import TransportProperties_Tests


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

    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    main()
