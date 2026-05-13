'use client';

import { useState } from 'react';

interface AgentOp {
  id: string;
  agent: string;
  operation: string;
  status: 'running' | 'completed' | 'failed';
  startTime: string;
  duration: number;
  cpu: number;
  memory: number;
}

const initialOps: AgentOp[] = [
  { id: '1', agent: 'Agent Zero', operation: 'orchestrate', status: 'running', startTime: '10:30:00', duration: 45, cpu: 45, memory: 512 },
  { id: '2', agent: 'Research Agent', operation: 'search', status: 'completed', startTime: '10:28:00', duration: 12, cpu: 30, memory: 256 },
  { id: '3', agent: 'Code Agent', operation: 'review', status: 'completed', startTime: '10:25:00', duration: 28, cpu: 60, memory: 384 },
  { id: '4', agent: 'Writer Agent', operation: 'write', status: 'failed', startTime: '10:20:00', duration: 5, cpu: 20, memory: 128 },
  { id: '5', agent: 'Triage Agent', operation: 'classify', status: 'running', startTime: '10:32:00', duration: 8, cpu: 25, memory: 192 },
];

export default function AgentOpsPage() {
  const [ops] = useState<AgentOp[]>(initialOps);
  const [filter, setFilter] = useState<string>('all');

  const filtered = filter === 'all' ? ops : ops.filter(o => o.status === filter);
  const running = ops.filter(o => o.status === 'running').length;
  const completed = ops.filter(o => o.status === 'completed').length;
  const failed = ops.filter(o => o.status === 'failed').length;

  return (
    <div style={{ padding: 24, background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <h1 style={{ fontSize: 24, marginBottom: 20 }}>Agent Operations</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#58A6FF' }}>{running}</div>
          <div style={{ color: '#8C8C8C' }}>Running</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#10B981' }}>{completed}</div>
          <div style={{ color: '#8C8C8C' }}>Completed</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#F85149' }}>{failed}</div>
          <div style={{ color: '#8C8C8C' }}>Failed</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#D29922' }}>{ops.length}</div>
          <div style={{ color: '#8C8C8C' }}>Total</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        {['all', 'running', 'completed', 'failed'].map(s => (
          <button key={s} onClick={() => setFilter(s)} style={{
            padding: '8px 16px', background: filter === s ? '#238636' : '#21262D',
            border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer', textTransform: 'capitalize'
          }}>
            {s}
          </button>
        ))}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {filtered.map(op => (
          <div key={op.id} style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <strong>{op.agent}</strong>
              <span style={{ color: op.status === 'running' ? '#58A6FF' : op.status === 'completed' ? '#10B981' : '#F85149' }}>
                {op.status}
              </span>
            </div>
            <p style={{ color: '#8C8C8C', margin: '4px 0' }}>{op.operation}</p>
            <div style={{ display: 'flex', gap: 16, fontSize: 12, color: '#8C8C8C' }}>
              <span>⏱ {op.duration}s</span>
              <span>💻 {op.cpu}%</span>
              <span>💾 {op.memory}MB</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}