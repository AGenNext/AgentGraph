'use client';

import { useState } from 'react';

interface CodeSnippet {
  id: string;
  title: string;
  language: string;
  code: string;
  description: string;
}

const snippets: CodeSnippet[] = [
  { id: '1', title: 'Initialize Agent Zero', language: 'python', code: 'from agent_zero import AgentOrchestrator\n\nagent = AgentOrchestrator(\n    name="Agent Zero",\n    frameworks=["langchain", "autogen"],\n    capabilities=["reasoning", "tool_use"]\n)', description: 'Create a new agent with custom capabilities' },
  { id: '2', title: 'Chain Multiple Agents', language: 'python', code: 'from langchain import LLMChain\n\n# Create agent chain\nresearch_chain = LLMChain(agent=research_agent, prompt=research_prompt)\ncode_chain = LLMChain(agent=code_agent, prompt=code_prompt)\n\n# Orchestrate\nresult = research_chain.run(topic) | code_chain.run', description: 'Connect agents in a pipeline' },
  { id: '3', title: 'Add Custom Tool', language: 'python', code: 'from agent_zero.tools import tool\n\n@tool\ndef search_web(query: str) -> str:\n    """Search the web for information."""\n    return web_search(query)\n\nagent.add_tool(search_web)', description: 'Register a custom tool function' },
  { id: '4', title: 'System Prompt', language: 'python', code: 'system_prompt = """You are a {role} agent.\n\nGuidelines:\n1. Be concise\n2. Validate inputs\n3. Log decisions\n\nAvailable tools: {tools}"""', description: 'Configure agent system prompt' },
  { id: '5', title: 'Streaming Response', language: 'javascript', code: '// JavaScript streaming\const stream = await agent.stream({\n  prompt: "Explain quantum computing",\n  stream: true\n});\n\nfor await (const chunk of stream) {\n  console.log(chunk);\n}', description: 'Stream agent responses' },
  { id: '6', title: 'Memory Integration', language: 'python', code: 'from agent_zero.memory import Memory\n\nmemory = Memory(\n    window_size=10,\n    importance_threshold=7\n)\n\n# Store conversation\nmemory.add({\n    role: "user",\n    content: "I prefer concise answers"\n})\n\n# Query memory\nprefs = memory.query("user preferences")', description: 'Add persistent memory' },
];

export default function CodeAssistPage() {
  const [selected, setSelected] = useState<string>('1');
  const [copied, setCopied] = useState(false);

  const active = snippets.find(s => s.id === selected) || snippets[0];

  const copyCode = () => {
    navigator.clipboard.writeText(active.code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const langColors: Record<string, string> = {
    python: '#3572A5',
    javascript: '#f7df1e',
    typescript: '#2b7489',
    bash: '#89e051',
  };

  return (
    <div style={{ padding: 24, background: '#0a0e14', minHeight: '100vh', color: '#e6edf3', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 8, color: '#f0f6fc' }}>Code Assist</h1>
      <p style={{ color: '#8b949e', fontSize: 14, marginBottom: 32 }}>Code snippets & examples for agent development</p>

      <div style={{ display: 'grid', gridTemplateColumns: '280px 1fr', gap: 24 }}>
        <div>
          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Snippets</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {snippets.map(s => (
              <div key={s.id} onClick={() => setSelected(s.id)} style={{ 
                padding: 12, background: selected === s.id ? '#1f242c' : '#161b22', 
                borderRadius: 8, border: selected === s.id ? '2px solid #238636' : '1px solid #30363d', 
                cursor: 'pointer' 
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <strong style={{ fontSize: 14, color: '#f0f6fc' }}>{s.title}</strong>
                  <span style={{ padding: '2px 6px', borderRadius: 4, fontSize: 10, background: langColors[s.language] + '33', color: langColors[s.language], textTransform: 'uppercase' }}>
                    {s.language}
                  </span>
                </div>
                <p style={{ fontSize: 12, color: '#8b949e', marginTop: 4 }}>{s.description}</p>
              </div>
            ))}
          </div>
        </div>

        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <h2 style={{ fontSize: 16, fontWeight: 600 }}>{active.title}</h2>
            <div style={{ display: 'flex', gap: 8 }}>
              <button onClick={copyCode} style={{ padding: '6px 12px', background: '#21262d', border: '1px solid #30363d', borderRadius: 6, color: '#fff', fontSize: 12, cursor: 'pointer' }}>
                {copied ? '✓ Copied' : '📋 Copy'}
              </button>
              <button style={{ padding: '6px 12px', background: '#238636', border: 'none', borderRadius: 6, color: '#fff', fontSize: 12, cursor: 'pointer' }}>
                ▶ Run
              </button>
            </div>
          </div>
          
          <div style={{ position: 'relative', background: '#0d1117', borderRadius: 8, border: '1px solid #30363d', overflow: 'hidden' }}>
            <div style={{ padding: '8px 12px', background: '#161b22', borderBottom: '1px solid #21262d', display: 'flex', justifyContent: 'space-between', fontSize: 11, color: '#8b949e' }}>
              <span>{active.language}</span>
              <span>{active.code.split('\n').length} lines</span>
            </div>
            <pre style={{ padding: 16, fontSize: 13, fontFamily: 'Menlo, Monaco, monospace', lineHeight: 1.6, overflow: 'auto' }}>
{active.code}
            </pre>
          </div>

          <div style={{ marginTop: 16, padding: 16, background: '#161b22', borderRadius: 8, border: '1px solid #30363d' }}>
            <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 8 }}>Related Examples</h3>
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              <span style={{ padding: '4px 10px', background: '#21262d', borderRadius: 6, fontSize: 12, color: '#8b949e' }}>Memory Integration</span>
              <span style={{ padding: '4px 10px', background: '#21262d', borderRadius: 6, fontSize: 12, color: '#8b949e' }}>Tool Creation</span>
              <span style={{ padding: '4px 10px', background: '#21262d', borderRadius: 6, fontSize: 12, color: '#8b949e' }}>Prompt Engineering</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}