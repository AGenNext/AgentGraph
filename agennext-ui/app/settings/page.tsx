'use client';

import { useState } from 'react';

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    theme: 'dark',
    language: 'en',
    notifications: true,
    telemetry: false,
    defaultFramework: 'langgraph',
    defaultLLM: 'gpt-4o',
  });

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F4F4F4', minHeight: '100vh' }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 24 }}>Settings</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
        <div style={{ background: '#fff', padding: 24, borderRadius: 4 }}>
          <h2 style={{ fontSize: 16, marginBottom: 16 }}>General</h2>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', fontSize: 12, marginBottom: 4 }}>Theme</label>
            <select value={settings.theme} onChange={e => setSettings({...settings, theme: e.target.value})}
              style={{ width: '100%', padding: 8, borderRadius: 4, border: '1px solid #E5E5E5' }}>
              <option value="light">Light</option>
              <option value="dark">Dark</option>
              <option value="system">System</option>
            </select>
          </div>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', fontSize: 12, marginBottom: 4 }}>Language</label>
            <select value={settings.language}
              style={{ width: '100%', padding: 8, borderRadius: 4, border: '1px solid #E5E5E5' }}>
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="zh">Chinese</option>
            </select>
          </div>
        </div>

        <div style={{ background: '#fff', padding: 24, borderRadius: 4 }}>
          <h2 style={{ fontSize: 16, marginBottom: 16 }}>Defaults</h2>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', fontSize: 12, marginBottom: 4 }}>Framework</label>
            <select value={settings.defaultFramework}
              style={{ width: '100%', padding: 8, borderRadius: 4, border: '1px solid #E5E5E5' }}>
              <option value="langgraph">LangGraph</option>
              <option value="crewai">CrewAI</option>
              <option value="autogen">AutoGen</option>
            </select>
          </div>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', fontSize: 12, marginBottom: 4 }}>LLM</label>
            <select value={settings.defaultLLM}
              style={{ width: '100%', padding: 8, borderRadius: 4, border: '1px solid #E5E5E5' }}>
              <option value="gpt-4o">GPT-4o</option>
              <option value="claude-3">Claude 3</option>
              <option value="gemini-pro">Gemini Pro</option>
            </select>
          </div>
        </div>

        <div style={{ background: '#fff', padding: 24, borderRadius: 4 }}>
          <h2 style={{ fontSize: 16, marginBottom: 16 }}>Privacy</h2>
          <label style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
            <input type="checkbox" checked={settings.notifications} onChange={e => setSettings({...settings, notifications: e.target.checked})} />
            <span>Enable notifications</span>
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <input type="checkbox" checked={settings.telemetry} onChange={e => setSettings({...settings, telemetry: e.target.checked})} />
            <span>Send telemetry</span>
          </label>
        </div>

        <div style={{ background: '#fff', padding: 24, borderRadius: 4 }}>
          <h2 style={{ fontSize: 16, marginBottom: 16 }}>Account</h2>
          <p style={{ fontSize: 13, color: '#525252' }}>Manage your account settings and preferences.</p>
          <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '8px 16px', borderRadius: 4, marginTop: 8 }}>
            Sign Out
          </button>
        </div>
      </div>
    </div>
  );
}