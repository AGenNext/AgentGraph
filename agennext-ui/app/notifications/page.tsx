'use client';

import { useState } from 'react';

interface Notification {
  id: string;
  type: 'approval' | 'task' | 'agent' | 'system';
  title: string;
  message: string;
  read: boolean;
  time: string;
}

const mockNotifs: Notification[] = [
  { id: 'n1', type: 'approval', title: 'New Agent Request', message: 'John requests "Data Analyzer" agent', read: false, time: '2 min ago' },
  { id: 'n2', type: 'task', title: 'Task Completed', message: 'Analyze Q4 data finished', read: false, time: '5 min ago' },
  { id: 'n3', type: 'agent', title: 'Agent Active', message: 'Report Writer is now running', read: true, time: '1 hour ago' },
  { id: 'n4', type: 'system', title: 'System Update', message: 'New version available', read: true, time: '1 day ago' },
];

const typeIcons = { approval: '📋', task: '✅', agent: '🤖', system: '⚙️' };

export default function NotificationsPage() {
  const [notifs, setNotifs] = useState<Notification[]>(mockNotifs);

  const markRead = (id: string) => {
    setNotifs(notifs.map(n => n.id === id ? { ...n, read: true } : n));
  };

  const markAllRead = () => {
    setNotifs(notifs.map(n => ({ ...n, read: true })));
  };

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F4F4F4', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600 }}>Notifications</h1>
          <p style={{ color: '#525252' }}>Stay updated on your agents</p>
        </div>
        <button onClick={markAllRead} style={{ background: '#E5E5E5', border: 'none', padding: '8px 16px', borderRadius: 4, cursor: 'pointer' }}>
          Mark all read
        </button>
      </div>

      <div style={{ background: '#fff', borderRadius: 4 }}>
        {notifs.map(notif => (
          <div key={notif.id} 
            onClick={() => markRead(notif.id)}
            style={{ 
              padding: 16, 
              borderBottom: '1px solid #E5E5E5', 
              cursor: 'pointer',
              background: notif.read ? '#fff' : '#F0F5FF',
              display: 'flex',
              gap: 12,
              alignItems: 'flex-start',
            }}>
            <span style={{ fontSize: 20 }}>{typeIcons[notif.type]}</span>
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: notif.read ? 400 : 600, fontSize: 14 }}>{notif.title}</div>
              <div style={{ fontSize: 13, color: '#525252' }}>{notif.message}</div>
              <div style={{ fontSize: 11, color: '#8C8C8C', marginTop: 4 }}>{notif.time}</div>
            </div>
            {!notif.read && <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#0F62FE' }} />}
          </div>
        ))}
      </div>
    </div>
  );
}