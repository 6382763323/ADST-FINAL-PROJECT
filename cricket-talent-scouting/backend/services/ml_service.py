"""
Cricket Talent Scouting & Analysis System
Service: backend/services/ml_service.py

Purpose:
Loads the trained Random Forest classifier pipeline and model metadata.
Provides classification inference, class confidence probabilities,
and limitations explanations for players or scouting prospects.
"""

import os
import json
import joblib
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "talent_classifier.joblib")
META_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "model_metadata.json")

_model = None
_metadata = None

def get_loaded_model():
    """
    Lazy loads the machine learning model.
    """
    global _model
    if _model is None:
        if os.path.exists(MODEL_PATH):
            _model = joblib.load(MODEL_PATH)
        else:
            from train_model import train_talent_model
            _model, _ = train_talent_model()
    return _model

def get_model_metadata():
    """
    Loads saved model metadata and limitations.
    """
    global _metadata
    if _metadata is None:
        if os.path.exists(META_PATH):
            with open(META_PATH, "r", encoding="utf-8") as f:
                _metadata = json.load(f)
        else:
            _metadata = {
                "model_type": "RandomForestClassifier",
                "status": "Trained but metadata file missing"
            }
    return _metadata

def predict_player_tier(player_stats):
    """
    Takes a dictionary or pandas Series of player stats and predicts:
    - Predicted Talent Grade / Tier (Elite, High_Impact, Developing)
    - Class Probabilities
    """
    model = get_loaded_model()
    meta = get_model_metadata()
    features = meta.get('features', [
        'Matches', 'Innings', 'Runs', 'Highest_Score', 'Batting_Average',
        'Strike_Rate', 'Centuries', 'Fifties', 'Wickets', 'Bowling_Average',
        'Economy_Rate', 'Bowling_Strike_Rate', 'Catches', 'Stumpings'
    ])
    
    # Build dataframe for inference
    input_row = {}
    for feat in features:
        # Check both lower and upper case keys
        val = player_stats.get(feat, player_stats.get(feat.lower(), 0))
        try:
            input_row[feat] = float(val) if val is not None and val != '' else 0.0
        except (ValueError, TypeError):
            input_row[feat] = 0.0
            
    df_input = pd.DataFrame([input_row])
    pred_tier = model.predict(df_input)[0]
    
    # Predict probabilities if supported
    probs = {}
    if hasattr(model, "predict_proba"):
        prob_vals = model.predict_proba(df_input)[0]
        classes = model.classes_
        for cls_name, prob in zip(classes, prob_vals):
            probs[cls_name] = round(float(prob) * 100.0, 1)
            
    return {
        "predicted_tier": pred_tier,
        "probabilities": probs,
        "input_features": input_row,
        "disclaimer": "Machine learning prediction is a statistical decision support tool. It does not replace qualitative scouting assessment or guarantee future performance."
    }

if __name__ == "__main__":
    test_player = {
        'Matches': 100, 'Innings': 95, 'Runs': 4200, 'Highest_Score': 135,
        'Batting_Average': 46.5, 'Strike_Rate': 138.0, 'Centuries': 8, 'Fifties': 26,
        'Wickets': 5, 'Bowling_Average': 45.0, 'Economy_Rate': 7.2, 'Bowling_Strike_Rate': 38.0,
        'Catches': 45, 'Stumpings': 0
    }
    result = predict_player_tier(test_player)
    print("Test Player Prediction:", result)
