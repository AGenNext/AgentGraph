'use client';

import { useState } from 'react';

interface Guardrail {
  id: string;
  name: string;
  type: 'content' | 'input' | 'output' | 'context';
  status: 'active' | 'draft';
  action: 'block' | 'warn' | 'audit';
  description: string;
}

const guardrails: Guardrail[] = [
  { id: '1', name: 'PII Detection', type: 'output', status: 'active', action: 'block', description: 'Block output containing personal identifiers' },
  { id: '2', name: 'Profanity Filter', type: 'content', status: 'active', action: 'block', description: 'Filter profanity and inappropriate content' },
  { id: '3', name: 'Injection Prevention', type: 'input', status: 'active', action: 'block', description: 'Detect and block prompt injection attempts' },
  { id: '4', name: 'Sensitive Data', type: 'input', status: 'active', action: 'warn', description: 'Warn on sensitive data in input' },
  { id: '5', name: 'Toxicity Detection', type: 'content', status: 'active', action: 'block', description: 'Detect toxic/harmful content' },
  { id: '6', name: 'Code Execution', type: 'output', status: 'draft', action: 'audit', description: 'Audit code execution in outputs' },
];

export default function GuardrailsPage() {
  const [filter, setFilter] = useState('all');
  const filtered = filter === 'all' ? guardrails : guardrails.filter(g => g.status === filter);

  return (
    <div style={{ padding: 24 }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 24 }}>AI Guardrails</h1>
      <div style={{ marginBottom: 16, display: 'flex', gap: 8 }}>
        {['all', 'active', 'draft'].map(s => (
          <button key={s} onClick={() => setFilter(s)}
            style={{ padding: '8px 16px', borderRadius: 4, border: '1px solid #E5E5E5', background: filter === s ? '#1A1A2E' : '#fff', color: filter === s ? '#fff' : '#000', cursor: 'pointer' }}>
            {s.charAt(0).toUpperCase() + s.slice(1)}
          </button>
        ))}
      </div>
      <table style={{ width: '100%', borderCollapse: 'collapse', background: '#fff' }}>
        <thead>
          <tr style={{ background: '#F4F4F4' }}>
            <th style={{ padding: 12, textAlign: 'left' }}>Guardrail</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Type</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Status</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Action</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Description</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(item => (
            <tr key={item.id} style={{ borderBottom: '1px solid #E5E5E5' }}>
              <td style={{ padding: 12, fontWeight: 500 }}>{item.name}</td>
              <td style={{ padding: 12 }}>{item.type}</td>
              <td style={{ padding: 12, color: item.status === 'active' ? '#10B981' : '#F59E0B' }}>{item.status}</td>
              <td style={{ padding: 12, color: item.action === 'block' ? '#DA1E28' : item.action === 'warn' ? '#F59E0B' : '#0F62FE' }}>{item.action.toUpperCase()}</td>
              <td style={{ padding: 12, fontSize: 12, color: '#666' }}>{item.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}