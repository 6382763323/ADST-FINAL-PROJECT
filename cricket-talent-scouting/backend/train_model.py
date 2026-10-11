"""
Cricket Talent Scouting & Analysis System
Module: backend/train_model.py

Purpose:
Trains a Scikit-learn Machine Learning classifier to predict talent tier / scouting category
based on multi-dimensional cricket metrics.
Evaluates model with cross-validation, precision, recall, and F1-score, and persists
the trained model pipeline to models/talent_classifier.joblib with metadata.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from sklearn.pipeline import Pipeline

def train_talent_model():
    """
    Train and save the cricket talent classification model.
    """
    print("\n" + "="*70)
    print("CRICKET TALENT SCOUTING - MACHINE LEARNING PIPELINE")
    print("="*70)
    
    # Locate paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, ".."))
    data_path = os.path.join(project_root, "dataset", "cleaned_cricket_players.csv")
    models_dir = os.path.join(project_root, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    model_output_path = os.path.join(models_dir, "talent_classifier.joblib")
    meta_output_path = os.path.join(models_dir, "model_metadata.json")
    
    if not os.path.exists(data_path):
        from clean_data import clean_cricket_data
        df = clean_cricket_data()
    else:
        df = pd.read_csv(data_path)
        
    print(f"Loaded {len(df)} player records for machine learning training.")
    
    # Define Ground-Truth Target Label: 'Scout_Category'
    # Based on verifiable domain performance criteria:
    # - Elite: Either top-tier batting (Avg >= 45 & Runs >= 3000) OR top-tier bowling (Wickets >= 250 & Econ <= 5.5) OR multi-faceted All-rounder
    # - High_Impact: Solid core performers (Avg >= 32 OR Wickets >= 80)
    # - Developing: Emerging prospects / developing tier
    
    def assign_scout_label(row):
        runs = row['Runs']
        avg = row['Batting_Average']
        sr = row['Strike_Rate']
        wkts = row['Wickets']
        econ = row['Economy_Rate']
        
        # Elite conditions
        if (avg >= 44.0 and runs >= 2500) or (wkts >= 250 and 0 < econ <= 5.5) or (runs >= 2000 and wkts >= 100):
            return "Elite"
        # High Impact conditions
        elif (avg >= 30.0 and runs >= 600) or (wkts >= 40 and 0 < econ <= 7.0) or (sr >= 130 and runs >= 400):
            return "High_Impact"
        else:
            return "Developing"
            
    df['Scout_Category'] = df.apply(assign_scout_label, axis=1)
    
    print("\nTarget Label Distribution:")
    label_counts = df['Scout_Category'].value_counts()
    print(label_counts)
    
    # Feature Selection (Numerical Performance Metrics)
    feature_cols = [
        'Matches', 'Innings', 'Runs', 'Highest_Score', 'Batting_Average',
        'Strike_Rate', 'Centuries', 'Fifties', 'Wickets', 'Bowling_Average',
        'Economy_Rate', 'Bowling_Strike_Rate', 'Catches', 'Stumpings'
    ]
    
    X = df[feature_cols].copy()
    y = df['Scout_Category'].copy()
    
    # Train / Test Split with Stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )
    
    print(f"\nTraining set size: {len(X_train)} samples")
    print(f"Testing set size: {len(X_test)} samples")
    
    # Build Scikit-learn Pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(
            n_estimators=100,
            max_depth=6,
            min_samples_split=4,
            random_state=42
        ))
    ])
    
    # Train Model
    pipeline.fit(X_train, y_train)
    
    # Cross Validation
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=4, scoring='accuracy')
    print(f"\n4-Fold Cross-Validation Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    # Evaluate on Unseen Test Split
    y_pred = pipeline.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    test_f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"\nTest Accuracy: {test_accuracy:.4f}")
    print(f"Weighted F1-Score: {test_f1:.4f}")
    
    print("\nDetailed Classification Report:")
    report_dict = classification_report(y_test, y_pred, output_dict=True)
    print(classification_report(y_test, y_pred))
    
    print("\nConfusion Matrix:")
    labels = sorted(list(y.unique()))
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    cm_df = pd.DataFrame(cm, index=[f"Actual_{l}" for l in labels], columns=[f"Pred_{l}" for l in labels])
    print(cm_df)
    
    # Extract Feature Importances
    rf_model = pipeline.named_steps['classifier']
    importances = rf_model.feature_importances_
    feat_imp = sorted(zip(feature_cols, importances), key=lambda x: x[1], reverse=True)
    
    print("\nTop Feature Importances:")
    for feat, imp in feat_imp[:6]:
        print(f" - {feat:20s}: {imp:.4f}")
        
    # Persist Trained Model Pipeline
    joblib.dump(pipeline, model_output_path)
    print(f"\nModel pipeline successfully saved to: {model_output_path}")
    
    # Persist Metadata & Limitations
    metadata = {
        "model_type": "RandomForestClassifier with StandardScaler Pipeline",
        "n_estimators": 100,
        "features": feature_cols,
        "classes": labels,
        "metrics": {
            "cv_accuracy_mean": round(float(cv_scores.mean()), 4),
            "cv_accuracy_std": round(float(cv_scores.std()), 4),
            "test_accuracy": round(float(test_accuracy), 4),
            "weighted_f1_score": round(float(test_f1), 4),
            "detailed_report": report_dict
        },
        "feature_importances": {feat: round(float(imp), 4) for feat, imp in feat_imp},
        "limitations": [
            "Historical stats do not capture match conditions, pitch behavior, or atmospheric factors.",
            "Aggregate metrics aggregate across formats (Test/ODI/T20) unless segregated.",
            "Player form and recent injury status are dynamic and cannot be guaranteed by static career numbers.",
            "Statistical classification provides a scouting guide, not an absolute guarantee of future match outcomes."
        ]
    }
    
    with open(meta_output_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        
    print(f"Model metadata & limitations saved to: {meta_output_path}")
    print("="*70 + "\n")
    
    return pipeline, metadata

if __name__ == "__main__":
    train_talent_model()
