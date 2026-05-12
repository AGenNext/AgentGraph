'use client';

import { useState } from 'react';

// Feature store item
interface Feature {
  id: string;
  name: string;
  description: string;
  type: 'vector' | 'scalar' | 'window' | 'derived';
  source: string;
  schema: string;
  updated: string;
  usedBy: number;
}

const mockFeatures: Feature[] = [
  { id: 'f1', name: 'user_embedding', description: 'User behavior embedding (384d)', type: 'vector', source: 'AWS Bedrock', schema: 'float32[384]', updated: '2024-02-01', usedBy: 12 },
  { id: 'f2', name: 'transaction_count_7d', description: '7-day transaction count', type: 'scalar', source: 'Analytics', schema: 'int64', updated: '2024-02-01', usedBy: 8 },
  { id: 'f3', name: 'session_window_1h', description: '1-hour session window', type: 'window', source: 'Stream', schema: 'struct', updated: '2024-02-01', usedBy: 5 },
  { id: 'f4', name: 'account_tier', description: 'Derived account tier', type: 'derived', source: 'Transformation', schema: 'enum', updated: '2024-02-01', usedBy: 15 },
  { id: 'f5', name: 'embedding_latest', description: 'Latest text embedding (1536d)', type: 'vector', source: 'Azure AI Foundry', schema: 'float32[1536]', updated: '2024-02-01', usedBy: 20 },
];

const typeColors = { vector: '#7C3AED', scalar: '#0F62FE', window: '#10B981', derived: '#F59E0B' };

export default function StorePage() {
  const [features] = useState<Feature[]>(mockFeatures);
  const [search, setSearch] = useState('');

  const filtered = search 
    ? features.filter(f => f.name.includes(search) || f.description.toLowerCase().includes(search.toLowerCase()))
    : features;

  const stats = {
    total: features.length,
    vector: features.filter(f => f.type === 'vector').length,
    used: features.reduce((a, f) => a + f.usedBy, 0),
  };

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>Feature Store</h1>
          <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Reusable ML features from all runtimes</p>
        </div>
        <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 6, fontSize: 13, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 6 }}>
          + New Feature
        </button>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{stats.total}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Total Features</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#7C3AED' }}>{stats.vector}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Vector</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#0F62FE' }}>{features.filter(f => f.type === 'scalar').length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Scalar</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{stats.used}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Total Usage</div>
        </div>
      </div>

      {/* Search */}
      <input
        placeholder="Search features..."
        value={search}
        onChange={e => setSearch(e.target.value)}
        style={{ width: '100%', maxWidth: 400, padding: '10px 14px', borderRadius: 6, border: '1px solid #E5E5E5', marginBottom: 16, fontSize: 13 }}
      />

      {/* Feature List */}
      <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#F8F9FA' }}>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280', fontWeight: 600 }}>FEATURE</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280', fontWeight: 600 }}>TYPE</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280', fontWeight: 600 }}>SOURCE</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280', fontWeight: 600 }}>SCHEMA</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280', fontWeight: 600 }}>USED BY</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280', fontWeight: 600 }}>UPDATED</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(feature => (
              <tr key={feature.id} style={{ borderTop: '1px solid #F4F4F4' }}>
                <td style={{ padding: '14px 16px' }}>
                  <div style={{ fontSize: 13, fontWeight: 500 }}>{feature.name}</div>
                  <div style={{ fontSize: 12, color: '#6B7280' }}>{feature.description}</div>
                </td>
                <td style={{ padding: '14px 16px' }}>
                  <span style={{ background: typeColors[feature.type as keyof typeof typeColors] + '20', color: typeColors[feature.type as keyof typeof typeColors], padding: '4px 8px', borderRadius: 4, fontSize: 11, textTransform: 'capitalize' }}>
                    {feature.type}
                  </span>
                </td>
                <td style={{ padding: '14px 16px', fontSize: 12 }}>{feature.source}</td>
                <td style={{ padding: '14px 16px', fontSize: 12, fontFamily: 'monospace', color: '#6B7280' }}>{feature.schema}</td>
                <td style={{ padding: '14px 16px', fontSize: 12 }}>{feature.usedBy} agents</td>
                <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280' }}>{feature.updated}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}