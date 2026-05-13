'use client';

import { useState } from 'react';

interface ModelEndpoint {
  id: string;
  provider: string;
  model: string;
  endpoint: string;
  status: 'available' | 'busy' | 'offline';
  latency: number;
  rpm: number;
}

const endpoints: ModelEndpoint[] = [
  { id: '1', provider: 'OpenAI', model: 'gpt-4o', endpoint: 'api.openai.com/v1', status: 'available', latency: 450, rpm: 500 },
  { id: '2', provider: 'OpenAI', model: 'gpt-4o-mini', endpoint: 'api.openai.com/v1', status: 'available', latency: 200, rpm: 1500 },
  { id: '3', provider: 'Anthropic', model: 'claude-3-opus', endpoint: 'api.anthropic.com', status: 'busy', latency: 800, rpm: 50 },
  { id: '4', provider: 'Anthropic', model: 'claude-3-sonnet', endpoint: 'api.anthropic.com', status: 'available', latency: 350, rpm: 100 },
  { id: '5', provider: 'Google', model: 'gemini-2.0-flash', endpoint: 'generativelanguage.googleapis.com', status: 'available', latency: 180, rpm: 1000 },
  { id: '6', provider: 'Azure', model: 'gpt-4', endpoint: 'openai.azure.com', status: 'available', latency: 400, rpm: 200 },
];

export default function ModelGatewayPage() {
  const [models] = useState<ModelEndpoint[]>(endpoints);
  const [provider, setProvider] = useState<string>('all');

  const filtered = provider === 'all' ? models : models.filter(m => m.provider === provider);
  const available = models.filter(m => m.status === 'available').length;

  return (
    <div style={{ padding: 24, background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <h1 style={{ fontSize: 24, marginBottom: 20 }}>Model Gateway</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#10B981' }}>{available}</div>
          <div style={{ color: '#8C8C8C' }}>Available</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#D29922' }}>{models.length}</div>
          <div style={{ color: '#8C8C8C' }}>Total Models</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#58A6FF' }}>{Math.round(models.reduce((a,m) => a + m.rpm, 0)/1000)}k</div>
          <div style={{ color: '#8C8C8C' }}>Combined RPM</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        {['all', 'OpenAI', 'Anthropic', 'Google', 'Azure'].map(p => (
          <button key={p} onClick={() => setProvider(p)} style={{
            padding: '8px 16px', background: provider === p ? '#238636' : '#21262D',
            border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer'
          }}>
            {p}
          </button>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
        {filtered.map(m => (
          <div key={m.id} style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <strong>{m.model}</strong>
              <span style={{ color: m.status === 'available' ? '#10B981' : m.status === 'busy' ? '#D29922' : '#F85149' }}>
                {m.status}
              </span>
            </div>
            <p style={{ color: '#8C8C8C', fontSize: 12 }}>{m.provider}</p>
            <div style={{ display: 'flex', gap: 12, fontSize: 12, color: '#8C8C8C', marginTop: 8 }}>
              <span>⏱ {m.latency}ms</span>
              <span>⚡ {m.rpm} RPM</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}