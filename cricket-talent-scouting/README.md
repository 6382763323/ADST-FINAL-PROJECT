# 🏏 Cricket Talent Scouting & Analysis System Using Data Analytics and Machine Learning

**MCA Capstone Project**  
*A full-stack, data-driven cricket analytics platform for transparent player evaluation, role-specific talent scouting, and machine learning tier classification.*

---

## 📌 Project Overview
In modern competitive cricket across multi-format international tours and premier franchise leagues (IPL, BBL, PSL, The Hundred), scouting and recruitment can no longer rely on gross career aggregates like total runs or total wickets. Total runs frequently reward top-order longevity while obscuring middle-order aggressive strike rates, efficiency, and clutch fielding contributions.

This project delivers:
1. **Automated Python Data Cleaning:** Identifies and resolves missing values, duplicates, and complex notation (e.g. `183*`), while preserving legitimate world-class outlier performances (e.g. Rohit Sharma's 264 or Muralitharan's 1300+ wickets).
2. **Comprehensive Jupyter EDA Notebook:** 17-section visual analysis spanning batting, bowling, fielding, age curves, and correlation matrices.
3. **Transparent Mathematical Talent Scoring:** Normalizes stats on a 0-100 scale using configurable weights tailored for T20, ODI, or Test scouting philosophies.
4. **Scikit-learn Machine Learning Classifier:** Predicts talent grade tiers with 85%+ cross-validation accuracy using a Random Forest pipeline.
5. **Robust SQLite Relational Database:** Structured tables with foreign keys and cascade rules for players, performances, shortlists, and scouting audit histories.
6. **Flask REST API:** Decoupled backend providing endpoints for CRUD, dynamic rankings, head-to-head comparison, CSV ingestion, and downloads.
7. **Modern React (Vite) Frontend:** 10 responsive pages styled in a cricket-themed emerald green, dark navy, and white palette featuring interactive Recharts (Radar, Bar, Pie, Scatter).

---

## 📂 Project Directory Structure

```
cricket-talent-scouting/
├── dataset/
│   ├── cricket_players.csv               # Raw cricket dataset
│   ├── cleaned_cricket_players.csv       # Cleaned, validated dataset
│   └── generate_dataset.py               # Dataset generation script
├── notebooks/
│   ├── cricket_analysis.ipynb            # Complete 17-section MCA analysis notebook
│   └── generate_notebook.py              # Notebook generator & validator script
├── models/
│   ├── .gitkeep
│   ├── talent_classifier.joblib          # Trained Random Forest Scikit-learn pipeline
│   └── model_metadata.json               # Model metrics, feature weights & limitations
├── backend/
│   ├── app.py                            # Flask application entry point with CORS
│   ├── clean_data.py                     # Pandas/NumPy data cleaning pipeline
│   ├── analyze_players.py                # Talent scoring & comparison engine
│   ├── train_model.py                    # Scikit-learn model training & evaluation
│   ├── requirements.txt                  # Python dependencies
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py                         # SQLite connection & CRUD operations
│   │   ├── schema.sql                    # SQL tables, indices, and foreign keys
│   │   └── cricket_scouting.db           # SQLite database file
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── player_routes.py              # Player CRUD & shortlist API endpoints
│   │   └── analytics_routes.py           # Dashboard, ranking, comparison, ML & upload routes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── scouting_service.py           # Business logic for rankings & report generation
│   │   └── ml_service.py                 # ML inference & probability service
│   └── tests/
│       ├── test_data_cleaning.py         # Unit tests for data cleaning pipeline
│       ├── test_talent_ranking.py        # Unit tests for talent scoring & normalizations
│       └── test_api.py                   # Integration tests for database & Flask endpoints
├── frontend/
│   ├── package.json                      # React, Vite, Recharts, Lucide-react dependencies
│   ├── vite.config.js                    # Vite configuration with API proxy to Flask
│   ├── index.html                        # Application HTML shell
│   └── src/
│       ├── main.jsx                      # React DOM mounting
│       ├── App.jsx                       # Application routing & page switcher
│       ├── index.css                     # Cricket-themed CSS design system
│       ├── components/
│       │   ├── Navbar.jsx                # Top header bar
│       │   ├── Sidebar.jsx               # Navigation drawer with cricket icons
│       │   ├── MetricCard.jsx            # KPI summary card
│       │   ├── RadarChartComp.jsx        # 5-Pillar radar chart (Recharts)
│       │   └── PlayerFilter.jsx          # Search, role filter & sorting controls
│       ├── pages/
│       │   ├── Dashboard.jsx             # KPI stats, top performers, role & tier charts
│       │   ├── PlayerManagement.jsx      # Add, edit, delete, and search player records
│       │   ├── PerformanceAnalysis.jsx   # Role breakdown (Batting, Bowling, Fielding)
│       │   ├── TalentScouting.jsx        # Interactive sliders & talent leaderboards
│       │   ├── PlayerComparison.jsx      # Head-to-head 5-pillar radar comparison
│       │   ├── PlayerProfile.jsx         # Career stats & ML tier prediction widget
│       │   ├── Analytics.jsx             # Efficiency frontiers & bubble scatter plots
│       │   ├── DataUpload.jsx            # CSV upload, validation & automated cleaning
│       │   ├── Reports.jsx               # Shortlist management & CSV export download
│       │   └── AboutMethodology.jsx      # MCA methodology, equations & Viva notes
│       ├── layouts/
│       │   └── MainLayout.jsx            # Responsive layout wrapper
│       └── services/
│           └── api.js                    # Fetch API client connected to Flask backend
├── reports/
│   └── scouting_methodology_report.md    # Detailed academic report & mathematical proofs
├── README.md                             # Exact setup & execution guide
├── .gitignore                            # Git ignore configuration
└── .env.example                          # Environment variables template
```

---

## 💻 Step-by-Step Instructions to Run on Windows

### Prerequisites
- **Python 3.10+** (Python 3.11, 3.12, 3.13, 3.14 verified)
- **Node.js v18+** and **npm**
- Shell: PowerShell or Command Prompt on Windows

---

### Step 1: Open Terminal in the Project Directory
Open PowerShell and navigate to the project directory:
```powershell
cd c:\Users\abhis\OneDrive\Desktop\ADSproject\cricket-talent-scouting
```

---

### Step 2: Install Python Backend Dependencies
Install the required Python libraries using pip:
```powershell
pip install -r backend/requirements.txt
```
*(Or install directly: `pip install flask flask-cors pandas numpy scikit-learn joblib matplotlib seaborn nbformat`)*

---

### Step 3: Verify Data Cleaning, ML Model, and Database
Run the cleaning script and verify the SQLite database:
```powershell
# 1. Run Data Cleaning Pipeline
python backend/clean_data.py

# 2. Initialize and Seed SQLite Database
python backend/database/db.py

# 3. Train the Machine Learning Classifier
python backend/train_model.py

# 4. Run Unit & Integration Tests
python -m unittest backend/tests/test_data_cleaning.py backend/tests/test_talent_ranking.py backend/tests/test_api.py
```
*(All 16 unit tests should report `OK`)*

---

### Step 4: Launch the Flask Backend Server
In your first PowerShell terminal, run:
```powershell
python backend/app.py
```
The Flask REST API will start on:  
👉 **`http://127.0.0.1:5000`**

Verify in your browser by visiting `http://127.0.0.1:5000/api/health` — it will return:
```json
{"service": "cricket-talent-scouting-backend", "status": "healthy"}
```

---

### Step 5: Install Frontend Dependencies and Launch React
Open a **second PowerShell terminal window**, navigate to `frontend`, install dependencies, and start Vite:
```powershell
cd c:\Users\abhis\OneDrive\Desktop\ADSproject\cricket-talent-scouting\frontend
npm install
npm run dev
```
The Vite development server will start on:  
👉 **`http://localhost:5173`**

Open your web browser and navigate to **`http://localhost:5173`** to access the complete application!

---

### Step 6: How to Open and Run the Jupyter Notebook
To inspect the data science analysis, charts, and visualizations in Jupyter:
```powershell
cd c:\Users\abhis\OneDrive\Desktop\ADSproject\cricket-talent-scouting
jupyter notebook notebooks/cricket_analysis.ipynb
```
Select **"Run All Cells"** from the Kernel menu to execute all 17 analysis sections.

---

## 🔬 Mathematical Talent Scoring Formulation

### 1. Batter Talent Score:
$$\text{Batter\_Score} = 0.35 \times \text{Norm}(\text{Avg}) + 0.30 \times \text{Norm}(\text{SR}) + 0.20 \times \text{Norm}(\ln(\text{Runs})) + 0.15 \times \text{Norm}(\text{Milestones})$$

### 2. Bowler Talent Score:
$$\text{Bowler\_Score} = 0.30 \times \text{InvNorm}(\text{BowlAvg}) + 0.30 \times \text{InvNorm}(\text{Econ}) + 0.25 \times \text{Norm}(\ln(\text{Wkts})) + 0.15 \times \text{InvNorm}(\text{BowlSR})$$

### 3. All-Rounder Composite Score:
$$\text{AllRounder\_Score} = 0.50 \times \text{Batter\_Score} + 0.50 \times \text{Bowler\_Score}$$

### 4. Wicketkeeper Composite Score:
$$\text{WK\_Score} = 0.65 \times \text{Batter\_Score} + 0.35 \times \text{Norm}(\text{Dismissals})$$

---

## 🎯 MCA Capstone Viva-Voce Questions & Answers

1. **Why not just rank players by total career runs or wickets?**
   *Total runs strongly reward longevity and batting positions 1-3. Modern scouting requires efficiency (strike rate >130 in T20, economy <6.5 in bowling). A middle-order finisher with fewer runs but a 160 strike rate is more valuable for specific tactical slots than a slower accumulator.*

2. **How did you handle missing values without distorting the cricket statistics?**
   *Missing bowling metrics for pure batters were imputed with domain sentinels (0.0) with documentation, because pure batters rarely bowl in professional matches. Indiscriminate deletion would have erroneously eliminated star batters like Babar Azam or Shubman Gill.*

3. **Did you delete statistical outliers like Rohit Sharma's 264 or Muralitharan's 1300+ wickets?**
   *No. In sports analytics, extreme records represent genuine world-class elite performances, not sensor defects. Removing them would distort talent benchmarks.*

4. **What are the limitations of this machine learning model?**
   *Career aggregates do not account for dynamic pitch conditions (spin vs seam), atmospheric weather/dew, opposition rankings, or current physical fitness. Machine learning acts as a quantitative decision-support tool, not an absolute guarantee of match outcomes.*
