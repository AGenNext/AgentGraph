'use client';

import { useState } from 'react';

interface Video {
  id: string;
  prompt: string;
  model: string;
  duration: string;
  status: 'ready' | 'generating' | 'failed';
  durationSec?: number;
  created: string;
  agent: string;
}

const videos: Video[] = [
  { id: 'v1', prompt: 'A futuristic city street at night with neon lights', model: 'Sora', duration: '10s', status: 'ready', durationSec: 10, created: '2 hours ago', agent: 'Research Agent' },
  { id: 'v2', prompt: 'Robot walking through office hallway', model: 'Kling 1.5', duration: '5s', status: 'ready', durationSec: 5, created: '3 hours ago', agent: 'Writer Agent' },
  { id: 'v3', prompt: 'Ocean waves crashing on beach at sunset', model: 'Runway Gen-3', duration: '10s', status: 'generating', created: '1 min ago', agent: 'Analyzer' },
  { id: 'v4', prompt: 'Abstract flowing colors', model: 'Sora', duration: '5s', status: 'failed', created: 'Yesterday', agent: 'Triage Agent' },
];

export default function VideoPage() {
  const [vids] = useState<Video[]>(videos);
  const [prompt, setPrompt] = useState('');
  const [selectedModel, setSelectedModel] = useState('Sora');

  const models = [
    { id: 'sora', name: 'Sora', provider: 'OpenAI', maxDuration: '20s' },
    { id: 'runway', name: 'Runway Gen-3', provider: 'Runway', maxDuration: '10s' },
    { id: 'kling', name: 'Kling 1.5', provider: 'Kuaishou', maxDuration: '10s' },
    { id: 'pika', name: 'Pika 1.0', provider: 'Pika', maxDuration: '5s' },
  ];

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 24 }}>Video Generation</h1>

      {/* Generate */}
      <div style={{ background: '#fff', borderRadius: 12, padding: 24, marginBottom: 24, border: '1px solid #E5E5E5' }}>
        <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 16 }}>Generate New Video</h2>
        
        <textarea
          placeholder="Describe the video you want to generate..."
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
            {models.map(m => <option key={m.id} value={m.id}>{m.name} ({m.provider})</option>)}
          </select>
          
          <select style={{ padding: '10px 14px', borderRadius: 6, border: '1px solid #E5E5E5', background: '#fff' }}>
            <option>5 seconds</option>
            <option>10 seconds</option>
            <option>15 seconds</option>
            <option>20 seconds</option>
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
            Generate Video
          </button>
        </div>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{vids.length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Total Videos</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{vids.filter(v => v.status === 'ready').length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Generated</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#0F62FE' }}>{vids.filter(v => v.status === 'generating').length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Processing</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#DA1E28' }}>{vids.filter(v => v.status === 'failed').length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Failed</div>
        </div>
      </div>

      {/* Gallery */}
      <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', padding: 20 }}>
        <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>Recent Videos</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
          {vids.map(vid => (
            <div key={vid.id} style={{ position: 'relative' }}>
              <div style={{ 
                aspectRatio: '16/9', 
                background: '#1A1A2E', 
                borderRadius: 8, 
                overflow: 'hidden',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                position: 'relative'
              }}>
                {vid.status === 'generating' ? (
                  <div style={{ textAlign: 'center', color: '#fff' }}>
                    <div style={{ fontSize: 24, animation: 'spin 1s linear infinite' }}>🎬</div>
                    <div style={{ fontSize: 11 }}>Generating...</div>
                  </div>
                ) : vid.status === 'failed' ? (
                  <div style={{ textAlign: 'center', color: '#DA1E28' }}>
                    <div style={{ fontSize: 24 }}>⚠️</div>
                    <div style={{ fontSize: 10 }}>Failed</div>
                  </div>
                ) : (
                  <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: 32 }}>
                    ▶️
                  </div>
                )}
                {vid.status === 'ready' && (
                  <div style={{ position: 'absolute', bottom: 8, right: 8, background: 'rgba(0,0,0,0.7)', color: '#fff', padding: '2px 6px', borderRadius: 4, fontSize: 10 }}>
                    {vid.durationSec}s
                  </div>
                )}
              </div>
              <div style={{ marginTop: 8, fontSize: 11, color: '#6B7280', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {vid.prompt.substring(0, 30)}...
              </div>
              <div style={{ fontSize: 10, color: '#9CA3AF' }}>
                {vid.model} • {vid.agent} • {vid.created}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}