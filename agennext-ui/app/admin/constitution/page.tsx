'use client';

import { useState } from 'react';

interface Principle {
  id: string;
  title: string;
  description: string;
  category: 'ethics' | 'safety' | 'transparency' | 'accountability';
  status: 'active' | 'draft';
}

const principles: Principle[] = [
  { id: '1', title: 'Human Override', description: 'Agents must always allow human intervention and cannot take irreversible actions without approval', category: 'safety', status: 'active' },
  { id: '2', title: 'Truthful Responses', description: 'Agents must not hallucinate or provide false information. Uncertainty should be expressed.', category: 'ethics', status: 'active' },
  { id: '3', title: 'Privacy Protection', description: 'Agents must not expose sensitive data or PII without proper authorization', category: 'safety', status: 'active' },
  { id: '4', title: 'Explainable Decisions', description: 'Agent decisions must be traceable and provide reasoning when requested', category: 'transparency', status: 'active' },
  { id: '5', title: 'Harm Prevention', description: 'Agents must not assist in harmful activities including illegal actions', category: 'ethics', status: 'active' },
  { id: '6', title: 'Audit Trail', description: 'All agent actions must be logged for compliance and accountability', category: 'accountability', status: 'active' },
  { id: '7', title: 'Scope Boundaries', description: 'Agents must operate within defined permission boundaries', category: 'safety', status: 'draft' },
  { id: '8', title: 'Continuous Learning', description: 'Agents should learn from feedback while preserving privacy', category: 'transparency', status: 'draft' },
];

export default function ConstitutionPage() {
  const [filter, setFilter] = useState('all');
  const filtered = filter === 'all' ? principles : principles.filter(p => p.status === filter);

  return (
    <div style={{ padding: 24 }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 8 }}>Agent Constitution</h1>
      <p style={{ color: '#666', marginBottom: 24 }}>Core principles and rules governing agent behavior</p>
      
      <div style={{ marginBottom: 16, display: 'flex', gap: 8 }}>
        {['all', 'active', 'draft'].map(s => (
          <button key={s} onClick={() => setFilter(s)}
            style={{ padding: '8px 16px', borderRadius: 4, border: '1px solid #E5E5E5', background: filter === s ? '#1A1A2E' : '#fff', color: filter === s ? '#fff' : '#000', cursor: 'pointer' }}>
            {s.charAt(0).toUpperCase() + s.slice(1)}
          </button>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        {filtered.map(item => (
          <div key={item.id} style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <span style={{ fontWeight: 600 }}>{item.title}</span>
              <span style={{ fontSize: 11, padding: '2px 8px', borderRadius: 4, background: item.status === 'active' ? '#10B98120' : '#F59E0B20', color: item.status === 'active' ? '#10B981' : '#F59E0B' }}>
                {item.status}
              </span>
            </div>
            <p style={{ fontSize: 13, color: '#666', marginBottom: 8 }}>{item.description}</p>
            <span style={{ fontSize: 11, color: '#8B8BA7' }}>{item.category}</span>
          </div>
        ))}
      </div>
    </div>
  );
}