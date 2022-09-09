import unittest
from collections import OrderedDict

from padelpy import from_mdl, from_sdf, from_smiles


class TestAll(unittest.TestCase):

    def test_from_smiles(self):
        descriptors = from_smiles('CCC')
        self.assertEqual(len(descriptors), 1875)
        self.assertAlmostEqual(float(descriptors['MW']), 44.0626, 4)
        self.assertEqual(int(descriptors['nC']), 3)

    def test_multiple_smiles(self):
        smiles = ['CCC', 'CCCC']
        descriptors = from_smiles(smiles)
        self.assertEqual(len(descriptors), 2)
        self.assertEqual(len(descriptors[0]), 1875)

    def test_errors(self):
        bad_smiles = 'SJLDFGSJ'
        self.assertRaises(RuntimeError, from_smiles, bad_smiles)
        bad_smiles = ['SJLDFGSJ', 'CCC']
        self.assertRaises(RuntimeError, from_smiles, bad_smiles)

    def test_from_sdf(self):
        """Test SDF file input functionality."""
        descriptors = from_sdf("aspirin_3d.sdf")[0]
        self.assertEqual(len(descriptors), 1875)
        self.assertAlmostEqual(float(descriptors['MW']), 180.04225, 4)
        self.assertAlmostEqual(float(descriptors['SsCH3']), 1.2209, 4)
        self.assertEqual(int(descriptors['nC']), 9)


if __name__ == '__main__':
    unittest.main()
