'use client';

import { useState } from 'react';

interface BrowserAction {
  id: string;
  action: string;
  selector: string;
  description: string;
}

const actions: BrowserAction[] = [
  { id: '1', action: 'navigate', selector: 'url', description: 'Navigate to a URL' },
  { id: '2', action: 'click', selector: '#id or .class', description: 'Click an element' },
  { id: '3', action: 'type', selector: 'input[name="x"]', description: 'Enter text into an input' },
  { id: '4', action: 'scroll', selector: 'selector', description: 'Scroll to an element' },
  { id: '5', action: 'screenshot', selector: 'viewport', description: 'Take a screenshot' },
  { id: '6', action: 'extract', selector: 'div.content', description: 'Extract content from element' },
  { id: '7', action: 'wait', selector: '.loaded', description: 'Wait for element' },
  { id: '8', action: 'evaluate', selector: 'js expression', description: 'Run JavaScript in page' },
];

const recentRuns = [
  { id: '1', action: 'navigate', target: 'github.com/agennext', status: 'success', duration: '1.2s' },
  { id: '2', action: 'screenshot', target: 'homepage.png', status: 'success', duration: '0.3s' },
  { id: '3', action: 'click', target: '#login-btn', status: 'success', duration: '0.1s' },
  { id: '4', action: 'type', target: 'input#email', status: 'success', duration: '0.5s' },
  { id: '5', action: 'extract', target: '.repo-list', status: 'success', duration: '0.8s' },
];

export default function BrowserToolPage() {
  const [selectedAction, setSelectedAction] = useState<string>('navigate');
  const [target, setTarget] = useState('');
  const [running, setRunning] = useState(false);
  const [url, setUrl] = useState('https://example.com');

  const activeAction = actions.find(a => a.id === selectedAction) || actions[0];

  const executeAction = () => {
    setRunning(true);
    setTimeout(() => setRunning(false), 1500);
  };

  return (
    <div style={{ padding: 24, background: '#0a0e14', minHeight: '100vh', color: '#e6edf3', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 8, color: '#f0f6fc' }}>Browser Tool</h1>
      <p style={{ color: '#8b949e', fontSize: 14, marginBottom: 32 }}>Automate browser interactions for web scraping and testing</p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 32 }}>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#58a6ff' }}>8</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Actions</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#3fb950' }}>156</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Runs Today</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#d29922' }}>98.5%</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Success Rate</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 400px', gap: 24 }}>
        <div>
          <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
            <input value={url} onChange={e => setUrl(e.target.value)} placeholder="https://example.com" style={{ flex: 1, padding: 10, background: '#161b22', border: '1px solid #30363d', borderRadius: 8, color: '#e6edf3', fontSize: 13 }} />
            <button style={{ padding: '10px 16px', background: '#238636', border: 'none', borderRadius: 8, color: '#fff', fontSize: 12, cursor: 'pointer' }}>Launch Browser</button>
          </div>

          <div style={{ background: '#161b22', borderRadius: 12, border: '1px solid #30363d', padding: 16, minHeight: 300, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column' }}>
            <div style={{ fontSize: 48, marginBottom: 12 }}>🌐</div>
            <p style={{ color: '#8b949e' }}>{url}</p>
            <p style={{ fontSize: 12, color: '#3fb950', marginTop: 8 }}>● Connected</p>
          </div>

          <h2 style={{ fontSize: 16, fontWeight: 600, marginTop: 24, marginBottom: 12 }}>Recent Runs</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {recentRuns.map(run => (
              <div key={run.id} style={{ padding: 10, background: '#161b22', borderRadius: 6, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
                  <span style={{ fontSize: 11, color: '#58a6ff', textTransform: 'uppercase' }}>{run.action}</span>
                  <span style={{ fontSize: 12, color: '#8b949e' }}>{run.target}</span>
                </div>
                <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                  <span style={{ fontSize: 10, color: run.status === 'success' ? '#3fb950' : '#f85149' }}>{run.status}</span>
                  <span style={{ fontSize: 10, color: '#8b949e' }}>{run.duration}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Actions</h2>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginBottom: 24 }}>
            {actions.map(action => (
              <div key={action.id} onClick={() => setSelectedAction(action.id)} style={{ 
                padding: 12, background: selectedAction === action.id ? '#1f242c' : '#161b22', 
                borderRadius: 8, border: selectedAction === action.id ? '2px solid #238636' : '1px solid #30363d', 
                cursor: 'pointer'
              }}>
                <strong style={{ fontSize: 13, color: '#f0f6fc', textTransform: 'uppercase' }}>{action.action}</strong>
                <p style={{ fontSize: 11, color: '#8b949e', marginTop: 2 }}>{action.description}</p>
              </div>
            ))}
          </div>

          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Execute</h2>
          <div style={{ padding: 16, background: '#161b22', borderRadius: 8, border: '1px solid #30363d' }}>
            <div style={{ marginBottom: 8 }}>
              <label style={{ fontSize: 12, color: '#8b949e' }}>Action</label>
              <div style={{ padding: '8px 12px', background: '#0d1117', borderRadius: 6, fontSize: 13, color: '#58a6ff' }}>{activeAction.action}</div>
            </div>
            <div style={{ marginBottom: 12 }}>
              <label style={{ fontSize: 12, color: '#8b949e' }}>Selector / Target</label>
              <input value={target} onChange={e => setTarget(e.target.value)} placeholder={activeAction.selector} style={{ width: '100%', padding: 8, background: '#0d1117', border: '1px solid #30363d', borderRadius: 6, color: '#e6edf3', fontSize: 13 }} />
            </div>
            <button onClick={executeAction} disabled={running || !target} style={{ width: '100%', padding: 10, background: !target || running ? '#21262d' : 'linear-gradient(135deg, #238636, #2ea043)', border: 'none', borderRadius: 6, color: '#fff', fontSize: 13, fontWeight: 500, cursor: target && !running ? 'pointer' : 'default' }}>
              {running ? '⟳ Running...' : '▶ Execute'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}