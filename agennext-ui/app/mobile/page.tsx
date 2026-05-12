'use client';

import { useState } from 'react';

interface Chat {
  id: string;
  agentName: string;
  lastMessage: string;
  time: string;
  unread: boolean;
}

const chats: Chat[] = [
  { id: 'c1', agentName: 'Research Agent', lastMessage: 'Can you summarize this?', time: '2m', unread: true },
  { id: 'c2', agentName: 'Writer Agent', lastMessage: 'Blog post drafted', time: '15m', unread: true },
  { id: 'c3', agentName: 'Analyzer Agent', lastMessage: 'Analysis complete', time: '1h', unread: false },
];

const agents = [
  { id: 'a1', name: 'Research Agent', icon: '🔬', color: '#667EEA' },
  { id: 'a2', name: 'Writer Agent', icon: '✍️', color: '#10B981' },
  { id: 'a3', name: 'Analyzer Agent', icon: '📊', color: '#F59E0B' },
  { id: 'a4', name: 'Triage Agent', icon: '📋', color: '#DA1E28' },
  { id: 'a5', name: 'Code Agent', icon: '💻', color: '#7C3AED' },
];

export default function MobileAppPage() {
  const [activeTab, setActiveTab] = useState<'chat' | 'agents' | 'discover'>('chat');
  const [chatsList] = useState<Chat[]>(chats);

  return (
    <div style={{ maxWidth: 393, margin: '0 auto', height: '100vh', fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', position: 'relative' }}>
      {/* Status Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 16px', background: '#fff', fontSize: 12, color: '#6B7280' }}>
        <span>9:41</span>
        <span>📶 🔋</span>
      </div>

      {/* Header */}
      <div style={{ padding: '16px', background: '#1A1A2E', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <h1 style={{ color: '#fff', fontSize: 20, fontWeight: 600, margin: 0 }}>AGenNext</h1>
          <p style={{ color: '#6B7280', fontSize: 12, margin: '4px 0 0 0' }}>Enterprise</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button style={{ background: '#2D2D44', border: 'none', width: 36, height: 36, borderRadius: 10, color: '#fff', fontSize: 16 }}>🔔</button>
          <button style={{ background: '#667EEA', border: 'none', width: 36, height: 36, borderRadius: 10, color: '#fff', fontSize: 16, fontWeight: 700 }}>+</button>
        </div>
      </div>

      {/* Main Content */}
      <div style={{ flex: 1, overflow: 'auto' }}>
        {activeTab === 'chat' ? (
          <div>
            {/* Quick Start */}
            <div style={{ padding: 16 }}>
              <div style={{ fontSize: 12, color: '#6B7280', marginBottom: 12 }}>Quick Start</div>
              <div style={{ display: 'flex', gap: 8, overflowX: 'auto', paddingBottom: 8 }}>
                <button style={{ background: '#fff', border: '1px solid #E5E5E5', padding: '10px 14px', borderRadius: 8, fontSize: 12, whiteSpace: 'nowrap', cursor: 'pointer' }}>
                  🔬 Research
                </button>
                <button style={{ background: '#fff', border: '1px solid #E5E5E5', padding: '10px 14px', borderRadius: 8, fontSize: 12, whiteSpace: 'nowrap', cursor: 'pointer' }}>
                  ✍️ Write
                </button>
                <button style={{ background: '#fff', border: '1px solid #E5E5E5', padding: '10px 14px', borderRadius: 8, fontSize: 12, whiteSpace: 'nowrap', cursor: 'pointer' }}>
                  📊 Analyze
                </button>
                <button style={{ background: '#fff', border: '1px solid #E5E5E5', padding: '10px 14px', borderRadius: 8, fontSize: 12, whiteSpace: 'nowrap', cursor: 'pointer' }}>
                  💻 Code
                </button>
              </div>
            </div>

            {/* Chats */}
            <div style={{ padding: '0 16px' }}>
              <div style={{ fontSize: 12, color: '#6B7280', marginBottom: 12 }}>Recent Chats</div>
              {chatsList.map(chat => (
                <div key={chat.id} style={{ background: '#fff', borderRadius: 12, padding: 14, marginBottom: 8, display: 'flex', alignItems: 'center', gap: 12, boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
                  <div style={{ width: 44, height: 44, borderRadius: 12, background: '#667EEA', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 20 }}>
                    {chat.agentName.charAt(0)}
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 2 }}>{chat.agentName}</div>
                    <div style={{ fontSize: 12, color: '#6B7280', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: 200 }}>
                      {chat.lastMessage}
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: 11, color: '#6B7280' }}>{chat.time}</div>
                    {chat.unread && <div style={{ width: 8, height: 8, borderRadius: '50%', background: '#667EEA', marginLeft: 'auto', marginTop: 4 }} />}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : activeTab === 'agents' ? (
          <div style={{ padding: 16 }}>
            <div style={{ fontSize: 12, color: '#6B7280', marginBottom: 12 }}>All Agents</div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 8 }}>
              {agents.map(agent => (
                <div key={agent.id} style={{ background: '#fff', borderRadius: 12, padding: 16, textAlign: 'center', boxShadow: '0 1px 3px rgba(0,0,0,0.05)', cursor: 'pointer' }}>
                  <div style={{ width: 48, height: 48, borderRadius: 12, background: agent.color + '20', margin: '0 auto 8px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 24 }}>
                    {agent.icon}
                  </div>
                  <div style={{ fontSize: 13, fontWeight: 500 }}>{agent.name}</div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div style={{ padding: 16, textAlign: 'center', paddingTop: 80 }}>
            <div style={{ fontSize: 48, marginBottom: 16 }}>🔍</div>
            <div style={{ fontSize: 16, fontWeight: 500, marginBottom: 8 }}>Discover Agents</div>
            <div style={{ fontSize: 13, color: '#6B7280' }}>Coming soon - Agent marketplace</div>
          </div>
        )}
      </div>

      {/* Bottom Nav */}
      <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, background: '#fff', borderTop: '1px solid #E5E5E5', display: 'flex', padding: '8px 0' }}>
        {[
          { id: 'chat', icon: '💬', label: 'Chat' },
          { id: 'agents', icon: '🤖', label: 'Agents' },
          { id: 'discover', icon: '🔍', label: 'Discover' },
          { id: 'profile', icon: '👤', label: 'Profile' },
        ].map(item => (
          <button
            key={item.id}
            onClick={() => setActiveTab(item.id as 'chat' | 'agents' | 'discover')}
            style={{
              flex: 1,
              background: 'transparent',
              border: 'none',
              padding: '8px 0',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 2,
              cursor: 'pointer',
            }}
          >
            <span style={{ fontSize: 20 }}>{item.icon}</span>
            <span style={{ fontSize: 10, color: activeTab === item.id ? '#667EEA' : '#6B7280' }}>{item.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}