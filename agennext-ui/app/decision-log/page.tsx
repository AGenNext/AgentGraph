'use client';

import { useState } from 'react';

interface Decision {
  id: string;
  timestamp: string;
  agent: string;
  type: 'action' | 'tool' | 'model' | 'route' | 'policy';
  decision: string;
  reasoning: string;
  outcome: 'success' | 'failed' | 'pending';
  confidence: number;
  alternatives: string[];
}

const decisions: Decision[] = [
  { id: '1', timestamp: '2024-03-15T11:30:00Z', agent: 'Agent Zero', type: 'tool', decision: 'Use web-search instead of direct API', reasoning: 'Web search provides fresher data with citations', outcome: 'success', confidence: 85, alternatives: ['Direct API call', 'Knowledge base'] },
  { id: '2', timestamp: '2024-03-15T11:25:00Z', agent: 'Research', type: 'route', decision: 'Route to Claude for complex analysis', reasoning: 'Claude has better reasoning for multi-step problems', outcome: 'success', confidence: 90, alternatives: ['GPT-4', 'Gemini'] },
  { id: '3', timestamp: '2024-03-15T11:20:00Z', agent: 'Code Agent', type: 'action', decision: 'Refactor authentication module', reasoning: 'Security audit findings suggest separation of concerns', outcome: 'pending', confidence: 75, alternatives: ['Add middleware', 'Leave as-is'] },
  { id: '4', timestamp: '2024-03-15T11:15:00Z', agent: 'DevOps', type: 'model', decision: 'Use gpt-4o-mini for validation', reasoning: 'Fast response needed, high accuracy not critical', outcome: 'success', confidence: 80, alternatives: ['gpt-4o', 'claude-sonnet'] },
  { id: '5', timestamp: '2024-03-15T11:10:00Z', agent: 'Sales Agent', type: 'policy', decision: 'Approve discount >20%', reasoning: 'Enterprise tier allows up to 30% discount', outcome: 'failed', confidence: 60, alternatives: ['Deny', 'Escalate'] },
  { id: '6', timestamp: '2024-03-15T11:05:00Z', agent: 'Research', type: 'tool', decision: 'Use code-executor for output validation', reasoning: 'Cannot trust external tool output directly', outcome: 'success', confidence: 92, alternatives: ['Skip validation', 'Manual review'] },
];

const typeColors: Record<string, { bg: string; color: string }> = {
  action: { bg: 'rgba(63, 185, 80, 0.15)', color: '#198038' },
  tool: { bg: 'rgba(247, 120, 186, 0.15)', color: '#D63384' },
  model: { bg: 'rgba(88, 166, 255, 0.15)', color: '#0530AD' },
  route: { bg: 'rgba(162, 113, 247, 0.15)', color: '#635BFF' },
  policy: { bg: 'rgba(210, 153, 34, 0.15)', color: '#B28600' },
};

export default function DecisionLogPage() {
  const [filter, setFilter] = useState<string>('all');
  const [view, setView] = useState<'table' | 'timeline'>('table');

  const filtered = decisions.filter(d => filter === 'all' || d.type === filter);

  const stats = {
    total: decisions.length,
    success: decisions.filter(d => d.outcome === 'success').length,
    pending: decisions.filter(d => d.outcome === 'pending').length,
    avgConfidence: Math.round(decisions.reduce((a,b) => a + b.confidence, 0) / decisions.length),
  };

  return (
    <div style={{ padding: 24, background: '#F1F3F5', minHeight: '100vh', fontFamily: "'IBM Plex Sans', -apple-system, sans-serif" }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, color: '#161616' }}>Decision Log</h1>
          <p style={{ color: '#5E6A75', fontSize: 14 }}>Agent reasoning & decision trail</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button onClick={() => setView('table')} style={{ padding: '8px 16px', background: view === 'table' ? '#0530AD' : 'white', border: '1px solid #C9D1D9', borderRadius: 2, color: view === 'table' ? 'white' : '#393D49', fontSize: 13, cursor: 'pointer' }}>Table</button>
          <button onClick={() => setView('timeline')} style={{ padding: '8px 16px', background: view === 'timeline' ? '#0530AD' : 'white', border: '1px solid #C9D1D9', borderRadius: 2, color: view === 'timeline' ? 'white' : '#393D49', fontSize: 13, cursor: 'pointer' }}>Timeline</button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ padding: 16, background: 'white', borderRadius: 4, border: '1px solid #E5E7E9' }}>
          <div style={{ fontSize: 28, fontWeight: 700, color: '#161616' }}>{stats.total}</div>
          <div style={{ fontSize: 12, color: '#5E6A75' }}>Total Decisions</div>
        </div>
        <div style={{ padding: 16, background: 'white', borderRadius: 4, border: '1px solid #E5E7E9' }}>
          <div style={{ fontSize: 28, fontWeight: 700, color: '#198038' }}>{stats.success}</div>
          <div style={{ fontSize: 12, color: '#5E6A75' }}>Successful</div>
        </div>
        <div style={{ padding: 16, background: 'white', borderRadius: 4, border: '1px solid #E5E7E9' }}>
          <div style={{ fontSize: 28, fontWeight: 700, color: '#B28600' }}>{stats.pending}</div>
          <div style={{ fontSize: 12, color: '#5E6A75' }}>Pending</div>
        </div>
        <div style={{ padding: 16, background: 'white', borderRadius: 4, border: '1px solid #E5E7E9' }}>
          <div style={{ fontSize: 28, fontWeight: 700, color: '#0530AD' }}>{stats.avgConfidence}%</div>
          <div style={{ fontSize: 12, color: '#5E6A75' }}>Avg Confidence</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        {['all', 'action', 'tool', 'model', 'route', 'policy'].map(f => (
          <button key={f} onClick={() => setFilter(f)} style={{ padding: '6px 12px', background: filter === f ? '#0530AD' : 'white', border: '1px solid #C9D1D9', borderRadius: 2, color: filter === f ? 'white' : '#393D49', fontSize: 12, cursor: 'pointer', textTransform: 'capitalize' }}>{f}</button>
        ))}
      </div>

      {view === 'table' ? (
        <div style={{ background: 'white', borderRadius: 4, border: '1px solid #E5E7E9', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
            <thead>
              <tr style={{ background: '#F1F3F5', borderBottom: '2px solid #E5E7E9' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontWeight: 600, color: '#5E6A75', fontSize: 11, textTransform: 'uppercase' }}>Time</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontWeight: 600, color: '#5E6A75', fontSize: 11, textTransform: 'uppercase' }}>Agent</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontWeight: 600, color: '#5E6A75', fontSize: 11, textTransform: 'uppercase' }}>Type</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontWeight: 600, color: '#5E6A75', fontSize: 11, textTransform: 'uppercase' }}>Decision</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontWeight: 600, color: '#5E6A75', fontSize: 11, textTransform: 'uppercase' }}>Reasoning</th>
                <th style={{ padding: '12px 16px', textAlign: 'center', fontWeight: 600, color: '#5E6A75', fontSize: 11, textTransform: 'uppercase' }}>Confidence</th>
                <th style={{ padding: '12px 16px', textAlign: 'center', fontWeight: 600, color: '#5E6A75', fontSize: 11, textTransform: 'uppercase' }}>Outcome</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(d => (
                <tr key={d.id} style={{ borderBottom: '1px solid #E5E7E9' }}>
                  <td style={{ padding: '12px 16px', fontSize: 12, color: '#5E6A75', fontFamily: 'monospace' }}>{d.timestamp.split('T')[1].replace('Z','')}</td>
                  <td style={{ padding: '12px 16px', fontWeight: 500 }}>{d.agent}</td>
                  <td style={{ padding: '12px 16px' }}>
                    <span style={{ padding: '2px 8px', borderRadius: 2, fontSize: 10, fontWeight: 500, background: typeColors[d.type].bg, color: typeColors[d.type].color, textTransform: 'uppercase' }}>{d.type}</span>
                  </td>
                  <td style={{ padding: '12px 16px', maxWidth: 200 }}>{d.decision}</td>
                  <td style={{ padding: '12px 16px', color: '#5E6A75', maxWidth: 180 }}>{d.reasoning}</td>
                  <td style={{ padding: '12px 16px', textAlign: 'center' }}>
                    <span style={{ padding: '4px 8px', background: d.confidence >= 80 ? 'rgba(25,128,56,0.15)' : d.confidence >= 60 ? 'rgba(178,134,0,0.15)' : 'rgba(220,38,38,0.15)', color: d.confidence >= 80 ? '#198038' : d.confidence >= 60 ? '#B28600' : '#DA1E28', borderRadius: 2, fontSize: 12, fontWeight: 500 }}>{d.confidence}%</span>
                  </td>
                  <td style={{ padding: '12px 16px', textAlign: 'center' }}>
                    <span style={{ 
                      display: 'inline-block', width: 8, height: 8, borderRadius: '50%', 
                      background: d.outcome === 'success' ? '#198038' : d.outcome === 'pending' ? '#B28600' : '#DA1E28'
                    }} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div style={{ position: 'relative', paddingLeft: 24 }}>
          <div style={{ position: 'absolute', left: 8, top: 0, bottom: 0, width: 2, background: '#E5E7E9' }} />
          {filtered.map((d, i) => (
            <div key={d.id} style={{ position: 'relative', padding: '16px 0 16px 16px' }}>
              <div style={{ position: 'absolute', left: 4, top: 20, width: 10, height: 10, borderRadius: '50%', background: d.outcome === 'success' ? '#198038' : d.outcome === 'pending' ? '#B28600' : '#DA1E28' }} />
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ fontSize: 12, color: '#5E6A75' }}>{d.timestamp.replace('T',' ').replace('Z','')}</span>
                <span style={{ fontWeight: 500, fontSize: 13 }}>{d.agent}</span>
              </div>
              <p style={{ fontSize: 14, fontWeight: 500, marginTop: 4 }}>{d.decision}</p>
              <p style={{ fontSize: 12, color: '#5E6A75', marginTop: 2 }}>{d.reasoning}</p>
              <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
                <span style={{ padding: '2px 6px', background: typeColors[d.type].bg, color: typeColors[d.type].color, borderRadius: 2, fontSize: 10, textTransform: 'uppercase' }}>{d.type}</span>
                <span style={{ fontSize: 11, color: '#5E6A75' }}>{d.confidence}% confidence</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}