'use client';

import { useState } from 'react';

interface SalesAgent {
  id: string;
  name: string;
  target: string;
  stage: 'prospecting' | 'qualification' | 'proposal' | 'negotiation';
  deals: number;
  value: number;
  status: 'active' | 'paused';
}

const agents: SalesAgent[] = [
  { id: '1', name: 'Prospector Pro', target: 'Enterprise', stage: 'prospecting', deals: 45, value: 250000, status: 'active' },
  { id: '2', name: 'Qualify Bot', target: 'Mid-Market', stage: 'qualification', deals: 28, value: 180000, status: 'active' },
  { id: '3', name: 'Proposal Gen', target: 'Enterprise', stage: 'proposal', deals: 12, value: 340000, status: 'active' },
  { id: '4', name: 'Negotiate AI', target: 'All Tiers', stage: 'negotiation', deals: 8, value: 520000, status: 'active' },
  { id: '5', name: 'Cold Outreach', target: 'Startup', stage: 'prospecting', deals: 120, value: 85000, status: 'paused' },
  { id: '6', name: 'Qualify Bot', target: 'Enterprise', stage: 'qualification', deals: 22, value: 390000, status: 'active' },
];

export default function AgentSalesAssistPage() {
  const [filter, setFilter] = useState<string>('all');

  const filtered = filter === 'all' ? agents : agents.filter(a => a.stage === filter);
  const active = agents.filter(a => a.status === 'active').length;
  const totalValue = agents.reduce((a, a2) => a + a2.value, 0);

  return (
    <div style={{ padding: 24, background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <h1 style={{ fontSize: 24, marginBottom: 20 }}>Agent Sales Assist</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#10B981' }}>{active}</div>
          <div style={{ color: '#8C8C8C' }}>Active</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#58A6FF' }}>${Math.round(totalValue/1000)}k</div>
          <div style={{ color: '#8C8C8C' }}>Pipeline Value</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#D29922' }}>{agents.reduce((a, a2) => a + a2.deals, 0)}</div>
          <div style={{ color: '#8C8C8C' }}>Total Deals</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#8C8C8C' }}>{agents.length}</div>
          <div style={{ color: '#8C8C8C' }}>Agents</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        {['all', 'prospecting', 'qualification', 'proposal', 'negotiation'].map(s => (
          <button key={s} onClick={() => setFilter(s)} style={{
            padding: '8px 16px', background: filter === s ? '#238636' : '#21262D',
            border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer', textTransform: 'capitalize'
          }}>
            {s}
          </button>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
        {filtered.map(a => (
          <div key={a.id} style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <strong>{a.name}</strong>
              <span style={{ color: a.status === 'active' ? '#10B981' : '#8C8C8C' }}>{a.status}</span>
            </div>
            <p style={{ color: '#8C8C8C', fontSize: 12 }}>{a.target}</p>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8, fontSize: 12, color: '#8C8C8C' }}>
              <span>📋 {a.deals} deals</span>
              <span style={{ color: '#58A6FF' }}>${(a.value/1000).toFixed(0)}k</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}