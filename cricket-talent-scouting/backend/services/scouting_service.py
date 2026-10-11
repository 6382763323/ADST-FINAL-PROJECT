"""
Cricket Talent Scouting & Analysis System
Service: backend/services/scouting_service.py

Purpose:
Encapsulates scouting business logic, multi-criteria talent rankings,
comparisons, and CSV report generation.
"""

import os
import io
import csv
import pandas as pd
from analyze_players import (
    calculate_talent_scores,
    compare_two_players,
    get_dashboard_summary,
    get_role_rankings,
    get_cleaned_data
)
from database.db import (
    get_all_players,
    get_player_by_id,
    insert_or_update_player,
    delete_player,
    get_shortlist,
    add_to_shortlist,
    remove_from_shortlist
)

def get_scouting_rankings(role=None, custom_weights=None, limit=50):
    """
    Computes real-time dynamic talent scores with custom weight configuration.
    """
    df = get_cleaned_data()
    scored_df = calculate_talent_scores(df, custom_weights=custom_weights)
    
    if role and role.lower() != 'all':
        scored_df = scored_df[scored_df['Role'].str.lower() == role.lower()]
        
    ranked = scored_df.sort_values(by='Talent_Score', ascending=False)
    if limit:
        ranked = ranked.head(limit)
        
    return ranked.to_dict(orient='records')

def get_player_head_to_head(player_id1, player_id2):
    """
    Returns head-to-head comparison with radar chart pillars.
    """
    df = get_cleaned_data()
    return compare_two_players(df, player_id1, player_id2)

def generate_scouting_report_csv():
    """
    Generates a full CSV report string with calculated talent metrics.
    """
    df = get_cleaned_data()
    scored_df = calculate_talent_scores(df)
    ranked = scored_df.sort_values(by='Talent_Score', ascending=False)
    
    output = io.StringIO()
    ranked.to_csv(output, index=False)
    return output.getvalue()
