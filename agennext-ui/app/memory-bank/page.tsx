'use client';

import { useState } from 'react';

interface MemoryEntry {
  id: string;
  type: 'fact' | 'preference' | 'conversation' | 'tool_use' | 'knowledge';
  key: string;
  value: string;
  source: string;
  agent: string;
  category: string;
  importance: number;
  timestamp: string;
}

const memories: MemoryEntry[] = [
  { id: '1', type: 'fact', key: 'user_industry', value: 'Enterprise Software', source: 'conversation', agent: 'Agent Zero', category: 'User', importance: 9, timestamp: '2024-03-15T10:00:00Z' },
  { id: '2', type: 'preference', key: 'response_style', value: 'Concise, under 100 words', source: 'explicit', agent: 'Agent Zero', category: 'User', importance: 9, timestamp: '2024-03-15T09:30:00Z' },
  { id: '3', type: 'fact', key: 'cloud_provider', value: 'Azure', source: 'conversation', agent: 'DevOps Agent', category: 'Infrastructure', importance: 8, timestamp: '2024-03-14T14:00:00Z' },
  { id: '4', type: 'preference', key: 'language', value: 'TypeScript', source: 'code_analysis', agent: 'Code Agent', category: 'Tech Stack', importance: 8, timestamp: '2024-03-14T16:00:00Z' },
  { id: '5', type: 'knowledge', key: 'api_rate_limit', value: '1000 req/min for OpenAI', source: 'tool', agent: 'Research', category: 'API', importance: 7, timestamp: '2024-03-15T08:00:00Z' },
  { id: '6', type: 'tool_use', key: 'web_search_count', value: '47 calls today', source: 'tool', agent: 'Research', category: 'Usage', importance: 5, timestamp: '2024-03-15T11:00:00Z' },
  { id: '7', type: 'fact', key: 'team_size', value: '5 developers', source: 'conversation', agent: 'Agent Zero', category: 'Team', importance: 6, timestamp: '2024-03-14T11:00:00Z' },
  { id: '8', type: 'knowledge', key: 'mcp_protocol', value: 'Model Context Protocol for tools', source: 'docs', agent: 'Research', category: 'Protocol', importance: 7, timestamp: '2024-03-13T15:00:00Z' },
];

const typeStyles: Record<string, { bg: string; color: string }> = {
  fact: { bg: 'rgba(63, 185, 80, 0.15)', color: '#3fb950' },
  preference: { bg: 'rgba(210, 153, 34, 0.15)', color: '#d29922' },
  conversation: { bg: 'rgba(88, 166, 255, 0.15)', color: '#58a6ff' },
  tool_use: { bg: 'rgba(247, 120, 186, 0.15)', color: '#f778ba' },
  knowledge: { bg: 'rgba(163, 113, 247, 0.15)', color: '#a371f7' },
};

export default function MemoryBankPage() {
  const [view, setView] = useState<'table' | 'cards'>('table');
  const [filter, setFilter] = useState<string>('all');
  const [search, setSearch] = useState('');

  const filtered = memories.filter(m =>
    (filter === 'all' || m.type === filter) &&
    (search === '' || m.key.toLowerCase().includes(search.toLowerCase()) || m.value.toLowerCase().includes(search.toLowerCase()))
  );

  const stats = {
    total: memories.length,
    facts: memories.filter(m => m.type === 'fact').length,
    preferences: memories.filter(m => m.type === 'preference').length,
    knowledge: memories.filter(m => m.type === 'knowledge').length,
  };

  return (
    <div style={{ padding: 24, background: '#F1F3F5', minHeight: '100vh', fontFamily: "'IBM Plex Sans', -apple-system, sans-serif" }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, color: '#161616' }}>Memory Bank</h1>
          <p style={{ color: '#5E6A75', fontSize: 14 }}>Persistent knowledge & context storage</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button onClick={() => setView('table')} style={{ padding: '8px 16px', background: view === 'table' ? '#0530AD' : 'white', border: '1px solid #C9D1D9', borderRadius: 2, color: view === 'table' ? 'white' : '#393D49', fontSize: 13, cursor: 'pointer' }}>Table</button>
          <button onClick={() => setView('cards')} style={{ padding: '8px 16px', background: view === 'cards' ? '#0530AD' : 'white', border: '1px solid #C9D1D9', borderRadius: 2, color: view === 'cards' ? 'white' : '#393D49', fontSize: 13, cursor: 'pointer' }}>Cards</button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ padding: 16, background: 'white', borderRadius: 4, border: '1px solid #E5E7E9' }}>
          <div style={{ fontSize: 28, fontWeight: 700, color: '#161616' }}>{stats.total}</div>
          <div style={{ fontSize: 12, color: '#5E6A75' }}>Total Entries</div>
        </div>
        <div style={{ padding: 16, background: 'white', borderRadius: 4, border: '1px solid #E5E7E9' }}>
          <div style={{ fontSize: 28, fontWeight: 700, color: '#198038' }}>{stats.facts}</div>
          <div style={{ fontSize: 12, color: '#5E6A75' }}>Facts</div>
        </div>
        <div style={{ padding: 16, background: 'white', borderRadius: 4, border: '1px solid #E5E7E9' }}>
          <div style={{ fontSize: 28, fontWeight: 700, color: '#B28600' }}>{stats.preferences}</div>
          <div style={{ fontSize: 12, color: '#5E6A75' }}>Preferences</div>
        </div>
        <div style={{ padding: 16, background: 'white', borderRadius: 4, border: '1px solid #E5E7E9' }}>
          <div style={{ fontSize: 28, fontWeight: 700, color: '#635BFF' }}>{stats.knowledge}</div>
          <div style={{ fontSize: 12, color: '#5E6A75' }}>Knowledge</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search memories..." style={{ flex: 1, padding: '10px 12px', background: 'white', border: '1px solid #C9D1D9', borderRadius: 2, fontSize: 13 }} />
        {['all', 'fact', 'preference', 'knowledge', 'conversation', 'tool_use'].map(f => (
          <button key={f} onClick={() => setFilter(f)} style={{ padding: '8px 12px', background: filter === f ? '#0530AD' : 'white', border: '1px solid #C9D1D9', borderRadius: 2, color: filter === f ? 'white' : '#393D49', fontSize: 12, cursor: 'pointer', textTransform: 'capitalize' }}>{f}</button>
        ))}
      </div>

      {view === 'table' ? (
        <div style={{ background: 'white', borderRadius: 4, border: '1px solid #E5E7E9', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
            <thead>
              <tr style={{ background: '#F1F3F5', borderBottom: '2px solid #E5E7E9' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontWeight: 600, color: '#5E6A75', fontSize: 11, textTransform: 'uppercase' }}>Type</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontWeight: 600, color: '#5E6A75', fontSize: 11, textTransform: 'uppercase' }}>Key</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontWeight: 600, color: '#5E6A75', fontSize: 11, textTransform: 'uppercase' }}>Value</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontWeight: 600, color: '#5E6A75', fontSize: 11, textTransform: 'uppercase' }}>Category</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontWeight: 600, color: '#5E6A75', fontSize: 11, textTransform: 'uppercase' }}>Agent</th>
                <th style={{ padding: '12px 16px', textAlign: 'right', fontWeight: 600, color: '#5E6A75', fontSize: 11, textTransform: 'uppercase' }}>Importance</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(m => (
                <tr key={m.id} style={{ borderBottom: '1px solid #E5E7E9' }}>
                  <td style={{ padding: '12px 16px' }}>
                    <span style={{ padding: '2px 8px', borderRadius: 2, fontSize: 11, fontWeight: 500, background: typeStyles[m.type].bg, color: typeStyles[m.type].color, textTransform: 'uppercase' }}>{m.type}</span>
                  </td>
                  <td style={{ padding: '12px 16px', fontWeight: 500, fontFamily: 'monospace', fontSize: 12 }}>{m.key}</td>
                  <td style={{ padding: '12px 16px', color: '#5E6A75' }}>{m.value}</td>
                  <td style={{ padding: '12px 16px', fontSize: 12, color: '#5E6A75' }}>{m.category}</td>
                  <td style={{ padding: '12px 16px', fontSize: 12 }}>{m.agent}</td>
                  <td style={{ padding: '12px 16px', textAlign: 'right' }}>
                    <div style={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                      {[1,2,3,4,5].map(i => (
                        <div key={i} style={{ width: 8, height: 8, borderRadius: 1, background: i <= m.importance ? '#0530AD' : '#E5E7E9' }} />
                      ))}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
          {filtered.map(m => (
            <div key={m.id} style={{ padding: 16, background: 'white', borderRadius: 4, border: '1px solid #E5E7E9' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                <span style={{ padding: '2px 8px', borderRadius: 2, fontSize: 10, fontWeight: 500, background: typeStyles[m.type].bg, color: typeStyles[m.type].color, textTransform: 'uppercase' }}>{m.type}</span>
                <span style={{ fontSize: 11, color: '#8993A5' }}>{m.category}</span>
              </div>
              <code style={{ fontSize: 12, color: '#0530AD' }}>{m.key}</code>
              <p style={{ fontSize: 13, color: '#393D49', marginTop: 4 }}>{m.value}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}