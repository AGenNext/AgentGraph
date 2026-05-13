'use client';

import { useState } from 'react';

interface Identity {
  id: string;
  name: string;
  email: string;
  role: string;
  department: string;
  status: 'active' | 'pending' | 'suspended';
  created: string;
  lastLogin: string;
}

const identities: Identity[] = [
  { id: '1', name: 'John Doe', email: 'john@company.com', role: 'Admin', department: 'IT', status: 'active', created: '2024-01-01', lastLogin: '2024-02-01' },
  { id: '2', name: 'Jane Smith', email: 'jane@company.com', role: 'Developer', department: 'Engineering', status: 'active', created: '2024-01-15', lastLogin: '2024-02-01' },
  { id: '3', name: 'Bob Wilson', email: 'bob@company.com', role: 'Viewer', department: 'Finance', status: 'pending', created: '2024-01-20', lastLogin: '-' },
  { id: '4', name: 'Alice Brown', email: 'alice@company.com', role: 'Operator', department: 'Operations', status: 'suspended', created: '2023-12-01', lastLogin: '2024-01-15' },
];

export default function IdentityPage() {
  const [filter, setFilter] = useState('all');

  const filtered = filter === 'all' ? identities : identities.filter(i => i.status === filter);

  return (
    <div style={{ padding: 24 }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 24 }}>Identity Management</h1>
      
      <div style={{ marginBottom: 16, display: 'flex', gap: 8 }}>
        {['all', 'active', 'pending', 'suspended'].map(s => (
          <button key={s} onClick={() => setFilter(s)}
            style={{ padding: '8px 16px', borderRadius: 4, border: '1px solid #E5E5E5', background: filter === s ? '#1A1A2E' : '#fff', color: filter === s ? '#fff' : '#000', cursor: 'pointer' }}>
            {s.charAt(0).toUpperCase() + s.slice(1)}
          </button>
        ))}
      </div>

      <table style={{ width: '100%', borderCollapse: 'collapse', background: '#fff' }}>
        <thead>
          <tr style={{ background: '#F4F4F4' }}>
            <th style={{ padding: 12, textAlign: 'left' }}>Name</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Email</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Role</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Department</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Status</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Created</th>
            <th style={{ padding: 12, textAlign: 'left' }}>Last Login</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(item => (
            <tr key={item.id} style={{ borderBottom: '1px solid #E5E5E5' }}>
              <td style={{ padding: 12 }}>{item.name}</td>
              <td style={{ padding: 12 }}>{item.email}</td>
              <td style={{ padding: 12 }}>{item.role}</td>
              <td style={{ padding: 12 }}>{item.department}</td>
              <td style={{ padding: 12, color: item.status === 'active' ? '#10B981' : item.status === 'pending' ? '#F59E0B' : '#DA1E28' }}>
                {item.status}
              </td>
              <td style={{ padding: 12 }}>{item.created}</td>
              <td style={{ padding: 12 }}>{item.lastLogin}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}