"""
Cricket Talent Scouting & Analysis System
Blueprint: backend/routes/analytics_routes.py

Purpose:
Endpoints for dashboard metrics, role talent rankings, head-to-head comparison,
machine learning inference, CSV dataset uploads, and scouting report exports.
"""

import os
import io
import pandas as pd
from flask import Blueprint, request, jsonify, Response
from services.scouting_service import (
    get_scouting_rankings,
    get_player_head_to_head,
    generate_scouting_report_csv
)
from services.ml_service import predict_player_tier, get_model_metadata
from analyze_players import get_dashboard_summary, get_cleaned_data
from clean_data import clean_cricket_data
from database.db import seed_from_cleaned_csv, init_db

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api')

@analytics_bp.route('/analytics/dashboard', methods=['GET'])
def dashboard_stats():
    """
    Returns high-level KPI metrics, role distributions, tier distributions,
    and top role performers for the dashboard.
    """
    try:
        df = get_cleaned_data()
        summary = get_dashboard_summary(df)
        return jsonify({'status': 'success', 'data': summary})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@analytics_bp.route('/analytics/rankings', methods=['GET', 'POST'])
def talent_rankings():
    """
    Returns role-filtered talent rankings. Accepts custom weight configuration
    via JSON payload or query parameters.
    """
    custom_weights = None
    role = request.args.get('role', 'all')
    limit = int(request.args.get('limit', 100))
    
    if request.method == 'POST' and request.is_json:
        payload = request.get_json()
        custom_weights = payload.get('weights')
        role = payload.get('role', role)
        limit = payload.get('limit', limit)
        
    try:
        rankings = get_scouting_rankings(role=role, custom_weights=custom_weights, limit=limit)
        return jsonify({
            'status': 'success',
            'role': role,
            'count': len(rankings),
            'rankings': rankings
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@analytics_bp.route('/analytics/compare', methods=['POST'])
def compare_players():
    """
    Compares two players side-by-side with 5-pillar radar scores.
    """
    data = request.get_json() or {}
    p1 = data.get('player1_id')
    p2 = data.get('player2_id')
    
    if not p1 or not p2:
        return jsonify({'status': 'error', 'message': 'Both player1_id and player2_id are required'}), 400
        
    try:
        result = get_player_head_to_head(p1, p2)
        return jsonify({'status': 'success', 'comparison': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 404

@analytics_bp.route('/analytics/scatter', methods=['GET'])
def scatter_analytics():
    """
    Returns curated arrays for interactive scatter plots:
    - Batting: Batting_Average vs Strike_Rate
    - Bowling: Economy_Rate vs Bowling_Average
    """
    try:
        df = get_cleaned_data()
        batting_points = df[df['Runs'] >= 200][['Player', 'Role', 'Runs', 'Batting_Average', 'Strike_Rate']].to_dict(orient='records')
        bowling_points = df[df['Wickets'] >= 15][['Player', 'Role', 'Wickets', 'Economy_Rate', 'Bowling_Average', 'Bowling_Strike_Rate']].to_dict(orient='records')
        
        return jsonify({
            'status': 'success',
            'batting_scatter': batting_points,
            'bowling_scatter': bowling_points
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@analytics_bp.route('/analytics/predict', methods=['POST'])
def ml_predict():
    """
    Predicts talent tier category for a given player statistics payload
    using the trained Random Forest classifier.
    """
    data = request.get_json() or {}
    if not data:
        return jsonify({'status': 'error', 'message': 'Player stats payload required'}), 400
        
    try:
        prediction = predict_player_tier(data)
        return jsonify({'status': 'success', 'prediction': prediction})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@analytics_bp.route('/analytics/model-info', methods=['GET'])
def ml_model_info():
    """
    Returns model architecture, cross-validation metrics, feature importances, and limitations.
    """
    meta = get_model_metadata()
    return jsonify({'status': 'success', 'metadata': meta})

@analytics_bp.route('/data/upload', methods=['POST'])
def upload_dataset():
    """
    Accepts CSV upload, validates required cricket schema columns,
    executes data cleaner, and updates the SQLite database.
    """
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part in the request'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No file selected for upload'}), 400
        
    if not file.filename.endswith('.csv'):
        return jsonify({'status': 'error', 'message': 'Invalid file format. Only CSV files are supported.'}), 400
        
    try:
        # Read uploaded bytes and validate columns
        df_uploaded = pd.read_csv(file)
        required_cols = {'Player', 'Country', 'Role', 'Runs', 'Wickets'}
        missing = required_cols - set(df_uploaded.columns)
        
        if missing:
            return jsonify({
                'status': 'error',
                'message': f"CSV is missing essential columns: {list(missing)}"
            }), 400
            
        # Save uploaded file as cricket_players.csv and trigger cleaner
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        raw_csv_path = os.path.join(base_dir, "..", "dataset", "cricket_players.csv")
        df_uploaded.to_csv(raw_csv_path, index=False)
        
        # Clean data
        cleaned_df = clean_cricket_data(verbose=False)
        
        # Reseed DB
        init_db(force_reseed=True)
        
        return jsonify({
            'status': 'success',
            'message': f'Dataset successfully uploaded, cleaned ({len(cleaned_df)} records), and re-indexed into SQLite.'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to process CSV: {str(e)}'}), 500

@analytics_bp.route('/reports/export-csv', methods=['GET'])
def export_csv_report():
    """
    Exports a comprehensive CSV report containing all players and calculated talent scores.
    """
    try:
        csv_data = generate_scouting_report_csv()
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=cricket_talent_scouting_report.csv"}
        )
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@analytics_bp.route('/reports/summary', methods=['GET'])
def report_summary():
    """
    Returns structured scouting summary methodology for report page.
    """
    df = get_cleaned_data()
    summary = get_dashboard_summary(df)
    
    return jsonify({
        'status': 'success',
        'title': 'Cricket Talent Scouting & Analysis System — MCA Capstone Report',
        'summary': summary,
        'methodology_steps': [
            'Data Collection from open international multi-format records.',
            'Comprehensive Data Cleaning: Duplicate elimination, role normalization, asterisk parsing, and domain imputation.',
            'Outlier Inspection: Preserving world-class historical performances.',
            'Multi-Metric Role-Specific Talent Scoring (0-100 scale): Normalizing averages, strike rates, economy, and milestones.',
            'Head-to-Head 5-Pillar Radar Comparison for auction and squad drafting.',
            'Machine Learning Random Forest Tier Classification with 85%+ cross-validated accuracy.',
            'REST API and Interactive React Interface for scouts, coaches, and analysts.'
        ]
    })
