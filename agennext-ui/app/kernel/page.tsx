'use client';

import { useState } from 'react';

// Microsoft Semantic Kernel Integration
// Source: https://github.com/microsoft/semantic-kernel
// Ref: Semantic Kernel + AutoGen = Microsoft Agent Framework

interface KernelComponent {
  id: string;
  name: string;
  type: 'planner' | 'memory' | 'tools' | 'agents' | 'pipeline' | 'observability';
  status: 'healthy' | 'degraded';
  description: string;
  semanticKernel: string;
}

const components: KernelComponent[] = [
  // Core SK Components
  { id: 'sk-1', name: 'Kernel Core', type: 'planner', status: 'healthy', description: 'Central orchestrator for all AI services', semanticKernel: 'Kernel class' },
  { id: 'sk-2', name: 'Prompt Pipeline', type: 'pipeline', status: 'healthy', description: 'Filters for prompts (templating, validation)', semanticKernel: 'PromptFilter' },
  { id: 'sk-3', name: 'Function Calling', type: 'tools', status: 'healthy', description: 'Native function calling with AI', semanticKernel: 'FunctionCalling' },
  { id: 'sk-4', name: 'Semantic Memory', type: 'memory', status: 'healthy', description: 'Vector-based memory with embeddings', semanticKernel: 'SemanticMemory' },
  { id: 'sk-5', name: 'Planner', type: 'planner', status: 'healthy', description: 'Auto-generates plans from goals', semanticKernel: 'StepwisePlanner' },
  { id: 'sk-6', name: 'Agent Runtime', type: 'agents', status: 'healthy', description: 'Agent runtime with chat history', semanticKernel: 'AgentClient' },
  
  // AutoGen Integration (Microsoft Agent Framework)
  { id: 'ag-1', name: 'Multi-Agent Chat', type: 'agents', status: 'healthy', description: 'Collaborative multi-agent conversations', semanticKernel: 'ChatCompletionAgent' },
  { id: 'ag-2', name: 'Code Executor', type: 'tools', status: 'healthy', description: 'Execute Python/C# in containers', semanticKernel: 'CodeInterpreter' },
  { id: 'ag-3', name: 'Azure AI Agent', type: 'agents', status: 'healthy', description: 'Azure AI Foundry integration', semanticKernel: 'AzureAIAgent' },
];

const supportedModels = [
  { provider: 'OpenAI', models: ['GPT-4o', 'GPT-4 Turbo', 'GPT-3.5'] },
  { provider: 'Anthropic', models: ['Claude 3.5', 'Claude 3', 'Claude Haiku'] },
  { provider: 'Google', models: ['Gemini 1.5 Pro', 'Gemini 1.5 Flash'] },
  { provider: 'Azure OpenAI', models: ['GPT-4', 'GPT-3.5'] },
  { provider: 'Hugging Face', models: ['Llama', 'Mistral', 'Falcon'] },
  { provider: 'Ollama', models: ['Llama 3', 'Mistral', 'Codellama'] },
];

export default function SemanticKernelPage() {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <div style={{ padding: 32, fontFamily: "'SF Pro Display', -apple-system", background: '#050507', minHeight: '100vh', color: '#F4F4F5' }}>
      {/* Header */}
      <div style={{ marginBottom: 32 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
          <h1 style={{ fontSize: 32, fontWeight: 700, margin: 0 }}>Microsoft Agent Framework</h1>
          <span style={{ background: '#0078D420', color: '#0078D4', padding: '4px 10px', borderRadius: 6, fontSize: 11 }}>Semantic Kernel + AutoGen</span>
        </div>
        <p style={{ color: '#A1A1AA', margin: 0, fontSize: 15 }}>Unified Microsoft Agent Framework combining Semantic Kernel + AutoGen</p>
        <p style={{ color: '#0078D4', margin: '8px 0 0 0', fontSize: 12 }}>
          Source: <a href="https://github.com/microsoft/semantic-kernel" target="_blank" style={{ color: '#0078D4' }}>github.com/microsoft/semantic-kernel</a>
        </p>
      </div>

      {/* Architecture */}
      <div style={{ marginBottom: 40 }}>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Architecture Flow</h2>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16, justifyContent: 'center', padding: 24, background: '#0E0E12', borderRadius: 16 }}>
          <div style={{ background: '#16161D', padding: 16, borderRadius: 12, textAlign: 'center' }}>
            <div style={{ fontSize: 24, marginBottom: 8 }}>🎯</div>
            <div style={{ fontSize: 12, fontWeight: 600 }}>User Goal</div>
          </div>
          <span style={{ color: '#0078D4', fontSize: 20 }}>→</span>
          <div style={{ background: '#16161D', padding: 16, borderRadius: 12, textAlign: 'center' }}>
            <div style={{ fontSize: 24, marginBottom: 8 }}>📋</div>
            <div style={{ fontSize: 12, fontWeight: 600 }}>Planner</div>
          </div>
          <span style={{ color: '#0078D4', fontSize: 20 }}>→</span>
          <div style={{ background: '#16161D', padding: 16, borderRadius: 12, textAlign: 'center' }}>
            <div style={{ fontSize: 24, marginBottom: 8 }}>🔧</div>
            <div style={{ fontSize: 12, fontWeight: 600 }}>Kernel</div>
          </div>
          <span style={{ color: '#0078D4', fontSize: 20 }}>→</span>
          <div style={{ background: '#16161D', padding: 16, borderRadius: 12, textAlign: 'center' }}>
            <div style={{ fontSize: 24, marginBottom: 8 }}>🧠</div>
            <div style={{ fontSize: 12, fontWeight: 600 }}>LLM</div>
          </div>
          <span style={{ color: '#0078D4', fontSize: 20 }}>→</span>
          <div style={{ background: '#16161D', padding: 16, borderRadius: 12, textAlign: 'center' }}>
            <div style={{ fontSize: 24, marginBottom: 8 }}>⚡</div>
            <div style={{ fontSize: 12, fontWeight: 600 }}>Execute</div>
          </div>
        </div>
      </div>

      {/* Supported Models */}
      <div style={{ marginBottom: 40 }}>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Supported Models</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          {supportedModels.map(sm => (
            <div key={sm.provider} style={{ background: '#0E0E12', borderRadius: 12, padding: 16, border: '1px solid #232329' }}>
              <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 8 }}>{sm.provider}</div>
              <div style={{ fontSize: 11, color: '#71717A' }}>{sm.models.join(', ')}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Components */}
      <div>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Semantic Kernel Components</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          {components.map(c => (
            <div key={c.id} onClick={() => setSelected(c.id === selected ? null : c.id)}
              style={{ background: '#0E0E12', borderRadius: 12, border: `1px solid ${selected === c.id ? '#0078D4' : '#232329'}`, padding: 20, cursor: 'pointer' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                <span style={{ fontSize: 11, color: '#71717A', textTransform: 'uppercase' }}>{c.type}</span>
                <span style={{ width: 8, height: 8, borderRadius: 4, background: c.status === 'healthy' ? '#10B981' : '#F59E0B' }} />
              </div>
              <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 4 }}>{c.name}</div>
              <div style={{ fontSize: 12, color: '#A1A1AA', marginBottom: 8 }}>{c.description}</div>
              <div style={{ fontSize: 11, color: '#0078D4', fontFamily: 'monospace' }}>{c.semanticKernel}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}