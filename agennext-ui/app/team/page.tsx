'use client';

import { useState } from 'react';

interface TeamMember {
  id: string;
  name: string;
  role: string;
  framework: string;
}

interface AgentTeam {
  id: string;
  name: string;
  pattern: 'sequential' | 'parallel' | 'hierarchical';
  members: TeamMember[];
  status: string;
}

const mockTeams: AgentTeam[] = [
  { id: '1', name: 'Research Team', pattern: 'sequential', members: [
    { id: 'm1', name: 'Researcher', role: 'research', framework: 'langgraph' },
    { id: 'm2', name: 'Summarizer', role: 'write', framework: 'crewai' },
  ], status: 'active' },
  { id: '2', name: 'Analysis Pipeline', pattern: 'parallel', members: [
    { id: 'm3', name: 'Data Agent', role: 'analyze', framework: 'autogen' },
    { id: 'm4', name: 'Visual Agent', role: 'visualize', framework: 'langchain' },
  ], status: 'active' },
];

export default function TeamPage() {
  const [teams] = useState<AgentTeam[]>(mockTeams);
  const [selected, setSelected] = useState<AgentTeam | null>(null);

  const patternIcons = { sequential: '→', parallel: '⫸', hierarchical: '⬡' };

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F4F4F4', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600 }}>Agent Teams</h1>
          <p style={{ color: '#525252' }}>Multi-agent orchestration patterns</p>
        </div>
        <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 4 }}>
          + New Team
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{teams.length}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Total Teams</div>
        </div>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{teams.filter(t => t.status === 'active').length}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Active</div>
        </div>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{teams.reduce((a, t) => a + t.members.length, 0)}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Total Agents</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <div style={{ background: '#fff', borderRadius: 4, padding: 16 }}>
          <h3 style={{ fontSize: 14, marginBottom: 16 }}>Teams</h3>
          {teams.map(team => (
            <div key={team.id} onClick={() => setSelected(team)}
              style={{ padding: 12, borderRadius: 4, marginBottom: 8, background: selected?.id === team.id ? '#F4F4F4' : '#F9FAFB', cursor: 'pointer', border: '1px solid #E5E5E5' }}>
              <div style={{ fontWeight: 500 }}>{team.name}</div>
              <div style={{ fontSize: 12, color: '#525252' }}>{patternIcons[team.pattern]} {team.pattern} • {team.members.length} agents</div>
            </div>
          ))}
        </div>

        <div style={{ background: '#fff', borderRadius: 4, padding: 16 }}>
          <h3 style={{ fontSize: 14, marginBottom: 16 }}>Team Details</h3>
          {selected ? (
            <div>
              <div style={{ fontSize: 20, fontWeight: 600, marginBottom: 16 }}>{selected.name}</div>
              <div style={{ fontSize: 12, marginBottom: 16, color: '#525252' }}>Pattern: {selected.pattern}</div>
              <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 8 }}>Members</div>
              {selected.members.map(m => (
                <div key={m.id} style={{ padding: 8, background: '#F4F4F4', borderRadius: 4, marginBottom: 4, fontSize: 13 }}>
                  <span style={{ fontWeight: 500 }}>{m.name}</span> • <span style={{ color: '#525252' }}>{m.role}</span>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ color: '#8C8C8C' }}>Select a team</div>
          )}
        </div>
      </div>
    </div>
  );
}