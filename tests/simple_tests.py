import unittest

from .context import Shares, Index 

class TestIndex(unittest.TestCase):
    def setUp(self):
        self.test_shares = [Shares('TEA', 'Common', 100, True, 0, 0), Shares('POP', 'Common', 100, True, 8, 0), Shares('ALE', 'Common', 60, True, 23, 0), Shares('GIN', 'Preferred', 100, True, 8, 2), Shares('JOE', 'Common', 250, True, 13, 0)]
        self.test_index = Index('GBCE', self.test_shares)
       
    def test_index_constructor(self):
        self.assertIsNotNone(self.test_index)
        self.assertEqual(self.test_index.symbol, 'GBCE')
        self.assertEqual(self.test_index.composition, self.test_shares)

    def test_geometric_mean(self):
        self.assertEqual(self.test_index.value, 1.08447)

    def test_composition(self):
        for elem in self.test_shares:
            self.assertIn(elem, self.test_index.composition)

