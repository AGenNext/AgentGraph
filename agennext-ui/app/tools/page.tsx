'use client';

import { useState, useEffect } from 'react';

interface Tool {
  id: string;
  name: string;
  description: string;
  framework: string;
}

export default function ToolsPage() {
  const [tools, setTools] = useState<Tool[]>([]);
  const [framework, setFramework] = useState<string>('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/tools' + (framework !== 'all' ? `?framework=${framework}` : ''))
      .then(r => r.json())
      .then(d => setTools(d.tools || []))
      .finally(() => setLoading(false));
  }, [framework]);

  return (
    <div style={{ padding: 24, background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <h1 style={{ fontSize: 24, marginBottom: 20 }}>Agent Tools</h1>
      
      <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
        {['all', 'langgraph', 'langchain', 'autogen', 'crewai'].map(f => (
          <button key={f} onClick={() => setFramework(f)} style={{
            padding: '8px 16px', background: framework === f ? '#238636' : '#21262D',
            border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer'
          }}>
            {f}
          </button>
        ))}
      </div>

      {loading ? <p>Loading...</p> : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {tools.map(tool => (
            <div key={tool.id} style={{
              padding: 16, background: '#21262D', borderRadius: 8
            }}>
              <strong>{tool.name}</strong>
              <p style={{ color: '#8C8C8C', margin: '4px 0' }}>{tool.description}</p>
              <span style={{ fontSize: 12, color: '#58A6FF' }}>{tool.framework}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}