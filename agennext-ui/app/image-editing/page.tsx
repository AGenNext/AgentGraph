'use client';

import { useState } from 'react';

interface EditTool {
  id: string;
  name: string;
  icon: string;
  description: string;
}

const editTools: EditTool[] = [
  { id: 'inpaint', name: 'Inpainting', icon: '🖌️', description: 'Remove or replace objects' },
  { id: 'outpaint', name: 'Outpainting', icon: '🖼️', description: 'Extend image boundaries' },
  { id: 'upscale', name: 'Upscale', icon: '⬆️', description: 'Increase resolution 4x' },
  { id: 'remove-bg', name: 'Remove BG', icon: '✂️', description: 'Remove background' },
  { id: 'colorize', name: 'Colorize', icon: '🎨', description: 'Add color to B&W images' },
  { id: 'enhance', name: 'Enhance', icon: '✨', description: 'Improve quality & details' },
  { id: 'style', name: 'Style Transfer', icon: '🎭', description: 'Apply artistic styles' },
  { id: 'variations', name: 'Variations', icon: '📐', description: 'Generate variations' },
];

const promptPresets = [
  'Remove the person on the left',
  'Change background to beach sunset',
  'Add mountains in background',
  'Make it look like a painting',
  'Increase brightness and contrast',
  'Remove watermark',
];

export default function ImageEditingPage() {
  const [selectedTool, setSelectedTool] = useState<string>('inpaint');
  const [prompt, setPrompt] = useState('');
  const [processing, setProcessing] = useState(false);

  const activeTool = editTools.find(t => t.id === selectedTool) || editTools[0];

  const applyEdit = () => {
    setProcessing(true);
    setTimeout(() => setProcessing(false), 2500);
  };

  return (
    <div style={{ padding: 24, background: '#0a0e14', minHeight: '100vh', color: '#e6edf3', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 8, color: '#f0f6fc' }}>Image Editing</h1>
      <p style={{ color: '#8b949e', fontSize: 14, marginBottom: 32 }}>AI-powered image manipulation</p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: 24 }}>
        <div>
          <div style={{ background: '#161b22', borderRadius: 12, border: '1px solid #30363d', padding: 24, marginBottom: 24, minHeight: 400, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <div style={{ textAlign: 'center', color: '#8b949e' }}>
              {processing ? (
                <>
                  <div style={{ fontSize: 32, marginBottom: 16, animation: 'spin 1s linear infinite' }}>⚙️</div>
                  <p>Processing image...</p>
                </>
              ) : (
                <>
                  <div style={{ fontSize: 48, marginBottom: 16 }}>🖼️</div>
                  <p>Drop image here or click to upload</p>
                  <p style={{ fontSize: 12, marginTop: 8 }}>Supports PNG, JPG, WebP up to 10MB</p>
                </>
              )}
            </div>
          </div>

          <div style={{ display: 'flex', gap: 12 }}>
            <button style={{ flex: 1, padding: 12, background: '#21262d', border: '1px solid #30363d', borderRadius: 8, color: '#fff', fontSize: 13, cursor: 'pointer' }}>← Previous</button>
            <button style={{ flex: 1, padding: 12, background: '#21262d', border: '1px solid #30363d', borderRadius: 8, color: '#fff', fontSize: 13, cursor: 'pointer' }}>Next →</button>
          </div>
        </div>

        <div>
          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Editing Tools</h2>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginBottom: 24 }}>
            {editTools.map(tool => (
              <div key={tool.id} onClick={() => setSelectedTool(tool.id)} style={{ 
                padding: 12, background: selectedTool === tool.id ? '#1f242c' : '#161b22', 
                borderRadius: 8, border: selectedTool === tool.id ? '2px solid #238636' : '1px solid #30363d', 
                cursor: 'pointer', textAlign: 'center'
              }}>
                <div style={{ fontSize: 20, marginBottom: 4 }}>{tool.icon}</div>
                <div style={{ fontSize: 12, color: '#f0f6fc' }}>{tool.name}</div>
              </div>
            ))}
          </div>

          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Edit Prompt</h2>
          <textarea value={prompt} onChange={e => setPrompt(e.target.value)} placeholder={`Describe what you want to ${activeTool.name.toLowerCase()}...`} style={{ width: '100%', minHeight: 80, padding: 12, background: '#161b22', border: '1px solid #30363d', borderRadius: 8, color: '#e6edf3', fontSize: 13, resize: 'vertical', marginBottom: 12 }} />

          <div style={{ marginBottom: 16 }}>
            <p style={{ fontSize: 12, color: '#8b949e', marginBottom: 8 }}>Quick prompts:</p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
              {promptPresets.map(p => (
                <button key={p} onClick={() => setPrompt(p)} style={{ padding: '4px 10px', background: '#21262d', border: '1px solid #30363d', borderRadius: 4, color: '#8b949e', fontSize: 11, cursor: 'pointer' }}>
                  {p}
                </button>
              ))}
            </div>
          </div>

          <button onClick={applyEdit} disabled={!prompt.trim() || processing} style={{ width: '100%', padding: 12, background: !prompt.trim() || processing ? '#21262d' : 'linear-gradient(135deg, #238636, #2ea043)', border: 'none', borderRadius: 8, color: '#fff', fontSize: 14, fontWeight: 600, cursor: prompt.trim() && !processing ? 'pointer' : 'default' }}>
            {processing ? '⟳ Processing...' : `Apply ${activeTool.name}`}
          </button>
        </div>
      </div>

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}