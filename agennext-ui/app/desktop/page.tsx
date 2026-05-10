'use client';

import { useState } from 'react';

interface Agent {
  id: string;
  name: string;
  status: 'active' | 'idle';
  lastUsed: string;
}

const agents: Agent[] = [
  { id: 'a1', name: 'Research Agent', status: 'active', lastUsed: '2 min ago' },
  { id: 'a2', name: 'Writer Agent', status: 'active', lastUsed: '5 min ago' },
  { id: 'a3', name: 'Analyzer Agent', status: 'idle', lastUsed: '1 hour ago' },
];

const recentChats = [
  { id: 'c1', agent: 'Research Agent', messages: 12, preview: 'Can you summarize this research paper?', time: '2 min ago' },
  { id: 'c2', agent: 'Writer Agent', messages: 8, preview: 'Write a blog post about...', time: '5 min ago' },
  { id: 'c3', agent: 'Analyzer Agent', messages: 24, preview: 'Analyze this dataset', time: '1 hour ago' },
];

export default function DesktopAppPage() {
  const [chats, setChats] = useState(recentChats);
  
  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'IBM Plex Sans, sans-serif', background: '#1A1A2E' }}>
      {/* Sidebar */}
      <div style={{ width: 260, borderRight: '1px solid #2D2D44', display: 'flex', flexDirection: 'column' }}>
        {/* Logo */}
        <div style={{ padding: 20, borderBottom: '1px solid #2D2D44' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{ width: 32, height: 32, background: 'linear-gradient(135deg, #667EEA, #764BA2)', borderRadius: 8, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontWeight: 700, fontSize: 16 }}>
              A
            </div>
            <span style={{ color: '#fff', fontWeight: 600 }}>AGenNext</span>
          </div>
        </div>

        {/* Quick Actions */}
        <div style={{ padding: 16 }}>
          <button style={{ width: '100%', background: '#667EEA', color: '#fff', border: 'none', padding: '12px 16px', borderRadius: 8, fontSize: 14, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8 }}>
            <span>+</span> New Chat
          </button>
        </div>

        {/* Agents */}
        <div style={{ flex: 1, padding: '0 16px', overflow: 'auto' }}>
          <div style={{ fontSize: 11, color: '#6B7280', marginBottom: 8, textTransform: 'uppercase', letterSpacing: 1 }}>Your Agents</div>
          {agents.map(agent => (
            <div key={agent.id} style={{ padding: '10px 12px', borderRadius: 8, marginBottom: 4, cursor: 'pointer', color: '#A0A0B8', display: 'flex', alignItems: 'center', gap: 10 }}>
              <span style={{ width: 8, height: 8, borderRadius: '50%', background: agent.status === 'active' ? '#10B981' : '#6B7280' }} />
              {agent.name}
            </div>
          ))}
        </div>

        {/* Footer */}
        <div style={{ padding: 16, borderTop: '1px solid #2D2D44' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, color: '#A0A0B8', fontSize: 12 }}>
            <div style={{ width: 28, height: 28, borderRadius: '50%', background: '#667EEA', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: 11 }}>
              JD
            </div>
            <div>
              <div style={{ color: '#fff', fontSize: 12 }}>John Doe</div>
              <div style={{ fontSize: 10 }}>Pro Plan</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Chat */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <div style={{ padding: '16px 24px', borderBottom: '1px solid #2D2D44', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ color: '#fff', fontSize: 16, fontWeight: 500 }}>Research Agent</div>
          <div style={{ display: 'flex', gap: 8 }}>
            <button style={{ background: 'transparent', border: '1px solid #2D2D44', color: '#fff', padding: '8px 12px', borderRadius: 6, fontSize: 12, cursor: 'pointer' }}>⚙️</button>
            <button style={{ background: 'transparent', border: '1px solid #2D2D44', color: '#fff', padding: '8px 12px', borderRadius: 6, fontSize: 12, cursor: 'pointer' }}>📤</button>
          </div>
        </div>

        {/* Messages */}
        <div style={{ flex: 1, padding: 24, overflow: 'auto' }}>
          {chats.map(chat => (
            <div key={chat.id} style={{ marginBottom: 24 }}>
              <div style={{ display: 'flex', gap: 12, marginBottom: 8 }}>
                <div style={{ width: 32, height: 32, borderRadius: 8, background: '#667EEA', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: 12, flexShrink: 0 }}>You</div>
                <div style={{ color: '#fff', fontSize: 14 }}>{chat.preview}</div>
              </div>
              <div style={{ display: 'flex', gap: 12 }}>
                <div style={{ width: 32, height: 32, borderRadius: 8, background: '#764BA2', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: 12, flexShrink: 0 }}>AI</div>
                <div style={{ color: '#A0A0B8', fontSize: 14, background: '#2D2D44', padding: 12, borderRadius: '0 12 12 12', maxWidth: 500 }}>
                  I've analyzed that request. Here's a comprehensive summary of the key findings from the research paper you provided. The main points are: [analysis would appear here]
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Input */}
        <div style={{ padding: 24, borderTop: '1px solid #2D2D44' }}>
          <div style={{ display: 'flex', gap: 12, background: '#2D2D44', padding: 12, borderRadius: 12 }}>
            <input 
              placeholder="Message Research Agent..." 
              style={{ flex: 1, background: 'transparent', border: 'none', outline: 'none', color: '#fff', fontSize: 14 }}
            />
            <button style={{ background: '#667EEA', color: '#fff', border: 'none', padding: '8px 16px', borderRadius: 8, fontSize: 12, cursor: 'pointer' }}>
              Send
            </button>
          </div>
        </div>
      </div>

      {/* Right Panel */}
      <div style={{ width: 280, borderLeft: '1px solid #2D2D44', padding: 16, display: 'flex', flexDirection: 'column' }}>
        <div style={{ color: '#fff', fontSize: 12, fontWeight: 600, marginBottom: 16 }}>Capabilities</div>
        <div style={{ background: '#2D2D44', borderRadius: 8, padding: 12, marginBottom: 8 }}>
          <div style={{ color: '#fff', fontSize: 12, fontWeight: 500, marginBottom: 4 }}>Web Search</div>
          <div style={{ color: '#6B7280', fontSize: 11 }}>Enabled</div>
        </div>
        <div style={{ background: '#2D2D44', borderRadius: 8, padding: 12, marginBottom: 8 }}>
          <div style={{ color: '#fff', fontSize: 12, fontWeight: 500, marginBottom: 4 }}>Knowledge Base</div>
          <div style={{ color: '#6B7280', fontSize: 11 }}>3 sources loaded</div>
        </div>
        <div style={{ background: '#2D2D44', borderRadius: 8, padding: 12, marginBottom: 8 }}>
          <div style={{ color: '#fff', fontSize: 12, fontWeight: 500, marginBottom: 4 }}>Image Analysis</div>
          <div style={{ color: '#6B7280', fontSize: 11 }}>Enabled</div>
        </div>
      </div>
    </div>
  );
}