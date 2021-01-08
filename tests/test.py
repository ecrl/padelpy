import unittest
from collections import OrderedDict

from padelpy import from_smiles, from_mdl


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


if __name__ == '__main__':

    unittest.main()
