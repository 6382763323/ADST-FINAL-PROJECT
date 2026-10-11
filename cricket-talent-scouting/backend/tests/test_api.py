"""
Integration Tests: Database and API Functionality
File: backend/tests/test_api.py
"""

import os
import sys
import unittest
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.db import (
    init_db,
    get_all_players,
    get_player_by_id,
    insert_or_update_player,
    delete_player,
    get_shortlist,
    add_to_shortlist,
    remove_from_shortlist
)

class TestDatabaseAndAPI(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        init_db()
        
    def test_database_query_players(self):
        players = get_all_players(limit=10)
        self.assertGreater(len(players), 0, "Database should contain seeded players.")
        first = players[0]
        self.assertIn('name', first)
        self.assertIn('role', first)
        self.assertIn('runs', first)
        
    def test_filter_by_role(self):
        batters = get_all_players(role='Batter', limit=10)
        self.assertTrue(all(p['role'] == 'Batter' for p in batters))
        
    def test_insert_and_delete_player(self):
        test_player = {
            'player_id': 'TEST_SCOUT_01',
            'name': 'Scout Prospect John',
            'country': 'India',
            'role': 'Batter',
            'batting_style': 'Right-hand bat',
            'age': 22,
            'matches': 15,
            'innings': 14,
            'runs': 650,
            'highest_score': 105,
            'batting_avg': 46.4,
            'strike_rate': 142.5,
            'centuries': 1,
            'fifties': 4
        }
        saved = insert_or_update_player(test_player)
        self.assertIsNotNone(saved)
        self.assertEqual(saved['name'], 'Scout Prospect John')
        
        # Verify fetch
        fetched = get_player_by_id('TEST_SCOUT_01')
        self.assertEqual(fetched['runs'], 650)
        
        # Clean up
        deleted = delete_player('TEST_SCOUT_01')
        self.assertTrue(deleted)
        self.assertIsNone(get_player_by_id('TEST_SCOUT_01'))
        
    def test_shortlist_operations(self):
        # Pick an existing player
        players = get_all_players(limit=1)
        p_id = players[0]['player_id']
        
        item_id = add_to_shortlist(p_id, 'Top Order Batter', 'High Priority', 'Excellent strike rotation')
        self.assertIsNotNone(item_id)
        
        shortlist = get_shortlist()
        self.assertTrue(any(s['player_id'] == p_id for s in shortlist))
        
        # Remove
        removed = remove_from_shortlist(item_id)
        self.assertTrue(removed)

    def test_flask_app_endpoints(self):
        try:
            from app import app
            client = app.test_client()
            
            # Health check
            res = client.get('/api/health')
            self.assertEqual(res.status_code, 200)
            
            # Dashboard
            dash_res = client.get('/api/analytics/dashboard')
            self.assertEqual(dash_res.status_code, 200)
            data = json.loads(dash_res.data)
            self.assertEqual(data['status'], 'success')
            
            # Rankings
            rank_res = client.get('/api/analytics/rankings?role=Batter&limit=5')
            self.assertEqual(rank_res.status_code, 200)
            
            # Model Info
            model_res = client.get('/api/analytics/model-info')
            self.assertEqual(model_res.status_code, 200)
            
        except ImportError:
            self.skipTest("Flask not yet installed in active Python environment. Skipping HTTP endpoint tests.")

if __name__ == '__main__':
    unittest.main()
