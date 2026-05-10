'use client';

import { useState } from 'react';

interface CrewAgent {
  id: string;
  name: string;
  role: string;
  goal: string;
  backstory: string;
  tools: string[];
}

interface Process {
  id: string;
  name: string;
  type: 'sequential' | 'hierarchical' | 'parallel';
  agents: string[];
  verbose: boolean;
}

interface Task {
  id: string;
  description: string;
  agent: string;
  expectedOutput: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
}

const crewAgents: CrewAgent[] = [
  {
    id: 'ca1',
    name: 'Research Lead',
    role: 'Senior Researcher',
    goal: 'Find and analyze the most relevant information',
    backstory: 'Expert at searching documents and extracting key insights',
    tools: ['search', 'scrape', 'analyze'],
  },
  {
    id: 'ca2',
    name: 'Analyst',
    role: 'Data Analyst',
    goal: 'Process and analyze data to find patterns',
    backstory: 'Statistical analysis expert with Python skills',
    tools: ['python', 'visualize', 'stats'],
  },
  {
    id: 'ca3',
    name: 'Writer',
    role: 'Technical Writer',
    goal: 'Create clear, concise documentation',
    backstory: 'Former tech writer at top companies',
    tools: ['write', 'edit', 'format'],
  },
  {
    id: 'ca4',
    name: 'Reviewer',
    role: 'Quality Assurance',
    goal: 'Ensure accuracy and quality of output',
    backstory: 'Detail-oriented with strong review skills',
    tools: ['review', 'validate', 'approve'],
  },
];

const processes: Process[] = [
  { id: 'p1', name: 'Research Pipeline', type: 'sequential', agents: ['Research Lead', 'Writer', 'Reviewer'], verbose: true },
  { id: 'p2', name: 'Analysis Pipeline', type: 'hierarchical', agents: ['Analyst', 'Reviewer'], verbose: true },
  { id: 'p3', name: 'Quick Analysis', type: 'parallel', agents: ['Research Lead', 'Analyst'], verbose: false },
];

const tasks: Task[] = [
  { id: 't1', description: 'Research AI trends', agent: 'Research Lead', expectedOutput: 'Summary report', status: 'completed' },
  { id: 't2', description: 'Analyze market data', agent: 'Analyst', expectedOutput: 'Charts and insights', status: 'running' },
  { id: 't3', description: 'Write findings', agent: 'Writer', expectedOutput: 'Blog post', status: 'pending' },
  { id: 't4', description: 'Review final draft', agent: 'Reviewer', expectedOutput: 'Approved document', status: 'pending' },
];

const executionLogs = [
  { id: 'e1', crew: 'Research Pipeline', start: '10:00', end: '10:45', status: 'success', duration: '45m' },
  { id: 'e2', crew: 'Analysis Pipeline', start: '09:00', end: '09:30', status: 'success', duration: '30m' },
  { id: 'e3', crew: 'Quick Analysis', start: '08:15', end: '08:25', status: 'success', duration: '10m' },
  { id: 'e4', crew: 'Research Pipeline', start: '07:00', end: '07:50', status: 'failed', duration: '50m' },
];

export default function CrewsPage() {
  const [selectedTab, setSelectedTab] = useState<'crews' | 'processes' | 'tasks' | 'logs'>('crews');
  const [selectedProcess, setSelectedProcess] = useState<Process | null>(null);

  const stats = {
    totalCrews: processes.length,
    totalAgents: crewAgents.length,
    completedTasks: tasks.filter(t => t.status === 'completed').length,
    successRate: 90,
  };

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>Crews</h1>
          <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>CrewAI-style multi-agent orchestration</p>
        </div>
        <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 6, fontSize: 13, cursor: 'pointer' }}>
          + New Crew
        </button>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{stats.totalCrews}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Total Crews</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#667EEA' }}>{stats.totalAgents}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Agents</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{stats.completedTasks}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Completed</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#F59E0B' }}>{stats.successRate}%</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Success Rate</div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        {(['crews', 'processes', 'tasks', 'logs'] as const).map(t => (
          <button
            key={t}
            onClick={() => setSelectedTab(t)}
            style={{
              background: selectedTab === t ? '#1A1A2E' : '#fff',
              color: selectedTab === t ? '#fff' : '#525252',
              border: '1px solid #E5E5E5',
              padding: '10px 20px',
              borderRadius: 8,
              fontSize: 13,
              cursor: 'pointer',
              textTransform: 'capitalize',
            }}
          >
            {t === 'crews' ? 'Agents' : t === 'processes' ? 'Processes' : t === 'tasks' ? 'Tasks' : 'Execution'}
          </button>
        ))}
      </div>

      {selectedTab === 'crews' ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 16 }}>
          {crewAgents.map(agent => (
            <div key={agent.id} style={{ background: '#fff', borderRadius: 12, border: '1px solid #E5E5E5', padding: 20 }}>
              <div style={{ fontSize: 16, fontWeight: 600, marginBottom: 4 }}>{agent.name}</div>
              <div style={{ fontSize: 12, color: '#0F62FE', marginBottom: 8 }}>{agent.role}</div>
              <div style={{ fontSize: 12, color: '#6B7280', marginBottom: 8, fontStyle: 'italic' }}>Goal: {agent.goal}</div>
              <p style={{ fontSize: 12, color: '#6B7280', marginBottom: 12, lineHeight: 1.5 }}>{agent.backstory}</p>
              <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                {agent.tools.map(tool => (
                  <span key={tool} style={{ background: '#F4F4F4', padding: '2px 8px', borderRadius: 4, fontSize: 11 }}>
                    {tool}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      ) : selectedTab === 'processes' ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          {processes.map(proc => (
            <div 
              key={proc.id} 
              style={{ background: '#fff', borderRadius: 12, border: '1px solid #E5E5E5', padding: 20, cursor: 'pointer' }}
              onClick={() => setSelectedProcess(proc)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
                <div style={{ fontSize: 16, fontWeight: 600 }}>{proc.name}</div>
                <span style={{ 
                  background: proc.type === 'sequential' ? '#667EEA20' : proc.type === 'hierarchical' ? '#F59E0B20' : '#10B98120',
                  color: proc.type === 'sequential' ? '#667EEA' : proc.type === 'hierarchical' ? '#F59E0B' : '#10B981',
                  padding: '4px 8px', borderRadius: 4, fontSize: 10, textTransform: 'capitalize',
                }}>
                  {proc.type}
                </span>
              </div>
              <div style={{ fontSize: 12, color: '#6B7280', marginBottom: 8 }}>Agents: {proc.agents.join(' → ')}</div>
              <div style={{ fontSize: 11, color: '#6B7280' }}>
                Verbose: {proc.verbose ? 'Yes' : 'No'}
              </div>
            </div>
          ))}
        </div>
      ) : selectedTab === 'tasks' ? (
        <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#F8F9FA' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>TASK</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>AGENT</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>EXPECTED OUTPUT</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>STATUS</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map(task => (
                <tr key={task.id} style={{ borderTop: '1px solid #F4F4F4' }}>
                  <td style={{ padding: '14px 16px', fontWeight: 500 }}>{task.description}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12 }}>{task.agent}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280' }}>{task.expectedOutput}</td>
                  <td style={{ padding: '14px 16px' }}>
                    <span style={{ 
                      color: task.status === 'completed' ? '#10B981' : task.status === 'running' ? '#F59E0B' : task.status === 'failed' ? '#DA1E28' : '#6B7280',
                      fontSize: 12, fontWeight: 500, textTransform: 'capitalize',
                    }}>
                      {task.status === 'completed' ? '✓' : task.status === 'running' ? '⏳' : task.status === 'failed' ? '✗' : '○'} {task.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#F8F9FA' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>CREW</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>START</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>END</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>DURATION</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>STATUS</th>
              </tr>
            </thead>
            <tbody>
              {executionLogs.map(log => (
                <tr key={log.id} style={{ borderTop: '1px solid #F4F4F4' }}>
                  <td style={{ padding: '14px 16px', fontWeight: 500 }}>{log.crew}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12 }}>{log.start}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12 }}>{log.end}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12, fontFamily: 'monospace' }}>{log.duration}</td>
                  <td style={{ padding: '14px 16px' }}>
                    <span style={{ color: log.status === 'success' ? '#10B981' : '#DA1E28', fontSize: 12, fontWeight: 500 }}>
                      {log.status === 'success' ? '✓ Success' : '✗ Failed'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Process Detail Modal */}
      {selectedProcess && (
        <div style={{ 
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, 
          background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000,
        }}>
          <div style={{ background: '#fff', borderRadius: 12, padding: 24, maxWidth: 500 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 20 }}>
              <h2 style={{ fontSize: 20, fontWeight: 600 }}>{selectedProcess.name}</h2>
              <button onClick={() => setSelectedProcess(null)} style={{ background: 'none', border: 'none', fontSize: 20, cursor: 'pointer' }}>✕</button>
            </div>
            <div style={{ fontSize: 14, marginBottom: 16 }}>
              <strong>Type:</strong> {selectedProcess.type}
            </div>
            <div style={{ fontSize: 14, marginBottom: 16 }}>
              <strong>Agents:</strong> {selectedProcess.agents.join(' → ')}
            </div>
            <div style={{ background: '#F8F9FA', padding: 16, borderRadius: 8, fontSize: 12, fontFamily: 'monospace' }}>
              # Example usage<br/>
              from crew import Crew, Process<br/><br/>
              crew = Crew(<br/>
              &nbsp;&nbsp;agents=[agent1, agent2, agent3],<br/>
              &nbsp;&nbsp;process=Process.{selectedProcess.type}(),<br/>
              &nbsp;&nbsp;verbose=True<br/>
              )<br/>
              result = crew.kickoff(inputs=&#123;'topic': 'AI'&#125;)
            </div>
          </div>
        </div>
      )}
    </div>
  );
}