'use client';

import { useState } from 'react';

interface Automation {
  id: string;
  name: string;
  trigger: 'cron' | 'event';
  schedule?: string;
  eventSource?: string;
  status: 'active' | 'paused';
  lastRun?: string;
  runs: number;
}

const mockAutomations: Automation[] = [
  { id: 'a1', name: 'Daily Agent Report', trigger: 'cron', schedule: '0 9 * * *', status: 'active', lastRun: '2024-02-01 09:00', runs: 45 },
  { id: 'a2', name: 'PR Review Agent', trigger: 'event', eventSource: 'github', status: 'active', runs: 128 },
  { id: 'a3', name: 'Weekly Cleanup', trigger: 'cron', schedule: '0 2 * * 0', status: 'paused', lastRun: '2024-01-28 02:00', runs: 12 },
  { id: 'a4', name: 'Issue Triage', trigger: 'event', eventSource: 'github', status: 'active', runs: 89 },
];

export default function AutomationPage() {
  const [automations] = useState<Automation[]>(mockAutomations);
  const [showCreate, setShowCreate] = useState(false);

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F4F4F4', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600 }}>Automations</h1>
          <p style={{ color: '#525252' }}>Scheduled and event-triggered workflows</p>
        </div>
        <button onClick={() => setShowCreate(true)} style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 4, cursor: 'pointer' }}>
          + New Automation
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{automations.length}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Total</div>
        </div>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{automations.filter(a => a.status === 'active').length}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Active</div>
        </div>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{automations.filter(a => a.trigger === 'cron').length}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Cron</div>
        </div>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{automations.reduce((a, c) => a + c.runs, 0)}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Total Runs</div>
        </div>
      </div>

      <div style={{ background: '#fff', borderRadius: 4 }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead><tr style={{ background: '#F4F4F4' }}>
            <th style={{ padding: 12, textAlign: 'left' }}>AUTOMATION</th>
            <th style={{ padding: 12, textAlign: 'left' }}>TRIGGER</th>
            <th style={{ padding: 12, textAlign: 'left' }}>SCHEDULE</th>
            <th style={{ padding: 12, textAlign: 'left' }}>STATUS</th>
            <th style={{ padding: 12, textAlign: 'left' }}>RUNS</th>
          </tr></thead>
          <tbody>
            {automations.map(a => (
              <tr key={a.id} style={{ borderBottom: '1px solid #E5E5E5' }}>
                <td style={{ padding: 12, fontWeight: 500 }}>{a.name}</td>
                <td style={{ padding: 12 }}>
                  <span style={{ background: a.trigger === 'cron' ? '#10B98120' : '#7C3AED20', color: a.trigger === 'cron' ? '#10B981' : '#7C3AED', padding: '4px 8px', borderRadius: 4, fontSize: 11 }}>{a.trigger}</span>
                </td>
                <td style={{ padding: 12, fontSize: 12, fontFamily: 'monospace' }}>{a.schedule || a.eventSource}</td>
                <td style={{ padding: 12, color: a.status === 'active' ? '#10B981' : '#8C8C8C', fontSize: 12 }}>{a.status}</td>
                <td style={{ padding: 12, fontSize: 12 }}>{a.runs}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showCreate && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div style={{ background: '#fff', borderRadius: 8, padding: 24, width: 400 }}>
            <h2 style={{ fontSize: 18, marginBottom: 16 }}>Create Automation</h2>
            <input placeholder="Name" style={{ width: '100%', padding: 8, marginBottom: 12, border: '1px solid #E5E5E5', borderRadius: 4 }} />
            <select style={{ width: '100%', padding: 8, marginBottom: 12, border: '1px solid #E5E5E5', borderRadius: 4 }}>
              <option>Cron (schedule)</option>
              <option>Event (webhook)</option>
            </select>
            <input placeholder="Schedule" style={{ width: '100%', padding: 8, marginBottom: 16, border: '1px solid #E5E5E5', borderRadius: 4 }} />
            <div style={{ display: 'flex', gap: 8 }}>
              <button onClick={() => setShowCreate(false)} style={{ flex: 1, padding: 8, border: '1px solid #E5E5E5', borderRadius: 4, cursor: 'pointer' }}>Cancel</button>
              <button style={{ flex: 1, padding: 8, background: '#0F62FE', color: '#fff', border: 'none', borderRadius: 4, cursor: 'pointer' }}>Create</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}