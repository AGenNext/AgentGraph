'use client';

import { useState } from 'react';

interface Source {
  id: string;
  name: string;
  type: 'pdf' | 'doc' | 'txt' | 'url';
  size: string;
  added: string;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
}

const sources: Source[] = [
  { id: 's1', name: 'Q4 Research Report.pdf', type: 'pdf', size: '2.4 MB', added: '2 days ago' },
  { id: 's2', name: 'Product Specs.docx', type: 'doc', size: '890 KB', added: '5 days ago' },
  { id: 's3', name: 'Meeting Notes.txt', type: 'txt', size: '45 KB', added: '1 week ago' },
];

const messages: Message[] = [
  { role: 'assistant', content: 'I\'ve analyzed your sources. What would you like to know?' },
];

export default function NotebookPage() {
  const [srcs] = useState<Source[]>(sources);
  const [msgs, setMsgs] = useState<Message[]>(messages);
  const [input, setInput] = useState('');

  const send = () => {
    if (!input.trim()) return;
    setMsgs([...msgs, { role: 'user', content: input }, { role: 'assistant', content: 'Based on your sources, I found relevant information about that topic. Here\'s the key insight:\n\n' + input }]);
    setInput('');
  };

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA' }}>
      {/* Sources Panel */}
      <div style={{ width: 280, background: '#1A1A2E', color: '#fff', padding: 16, display: 'flex', flexDirection: 'column' }}>
        <div style={{ fontWeight: 600, fontSize: 14, marginBottom: 16, padding: '8px 12px', background: 'rgba(255,255,255,0.1)', borderRadius: 8 }}>
          📚 Sources
        </div>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8, flex: 1 }}>
          {srcs.map(s => (
            <div key={s.id} style={{ padding: 12, background: 'rgba(255,255,255,0.05)', borderRadius: 8, cursor: 'pointer' }}>
              <div style={{ fontSize: 13, fontWeight: 500, marginBottom: 4 }}>{s.name}</div>
              <div style={{ fontSize: 11, color: '#A0A0B8' }}>{s.size}</div>
            </div>
          ))}
        </div>

        <button style={{ background: '#667EEA', color: '#fff', border: 'none', padding: 12, borderRadius: 8, fontSize: 13, cursor: 'pointer', marginTop: 12 }}>
          + Add Source
        </button>
      </div>

      {/* Chat Panel */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <div style={{ padding: '16px 24px', background: '#fff', borderBottom: '1px solid #E5E5E5', display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{ width: 36, height: 36, borderRadius: 8, background: 'linear-gradient(135deg, #667EEA, #764BA2)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: 18 }}>N</div>
          <div>
            <div style={{ fontWeight: 600, fontSize: 14 }}>Notebook</div>
            <div style={{ fontSize: 11, color: '#6B7280' }}>3 sources loaded</div>
          </div>
        </div>

        {/* Messages */}
        <div style={{ flex: 1, overflow: 'auto', padding: 24 }}>
          {msgs.map((msg, i) => (
            <div key={i} style={{ display: 'flex', gap: 12, marginBottom: 20 }}>
              <div style={{ width: 32, height: 32, borderRadius: 8, background: msg.role === 'assistant' ? '#667EEA' : '#E5E5E5', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 14 }}>
                {msg.role === 'assistant' ? 'AI' : 'You'}
              </div>
              <div style={{ flex: 1, background: msg.role === 'assistant' ? '#F8F9FA' : '#fff', padding: 16, borderRadius: 12, border: '1px solid #E5E5E5', fontSize: 14, lineHeight: 1.6 }}>
                {msg.content}
                {msg.sources && msg.sources.length > 0 && (
                  <div style={{ marginTop: 12, paddingTop: 12, borderTop: '1px solid #E5E5E5' }}>
                    <div style={{ fontSize: 11, color: '#6B7280', marginBottom: 8 }}>Sources:</div>
                    {msg.sources.map((s, j) => (
                      <div key={j} style={{ fontSize: 12, color: '#0F62FE', marginBottom: 4 }}>📄 {s}</div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Input */}
        <div style={{ padding: 16, background: '#fff', borderTop: '1px solid #E5E5E5' }}>
          <div style={{ display: 'flex', gap: 12, background: '#F8F9FA', borderRadius: 12, padding: 8, border: '1px solid #E5E5E5' }}>
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && send()}
              placeholder="Ask about your sources..."
              style={{ flex: 1, background: 'transparent', border: 'none', outline: 'none', fontSize: 14, padding: '4px 8px' }}
            />
            <button 
              onClick={send}
              style={{ background: '#667EEA', color: '#fff', border: 'none', padding: '8px 16px', borderRadius: 8, fontSize: 13, cursor: 'pointer' }}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}