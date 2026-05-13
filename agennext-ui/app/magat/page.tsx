'use client';

import { useState } from 'react';

interface GovernancePolicy {
  id: string;
  name: string;
  category: 'safety' | 'compliance' | 'audit' | 'access';
  severity: 'critical' | 'high' | 'medium' | 'low';
  status: 'enforced' | 'disabled' | 'audit';
  lastChecked: string;
}

const policies: GovernancePolicy[] = [
  { id: '1', name: 'Prompt Injection Shield', category: 'safety', severity: 'critical', status: 'enforced', lastChecked: '2m ago' },
  { id: '2', name: 'PII Redaction', category: 'safety', severity: 'critical', status: 'enforced', lastChecked: '5m ago' },
  { id: '3', name: 'Azure RBAC Sync', category: 'access', severity: 'high', status: 'enforced', lastChecked: '10m ago' },
  { id: '4', name: 'Data Residency', category: 'compliance', severity: 'high', status: 'audit', lastChecked: '1h ago' },
  { id: '5', name: 'Audit Logging', category: 'audit', severity: 'medium', status: 'enforced', lastChecked: '1m ago' },
  { id: '6', name: 'API Rate Limiting', category: 'access', severity: 'medium', status: 'enforced', lastChecked: '3m ago' },
  { id: '7', name: 'Content Filtering', category: 'safety', severity: 'high', status: 'disabled', lastChecked: '24h ago' },
  { id: '8', name: 'GDPR Compliance', category: 'compliance', severity: 'critical', status: 'enforced', lastChecked: '2h ago' },
];

export default function MagatPage() {
  const [policys] = useState<GovernancePolicy[]>(policies);
  const [category, setCategory] = useState<string>('all');

  const filtered = category === 'all' ? policys : policys.filter(p => p.category === category);
  const enforced = policys.filter(p => p.status === 'enforced').length;
  const critical = policys.filter(p => p.severity === 'critical').length;

  return (
    <div style={{ padding: 24, background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <h1 style={{ fontSize: 24, marginBottom: 8 }}>Microsoft Agent Governance Toolkit</h1>
      <p style={{ color: '#8C8C8C', marginBottom: 20 }}>Enterprise-ready agent guardrails & compliance</p>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#10B981' }}>{enforced}</div>
          <div style={{ color: '#8C8C8C' }}>Enforced</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#F85149' }}>{critical}</div>
          <div style={{ color: '#8C8C8C' }}>Critical</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#D29922' }}>{policys.filter(p => p.category === 'compliance').length}</div>
          <div style={{ color: '#8C8C8C' }}>Compliance</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#58A6FF' }}>{policys.length}</div>
          <div style={{ color: '#8C8C8C' }}>Total Policies</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        {['all', 'safety', 'compliance', 'access', 'audit'].map(c => (
          <button key={c} onClick={() => setCategory(c)} style={{
            padding: '8px 16px', background: category === c ? '#238636' : '#21262D',
            border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer', textTransform: 'capitalize'
          }}>
            {c}
          </button>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
        {filtered.map(p => (
          <div key={p.id} style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <strong>{p.name}</strong>
              <span style={{ fontSize: 12, color: p.status === 'enforced' ? '#10B981' : p.status === 'audit' ? '#D29922' : '#8C8C8C' }}>
                {p.status}
              </span>
            </div>
            <div style={{ display: 'flex', gap: 8, fontSize: 12 }}>
              <span style={{ padding: '2px 8px', background: '#30363D', borderRadius: 4, color: '#8C8C8C' }}>{p.category}</span>
              <span style={{ padding: '2px 8px', borderRadius: 4, 
                background: p.severity === 'critical' ? '#F8514933' : p.severity === 'high' ? '#D2992233' : '#30363D',
                color: p.severity === 'critical' ? '#F85149' : p.severity === 'high' ? '#D29922' : '#8C8C8C'
              }}>{p.severity}</span>
            </div>
            <p style={{ fontSize: 12, color: '#8C8C8C', marginTop: 8 }}>Checked: {p.lastChecked}</p>
          </div>
        ))}
      </div>
    </div>
  );
}