"""Protect interpretation of partial coverage and year-on-year observations."""
import unittest
from scripts.summarize_market import aggregate_daily, aggregate_monthly


class MarketTests(unittest.TestCase):
    def test_partial_daily_quarter_keeps_coverage(self):
        rows = [{'date': '2026-10-31', 'country': 'US', 'metric': 'share', 'value': 4}]
        out = aggregate_daily(rows)[0]
        self.assertTrue(out['partial_quarter'])
        self.assertEqual(out['last_date'], '2026-10-31')
        self.assertEqual(out['n_observations'], 1)

    def test_monthly_yoy_rates_are_averaged(self):
        rows = [{'date': f'2025-{m:02d}-01', 'country': 'CA', 'metric': 'growth_yoy',
                 'group': 'all', 'value_pct': v} for m, v in [(1, 12), (2, -3), (3, 6)]]
        out = aggregate_monthly(rows)[0]
        self.assertEqual(out['value_pct'], 5)
        self.assertFalse(out['partial_quarter'])
        self.assertIn('not quarter-on-quarter', out['aggregation'])

    def test_quarter_with_only_one_month_is_partial(self):
        rows = [{'date': '2026-10-01', 'country': 'US', 'metric': 'growth_yoy',
                 'group': 'all', 'value_pct': -2}]
        out = aggregate_monthly(rows)[0]
        self.assertTrue(out['partial_quarter'])
        self.assertEqual(out['n_months'], 1)


if __name__ == '__main__':
    unittest.main()
