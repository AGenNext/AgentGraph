'use client';

import { useState } from 'react';

interface ModelRunner {
  id: string;
  name: string;
  model: string;
  provider: string;
  status: 'idle' | 'running' | 'completed' | 'error';
  progress: number;
  started: string;
  duration: number;
  cost: number;
}

const runners: ModelRunner[] = [
  { id: '1', name: 'GPT-4o Production', model: 'gpt-4o', provider: 'OpenAI', status: 'running', progress: 65, started: '10:30:00', duration: 45, cost: 0.32 },
  { id: '2', name: 'Claude Research', model: 'claude-3-opus', provider: 'Anthropic', status: 'completed', progress: 100, started: '10:15:00', duration: 28, cost: 1.25 },
  { id: '3', name: 'Gemini Fast', model: 'gemini-2.0-flash', provider: 'Google', status: 'running', progress: 35, started: '10:32:00', duration: 8, cost: 0.05 },
  { id: '4', name: 'Azure Enterprise', model: 'gpt-4', provider: 'Azure', status: 'completed', progress: 100, started: '10:00:00', duration: 120, cost: 0.85 },
  { id: '5', name: 'Sonnet Light', model: 'claude-3-sonnet', provider: 'Anthropic', status: 'idle', progress: 0, started: '-', duration: 0, cost: 0 },
  { id: '6', name: 'Mini Development', model: 'gpt-4o-mini', provider: 'OpenAI', status: 'error', progress: 12, started: '10:28:00', duration: 3, cost: 0.01 },
];

export default function ModelRunnerPage() {
  const [models] = useState<ModelRunner[]>(runners);
  const [filter, setFilter] = useState<string>('all');

  const filtered = filter === 'all' ? models : models.filter(m => m.status === filter);
  const running = models.filter(m => m.status === 'running').length;
  const totalCost = models.reduce((a, m) => a + m.cost, 0);

  return (
    <div style={{ padding: 24, background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <h1 style={{ fontSize: 24, marginBottom: 20 }}>Model Runner</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#58A6FF' }}>{running}</div>
          <div style={{ color: '#8C8C8C' }}>Running</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#10B981' }}>{models.filter(m => m.status === 'completed').length}</div>
          <div style={{ color: '#8C8C8C' }}>Completed</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#F85149' }}>{models.filter(m => m.status === 'error').length}</div>
          <div style={{ color: '#8C8C8C' }}>Errors</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#D29922' }}>${totalCost.toFixed(2)}</div>
          <div style={{ color: '#8C8C8C' }}>Total Cost</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        {['all', 'running', 'completed', 'error', 'idle'].map(s => (
          <button key={s} onClick={() => setFilter(s)} style={{
            padding: '8px 16px', background: filter === s ? '#238636' : '#21262D',
            border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer', textTransform: 'capitalize'
          }}>
            {s}
          </button>
        ))}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {filtered.map(m => (
          <div key={m.id} style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <strong>{m.name}</strong>
              <span style={{ color: m.status === 'running' ? '#58A6FF' : m.status === 'completed' ? '#10B981' : m.status === 'error' ? '#F85149' : '#8C8C8C' }}>
                {m.status}
              </span>
            </div>
            <p style={{ color: '#8C8C8C', fontSize: 12 }}>{m.model} · {m.provider}</p>
            {m.status === 'running' && (
              <div style={{ marginTop: 8, height: 6, background: '#30363D', borderRadius: 3, overflow: 'hidden' }}>
                <div style={{ width: m.progress + '%', height: '100%', background: '#238636', transition: 'width 0.3s' }} />
              </div>
            )}
            <div style={{ display: 'flex', gap: 16, fontSize: 12, color: '#8C8C8C', marginTop: 8 }}>
              <span>⏱ {m.duration}s</span>
              <span>${m.cost.toFixed(2)}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}