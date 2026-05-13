'use client';

import { useState } from 'react';
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

export default function NewAgentPage() {
  const router = useRouter();
  const [formData, setFormData] = useState<AgentFormData>({ name: '', description: '', provider: 'openai', model: 'gpt-4o', temperature: 0.7, maxTokens: 2000, systemPrompt: '', authMethod: 'api_key', apiKey: '', enableChat: true, enableRAG: false, tools: ['calculator', 'search'] });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [showApiKey, setShowApiKey] = useState(false);

  const handleChange = (field: keyof AgentFormData, value: string | number | boolean | string[]) => setFormData(prev => ({ ...prev, [field]: value }));
  const handleProviderChange = (provider: string) => setFormData(prev => ({ ...prev, provider, model: providerModels[provider]?.[0] || '' }));

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};
    if (!formData.name.trim()) newErrors.name = 'This field is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSave = async () => {
    if (!validate()) return;
    try {
      const response = await fetch(`${API_BASE}/agents`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formData) });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      router.push('/registry');
    } catch (err) { console.error('Failed to save:', err); }
  };

  const Section = ({ title, children }: { title: string; children: React.ReactNode }) => (
    <div style={{ background: tokens.colors.card, border: `1px solid ${tokens.colors.border}`, borderRadius: '8px', padding: tokens.spacing.md, marginBottom: tokens.spacing.md }}>
      <h3 style={{ fontSize: tokens.font.size.body, fontWeight: 600, margin: `0 0 ${tokens.spacing.md}`, color: tokens.colors.textMuted, textTransform: 'uppercase', letterSpacing: '0.5px' }}>{title}</h3>
      {children}
    </div>
  );

  return (
    <div style={{ minHeight: '100vh', background: tokens.colors.background, fontFamily: tokens.font.family, color: tokens.colors.text }}>
      <header style={{ background: tokens.colors.card, borderBottom: `1px solid ${tokens.colors.border}`, padding: `${tokens.spacing.md} ${tokens.spacing.xl}`, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h1 style={{ fontSize: tokens.font.size.h2, fontWeight: 600, margin: 0 }}>+ New Agent</h1>
        <div style={{ display: 'flex', gap: tokens.spacing.sm }}>
          <Link href="/registry" style={{ padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, borderRadius: '6px', textDecoration: 'none', color: tokens.colors.text, border: `1px solid ${tokens.colors.border}`, background: tokens.colors.card }}>Cancel</Link>
          <button onClick={handleSave} style={{ background: tokens.colors.primary, color: 'white', padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, borderRadius: '6px', border: 'none', fontWeight: 500, cursor: 'pointer' }}>Save</button>
        </div>
      </header>

      <main style={{ padding: tokens.spacing.xl, maxWidth: '800px' }}>
        <Section title="Basic">
          <div style={{ marginBottom: tokens.spacing.md }}>
            <label style={{ display: 'block', fontSize: tokens.font.size.small, fontWeight: 500, marginBottom: tokens.spacing.xs }}>Name</label>
            <input type="text" value={formData.name} onChange={(e) => handleChange('name', e.target.value)} placeholder="Agent name" style={{ width: '100%', padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, border: `1px solid ${errors.name ? '#ef4444' : tokens.colors.border}`, borderRadius: '6px', fontSize: tokens.font.size.body, outline: 'none', boxSizing: 'border-box' }} />
            {errors.name && <span style={{ color: '#ef4444', fontSize: tokens.font.size.small }}>← {errors.name}</span>}
          </div>
          <div>
            <label style={{ display: 'block', fontSize: tokens.font.size.small, fontWeight: 500, marginBottom: tokens.spacing.xs }}>Description</label>
            <textarea value={formData.description} onChange={(e) => handleChange('description', e.target.value)} placeholder="Describe what this agent does..." maxLength={500} style={{ width: '100%', padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, border: `1px solid ${tokens.colors.border}`, borderRadius: '6px', fontSize: tokens.font.size.body, outline: 'none', minHeight: '80px', resize: 'vertical', fontFamily: tokens.font.family }} />
          </div>
        </Section>

        <Section title="Provider">
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: tokens.spacing.md, marginBottom: tokens.spacing.md }}>
            <div>
              <label style={{ display: 'block', fontSize: tokens.font.size.small, fontWeight: 500, marginBottom: tokens.spacing.xs }}>SDK</label>
              <select value={formData.provider} onChange={(e) => handleProviderChange(e.target.value)} style={{ width: '100%', padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, border: `1px solid ${tokens.colors.border}`, borderRadius: '6px', fontSize: tokens.font.size.body, background: 'white' }}>
                <option value="openai">OpenAI</option>
                <option value="google">Google</option>
                <option value="microsoft">Microsoft</option>
                <option value="langchain">LangChain</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', fontSize: tokens.font.size.small, fontWeight: 500, marginBottom: tokens.spacing.xs }}>Model</label>
              <select value={formData.model} onChange={(e) => handleChange('model', e.target.value)} style={{ width: '100%', padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, border: `1px solid ${tokens.colors.border}`, borderRadius: '6px', fontSize: tokens.font.size.body, background: 'white' }}>
                {(providerModels[formData.provider] || []).map(m => <option key={m} value={m}>{m}</option>)}
              </select>
            </div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: tokens.spacing.md, marginBottom: tokens.spacing.md }}>
            <div>
              <label style={{ display: 'block', fontSize: tokens.font.size.small, fontWeight: 500, marginBottom: tokens.spacing.xs }}>Temperature: {formData.temperature}</label>
              <input type="range" min={0} max={2} step={0.1} value={formData.temperature} onChange={(e) => handleChange('temperature', parseFloat(e.target.value))} style={{ width: '100%' }} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: tokens.font.size.small, fontWeight: 500, marginBottom: tokens.spacing.xs }}>Max Tokens: {formData.maxTokens}</label>
              <input type="range" min={100} max={128000} step={100} value={formData.maxTokens} onChange={(e) => handleChange('maxTokens', parseInt(e.target.value))} style={{ width: '100%' }} />
            </div>
          </div>
          <div>
            <label style={{ display: 'block', fontSize: tokens.font.size.small, fontWeight: 500, marginBottom: tokens.spacing.xs }}>System Prompt</label>
            <textarea value={formData.systemPrompt} onChange={(e) => handleChange('systemPrompt', e.target.value)} placeholder="Instructions for the agent..." style={{ width: '100%', padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, border: `1px solid ${tokens.colors.border}`, borderRadius: '6px', fontSize: tokens.font.size.body, outline: 'none', minHeight: '100px', resize: 'vertical', fontFamily: tokens.font.family }} />
          </div>
        </Section>

        <Section title="Authentication">
          <div style={{ marginBottom: tokens.spacing.md }}>
            <label style={{ display: 'block', fontSize: tokens.font.size.small, fontWeight: 500, marginBottom: tokens.spacing.xs }}>Auth Method</label>
            <select value={formData.authMethod} onChange={(e) => handleChange('authMethod', e.target.value)} style={{ width: '100%', padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, border: `1px solid ${tokens.colors.border}`, borderRadius: '6px', fontSize: tokens.font.size.body, background: 'white' }}>
              <option value="api_key">API Key</option>
              <option value="env">Environment Variable</option>
              <option value="oauth">OAuth</option>
            </select>
          </div>
          {formData.authMethod === 'api_key' && (
            <div>
              <label style={{ display: 'block', fontSize: tokens.font.size.small, fontWeight: 500, marginBottom: tokens.spacing.xs }}>API Key</label>
              <div style={{ position: 'relative' }}>
                <input type={showApiKey ? 'text' : 'password'} value={formData.apiKey} onChange={(e) => handleChange('apiKey', e.target.value)} placeholder="sk-..." style={{ width: '100%', padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, border: `1px solid ${tokens.colors.border}`, borderRadius: '6px', fontSize: tokens.font.size.body, outline: 'none', boxSizing: 'border-box' }} />
                <button type="button" onClick={() => setShowApiKey(!showApiKey)} style={{ position: 'absolute', right: tokens.spacing.sm, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', fontSize: tokens.font.size.small }}>{showApiKey ? 'Hide' : 'Show'}</button>
              </div>
            </div>
          )}
        </Section>

        <Section title="UI Interface">
          <div style={{ display: 'flex', flexDirection: 'column', gap: tokens.spacing.sm }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: tokens.spacing.sm }}><input type="checkbox" checked={formData.enableChat} onChange={(e) => handleChange('enableChat', e.target.checked)} /><span>Chat UI</span></label>
            <label style={{ display: 'flex', alignItems: 'center', gap: tokens.spacing.sm }}><input type="checkbox" checked={formData.enableRAG} onChange={(e) => handleChange('enableRAG', e.target.checked)} /><span>RAG UI</span></label>
            <div style={{ marginTop: tokens.spacing.sm }}>
              <label style={{ display: 'block', fontSize: tokens.font.size.small, fontWeight: 500, marginBottom: tokens.spacing.xs }}>Tools</label>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: tokens.spacing.md }}>
                {['Calculator', 'Search', 'Database', 'Code Interpreter'].map(tool => (
                  <label key={tool} style={{ display: 'flex', alignItems: 'center', gap: tokens.spacing.xs }}><input type="checkbox" checked={formData.tools.includes(tool.toLowerCase())} onChange={(e) => handleChange('tools', e.target.checked ? [...formData.tools, tool.toLowerCase()] : formData.tools.filter(t => t !== tool.toLowerCase())[0] || '')} /><span>{tool}</span></label>
                ))}
              </div>
            </div>
          </div>
        </Section>
      </main>
    </div>
  );
}