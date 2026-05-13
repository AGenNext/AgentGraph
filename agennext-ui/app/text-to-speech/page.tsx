'use client';

import { useState } from 'react';

interface Voice {
  id: string;
  name: string;
  gender: string;
  accent: string;
  preview: string;
}

const voices: Voice[] = [
  { id: '1', name: 'Alloy', gender: 'Neutral', accent: 'American', preview: 'Hello, I am your AI assistant.' },
  { id: '2', name: 'Echo', gender: 'Male', accent: 'American', preview: 'Welcome to the future of AI.' },
  { id: '3', name: 'Fable', gender: 'Male', accent: 'British', preview: 'Good day, how may I assist you?' },
  { id: '4', name: 'Onyx', gender: 'Male', accent: 'American', preview: 'Let me explain the process.' },
  { id: '5', name: 'Nova', gender: 'Female', accent: 'American', preview: 'I would be happy to help you.' },
  { id: '6', name: 'Shimmer', gender: 'Female', accent: 'American', preview: 'Thank you for your patience.' },
  { id: '7', name: 'Adam', gender: 'Male', accent: 'Australian', preview: 'G day! Ready to get started?' },
  { id: '8', name: 'Emily', gender: 'Female', accent: 'Irish', preview: 'Aye, tis a fine day for it.' },
];

export default function TextToSpeechPage() {
  const [text, setText] = useState('Hello! I am your AI voice assistant. Select a voice and enter text to convert to speech.');
  const [selectedVoice, setSelectedVoice] = useState<string>('1');
  const [speed, setSpeed] = useState(1);
  const [playing, setPlaying] = useState(false);
  const [generated, setGenerated] = useState(false);

  const activeVoice = voices.find(v => v.id === selectedVoice) || voices[0];

  const generateSpeech = () => {
    setPlaying(true);
    setGenerated(true);
    setTimeout(() => setPlaying(false), 2000);
  };

  return (
    <div style={{ padding: 24, background: '#0a0e14', minHeight: '100vh', color: '#e6edf3', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 8, color: '#f0f6fc' }}>Text to Speech</h1>
      <p style={{ color: '#8b949e', fontSize: 14, marginBottom: 32 }}>Convert text to natural-sounding speech</p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: 24 }}>
        <div>
          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Input Text</h2>
          <textarea value={text} onChange={e => setText(e.target.value)} style={{ width: '100%', minHeight: 150, padding: 14, background: '#161b22', border: '1px solid #30363d', borderRadius: 8, color: '#e6edf3', fontSize: 14, lineHeight: 1.6, resize: 'vertical' }} />

          <div style={{ marginTop: 16 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
              <span style={{ fontSize: 14 }}>Speed: {speed.toFixed(1)}x</span>
              <input type="range" min="0.5" max="2" step="0.1" value={speed} onChange={e => setSpeed(parseFloat(e.target.value))} style={{ width: 150 }} />
            </div>
          </div>

          <button onClick={generateSpeech} disabled={!text.trim() || playing} style={{ marginTop: 16, padding: '12px 24px', background: !text.trim() || playing ? '#21262d' : 'linear-gradient(135deg, #238636, #2ea043)', border: 'none', borderRadius: 8, color: '#fff', fontSize: 14, fontWeight: 600, cursor: text.trim() && !playing ? 'pointer' : 'default', width: '100%' }}>
            {playing ? '⟳ Generating...' : '▶ Generate Speech'}
          </button>

          {generated && (
            <div style={{ marginTop: 24, padding: 16, background: '#161b22', borderRadius: 8, border: '1px solid #30363d' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                <span style={{ fontSize: 14, fontWeight: 600 }}>Generated Audio</span>
                <div style={{ display: 'flex', gap: 8 }}>
                  <button style={{ padding: '6px 12px', background: '#21262d', border: '1px solid #30363d', borderRadius: 6, color: '#fff', fontSize: 12, cursor: 'pointer' }}>▶ Play</button>
                  <button style={{ padding: '6px 12px', background: '#238636', border: 'none', borderRadius: 6, color: '#fff', fontSize: 12, cursor: 'pointer' }}>↓ Download</button>
                </div>
              </div>
              <div style={{ height: 60, background: '#0d1117', borderRadius: 4, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#8b949e' }}>
                [Audio Waveform Visualization]
              </div>
            </div>
          )}
        </div>

        <div>
          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Voice Selection</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginBottom: 24 }}>
            {voices.map(voice => (
              <div key={voice.id} onClick={() => setSelectedVoice(voice.id)} style={{ 
                padding: 12, background: selectedVoice === voice.id ? '#1f242c' : '#161b22', 
                borderRadius: 8, border: selectedVoice === voice.id ? '2px solid #238636' : '1px solid #30363d', 
                cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center'
              }}>
                <div>
                  <strong style={{ fontSize: 14, color: '#f0f6fc' }}>{voice.name}</strong>
                  <p style={{ fontSize: 11, color: '#8b949e' }}>{voice.gender} · {voice.accent}</p>
                </div>
                {selectedVoice === voice.id && (
                  <button style={{ padding: '4px 8px', background: '#238636', border: 'none', borderRadius: 4, color: '#fff', fontSize: 10, cursor: 'pointer' }}>▶</button>
                )}
              </div>
            ))}
          </div>

          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Preview</h2>
          <div style={{ padding: 16, background: '#161b22', borderRadius: 8, border: '1px solid #30363d' }}>
            <p style={{ fontSize: 13, color: '#8b949e', marginBottom: 12 }}>"{activeVoice.preview}"</p>
            <button style={{ padding: '8px 16px', background: '#21262d', border: '1px solid #30363d', borderRadius: 6, color: '#fff', fontSize: 12, cursor: 'pointer', width: '100%' }}>
              ▶ Preview {activeVoice.name}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}