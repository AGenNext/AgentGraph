'use client';

import { useState, useMemo, useCallback } from 'react';

// Types - production grade
interface AgentIdentity {
  readonly id: string;
  name: string;
  readonly canonicalId: string;
  readonly owner: string;
  readonly workspace: string;
  status: AgentStatus;
  framework: string;
  credentials: Credential[];
  created: string;
  updated: string;
}

type AgentStatus = 'draft' | 'registered' | 'active' | 'suspended' | 'revoked';

interface Credential {
  id: string;
  type: 'api_key' | 'oauth' | 'vc';
  provider: string;
  status: 'pending' | 'approved' | 'revoked';
  createdAt: string;
}

// Constants
const STATUS_CONFIG: Record<AgentStatus, { label: string; color: string }> = {
  draft: { label: 'Draft', color: '#8C8C8C' },
  registered: { label: 'Registered', color: '#0F62FE' },
  active: { label: 'Active', color: '#10B981' },
  suspended: { label: 'Suspended', color: '#F59E0B' },
  revoked: { label: 'Revoked', color: '#DA1E28' },
};

const FRAMEWORK_OPTIONS = ['langgraph', 'crewai', 'autogen', 'langchain'] as const;
const STATUS_OPTIONS: AgentStatus[] = ['draft', 'registered', 'active', 'suspended', 'revoked'];

// Mock data with owner/workspace
const INITIAL_AGENTS: AgentIdentity[] = [
  {
    id: '1',
    name: 'Research Agent',
    canonicalId: 'urn:uuid:research-v1',
    owner: 'john@company.com',
    workspace: 'Production',
    status: 'active',
    framework: 'langgraph',
    credentials: [
      { id: 'c1', type: 'api_key', provider: 'openai', status: 'approved', createdAt: '2024-01-15' },
    ],
    created: '2024-01-15',
    updated: '2024-02-01',
  },
  {
    id: '2',
    name: 'Writer Agent',
    canonicalId: 'urn:uuid:writer-v1',
    owner: 'jane@company.com',
    workspace: 'Development',
    status: 'active',
    framework: 'crewai',
    credentials: [
      { id: 'c2', type: 'api_key', provider: 'anthropic', status: 'approved', createdAt: '2024-01-20' },
    ],
    created: '2024-01-20',
    updated: '2024-02-01',
  },
  {
    id: '3',
    name: 'Analyzer',
    canonicalId: 'urn:uuid:analyzer-v1',
    owner: 'john@company.com',
    workspace: 'Production',
    status: 'suspended',
    framework: 'autogen',
    credentials: [],
    created: '2024-01-25',
    updated: '2024-01-28',
  },
];

export default function LifecyclePage() {
  const [agents, setAgents] = useState<AgentIdentity[]>(INITIAL_AGENTS);
  const [filter, setFilter] = useState<AgentStatus | 'all'>('all');
  const [userFilter, setUserFilter] = useState<string | 'all'>('all');

  const filteredAgents = useMemo(() => {
    return agents.filter(a => {
      const statusMatch = filter === 'all' || a.status === filter;
      const userMatch = userFilter === 'all' || a.owner === userFilter;
      return statusMatch && userMatch;
    });
  }, [agents, filter, userFilter]);

  const handleStatusChange = useCallback((id: string, newStatus: AgentStatus) => {
    setAgents(prev => prev.map(a => 
      a.id === id 
        ? { ...a, status: newStatus, updated: new Date().toISOString().split('T')[0] }
        : a
    ));
  }, []);

  const stats = useMemo(() => ({
    total: agents.length,
    active: agents.filter(a => a.status === 'active').length,
    byStatus: Object.fromEntries(STATUS_OPTIONS.map(s => [s, agents.filter(a => a.status === s).length])) as Record<AgentStatus, number>,
    byOwner: agents.reduce((acc, a) => {
      acc[a.owner] = (acc[a.owner] || 0) + 1;
      return acc;
    }, {} as Record<string, number>),
  }), [agents]);

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F4F4F4', minHeight: '100vh' }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 24 }}>Agent Identity & Lifecycle</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{stats.total}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Total Agents</div>
        </div>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{stats.active}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Active</div>
        </div>
        {STATUS_OPTIONS.slice(0, 3).map(s => (
          <div key={s} style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
            <div style={{ fontSize: 28, fontWeight: 600, color: STATUS_CONFIG[s].color }}>{stats.byStatus[s]}</div>
            <div style={{ fontSize: 12, color: '#525252' }}>{STATUS_CONFIG[s].label}</div>
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
        <select value={filter} onChange={e => setFilter(e.target.value as AgentStatus | 'all')}
          style={{ padding: '8px 12px', borderRadius: 4, border: '1px solid #E5E5E5' }}>
          <option value="all">All Status</option>
          {STATUS_OPTIONS.map(s => <option key={s} value={s}>{STATUS_CONFIG[s].label}</option>)}
        </select>
        <select value={userFilter} onChange={e => setUserFilter(e.target.value)}
          style={{ padding: '8px 12px', borderRadius: 4, border: '1px solid #E5E5E5' }}>
          <option value="all">All Owners</option>
          {Object.keys(stats.byOwner).map(u => <option key={u} value={u}>{u}</option>)}
        </select>
      </div>

      <div style={{ background: '#fff', borderRadius: 4 }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#F4F4F4' }}>
              <th style={{ padding: 12, textAlign: 'left' }}>AGENT</th>
              <th style={{ padding: 12, textAlign: 'left' }}>OWNER</th>
              <th style={{ padding: 12, textAlign: 'left' }}>WORKSPACE</th>
              <th style={{ padding: 12, textAlign: 'left' }}>FRAMEWORK</th>
              <th style={{ padding: 12, textAlign: 'left' }}>STATUS</th>
              <th style={{ padding: 12, textAlign: 'left' }}>ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            {filteredAgents.map(agent => (
              <tr key={agent.id} style={{ borderBottom: '1px solid #E5E5E5' }}>
                <td style={{ padding: 12 }}>
                  <div style={{ fontWeight: 500 }}>{agent.name}</div>
                  <div style={{ fontSize: 11, color: '#8C8C8C' }}>{agent.canonicalId}</div>
                </td>
                <td style={{ padding: 12, fontSize: 12 }}>{agent.owner}</td>
                <td style={{ padding: 12, fontSize: 12 }}>{agent.workspace}</td>
                <td style={{ padding: 12 }}>
                  <span style={{ background: '#E5E5E5', padding: '4px 8px', borderRadius: 4, fontSize: 12 }}>{agent.framework}</span>
                </td>
                <td style={{ padding: 12 }}>
                  <span style={{ color: STATUS_CONFIG[agent.status].color, fontWeight: 500 }}>{STATUS_CONFIG[agent.status].label}</span>
                </td>
                <td style={{ padding: 12 }}>
                  <select value={agent.status} onChange={e => handleStatusChange(agent.id, e.target.value as AgentStatus)}
                    style={{ padding: '4px 8px', borderRadius: 4, border: '1px solid #E5E5E5', fontSize: 12 }}>
                    {STATUS_OPTIONS.map(s => <option key={s} value={s}>{STATUS_CONFIG[s].label}</option>)}
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}