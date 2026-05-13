'use client';

import { useState } from 'react';

interface Identity {
  id: string;
  name: string;
  type: 'user' | 'service' | 'agent';
  status: 'active' | 'suspended' | 'revoked';
  created: string;
}

const identities: Identity[] = [
  { id: '1', name: 'Admin User', type: 'user', status: 'active', created: '2024-01-01' },
  { id: '2', name: 'Agent Zero', type: 'agent', status: 'active', created: '2024-01-15' },
  { id: '3', name: 'Research Agent', type: 'agent', status: 'active', created: '2024-01-20' },
];

export default function IdentityPage() {
  const [filter, setFilter] = useState<'all' | 'user' | 'service' | 'agent'>('all');
  const filtered = filter === 'all' ? identities : identities.filter(i => i.type === filter);

  return (
    <div style={{ padding: 24, background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <h1 style={{ fontSize: 24, marginBottom: 20 }}>Identity Management</h1>
      
      <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
        {(['all', 'user', 'service', 'agent'] as const).map(t => (
          <button key={t} onClick={() => setFilter(t)} style={{
            padding: '8px 16px', background: filter === t ? '#238636' : '#21262D',
            border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer'
          }}>
            {t}
          </button>
        ))}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {filtered.map(id => (
          <div key={id.id} style={{
            padding: 16, background: '#21262D', borderRadius: 8,
            display: 'flex', justifyContent: 'space-between'
          }}>
            <span>{id.name}</span>
            <span style={{ color: id.status === 'active' ? '#10B981' : '#F85149' }}>{id.status}</span>
          </div>
        ))}
      </div>
    </div>
  );
}