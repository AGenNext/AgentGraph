'use client';

import { useState } from 'react';

// Agent Zero - The Root Orchestrator
// According to Agent Factory blueprint: Agent Zero serves as the primary agent that coordinates all other agents

interface AgentCapability {
  name: string;
  enabled: boolean;
  policy: string;
}

interface ChildAgent {
  id: string;
  name: string;
  role: string;
  status: 'active' | 'idle' | 'error';
  capabilities: string[];
  delegate: string;
}

const agentCapabilities: AgentCapability[] = [
  { name: 'orchestrate', enabled: true, policy: 'allow' },
  { name: 'delegate', enabled: true, policy: 'allow' },
  { name: 'monitor', enabled: true, policy: 'allow' },
  { name: 'evaluate', enabled: true, policy: 'require_approval' },
  { name: 'escalate', enabled: true, policy: 'require_approval' },
  { name: 'rollcall', enabled: true, policy: 'allow' },
];

const childAgents: ChildAgent[] = [
  { id: 'c1', name: 'Research Agent', role: 'Research', status: 'active', capabilities: ['search', 'analyze', 'summarize'], delegate: 'research' },
  { id: 'c2', name: 'Writer Agent', role: 'Content', status: 'active', capabilities: ['write', 'edit', 'seo'], delegate: 'writing' },
  { id: 'c3', name: 'Code Agent', role: 'Development', status: 'active', capabilities: ['code', 'review', 'debug'], delegate: 'coding' },
  { id: 'c4', name: 'Triage Agent', role: 'Routing', status: 'idle', capabilities: ['classify', 'route', 'prioritize'], delegate: 'triage' },
  { id: 'c5', name: 'Finance Agent', role: 'Finance', status: 'active', capabilities: ['analyze', 'report', 'predict'], delegate: 'finance' },
];

const delegationLog = [
  { id: 'd1', from: 'Agent Zero', to: 'Research Agent', task: 'Analyze quarterly report', time: '10:32', status: 'completed' },
  { id: 'd2', from: 'Agent Zero', to: 'Writer Agent', task: 'Draft blog post', time: '10:30', status: 'completed' },
  { id: 'd3', from: 'Agent Zero', to: 'Code Agent', task: 'Review PR #245', time: '10:28', status: 'completed' },
  { id: 'd4', from: 'Agent Zero', to: 'ALL', task: 'Health check', time: '10:00', status: 'completed' },
];

const metrics = {
  totalDelegations: 12450,
  successRate: 97.2,
  avgLatency: 450,
  activeAgents: childAgents.filter(a => a.status === 'active').length,
};

export default function AgentZeroPage() {
  const [selectedTab, setSelectedTab] = useState<'overview' | 'capabilities' | 'agents' | 'logs'>('overview');
  
  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <div style={{ width: 48, height: 48, borderRadius: 24, background: 'linear-gradient(135deg, #667EEA, #764BA2)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 24 }}>
            0
          </div>
          <div>
            <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>Agent Zero</h1>
            <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Root orchestrator & delegation authority</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <span style={{ background: '#10B98120', color: '#10B981', padding: '6px 12px', borderRadius: 6, fontSize: 12 }}>
            ● Active
          </span>
        </div>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#1F2937', padding: 20, borderRadius: 12 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#667EEA' }}>{metrics.totalDelegations.toLocaleString()}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Total Delegations</div>
        </div>
        <div style={{ background: '#1F2937', padding: 20, borderRadius: 12 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{metrics.successRate}%</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Success Rate</div>
        </div>
        <div style={{ background: '#1F2937', padding: 20, borderRadius: 12 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#F59E0B' }}>{metrics.avgLatency}ms</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Avg Latency</div>
        </div>
        <div style={{ background: '#1F2937', padding: 20, borderRadius: 12 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{metrics.activeAgents}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Active Agents</div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        {(['overview', 'capabilities', 'agents', 'logs'] as const).map(t => (
          <button
            key={t}
            onClick={() => setSelectedTab(t)}
            style={{
              background: selectedTab === t ? '#1F2937' : 'transparent',
              color: selectedTab === t ? '#fff' : '#6B7280',
              border: 'none',
              padding: '10px 20px',
              borderRadius: 8,
              fontSize: 13,
              cursor: 'pointer',
              textTransform: 'capitalize',
            }}
          >
            {t === 'overview' ? 'Overview' : t === 'capabilities' ? 'Capabilities' : t === 'agents' ? 'Child Agents' : 'Delegation Logs'}
          </button>
        ))}
      </div>

      {selectedTab === 'overview' ? (
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 16 }}>
          {/* Orchestration Flow */}
          <div style={{ background: '#1F2937', borderRadius: 12, padding: 20 }}>
            <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>Orchestration Hierarchy</h3>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16 }}>
              <div style={{ width: 120, height: 60, borderRadius: 30, background: 'linear-gradient(135deg, #667EEA, #764BA2)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 600, fontSize: 14 }}>
                Agent Zero
              </div>
              <div style={{ width: 2, height: 20, background: '#374151' }} />
              <div style={{ width: '80%', height: 2, background: '#374151' }} />
              <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', justifyContent: 'center' }}>
                {childAgents.map(agent => (
                  <div key={agent.id} style={{ width: 100, height: 50, borderRadius: 10, background: '#374151', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 11, flexDirection: 'column' }}>
                    <span>{agent.name.split(' ')[0]}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div style={{ background: '#1F2937', borderRadius: 12, padding: 20 }}>
            <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>Quick Actions</h3>
            {[
              { label: 'Delegate Task', icon: '→', color: '#667EEA' },
              { label: 'Rollcall All', icon: '👥', color: '#10B981' },
              { label: 'Health Check', icon: '✓', color: '#F59E0B' },
              { label: 'Emergency Stop', icon: '⏹', color: '#DA1E28' },
            ].map(action => (
              <button key={action.label} style={{ width: '100%', background: '#374151', border: 'none', padding: '12px 16px', borderRadius: 8, marginBottom: 8, color: '#fff', fontSize: 13, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 8 }}>
                <span>{action.icon}</span> {action.label}
              </button>
            ))}
          </div>
        </div>
      ) : selectedTab === 'capabilities' ? (
        <div style={{ background: '#1F2937', borderRadius: 12, padding: 20 }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid #374151' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>CAPABILITY</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>STATUS</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>POLICY</th>
              </tr>
            </thead>
            <tbody>
              {agentCapabilities.map(cap => (
                <tr key={cap.name} style={{ borderBottom: '1px solid #374151' }}>
                  <td style={{ padding: '14px 16px', fontWeight: 500, textTransform: 'capitalize' }}>{cap.name}</td>
                  <td style={{ padding: '14px 16px' }}>
                    <span style={{ color: cap.enabled ? '#10B981' : '#DA1E28' }}>
                      {cap.enabled ? '✓ Enabled' : '✗ Disabled'}
                    </span>
                  </td>
                  <td style={{ padding: '14px 16px', fontSize: 12, fontFamily: 'monospace' }}>{cap.policy}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : selectedTab === 'agents' ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          {childAgents.map(agent => (
            <div key={agent.id} style={{ background: '#1F2937', borderRadius: 12, padding: 20 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
                <div style={{ fontSize: 14, fontWeight: 600 }}>{agent.name}</div>
                <span style={{ 
                  width: 8, height: 8, borderRadius: 4, 
                  background: agent.status === 'active' ? '#10B981' : agent.status === 'idle' ? '#F59E0B' : '#DA1E28' 
                }} />
              </div>
              <div style={{ fontSize: 12, color: '#6B7280', marginBottom: 8 }}>{agent.role}</div>
              <div style={{ fontSize: 11, color: '#6B7280', marginBottom: 8 }}>Delegate: {agent.delegate}</div>
              <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                {agent.capabilities.map(cap => (
                  <span key={cap} style={{ background: '#374151', padding: '2px 6px', borderRadius: 4, fontSize: 10 }}>
                    {cap}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div style={{ background: '#1F2937', borderRadius: 12, overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#111827' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>FROM</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>TO</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>TASK</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>TIME</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>STATUS</th>
              </tr>
            </thead>
            <tbody>
              {delegationLog.map(log => (
                <tr key={log.id} style={{ borderTop: '1px solid #374151' }}>
                  <td style={{ padding: '14px 16px', fontWeight: 500 }}>{log.from}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12 }}>{log.to}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12 }}>{log.task}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280' }}>{log.time}</td>
                  <td style={{ padding: '14px 16px' }}>
                    <span style={{ color: log.status === 'completed' ? '#10B981' : '#F59E0B', fontSize: 12 }}>
                      {log.status === 'completed' ? '✓' : '⏳'} {log.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}