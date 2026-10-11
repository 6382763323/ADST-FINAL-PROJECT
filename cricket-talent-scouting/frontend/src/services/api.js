/**
 * Cricket Talent Scouting & Analysis System
 * Frontend API Service: src/services/api.js
 * 
 * Handles all HTTP communication with the Flask backend.
 */

const API_BASE = '/api';

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || `HTTP Error ${response.status}`);
    }
    return data;
  } catch (err) {
    console.error(`API Error on [${options.method || 'GET'} ${endpoint}]:`, err);
    throw err;
  }
}

export const api = {
  // Dashboard statistics
  getDashboard: () => request('/analytics/dashboard'),

  // Players
  getPlayers: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return request(`/players${query ? `?${query}` : ''}`);
  },

  getPlayerById: (playerId) => request(`/players/${encodeURIComponent(playerId)}`),

  createPlayer: (playerData) =>
    request('/players', {
      method: 'POST',
      body: JSON.stringify(playerData),
    }),

  updatePlayer: (playerId, playerData) =>
    request(`/players/${encodeURIComponent(playerId)}`, {
      method: 'PUT',
      body: JSON.stringify(playerData),
    }),

  deletePlayer: (playerId) =>
    request(`/players/${encodeURIComponent(playerId)}`, {
      method: 'DELETE',
    }),

  // Shortlist
  getShortlist: () => request('/shortlist'),
  addToShortlist: (data) =>
    request('/shortlist', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  removeFromShortlist: (id) =>
    request(`/shortlist/${id}`, {
      method: 'DELETE',
    }),

  // Talent Rankings & Scoring
  getRankings: (role = 'all', weights = null, limit = 50) => {
    if (weights) {
      return request('/analytics/rankings', {
        method: 'POST',
        body: JSON.stringify({ role, weights, limit }),
      });
    }
    return request(`/analytics/rankings?role=${encodeURIComponent(role)}&limit=${limit}`);
  },

  // Player Comparison
  comparePlayers: (player1Id, player2Id) =>
    request('/analytics/compare', {
      method: 'POST',
      body: JSON.stringify({ player1_id: player1Id, player2_id: player2Id }),
    }),

  // Scatter Analytics
  getScatterData: () => request('/analytics/scatter'),

  // Machine Learning
  predictTier: (playerStats) =>
    request('/analytics/predict', {
      method: 'POST',
      body: JSON.stringify(playerStats),
    }),

  getModelInfo: () => request('/analytics/model-info'),

  // Upload Dataset
  uploadCSV: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch(`${API_BASE}/data/upload`, {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || `Upload failed with status ${response.status}`);
    }
    return data;
  },

  // Reports
  getSummaryReport: () => request('/reports/summary'),
  getExportCsvUrl: () => `${API_BASE}/reports/export-csv`,
};
