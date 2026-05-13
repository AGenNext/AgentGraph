'use client';

import { useState } from 'react';

interface Channel {
  id: string;
  name: string;
  icon: string;
  type: 'messaging' | 'video' | 'social' | 'email';
  status: 'connected' | 'disconnected' | 'pending';
  lastActivity: string;
  messages: number;
}

const channels: Channel[] = [
  { id: '1', name: 'WhatsApp', icon: '💬', type: 'messaging', status: 'connected', lastActivity: '5 min ago', messages: 1250 },
  { id: '2', name: 'Slack', icon: '💼', type: 'messaging', status: 'connected', lastActivity: '1 min ago', messages: 3420 },
  { id: '3', name: 'Microsoft Teams', icon: '👥', type: 'video', status: 'connected', lastActivity: '30 min ago', messages: 890 },
  { id: '4', name: 'Discord', icon: '🎮', type: 'messaging', status: 'disconnected', lastActivity: '2 days ago', messages: 450 },
  { id: '5', name: 'Telegram', icon: '✈️', type: 'messaging', status: 'pending', lastActivity: '-', messages: 0 },
  { id: '6', name: 'Email', icon: '📧', type: 'email', status: 'connected', lastActivity: '10 min ago', messages: 2100 },
  { id: '7', name: 'Zoom', icon: '📹', type: 'video', status: 'disconnected', lastActivity: '1 week ago', messages: 45 },
  { id: '8', name: 'Twitter/X', icon: '🐦', type: 'social', status: 'connected', lastActivity: '15 min ago', messages: 780 },
];

export default function ChannelsPage() {
  const [selected, setSelected] = useState<string | null>(null);
  const connected = channels.filter(c => c.status === 'connected').length;
  const totalMessages = channels.reduce((a, c) => a + c.messages, 0);

  const connectChannel = (id: string) => {
    alert(`Connect flow for channel ${id} would open OAuth popup`);
  };

  return (
    <div style={{ padding: 24, background: '#0a0e14', minHeight: '100vh', color: '#e6edf3', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 8, color: '#f0f6fc' }}>Channels</h1>
      <p style={{ color: '#8b949e', fontSize: 14, marginBottom: 32 }}>Configure communication channels for your agents</p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 32 }}>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#3fb950' }}>{connected}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Connected</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#58a6ff' }}>{totalMessages.toLocaleString()}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Messages</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#d29922' }}>{channels.filter(c => c.status === 'pending').length}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Pending</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#f778ba' }}>{channels.length}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Total Channels</div>
        </div>
      </div>

      <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Available Channels</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
        {channels.map(channel => (
          <div key={channel.id} onClick={() => setSelected(selected === channel.id ? null : channel.id)} style={{ 
            padding: 20, background: selected === channel.id ? '#1f242c' : '#161b22', 
            borderRadius: 12, border: selected === channel.id ? '2px solid #238636' : '1px solid #30363d', 
            cursor: 'pointer', transition: 'all 0.15s' 
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <span style={{ fontSize: 28 }}>{channel.icon}</span>
                <div>
                  <strong style={{ fontSize: 15, color: '#f0f6fc' }}>{channel.name}</strong>
                  <p style={{ fontSize: 12, color: '#8b949e', textTransform: 'capitalize' }}>{channel.type}</p>
                </div>
              </div>
              <span style={{ padding: '4px 10px', borderRadius: 12, fontSize: 11, fontWeight: 500, 
                background: channel.status === 'connected' ? 'rgba(63, 185, 80, 0.15)' : channel.status === 'pending' ? 'rgba(210, 153, 34, 0.15)' : 'rgba(139, 148, 158, 0.15)', 
                color: channel.status === 'connected' ? '#3fb950' : channel.status === 'pending' ? '#d29922' : '#8b949e' 
              }}>
                {channel.status}
              </span>
            </div>

            {selected === channel.id && (
              <div style={{ marginTop: 12, paddingTop: 12, borderTop: '1px solid #30363d' }}>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, fontSize: 12, marginBottom: 12 }}>
                  <div><span style={{ color: '#8b949e' }}>Last Activity:</span><br /><span style={{ color: '#e6edf3' }}>{channel.lastActivity}</span></div>
                  <div><span style={{ color: '#8b949e' }}>Messages:</span><br /><span style={{ color: '#e6edf3' }}>{channel.messages.toLocaleString()}</span></div>
                </div>
                {channel.status === 'disconnected' && (
                  <button onClick={(e) => { e.stopPropagation(); connectChannel(channel.id); }} style={{ width: '100%', padding: '10px', background: 'linear-gradient(135deg, #238636, #2ea043)', border: 'none', borderRadius: 6, color: '#fff', fontSize: 13, fontWeight: 500, cursor: 'pointer' }}>
                    Connect {channel.name}
                  </button>
                )}
                {channel.status === 'pending' && (
                  <button style={{ width: '100%', padding: '10px', background: '#21262d', border: '1px solid #d29922', borderRadius: 6, color: '#d29922', fontSize: 13, fontWeight: 500, cursor: 'pointer' }}>
                    Complete Setup
                  </button>
                )}
                {channel.status === 'connected' && (
                  <div style={{ display: 'flex', gap: 8 }}>
                    <button style={{ flex: 1, padding: '10px', background: '#21262d', border: '1px solid #30363d', borderRadius: 6, color: '#e6edf3', fontSize: 13, cursor: 'pointer' }}>
                      Settings
                    </button>
                    <button style={{ flex: 1, padding: '10px', background: '#21262d', border: '1px solid #f85149', borderRadius: 6, color: '#f85149', fontSize: 13, cursor: 'pointer' }}>
                      Disconnect
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      <h2 style={{ fontSize: 18, fontWeight: 600, marginTop: 32, marginBottom: 16 }}>Add New Channel</h2>
      <div style={{ padding: 20, background: '#161b22', borderRadius: 12, border: '1px dashed #30363d', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer' }}>
        <span style={{ fontSize: 28, marginRight: 12 }}>➕</span>
        <span style={{ color: '#8b949e' }}>Add another channel</span>
      </div>
    </div>
  );
}