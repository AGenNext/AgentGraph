'use client';

import { useState } from 'react';

interface CommunityMember {
  id: string;
  name: string;
  role: string;
  expertise: string[];
  contributions: number;
  status: 'online' | 'offline' | 'away';
}

const members: CommunityMember[] = [
  { id: '1', name: 'Sarah Chen', role: 'Core Contributor', expertise: ['LangChain', 'Python'], contributions: 245, status: 'online' },
  { id: '2', name: 'Alex Kumar', role: 'Maintainer', expertise: ['AutoGen', 'RAG'], contributions: 189, status: 'online' },
  { id: '3', name: 'Jordan Lee', role: 'Developer', expertise: ['CrewAI', 'VectorDB'], contributions: 78, status: 'away' },
  { id: '4', name: 'Morgan Smith', role: 'Community Lead', expertise: ['Mentorship', 'Events'], contributions: 156, status: 'online' },
  { id: '5', name: 'Casey Brown', role: 'Reviewer', expertise: ['Code Review', 'Security'], contributions: 312, status: 'offline' },
  { id: '6', name: 'Riley Davis', role: 'Contributor', expertise: ['Documentation', 'Testing'], contributions: 45, status: 'online' },
];

export default function AgentCommunityPage() {
  const [filter, setFilter] = useState<string>('all');

  const filtered = filter === 'all' ? members : members.filter(m => m.status === filter);
  const topContributor = members.sort((a, b) => b.contributions - a.contributions)[0];

  return (
    <div style={{ padding: 24, background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <h1 style={{ fontSize: 24, marginBottom: 20 }}>Agent Community</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#10B981' }}>{members.filter(m => m.status === 'online').length}</div>
          <div style={{ color: '#8C8C8C' }}>Online</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#D29922' }}>{members.filter(m => m.status === 'away').length}</div>
          <div style={{ color: '#8C8C8C' }}>Away</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#58A6FF' }}>{members.reduce((a, m) => a + m.contributions, 0)}</div>
          <div style={{ color: '#8C8C8C' }}>Contributions</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 24, color: '#10B981' }}>{topContributor.name}</div>
          <div style={{ color: '#8C8C8C', fontSize: 12 }}>Top Contributor</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        {['all', 'online', 'away', 'offline'].map(s => (
          <button key={s} onClick={() => setFilter(s)} style={{
            padding: '8px 16px', background: filter === s ? '#238636' : '#21262D',
            border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer', textTransform: 'capitalize'
          }}>
            {s}
          </button>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
        {filtered.map(m => (
          <div key={m.id} style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <strong>{m.name}</strong>
              <span style={{ 
                width: 8, height: 8, borderRadius: '50%', background: m.status === 'online' ? '#10B981' : m.status === 'away' ? '#D29922' : '#8C8C8C' 
              }} />
            </div>
            <p style={{ color: '#8C8C8C', fontSize: 12 }}>{m.role}</p>
            <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap', marginTop: 8 }}>
              {m.expertise.map(e => (
                <span key={e} style={{ fontSize: 10, padding: '2px 6px', background: '#30363D', borderRadius: 4 }}>{e}</span>
              ))}
            </div>
            <p style={{ fontSize: 12, color: '#58A6FF', marginTop: 8 }}>⭐ {m.contributions} contributions</p>
          </div>
        ))}
      </div>
    </div>
  );
}