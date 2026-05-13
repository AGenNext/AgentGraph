'use client';

import { useState } from 'react';

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
  { name: 'reason', enabled: true, policy: 'allow' },
  { name: 'plan', enabled: true, policy: 'allow' },
];

const childAgents: ChildAgent[] = [
  { id: 'c1', name: 'Research Agent', role: 'Research', status: 'active', capabilities: ['search', 'analyze', 'summarize'], delegate: 'research' },
  { id: 'c2', name: 'Writer Agent', role: 'Content', status: 'active', capabilities: ['write', 'edit', 'seo'], delegate: 'writing' },
  { id: 'c3', name: 'Code Agent', role: 'Development', status: 'active', capabilities: ['code', 'review', 'debug'], delegate: 'coding' },
  { id: 'c4', name: 'Security Agent', role: 'Security', status: 'active', capabilities: ['scan', 'audit', 'protect'], delegate: 'security' },
  { id: 'c5', name: 'Data Agent', role: 'Analytics', status: 'idle', capabilities: ['etl', 'visualize', 'predict'], delegate: 'data' },
  { id: 'c6', name: 'Support Agent', role: 'Customer Success', status: 'active', capabilities: ['ticket', 'resolve', 'escalate'], delegate: 'support' },
];

export default function AgentZeroPage() {
  const [tab, setTab] = useState<string>('overview');
  const [expanded, setExpanded] = useState<string | null>(null);
  const activeCount = childAgents.filter(a => a.status === 'active').length;

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'capabilities', label: 'Capabilities' },
    { id: 'agents', label: 'Child Agents' },
    { id: 'blueprint', label: 'Blueprint' },
  ];

  return (
    <div style={{ padding: 24, background: '#0a0e14', minHeight: '100vh', color: '#e6edf3', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 4, color: '#f0f6fc' }}>Agent Zero</h1>
        <p style={{ color: '#8b949e', fontSize: 14 }}>The Root Orchestrator - Enterprise AI Agent Platform</p>
      </div>

      <div style={{ display: 'flex', gap: 4, background: '#161b22', padding: 4, borderRadius: 8, marginBottom: 24, width: 'fit-content' }}>
        {tabs.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)} style={{
            padding: '8px 16px', background: tab === t.id ? '#238636' : 'transparent',
            border: 'none', borderRadius: 6, color: tab === t.id ? '#fff' : '#8b949e',
            fontSize: 13, fontWeight: 500, cursor: 'pointer', transition: 'all 0.15s'
          }}>
            {t.label}
          </button>
        ))}
      </div>

      {tab === 'overview' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
          <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
            <div style={{ fontSize: 36, fontWeight: 700, color: '#58a6ff' }}>{activeCount}</div>
            <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Active Agents</div>
          </div>
          <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
            <div style={{ fontSize: 36, fontWeight: 700, color: '#3fb950' }}>{childAgents.length}</div>
            <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Total Child Agents</div>
          </div>
          <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
            <div style={{ fontSize: 36, fontWeight: 700, color: '#d29922' }}>{agentCapabilities.length}</div>
            <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Capabilities</div>
          </div>
          <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
            <div style={{ fontSize: 36, fontWeight: 700, color: '#f778ba' }}>99.9%</div>
            <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Uptime SLA</div>
          </div>
        </div>
      )}

      {tab === 'capabilities' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
          {agentCapabilities.map(cap => (
            <div key={cap.name} style={{ padding: 16, background: '#161b22', borderRadius: 8, border: '1px solid #30363d' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                <strong style={{ color: '#f0f6fc', textTransform: 'capitalize' }}>{cap.name}</strong>
                <span style={{ padding: '2px 8px', borderRadius: 4, fontSize: 11, background: cap.enabled ? 'rgba(63, 185, 80, 0.15)' : 'rgba(248, 81, 73, 0.15)', color: cap.enabled ? '#3fb950' : '#f85149' }}>
                  {cap.enabled ? 'Enabled' : 'Disabled'}
                </span>
              </div>
              <p style={{ fontSize: 12, color: '#8b949e' }}>Policy: {cap.policy}</p>
            </div>
          ))}
        </div>
      )}

      {tab === 'agents' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
          {childAgents.map(agent => (
            <div key={agent.id} onClick={() => setExpanded(expanded === agent.id ? null : agent.id)} style={{ padding: 16, background: '#161b22', borderRadius: 8, border: '1px solid #30363d', cursor: 'pointer' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                <strong style={{ color: '#f0f6fc' }}>{agent.name}</strong>
                <span style={{ padding: '2px 8px', borderRadius: 4, fontSize: 11, background: agent.status === 'active' ? 'rgba(63, 185, 80, 0.15)' : agent.status === 'idle' ? 'rgba(210, 153, 34, 0.15)' : 'rgba(248, 81, 73, 0.15)', color: agent.status === 'active' ? '#3fb950' : agent.status === 'idle' ? '#d29922' : '#f85149' }}>
                  {agent.status}
                </span>
              </div>
              <p style={{ fontSize: 12, color: '#8b949e' }}>Role: {agent.role}</p>
              <p style={{ fontSize: 12, color: '#8b949e', marginTop: 4 }}>Delegate: {agent.delegate}</p>
            </div>
          ))}
        </div>
      )}

      {tab === 'blueprint' && (
        <div style={{ padding: 24, background: '#161b22', borderRadius: 12, border: '1px solid #30363d' }}>
          <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16, color: '#f0f6fc' }}>Agent Blueprint</h2>
          <pre style={{ fontSize: 12, color: '#8b949e', fontFamily: 'monospace', lineHeight: 1.6 }}>
{`Agent Zero (Root Orchestrator)
├── Capabilities
│   ├── orchestrate    [✓ enabled]
│   ├── delegate      [✓ enabled]
│   ├── monitor       [✓ enabled]
│   ├── evaluate     [✓ enabled - require_approval]
│   ├── escalate     [✓ enabled - require_approval]
│   ├── rollcall     [✓ enabled]
│   ├── reason        [✓ enabled]
│   └── plan          [✓ enabled]
│
└── Child Agents
    ├── Research Agent    [active]
    ├── Writer Agent     [active]
    ├── Code Agent      [active]
    ├── Security Agent  [active]
    ├── Data Agent       [idle]
    └── Support Agent   [active]
`}
          </pre>
        </div>
      )}
    </div>
  );
}