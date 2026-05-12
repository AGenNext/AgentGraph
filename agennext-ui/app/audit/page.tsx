'use client';

import { useState } from 'react';

interface AuditLog {
  id: string;
  action: string;
  user: string;
  resource: string;
  details: string;
  timestamp: string;
  ip: string;
  status: 'success' | 'failed';
}

const logs: AuditLog[] = [
  { id: 'a1', action: 'agent.create', user: 'john.doe@company.com', resource: 'Research Agent v2', details: 'Created new agent', timestamp: '2024-02-01 10:30:00', ip: '192.168.1.100', status: 'success' },
  { id: 'a2', action: 'agent.execute', user: 'jane.smith@company.com', resource: 'Analyzer Agent', details: 'Executed workflow', timestamp: '2024-02-01 10:25:00', ip: '192.168.1.101', status: 'success' },
  { id: 'a3', action: 'integration.connect', user: 'admin@company.com', resource: 'AWS Bedrock', details: 'Connected integration', timestamp: '2024-02-01 10:00:00', ip: '192.168.1.50', status: 'success' },
  { id: 'a4', action: 'user.login', user: 'unknown', resource: '-', details: 'Failed login attempt', timestamp: '2024-02-01 09:45:00', ip: '10.0.0.55', status: 'failed' },
  { id: 'a5', action: 'agent.delete', user: 'john.doe@company.com', resource: 'Legacy Agent', details: 'Deleted agent', timestamp: '2024-02-01 09:30:00', ip: '192.168.1.100', status: 'success' },
  { id: 'a6', action: 'user.rolechange', user: 'admin@company.com', resource: 'jane.smith', details: 'Changed role to admin', timestamp: '2024-02-01 09:00:00', ip: '192.168.1.50', status: 'success' },
];

export default function AuditPage() {
  const [search, setSearch] = useState('');
  
  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>Audit Logs</h1>
          <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Full activity tracking & compliance logs</p>
        </div>
        <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 6, fontSize: 13, cursor: 'pointer' }}>
          Export Logs
        </button>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{logs.length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Events (24h)</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{logs.filter(l => l.status === 'success').length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Successful</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#DA1E28' }}>{logs.filter(l => l.status === 'failed').length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Failed</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>4</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Unique Users</div>
        </div>
      </div>

      {/* Filters */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
        <input
          placeholder="Search logs..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{ flex: 1, padding: '10px 14px', borderRadius: 6, border: '1px solid #E5E5E5', maxWidth: 300, fontSize: 13 }}
        />
        <select style={{ padding: '10px 14px', borderRadius: 6, border: '1px solid #E5E5E5', background: '#fff' }}>
          <option>All Actions</option>
          <option>agent.*</option>
          <option>user.*</option>
          <option>integration.*</option>
        </select>
        <input type="date" style={{ padding: '10px 14px', borderRadius: 6, border: '1px solid #E5E5E5' }} />
      </div>

      {/* Logs */}
      <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#F8F9FA' }}>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>TIMESTAMP</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>ACTION</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>USER</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>RESOURCE</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>DETAILS</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>IP</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>STATUS</th>
            </tr>
          </thead>
          <tbody>
            {logs.map(log => (
              <tr key={log.id} style={{ borderTop: '1px solid #F4F4F4' }}>
                <td style={{ padding: '14px 16px', fontSize: 12, fontFamily: 'monospace' }}>{log.timestamp}</td>
                <td style={{ padding: '14px 16px', fontSize: 12, fontWeight: 500, fontFamily: 'monospace' }}>{log.action}</td>
                <td style={{ padding: '14px 16px', fontSize: 12 }}>{log.user}</td>
                <td style={{ padding: '14px 16px', fontSize: 12 }}>{log.resource}</td>
                <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280' }}>{log.details}</td>
                <td style={{ padding: '14px 16px', fontSize: 12, fontFamily: 'monospace', color: '#6B7280' }}>{log.ip}</td>
                <td style={{ padding: '14px 16px' }}>
                  <span style={{ color: log.status === 'success' ? '#10B981' : '#DA1E28', fontSize: 12, fontWeight: 500 }}>
                    {log.status === 'success' ? '✓' : '✗'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}