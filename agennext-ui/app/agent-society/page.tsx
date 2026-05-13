'use client';

import { useState } from 'react';

interface Society {
  id: string;
  name: string;
  description: string;
  members: number;
  type: 'research' | 'open-source' | 'enterprise' | 'hackathon';
  status: 'public' | 'private';
}

const societies: Society[] = [
  { id: '1', name: 'LangChain Community', description: 'Open source LLM framework', members: 12500, type: 'open-source', status: 'public' },
  { id: '2', name: 'AI Safety Research', description: 'Responsible AI development', members: 3400, type: 'research', status: 'public' },
  { id: '3', name: 'Enterprise Agents', description: 'Business AI solutions', members: 890, type: 'enterprise', status: 'private' },
  { id: '4', name: 'Hackathon Builders', description: 'Weekend agent challenges', members: 2200, type: 'hackathon', status: 'public' },
  { id: '5', name: 'Autogen Collective', description: 'Multi-agent systems', members: 5600, type: 'open-source', status: 'public' },
  { id: '6', name: 'Healthcare AI', description: 'Medical agent applications', members: 780, type: 'enterprise', status: 'private' },
];

export default function AgentSocietyPage() {
  const [filter, setFilter] = useState<string>('all');

  const filtered = filter === 'all' ? societies : societies.filter(s => s.type === filter);
  const totalMembers = societies.reduce((a, s) => a + s.members, 0);

  return (
    <div style={{ padding: 24, background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <h1 style={{ fontSize: 24, marginBottom: 20 }}>Agent Society</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#58A6FF' }}>{societies.length}</div>
          <div style={{ color: '#8C8C8C' }}>Societies</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#10B981' }}>{Math.round(totalMembers/1000)}k</div>
          <div style={{ color: '#8C8C8C' }}>Total Members</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#D29922' }}>{societies.filter(s => s.status === 'public').length}</div>
          <div style={{ color: '#8C8C8C' }}>Public</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        {['all', 'open-source', 'research', 'enterprise', 'hackathon'].map(t => (
          <button key={t} onClick={() => setFilter(t)} style={{
            padding: '8px 16px', background: filter === t ? '#238636' : '#21262D',
            border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer', textTransform: 'capitalize'
          }}>
            {t.replace('-', ' ')}
          </button>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
        {filtered.map(s => (
          <div key={s.id} style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <strong>{s.name}</strong>
              <span style={{ fontSize: 12, color: s.status === 'public' ? '#10B981' : '#D29922' }}>{s.status}</span>
            </div>
            <p style={{ color: '#8C8C8C', fontSize: 12, marginBottom: 8 }}>{s.description}</p>
            <div style={{ display: 'flex', gap: 8, fontSize: 12 }}>
              <span style={{ padding: '2px 8px', background: '#30363D', borderRadius: 4 }}>{s.type}</span>
              <span style={{ color: '#8C8C8C' }}>👥 {s.members.toLocaleString()}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}