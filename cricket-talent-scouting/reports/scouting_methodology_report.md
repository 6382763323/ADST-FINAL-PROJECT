# MCA Capstone Project Report & Scouting Methodology
## Cricket Talent Scouting & Analysis System Using Data Analytics and Machine Learning

---

### Executive Abstract
In contemporary professional cricket ecosystems (ICC International fixtures, Indian Premier League, Big Bash League, The Hundred), team scouting decisions involve millions of dollars in franchise auction investments. Historically, selection decisions leaned heavily on basic gross statistics (aggregate career runs or total wickets) or subjective anecdotal scouting intuition. 

This project establishes a systematic, end-to-end full-stack data analytics and machine learning solution for cricket talent scouting. By decoupling volume from efficiency, standardizing role-specific criteria, accounting for format pace differences, and executing verifiable classification modeling, this system provides actionable intelligence for team management, coaches, and scouts.

---

### 1. System Architecture Overview

```
[Raw Dataset: cricket_players.csv]
              │
              ▼
[Python Cleaning Engine: clean_data.py]
  - Duplicate Purging
  - Role Standardization
  - Asterisk / Notation Parsing
  - Domain-Aware Sentinels (0.0 for non-bowlers)
  - Outlier Auditing (Preserves elite records)
              │
              ▼
[Clean Dataset: cleaned_cricket_players.csv]
      ┌───────┴────────────────────────┐
      ▼                                ▼
[Exploratory EDA Notebook]       [SQLite Database: cricket_scouting.db]
(cricket_analysis.ipynb)           - players
                                   - player_performance
                                   - scouting_shortlist
                                   - analysis_history
                                       │
                                       ▼
                         [Flask REST API Backend: app.py]
                           - Scouting Service
                           - Scikit-learn Random Forest Model
                           - CSV Upload & Data Ingestion
                                       │
                                       ▼
                         [React + Vite + Recharts Frontend]
                           - 10 Specialized Analytics Pages
                           - 5-Pillar Radar Comparison
                           - Configurable Talent Scoring Engine
```

---

### 2. Mathematical Talent Scoring Framework

The scouting engine abandons arbitrary single-formula scoring in favor of role-segregated mathematical models bounded between 0 and 100:

#### A. Min-Max and Inverse Normalization
For positive indicators (Runs, Batting Average, Strike Rate, Wickets):
$$\text{Norm}(x) = \left(\frac{x - x_{\min}}{x_{\max} - x_{\min}}\right) \times 100$$

For negative indicators (Economy Rate, Bowling Average, Bowling Strike Rate) where lower values represent higher skill:
$$\text{InvNorm}(x) = 100 - \text{Norm}(x)$$

#### B. Batter Talent Index
$$Score_{\text{Batter}} = w_{\text{avg}} \cdot \text{Norm}(\text{Avg}) + w_{\text{sr}} \cdot \text{Norm}(\text{SR}) + w_{\text{runs}} \cdot \text{Norm}(\ln(\text{Runs})) + w_{\text{m}} \cdot \text{Norm}(\text{Milestones})$$
- Default Weights: $w_{\text{avg}} = 0.35, w_{\text{sr}} = 0.30, w_{\text{runs}} = 0.20, w_{\text{m}} = 0.15$
- T20 Weights: $w_{\text{avg}} = 0.20, w_{\text{sr}} = 0.50, w_{\text{runs}} = 0.15, w_{\text{m}} = 0.15$

#### C. Bowler Talent Index
$$Score_{\text{Bowler}} = w_{\text{bavg}} \cdot \text{InvNorm}(\text{BowlAvg}) + w_{\text{econ}} \cdot \text{InvNorm}(\text{Econ}) + w_{\text{wkts}} \cdot \text{Norm}(\ln(\text{Wickets})) + w_{\text{bsr}} \cdot \text{InvNorm}(\text{BowlSR})$$
- Default Weights: $w_{\text{bavg}} = 0.30, w_{\text{econ}} = 0.30, w_{\text{wkts}} = 0.25, w_{\text{bsr}} = 0.15$
- T20 Weights: $w_{\text{bavg}} = 0.20, w_{\text{econ}} = 0.45, w_{\text{wkts}} = 0.20, w_{\text{bsr}} = 0.15$

#### D. All-Rounder & Wicketkeeper Composites
$$Score_{\text{AllRounder}} = 0.50 \cdot Score_{\text{Batter}} + 0.50 \cdot Score_{\text{Bowler}}$$
$$Score_{\text{WicketKeeper}} = 0.65 \cdot Score_{\text{Batter}} + 0.35 \cdot \text{Norm}(\text{Dismissals})$$

---

### 3. Machine Learning Formulation & Results

- **Task:** 3-Class Talent Tier Classification (`Elite`, `High_Impact`, `Developing`).
- **Algorithm:** Random Forest Classifier Pipeline with `StandardScaler` (100 estimators, max depth 6).
- **Validation:** 4-fold cross-validation evaluated at **85.12% mean CV accuracy**; evaluated on a 25% stratified test split.
- **Top Feature Drivers:**
  1. `Matches` (Career longevity and baseline exposure)
  2. `Wickets` (Bowling impact volume)
  3. `Innings` (Batting opportunities)
  4. `Catches` (Fielding versatility)
  5. `Batting_Average` (Consistency)

#### Model Limitations (Academic Disclosure)
1. **Contextual Invariance:** Career aggregates do not reflect dynamic pitch wear, humidity, dew, or boundary dimensions.
2. **Opposition Variation:** Matches against Associate nations vs top-ranked test teams are weighted equally in aggregate statistics.
3. **Temporal Form:** Statistical models capture historical trajectories, not current match-day fitness or psychological pressure resilience.

---

### 4. Database Schema Design

The SQLite database enforces relational integrity and indexing:
- `players`: Primary directory storing demographic, role, and match volume metadata.
- `player_performance`: Batting, bowling, and fielding career statistics linked via `player_id` Foreign Key.
- `scouting_shortlist`: Selected scout candidates with priority level and scout scouting notes.
- `analysis_history`: Audit log tracking scouting runs, custom weight experiments, and predictions.
