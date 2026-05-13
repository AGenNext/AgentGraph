'use client';

import { useState } from 'react';

interface GuardRule {
  id: string;
  name: string;
  type: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  status: 'active' | 'inactive';
  lastTriggered: string;
}

const initialRules: GuardRule[] = [
  { id: '1', name: 'Prompt Injection', type: 'security', severity: 'critical', status: 'active', lastTriggered: '2h ago' },
  { id: '2', name: 'Data Exfiltration', type: 'security', severity: 'critical', status: 'active', lastTriggered: '5h ago' },
  { id: '3', name: 'Unauthorized API', type: 'access', severity: 'high', status: 'active', lastTriggered: '1d ago' },
  { id: '4', name: 'Rate Limit', type: 'throttle', severity: 'medium', status: 'active', lastTriggered: '30m ago' },
  { id: '5', name: 'Content Filter', type: 'content', severity: 'low', status: 'active', lastTriggered: '12h ago' },
  { id: '6', name: 'PII Detection', type: 'privacy', severity: 'high', status: 'inactive', lastTriggered: 'Never' },
];

export default function AgentSafePage() {
  const [rules] = useState<GuardRule[]>(initialRules);
  const [status, setStatus] = useState<string>('all');

  const filtered = status === 'all' ? rules : rules.filter(r => r.status === status);
  const active = rules.filter(r => r.status === 'active').length;
  const critical = rules.filter(r => r.severity === 'critical').length;

  return (
    <div style={{ padding: 24, background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <h1 style={{ fontSize: 24, marginBottom: 20 }}>Agent Safety & Guardrails</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#10B981' }}>{active}</div>
          <div style={{ color: '#8C8C8C' }}>Active Guards</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#F85149' }}>{critical}</div>
          <div style={{ color: '#8C8C8C' }}>Critical</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#D29922' }}>{rules.length}</div>
          <div style={{ color: '#8C8C8C' }}>Total Rules</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        {['all', 'active', 'inactive'].map(s => (
          <button key={s} onClick={() => setStatus(s)} style={{
            padding: '8px 16px', background: status === s ? '#238636' : '#21262D',
            border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer', textTransform: 'capitalize'
          }}>
            {s}
          </button>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
        {filtered.map(rule => (
          <div key={rule.id} style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <strong>{rule.name}</strong>
              <span style={{ fontSize: 12, color: rule.status === 'active' ? '#10B981' : '#8C8C8C' }}>{rule.status}</span>
            </div>
            <div style={{ display: 'flex', gap: 8, fontSize: 12, color: '#8C8C8C' }}>
              <span style={{ padding: '2px 8px', background: '#30363D', borderRadius: 4 }}>{rule.type}</span>
              <span style={{ padding: '2px 8px', borderRadius: 4, 
                background: rule.severity === 'critical' ? '#F8514933' : rule.severity === 'high' ? '#D2992233' : '#30363D',
                color: rule.severity === 'critical' ? '#F85149' : rule.severity === 'high' ? '#D29922' : '#8C8C8C'
              }}>{rule.severity}</span>
            </div>
            <p style={{ fontSize: 12, color: '#8C8C8C', marginTop: 8 }}>Last triggered: {rule.lastTriggered}</p>
          </div>
        ))}
      </div>
    </div>
  );
}