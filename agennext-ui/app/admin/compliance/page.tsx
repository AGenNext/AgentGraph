'use client';

import { useState } from 'react';

interface ComplianceCheck {
  id: string;
  name: string;
  category: string;
  status: 'pass' | 'fail' | 'warning' | 'pending';
  lastRun: string;
  description: string;
}

const checks: ComplianceCheck[] = [
  { id: '1', name: 'SSO Enforcement', category: 'Security', status: 'pass', lastRun: '2024-02-01 10:00', description: 'All users authenticated via SSO' },
  { id: '2', name: 'MFA Enabled', category: 'Security', status: 'pass', lastRun: '2024-02-01 10:00', description: 'MFA required for all admin users' },
  { id: '3', name: 'Audit Logging', category: 'Compliance', status: 'pass', lastRun: '2024-02-01 10:00', description: 'All admin actions logged' },
  { id: '4', name: 'Data Encryption', category: 'Data', status: 'warning', lastRun: '2024-02-01 10:00', description: 'Some logs not encrypted at rest' },
  { id: '5', name: 'Access Review', category: 'Access', status: 'fail', lastRun: '2024-02-01 10:00', description: 'Quarterly access review overdue' },
  { id: '6', name: 'Agent Approval', category: 'Governance', status: 'pass', lastRun: '2024-02-01 10:00', description: 'New agents require approval' },
];

export default function CompliancePage() {
  const [category, setCategory] = useState('all');
  const filtered = category === 'all' ? checks : checks.filter(c => c.category === category);

  return (
    <div style={{ padding: 24 }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 24 }}>Compliance Automation</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>4</div>
          <div style={{ fontSize: 12 }}>Pass</div>
        </div>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#F59E0B' }}>1</div>
          <div style={{ fontSize: 12 }}>Warning</div>
        </div>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#DA1E28' }}>1</div>
          <div style={{ fontSize: 12 }}>Fail</div>
        </div>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#8C8C8C' }}>0</div>
          <div style={{ fontSize: 12 }}>Pending</div>
        </div>
      </div>

      <div style={{ marginBottom: 16, display: 'flex', gap: 8 }}>
        {['all', 'Security', 'Compliance', 'Data', 'Access', 'Governance'].map(c => (
          <button key={c} onClick={() => setCategory(c)}
            style={{ padding: '8px 16px', borderRadius: 4, border: '1px solid #E5E5E5', background: category === c ? '#1A1A2E' : '#fff', color: category === c ? '#fff' : '#000', cursor: 'pointer' }}>
            {c === 'all' ? 'All' : c}
          </button>
        ))}
      </div>

      <table style={{ width: '100%', borderCollapse: 'collapse', background: '#fff' }}>
        <thead>
          <tr style={{ background: '#F4F4F4' }}>
            <th style={{ padding: 12, textAlign: 'left' }}>Check</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Category</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Status</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Last Run</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Description</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(item => (
            <tr key={item.id} style={{ borderBottom: '1px solid #E5E5E5' }}>
              <td style={{ padding: 12, fontWeight: 500 }}>{item.name}</td>
              <td style={{ padding: 12 }}>{item.category}</td>
              <td style={{ padding: 12, color: item.status === 'pass' ? '#10B981' : item.status === 'warning' ? '#F59E0B' : item.status === 'fail' ? '#DA1E28' : '#8C8C8C' }}>
                {item.status.toUpperCase()}
              </td>
              <td style={{ padding: 12, fontSize: 12 }}>{item.lastRun}</td>
              <td style={{ padding: 12, fontSize: 12, color: '#666' }}>{item.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}