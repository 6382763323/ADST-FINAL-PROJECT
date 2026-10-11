"""
Unit Tests: Talent Ranking and Scoring Engine
File: backend/tests/test_talent_ranking.py
"""

import os
import sys
import unittest
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from analyze_players import (
    get_cleaned_data,
    calculate_talent_scores,
    compare_two_players,
    min_max_normalize,
    inverse_normalize
)

class TestTalentRanking(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.df = get_cleaned_data()
        cls.scored_df = calculate_talent_scores(cls.df)
        
    def test_normalization_bounds(self):
        s = pd.Series([10, 20, 30, 40, 50])
        norm = min_max_normalize(s)
        self.assertAlmostEqual(norm.min(), 0.0)
        self.assertAlmostEqual(norm.max(), 100.0)
        
        inv = inverse_normalize(s)
        self.assertAlmostEqual(inv.min(), 0.0)
        self.assertAlmostEqual(inv.max(), 100.0)
        self.assertEqual(inv.iloc[0], 100.0)  # Lowest input gets highest inverse score
        
    def test_talent_scores_range(self):
        self.assertIn('Talent_Score', self.scored_df.columns)
        self.assertTrue((self.scored_df['Talent_Score'] >= 0.0).all())
        self.assertTrue((self.scored_df['Talent_Score'] <= 100.0).all())
        
    def test_tier_assignment(self):
        valid_tiers = {
            'Elite / Grade 1',
            'High Impact / Grade 2',
            'Reliable / Grade 3',
            'Development / Grade 4'
        }
        tiers_in_data = set(self.scored_df['Talent_Tier'].unique())
        self.assertTrue(tiers_in_data.issubset(valid_tiers))
        
    def test_custom_weights(self):
        # Adjust weight to emphasize strike rate heavily
        custom_w = {'batter': {'avg': 0.10, 'sr': 0.70, 'runs': 0.10, 'milestones': 0.10}}
        custom_scored = calculate_talent_scores(self.df, custom_weights=custom_w)
        
        # High strike-rate batter (e.g. Suryakumar Yadav) should score higher under SR-heavy model
        sky_default = self.scored_df[self.scored_df['Player'] == 'Suryakumar Yadav']['Talent_Score'].iloc[0]
        sky_custom = custom_scored[custom_scored['Player'] == 'Suryakumar Yadav']['Talent_Score'].iloc[0]
        self.assertGreater(sky_custom, sky_default)
        
    def test_player_comparison(self):
        comp = compare_two_players(self.df, "CRIC_001", "CRIC_002")
        self.assertIn('player1', comp)
        self.assertIn('player2', comp)
        self.assertIn('p1_radar', comp)
        self.assertIn('p2_radar', comp)
        self.assertIn('Batting Power', comp['p1_radar'])

if __name__ == '__main__':
    unittest.main()
