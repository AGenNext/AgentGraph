'use client';

import { useState } from 'react';

interface Tool {
  id: string;
  name: string;
  description: string;
  framework: string;
  input: 'text' | 'image' | 'audio' | 'video' | 'file' | 'multimodal';
  output: 'text' | 'image' | 'audio' | 'video' | 'json' | 'multimodal';
  icon: string;
}

const tools: Tool[] = [
  { id: '1', name: 'Web Search', description: 'Search the web for information', framework: 'LangChain', input: 'text', output: 'text', icon: '🔍' },
  { id: '2', name: 'Image Generation', description: 'Generate images from text prompts', framework: 'DALL-E', input: 'text', output: 'image', icon: '🎨' },
  { id: '3', name: 'Speech to Text', description: 'Convert audio to text', framework: 'Whisper', input: 'audio', output: 'text', icon: '🎤' },
  { id: '4', name: 'Text to Speech', description: 'Convert text to audio', framework: 'TTS', input: 'text', output: 'audio', icon: '🔊' },
  { id: '5', name: 'Code Executor', description: 'Run code in sandbox', framework: 'e2b', input: 'text', output: 'json', icon: '💻' },
  { id: '6', name: 'Image Analyzer', description: 'Analyze images with vision', framework: 'GPT-4V', input: 'image', output: 'text', icon: '🖼️' },
  { id: '7', name: 'Video Analyzer', description: 'Analyze video content', framework: 'VertexAI', input: 'video', output: 'text', icon: '📹' },
  { id: '8', name: 'Document OCR', description: 'Extract text from documents', framework: 'AWS Textract', input: 'file', output: 'json', icon: '📄' },
  { id: '9', name: 'Multimodal Agent', description: 'Process text, images, and audio', framework: 'GPT-4V', input: 'multimodal', output: 'multimodal', icon: '🧠' },
  { id: '10', name: 'Knowledge Graph', description: 'Query knowledge bases', framework: ' Neo4j', input: 'text', output: 'json', icon: '🕸️' },
  // Browser & Computer Tools
  { id: '11', name: 'Browser Automation', description: 'Navigate, click, type in browser', framework: 'Playwright', input: 'text', output: 'text', icon: '🌐' },
  { id: '12', name: 'Computer Control', description: 'Mouse, keyboard control', framework: 'pyautogui', input: 'text', output: 'json', icon: '🖱️' },
  { id: '13', name: 'File I/O', description: 'Read/write files', framework: 'fs', input: 'file', output: 'text', icon: '📁' },
];

export default function ToolsPage() {
  const [filter, setFilter] = useState<string>('all');
  const [ioFilter, setIoFilter] = useState<string>('all');

  const filtered = tools.filter(t => 
    (filter === 'all' || t.framework.toLowerCase().includes(filter.toLowerCase())) &&
    (ioFilter === 'all' || t.input === ioFilter || t.output === ioFilter)
  );

  const ioTypes = ['text', 'image', 'audio', 'video', 'file', 'multimodal', 'json'];

  return (
    <div style={{ padding: 24, background: '#0a0e14', minHeight: '100vh', color: '#e6edf3', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 8, color: '#f0f6fc' }}>Agent Tools</h1>
      <p style={{ color: '#8b949e', fontSize: 14, marginBottom: 32 }}>Multimodal tools for agent capabilities</p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 32 }}>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#58a6ff' }}>{tools.length}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Total Tools</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#f778ba' }}>{tools.filter(t => t.input === 'multimodal' || t.output === 'multimodal').length}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Multimodal</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#3fb950' }}>{tools.filter(t => t.input === 'image' || t.output === 'image').length}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Vision</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#d29922' }}>{tools.filter(t => t.input === 'audio' || t.output === 'audio').length}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Audio</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        <input placeholder="Search tools..." style={{ flex: 1, padding: 10, background: '#161b22', border: '1px solid #30363d', borderRadius: 8, color: '#e6edf3', fontSize: 14 }} />
        <div style={{ display: 'flex', gap: 4, background: '#161b22', padding: 4, borderRadius: 8 }}>
          {['all', 'LangChain', 'GPT-4V', 'DALL-E'].map(f => (
            <button key={f} onClick={() => setFilter(f)} style={{ padding: '6px 12px', background: filter === f ? '#238636' : 'transparent', border: 'none', borderRadius: 6, color: '#fff', fontSize: 12, cursor: 'pointer', textTransform: 'capitalize' }}>
              {f}
            </button>
          ))}
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 24, flexWrap: 'wrap' }}>
        <span style={{ fontSize: 12, color: '#8b949e', marginRight: 8, alignSelf: 'center' }}>I/O:</span>
        {['all', 'text', 'image', 'audio', 'video', 'multimodal'].map(io => (
          <button key={io} onClick={() => setIoFilter(io)} style={{ padding: '4px 10px', background: ioFilter === io ? '#238636' : '#21262d', border: '1px solid #30363d', borderRadius: 6, color: '#fff', fontSize: 11, cursor: 'pointer', textTransform: 'uppercase' }}>
            {io}
          </button>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 12 }}>
        {filtered.map(tool => (
          <div key={tool.id} style={{ padding: 16, background: '#161b22', borderRadius: 8, border: '1px solid #30363d' }}>
            <div style={{ display: 'flex', gap: 12, marginBottom: 12 }}>
              <span style={{ fontSize: 24 }}>{tool.icon}</span>
              <div>
                <strong style={{ fontSize: 15, color: '#f0f6fc' }}>{tool.name}</strong>
                <p style={{ fontSize: 12, color: '#8b949e' }}>{tool.framework}</p>
              </div>
            </div>
            <p style={{ fontSize: 13, color: '#8b949e', marginBottom: 12 }}>{tool.description}</p>
            <div style={{ display: 'flex', gap: 8 }}>
              <span style={{ padding: '4px 8px', borderRadius: 4, fontSize: 10, background: 'rgba(88, 166, 255, 0.15)', color: '#58a6ff', textTransform: 'uppercase' }}>
                {tool.input} → {tool.output}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}