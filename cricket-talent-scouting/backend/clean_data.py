"""
Cricket Talent Scouting & Analysis System
Script: backend/clean_data.py

Purpose:
Loads the raw cricket player statistics dataset, inspects data quality,
handles missing values, removes duplicates, cleans formatting inconsistencies,
detects outliers without erroneously removing elite records, and outputs
a clean, validated dataset for analysis, ML modeling, and API consumption.
"""

import os
import sys
import numpy as np
import pandas as pd

def get_dataset_paths():
    """
    Dynamically locate the dataset paths whether executed from
    the root directory or from inside the backend/ folder.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    
    raw_csv = os.path.join(project_root, "dataset", "cricket_players.csv")
    cleaned_csv = os.path.join(project_root, "dataset", "cleaned_cricket_players.csv")
    
    return raw_csv, cleaned_csv

def load_and_inspect_raw(raw_path):
    """
    Step 1: Load raw dataset and display shape, columns, first 5 rows, and dtypes.
    """
    print("\n" + "="*70)
    print("STEP 1: LOADING & INSPECTING RAW DATASET")
    print("="*70)
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw dataset not found at: {raw_path}")
        
    df = pd.read_csv(raw_path)
    print(f"Raw Dataset File: {raw_path}")
    print(f"Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\nColumn Names:")
    for col in df.columns:
        print(f" - {col}")
        
    print("\nFirst 5 Rows:")
    print(df.head())
    
    print("\nData Types:")
    print(df.dtypes)
    return df

def analyze_missing_and_duplicates(df):
    """
    Step 2: Inspect missing values and duplicate records.
    """
    print("\n" + "="*70)
    print("STEP 2: MISSING VALUES & DUPLICATES AUDIT")
    print("="*70)
    
    # Duplicate check
    duplicate_count = df.duplicated(subset=['Player_ID']).sum()
    print(f"Duplicate Player_ID records identified: {duplicate_count}")
    
    # Missing values audit
    missing_summary = df.isnull().sum()
    print("\nMissing Values Count Per Column:")
    print(missing_summary[missing_summary > 0] if missing_summary.sum() > 0 else "No NaN values detected.")
    
    return duplicate_count

def clean_cricket_data(raw_path=None, save_path=None, verbose=True):
    """
    Main data cleaning pipeline.
    Handles data anomalies, type conversions, missing values, and formatting.
    """
    default_raw, default_clean = get_dataset_paths()
    raw_path = raw_path or default_raw
    save_path = save_path or default_clean
    
    if verbose:
        print("\n" + "#"*70)
        print("CRICKET DATA CLEANING PIPELINE INITIALIZED")
        print("#"*70)
        
    df = load_and_inspect_raw(raw_path)
    initial_rows = len(df)
    initial_missing = df.isnull().sum().sum()
    
    # Step 2: Audit
    analyze_missing_and_duplicates(df)
    
    # Step 3: Handle Duplicates
    if verbose:
        print("\n" + "="*70)
        print("STEP 3: HANDLING DUPLICATES")
        print("="*70)
    df = df.drop_duplicates(subset=['Player_ID'], keep='first')
    if verbose:
        print(f"Rows after dropping duplicates: {len(df)} (Dropped {initial_rows - len(df)} row(s))")

    # Step 4: String Normalization and Whitespace Stripping
    if verbose:
        print("\n" + "="*70)
        print("STEP 4: CATEGORICAL NORMALIZATION")
        print("="*70)
    
    # Normalize string columns
    str_cols = ['Player', 'Country', 'Role', 'Batting_Style', 'Bowling_Style']
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            
    # Normalize Role values
    role_mapping = {
        'BATTER': 'Batter',
        'Batter': 'Batter',
        'Batsman': 'Batter',
        'Bowler': 'Bowler',
        'BOWLER': 'Bowler',
        'All-Rounder': 'All-rounder',
        'all-rounder': 'All-rounder',
        'All Rounder': 'All-rounder',
        'all rounder': 'All-rounder',
        'All-rounder': 'All-rounder',
        'Wicketkeeper': 'Wicketkeeper',
        'Wicket-Keeper': 'Wicketkeeper',
        'Wicket Keeper': 'Wicketkeeper',
        'WK': 'Wicketkeeper'
    }
    df['Role'] = df['Role'].map(lambda x: role_mapping.get(x, x.title()))
    if verbose:
        print("Normalized Role Distribution:")
        print(df['Role'].value_counts())

    # Step 5: Clean Highest_Score and preserve not-out information
    if verbose:
        print("\n" + "="*70)
        print("STEP 5: HIGHEST SCORE CLEANING & NOT-OUT EXTRACTION")
        print("="*70)
        
    df['Highest_Score_Clean'] = df['Highest_Score'].astype(str).str.replace('*', '', regex=False).str.strip()
    df['Highest_Score_Clean'] = pd.to_numeric(df['Highest_Score_Clean'], errors='coerce').fillna(0).astype(int)
    df['Is_Highest_Score_NotOut'] = df['Highest_Score'].astype(str).str.contains(r'\*').astype(int)
    df['Highest_Score'] = df['Highest_Score_Clean']
    df.drop(columns=['Highest_Score_Clean'], inplace=True)
    if verbose:
        print("Sample parsed Highest Scores:")
        print(df[['Player', 'Highest_Score', 'Is_Highest_Score_NotOut']].head())

    # Step 6: Numerical Type Conversions and Missing Value Handling
    if verbose:
        print("\n" + "="*70)
        print("STEP 6: NUMERICAL VALIDATION & MISSING VALUE IMPUTATION")
        print("="*70)
        
    numeric_int_cols = ['Age', 'Matches', 'Innings', 'Runs', 'Centuries', 'Fifties', 'Wickets', 'Catches', 'Stumpings']
    for col in numeric_int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    numeric_float_cols = ['Batting_Average', 'Strike_Rate', 'Bowling_Average', 'Economy_Rate', 'Bowling_Strike_Rate']
    for col in numeric_float_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Domain-specific imputation:
    # 1. Pure batters who do not bowl will have NaN for bowling metrics. In cricket analytics,
    # setting economy or bowling average to 0.0 or a neutral sentinel indicates 'Not a regular bowler'.
    # For computation, we keep Bowling_Average as 0.0 and Economy_Rate as 0.0 with Wickets = 0.
    df['Bowling_Average'] = df['Bowling_Average'].fillna(0.0).round(2)
    df['Economy_Rate'] = df['Economy_Rate'].fillna(0.0).round(2)
    df['Bowling_Strike_Rate'] = df['Bowling_Strike_Rate'].fillna(0.0).round(2)

    # 2. Pure bowlers who did not bat or have missing batting averages
    # If a bowler's batting average is NaN, impute with 0.0 or calculated Runs / Innings
    df['Batting_Average'] = df.apply(
        lambda row: round(row['Runs'] / max(row['Innings'], 1), 2) 
        if pd.isna(row['Batting_Average']) or row['Batting_Average'] == 0 
        else row['Batting_Average'],
        axis=1
    ).round(2)
    
    # Missing strike rates: if 0 or NaN, default to standard lower-bound estimate
    df['Strike_Rate'] = df['Strike_Rate'].fillna(75.0).round(2)

    # Clean Best_Bowling: replace empty strings or NaN with '-'
    df['Best_Bowling'] = df['Best_Bowling'].fillna('-').astype(str).str.strip()
    df.loc[df['Best_Bowling'] == '', 'Best_Bowling'] = '-'

    # Step 7: Engineered Analytical Indicators
    df['Milestones_Total'] = df['Centuries'] + df['Fifties']
    df['Dismissals_Total'] = df['Catches'] + df['Stumpings']
    
    # Batting Impact metric: (Runs / Matches) * (Strike_Rate / 100)
    df['Batting_Impact'] = ((df['Runs'] / df['Matches'].clip(lower=1)) * (df['Strike_Rate'] / 100.0)).round(2)
    
    # Bowling Impact metric: (Wickets / Matches) * (10 / max(Economy, 3.0)) for active bowlers
    df['Bowling_Impact'] = df.apply(
        lambda r: round((r['Wickets'] / max(r['Matches'], 1)) * (10.0 / max(r['Economy_Rate'], 3.0)), 2)
        if r['Wickets'] > 0 and r['Economy_Rate'] > 0 else 0.0,
        axis=1
    )

    # Step 8: Outlier Inspection (Without deleting genuine stellar records!)
    if verbose:
        print("\n" + "="*70)
        print("STEP 7: OUTLIER AUDIT (INSPECTION WITHOUT DELETION)")
        print("="*70)
        print("Note: In elite cricket scouting, extreme scores (e.g. 264 runs, 800+ wickets)")
        print("represent world-class mastery rather than data corruption. We audit them here.")
        
        for metric in ['Runs', 'Wickets', 'Batting_Average', 'Strike_Rate']:
            q25 = df[metric].quantile(0.25)
            q75 = df[metric].quantile(0.75)
            iqr = q75 - q25
            upper_bound = q75 + 1.5 * iqr
            outliers = df[df[metric] > upper_bound][['Player', 'Role', metric]]
            print(f"\nStatistical Outliers in {metric} (Upper threshold = {upper_bound:.2f}):")
            print(f"Count: {len(outliers)}")
            if not outliers.empty:
                print(outliers.head(3).to_string(index=False))

    # Step 9: Save Cleaned Dataset
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    
    # Step 10: Before and After Statistics
    if verbose:
        print("\n" + "="*70)
        print("BEFORE & AFTER CLEANING SUMMARY")
        print("="*70)
        print(f"Total rows before: {initial_rows}  -->  After: {len(df)}")
        print(f"Total missing cells before: {initial_missing}  -->  After: {df.isnull().sum().sum()}")
        print(f"Cleaned dataset successfully saved to:\n  {save_path}")
        print("="*70 + "\n")
        
    return df

if __name__ == "__main__":
    clean_cricket_data()
