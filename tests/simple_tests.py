import unittest
from unittest.mock import patch

from .context import Shares, Index, Market 

class TestIndex(unittest.TestCase):
    def setUp(self):
        self.test_shares = [Shares('TEA', 'Common', 100, True, 0, 0), Shares('POP', 'Common', 100, True, 8, 0), Shares('ALE', 'Common', 60, True, 23, 0), Shares('GIN', 'Preferred', 100, True, 8, 2), Shares('JOE', 'Common', 250, True, 13, 0)]
        self.test_index = Index('GBCE', self.test_shares)
       
    def test_index_constructor(self):
        self.assertIsNotNone(self.test_index)
        self.assertEqual(self.test_index.symbol, 'GBCE')
        self.assertEqual(self.test_index.composition, self.test_shares)
        self.assertFalse(self.test_index.tradeable)

    def test_geometric_mean(self):
        self.assertEqual(round(self.test_index.value, 5), 1.08447)

    def test_composition(self):
        for elem in self.test_shares:
            self.assertIn(elem, self.test_index.composition)

class TestMarket(unittest.TestCase):
    def setUp(self):
        self.test_shares = [Shares('TEA', 'Common', 100, True, 0, 0), Shares('POP', 'Common', 100, True, 8, 0), Shares('ALE', 'Common', 60, True, 23, 0), Shares('GIN', 'Preferred', 100, True, 8, 2), Shares('JOE', 'Common', 250, True, 13, 0), Shares('DYS', 'Preferred', 100, True, 0, 0), Shares('TSLA','Common',100,True,0,0)]
        self.test_index = Index('GBCE', self.test_shares)
        self.test_market = Market(self.test_shares + [self.test_index])

    def test_market_calculate_dividend_yield(self):
        self.assertEqual(round(self.test_market.calculate_dividend_yield('POP', 0.9),4), 0.0889)
        self.assertEqual(round(self.test_market.calculate_dividend_yield('GIN', 0.8),4), 0.0250)
        self.assertEqual(self.test_market.calculate_dividend_yield('DYS', 0.5), 0)
        self.assertEqual(self.test_market.calculate_dividend_yield('TSLA', 0.85), 0)

    def test_market_calculate_price_earnings_ratio(self):
        self.assertEqual(self.test_market.calculate_price_earning_ratio('TEA', 0.98), -1)
        self.assertEqual(self.test_market.calculate_price_earning_ratio('POP', 0.75), 9.375)
        self.assertEqual(round(self.test_market.calculate_price_earning_ratio('ALE', 0.6),3), 2.609)
        self.assertEqual(round(self.test_market.calculate_price_earning_ratio('GIN', 0.6),3), 7.500)

    def test_market_transact(self):
        self.assertIn(self.test_market.transact('TEA', 5, 'B')['transaction_id'],self.test_market.transaction_log)
        self.assertIn(self.test_market.transact('ALE', 3.5, 'B')['transaction_id'],self.test_market.transaction_log)
        self.assertIn(self.test_market.transact('JOE', 2.1, 'B')['transaction_id'],self.test_market.transaction_log)
        self.assertIn(self.test_market.transact('JOE', 0.1, 'B')['transaction_id'],self.test_market.transaction_log)

