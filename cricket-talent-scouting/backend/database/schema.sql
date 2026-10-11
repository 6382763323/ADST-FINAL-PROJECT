-- Cricket Talent Scouting & Analysis System
-- SQLite Database Schema

DROP TABLE IF EXISTS analysis_history;
DROP TABLE IF EXISTS scouting_shortlist;
DROP TABLE IF EXISTS player_performance;
DROP TABLE IF EXISTS players;

CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    role TEXT NOT NULL,
    batting_style TEXT DEFAULT '-',
    bowling_style TEXT DEFAULT '-',
    age INTEGER DEFAULT 0,
    matches INTEGER DEFAULT 0,
    innings INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE player_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id TEXT UNIQUE NOT NULL,
    runs INTEGER DEFAULT 0,
    highest_score INTEGER DEFAULT 0,
    batting_avg REAL DEFAULT 0.0,
    strike_rate REAL DEFAULT 0.0,
    centuries INTEGER DEFAULT 0,
    fifties INTEGER DEFAULT 0,
    wickets INTEGER DEFAULT 0,
    bowling_avg REAL DEFAULT 0.0,
    economy_rate REAL DEFAULT 0.0,
    bowling_sr REAL DEFAULT 0.0,
    best_bowling TEXT DEFAULT '-',
    catches INTEGER DEFAULT 0,
    stumpings INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players (player_id) ON DELETE CASCADE
);

CREATE TABLE scouting_shortlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id TEXT NOT NULL,
    target_role TEXT,
    priority_tier TEXT DEFAULT 'Medium',
    scout_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players (player_id) ON DELETE CASCADE
);

CREATE TABLE analysis_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id TEXT,
    analysis_type TEXT NOT NULL,
    talent_score REAL DEFAULT 0.0,
    calculated_tier TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players (player_id) ON DELETE SET NULL
);

-- Indices for rapid querying and filtering
CREATE INDEX idx_players_role ON players(role);
CREATE INDEX idx_players_country ON players(country);
CREATE INDEX idx_perf_player_id ON player_performance(player_id);
CREATE INDEX idx_shortlist_player_id ON scouting_shortlist(player_id);
