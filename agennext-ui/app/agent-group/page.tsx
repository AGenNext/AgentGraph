'use client';

import { useState } from 'react';

interface AgentGroup {
  id: string;
  name: string;
  description: string;
  agents: number;
  status: 'active' | 'archived' | 'development';
  lastUpdated: string;
}

const groups: AgentGroup[] = [
  { id: '1', name: 'Data Processing', description: 'ETL and data pipelines', agents: 12, status: 'active', lastUpdated: '1h ago' },
  { id: '2', name: 'Content Generation', description: 'Text and media creation', agents: 8, status: 'active', lastUpdated: '30m ago' },
  { id: '3', name: 'Customer Support', description: 'Ticket handling', agents: 15, status: 'active', lastUpdated: '5m ago' },
  { id: '4', name: 'Security Audit', description: 'Vulnerability scanning', agents: 6, status: 'development', lastUpdated: '2d ago' },
  { id: '5', name: 'Legacy Systems', description: 'Old integration agents', agents: 4, status: 'archived', lastUpdated: '30d ago' },
  { id: '6', name: 'Code Review', description: 'PR analysis', agents: 3, status: 'active', lastUpdated: '15m ago' },
];

export default function AgentGroupPage() {
  const [filter, setFilter] = useState<string>('all');

  const filtered = filter === 'all' ? groups : groups.filter(g => g.status === filter);
  const totalAgents = groups.reduce((a, g) => a + g.agents, 0);

  return (
    <div style={{ padding: 24, background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <h1 style={{ fontSize: 24, marginBottom: 20 }}>Agent Groups</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#10B981' }}>{groups.filter(g => g.status === 'active').length}</div>
          <div style={{ color: '#8C8C8C' }}>Active</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#58A6FF' }}>{totalAgents}</div>
          <div style={{ color: '#8C8C8C' }}>Total Agents</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#D29922' }}>{groups.filter(g => g.status === 'development').length}</div>
          <div style={{ color: '#8C8C8C' }}>In Development</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#8C8C8C' }}>{groups.length}</div>
          <div style={{ color: '#8C8C8C' }}>Groups</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        {['all', 'active', 'development', 'archived'].map(s => (
          <button key={s} onClick={() => setFilter(s)} style={{
            padding: '8px 16px', background: filter === s ? '#238636' : '#21262D',
            border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer', textTransform: 'capitalize'
          }}>
            {s}
          </button>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
        {filtered.map(g => (
          <div key={g.id} style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <strong>{g.name}</strong>
              <span style={{ color: g.status === 'active' ? '#10B981' : g.status === 'development' ? '#58A6FF' : '#8C8C8C' }}>
                {g.status}
              </span>
            </div>
            <p style={{ color: '#8C8C8C', fontSize: 12 }}>{g.description}</p>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8, fontSize: 12, color: '#8C8C8C' }}>
              <span>🤖 {g.agents} agents</span>
              <span>⏱ {g.lastUpdated}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}