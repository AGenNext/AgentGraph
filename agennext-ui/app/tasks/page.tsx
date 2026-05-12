'use client';

import { useState } from 'react';

interface Task {
  id: string;
  name: string;
  agent: string;
  status: 'queued' | 'running' | 'completed' | 'failed';
  created: string;
  duration?: string;
  result?: string;
}

const mockTasks: Task[] = [
  { id: 't1', name: 'Analyze Q4 data', agent: 'Data Analyzer', status: 'completed', created: '2024-02-01 10:00', duration: '2.3s', result: 'Score: 92%' },
  { id: 't2', name: 'Write report', agent: 'Report Writer', status: 'running', created: '2024-02-01 10:05', duration: '5.2s' },
  { id: 't3', name: 'Search docs', agent: 'Research Agent', status: 'queued', created: '2024-02-01 10:10' },
  { id: 't4', name: 'Fix bug', agent: 'Dev Agent', status: 'failed', created: '2024-02-01 09:00', duration: '30s', result: 'Error: API limit' },
];

export default function TasksPage() {
  const [tasks] = useState<Task[]>(mockTasks);

  const statusColors = {
    queued: '#8C8C8C',
    running: '#0F62FE',
    completed: '#10B981',
    failed: '#DA1E28',
  };

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F4F4F4', minHeight: '100vh' }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 24 }}>Task Manager</h1>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{tasks.length}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Total</div>
        </div>
        {Object.entries(statusColors).map(([status, color]) => (
          <div key={status} style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
            <div style={{ fontSize: 28, fontWeight: 600, color }}>{tasks.filter(t => t.status === status).length}</div>
            <div style={{ fontSize: 12, color: '#525252', textTransform: 'capitalize' }}>{status}</div>
          </div>
        ))}
      </div>

      <div style={{ background: '#fff', borderRadius: 4 }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#F4F4F4' }}>
              <th style={{ padding: 12, textAlign: 'left' }}>TASK</th>
              <th style={{ padding: 12, textAlign: 'left' }}>AGENT</th>
              <th style={{ padding: 12, textAlign: 'left' }}>STATUS</th>
              <th style={{ padding: 12, textAlign: 'left' }}>CREATED</th>
              <th style={{ padding: 12, textAlign: 'left' }}>DURATION</th>
              <th style={{ padding: 12, textAlign: 'left' }}>RESULT</th>
            </tr>
          </thead>
          <tbody>
            {tasks.map(task => (
              <tr key={task.id} style={{ borderBottom: '1px solid #E5E5E5' }}>
                <td style={{ padding: 12, fontWeight: 500 }}>{task.name}</td>
                <td style={{ padding: 12, fontSize: 12 }}>{task.agent}</td>
                <td style={{ padding: 12 }}>
                  <span style={{ 
                    color: statusColors[task.status], 
                    fontWeight: 500,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 6,
                  }}>
                    {task.status === 'running' && <span style={{ width: 8, height: 8, borderRadius: '50%', background: statusColors[task.status], animation: 'pulse 1s infinite' }} />}
                    {task.status}
                  </span>
                </td>
                <td style={{ padding: 12, fontSize: 12, color: '#525252' }}>{task.created}</td>
                <td style={{ padding: 12, fontSize: 12, fontFamily: 'monospace' }}>{task.duration || '-'}</td>
                <td style={{ padding: 12, fontSize: 12, color: task.status === 'failed' ? '#DA1E28' : '#525252' }}>
                  {task.result || '-'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      `}</style>
    </div>
  );
}