"""
Unit Tests: Data Cleaning Pipeline
File: backend/tests/test_data_cleaning.py
"""

import os
import sys
import unittest
import pandas as pd

# Add backend directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from clean_data import clean_cricket_data, get_dataset_paths

class TestDataCleaning(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        raw_path, clean_path = get_dataset_paths()
        cls.raw_path = raw_path
        cls.clean_path = clean_path
        cls.df_clean = clean_cricket_data(verbose=False)
        
    def test_dataset_exists(self):
        self.assertTrue(os.path.exists(self.raw_path), "Raw dataset must exist.")
        self.assertTrue(os.path.exists(self.clean_path), "Cleaned dataset must exist.")
        
    def test_no_duplicate_players(self):
        duplicates = self.df_clean.duplicated(subset=['Player_ID']).sum()
        self.assertEqual(duplicates, 0, "Cleaned dataset must have zero duplicate Player_IDs.")
        
    def test_role_normalization(self):
        valid_roles = {'Batter', 'Bowler', 'All-rounder', 'Wicketkeeper'}
        unique_roles = set(self.df_clean['Role'].unique())
        self.assertTrue(unique_roles.issubset(valid_roles), f"Found unnormalized roles: {unique_roles - valid_roles}")
        
    def test_highest_score_numeric(self):
        # Must be integer and not contain asterisk
        self.assertTrue(pd.api.types.is_integer_dtype(self.df_clean['Highest_Score']), "Highest_Score must be numeric integer.")
        self.assertTrue((self.df_clean['Highest_Score'] >= 0).all(), "Highest_Score cannot be negative.")
        
    def test_no_null_values(self):
        null_count = self.df_clean.isnull().sum().sum()
        self.assertEqual(null_count, 0, f"Cleaned dataset should not have null values. Found: {null_count}")
        
    def test_engineered_features_exist(self):
        expected_cols = ['Milestones_Total', 'Dismissals_Total', 'Batting_Impact', 'Bowling_Impact']
        for col in expected_cols:
            self.assertIn(col, self.df_clean.columns, f"Engineered column {col} must exist.")

if __name__ == '__main__':
    unittest.main()
