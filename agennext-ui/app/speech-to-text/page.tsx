'use client';

import { useState } from 'react';

interface Transcription {
  id: string;
  file: string;
  duration: string;
  timestamp: string;
  text: string;
  language: string;
  status: 'completed' | 'processing';
}

const transcriptions: Transcription[] = [
  { id: '1', file: 'meeting-recording-2024-03-15.mp3', duration: '45:30', timestamp: '2024-03-15T14:00:00Z', text: 'So lets circle back on the deployment timeline. I think we need to prioritize the agent orchestration layer first...', language: 'English', status: 'completed' },
  { id: '2', file: 'customer-call-2024-03-14.mp3', duration: '12:45', timestamp: '2024-03-14T10:30:00Z', text: 'Thank you for calling. I would like to inquire about the enterprise pricing for your AI agent platform...', language: 'English', status: 'completed' },
  { id: '3', file: 'team-standup-2024-03-13.mp3', duration: '15:00', timestamp: '2024-03-13T09:00:00Z', text: 'Good morning everyone. Lets start with round-robin updates. Sarah, what is your status on the integration...', language: 'English', status: 'completed' },
  { id: '4', file: 'interview-2024-03-12.mp3', duration: '32:15', timestamp: '2024-03-12T15:00:00Z', text: 'Can you tell me about a challenging problem you solved with multi-agent systems? Well, I worked on...', language: 'English', status: 'completed' },
];

export default function SpeechToTextPage() {
  const [recordings, setRecordings] = useState<Transcription[]>(transcriptions);
  const [recording, setRecording] = useState(false);
  const [selected, setSelected] = useState<string | null>(null);

  const startRecording = () => {
    setRecording(true);
    setTimeout(() => setRecording(false), 3000);
  };

  const formatDuration = (dur: string) => {
    const [min, sec] = dur.split(':');
    return `${parseInt(min)}m ${parseInt(sec)}s`;
  };

  const activeTranscription = recordings.find(t => t.id === selected) || transcriptions[0];

  return (
    <div style={{ padding: 24, background: '#0a0e14', minHeight: '100vh', color: '#e6edf3', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 8, color: '#f0f6fc' }}>Speech to Text</h1>
      <p style={{ color: '#8b949e', fontSize: 14, marginBottom: 32 }}>Transcribe audio recordings to text</p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 32 }}>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#58a6ff' }}>{transcriptions.length}</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Transcriptions</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#3fb950' }}>{transcriptions.reduce((a, t) => a + parseInt(t.duration.split(':')[0]), 0)}m</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Total Audio</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#d29922' }}>99.2%</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Accuracy</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 400px', gap: 24 }}>
        <div>
          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Recordings</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginBottom: 24 }}>
            {transcriptions.map(t => (
              <div key={t.id} onClick={() => setSelected(t.id)} style={{ padding: 12, background: selected === t.id ? '#1f242c' : '#161b22', borderRadius: 8, border: selected === t.id ? '2px solid #238636' : '1px solid #30363d', cursor: 'pointer' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <strong style={{ fontSize: 14, color: '#f0f6fc' }}>{t.file}</strong>
                    <p style={{ fontSize: 11, color: '#8b949e' }}>{formatDuration(t.duration)} · {new Date(t.timestamp).toLocaleDateString()}</p>
                  </div>
                  <span style={{ padding: '4px 8px', borderRadius: 4, fontSize: 10, background: t.status === 'completed' ? '#23863622' : '#d2992222', color: t.status === 'completed' ? '#3fb950' : '#d29922' }}>{t.status}</span>
                </div>
              </div>
            ))}
          </div>

          <div onClick={startRecording} style={{ padding: 24, background: '#161b22', borderRadius: 12, border: '2px dashed #30363d', textAlign: 'center', cursor: 'pointer' }}>
            <span style={{ fontSize: 32, display: 'block', marginBottom: 8 }}>{recording ? '🔴' : '🎤'}</span>
            <span style={{ color: '#8b949e' }}>
              {recording ? 'Recording...' : 'Click to Record'}
            </span>
          </div>
        </div>

        <div>
          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Transcription</h2>
          <div style={{ padding: 16, background: '#161b22', borderRadius: 8, border: '1px solid #30363d', minHeight: 300 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
              <span style={{ fontSize: 12, color: '#8b949e' }}>{activeTranscription.language}</span>
              <div style={{ display: 'flex', gap: 8 }}>
                <button style={{ padding: '4px 8px', background: '#21262d', border: 'none', borderRadius: 4, color: '#8b949e', fontSize: 10, cursor: 'pointer' }}>📋</button>
                <button style={{ padding: '4px 8px', background: '#238636', border: 'none', borderRadius: 4, color: '#fff', fontSize: 10, cursor: 'pointer' }}>↓</button>
              </div>
            </div>
            <p style={{ fontSize: 14, lineHeight: 1.7, color: '#e6edf3' }}>"{activeTranscription.text}"</p>
          </div>

          <div style={{ marginTop: 16, padding: 12, background: '#161b22', borderRadius: 8, border: '1px solid #30363d' }}>
            <h3 style={{ fontSize: 13, fontWeight: 600, marginBottom: 8 }}>Speaker Diarization</h3>
            <div style={{ display: 'flex', gap: 16 }}>
              <span style={{ fontSize: 12 }}><span style={{ color: '#58a6ff' }}>●</span> Speaker 1 (70%)</span>
              <span style={{ fontSize: 12 }}><span style={{ color: '#f778ba' }}>●</span> Speaker 2 (30%)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}