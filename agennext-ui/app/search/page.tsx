'use client';

import { useState } from 'react';

interface SearchResult {
  id: string;
  type: 'agent' | 'task' | 'document' | 'contract' | 'user' | 'team' | 'kb';
  title: string;
  description: string;
  source: string;
  timestamp: string;
}

const mockResults: SearchResult[] = [
  { id: 'a1', type: 'agent', title: 'Research Agent', description: 'Multi-source research agent', source: 'Workspace', timestamp: '2024-02-01' },
  { id: 't1', type: 'task', title: 'Analyze Q4 data', description: 'Completed successfully', source: 'Tasks', timestamp: '2024-02-01' },
  { id: 'd1', type: 'document', title: 'API Documentation', description: 'REST API reference', source: 'RAG', timestamp: '2024-01-28' },
  { id: 'c1', type: 'contract', title: 'Vendor NDA', description: 'Active contract', source: 'Contracts', timestamp: '2024-01-01' },
  { id: 'u1', type: 'user', title: 'Admin User', description: 'admin@company.io', source: 'Admin', timestamp: '2024-01-15' },
  { id: 'tm1', type: 'team', title: 'Research Team', description: 'Sequential pipeline', source: 'Team', timestamp: '2024-01-20' },
  { id: 'kb1', type: 'kb', title: 'Product Docs', description: '150 documents', source: 'RAG', timestamp: '2024-02-01' },
];

const typeIcons = { agent: '🤖', task: '✅', document: '📄', contract: '📜', user: '👤', team: '👥', kb: '📚' };
const typeColors = { agent: '#7C3AED', task: '#10B981', document: '#0F62FE', contract: '#F59E0B', user: '#6B7280', team: '#8B5CF6', kb: '#EC4899' };

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [results] = useState<SearchResult[]>(mockResults);

  const filtered = query ? results.filter(r => 
    r.title.toLowerCase().includes(query.toLowerCase()) || 
    r.description.toLowerCase().includes(query.toLowerCase())
  ) : results;

  const byType = Object.entries(typeIcons).reduce((acc, [type]) => {
    acc[type] = filtered.filter(r => r.type === type).length;
    return acc;
  }, {} as Record<string, number>);

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F4F4F4', minHeight: '100vh' }}>
      <div style={{ maxWidth: 800, margin: '0 auto' }}>
        <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 24, textAlign: 'center' }}>Search</h1>
        
        <div style={{ position: 'relative', marginBottom: 24 }}>
          <input
            placeholder="Search agents, tasks, documents, contracts..."
            value={query}
            onChange={e => setQuery(e.target.value)}
            style={{ 
              width: '100%', 
              padding: '16px 48px 16px 48px', 
              border: '1px solid #E5E5E5', 
              borderRadius: 8, 
              fontSize: 16,
              boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
            }}
          />
          <span style={{ position: 'absolute', left: 16, top: 16, fontSize: 20 }}>🔍</span>
        </div>

        <div style={{ display: 'flex', gap: 8, marginBottom: 24, flexWrap: 'wrap' }}>
          {Object.entries(typeIcons).map(([type, icon]) => (
            <button key={type} style={{ 
              background: '#fff', 
              border: '1px solid #E5E5E5', 
              padding: '6px 12px', 
              borderRadius: 999, 
              fontSize: 12,
              display: 'flex',
              alignItems: 'center',
              gap: 6,
              cursor: 'pointer',
            }}>
              <span>{icon}</span>
              <span style={{ textTransform: 'capitalize' }}>{type}</span>
              <span style={{ color: '#8C8C8C' }}>{byType[type]}</span>
            </button>
          ))}
        </div>

        <div style={{ background: '#fff', borderRadius: 8, overflow: 'hidden' }}>
          {filtered.map(r => (
            <div key={r.id} style={{ padding: 16, borderBottom: '1px solid #E5E5E5', cursor: 'pointer' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <span style={{ fontSize: 20 }}>{typeIcons[r.type as keyof typeof typeIcons]}</span>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 500 }}>{r.title}</div>
                  <div style={{ fontSize: 12, color: '#525252' }}>{r.description}</div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <span style={{ background: typeColors[r.type as keyof typeof typeColors] + '20', color: typeColors[r.type as keyof typeof typeColors], padding: '2px 8px', borderRadius: 4, fontSize: 10, textTransform: 'capitalize' }}>
                    {r.type}
                  </span>
                  <div style={{ fontSize: 10, color: '#8C8C8C', marginTop: 4 }}>{r.timestamp}</div>
                </div>
              </div>
            </div>
          ))}
          {filtered.length === 0 && (
            <div style={{ padding: 32, textAlign: 'center', color: '#8C8C8C' }}>No results found</div>
          )}
        </div>
      </div>
    </div>
  );
}