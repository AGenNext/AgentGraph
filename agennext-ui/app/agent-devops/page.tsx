'use client';

import { useState } from 'react';

interface DevOpsAgent {
  id: string;
  name: string;
  role: string;
  status: 'idle' | 'running' | 'completed';
  tasks: number;
  success: number;
}

const agents: DevOpsAgent[] = [
  { id: '1', name: 'CI Builder', role: 'build', status: 'running', tasks: 156, success: 98 },
  { id: '2', name: 'Test Runner', role: 'test', status: 'running', tasks: 89, success: 95 },
  { id: '3', name: 'Deploy Bot', role: 'deploy', status: 'completed', tasks: 45, success: 100 },
  { id: '4', name: 'Monitor Pro', role: 'monitor', status: 'running', tasks: 234, success: 99 },
  { id: '5', name: 'Security Scan', role: 'security', status: 'idle', tasks: 12, success: 92 },
  { id: '6', name: 'Infra Manager', role: 'infrastructure', status: 'completed', tasks: 28, success: 97 },
];

export default function AgentDevOpsPage() {
  const [filter, setFilter] = useState<string>('all');

  const filtered = filter === 'all' ? agents : agents.filter(a => a.role === filter);
  const running = agents.filter(a => a.status === 'running').length;
  const totalTasks = agents.reduce((a, a2) => a + a2.tasks, 0);

  return (
    <div style={{ padding: 24, background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <h1 style={{ fontSize: 24, marginBottom: 20 }}>Agent DevOps</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#58A6FF' }}>{running}</div>
          <div style={{ color: '#8C8C8C' }}>Running</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#10B981' }}>{totalTasks}</div>
          <div style={{ color: '#8C8C8C' }}>Tasks</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#D29922' }}>{Math.round(agents.reduce((a, a2) => a + a2.success, 0)/agents.length)}%</div>
          <div style={{ color: '#8C8C8C' }}>Avg Success</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#8C8C8C' }}>{agents.length}</div>
          <div style={{ color: '#8C8C8C' }}>Agents</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        {['all', 'build', 'test', 'deploy', 'monitor', 'security', 'infrastructure'].map(f => (
          <button key={f} onClick={() => setFilter(f)} style={{
            padding: '8px 16px', background: filter === f ? '#238636' : '#21262D',
            border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer', textTransform: 'capitalize'
          }}>
            {f}
          </button>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
        {filtered.map(a => (
          <div key={a.id} style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <strong>{a.name}</strong>
              <span style={{ color: a.status === 'running' ? '#58A6FF' : a.status === 'completed' ? '#10B981' : '#8C8C8C' }}>
                {a.status}
              </span>
            </div>
            <p style={{ color: '#8C8C8C', fontSize: 12, textTransform: 'capitalize' }}>{a.role}</p>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8, fontSize: 12, color: '#8C8C8C' }}>
              <span>✓ {a.tasks} tasks</span>
              <span style={{ color: a.success >= 95 ? '#10B981' : '#D29922' }}>{a.success}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}