'use client';

import { useState, useEffect, use } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

interface AgentFormData {
  name: string;
  description: string;
  provider: string;
  model: string;
  temperature: number;
  maxTokens: number;
  systemPrompt: string;
  authMethod: string;
  apiKey: string;
  enableChat: boolean;
  enableRAG: boolean;
  tools: string[];
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
const tokens = {
  colors: { primary: '#6366f1', secondary: '#64748b', success: '#22c55e', background: '#f8fafc', card: '#ffffff', text: '#1e293b', textMuted: '#64748b', border: '#e2e8f0' },
  spacing: { xs: '4px', sm: '8px', md: '16px', lg: '24px', xl: '32px' },
  font: { family: 'Inter, system-ui, sans-serif', size: { small: '14px', body: '16px', h3: '20px', h2: '24px' } },
};

const providerModels: Record<string, string[]> = { openai: ['gpt-4o', 'gpt-4o-mini'], google: ['gemini-2.0-flash', 'gemini-1.5-pro'], microsoft: ['gpt-4o', 'gpt-35-turbo'], langchain: ['gpt-4o', 'claude-3-opus'] };

export default function EditAgentPage({ params }: { params: { id: string } }) {
  const id = params.id;
  const router = useRouter();
  const [formData, setFormData] = useState<AgentFormData>({ name: '', description: '', provider: 'openai', model: 'gpt-4o', temperature: 0.7, maxTokens: 2000, systemPrompt: '', authMethod: 'api_key', apiKey: '', enableChat: true, enableRAG: false, tools: ['calculator', 'search'] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/agents/${id}`).then(res => res.json()).then(data => {
      const agent = data.agent;
      if (agent) {
        setFormData({
          name: agent.name || '',
          description: agent.description || '',
          provider: agent.provider || 'openai',
          model: agent.model || 'gpt-4o',
          temperature: agent.temperature || 0.7,
          maxTokens: agent.max_tokens || 2000,
          systemPrompt: agent.system_prompt || '',
          authMethod: agent.auth_method || 'api_key',
          apiKey: '',
          enableChat: agent.enable_chat ?? true,
          enableRAG: agent.enable_rag ?? false,
          tools: agent.tools || ['calculator', 'search']
        });
      }
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [id]);

  const handleChange = (field: keyof AgentFormData, value: string | number | boolean) => setFormData(prev => ({ ...prev, [field]: value }));
  const handleProviderChange = (provider: string) => setFormData(prev => ({ ...prev, provider, model: providerModels[provider]?.[0] || '' }));

  const handleSave = async () => {
    try {
      const response = await fetch(`${API_BASE}/agents/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formData) });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      router.push('/registry');
    } catch (err) { console.error('Failed to update:', err); }
  };

  const Section = ({ title, children }: { title: string; children: React.ReactNode }) => (
    <div style={{ background: tokens.colors.card, border: `1px solid ${tokens.colors.border}`, borderRadius: '8px', padding: tokens.spacing.md, marginBottom: tokens.spacing.md }}>
      <h3 style={{ fontSize: tokens.font.size.body, fontWeight: 600, margin: `0 0 ${tokens.spacing.md}`, color: tokens.colors.textMuted, textTransform: 'uppercase', letterSpacing: '0.5px' }}>{title}</h3>
      {children}
    </div>
  );

  if (loading) return <div style={{ minHeight: '100vh', background: tokens.colors.background, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>Loading...</div>;

  return (
    <div style={{ minHeight: '100vh', background: tokens.colors.background, fontFamily: tokens.font.family, color: tokens.colors.text }}>
      <header style={{ background: tokens.colors.card, borderBottom: `1px solid ${tokens.colors.border}`, padding: `${tokens.spacing.md} ${tokens.spacing.xl}`, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h1 style={{ fontSize: tokens.font.size.h2, fontWeight: 600, margin: 0 }}>Edit Agent</h1>
        <div style={{ display: 'flex', gap: tokens.spacing.sm }}>
          <Link href="/registry" style={{ padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, borderRadius: '6px', textDecoration: 'none', color: tokens.colors.text, border: `1px solid ${tokens.colors.border}`, background: tokens.colors.card }}>Cancel</Link>
          <button onClick={handleSave} style={{ background: tokens.colors.primary, color: 'white', padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, borderRadius: '6px', border: 'none', fontWeight: 500, cursor: 'pointer' }}>Save</button>
        </div>
      </header>

      <main style={{ padding: tokens.spacing.xl, maxWidth: '800px' }}>
        <Section title="Basic">
          <div style={{ marginBottom: tokens.spacing.md }}>
            <label style={{ display: 'block', fontSize: tokens.font.size.small, fontWeight: 500, marginBottom: tokens.spacing.xs }}>Name</label>
            <input type="text" value={formData.name} onChange={(e) => handleChange('name', e.target.value)} style={{ width: '100%', padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, border: `1px solid ${tokens.colors.border}`, borderRadius: '6px', fontSize: tokens.font.size.body, boxSizing: 'border-box' }} />
          </div>
          <div><textarea value={formData.description} onChange={(e) => handleChange('description', e.target.value)} style={{ width: '100%', padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, border: `1px solid ${tokens.colors.border}`, borderRadius: '6px', fontSize: tokens.font.size.body, minHeight: '80px', fontFamily: tokens.font.family }} /></div>
        </Section>

        <Section title="Provider">
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: tokens.spacing.md, marginBottom: tokens.spacing.md }}>
            <div>
              <label style={{ display: 'block', fontSize: tokens.font.size.small, fontWeight: 500, marginBottom: tokens.spacing.xs }}>SDK</label>
              <select value={formData.provider} onChange={(e) => handleProviderChange(e.target.value)} style={{ width: '100%', padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, border: `1px solid ${tokens.colors.border}`, borderRadius: '6px', background: 'white' }}>
                <option value="openai">OpenAI</option>
                <option value="google">Google</option>
                <option value="microsoft">Microsoft</option>
                <option value="langchain">LangChain</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', fontSize: tokens.font.size.small, fontWeight: 500, marginBottom: tokens.spacing.xs }}>Model</label>
              <select value={formData.model} onChange={(e) => handleChange('model', e.target.value)} style={{ width: '100%', padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, border: `1px solid ${tokens.colors.border}`, borderRadius: '6px', background: 'white' }}>
                {(providerModels[formData.provider] || []).map(m => <option key={m} value={m}>{m}</option>)}
              </select>
            </div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: tokens.spacing.md }}>
            <div><label style={{ fontSize: tokens.font.size.small }}>Temperature: {formData.temperature}</label><input type="range" min={0} max={2} step={0.1} value={formData.temperature} onChange={(e) => handleChange('temperature', parseFloat(e.target.value))} style={{ width: '100%' }} /></div>
            <div><label style={{ fontSize: tokens.font.size.small }}>Max Tokens: {formData.maxTokens}</label><input type="range" min={100} max={128000} step={100} value={formData.maxTokens} onChange={(e) => handleChange('maxTokens', parseInt(e.target.value))} style={{ width: '100%' }} /></div>
          </div>
        </Section>

        <Section title="UI">
          <label style={{ display: 'flex', alignItems: 'center', gap: tokens.spacing.sm }}><input type="checkbox" checked={formData.enableChat} onChange={(e) => handleChange('enableChat', e.target.checked)} /><span>Chat UI</span></label>
          <label style={{ display: 'flex', alignItems: 'center', gap: tokens.spacing.sm }}><input type="checkbox" checked={formData.enableRAG} onChange={(e) => handleChange('enableRAG', e.target.checked)} /><span>RAG UI</span></label>
        </Section>
      </main>
    </div>
  );
}