import React from 'react';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
  Tooltip
} from 'recharts';

export default function RadarChartComp({ p1Name, p1Radar, p2Name, p2Radar }) {
  if (!p1Radar) return null;

  // Format data for Recharts Radar
  const pillars = Object.keys(p1Radar);
  const data = pillars.map((pillar) => ({
    metric: pillar,
    [p1Name]: p1Radar[pillar],
    ...(p2Name && p2Radar ? { [p2Name]: p2Radar[pillar] } : {})
  }));

  return (
    <div style={{ width: '100%', height: 350 }}>
      <ResponsiveContainer>
        <RadarChart cx="50%" cy="50%" outerRadius="75%" data={data}>
          <PolarGrid stroke="#cbd5e1" />
          <PolarAngleAxis dataKey="metric" tick={{ fill: '#334155', fontSize: 12, fontWeight: 600 }} />
          <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#94a3b8" />
          <Radar
            name={p1Name}
            dataKey={p1Name}
            stroke="#16a34a"
            fill="#16a34a"
            fillOpacity={0.45}
          />
          {p2Name && p2Radar && (
            <Radar
              name={p2Name}
              dataKey={p2Name}
              stroke="#0284c7"
              fill="#0284c7"
              fillOpacity={0.4}
            />
          )}
          <Legend wrapperStyle={{ paddingTop: '10px' }} />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
