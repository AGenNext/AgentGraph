'use client';

import { useState, useEffect } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Node,
  Edge,
  Connection,
  BackgroundVariant,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

interface AgentIdentity {
  id: string;
  name: string;
  framework: 'langgraph' | 'crewai' | 'autogen' | 'langchain' | 'dify' | 'google-adk';
  status: 'draft' | 'registered' | 'active' | 'suspended' | 'revoked';
  credentials: {
    type: 'waltid' | 'wso2' | 'auth0' | 'keycloak' | 'polygon-id';
    verified: boolean;
    vcIssued: string;
  }[];
  created: string;
  updated: string;
  owner: string;
  canonicalId: string;
  version: string;
  capabilities: string[];
}

const mockAgents: AgentIdentity[] = [
  { id: '1', name: 'Research Agent', framework: 'langgraph', status: 'active', credentials: [{ type: 'wso2', verified: true, vcIssued: '2024-01-15' }], created: '2024-01-15', updated: '2024-02-01', owner: 'system', canonicalId: 'urn:uuid:research-v1', version: '1.0.0', capabilities: ['search', 'analyze'] },
  { id: '2', name: 'Writer Agent', framework: 'crewai', status: 'active', credentials: [{ type: 'waltid', verified: true, vcIssued: '2024-01-20' }], created: '2024-01-20', updated: '2024-02-01', owner: 'system', canonicalId: 'urn:uuid:writer-v1', version: '1.0.0', capabilities: ['write', 'edit'] },
  { id: '3', name: 'Analyzer', framework: 'autogen', status: 'registered', credentials: [{ type: 'auth0', verified: false, vcIssued: '-' }], created: '2024-01-25', updated: '2024-01-25', owner: 'system', canonicalId: 'urn:uuid:analyzer-v1', version: '0.9.0', capabilities: ['analyze'] },
  { id: '4', name: 'Assistant', framework: 'langchain', status: 'draft', credentials: [], created: '2024-02-01', updated: '2024-02-01', owner: 'system', canonicalId: 'urn:uuid:assistant-v1', version: '0.1.0', capabilities: [] },
];

const frameworks = [
  { id: 'langgraph', name: 'LangGraph', logo: 'LG', color: '#7C3AED' },
  { id: 'crewai', name: 'CrewAI', logo: 'CA', color: '#0F62FE' },
  { id: 'autogen', name: 'AutoGen', logo: 'AG', color: '#DA1E28' },
  { id: 'langchain', name: 'LangChain', logo: 'LC', color: '#000' },
  { id: 'dify', name: 'Dify', logo: 'DF', color: '#10B981' },
  { id: 'google-adk', name: 'Google ADK', logo: 'ADK', color: '#4285F4' },
];

const statusConfig = {
  draft: { label: 'Draft', color: '#8C8C8C' },
  registered: { label: 'Registered', color: '#0F62FE' },
  active: { label: 'Active', color: '#10B981' },
  suspended: { label: 'Suspended', color: '#F59E0B' },
  revoked: { label: 'Revoked', color: '#DA1E28' },
};

const providerIcons: Record<string, string> = {
  wso2: '⟳',
  waltid: '◎',
  auth0: '②',
  keycloak: '🛡',
  'polygon-id': '⬡',
};

export function AgentLifecycleManager() {
  const [agents, setAgents] = useState<AgentIdentity[]>(mockAgents);
  const [selected, setSelected] = useState<AgentIdentity | null>(null);
  const [view, setView] = useState<'list' | 'graph'>('list');
  const [showModal, setShowModal] = useState(false);
  const [filter, setFilter] = useState<string>('all');
  
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  useEffect(() => {
    if (view === 'graph' && agents.length > 0) {
      const graphNodes = agents.map((agent, i) => ({
        id: agent.id,
        position: { x: 100 + (i % 3) * 250, y: 100 + Math.floor(i / 3) * 150 },
        data: { label: agent.name },
        style: {
          background: statusConfig[agent.status].color + '20',
          border: `2px solid ${statusConfig[agent.status].color}`,
          borderRadius: 8,
          padding: 12,
          width: 180,
        },
      }));
      setNodes(graphNodes as any);
    }
  }, [view, agents]);

  const filteredAgents = filter === 'all' ? agents : agents.filter(a => a.status === filter);

  const handleStatusChange = (id: string, newStatus: AgentIdentity['status']) => {
    setAgents(agents.map(a => a.id === id ? { ...a, status: newStatus, updated: new Date().toISOString().split('T')[0] } : a));
  };

  const handleCredentialIssue = (id: string, provider: string) => {
    setAgents(agents.map(a => {
      if (a.id === id) {
        return {
          ...a,
          credentials: [...a.credentials, { type: provider as any, verified: false, vcIssued: new Date().toISOString().split('T')[0] }],
          status: 'registered' as const,
        };
      }
      return a;
    }));
  };

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F4F4F4', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24, background: '#fff', padding: 16, borderRadius: 4 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, color: '#161616', margin: 0 }}>Agent Lifecycle Management</h1>
          <p style={{ color: '#525252', margin: '4px 0 0' }}>Register, provision, and manage agent identities with verifiable credentials</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button
            onClick={() => setView('list')}
            style={{
              background: view === 'list' ? '#0F62FE' : '#E5E5E5',
              color: view === 'list' ? '#fff' : '#161616',
              border: 'none',
              padding: '8px 16px',
              borderRadius: 4,
              cursor: 'pointer',
              fontSize: 14,
            }}
          >
            List
          </button>
          <button
            onClick={() => setView('graph')}
            style={{
              background: view === 'graph' ? '#0F62FE' : '#E5E5E5',
              color: view === 'graph' ? '#fff' : '#161616',
              border: 'none',
              padding: '8px 16px',
              borderRadius: 4,
              cursor: 'pointer',
              fontSize: 14,
            }}
          >
            Graph
          </button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#161616' }}>{agents.length}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Total</div>
        </div>
        {Object.entries(statusConfig).map(([key, config]) => (
          <div key={key} style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
            <div style={{ fontSize: 28, fontWeight: 600, color: config.color }}>{agents.filter(a => a.status === key).length}</div>
            <div style={{ fontSize: 12, color: '#525252' }}>{config.label}</div>
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        {['all', ...Object.keys(statusConfig)].map(s => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            style={{
              background: filter === s ? '#0F62FE' : '#fff',
              color: filter === s ? '#fff' : '#161616',
              border: '1px solid #E5E5E5',
              padding: '6px 12px',
              borderRadius: 4,
              cursor: 'pointer',
              fontSize: 12,
              textTransform: 'capitalize',
            }}
          >
            {s}
          </button>
        ))}
      </div>

      {view === 'list' ? (
        <div style={{ background: '#fff', borderRadius: 4, overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#F4F4F4', borderBottom: '2px solid #E5E5E5' }}>
                <th style={{ padding: 12, textAlign: 'left', fontSize: 12, color: '#525252' }}>AGENT</th>
                <th style={{ padding: 12, textAlign: 'left', fontSize: 12, color: '#525252' }}>FRAMEWORK</th>
                <th style={{ padding: 12, textAlign: 'left', fontSize: 12, color: '#525252' }}>STATUS</th>
                <th style={{ padding: 12, textAlign: 'left', fontSize: 12, color: '#525252' }}>CREDENTIALS</th>
                <th style={{ padding: 12, textAlign: 'left', fontSize: 12, color: '#525252' }}>VERSION</th>
                <th style={{ padding: 12, textAlign: 'left', fontSize: 12, color: '#525252' }}>UPDATED</th>
                <th style={{ padding: 12, textAlign: 'left', fontSize: 12, color: '#525252' }}>ACTIONS</th>
              </tr>
            </thead>
            <tbody>
              {filteredAgents.map(agent => (
                <tr key={agent.id} style={{ borderBottom: '1px solid #E5E5E5', cursor: 'pointer' }} onClick={() => setSelected(agent)}>
                  <td style={{ padding: 12 }}>
                    <div style={{ fontWeight: 500 }}>{agent.name}</div>
                    <div style={{ fontSize: 11, color: '#8C8C8C', fontFamily: 'monospace' }}>{agent.canonicalId}</div>
                  </td>
                  <td style={{ padding: 12 }}>
                    {(() => {
                      const fw = frameworks.find(f => f.id === agent.framework);
                      return (
                        <span style={{ 
                          display: 'inline-flex', 
                          alignItems: 'center', 
                          gap: 6, 
                          background: fw?.color + '15', 
                          color: fw?.color,
                          padding: '4px 8px', 
                          borderRadius: 4, 
                          fontSize: 12,
                          fontWeight: 500,
                        }}>
                          <span style={{ fontSize: 10 }}>{fw?.logo}</span>
                          {fw?.name}
                        </span>
                      );
                    })()}
                  </td>
                  <td style={{ padding: 12 }}>
                    <span style={{ 
                      display: 'inline-flex', 
                      alignItems: 'center',
                      gap: 6,
                      color: statusConfig[agent.status].color,
                      fontSize: 12,
                      fontWeight: 500,
                    }}>
                      <span style={{ 
                        width: 8, 
                        height: 8, 
                        borderRadius: '50%', 
                        background: statusConfig[agent.status].color 
                      }} />
                      {statusConfig[agent.status].label}
                    </span>
                  </td>
                  <td style={{ padding: 12 }}>
                    <div style={{ display: 'flex', gap: 4 }}>
                      {agent.credentials.map(c => (
                        <span key={c.type} style={{ 
                          fontSize: 12, 
                          background: c.verified ? '#10B98115' : '#F59E0B15',
                          color: c.verified ? '#10B981' : '#F59E0B',
                          padding: '2px 6px',
                          borderRadius: 4,
                        }}>
                          {providerIcons[c.type]} {c.type}
                        </span>
                      ))}
                      {agent.credentials.length === 0 && (
                        <span style={{ fontSize: 11, color: '#8C8C8C' }}>No credentials</span>
                      )}
                    </div>
                  </td>
                  <td style={{ padding: 12, fontSize: 12, fontFamily: 'monospace' }}>{agent.version}</td>
                  <td style={{ padding: 12, fontSize: 12, color: '#525252' }}>{agent.updated}</td>
                  <td style={{ padding: 12 }} onClick={e => e.stopPropagation()}>
                    <select
                      value={agent.status}
                      onChange={e => handleStatusChange(agent.id, e.target.value as any)}
                      style={{ 
                        padding: '4px 8px', 
                        border: '1px solid #E5E5E5', 
                        borderRadius: 4, 
                        fontSize: 11,
                        background: '#fff',
                      }}
                    >
                      {Object.keys(statusConfig).map(s => (
                        <option key={s} value={s}>{statusConfig[s as keyof typeof statusConfig].label}</option>
                      ))}
                    </select>
                    {agent.credentials.length === 0 && (
                      <button
                        onClick={() => handleCredentialIssue(agent.id, 'wso2')}
                        style={{
                          background: '#0F62FE',
                          color: '#fff',
                          border: 'none',
                          padding: '4px 8px',
                          borderRadius: 4,
                          fontSize: 11,
                          cursor: 'pointer',
                          marginLeft: 8,
                        }}
                      >
                        Issue VC
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div style={{ background: '#fff', borderRadius: 4, height: 400 }}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={(params: Connection) => setEdges(eds => addEdge(params, eds))}
            fitView
          >
            <Controls />
            <MiniMap />
            <Background variant={BackgroundVariant.Dots} gap={20} />
          </ReactFlow>
        </div>
      )}
    </div>
  );
}