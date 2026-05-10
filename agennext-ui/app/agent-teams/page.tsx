'use client';

import { useState } from 'react';

interface Agent {
  id: string;
  name: string;
  role: string;
  capabilities: string[];
  model: string;
  status: 'active' | 'idle' | 'error';
  tasks: number;
  success: number;
}

interface AgentTeam {
  id: string;
  name: string;
  description: string;
  agents: Agent[];
  leader: string;
  purpose: string;
  status: 'active' | 'planning' | 'paused';
  metrics: { totalTasks: number; successRate: number };
}

const agents: Agent[] = [
  {
    id: 'a1',
    name: 'Research Lead',
    role: 'Lead Researcher',
    capabilities: ['web_search', 'pdf_analysis', 'citation'],
    model: 'Claude Opus 4',
    status: 'active',
    tasks: 1250,
    success: 94.5,
  },
  {
    id: 'a2',
    name: 'Research Assistant',
    role: 'Research Support',
    capabilities: ['data_gathering', 'note_taking'],
    model: 'Claude Haiku',
    status: 'active',
    tasks: 3200,
    success: 92.1,
  },
  {
    id: 'a3',
    name: 'Code Engineer',
    role: 'Senior Developer',
    capabilities: ['code_review', 'debugging', 'security'],
    model: 'Claude Sonnet',
    status: 'active',
    tasks: 890,
    success: 96.8,
  },
  {
    id: 'a4',
    name: 'Writer Lead',
    role: 'Content Lead',
    capabilities: ['writing', 'editing', 'seo'],
    model: 'GPT-4o',
    status: 'active',
    tasks: 650,
    success: 91.2,
  },
  {
    id: 'a5',
    name: 'Triage Coordinator',
    role: 'Routing',
    capabilities: ['classification', 'routing', 'prioritization'],
    model: 'Haiku',
    status: 'active',
    tasks: 5400,
    success: 97.3,
  },
  {
    id: 'a6',
    name: 'Financial Analyst',
    role: 'Finance Lead',
    capabilities: ['analysis', 'reporting', 'predictions'],
    model: 'Command R+',
    status: 'idle',
    tasks: 320,
    success: 89.5,
  },
];

const agentTeams: AgentTeam[] = [
  {
    id: 't1',
    name: 'Research Team',
    description: 'Academic research and document analysis',
    agents: [agents[0], agents[1]],
    leader: 'Research Lead',
    purpose: 'Research & Analysis',
    status: 'active',
    metrics: { totalTasks: 4450, successRate: 93.2 },
  },
  {
    id: 't2',
    name: 'Development Team',
    description: 'Software engineering and code review',
    agents: [agents[2]],
    leader: 'Code Engineer',
    purpose: 'Software Development',
    status: 'active',
    metrics: { totalTasks: 890, successRate: 96.8 },
  },
  {
    id: 't3',
    name: 'Content Team',
    description: 'Marketing and documentation',
    agents: [agents[3]],
    leader: 'Writer Lead',
    purpose: 'Content Creation',
    status: 'active',
    metrics: { totalTasks: 650, successRate: 91.2 },
  },
  {
    id: 't4',
    name: 'Support Automation',
    description: 'Customer support automation',
    agents: [agents[4]],
    leader: 'Triage Coordinator',
    purpose: 'Customer Support',
    status: 'active',
    metrics: { totalTasks: 5400, successRate: 97.3 },
  },
  {
    id: 't5',
    name: 'Analytics Team',
    description: 'Financial and business analytics',
    agents: [agents[5]],
    leader: 'Financial Analyst',
    purpose: 'Business Intelligence',
    status: 'planning',
    metrics: { totalTasks: 320, successRate: 89.5 },
  },
];

const chatMessages = [
  { id: 'm1', from: 'user', text: 'ResearchAgent: Analyze this paper and summarize key findings', time: '10:30' },
  { id: 'm2', from: 'agent', text: 'Research Assistant: Gathering paper... Research Lead: Analyzing key points...', time: '10:31' },
  { id: 'm3', from: 'agent', text: 'Research Lead: Summary complete with 3 key findings and implications.', time: '10:32' },
  { id: 'm4', from: 'user', text: 'CodeAgent: Review this PR for security issues', time: '10:35' },
  { id: 'm5', from: 'agent', text: 'Code Engineer: Found 2 vulnerabilities. Detailed report attached.', time: '10:36' },
];

export default function AgentTeamsPage() {
  const [selectedTeam, setSelectedTeam] = useState<AgentTeam | null>(null);
  
  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>Agents & Teams</h1>
          <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Manage AI agents and team orchestration</p>
        </div>
        <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 6, fontSize: 13, cursor: 'pointer' }}>
          + New Agent
        </button>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{agents.length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Total Agents</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{agents.filter(a => a.status === 'active').length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Active</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#667EEA' }}>{agentTeams.length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Teams</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#F59E0B' }}>
            {(agents.reduce((a, b) => a + b.tasks, 0) / 1000).toFixed(1)}K
          </div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Tasks Run</div>
        </div>
      </div>

      {/* Agent Teams Grid */}
      <div style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Agent Teams</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          {agentTeams.map(team => (
            <div 
              key={team.id}
              style={{ 
                background: '#fff', 
                borderRadius: 12, 
                border: '1px solid #E5E5E5', 
                padding: 20,
                cursor: 'pointer',
              }}
              onClick={() => setSelectedTeam(team)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
                <div style={{ fontSize: 16, fontWeight: 600 }}>{team.name}</div>
                <span style={{ 
                  background: team.status === 'active' ? '#10B98120' : team.status === 'planning' ? '#F59E0B20' : '#6B728020',
                  color: team.status === 'active' ? '#10B981' : team.status === 'planning' ? '#F59E0B' : '#6B7280',
                  padding: '4px 8px', borderRadius: 4, fontSize: 10, textTransform: 'capitalize',
                }}>
                  {team.status}
                </span>
              </div>
              <div style={{ fontSize: 12, color: '#6B7280', marginBottom: 12 }}>{team.description}</div>
              
              <div style={{ display: 'flex', gap: 4, marginBottom: 12 }}>
                {team.agents.map(a => (
                  <span 
                    key={a.id}
                    style={{ 
                      width: 24, height: 24, borderRadius: 12, background: '#667EEA', 
                      color: '#fff', fontSize: 10, display: 'flex', alignItems: 'center', justifyContent: 'center' 
                    }}
                    title={a.name}
                  >
                    {a.name.charAt(0)}
                  </span>
                ))}
              </div>
              
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12 }}>
                <span>{team.metrics.totalTasks} tasks</span>
                <span style={{ color: '#10B981', fontWeight: 500 }}>{team.metrics.successRate}% success</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* All Agents */}
      <div style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>All Agents</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          {agents.map(agent => (
            <div key={agent.id} style={{ background: '#fff', borderRadius: 12, border: '1px solid #E5E5E5', padding: 20 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 600 }}>{agent.name}</div>
                  <div style={{ fontSize: 11, color: '#6B7280' }}>{agent.role}</div>
                </div>
                <span style={{ 
                  width: 8, height: 8, borderRadius: 4, background: agent.status === 'active' ? '#10B981' : agent.status === 'idle' ? '#F59E0B' : '#DA1E28',
                }} />
              </div>
              
              <div style={{ fontSize: 11, marginBottom: 8 }}>
                {agent.capabilities.map(cap => (
                  <span key={cap} style={{ background: '#F4F4F4', padding: '2px 6px', borderRadius: 4, marginRight: 4 }}>
                    {cap}
                  </span>
                ))}
              </div>
              
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, color: '#6B7280', paddingTop: 12, borderTop: '1px solid #F4F4F4' }}>
                <span>{agent.tasks} tasks</span>
                <span style={{ color: '#10B981' }}>{agent.success}% success</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Multi-Agent Orchestration Chat */}
      <div style={{ background: '#fff', borderRadius: 12, border: '1px solid #E5E5E5', padding: 20 }}>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Multi-Agent Orchestration</h2>
        
        <div style={{ background: '#F8F9FA', borderRadius: 8, padding: 16, marginBottom: 16, minHeight: 200 }}>
          {chatMessages.map(msg => (
            <div key={msg.id} style={{ marginBottom: 12, display: 'flex', flexDirection: 'column', alignItems: msg.from === 'user' ? 'flex-end' : 'flex-start' }}>
              {msg.from === 'agent' && (
                <div style={{ fontSize: 10, color: '#667EEA', marginBottom: 2 }}>{msg.text.split(':')[0]}</div>
              )}
              <div style={{ 
                background: msg.from === 'user' ? '#667EEA' : '#E5E5E5', 
                color: msg.from === 'user' ? '#fff' : '#1A1A2E',
                padding: '8px 12px', borderRadius: 12, fontSize: 13, maxWidth: '70%',
              }}>
                {msg.from === 'agent' ? msg.text.split(':').slice(1).join(':') : msg.text}
              </div>
              <div style={{ fontSize: 10, color: '#6B7280', marginTop: 2 }}>{msg.time}</div>
            </div>
          ))}
        </div>
        
        <div style={{ display: 'flex', gap: 8 }}>
          <input 
            placeholder="Ask a team..." 
            style={{ flex: 1, padding: '12px 16px', borderRadius: 8, border: '1px solid #E5E5E5', fontSize: 14 }}
          />
          <button style={{ background: '#667EEA', color: '#fff', border: 'none', padding: '12px 20px', borderRadius: 8, fontSize: 13, cursor: 'pointer' }}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}