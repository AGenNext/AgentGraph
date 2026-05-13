'use client';

import { useState } from 'react';

interface SearchResult {
  id: string;
  title: string;
  snippet: string;
  source: 'notion' | 'confluence' | 'slack' | 'drive' | 'github' | 'internal';
  url: string;
  timestamp: string;
  relevance: number;
}

const results: SearchResult[] = [
  { id: '1', title: 'Agent Zero Architecture', snippet: 'The root orchestrator delegates tasks to child agents using LangGraph for state management and tool calling...', source: 'notion', url: '#', timestamp: '2024-03-15', relevance: 95 },
  { id: '2', title: 'Integration Guide', snippet: 'Step 1: Initialize Agent SDK. Step 2: Configure frameworks. Step 3: Add custom tools...', source: 'confluence', url: '#', timestamp: '2024-03-14', relevance: 92 },
  { id: '3', title: 'Deployment Runbook', snippet: 'Deploy using Docker: docker-compose up -d. Scale agents: kubectl scale deployment agent-zero...', source: 'internal', url: '#', timestamp: '2024-03-14', relevance: 88 },
  { id: '4', title: 'API Reference', snippet: 'POST /agents - Create new agent. GET /agents/:id - Get agent status...', source: 'github', url: '#', timestamp: '2024-03-13', relevance: 85 },
  { id: '5', title: 'Team Guidelines', snippet: 'Use #agent-support for questions. Review PRs within 24 hours...', source: 'slack', url: '#', timestamp: '2024-03-12', relevance: 82 },
  { id: '6', title: 'Q1 Roadmap', snippet: 'Multi-modal support, Knowledge graphs, Enterprise SSO, Custom tools...', source: 'drive', url: '#', timestamp: '2024-03-10', relevance: 78 },
];

const sourceIcons: Record<string, string> = {
  notion: '📝',
  confluence: '📘',
  slack: '💬',
  drive: '📁',
  github: '🐙',
  internal: '🏢',
};

const sourceColors: Record<string, string> = {
  notion: '#fff',
  confluence: '#0052CC',
  slack: '#4A154B',
  drive: '#4285F4',
  github: '#f0f6fc',
  internal: '#238636',
};

export default function EnterpriseSearchPage() {
  const [query, setQuery] = useState('');
  const [searched, setSearched] = useState(false);
  const [filter, setFilter] = useState<string>('all');

  const filtered = results.filter(r => 
    (filter === 'all' || r.source === filter) &&
    (query === '' || r.title.toLowerCase().includes(query.toLowerCase()) || r.snippet.toLowerCase().includes(query.toLowerCase()))
  );

  const handleSearch = () => {
    if (query.trim()) setSearched(true);
  };

  return (
    <div style={{ padding: 24, background: '#0a0e14', minHeight: '100vh', color: '#e6edf3', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 8, color: '#f0f6fc' }}>Enterprise Search</h1>
      <p style={{ color: '#8b949e', fontSize: 14, marginBottom: 32 }}>Search across all company knowledge sources</p>

      <div style={{ marginBottom: 24 }}>
        <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
          <input value={query} onChange={e => setQuery(e.target.value)} onKeyDown={e => e.key === 'Enter' && handleSearch()} placeholder="Search documentation, code, conversations..." style={{ flex: 1, padding: 14, background: '#161b22', border: '1px solid #30363d', borderRadius: 8, color: '#e6edf3', fontSize: 15 }} />
          <button onClick={handleSearch} style={{ padding: '14px 24px', background: 'linear-gradient(135deg, #238636, #2ea043)', border: 'none', borderRadius: 8, color: '#fff', fontSize: 15, fontWeight: 500, cursor: 'pointer' }}>
            🔍 Search
          </button>
        </div>

        <div style={{ display: 'flex', gap: 8 }}>
          {['all', 'notion', 'confluence', 'github', 'slack', 'drive', 'internal'].map(s => (
            <button key={s} onClick={() => setFilter(s)} style={{ padding: '6px 12px', background: filter === s ? '#238636' : '#21262d', border: '1px solid #30363d', borderRadius: 6, color: '#fff', fontSize: 12, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 6 }}>
              <span>{sourceIcons[s]}</span>
              <span style={{ textTransform: 'capitalize' }}>{s}</span>
            </button>
          ))}
        </div>
      </div>

      {searched && (
        <div style={{ marginBottom: 16, fontSize: 14, color: '#8b949e' }}>
          Found <strong style={{ color: '#f0f6fc' }}>{filtered.length}</strong> results for "<strong style={{ color: '#f0f6fc' }}>{query}</strong>"
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {(searched ? filtered : results.slice(0, 3)).map(result => (
          <div key={result.id} style={{ padding: 16, background: '#161b22', borderRadius: 8, border: '1px solid #30363d', cursor: 'pointer' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <span style={{ fontSize: 20 }}>{sourceIcons[result.source]}</span>
                <div>
                  <h3 style={{ fontSize: 15, fontWeight: 600, color: '#58a6ff' }}>{result.title}</h3>
                  <p style={{ fontSize: 12, color: '#8b949e', textTransform: 'capitalize' }}>{result.source} · {result.timestamp}</p>
                </div>
              </div>
              <div style={{ padding: '4px 8px', background: result.relevance >= 90 ? '#23863622' : '#21262d', borderRadius: 4, fontSize: 11, color: result.relevance >= 90 ? '#3fb950' : '#8b949e' }}>
                {result.relevance}% match
              </div>
            </div>
            <p style={{ fontSize: 13, color: '#8b949e', lineHeight: 1.5 }}>{result.snippet}</p>
          </div>
        ))}
      </div>

      {!searched && (
        <div style={{ marginTop: 24, display: 'flex', gap: 8, justifyContent: 'center' }}>
          <span style={{ fontSize: 12, color: '#8b949e' }}>Try: agent setup, deployment, API integration</span>
        </div>
      )}

      <div style={{ marginTop: 32, padding: 16, background: '#161b22', borderRadius: 8, border: '1px solid #30363d' }}>
        <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>Connected Sources</h3>
        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
          {Object.entries(sourceIcons).map(([source, icon]) => (
            <div key={source} style={{ padding: '8px 12px', background: '#21262d', borderRadius: 6, display: 'flex', alignItems: 'center', gap: 8 }}>
              <span>{icon}</span>
              <span style={{ fontSize: 12, textTransform: 'capitalize' }}>{source}</span>
              <span style={{ fontSize: 10, color: '#3fb950' }}>✓</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}