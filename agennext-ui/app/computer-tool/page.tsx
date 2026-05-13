'use client';

import { useState } from 'react';

interface ComputerAction {
  id: string;
  name: string;
  icon: string;
  category: string;
}

const actions: ComputerAction[] = [
  { id: 'click', name: 'Click', icon: '👆', category: 'mouse' },
  { id: 'double_click', name: 'Double Click', icon: '👆👆', category: 'mouse' },
  { id: 'right_click', name: 'Right Click', icon: '📱', category: 'mouse' },
  { id: 'drag', name: 'Drag', icon: '✋', category: 'mouse' },
  { id: 'type', name: 'Type', icon: '⌨️', category: 'keyboard' },
  { id: 'press_key', name: 'Press Key', icon: '🔑', category: 'keyboard' },
  { id: 'screenshot', name: 'Screenshot', icon: '📸', category: 'capture' },
  { id: 'record', name: 'Record', icon: '⏺', category: 'capture' },
  { id: 'open_app', name: 'Open App', icon: '📂', category: 'system' },
  { id: 'close_app', name: 'Close App', icon: '✖️', category: 'system' },
  { id: 'move_file', name: 'Move File', icon: '📁', category: 'filesystem' },
  { id: 'read_file', name: 'Read File', icon: '📄', category: 'filesystem' },
];

const recentActions = [
  { id: '1', action: 'type', details: 'Hello World into terminal', status: 'success' },
  { id: '2', action: 'screenshot', details: 'saved as screen_2024-03-15.png', status: 'success' },
  { id: '3', action: 'click', details: 'at (1024, 568)', status: 'success' },
  { id: '4', action: 'open_app', details: 'Terminal.app', status: 'success' },
  { id: '5', action: 'press_key', details: 'Command+C', status: 'success' },
];

export default function ComputerToolPage() {
  const [selectedAction, setSelectedAction] = useState<string | null>(null);
  const [running, setRunning] = useState(false);
  const [coordinates, setCoordinates] = useState({ x: 0, y: 0 });

  const categories = ['mouse', 'keyboard', 'capture', 'system', 'filesystem'];

  const executeAction = () => {
    setRunning(true);
    setTimeout(() => setRunning(false), 1000);
  };

  return (
    <div style={{ padding: 24, background: '#0a0e14', minHeight: '100vh', color: '#e6edf3', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 8, color: '#f0f6fc' }}>Computer Tool</h1>
      <p style={{ color: '#8b949e', fontSize: 14, marginBottom: 32 }}>Control the computer like a human - mouse, keyboard, and file operations</p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 32 }}>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#58a6ff' }}>{actions.length}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Actions</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#3fb950' }}>192</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Actions Today</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#d29922' }}>2560x1600</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Resolution</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#f778ba' }}>macOS</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Operating System</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: 24 }}>
        <div>
          <div style={{ background: '#161b22', borderRadius: 12, border: '1px solid #30363d', padding: 24, marginBottom: 24, minHeight: 300, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', cursor: 'crosshair' }}>
            <div style={{ fontSize: 48, marginBottom: 12 }}>💻</div>
            <p style={{ color: '#8b949e' }}>Screen {coordinates.x}, {coordinates.y}</p>
            <p style={{ fontSize: 12, color: '#3fb950', marginTop: 8 }}>● Connected</p>
          </div>

          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Recent Actions</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {recentActions.map(action => (
              <div key={action.id} style={{ padding: 10, background: '#161b22', borderRadius: 6, display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ fontSize: 12, color: '#58a6ff', textTransform: 'uppercase' }}>{action.action}</span>
                <span style={{ fontSize: 12, color: '#8b949e' }}>{action.details}</span>
                <span style={{ fontSize: 10, color: '#3fb950' }}>✓</span>
              </div>
            ))}
          </div>
        </div>

        <div>
          {categories.map(cat => (
            <div key={cat} style={{ marginBottom: 16 }}>
              <h3 style={{ fontSize: 13, fontWeight: 600, marginBottom: 8, textTransform: 'capitalize', color: '#8b949e' }}>{cat}</h3>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 6 }}>
                {actions.filter(a => a.category === cat).map(action => (
                  <div key={action.id} onClick={() => setSelectedAction(action.id)} style={{ 
                    padding: 10, background: selectedAction === action.id ? '#238636' : '#161b22', 
                    borderRadius: 6, cursor: 'pointer', textAlign: 'center'
                  }}>
                    <div style={{ fontSize: 16, marginBottom: 2 }}>{action.icon}</div>
                    <div style={{ fontSize: 11, color: '#e6edf3' }}>{action.name}</div>
                  </div>
                ))}
              </div>
            </div>
          ))}

          {selectedAction && (
            <div style={{ padding: 16, background: '#161b22', borderRadius: 8, border: '1px solid #30363d', marginTop: 16 }}>
              <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>Execute {actions.find(a => a.id === selectedAction)?.name}</h3>
              <input placeholder="Parameters (e.g., coordinates, text)" style={{ width: '100%', padding: 8, background: '#0d1117', border: '1px solid #30363d', borderRadius: 6, color: '#e6edf3', fontSize: 13, marginBottom: 12 }} />
              <button onClick={executeAction} disabled={running} style={{ width: '100%', padding: 10, background: running ? '#21262d' : 'linear-gradient(135deg, #238636, #2ea043)', border: 'none', borderRadius: 6, color: '#fff', fontSize: 13, fontWeight: 500, cursor: running ? 'default' : 'pointer' }}>
                {running ? '⟳ Executing...' : '▶ Execute'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}