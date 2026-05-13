'use client';

import { useState } from 'react';

interface Step {
  id: number;
  title: string;
  description: string;
}

interface GeneratedAgent {
  name: string;
  role: string;
  framework: string;
  prompt: string;
  capabilities: string[];
}

const steps: Step[] = [
  { id: 1, title: 'Define Role', description: 'What should your agent do?' },
  { id: 2, title: 'Choose Framework', description: 'Select the underlying framework' },
  { id: 3, title: 'Write Prompt', description: 'Define agent behavior & instructions' },
  { id: 4, title: 'Configure', description: 'Set capabilities & tools' },
  { id: 5, title: 'Generate', description: 'Create and deploy your agent' },
];

export default function CreateAgentPage() {
  const [currentStep, setCurrentStep] = useState(1);
  const [role, setRole] = useState('');
  const [framework, setFramework] = useState('');
  const [prompt, setPrompt] = useState('');
  const [capabilities, setCapabilities] = useState<string[]>([]);
  const [generated, setGenerated] = useState<GeneratedAgent | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const frameworks = ['LangChain', 'AutoGen', 'CrewAI', 'LangGraph', 'SMAP', 'VertexAI', 'Bedrock'];

  const capabilityOptions = ['web-search', 'code-generation', 'data-analysis', 'image-understanding', 'document-processing', 'api-integration', 'database-query', 'text-generation'];

  const toggleCapability = (cap: string) => {
    setCapabilities(prev => prev.includes(cap) ? prev.filter(c => c !== cap) : [...prev, cap]);
  };

  const generateAgent = () => {
    setIsGenerating(true);
    setTimeout(() => {
      setGenerated({
        name: `${role.split(' ')[0]} Agent`,
        role,
        framework,
        prompt,
        capabilities,
      });
      setIsGenerating(false);
    }, 2000);
  };

  return (
    <div style={{ padding: 24, background: '#0a0e14', minHeight: '100vh', color: '#e6edf3', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 8, color: '#f0f6fc' }}>Create Agent</h1>
      <p style={{ color: '#8b949e', fontSize: 14, marginBottom: 32 }}>Build your custom AI agent with prompt engineering</p>

      {/* Progress Steps */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 40, position: 'relative' }}>
        <div style={{ position: 'absolute', top: 20, left: 40, right: 40, height: 2, background: '#21262d', zIndex: 0 }} />
        <div style={{ position: 'absolute', top: 20, left: 40, height: 2, background: 'linear-gradient(90deg, #238636, #3fb950)', zIndex: 0, width: `${((currentStep - 1) / (steps.length - 1)) * 100}%`, maxWidth: 'calc(100% - 80px)', transition: 'width 0.3s' }} />
        {steps.map(step => (
          <div key={step.id} onClick={() => currentStep > step.id && setCurrentStep(step.id)} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', cursor: currentStep > step.id ? 'pointer' : 'default', zIndex: 1, position: 'relative' }}>
            <div style={{
              width: 40, height: 40, borderRadius: '50%', background: currentStep >= step.id ? 'linear-gradient(135deg, #238636, #2ea043)' : '#21262d',
              border: currentStep === step.id ? '2px solid #3fb950' : '2px solid #30363d', display: 'flex', alignItems: 'center', justifyContent: 'center',
              transition: 'all 0.2s'
            }}>
              <span style={{ fontSize: 14, fontWeight: 600, color: currentStep >= step.id ? '#fff' : '#8b949e' }}>{step.id}</span>
            </div>
            <p style={{ fontSize: 12, marginTop: 8, color: currentStep >= step.id ? '#f0f6fc' : '#8b949e', fontWeight: currentStep === step.id ? 600 : 400 }}>{step.title}</p>
          </div>
        ))}
      </div>

      {/* Step Content */}
      <div style={{ background: '#161b22', borderRadius: 12, border: '1px solid #30363d', padding: 24, minHeight: 300 }}>
        {currentStep === 1 && (
          <div>
            <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Define Agent Role</h2>
            <p style={{ color: '#8b949e', marginBottom: 16 }}>What is the primary purpose of your agent?</p>
            <input value={role} onChange={e => setRole(e.target.value)} placeholder="e.g., Research Analyst, Code Reviewer, Customer Support..." style={{ width: '100%', padding: 12, background: '#0d1117', border: '1px solid #30363d', borderRadius: 8, color: '#e6edf3', fontSize: 14 }} />
          </div>
        )}

        {currentStep === 2 && (
          <div>
            <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Choose Framework</h2>
            <p style={{ color: '#8b949e', marginBottom: 16 }}>Select the agent framework</p>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12 }}>
              {frameworks.map(fw => (
                <div key={fw} onClick={() => setFramework(fw)} style={{ padding: 16, background: framework === fw ? '#238636' : '#21262d', borderRadius: 8, border: framework === fw ? '2px solid #3fb950' : '2px solid transparent', cursor: 'pointer', textAlign: 'center' }}>
                  <span style={{ fontSize: 14, fontWeight: 500 }}>{fw}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {currentStep === 3 && (
          <div>
            <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Write Prompt</h2>
            <p style={{ color: '#8b949e', marginBottom: 16 }}>Define your agent's behavior and instructions</p>
            <textarea value={prompt} onChange={e => setPrompt(e.target.value)} placeholder="You are a helpful AI agent that...&#10;Your responsibilities include:&#10;- Task 1&#10;- Task 2&#10;Always ensure..." style={{ width: '100%', minHeight: 180, padding: 12, background: '#0d1117', border: '1px solid #30363d', borderRadius: 8, color: '#e6edf3', fontSize: 14, fontFamily: 'monospace', resize: 'vertical' }} />
          </div>
        )}

        {currentStep === 4 && (
          <div>
            <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Configure Capabilities</h2>
            <p style={{ color: '#8b949e', marginBottom: 16 }}>Select tools and capabilities</p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
              {capabilityOptions.map(cap => (
                <button key={cap} onClick={() => toggleCapability(cap)} style={{ padding: '8px 16px', background: capabilities.includes(cap) ? '#238636' : '#21262d', border: '1px solid #30363d', borderRadius: 6, color: '#fff', fontSize: 13, cursor: 'pointer' }}>
                  {capabilities.includes(cap) ? '✓' : '+'} {cap}
                </button>
              ))}
            </div>
          </div>
        )}

        {currentStep === 5 && (
          <div>
            <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Generate Agent</h2>
            {isGenerating ? (
              <div style={{ textAlign: 'center', padding: 40 }}>
                <div style={{ fontSize: 24, marginBottom: 16 }}>⚙️ Generating Agent...</div>
                <div style={{ width: 200, height: 4, background: '#21262d', borderRadius: 2, overflow: 'hidden', margin: '0 auto' }}>
                  <div style={{ width: '60%', height: '100%', background: 'linear-gradient(90deg, #238636, #3fb950)', animation: 'loading 1s ease-in-out infinite' }} />
                </div>
              </div>
            ) : generated ? (
              <div style={{ background: '#0d1117', borderRadius: 8, padding: 16 }}>
                <div style={{ color: '#3fb950', fontSize: 14, marginBottom: 12 }}>✓ Agent Created Successfully!</div>
                <pre style={{ fontSize: 12, color: '#8b949e', fontFamily: 'monospace' }}>{JSON.stringify(generated, null, 2)}</pre>
              </div>
            ) : (
              <div>
                <p style={{ color: '#8b949e', marginBottom: 16 }}>Review your agent configuration and click Generate</p>
                <div style={{ background: '#0d1117', borderRadius: 8, padding: 16, marginBottom: 16 }}>
                  <p><strong style={{ color: '#58a6ff' }}>Role:</strong> {role || '-'}</p>
                  <p><strong style={{ color: '#58a6ff' }}>Framework:</strong> {framework || '-'}</p>
                  <p><strong style={{ color: '#58a6ff' }}>Capabilities:</strong> {capabilities.join(', ') || '-'}</p>
                </div>
                <button onClick={generateAgent} style={{ padding: '12px 24px', background: 'linear-gradient(135deg, #238636, #2ea043)', border: 'none', borderRadius: 8, color: '#fff', fontSize: 14, fontWeight: 600, cursor: 'pointer' }}>
                  Generate Agent
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Navigation */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 24 }}>
        <button onClick={() => setCurrentStep(prev => Math.max(1, prev - 1))} disabled={currentStep === 1} style={{ padding: '10px 20px', background: '#21262d', border: '1px solid #30363d', borderRadius: 8, color: '#fff', fontSize: 14, cursor: currentStep === 1 ? 'default' : 'pointer' }}>
          ← Back
        </button>
        <button onClick={() => setCurrentStep(prev => Math.min(steps.length, prev + 1))} disabled={currentStep === steps.length} style={{ padding: '10px 20px', background: currentStep === steps.length ? '#21262d' : 'linear-gradient(135deg, #238636, #2ea043)', border: 'none', borderRadius: 8, color: '#fff', fontSize: 14, cursor: currentStep === steps.length ? 'default' : 'pointer' }}>
          {currentStep === steps.length ? 'Complete' : 'Next →'}
        </button>
      </div>

      <style>{`
        @keyframes loading {
          0% { width: 0%; }
          50% { width: 70%; }
          100% { width: 100%; }
        }
      `}</style>
    </div>
  );
}