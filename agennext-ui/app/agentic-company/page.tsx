'use client';

import { useState } from 'react';

interface AgenticCompany {
  id: string;
  name: string;
  type: 'startup' | 'enterprise' | 'msp' | 'consulting';
  agents: number;
  status: 'active' | 'pending' | 'suspended';
  region: string;
  created: string;
}

const companies: AgenticCompany[] = [
  { id: '1', name: 'TechCorp AI', type: 'enterprise', agents: 45, status: 'active', region: 'US-West', created: '2024-01-15' },
  { id: '2', name: "Founder's AI", type: 'startup', agents: 8, status: 'active', region: 'EU-Central', created: '2024-02-20' },
  { id: '3', name: 'Managed Solutions', type: 'msp', agents: 22, status: 'active', region: 'US-East', created: '2023-11-05' },
  { id: '4', name: 'Cloud Agents Inc', type: 'enterprise', agents: 67, status: 'pending', region: 'AP-South', created: '2024-03-01' },
  { id: '5', name: 'AI Consultants', type: 'consulting', agents: 12, status: 'active', region: 'EU-West', created: '2024-01-25' },
  { id: '6', name: 'Digital Force', type: 'enterprise', agents: 33, status: 'suspended', region: 'US-Central', created: '2023-08-10' },
];

export default function AgenticCompanyPage() {
  const [companys] = useState<AgenticCompany[]>(companies);
  const [filter, setFilter] = useState<string>('all');

  const filtered = filter === 'all' ? companys : companys.filter(c => c.type === filter);
  const totalAgents = companys.reduce((a, c) => a + c.agents, 0);
  const active = companys.filter(c => c.status === 'active').length;

  return (
    <div style={{ padding: 24, background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <h1 style={{ fontSize: 24, marginBottom: 20 }}>Agentic Companies</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#10B981' }}>{active}</div>
          <div style={{ color: '#8C8C8C' }}>Active</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#58A6FF' }}>{totalAgents}</div>
          <div style={{ color: '#8C8C8C' }}>Total Agents</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#D29922' }}>{companys.filter(c => c.type === 'enterprise').length}</div>
          <div style={{ color: '#8C8C8C' }}>Enterprise</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#8C8C8C' }}>{companys.length}</div>
          <div style={{ color: '#8C8C8C' }}>Companies</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        {['all', 'enterprise', 'startup', 'msp', 'consulting'].map(t => (
          <button key={t} onClick={() => setFilter(t)} style={{
            padding: '8px 16px', background: filter === t ? '#238636' : '#21262D',
            border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer', textTransform: 'capitalize'
          }}>
            {t}
          </button>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
        {filtered.map(c => (
          <div key={c.id} style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <strong>{c.name}</strong>
              <span style={{ color: c.status === 'active' ? '#10B981' : c.status === 'pending' ? '#D29922' : '#F85149' }}>
                {c.status}
              </span>
            </div>
            <p style={{ color: '#8C8C8C', fontSize: 12 }}>{c.type} · {c.region}</p>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: '#8C8C8C', marginTop: 8 }}>
              <span>🤖 {c.agents} agents</span>
              <span>📅 {c.created}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}