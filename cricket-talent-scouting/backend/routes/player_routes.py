"""
Cricket Talent Scouting & Analysis System
Blueprint: backend/routes/player_routes.py

Purpose:
CRUD endpoints for player directory, performance stats, and scouting shortlists.
"""

from flask import Blueprint, request, jsonify
from database.db import (
    get_all_players,
    get_player_by_id,
    insert_or_update_player,
    delete_player,
    get_shortlist,
    add_to_shortlist,
    remove_from_shortlist
)

player_bp = Blueprint('players', __name__, url_prefix='/api')

@player_bp.route('/players', methods=['GET'])
def list_players():
    """
    List players with search, role filter, country filter, and sorting.
    """
    search = request.args.get('search', '').strip() or None
    role = request.args.get('role', 'all').strip()
    country = request.args.get('country', 'all').strip()
    sort_by = request.args.get('sort_by', 'runs').strip()
    order = request.args.get('order', 'desc').strip()
    limit = int(request.args.get('limit', 150))
    
    players = get_all_players(
        search=search,
        role=role,
        country=country,
        sort_by=sort_by,
        order=order,
        limit=limit
    )
    return jsonify({
        'status': 'success',
        'count': len(players),
        'players': players
    })

@player_bp.route('/players/<player_id>', methods=['GET'])
def get_player(player_id):
    """
    Get individual player full profile.
    """
    player = get_player_by_id(player_id)
    if not player:
        return jsonify({'status': 'error', 'message': f'Player {player_id} not found'}), 404
        
    return jsonify({'status': 'success', 'player': player})

@player_bp.route('/players', methods=['POST'])
def add_player():
    """
    Add a new player record.
    """
    data = request.get_json() or {}
    
    # Validation
    if not data.get('name') or not data.get('country') or not data.get('role'):
        return jsonify({'status': 'error', 'message': 'Missing required fields: name, country, role'}), 400
        
    # Auto-generate player_id if not supplied
    if not data.get('player_id'):
        import time
        data['player_id'] = f"CRIC_NEW_{int(time.time() * 1000) % 100000}"
        
    try:
        saved_player = insert_or_update_player(data)
        return jsonify({
            'status': 'success',
            'message': 'Player created successfully',
            'player': saved_player
        }), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@player_bp.route('/players/<player_id>', methods=['PUT'])
def update_player(player_id):
    """
    Update an existing player record.
    """
    data = request.get_json() or {}
    existing = get_player_by_id(player_id)
    if not existing:
        return jsonify({'status': 'error', 'message': f'Player {player_id} not found'}), 404
        
    data['player_id'] = player_id
    try:
        updated = insert_or_update_player(data)
        return jsonify({
            'status': 'success',
            'message': 'Player updated successfully',
            'player': updated
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@player_bp.route('/players/<player_id>', methods=['DELETE'])
def remove_player(player_id):
    """
    Delete a player record.
    """
    success = delete_player(player_id)
    if not success:
        return jsonify({'status': 'error', 'message': f'Player {player_id} not found or could not be deleted'}), 404
        
    return jsonify({'status': 'success', 'message': f'Player {player_id} deleted successfully'})

# Shortlist endpoints
@player_bp.route('/shortlist', methods=['GET'])
def list_shortlist():
    shortlist = get_shortlist()
    return jsonify({'status': 'success', 'count': len(shortlist), 'shortlist': shortlist})

@player_bp.route('/shortlist', methods=['POST'])
def add_shortlist_item():
    data = request.get_json() or {}
    player_id = data.get('player_id')
    if not player_id:
        return jsonify({'status': 'error', 'message': 'player_id is required'}), 400
        
    target_role = data.get('target_role', 'Main Squad')
    priority = data.get('priority_tier', 'High')
    notes = data.get('scout_notes', '')
    
    item_id = add_to_shortlist(player_id, target_role, priority, notes)
    return jsonify({'status': 'success', 'message': 'Player added to scouting shortlist', 'id': item_id}), 201

@player_bp.route('/shortlist/<shortlist_id>', methods=['DELETE'])
def remove_shortlist_item(shortlist_id):
    success = remove_from_shortlist(shortlist_id)
    if not success:
        return jsonify({'status': 'error', 'message': 'Item not found in shortlist'}), 404
    return jsonify({'status': 'success', 'message': 'Item removed from shortlist'})
