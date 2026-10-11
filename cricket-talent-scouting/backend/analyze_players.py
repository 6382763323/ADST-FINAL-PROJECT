"""
Cricket Talent Scouting & Analysis System
Module: backend/analyze_players.py

Purpose:
Provides statistical analysis and role-specific talent scoring algorithms.
Features transparent, configurable weighting models for Batters, Bowlers,
All-rounders, and Wicketkeepers with normalization and head-to-head comparison.
"""

import os
import numpy as np
import pandas as pd

def get_cleaned_data(filepath=None):
    """
    Load the cleaned cricket players dataset.
    """
    if filepath is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, "..", "dataset", "cleaned_cricket_players.csv")
        
    if not os.path.exists(filepath):
        # Fallback to running cleaner if cleaned csv not yet generated
        from clean_data import clean_cricket_data
        return clean_cricket_data()
        
    return pd.read_csv(filepath)

def min_max_normalize(series, min_cap=None, max_cap=None):
    """
    Min-Max normalizes a series to a 0 - 100 scale.
    Optional capping prevents disproportionate skew from extreme outliers.
    """
    s = series.copy()
    if min_cap is not None:
        s = s.clip(lower=min_cap)
    if max_cap is not None:
        s = s.clip(upper=max_cap)
        
    s_min = s.min()
    s_max = s.max()
    
    if s_max == s_min:
        return pd.Series(50.0, index=series.index)
        
    return ((s - s_min) / (s_max - s_min)) * 100.0

def inverse_normalize(series, min_cap=None, max_cap=None):
    """
    Inverse normalization (lower values score higher).
    Essential for cricket bowling metrics: Bowling Average, Economy Rate, Bowling Strike Rate.
    """
    norm = min_max_normalize(series, min_cap, max_cap)
    return 100.0 - norm

def calculate_talent_scores(df, custom_weights=None):
    """
    Calculates role-specific and composite talent scores (0-100 scale).
    Allows custom weights to simulate different scouting philosophies (e.g., T20 vs ODI vs Test).
    """
    data = df.copy()
    
    # Default weighting configurations
    weights = {
        'batter': {
            'avg': 0.35,
            'sr': 0.30,
            'runs': 0.20,
            'milestones': 0.15
        },
        'bowler': {
            'avg': 0.30,
            'econ': 0.30,
            'wkts': 0.25,
            'sr': 0.15
        },
        'allrounder': {
            'bat': 0.50,
            'bowl': 0.50
        },
        'wicketkeeper': {
            'bat': 0.65,
            'field': 0.35
        }
    }
    
    if custom_weights:
        for role_key, w_dict in custom_weights.items():
            if role_key in weights and isinstance(w_dict, dict):
                weights[role_key].update(w_dict)
                
    # 1. Batting Normalizations
    norm_bat_avg = min_max_normalize(data['Batting_Average'], min_cap=10.0, max_cap=60.0)
    norm_bat_sr = min_max_normalize(data['Strike_Rate'], min_cap=60.0, max_cap=165.0)
    norm_runs = min_max_normalize(np.log1p(data['Runs']))
    milestones = data['Centuries'] * 2 + data['Fifties']
    norm_milestones = min_max_normalize(milestones, min_cap=0, max_cap=100)
    
    bw = weights['batter']
    data['Batter_Score'] = (
        bw['avg'] * norm_bat_avg +
        bw['sr'] * norm_bat_sr +
        bw['runs'] * norm_runs +
        bw['milestones'] * norm_milestones
    ).round(2)
    
    # 2. Bowling Normalizations
    bowl_mask = data['Wickets'] > 0
    data['Bowler_Score'] = 0.0
    
    if bowl_mask.any():
        norm_bowl_avg = inverse_normalize(data.loc[bowl_mask, 'Bowling_Average'], min_cap=15.0, max_cap=55.0)
        norm_econ = inverse_normalize(data.loc[bowl_mask, 'Economy_Rate'], min_cap=3.5, max_cap=9.0)
        norm_wkts = min_max_normalize(np.log1p(data.loc[bowl_mask, 'Wickets']))
        norm_bowl_sr = inverse_normalize(data.loc[bowl_mask, 'Bowling_Strike_Rate'], min_cap=15.0, max_cap=55.0)
        
        bow = weights['bowler']
        data.loc[bowl_mask, 'Bowler_Score'] = (
            bow['avg'] * norm_bowl_avg +
            bow['econ'] * norm_econ +
            bow['wkts'] * norm_wkts +
            bow['sr'] * norm_bowl_sr
        ).round(2)
        
    # 3. Fielding Normalization
    dismissals = data['Catches'] + (data['Stumpings'] * 1.5)
    norm_fielding = min_max_normalize(dismissals, min_cap=0, max_cap=300)
    
    # 4. Composite Role Talent Score
    composite_scores = []
    tiers = []
    
    ar_w = weights['allrounder']
    wk_w = weights['wicketkeeper']
    
    for idx, row in data.iterrows():
        role = row['Role']
        b_score = row['Batter_Score']
        bw_score = row['Bowler_Score']
        f_score = norm_fielding.iloc[idx]
        
        if role == 'Batter':
            final_score = b_score
        elif role == 'Bowler':
            final_score = bw_score
        elif role == 'All-rounder':
            final_score = round(ar_w['bat'] * b_score + ar_w['bowl'] * bw_score, 2)
        elif role == 'Wicketkeeper':
            final_score = round(wk_w['bat'] * b_score + wk_w['field'] * f_score, 2)
        else:
            final_score = b_score
            
        final_score = float(np.clip(final_score, 0.0, 100.0))
        composite_scores.append(round(final_score, 2))
        
        # Tier assignment
        if final_score >= 75.0:
            tiers.append('Elite / Grade 1')
        elif final_score >= 55.0:
            tiers.append('High Impact / Grade 2')
        elif final_score >= 40.0:
            tiers.append('Reliable / Grade 3')
        else:
            tiers.append('Development / Grade 4')
            
    data['Talent_Score'] = composite_scores
    data['Talent_Tier'] = tiers
    
    return data

def get_role_rankings(df, role=None, limit=20):
    """
    Returns ranked leaderboard of players filtered by role or overall.
    """
    scored_df = calculate_talent_scores(df)
    if role and role.lower() != 'all':
        scored_df = scored_df[scored_df['Role'].str.lower() == role.lower()]
        
    ranked = scored_df.sort_values(by='Talent_Score', ascending=False)
    if limit:
        ranked = ranked.head(limit)
        
    return ranked

def compare_two_players(df, player_id1, player_id2):
    """
    Compares two players side-by-side and returns head-to-head metrics,
    including 5-pillar radar scores (Batting, Consistency, Bowling, Economy, Fielding).
    """
    scored = calculate_talent_scores(df)
    
    p1_row = scored[scored['Player_ID'] == player_id1]
    p2_row = scored[scored['Player_ID'] == player_id2]
    
    if p1_row.empty or p2_row.empty:
        # Fallback to name search
        p1_row = scored[scored['Player'].str.lower() == str(player_id1).lower()]
        p2_row = scored[scored['Player'].str.lower() == str(player_id2).lower()]
        
    if p1_row.empty or p2_row.empty:
        raise ValueError("One or both player profiles could not be found.")
        
    p1 = p1_row.iloc[0].to_dict()
    p2 = p2_row.iloc[0].to_dict()
    
    # Generate 5-Pillar Radar Scores (0-100 scale)
    def calculate_radar_pillars(p):
        batting_power = float(np.clip((p['Strike_Rate'] / 160.0) * 100.0, 0, 100))
        consistency = float(np.clip((p['Batting_Average'] / 55.0) * 100.0, 0, 100))
        
        # Bowling threat
        if p['Wickets'] > 0 and p['Bowling_Strike_Rate'] > 0:
            bowling_threat = float(np.clip(100.0 - ((p['Bowling_Strike_Rate'] - 15) / 45.0) * 100.0, 10, 100))
        else:
            bowling_threat = 5.0
            
        # Economy control
        if p['Wickets'] > 0 and p['Economy_Rate'] > 0:
            economy_control = float(np.clip(100.0 - ((p['Economy_Rate'] - 3.5) / 6.0) * 100.0, 10, 100))
        else:
            economy_control = 5.0
            
        fielding_impact = float(np.clip(((p['Catches'] + p['Stumpings']) / 200.0) * 100.0, 10, 100))
        
        return {
            'Batting Power': round(batting_power, 1),
            'Consistency': round(consistency, 1),
            'Bowling Threat': round(bowling_threat, 1),
            'Economy Control': round(economy_control, 1),
            'Fielding Impact': round(fielding_impact, 1)
        }
        
    return {
        'player1': p1,
        'player2': p2,
        'p1_radar': calculate_radar_pillars(p1),
        'p2_radar': calculate_radar_pillars(p2)
    }

def get_dashboard_summary(df):
    """
    Returns aggregated dashboard statistics for API and frontend.
    """
    scored = calculate_talent_scores(df)
    
    total_players = len(scored)
    role_dist = scored['Role'].value_counts().to_dict()
    avg_bat_avg = round(float(scored[scored['Batting_Average'] > 0]['Batting_Average'].mean()), 2)
    avg_strike_rate = round(float(scored['Strike_Rate'].mean()), 2)
    total_runs = int(scored['Runs'].sum())
    total_wickets = int(scored['Wickets'].sum())
    
    # Top performers
    top_batter = scored[scored['Role'] == 'Batter'].sort_values(by='Runs', ascending=False).iloc[0].to_dict()
    top_bowler = scored[scored['Role'] == 'Bowler'].sort_values(by='Wickets', ascending=False).iloc[0].to_dict()
    top_allrounder = scored[scored['Role'] == 'All-rounder'].sort_values(by='Talent_Score', ascending=False).iloc[0].to_dict()
    top_keeper = scored[scored['Role'] == 'Wicketkeeper'].sort_values(by='Talent_Score', ascending=False).iloc[0].to_dict()
    
    # Tier breakdown
    tier_dist = scored['Talent_Tier'].value_counts().to_dict()
    
    return {
        'total_players': total_players,
        'role_distribution': role_dist,
        'tier_distribution': tier_dist,
        'avg_batting_average': avg_bat_avg,
        'avg_strike_rate': avg_strike_rate,
        'total_runs': total_runs,
        'total_wickets': total_wickets,
        'top_performers': {
            'batter': top_batter,
            'bowler': top_bowler,
            'allrounder': top_allrounder,
            'wicketkeeper': top_keeper
        }
    }

if __name__ == "__main__":
    df = get_cleaned_data()
    print("\n--- DASHBOARD SUMMARY ---")
    summary = get_dashboard_summary(df)
    print(f"Total Players: {summary['total_players']}")
    print(f"Role Breakdown: {summary['role_distribution']}")
    print(f"Tier Breakdown: {summary['tier_distribution']}")
    
    print("\n--- TOP 5 OVERALL RANKED TALENTS ---")
    rankings = get_role_rankings(df, limit=5)
    print(rankings[['Player', 'Country', 'Role', 'Talent_Score', 'Talent_Tier']])
