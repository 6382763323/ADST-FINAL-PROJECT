"""
Cricket Talent Scouting & Analysis System
Application Entry Point: backend/app.py

Purpose:
Main Flask application runner. Configures CORS, registers API blueprints,
handles global errors, and serves API endpoints for the React frontend.
"""

import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS

# Ensure backend root is in Python sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.db import init_db
from routes.player_routes import player_bp
from routes.analytics_routes import analytics_bp

def create_app():
    """
    Application Factory Pattern for Flask.
    """
    app = Flask(__name__)
    
    # Configure CORS to allow React Vite dev server (typically port 5173 / localhost)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    app.register_blueprint(player_bp)
    app.register_blueprint(analytics_bp)
    
    # Base route & Health check
    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            "project": "Cricket Talent Scouting & Analysis System",
            "version": "1.0.0",
            "status": "online",
            "api_documentation": "/api/docs",
            "endpoints": {
                "dashboard": "/api/analytics/dashboard",
                "players": "/api/players",
                "rankings": "/api/analytics/rankings",
                "compare": "/api/analytics/compare",
                "ml_predict": "/api/analytics/predict",
                "model_info": "/api/analytics/model-info",
                "export_csv": "/api/reports/export-csv"
            }
        })
        
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "healthy", "service": "cricket-talent-scouting-backend"})
        
    # Error Handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"status": "error", "message": "The requested resource was not found"}), 404
        
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"status": "error", "message": "An internal server error occurred"}), 500
        
    # Ensure database is initialized
    try:
        init_db()
    except Exception as err:
        print(f"Warning during DB init: {err}")
        
    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n==================================================================")
    print(f"[Cricket Talent Scouting] Flask Backend Running on http://127.0.0.1:{port}")
    print(f"==================================================================\n")
    app.run(host="0.0.0.0", port=port, debug=False)
