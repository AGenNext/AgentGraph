'use client';

import { useState, useRef, useEffect } from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

const initialMessages: Message[] = [
  { id: '1', role: 'assistant', content: 'Hello! I\'m Agent Zero, your enterprise AI orchestrator. How can I help you today?', timestamp: '10:30:00' },
];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEnd = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEnd.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = () => {
    if (!input.trim()) return;
    
    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
    };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    setTimeout(() => {
      const aiMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `I understand you want to: "${input}". I'm processing this request using my orchestration capabilities across ${childAgents.length} child agents. What specific action would you like me to take?`,
        timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages(prev => [...prev, aiMsg]);
      setIsTyping(false);
    }, 1500);
  };

  const childAgents = [
    { name: 'Research Agent', icon: '🔍' },
    { name: 'Writer Agent', icon: '✍️' },
    { name: 'Code Agent', icon: '💻' },
    { name: 'Security Agent', icon: '🛡️' },
  ];

  return (
    <div style={{ display: 'flex', height: '100vh', background: '#0a0e14' }}>
      <div style={{ width: 240, background: '#161b22', borderRight: '1px solid #30363d', padding: 16 }}>
        <h2 style={{ fontSize: 16, fontWeight: 600, color: '#f0f6fc', marginBottom: 16 }}>Agents</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {childAgents.map(agent => (
            <div key={agent.name} style={{ padding: '10px 12px', background: '#21262d', borderRadius: 6, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 8 }}>
              <span>{agent.icon}</span>
              <span style={{ fontSize: 13, color: '#e6edf3' }}>{agent.name}</span>
            </div>
          ))}
        </div>
      </div>

      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '16px 20px', borderBottom: '1px solid #30363d', display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{ width: 32, height: 32, borderRadius: '50%', background: 'linear-gradient(135deg, #238636, #2ea043)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <span style={{ fontSize: 16 }}>🤖</span>
          </div>
          <div>
            <h1 style={{ fontSize: 16, fontWeight: 600, color: '#f0f6fc' }}>Agent Zero</h1>
            <p style={{ fontSize: 12, color: '#3fb950' }}>● Online</p>
          </div>
        </div>

        <div style={{ flex: 1, overflow: 'auto', padding: 20 }}>
          {messages.map(msg => (
            <div key={msg.id} style={{ display: 'flex', gap: 12, marginBottom: 16, flexDirection: msg.role === 'user' ? 'row-reverse' : 'row' }}>
              <div style={{ width: 32, height: 32, borderRadius: '50%', background: msg.role === 'user' ? '#58a6ff' : 'linear-gradient(135deg, #238636, #2ea043)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                <span style={{ fontSize: 14 }}>{msg.role === 'user' ? '👤' : '🤖'}</span>
              </div>
              <div style={{ maxWidth: '70%', padding: '12px 16px', background: msg.role === 'user' ? '#21262d' : '#161b22', borderRadius: 12, border: '1px solid #30363d' }}>
                <p style={{ fontSize: 14, color: '#e6edf3', lineHeight: 1.5 }}>{msg.content}</p>
                <p style={{ fontSize: 11, color: '#8b949e', marginTop: 4 }}>{msg.timestamp}</p>
              </div>
            </div>
          ))}
          {isTyping && (
            <div style={{ display: 'flex', gap: 12 }}>
              <div style={{ width: 32, height: 32, borderRadius: '50%', background: 'linear-gradient(135deg, #238636, #2ea043)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <span style={{ fontSize: 14 }}>🤖</span>
              </div>
              <div style={{ padding: '12px 16px', background: '#161b22', borderRadius: 12, border: '1px solid #30363d' }}>
                <div style={{ display: 'flex', gap: 4 }}>
                  <div style={{ width: 8, height: 8, borderRadius: '50%', background: '#58a6ff', animation: 'pulse 1s infinite' }} />
                  <div style={{ width: 8, height: 8, borderRadius: '50%', background: '#58a6ff', animation: 'pulse 1s infinite 0.2s' }} />
                  <div style={{ width: 8, height: 8, borderRadius: '50%', background: '#58a6ff', animation: 'pulse 1s infinite 0.4s' }} />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEnd} />
        </div>

        <div style={{ padding: 16, borderTop: '1px solid #30363d' }}>
          <div style={{ display: 'flex', gap: 8, background: '#161b22', borderRadius: 12, padding: 8, border: '1px solid #30363d' }}>
            <input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && sendMessage()} placeholder="Type your message..." style={{ flex: 1, background: 'transparent', border: 'none', outline: 'none', color: '#e6edf3', fontSize: 14, padding: '4px 8px' }} />
            <button onClick={sendMessage} disabled={!input.trim()} style={{ padding: '8px 16px', background: input.trim() ? 'linear-gradient(135deg, #238636, #2ea043)' : '#21262d', border: 'none', borderRadius: 8, color: '#fff', fontSize: 13, fontWeight: 500, cursor: input.trim() ? 'pointer' : 'default' }}>
              Send
            </button>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 0.3; }
          50% { opacity: 1; }
        }
      `}</style>
    </div>
  );
}