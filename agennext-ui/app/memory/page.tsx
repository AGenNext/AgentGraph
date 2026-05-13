'use client';

import { useState } from 'react';

interface MemoryEntry {
  id: string;
  type: 'conversation' | 'fact' | 'preference' | 'tool_use';
  content: string;
  agent: string;
  timestamp: string;
  importance: number;
}

const memories: MemoryEntry[] = [
  { id: '1', type: 'preference', content: 'User prefers concise responses under 100 words', agent: 'Agent Zero', timestamp: '2024-03-15T10:00:00Z', importance: 9 },
  { id: '2', type: 'fact', content: 'User works in enterprise software development', agent: 'Research Agent', timestamp: '2024-03-15T09:30:00Z', importance: 7 },
  { id: '3', type: 'conversation', content: 'Discussed API integration requirements', agent: 'Agent Zero', timestamp: '2024-03-15T09:15:00Z', importance: 6 },
  { id: '4', type: 'tool_use', content: 'Used web-search tool 5 times today', agent: 'Research Agent', timestamp: '2024-03-15T08:45:00Z', importance: 5 },
  { id: '5', type: 'preference', content: 'Prefers TypeScript over Python for code', agent: 'Code Agent', timestamp: '2024-03-14T16:00:00Z', importance: 8 },
  { id: '6', type: 'fact', content: 'Company uses Azure for cloud infrastructure', agent: 'DevOps Agent', timestamp: '2024-03-14T14:00:00Z', importance: 8 },
];

const typeColors: Record<string, { bg: string; text: string }> = {
  conversation: { bg: 'rgba(88, 166, 255, 0.15)', text: '#58a6ff' },
  fact: { bg: 'rgba(63, 185, 80, 0.15)', text: '#3fb950' },
  preference: { bg: 'rgba(210, 153, 34, 0.15)', text: '#d29922' },
  tool_use: { bg: 'rgba(247, 120, 186, 0.15)', text: '#f778ba' },
};

export default function MemoryPage() {
  const [filter, setFilter] = useState<string>('all');
  const [search, setSearch] = useState('');

  const filtered = memories.filter(m => 
    (filter === 'all' || m.type === filter) && 
    (search === '' || m.content.toLowerCase().includes(search.toLowerCase()))
  );

  const total = memories.length;
  const highPriority = memories.filter(m => m.importance >= 8).length;

  return (
    <div style={{ padding: 24, background: '#0a0e14', minHeight: '100vh', color: '#e6edf3', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 8, color: '#f0f6fc' }}>Agent Memory</h1>
      <p style={{ color: '#8b949e', fontSize: 14, marginBottom: 32 }}>Persistent knowledge & conversation context</p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 32 }}>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#58a6ff' }}>{total}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Total Memories</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#d29922' }}>{highPriority}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>High Priority</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#3fb950' }}>98%</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Recall Rate</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 12, marginBottom: 24 }}>
        <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search memories..." style={{ flex: 1, padding: 10, background: '#161b22', border: '1px solid #30363d', borderRadius: 8, color: '#e6edf3', fontSize: 14 }} />
        <div style={{ display: 'flex', gap: 4, background: '#161b22', padding: 4, borderRadius: 8 }}>
          {['all', 'conversation', 'fact', 'preference', 'tool_use'].map(f => (
            <button key={f} onClick={() => setFilter(f)} style={{ padding: '6px 12px', background: filter === f ? '#238636' : 'transparent', border: 'none', borderRadius: 6, color: '#fff', fontSize: 12, cursor: 'pointer', textTransform: 'capitalize' }}>
              {f.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {filtered.map(mem => (
          <div key={mem.id} style={{ padding: 16, background: '#161b22', borderRadius: 8, border: '1px solid #30363d' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <span style={{ padding: '4px 8px', borderRadius: 4, fontSize: 11, background: typeColors[mem.type].bg, color: typeColors[mem.type].text, textTransform: 'capitalize' }}>
                {mem.type.replace('_', ' ')}
              </span>
              <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                <span style={{ fontSize: 12, color: '#8b949e' }}>{mem.agent}</span>
                <span style={{ fontSize: 12, color: '#8b949e' }}>Importance: {mem.importance}/10</span>
              </div>
            </div>
            <p style={{ fontSize: 14, color: '#e6edf3' }}>{mem.content}</p>
            <p style={{ fontSize: 11, color: '#8b949e', marginTop: 8 }}>{new Date(mem.timestamp).toLocaleString()}</p>
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', gap: 12, marginTop: 24 }}>
        <button style={{ flex: 1, padding: 12, background: '#21262d', border: '1px solid #30363d', borderRadius: 8, color: '#fff', fontSize: 14, cursor: 'pointer' }}>
          Export Memory
        </button>
        <button style={{ flex: 1, padding: 12, background: '#f8514922', border: '1px solid #f85149', borderRadius: 8, color: '#f85149', fontSize: 14, cursor: 'pointer' }}>
          Clear All
        </button>
      </div>
    </div>
  );
}