"""
Generator script for notebooks/cricket_analysis.ipynb
Creates a complete, 17-section MCA Capstone Jupyter Notebook with detailed
Markdown notes, clean code cells, and statistical visualizations.
"""
import os
import nbformat as nbf

notebook_dir = r"c:\Users\abhis\OneDrive\Desktop\ADSproject\cricket-talent-scouting\notebooks"
os.makedirs(notebook_dir, exist_ok=True)
notebook_path = os.path.join(notebook_dir, "cricket_analysis.ipynb")

nb = nbf.v4.new_notebook()
nb.metadata = {
    "language_info": {"name": "python", "version": "3.11"},
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
}

cells = []

# Section 1
cells.append(nbf.v4.new_markdown_cell("""# 🏏 Cricket Talent Scouting & Analysis System
### MCA Capstone Project — Exploratory Data Analysis & Talent Ranking Pipeline

---

## 1. Project Introduction
In modern professional cricket (across Test, ODI, and franchise T20 leagues), scouting and talent acquisition cannot rely solely on basic raw stats like total runs or total wickets. Total runs often favor players who bat in top positions or have simply played more matches over many years, while overlooking explosive strike rates, clutch averages, or role-specific discipline.

### Objectives of this System:
1. **Data Cleaning & Normalization:** Handle missing data, standardize roles, parse complex cricket notation (e.g., unbeaten scores `*`), and audit outliers without discarding genuine world-class records.
2. **Exploratory Data Analysis (EDA):** Perform granular batting, bowling, fielding, and demographic analysis.
3. **Role-Specific Performance Metrics:** Segment players into Batters, Bowlers, All-rounders, and Wicketkeepers.
4. **Transparent Talent Scoring Formula:** Provide a weighted, normalized multi-metric talent score (0-100) instead of a black-box formula.
5. **Data-Driven Player Comparison:** Enable head-to-head scouting comparisons for team drafting and auction strategies.
"""))

# Section 2
cells.append(nbf.v4.new_markdown_cell("""---
## 2. Dataset Source & Description

- **Data Source:** Compiled from public cricket records (ESPNcricinfo & ICC multi-format player profiles) and Kaggle open cricket repositories.
- **File Location:** `../dataset/cricket_players.csv`
- **Cleaned Target:** `../dataset/cleaned_cricket_players.csv`

### Data Dictionary:
| Column | Description |
| :--- | :--- |
| `Player_ID` | Unique scout identifier (e.g., `CRIC_001`) |
| `Player` | Player full name |
| `Country` | National team / cricketing nation |
| `Role` | Primary role (`Batter`, `Bowler`, `All-rounder`, `Wicketkeeper`) |
| `Batting_Style` | Right-hand bat / Left-hand bat |
| `Bowling_Style` | Bowling category (Fast, Medium, Spin, Orthodox, Legbreak) |
| `Age` | Player age in years |
| `Matches`, `Innings` | Match volume and batting opportunities |
| `Runs`, `Highest_Score` | Run tally and highest individual score |
| `Batting_Average`, `Strike_Rate` | Scoring consistency and scoring pace |
| `Centuries`, `Fifties` | Major scoring milestones |
| `Wickets`, `Bowling_Average` | Wickets taken and runs conceded per wicket |
| `Economy_Rate`, `Bowling_Strike_Rate` | Conceded runs per over and balls per dismissal |
| `Best_Bowling` | Best match bowling figures (e.g. `6/19`) |
| `Catches`, `Stumpings` | Fielding and wicketkeeping dismissals |
"""))

# Section 3
cells.append(nbf.v4.new_markdown_cell("""---
## 3. Library Imports
We import standard data science and visualization libraries: `numpy`, `pandas`, `matplotlib`, and `seaborn`.
"""))

cells.append(nbf.v4.new_code_cell("""import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual styling for cricket analytics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11

print("✅ Data analysis and plotting libraries loaded successfully.")
"""))

# Section 4
cells.append(nbf.v4.new_markdown_cell("""---
## 4. Dataset Loading & Inspection
We load the raw CSV dataset and examine its initial dimensions, columns, and data types.
"""))

cells.append(nbf.v4.new_code_cell("""dataset_path = os.path.join('..', 'dataset', 'cricket_players.csv')
raw_df = pd.read_csv(dataset_path)

print(f"Dataset Shape: {raw_df.shape[0]} Rows, {raw_df.shape[1]} Columns")
print("\\nFirst 5 Records:")
display(raw_df.head())

print("\\nData Types & Memory Usage:")
display(raw_df.dtypes)
"""))

# Section 5
cells.append(nbf.v4.new_markdown_cell("""---
## 5. Missing Value Analysis
In sports analytics, missing values often represent structural domain realities rather than corrupt data. For instance:
- Pure Batters rarely bowl, leaving `Bowling_Average`, `Economy_Rate`, and `Bowling_Strike_Rate` as `NaN`.
- Tailend Bowlers with few batting innings may lack defined batting averages if not dismissed.
"""))

cells.append(nbf.v4.new_code_cell("""missing_counts = raw_df.isnull().sum()
missing_pct = (missing_counts / len(raw_df)) * 100

missing_df = pd.DataFrame({'Missing_Count': missing_counts, 'Percentage (%)': missing_pct.round(2)})
display(missing_df[missing_df['Missing_Count'] > 0])

# Bar plot of missing columns
plt.figure(figsize=(9, 4))
missing_df[missing_df['Missing_Count'] > 0]['Missing_Count'].plot(kind='bar', color='#e11d48')
plt.title('Missing Value Audit Across Features')
plt.ylabel('Missing Records Count')
plt.xticks(rotation=25)
plt.tight_layout()
plt.show()
"""))

# Section 6
cells.append(nbf.v4.new_markdown_cell("""---
## 6. Duplicate & Invalid Data Checks
We check for duplicated player identifiers or duplicate player names.
"""))

cells.append(nbf.v4.new_code_cell("""duplicates = raw_df.duplicated(subset=['Player_ID']).sum()
print(f"Identified duplicate Player_IDs: {duplicates}")

if duplicates > 0:
    print("Duplicate entries found:")
    display(raw_df[raw_df.duplicated(subset=['Player_ID'], keep=False)])
"""))

# Section 7
cells.append(nbf.v4.new_markdown_cell("""---
## 7. Data Cleaning & Preprocessing
Here we apply the structured data transformations:
1. Drop duplicate records.
2. Strip trailing whitespaces and normalize role classifications (`BATTER ` -> `Batter`, `All-Rounder` -> `All-rounder`).
3. Strip asterisk notations from `Highest_Score` (e.g., `264*` -> `264`) and record an `Is_Highest_Score_NotOut` flag.
4. Convert types and impute domain-specific sentinels (`0.0` for non-bowling metrics).
5. Engineer composite analytical indicators: `Milestones_Total`, `Batting_Impact`, and `Bowling_Impact`.
"""))

cells.append(nbf.v4.new_code_cell("""df = raw_df.copy()

# 1. Drop duplicates
df = df.drop_duplicates(subset=['Player_ID'], keep='first')

# 2. Normalize text and roles
for col in ['Player', 'Country', 'Role', 'Batting_Style', 'Bowling_Style']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

role_mapping = {
    'BATTER': 'Batter', 'Batter': 'Batter', 'Batsman': 'Batter',
    'Bowler': 'Bowler', 'BOWLER': 'Bowler',
    'All-Rounder': 'All-rounder', 'all-rounder': 'All-rounder',
    'All Rounder': 'All-rounder', 'All-rounder': 'All-rounder',
    'Wicketkeeper': 'Wicketkeeper', 'WK': 'Wicketkeeper'
}
df['Role'] = df['Role'].map(lambda x: role_mapping.get(x, x.title()))

# 3. Clean Highest_Score
df['Is_Highest_Score_NotOut'] = df['Highest_Score'].astype(str).str.contains(r'\\*').astype(int)
df['Highest_Score'] = pd.to_numeric(
    df['Highest_Score'].astype(str).str.replace('*', '', regex=False).str.strip(),
    errors='coerce'
).fillna(0).astype(int)

# 4. Impute numerical columns
int_cols = ['Age', 'Matches', 'Innings', 'Runs', 'Centuries', 'Fifties', 'Wickets', 'Catches', 'Stumpings']
for col in int_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

float_cols = ['Batting_Average', 'Strike_Rate', 'Bowling_Average', 'Economy_Rate', 'Bowling_Strike_Rate']
for col in float_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df['Bowling_Average'] = df['Bowling_Average'].fillna(0.0).round(2)
df['Economy_Rate'] = df['Economy_Rate'].fillna(0.0).round(2)
df['Bowling_Strike_Rate'] = df['Bowling_Strike_Rate'].fillna(0.0).round(2)
df['Batting_Average'] = df['Batting_Average'].fillna(0.0).round(2)
df['Strike_Rate'] = df['Strike_Rate'].fillna(75.0).round(2)
df['Best_Bowling'] = df['Best_Bowling'].fillna('-').astype(str).str.strip()

# 5. Feature Engineering
df['Milestones_Total'] = df['Centuries'] + df['Fifties']
df['Dismissals_Total'] = df['Catches'] + df['Stumpings']
df['Batting_Impact'] = ((df['Runs'] / df['Matches'].clip(lower=1)) * (df['Strike_Rate'] / 100.0)).round(2)
df['Bowling_Impact'] = df.apply(
    lambda r: round((r['Wickets'] / max(r['Matches'], 1)) * (10.0 / max(r['Economy_Rate'], 3.0)), 2)
    if r['Wickets'] > 0 and r['Economy_Rate'] > 0 else 0.0,
    axis=1
)

print(f"Cleaned DataFrame Shape: {df.shape}")
print(f"Remaining Missing Values: {df.isnull().sum().sum()}")
display(df.head())
"""))

# Section 8
cells.append(nbf.v4.new_markdown_cell("""---
## 8. Exploratory Data Analysis (EDA)
Summary statistics of key metrics across the entire dataset.
"""))

cells.append(nbf.v4.new_code_cell("""display(df[['Age', 'Matches', 'Runs', 'Batting_Average', 'Strike_Rate', 'Wickets', 'Economy_Rate']].describe().round(2))
"""))

# Section 9
cells.append(nbf.v4.new_markdown_cell("""---
## 9. Batting Performance Analysis
Here we evaluate Batters and All-rounders on scoring volume (`Runs`), consistency (`Batting_Average`), and aggressive tempo (`Strike_Rate`).
"""))

cells.append(nbf.v4.new_code_cell("""top_batters = df.sort_values(by='Runs', ascending=False).head(10)

plt.figure(figsize=(11, 5))
sns.barplot(data=top_batters, x='Runs', y='Player', hue='Role', palette='crest')
plt.title('Top 10 All-Time Run Scorers')
plt.xlabel('Career Runs')
plt.tight_layout()
plt.show()

# Scatter Plot: Batting Average vs Strike Rate
active_bats = df[(df['Runs'] >= 500) & (df['Role'].isin(['Batter', 'All-rounder', 'Wicketkeeper']))]

plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(
    data=active_bats,
    x='Batting_Average', y='Strike_Rate',
    hue='Role', size='Runs', sizes=(40, 400),
    palette='viridis', alpha=0.85
)
plt.axvline(40, color='gray', linestyle='--', alpha=0.6, label='Elite Avg Benchmark (40)')
plt.axhline(100, color='red', linestyle='--', alpha=0.6, label='Modern SR Benchmark (100)')
plt.title('Batting Average vs. Batting Strike Rate (Bubble Size = Runs)')
plt.xlabel('Batting Average')
plt.ylabel('Strike Rate')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
"""))

# Section 10
cells.append(nbf.v4.new_markdown_cell("""---
## 10. Bowling Performance Analysis
We analyze wicket-takers on volume (`Wickets`), stinginess (`Economy_Rate`), and strike efficiency (`Bowling_Strike_Rate`).
"""))

cells.append(nbf.v4.new_code_cell("""active_bowlers = df[(df['Wickets'] >= 30) & (df['Role'].isin(['Bowler', 'All-rounder']))]
top_bowlers = active_bowlers.sort_values(by='Wickets', ascending=False).head(10)

plt.figure(figsize=(11, 5))
sns.barplot(data=top_bowlers, x='Wickets', y='Player', hue='Bowling_Style', palette='mako')
plt.title('Top 10 Wicket Takers')
plt.xlabel('Career Wickets')
plt.tight_layout()
plt.show()

# Economy Rate vs Bowling Average (Lower is better in both!)
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=active_bowlers,
    x='Economy_Rate', y='Bowling_Average',
    hue='Role', size='Wickets', sizes=(50, 450),
    palette='flare', alpha=0.85
)
plt.title('Economy Rate vs. Bowling Average (Bottom-Left Quadrant = Elite Bowlers)')
plt.xlabel('Economy Rate (Runs/Over)')
plt.ylabel('Bowling Average (Runs/Wicket)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
"""))

# Section 11
cells.append(nbf.v4.new_markdown_cell("""---
## 11. Fielding Analysis
Fielding contribution is measured through Catches and Stumpings. Wicketkeepers generate decisive dismissals, while outfielders save vital runs.
"""))

cells.append(nbf.v4.new_code_cell("""top_fielders = df.sort_values(by='Dismissals_Total', ascending=False).head(10)

plt.figure(figsize=(10, 5))
sns.barplot(data=top_fielders, x='Dismissals_Total', y='Player', hue='Role', palette='Set2')
plt.title('Top 10 Players by Total Dismissals (Catches + Stumpings)')
plt.xlabel('Total Dismissals')
plt.tight_layout()
plt.show()
"""))

# Section 12
cells.append(nbf.v4.new_markdown_cell("""---
## 12. Player Role Distribution
Analyzing the squad balance and distribution across roles in the dataset.
"""))

cells.append(nbf.v4.new_code_cell("""role_counts = df['Role'].value_counts()

plt.figure(figsize=(7, 7))
plt.pie(
    role_counts,
    labels=role_counts.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=['#0d6e38', '#16a34a', '#38bdf8', '#fbbf24']
)
plt.title('Player Squad Role Distribution')
plt.tight_layout()
plt.show()
"""))

# Section 13
cells.append(nbf.v4.new_markdown_cell("""---
## 13. Age & Experience Analysis
Examining the age spectrum to identify young emerging prospects vs experienced veterans.
"""))

cells.append(nbf.v4.new_code_cell("""plt.figure(figsize=(10, 5))
sns.histplot(data=df, x='Age', bins=12, kde=True, color='#0d6e38')
plt.title('Age Distribution of Cricket Players')
plt.xlabel('Age (Years)')
plt.ylabel('Player Count')
plt.tight_layout()
plt.show()

# Experience (Matches) vs Batting Impact by Age Bracket
df['Age_Group'] = pd.cut(df['Age'], bins=[18, 25, 30, 35, 60], labels=['<25 (Emerging)', '25-30 (Prime)', '31-35 (Experienced)', '35+ (Veteran)'])
print("Average Metrics by Age Bracket:")
display(df.groupby('Age_Group', observed=True)[['Matches', 'Runs', 'Wickets', 'Batting_Impact', 'Bowling_Impact']].mean().round(2))
"""))

# Section 14
cells.append(nbf.v4.new_markdown_cell("""---
## 14. Graphs & Visualizations: Correlation Matrix
Examining cross-correlations between cricket performance metrics.
"""))

cells.append(nbf.v4.new_code_cell("""corr_cols = ['Age', 'Matches', 'Runs', 'Batting_Average', 'Strike_Rate', 'Wickets', 'Economy_Rate', 'Milestones_Total', 'Dismissals_Total']
corr_matrix = df[corr_cols].corr()

plt.figure(figsize=(9, 7))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', cbar=True, square=True)
plt.title('Correlation Matrix of Cricket Performance Metrics')
plt.tight_layout()
plt.show()
"""))

# Section 15
cells.append(nbf.v4.new_markdown_cell("""---
## 15. Player Comparison Matrix
Head-to-head comparison function enabling scouts to compare any two players across standard cricket metrics.
"""))

cells.append(nbf.v4.new_code_cell("""def compare_players(df, p1_name, p2_name):
    p1 = df[df['Player'].str.lower() == p1_name.lower()]
    p2 = df[df['Player'].str.lower() == p2_name.lower()]
    
    if p1.empty or p2.empty:
        print(f"Error: Could not locate one of the players ('{p1_name}' or '{p2_name}').")
        return
        
    metrics = ['Matches', 'Runs', 'Batting_Average', 'Strike_Rate', 'Centuries', 'Wickets', 'Economy_Rate', 'Catches']
    comp_df = pd.DataFrame({
        'Metric': metrics,
        p1.iloc[0]['Player']: [p1.iloc[0][m] for m in metrics],
        p2.iloc[0]['Player']: [p2.iloc[0][m] for m in metrics]
    })
    return comp_df

# Example Head-to-Head: Virat Kohli vs Steve Smith
display(compare_players(df, "Virat Kohli", "Steve Smith"))
"""))

# Section 16
cells.append(nbf.v4.new_markdown_cell("""---
## 16. Talent Scoring & Player Ranking
A transparent, configurable role-specific talent scoring formula (0 to 100 scale).

### Mathematical Formulas:
1. **Batter Talent Score (0-100):**
   $$Score_{Batter} = 0.35 \\times \\text{Norm}(Avg) + 0.30 \\times \\text{Norm}(SR) + 0.20 \\times \\text{Norm}(Runs) + 0.15 \\times \\text{Norm}(Milestones)$$
2. **Bowler Talent Score (0-100):**
   $$Score_{Bowler} = 0.30 \\times \\text{Norm}_{inv}(BowlAvg) + 0.30 \\times \\text{Norm}_{inv}(Econ) + 0.25 \\times \\text{Norm}(Wickets) + 0.15 \\times \\text{Norm}_{inv}(BowlSR)$$
3. **All-Rounder Talent Score (0-100):**
   $$Score_{AllRounder} = 0.50 \\times Score_{Batter} + 0.50 \\times Score_{Bowler}$$
4. **Wicketkeeper Talent Score (0-100):**
   $$Score_{WK} = 0.65 \\times Score_{Batter} + 0.35 \\times \\text{Norm}(Dismissals)$$
"""))

cells.append(nbf.v4.new_code_cell("""def min_max_norm(series, min_val=None, max_val=None):
    s_min = series.min() if min_val is None else min_val
    s_max = series.max() if max_val is None else max_val
    if s_max == s_min:
        return series * 0.0 + 50.0
    return ((series - s_min) / (s_max - s_min)) * 100.0

def inverse_norm(series, min_val=None, max_val=None):
    norm = min_max_norm(series, min_val, max_val)
    return 100.0 - norm

# Calculate Batting Talent Score
norm_bat_avg = min_max_norm(df['Batting_Average'].clip(upper=60))
norm_bat_sr = min_max_norm(df['Strike_Rate'].clip(upper=170))
norm_runs = min_max_norm(np.log1p(df['Runs']))
norm_milestones = min_max_norm(df['Milestones_Total'])

df['Batter_Talent_Score'] = (
    0.35 * norm_bat_avg +
    0.30 * norm_bat_sr +
    0.20 * norm_runs +
    0.15 * norm_milestones
).round(2)

# Calculate Bowling Talent Score for active bowlers
bowlers_mask = df['Wickets'] > 0
df['Bowler_Talent_Score'] = 0.0

if bowlers_mask.any():
    norm_bowl_avg = inverse_norm(df.loc[bowlers_mask, 'Bowling_Average'].clip(15, 60))
    norm_econ = inverse_norm(df.loc[bowlers_mask, 'Economy_Rate'].clip(3.5, 9.5))
    norm_wkts = min_max_norm(np.log1p(df.loc[bowlers_mask, 'Wickets']))
    norm_bowl_sr = inverse_norm(df.loc[bowlers_mask, 'Bowling_Strike_Rate'].clip(15, 60))
    
    df.loc[bowlers_mask, 'Bowler_Talent_Score'] = (
        0.30 * norm_bowl_avg +
        0.30 * norm_econ +
        0.25 * norm_wkts +
        0.15 * norm_bowl_sr
    ).round(2)

# Calculate All-Rounder and Wicketkeeper composite scores
norm_dismissals = min_max_norm(df['Dismissals_Total'])

df['Composite_Talent_Score'] = 0.0
for idx, r in df.iterrows():
    role = r['Role']
    if role == 'Batter':
        df.at[idx, 'Composite_Talent_Score'] = r['Batter_Talent_Score']
    elif role == 'Bowler':
        df.at[idx, 'Composite_Talent_Score'] = r['Bowler_Talent_Score']
    elif role == 'All-rounder':
        df.at[idx, 'Composite_Talent_Score'] = round(0.50 * r['Batter_Talent_Score'] + 0.50 * r['Bowler_Talent_Score'], 2)
    elif role == 'Wicketkeeper':
        df.at[idx, 'Composite_Talent_Score'] = round(0.65 * r['Batter_Talent_Score'] + 0.35 * norm_dismissals.iloc[idx], 2)

# Assign Talent Tier
def assign_tier(score):
    if score >= 75:
        return 'Tier 1 - Elite Grade'
    elif score >= 55:
        return 'Tier 2 - High Impact'
    elif score >= 40:
        return 'Tier 3 - Reliable Squad'
    else:
        return 'Tier 4 - Emerging Prospect'

df['Talent_Tier'] = df['Composite_Talent_Score'].apply(assign_tier)

print("Top 5 Batters by Talent Score:")
display(df[df['Role'] == 'Batter'][['Player', 'Country', 'Runs', 'Batting_Average', 'Strike_Rate', 'Batter_Talent_Score', 'Talent_Tier']].sort_values(by='Batter_Talent_Score', ascending=False).head(5))

print("\\nTop 5 Bowlers by Talent Score:")
display(df[df['Role'] == 'Bowler'][['Player', 'Country', 'Wickets', 'Economy_Rate', 'Bowling_Average', 'Bowler_Talent_Score', 'Talent_Tier']].sort_values(by='Bowler_Talent_Score', ascending=False).head(5))

print("\\nTop 5 All-Rounders by Talent Score:")
display(df[df['Role'] == 'All-rounder'][['Player', 'Country', 'Runs', 'Wickets', 'Composite_Talent_Score', 'Talent_Tier']].sort_values(by='Composite_Talent_Score', ascending=False).head(5))
"""))

# Section 17
cells.append(nbf.v4.new_markdown_cell("""---
## 17. Findings & Conclusion

### Key Insights:
1. **De-coupling Volume from Impact:** While legends like Sachin Tendulkar or Wasim Akram possess historic volume, modern T20/ODI scout requirements prioritize high strike rates (>135 for batters) and stingy economy rates (<6.5 for bowlers).
2. **Role-Specific Evaluation:** Standardizing metrics separately by role prevents misleading comparisons (e.g. comparing a tailend bowler's batting average against a top-order batter).
3. **Talent Scoring Transparency:** The multi-factor scoring model allows franchise analysts to tweak weighting coefficients based on whether they are drafting for Test resilience or T20 aggression.

### Capstone Viva Notes:
- **Data Integrity:** We handled missing values through role-informed sentinels rather than indiscriminate row dropping.
- **Outlier Preservation:** Extreme records (e.g. 264 runs or 800+ wickets) were preserved as true domain representations.
- **Next Steps:** Integrate with Flask REST API and React UI for real-time scouting exploration and shortlist management.
"""))

nb['cells'] = cells

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Successfully created Jupyter Notebook at: {notebook_path}")
print(f"Total notebook cells created: {len(cells)}")
