import unittest

import Convert_Tests
import Region1_Tests
import Region2_Tests
import Region3_Tests
import Region4_Tests
import Boundaries_Tests

def main():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTest(loader.loadTestsFromModule(Convert_Tests))
    suite.addTest(loader.loadTestsFromModule(Region1_Tests))
    suite.addTest(loader.loadTestsFromModule(Region2_Tests))
    suite.addTest(loader.loadTestsFromModule(Region3_Tests))
    suite.addTest(loader.loadTestsFromModule(Region4_Tests))
    suite.addTest(loader.loadTestsFromModule(Boundaries_Tests))

    runner = unittest.TextTestRunner()
    result = runner.run(suite)

if __name__ == '__main__':
    main()
