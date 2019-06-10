import unittest
from collections import OrderedDict

from padelpy import from_smiles, from_mdl


class TestAll(unittest.TestCase):

    def test_from_smiles(self):

        descriptors = from_smiles('CCC')
        self.assertEqual(len(descriptors), 1875)
        self.assertAlmostEqual(float(descriptors['MW']), 44.0626, 4)
        self.assertEqual(int(descriptors['nC']), 3)


if __name__ == '__main__':

    unittest.main()
