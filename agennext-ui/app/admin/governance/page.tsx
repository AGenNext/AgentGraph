'use client';

import { useState } from 'react';

interface Role {
  id: string;
  name: string;
  permissions: string[];
  users: number;
  description: string;
}

interface Policy {
  id: string;
  name: string;
  effect: 'allow' | 'deny';
  resource: string;
  action: string;
  condition: string;
}

const roles: Role[] = [
  { id: '1', name: 'Admin', permissions: ['*'], users: 3, description: 'Full system access' },
  { id: '2', name: 'Developer', permissions: ['agent:*', 'task:*', 'deploy:*'], users: 12, description: 'Can manage agents and tasks' },
  { id: '3', name: 'Operator', permissions: ['task:run', 'task:view'], users: 25, description: 'Can run predefined tasks' },
  { id: '4', name: 'Viewer', permissions: ['*:view'], users: 50, description: 'Read-only access' },
];

const policies: Policy[] = [
  { id: '1', name: 'Admin Access', effect: 'allow', resource: '*', action: '*', condition: 'role=Admin' },
  { id: '2', name: 'Dev Deploy', effect: 'allow', resource: 'agent:*', action: 'deploy', condition: 'role=Developer' },
  { id: '3', name: 'Task Execute', effect: 'allow', resource: 'task:*', action: 'run', condition: 'role=Operator' },
  { id: '4', name: 'Deny Delete', effect: 'deny', resource: 'agent:*', action: 'delete', condition: 'NOT role=Admin' },
];

export default function GovernancePage() {
  const [tab, setTab] = useState<'roles' | 'policies'>('roles');

  return (
    <div style={{ padding: 24 }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 24 }}>Access Governance (RBAC)</h1>
      
      <div style={{ marginBottom: 16, display: 'flex', gap: 8 }}>
        <button onClick={() => setTab('roles')}
          style={{ padding: '8px 16px', borderRadius: 4, border: '1px solid #E5E5E5', background: tab === 'roles' ? '#1A1A2E' : '#fff', color: tab === 'roles' ? '#fff' : '#000', cursor: 'pointer' }}>
          Roles
        </button>
        <button onClick={() => setTab('policies')}
          style={{ padding: '8px 16px', borderRadius: 4, border: '1px solid #E5E5E5', background: tab === 'policies' ? '#1A1A2E' : '#fff', color: tab === 'policies' ? '#fff' : '#000', cursor: 'pointer' }}>
          Policies
        </button>
      </div>

      {tab === 'roles' ? (
        <table style={{ width: '100%', borderCollapse: 'collapse', background: '#fff' }}>
          <thead>
            <tr style={{ background: '#F4F4F4' }}>
              <th style={{ padding: 12, textAlign: 'left' }}>Role</th>
              <th style={{ padding: 12, textAlign: 'left' }}>Permissions</th>
              <th style={{ padding: 12, textAlign: 'left' }}>Users</th>
              <th style={{ padding: 12, textAlign: 'left' }}>Description</th>
            </tr>
          </thead>
          <tbody>
            {roles.map(item => (
              <tr key={item.id} style={{ borderBottom: '1px solid #E5E5E5' }}>
                <td style={{ padding: 12, fontWeight: 500 }}>{item.name}</td>
                <td style={{ padding: 12, fontFamily: 'monospace', fontSize: 12 }}>{item.permissions.join(', ')}</td>
                <td style={{ padding: 12 }}>{item.users}</td>
                <td style={{ padding: 12, fontSize: 12, color: '#666' }}>{item.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse', background: '#fff' }}>
          <thead>
            <tr style={{ background: '#F4F4F4' }}>
              <th style={{ padding: 12, textAlign: 'left' }}>Policy</th>
              <th style={{ padding: 12, textAlign: 'left' }}>Effect</th>
              <th style={{ padding: 12, textAlign: 'left' }}>Resource</th>
              <th style={{ padding: 12, textAlign: 'left' }}>Action</th>
              <th style={{ padding: 12, textAlign: 'left' }}>Condition</th>
            </tr>
          </thead>
          <tbody>
            {policies.map(item => (
              <tr key={item.id} style={{ borderBottom: '1px solid #E5E5E5' }}>
                <td style={{ padding: 12, fontWeight: 500 }}>{item.name}</td>
                <td style={{ padding: 12, color: item.effect === 'allow' ? '#10B981' : '#DA1E28' }}>{item.effect}</td>
                <td style={{ padding: 12, fontFamily: 'monospace', fontSize: 12 }}>{item.resource}</td>
                <td style={{ padding: 12, fontFamily: 'monospace', fontSize: 12 }}>{item.action}</td>
                <td style={{ padding: 12, fontSize: 12 }}>{item.condition}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}