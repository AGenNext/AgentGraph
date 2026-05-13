'use client';

import { useState } from 'react';

interface Artifact {
  id: string;
  name: string;
  type: 'document' | 'image' | 'code' | 'data' | 'agent';
  size: string;
  created: string;
  agent: string;
  preview?: string;
}

const artifacts: Artifact[] = [
  { id: '1', name: 'agent-blueprint.yaml', type: 'agent', size: '4.2 KB', created: '2024-03-15T10:30:00Z', agent: 'Agent Zero', preview: 'name: Research Agent\nrole: research\nframework: langchain' },
  { id: '2', name: 'research-report.md', type: 'document', size: '128 KB', created: '2024-03-15T09:15:00Z', agent: 'Research Agent', preview: '# AI Agents Report\n\n## Executive Summary' },
  { id: '3', name: 'query-analysis.json', type: 'data', size: '2.1 KB', created: '2024-03-14T16:00:00Z', agent: 'Data Agent', preview: '{"queries": ["metrics", "ROI"]}' },
  { id: '4', name: 'generated-image.png', type: 'image', size: '2.4 MB', created: '2024-03-14T14:30:00Z', agent: 'DALL-E Agent' },
  { id: '5', name: 'deployment.sh', type: 'code', size: '1.8 KB', created: '2024-03-14T11:00:00Z', agent: 'DevOps Agent', preview: '#!/bin/bash\ndocker build...' },
  { id: '6', name: 'agent-config.json', type: 'data', size: '856 B', created: '2024-03-13T15:00:00Z', agent: 'Agent Zero', preview: '{"frameworks": ["langchain"]}' },
  { id: '7', name: 'architecture-diagram.png', type: 'image', size: '1.2 MB', created: '2024-03-13T10:00:00Z', agent: 'Writer Agent' },
  { id: '8', name: 'api-spec.yaml', type: 'document', size: '12 KB', created: '2024-03-12T09:00:00Z', agent: 'Code Agent', preview: 'openapi: 3.0.0\npaths: /agents' },
];

const typeIcons: Record<string, string> = {
  document: '📄',
  image: '🖼️',
  code: '💻',
  data: '📊',
  agent: '🤖',
};

const typeColors: Record<string, string> = {
  document: '#58a6ff',
  image: '#f778ba',
  code: '#3fb950',
  data: '#d29922',
  agent: '#8b949e',
};

export default function ArtifactLibraryPage() {
  const [filter, setFilter] = useState<string>('all');
  const [selected, setSelected] = useState<string | null>(null);
  const [view, setView] = useState<'grid' | 'list'>('grid');

  const filtered = filter === 'all' ? artifacts : artifacts.filter(a => a.type === filter);

  return (
    <div style={{ padding: 24, background: '#0a0e14', minHeight: '100vh', color: '#e6edf3', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 4, color: '#f0f6fc' }}>Artifact Library</h1>
          <p style={{ color: '#8b949e', fontSize: 14 }}>Generated files, documents, and outputs</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button onClick={() => setView('grid')} style={{ padding: '8px 12px', background: view === 'grid' ? '#238636' : '#21262d', border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer' }}>▦</button>
          <button onClick={() => setView('list')} style={{ padding: '8px 12px', background: view === 'list' ? '#238636' : '#21262d', border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer' }}>☰</button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 32 }}>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#58a6ff' }}>{artifacts.length}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Total Artifacts</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#3fb950' }}>{artifacts.filter(a => a.type === 'document').length}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Documents</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#d29922' }}>{artifacts.filter(a => a.type === 'data').length}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Data Files</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#f778ba' }}>{(artifacts.reduce((a, a2) => a + parseFloat(a2.size), 0)).toFixed(1)} MB</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Total Size</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        {['all', 'document', 'image', 'code', 'data', 'agent'].map(f => (
          <button key={f} onClick={() => setFilter(f)} style={{ padding: '6px 14px', background: filter === f ? '#238636' : '#21262d', border: '1px solid #30363d', borderRadius: 6, color: '#fff', fontSize: 12, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 6 }}>
            <span>{typeIcons[f]}</span>
            <span style={{ textTransform: 'capitalize' }}>{f}</span>
          </button>
        ))}
      </div>

      <div style={{ display: view === 'grid' ? 'grid' : 'flex', gridTemplateColumns: view === 'grid' ? 'repeat(auto-fill, minmax(260px, 1fr))' : undefined, flexDirection: view === 'list' ? 'column' : undefined, gap: 12 }}>
        {filtered.map(artifact => (
          <div key={artifact.id} onClick={() => setSelected(artifact.id)} style={{ padding: 16, background: selected === artifact.id ? '#1f242c' : '#161b22', borderRadius: 8, border: selected === artifact.id ? '2px solid #238636' : '1px solid #30363d', cursor: 'pointer' }}>
            <div style={{ display: 'flex', gap: 12, marginBottom: 8 }}>
              <span style={{ fontSize: 24 }}>{typeIcons[artifact.type]}</span>
              <div>
                <strong style={{ fontSize: 14, color: '#f0f6fc' }}>{artifact.name}</strong>
                <p style={{ fontSize: 11, color: '#8b949e' }}>{artifact.size} · {new Date(artifact.created).toLocaleDateString()}</p>
              </div>
            </div>
            {view === 'list' && artifact.preview && (
              <pre style={{ fontSize: 11, color: '#8b949e', marginTop: 8, maxHeight: 60, overflow: 'hidden' }}>{artifact.preview}</pre>
            )}
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8, alignItems: 'center' }}>
              <span style={{ fontSize: 11, color: '#8b949e' }}>🤖 {artifact.agent}</span>
              <div style={{ display: 'flex', gap: 4 }}>
                <button style={{ padding: '4px 8px', background: '#21262d', border: 'none', borderRadius: 4, color: '#8b949e', fontSize: 10, cursor: 'pointer' }}>↓</button>
                <button style={{ padding: '4px 8px', background: '#21262d', border: 'none', borderRadius: 4, color: '#8b949e', fontSize: 10, cursor: 'pointer' }}>⋮</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}