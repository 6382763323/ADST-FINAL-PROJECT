"""
Cricket Talent Scouting & Analysis System
Module: backend/database/db.py

Purpose:
Manages SQLite database connections, executes schema initialization,
seeds tables from cleaned_cricket_players.csv, and provides clean CRUD helpers
for players, performances, shortlists, and scouting history.
"""

import os
import sqlite3
import pandas as pd

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cricket_scouting.db")
SCHEMA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")

def get_db_connection():
    """
    Returns a connection to the SQLite database with Row row_factory
    for dictionary-like access.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(force_reseed=False):
    """
    Initializes tables from schema.sql.
    Seeds player records from cleaned CSV if database is newly initialized.
    """
    conn = get_db_connection()
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database schema successfully created.")
    
    # Check if seed data exists
    seed_from_cleaned_csv()

def seed_from_cleaned_csv():
    """
    Populates 'players' and 'player_performance' tables from cleaned_cricket_players.csv.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.abspath(os.path.join(base_dir, "..", "..", "dataset", "cleaned_cricket_players.csv"))
    
    if not os.path.exists(csv_path):
        print(f"Seed file not found at {csv_path}. Skipping initial seeding.")
        return
        
    df = pd.read_csv(csv_path)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if players already exist
    cursor.execute("SELECT COUNT(*) FROM players")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
        
    print(f"Seeding database with {len(df)} players from {csv_path}...")
    
    for _, r in df.iterrows():
        p_id = str(r['Player_ID'])
        cursor.execute("""
            INSERT OR REPLACE INTO players 
            (player_id, name, country, role, batting_style, bowling_style, age, matches, innings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p_id, str(r['Player']), str(r['Country']), str(r['Role']),
            str(r.get('Batting_Style', '-')), str(r.get('Bowling_Style', '-')),
            int(r.get('Age', 0)), int(r.get('Matches', 0)), int(r.get('Innings', 0))
        ))
        
        cursor.execute("""
            INSERT OR REPLACE INTO player_performance
            (player_id, runs, highest_score, batting_avg, strike_rate, centuries, fifties,
             wickets, bowling_avg, economy_rate, bowling_sr, best_bowling, catches, stumpings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p_id, int(r.get('Runs', 0)), int(r.get('Highest_Score', 0)),
            float(r.get('Batting_Average', 0.0)), float(r.get('Strike_Rate', 0.0)),
            int(r.get('Centuries', 0)), int(r.get('Fifties', 0)),
            int(r.get('Wickets', 0)), float(r.get('Bowling_Average', 0.0)),
            float(r.get('Economy_Rate', 0.0)), float(r.get('Bowling_Strike_Rate', 0.0)),
            str(r.get('Best_Bowling', '-')), int(r.get('Catches', 0)), int(r.get('Stumpings', 0))
        ))
        
    conn.commit()
    conn.close()
    print("Database seeding completed.")

def get_all_players(search=None, role=None, country=None, sort_by="runs", order="desc", limit=100):
    """
    Queries joined player profiles and performances with filtering and sorting.
    """
    conn = get_db_connection()
    query = """
        SELECT p.*, perf.runs, perf.highest_score, perf.batting_avg, perf.strike_rate,
               perf.centuries, perf.fifties, perf.wickets, perf.bowling_avg,
               perf.economy_rate, perf.bowling_sr, perf.best_bowling, perf.catches, perf.stumpings
        FROM players p
        JOIN player_performance perf ON p.player_id = perf.player_id
        WHERE 1=1
    """
    params = []
    
    if search:
        query += " AND (p.name LIKE ? OR p.country LIKE ? OR p.player_id LIKE ?)"
        s_term = f"%{search}%"
        params.extend([s_term, s_term, s_term])
        
    if role and role.lower() != 'all':
        query += " AND LOWER(p.role) = LOWER(?)"
        params.append(role)
        
    if country and country.lower() != 'all':
        query += " AND LOWER(p.country) = LOWER(?)"
        params.append(country)
        
    # Safe sorting column mapping
    sort_mapping = {
        'name': 'p.name',
        'matches': 'p.matches',
        'runs': 'perf.runs',
        'batting_avg': 'perf.batting_avg',
        'strike_rate': 'perf.strike_rate',
        'wickets': 'perf.wickets',
        'economy_rate': 'perf.economy_rate'
    }
    col = sort_mapping.get(sort_by.lower(), 'perf.runs')
    direction = "DESC" if order.lower() == "desc" else "ASC"
    
    query += f" ORDER BY {col} {direction}"
    if limit:
        query += f" LIMIT {int(limit)}"
        
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_player_by_id(player_id):
    """
    Fetches full player profile and performance by player_id.
    """
    conn = get_db_connection()
    query = """
        SELECT p.*, perf.runs, perf.highest_score, perf.batting_avg, perf.strike_rate,
               perf.centuries, perf.fifties, perf.wickets, perf.bowling_avg,
               perf.economy_rate, perf.bowling_sr, perf.best_bowling, perf.catches, perf.stumpings
        FROM players p
        JOIN player_performance perf ON p.player_id = perf.player_id
        WHERE p.player_id = ? OR LOWER(p.name) = LOWER(?)
    """
    row = conn.execute(query, (player_id, player_id)).fetchone()
    conn.close()
    return dict(row) if row else None

def insert_or_update_player(player_data):
    """
    Inserts a new player or updates an existing player record.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    p_id = player_data.get('player_id')
    
    cursor.execute("""
        INSERT OR REPLACE INTO players 
        (player_id, name, country, role, batting_style, bowling_style, age, matches, innings)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        p_id, player_data.get('name', 'Unknown'), player_data.get('country', 'Unknown'),
        player_data.get('role', 'Batter'), player_data.get('batting_style', '-'),
        player_data.get('bowling_style', '-'), int(player_data.get('age', 25)),
        int(player_data.get('matches', 0)), int(player_data.get('innings', 0))
    ))
    
    cursor.execute("""
        INSERT OR REPLACE INTO player_performance
        (player_id, runs, highest_score, batting_avg, strike_rate, centuries, fifties,
         wickets, bowling_avg, economy_rate, bowling_sr, best_bowling, catches, stumpings)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        p_id, int(player_data.get('runs', 0)), int(player_data.get('highest_score', 0)),
        float(player_data.get('batting_avg', 0.0)), float(player_data.get('strike_rate', 0.0)),
        int(player_data.get('centuries', 0)), int(player_data.get('fifties', 0)),
        int(player_data.get('wickets', 0)), float(player_data.get('bowling_avg', 0.0)),
        float(player_data.get('economy_rate', 0.0)), float(player_data.get('bowling_sr', 0.0)),
        str(player_data.get('best_bowling', '-')), int(player_data.get('catches', 0)),
        int(player_data.get('stumpings', 0))
    ))
    
    conn.commit()
    conn.close()
    return get_player_by_id(p_id)

def delete_player(player_id):
    """
    Deletes a player by player_id. Cascades to performance and shortlist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scouting_shortlist WHERE player_id = ?", (player_id,))
    cursor.execute("DELETE FROM player_performance WHERE player_id = ?", (player_id,))
    cursor.execute("DELETE FROM players WHERE player_id = ?", (player_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

# Shortlist helpers
def get_shortlist():
    conn = get_db_connection()
    query = """
        SELECT s.*, p.name, p.country, p.role, perf.runs, perf.batting_avg, perf.wickets, perf.economy_rate
        FROM scouting_shortlist s
        JOIN players p ON s.player_id = p.player_id
        JOIN player_performance perf ON s.player_id = perf.player_id
        ORDER BY s.created_at DESC
    """
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_to_shortlist(player_id, target_role, priority_tier='High', scout_notes=''):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scouting_shortlist (player_id, target_role, priority_tier, scout_notes)
        VALUES (?, ?, ?, ?)
    """, (player_id, target_role, priority_tier, scout_notes))
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id

def remove_from_shortlist(shortlist_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scouting_shortlist WHERE id = ? OR player_id = ?", (shortlist_id, shortlist_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

if __name__ == "__main__":
    init_db()
    players = get_all_players(limit=3)
    print(f"Sample queried players ({len(players)}):")
    for p in players:
        print(f" - {p['player_id']}: {p['name']} ({p['role']}) - Runs: {p['runs']}, Wkts: {p['wickets']}")
