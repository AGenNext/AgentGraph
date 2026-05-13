'use client';

import { useState } from 'react';

interface SystemPrompt {
  id: string;
  name: string;
  role: string;
  content: string;
  version: string;
  lastModified: string;
  tokens: number;
}

const prompts: SystemPrompt[] = [
  { id: '1', name: 'Default Assistant', role: 'assistant', version: 'v2.3', lastModified: '2024-03-15T10:00:00Z', tokens: 450 },
  { id: '2', name: 'Research Agent', role: 'research', version: 'v1.8', lastModified: '2024-03-14T16:30:00Z', tokens: 680 },
  { id: '3', name: 'Code Reviewer', role: 'code', version: 'v3.1', lastModified: '2024-03-14T14:00:00Z', tokens: 520 },
  { id: '4', name: 'Customer Support', role: 'support', version: 'v2.0', lastModified: '2024-03-13T09:00:00Z', tokens: 380 },
  { id: '5', name: '数据分析员', role: 'analytics', version: 'v1.5', lastModified: '2024-03-12T11:00:00Z', tokens: 290 },
];

const defaultPrompt = `You are Agent Zero, an enterprise AI agent orchestration platform.

## Core Capabilities
- Orchestrate multiple child agents
- Delegate tasks to specialized agents
- Monitor and evaluate agent performance
- Ensure compliance and security

## Guidelines
1. Always prioritize user privacy
2. Validate all tool inputs
3. Log significant decisions
4. Request approval for sensitive actions

## agent_type:
- Research: Web search, analysis, summarization
- Code: Generation, review, debugging
- Writing: Content creation, editing
- Support: Customer assistance

Always respond concisely and accurately.`;

export default function SystemPromptPage() {
  const [selected, setSelected] = useState<string>('1');
  const [content, setContent] = useState(defaultPrompt);
  const [isEditing, setIsEditing] = useState(false);

  const activePrompt = prompts.find(p => p.id === selected) || prompts[0];
  const totalTokens = prompts.reduce((a, p) => a + p.tokens, 0);

  return (
    <div style={{ padding: 24, background: '#0a0e14', minHeight: '100vh', color: '#e6edf3', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 8, color: '#f0f6fc' }}>System Prompts</h1>
      <p style={{ color: '#8b949e', fontSize: 14, marginBottom: 32 }}>Configure agent instructions & behavior</p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 32 }}>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#58a6ff' }}>{prompts.length}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Prompt Templates</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#3fb950' }}>{(totalTokens / 10).toFixed(1)}k</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Total Tokens</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#d29922' }}>{Math.max(...prompts.map(p => parseInt(p.version.split('.')[1]))).toFixed(0)}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Latest Version</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '280px 1fr', gap: 24 }}>
        <div>
          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Templates</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {prompts.map(p => (
              <div key={p.id} onClick={() => { setSelected(p.id); setContent(defaultPrompt); setIsEditing(false); }} style={{ 
                padding: 12, background: selected === p.id ? '#1f242c' : '#161b22', 
                borderRadius: 8, border: selected === p.id ? '2px solid #238636' : '1px solid #30363d', 
                cursor: 'pointer' 
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <strong style={{ fontSize: 14, color: '#f0f6fc' }}>{p.name}</strong>
                  <span style={{ fontSize: 11, color: '#8b949e' }}>{p.version}</span>
                </div>
                <p style={{ fontSize: 12, color: '#8b949e', marginTop: 4 }}>Role: {p.role}</p>
              </div>
            ))}
            <button style={{ padding: 12, background: '#21262d', border: '1px dashed #30363d', borderRadius: 8, color: '#8b949e', fontSize: 14, cursor: 'pointer', marginTop: 8 }}>
              ➕ New Prompt
            </button>
          </div>
        </div>

        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <h2 style={{ fontSize: 16, fontWeight: 600 }}>{activePrompt.name}</h2>
            <div style={{ display: 'flex', gap: 8 }}>
              <button onClick={() => setIsEditing(!isEditing)} style={{ padding: '6px 12px', background: isEditing ? '#238636' : '#21262d', border: '1px solid #30363d', borderRadius: 6, color: '#fff', fontSize: 12, cursor: 'pointer' }}>
                {isEditing ? 'Save' : 'Edit'}
              </button>
              <button style={{ padding: '6px 12px', background: '#21262d', border: '1px solid #30363d', borderRadius: 6, color: '#fff', fontSize: 12, cursor: 'pointer' }}>
                Duplicate
              </button>
              <button style={{ padding: '6px 12px', background: '#f8514922', border: '1px solid #f85149', borderRadius: 6, color: '#f85149', fontSize: 12, cursor: 'pointer' }}>
                Delete
              </button>
            </div>
          </div>
          
          {isEditing ? (
            <textarea value={content} onChange={e => setContent(e.target.value)} style={{ width: '100%', minHeight: 400, padding: 16, background: '#0d1117', border: '1px solid #30363d', borderRadius: 8, color: '#e6edf3', fontSize: 13, fontFamily: 'monospace', lineHeight: 1.6, resize: 'vertical' }} />
          ) : (
            <pre style={{ padding: 16, background: '#0d1117', borderRadius: 8, fontSize: 13, fontFamily: 'monospace', lineHeight: 1.6, whiteSpace: 'pre-wrap', overflow: 'auto', maxHeight: 400 }}>
{content}
            </pre>
          )}

          <div style={{ display: 'flex', gap: 16, marginTop: 12, fontSize: 12, color: '#8b949e' }}>
            <span>Version: {activePrompt.version}</span>
            <span>Tokens: ~{activePrompt.tokens}</span>
            <span>Modified: {new Date(activePrompt.lastModified).toLocaleDateString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
}