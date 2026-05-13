'use client';

import { useState } from 'react';

interface SearchResult {
  id: string;
  title: string;
  url: string;
  snippet: string;
  source: string;
  date: string;
}

const results: SearchResult[] = [
  { id: '1', title: 'LangChain | 🦜🔗 Build context-aware reasoning applications', url: 'https://python.langchain.com', snippet: 'LangChain is a framework for developing applications powered by large language models. It enables AI models to connect to data sources and interact with their environment.', source: 'langchain.com', date: '2024' },
  { id: '2', title: 'AutoGPT | Autonomous GPT-4 Experiment', url: 'https://github.com/Significant-Auto-GPT', snippet: 'An experimental open-source attempt to make GPT-4 fully autonomous. Given a goal, it will accomplish it by breaking it down into sub-tasks.', source: 'github.com', date: '2024' },
  { id: '3', title: 'LangGraph | Build stateful, multi-agent applications', url: 'https://langchain-ai.github.io/langgraph', snippet: 'LangGraph is a library for building stateful, multi-actor applications with LLMs. It extends LangChain with cycles.', source: 'langchain-ai.github.io', date: '2024' },
  { id: '4', title: 'CrewAI | Framework for building autonomous agents', url: 'https://docs.crewai.com', snippet: 'CrewAI is a framework that enables you to build autonomous agents that can collaborate to accomplish complex tasks.', source: 'crewai.com', date: '2024' },
  { id: '5', title: 'SmolAgents | Minimal agent framework by HuggingFace', url: 'https://huggingface.co/smolagents', snippet: 'SmolAgents is a minimal agent framework from HuggingFace. Write agents in a few lines of code with tool support.', source: 'huggingface.co', date: '2024' },
  { id: '6', title: 'Microsoft AutoGen | Multi-agent conversation framework', url: 'https://microsoft.com/autogen', snippet: 'Microsoft AutoGen enables next-gen LLM applications with multi-agent conversations. It automates agent chat workflows.', source: 'microsoft.com', date: '2024' },
  { id: '7', title: 'OpenAI o1 | Next generation reasoning model', url: 'https://openai.com/o1', snippet: 'OpenAI o1 has been trained to think more before responding. It can reason about complex tasks and multi-step problems.', source: 'openai.com', date: '2024' },
  { id: '8', title: 'Anthropic Claude | AI assistant with large context', url: 'https://anthropic.com/claude', snippet: 'Claude is an AI assistant built by Anthropic. It excels at complex reasoning, analysis, and long-form generation.', source: 'anthropic.com', date: '2024' },
];

const recentSearches = ['ai agents framework comparison', 'autogen multi-agent', 'langgraph tutorial', 'crewai tools'];

export default function WebSearchPage() {
  const [query, setQuery] = useState('');
  const [searched, setSearched] = useState(false);

  const handleSearch = () => {
    if (query.trim()) setSearched(true);
  };

  return (
    <div style={{ padding: 24, background: '#0a0e14', minHeight: '100vh', color: '#e6edf3', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 8, color: '#f0f6fc' }}>Web Search</h1>
      <p style={{ color: '#8b949e', fontSize: 14, marginBottom: 32 }}>AI-enhanced search with source citations</p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 32 }}>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#58a6ff' }}>8</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Search Engines</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#3fb950' }}>156</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Results Today</div>
        </div>
        <div style={{ padding: 20, background: 'linear-gradient(135deg, #161b22 0%, #21262d 100%)', borderRadius: 12, border: '1px solid #30363d' }}>
          <div style={{ fontSize: 36, fontWeight: 700, color: '#d29922' }}>0.4s</div>
          <div style={{ color: '#8b949e', fontSize: 13, marginTop: 4 }}>Avg Response Time</div>
        </div>
      </div>

      <div style={{ marginBottom: 24 }}>
        <div style={{ display: 'flex', gap: 12, marginBottom: 12 }}>
          <input value={query} onChange={e => setQuery(e.target.value)} onKeyDown={e => e.key === 'Enter' && handleSearch()} placeholder="Search the web..." style={{ flex: 1, padding: 14, background: '#161b22', border: '1px solid #30363d', borderRadius: 8, color: '#e6edf3', fontSize: 15 }} />
          <button onClick={handleSearch} style={{ padding: '14px 24px', background: 'linear-gradient(135deg, #238636, #2ea043)', border: 'none', borderRadius: 8, color: '#fff', fontSize: 15, fontWeight: 500, cursor: 'pointer' }}>
            🔍 Search
          </button>
        </div>
        <p style={{ fontSize: 12, color: '#8b949e' }}>Recent: {recentSearches.map((s, i) => <span key={s} onClick={() => setQuery(s)} style={{ marginLeft: 8, color: '#58a6ff', cursor: 'pointer' }}>{s}</span>)}</p>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        <span style={{ fontSize: 12, color: '#8b949e', alignSelf: 'center' }}>Filter:</span>
        {['All', 'Documentation', 'GitHub', 'Blog', 'Paper'].map(f => (
          <button key={f} style={{ padding: '6px 12px', background: '#21262d', border: '1px solid #30363d', borderRadius: 6, color: '#fff', fontSize: 12, cursor: 'pointer' }}>{f}</button>
        ))}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {(searched ? results : results.slice(0, 4)).map(result => (
          <div key={result.id} style={{ padding: 16, background: '#161b22', borderRadius: 8, border: '1px solid #30363d' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <div>
                <h3 style={{ fontSize: 16, fontWeight: 600, color: '#58a6ff', marginBottom: 4 }}>{result.title}</h3>
                <p style={{ fontSize: 12, color: '#8b949e' }}>{result.url}</p>
              </div>
              <span style={{ padding: '4px 8px', background: '#21262d', borderRadius: 4, fontSize: 10, color: '#8b949e' }}>{result.source}</span>
            </div>
            <p style={{ fontSize: 13, color: '#8b949e', lineHeight: 1.5 }}>{result.snippet}</p>
          </div>
        ))}
      </div>

      {!searched && (
        <div style={{ textAlign: 'center', marginTop: 24, color: '#8b949e' }}>
          Enter a query to search the web
        </div>
      )}
    </div>
  );
}