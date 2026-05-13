'use client';

import { useState } from 'react';

interface AuditLog {
  id: string;
  action: string;
  resource: string;
  user: string;
  ip: string;
  timestamp: string;
  result: 'success' | 'failure';
  details: string;
}

const logs: AuditLog[] = [
  { id: '1', action: 'LOGIN', resource: 'Dashboard', user: 'admin@company.com', ip: '192.168.1.1', timestamp: '2024-02-01 10:00:00', result: 'success', details: 'SSO authentication' },
  { id: '2', action: 'CREATE', resource: 'Agent', user: 'john@company.com', ip: '192.168.1.5', timestamp: '2024-02-01 09:45:00', result: 'success', details: 'Created Sales-Agent v2.1' },
  { id: '3', action: 'UPDATE', resource: 'Config', user: 'admin@company.com', ip: '192.168.1.1', timestamp: '2024-02-01 09:30:00', result: 'success', details: 'Updated security policy' },
  { id: '4', action: 'DELETE', resource: 'Agent', user: 'bob@company.com', ip: '192.168.1.10', timestamp: '2024-02-01 09:15:00', result: 'failure', details: 'Permission denied' },
  { id: '5', action: 'EXPORT', resource: 'Data', user: 'jane@company.com', ip: '192.168.1.8', timestamp: '2024-02-01 09:00:00', result: 'success', details: 'Exported Q4 report' },
  { id: '6', action: 'LOGIN', resource: 'Dashboard', user: 'test@company.com', ip: '10.0.0.55', timestamp: '2024-02-01 08:45:00', result: 'failure', details: 'Invalid credentials' },
];

export default function AuditPage() {
  const [filter, setFilter] = useState('all');

  const filtered = filter === 'all' ? logs : logs.filter(l => l.result === filter);

  return (
    <div style={{ padding: 24 }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 24 }}>Audit Log</h1>
      
      <div style={{ marginBottom: 16, display: 'flex', gap: 8 }}>
        {['all', 'success', 'failure'].map(s => (
          <button key={s} onClick={() => setFilter(s)}
            style={{ padding: '8px 16px', borderRadius: 4, border: '1px solid #E5E5E5', background: filter === s ? '#1A1A2E' : '#fff', color: filter === s ? '#fff' : '#000', cursor: 'pointer' }}>
            {s.charAt(0).toUpperCase() + s.slice(1)}
          </button>
        ))}
      </div>

      <table style={{ width: '100%', borderCollapse: 'collapse', background: '#fff' }}>
        <thead>
          <tr style={{ background: '#F4F4F4' }}>
            <th style={{ padding: 12, textAlign: 'left' }}>Action</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Resource</th>
            <th style={{ padding: 12, textAlign: 'left' }}>User</th>
            <th style={{ padding: 12, textAlign: 'left' }}>IP</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Timestamp</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Result</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Details</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(item => (
            <tr key={item.id} style={{ borderBottom: '1px solid #E5E5E5' }}>
              <td style={{ padding: 12, fontWeight: 500 }}>{item.action}</td>
              <td style={{ padding: 12 }}>{item.resource}</td>
              <td style={{ padding: 12 }}>{item.user}</td>
              <td style={{ padding: 12, fontFamily: 'monospace', fontSize: 12 }}>{item.ip}</td>
              <td style={{ padding: 12, fontSize: 12 }}>{item.timestamp}</td>
              <td style={{ padding: 12, color: item.result === 'success' ? '#10B981' : '#DA1E28' }}>
                {item.result}
              </td>
              <td style={{ padding: 12, fontSize: 12, color: '#666' }}>{item.details}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}