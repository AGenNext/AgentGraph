'use client';

import { useState } from 'react';

interface Workspace {
  id: string;
  name: string;
  description: string;
  agents: number;
  lastActive: string;
  status: 'active' | 'archived';
}

const mockWorkspaces: Workspace[] = [
  { id: 'w1', name: 'Production', description: 'Production agents', agents: 5, lastActive: '2024-02-01', status: 'active' },
  { id: 'w2', name: 'Development', description: 'Testing new agents', agents: 3, lastActive: '2024-02-01', status: 'active' },
  { id: 'w3', name: 'Staging', description: 'Pre-production', agents: 2, lastActive: '2024-01-28', status: 'active' },
  { id: 'w4', name: 'Archive', description: 'Old projects', agents: 0, lastActive: '2024-01-01', status: 'archived' },
];

export default function WorkspacesPage() {
  const [workspaces] = useState<Workspace[]>(mockWorkspaces);

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F4F4F4', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600 }}>Workspaces</h1>
          <p style={{ color: '#525252' }}>Organize your agents by workspace</p>
        </div>
        <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 4, cursor: 'pointer' }}>
          + New Workspace
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{workspaces.filter(w => w.status === 'active').length}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Active Workspaces</div>
        </div>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{workspaces.reduce((a, w) => a + w.agents, 0)}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Total Agents</div>
        </div>
      </div>

      <div style={{ background: '#fff', borderRadius: 4 }}>
        {workspaces.map(ws => (
          <div key={ws.id} style={{ padding: 16, borderBottom: '1px solid #E5E5E5', cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <div style={{ fontWeight: 600, fontSize: 16 }}>{ws.name}</div>
              <div style={{ fontSize: 12, color: '#525252' }}>{ws.description}</div>
              <div style={{ fontSize: 11, color: '#8C8C8C', marginTop: 4 }}>{ws.agents} agents • Last active {ws.lastActive}</div>
            </div>
            <span style={{ 
              background: ws.status === 'active' ? '#10B98120' : '#E5E5E5', 
              color: ws.status === 'active' ? '#10B981' : '#525252',
              padding: '4px 12px', 
              borderRadius: 999, 
              fontSize: 12 
            }}>
              {ws.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}