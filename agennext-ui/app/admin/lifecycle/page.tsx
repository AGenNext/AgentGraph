'use client';

import { useState } from 'react';

interface LifecycleEvent {
  id: string;
  agent: string;
  action: 'created' | 'updated' | 'deployed' | 'archived' | 'deleted';
  version: string;
  user: string;
  timestamp: string;
  status: 'completed' | 'in_progress' | 'failed';
}

const events: LifecycleEvent[] = [
  { id: '1', agent: 'Sales-Agent', action: 'deployed', version: '2.1', user: 'john@company.com', timestamp: '2024-02-01 10:00', status: 'completed' },
  { id: '2', agent: 'Support-Agent', action: 'updated', version: '1.5', user: 'jane@company.com', timestamp: '2024-02-01 09:30', status: 'completed' },
  { id: '3', agent: 'Research-Agent', action: 'created', version: '1.0', user: 'john@company.com', timestamp: '2024-02-01 09:00', status: 'completed' },
  { id: '4', agent: 'Legacy-Agent', action: 'archived', version: '0.9', user: 'admin@company.com', timestamp: '2024-01-31 18:00', status: 'completed' },
  { id: '5', agent: 'Dev-Agent', action: 'updated', version: '3.2', user: 'bob@company.com', timestamp: '2024-02-01 11:00', status: 'in_progress' },
  { id: '6', agent: 'Test-Agent', action: 'deleted', version: '0.5', user: 'admin@company.com', timestamp: '2024-01-30 12:00', status: 'failed' },
];

export default function LifecyclePage() {
  const [filter, setFilter] = useState('all');

  const filtered = filter === 'all' ? events : events.filter(e => e.status === filter);

  return (
    <div style={{ padding: 24 }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 24 }}>Agent Lifecycle</h1>
      
      <div style={{ marginBottom: 16, display: 'flex', gap: 8 }}>
        {['all', 'completed', 'in_progress', 'failed'].map(s => (
          <button key={s} onClick={() => setFilter(s)}
            style={{ padding: '8px 16px', borderRadius: 4, border: '1px solid #E5E5E5', background: filter === s ? '#1A1A2E' : '#fff', color: filter === s ? '#fff' : '#000', cursor: 'pointer' }}>
            {s === 'in_progress' ? 'In Progress' : s.charAt(0).toUpperCase() + s.slice(1)}
          </button>
        ))}
      </div>

      <table style={{ width: '100%', borderCollapse: 'collapse', background: '#fff' }}>
        <thead>
          <tr style={{ background: '#F4F4F4' }}>
            <th style={{ padding: 12, textAlign: 'left' }}>Agent</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Action</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Version</th>
            <th style={{ padding: 12, textAlign: 'left' }}>User</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Timestamp</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Status</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(item => (
            <tr key={item.id} style={{ borderBottom: '1px solid #E5E5E5' }}>
              <td style={{ padding: 12, fontWeight: 500 }}>{item.agent}</td>
              <td style={{ padding: 12 }}>{item.action}</td>
              <td style={{ padding: 12, fontFamily: 'monospace' }}>{item.version}</td>
              <td style={{ padding: 12 }}>{item.user}</td>
              <td style={{ padding: 12 }}>{item.timestamp}</td>
              <td style={{ padding: 12, color: item.status === 'completed' ? '#10B981' : item.status === 'in_progress' ? '#0F62FE' : '#DA1E28' }}>
                {item.status === 'in_progress' ? 'In Progress' : item.status}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}