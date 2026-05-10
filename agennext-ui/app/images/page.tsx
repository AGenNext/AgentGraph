'use client';

import { useState } from 'react';

interface GeneratedImage {
  id: string;
  prompt: string;
  model: string;
  size: string;
  status: 'ready' | 'generating' | 'failed';
  url?: string;
  created: string;
  agent: string;
}

const images: GeneratedImage[] = [
  { id: 'img1', prompt: 'A futuristic city with flying cars', model: 'DALL-E 3', size: '1024x1024', status: 'ready', url: 'https://placeholder.com/300', created: '2 hours ago', agent: 'Research Agent' },
  { id: 'img2', prompt: 'Abstract data visualization', model: 'Stable Diffusion XL', size: '1024x1024', status: 'ready', url: 'https://placeholder.com/300', created: '3 hours ago', agent: 'Writer Agent' },
  { id: 'img3', prompt: 'Robot assistant in office', model: 'DALL-E 3', size: '1792x1024', status: 'generating', created: '5 min ago', agent: 'Analyzer' },
  { id: 'img4', prompt: 'Neural network diagram', model: 'Midjourney v6', size: '1024x1024', status: 'ready', url: 'https://placeholder.com/300', created: 'Yesterday', agent: 'Research Agent' },
  { id: 'img5', prompt: 'Cyberpunk street scene', model: 'Stable Diffusion XL', size: '512x512', status: 'failed', created: 'Yesterday', agent: 'Triage Agent' },
];

export default function ImagesPage() {
  const [imgs] = useState<GeneratedImage[]>(images);
  const [prompt, setPrompt] = useState('');
  const [selectedModel, setSelectedModel] = useState('DALL-E 3');

  const models = [
    { id: 'dalle3', name: 'DALL-E 3', provider: 'OpenAI' },
    { id: 'sdxl', name: 'Stable Diffusion XL', provider: 'Stability AI' },
    { id: 'midjourney', name: 'Midjourney v6', provider: 'Midjourney' },
    { id: 'imagen', name: 'Imagen 3', provider: 'Google' },
  ];

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 24 }}>Image Generation</h1>

      {/* Generate */}
      <div style={{ background: '#fff', borderRadius: 12, padding: 24, marginBottom: 24, border: '1px solid #E5E5E5' }}>
        <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 16 }}>Generate New Image</h2>
        
        <textarea
          placeholder="Describe the image you want to generate..."
          value={prompt}
          onChange={e => setPrompt(e.target.value)}
          style={{ width: '100%', minHeight: 100, padding: 12, borderRadius: 8, border: '1px solid #E5E5E5', marginBottom: 16, fontSize: 14, resize: 'vertical' }}
        />
        
        <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          <select 
            value={selectedModel} 
            onChange={e => setSelectedModel(e.target.value)}
            style={{ padding: '10px 14px', borderRadius: 6, border: '1px solid #E5E5E5', background: '#fff' }}
          >
            {models.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
          </select>
          
          <select style={{ padding: '10px 14px', borderRadius: 6, border: '1px solid #E5E5E5', background: '#fff' }}>
            <option>1024x1024</option>
            <option>1024x1792</option>
            <option>1792x1024</option>
            <option>512x512</option>
          </select>
          
          <button 
            disabled={!prompt}
            style={{ 
              background: prompt ? '#0F62FE' : '#E5E5E5', 
              color: prompt ? '#fff' : '#8C8C8C', 
              border: 'none', 
              padding: '10px 20px', 
              borderRadius: 6, 
              fontSize: 13, 
              cursor: prompt ? 'pointer' : 'not-allowed',
              marginLeft: 'auto'
            }}
          >
            Generate
          </button>
        </div>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{imgs.length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Total Images</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{imgs.filter(i => i.status === 'ready').length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Generated</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#0F62FE' }}>{imgs.filter(i => i.status === 'generating').length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Processing</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#DA1E28' }}>{imgs.filter(i => i.status === 'failed').length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Failed</div>
        </div>
      </div>

      {/* Gallery */}
      <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', padding: 20 }}>
        <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>Recent Images</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 16 }}>
          {imgs.map(img => (
            <div key={img.id} style={{ position: 'relative' }}>
              <div style={{ 
                aspectRatio: '1', 
                background: '#F4F4F4', 
                borderRadius: 8, 
                overflow: 'hidden',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                border: img.status === 'failed' ? '2px solid #DA1E28' : 'none'
              }}>
                {img.status === 'generating' ? (
                  <div style={{ textAlign: 'center', color: '#6B7280' }}>
                    <div style={{ fontSize: 24, animation: 'spin 1s linear infinite' }}>⏳</div>
                    <div style={{ fontSize: 11 }}>Generating...</div>
                  </div>
                ) : img.status === 'failed' ? (
                  <div style={{ textAlign: 'center', color: '#DA1E28' }}>
                    <div style={{ fontSize: 24 }}>⚠️</div>
                    <div style={{ fontSize: 10 }}>Failed</div>
                  </div>
                ) : (
                  <div style={{ width: '100%', height: '100%', background: `linear-gradient(135deg, #667EEA 0%, #764BA2 100%)`, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: 32 }}>
                    🖼️
                  </div>
                )}
              </div>
              <div style={{ marginTop: 8, fontSize: 11, color: '#6B7280', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {img.prompt.substring(0, 30)}...
              </div>
              <div style={{ fontSize: 10, color: '#9CA3AF' }}>
                {img.model} • {img.agent}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}