import React from 'react';
import { Search, SlidersHorizontal } from 'lucide-react';

export default function PlayerFilter({
  search,
  setSearch,
  role,
  setRole,
  country,
  setCountry,
  sortBy,
  setSortBy,
  order,
  setOrder,
  onReset
}) {
  const roles = ['all', 'Batter', 'Bowler', 'All-rounder', 'Wicketkeeper'];
  const countries = [
    'all', 'India', 'Australia', 'England', 'South Africa',
    'Pakistan', 'New Zealand', 'West Indies', 'Sri Lanka',
    'Afghanistan', 'Bangladesh', 'Zimbabwe'
  ];

  return (
    <div className="filter-bar">
      <div className="filter-group">
        <div style={{ position: 'relative' }}>
          <input
            type="text"
            className="search-input"
            placeholder="Search player, country..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <select
          className="select-control"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        >
          {roles.map((r) => (
            <option key={r} value={r}>
              {r === 'all' ? 'All Roles' : r}
            </option>
          ))}
        </select>

        <select
          className="select-control"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
        >
          {countries.map((c) => (
            <option key={c} value={c}>
              {c === 'all' ? 'All Countries' : c}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <SlidersHorizontal size={16} color="#64748b" />
          <span style={{ fontSize: '0.82rem', color: '#64748b' }}>Sort by:</span>
        </div>
        <select
          className="select-control"
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
        >
          <option value="runs">Runs</option>
          <option value="wickets">Wickets</option>
          <option value="batting_avg">Batting Average</option>
          <option value="strike_rate">Strike Rate</option>
          <option value="matches">Matches</option>
          <option value="name">Player Name</option>
        </select>

        <button
          className="btn btn-secondary btn-sm"
          onClick={() => setOrder(order === 'desc' ? 'asc' : 'desc')}
        >
          {order.toUpperCase()}
        </button>

        {onReset && (
          <button className="btn btn-secondary btn-sm" onClick={onReset}>
            Reset
          </button>
        )}
      </div>
    </div>
  );
}
