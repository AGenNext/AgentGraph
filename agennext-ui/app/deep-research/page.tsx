'use client';

import { useState } from 'react';

interface ResearchTask {
  id: string;
  query: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  sources: number;
  started: string;
  duration: string;
  agent: string;
}

interface ResearchStage {
  id: number;
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  result?: string;
}

interface ResearchSource {
  name: string;
  status: 'pending' | 'found' | 'error';
  relevance?: number;
  url?: string;
}

const researchTasks: ResearchTask[] = [
  { id: '1', query: 'Compare multimodal AI models for enterprise', status: 'completed', progress: 100, sources: 12, started: '10:30:00', duration: '4m 32s', agent: 'Research' },
  { id: '2', query: 'LangChain vs AutoGen benchmark', status: 'completed', progress: 100, sources: 8, started: '11:00:00', duration: '2m 15s', agent: 'Research' },
  { id: '3', query: 'Claude API pricing analysis', status: 'running', progress: 65, sources: 5, started: '11:15:00', duration: '1m 20s', agent: 'Sales' },
  { id: '4', query: 'Azure OpenAI limits', status: 'completed', progress: 100, sources: 6, started: '11:30:00', duration: '45s', agent: 'DevOps' },
  { id: '5', query: 'Best RAG implementations 2024', status: 'pending', progress: 0, sources: 0, started: '-', duration: '-', agent: 'Research' },
];

const initialStages: ResearchStage[] = [
  { id: 1, name: 'Query Analysis', status: 'completed', result: 'Extracted key topics: AI agents, enterprise deployment, ROI metrics' },
  { id: 2, name: 'Web Search', status: 'completed', result: 'Found 47 relevant sources' },
  { id: 3, name: 'Source Screening', status: 'completed', result: 'Selected 12 high-quality sources' },
  { id: 4, name: 'Deep Dive Research', status: 'running', result: 'Analyzing 8 technical papers and 4 case studies...' },
  { id: 5, name: 'Synthesis', status: 'pending' },
  { id: 6, name: 'Report Generation', status: 'pending' },
];

const sources: ResearchSource[] = [
  { name: 'ArXiv Papers', status: 'found', relevance: 95, url: 'arxiv.org' },
  { name: 'HuggingFace', status: 'found', relevance: 88, url: 'huggingface.co' },
  { name: 'GitHub', status: 'found', relevance: 82, url: 'github.com' },
  { name: 'Tech Blogs', status: 'found', relevance: 75, url: 'anthropic.com' },
  { name: 'Industry Reports', status: 'found', relevance: 71, url: 'gartner.com' },
  { name: 'Academic', status: 'pending', relevance: 0 },
];

export default function DeepResearchPage() {
  const [query, setQuery] = useState('');
  const [stages, setStages] = useState<ResearchStage[]>(initialStages);
  const [researching, setResearching] = useState(false);
  const [view, setView] = useState<'run' | 'history'>('run');
  const [taskFilter, setTaskFilter] = useState<string>('all');

  const startResearch = () => {
    if (!query.trim()) return;
    setResearching(true);
    
    let currentStage = 0;
    const runNext = () => {
      if (currentStage >= stages.length) {
        setResearching(false);
        return;
      }
      
      setStages(prev => prev.map((s, i) => {
        if (i < currentStage) return { ...s, status: 'completed', result: s.result || 'Done' };
        if (i === currentStage) return { ...s, status: 'running' };
        return { ...s, status: 'pending' };
      }));
      
      currentStage++;
      setTimeout(runNext, 1500);
    };
    runNext();
  };

  const statusColors: Record<string, { bg: string; text: string; icon: string }> = {
    pending: { bg: '#21262d', text: '#8b949e', icon: '○' },
    running: { bg: '#23863622', text: '#3fb950', icon: '⟳' },
    completed: { bg: '#23863622', text: '#3fb950', icon: '✓' },
    failed: { bg: '#f8514922', text: '#f85149', icon: '✕' },
  };

  const filteredTasks = researchTasks.filter(t => taskFilter === 'all' || t.status === taskFilter);

  return (
    <div style={{ padding: 24, background: '#0a0e14', minHeight: '100vh', color: '#e6edf3', fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <div>
          <h1 style={{ fontSize: 28, fontWeight: 600, marginBottom: 8, color: '#f0f6fc' }}>Deep Research</h1>
          <p style={{ color: '#8b949e', fontSize: 14 }}>Multi-stage autonomous research agent</p>
        </div>
        <div style={{ display: 'flex', gap: 4, background: '#161b22', borderRadius: 8, padding: 4 }}>
          <button onClick={() => setView('run')} style={{ padding: '8px 16px', background: view === 'run' ? '#238636' : 'transparent', border: 'none', borderRadius: 6, color: '#fff', fontSize: 13, cursor: 'pointer' }}>Run</button>
          <button onClick={() => setView('history')} style={{ padding: '8px 16px', background: view === 'history' ? '#238636' : 'transparent', border: 'none', borderRadius: 6, color: '#fff', fontSize: 13, cursor: 'pointer' }}>History</button>
        </div>
      </div>

      {view === 'history' ? (
        <div style={{ background: '#161b22', borderRadius: 8, border: '1px solid #30363d', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
            <thead>
              <tr style={{ background: '#21262d', borderBottom: '1px solid #30363d' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontWeight: 600, color: '#8b949e', fontSize: 11, textTransform: 'uppercase' }}>Query</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontWeight: 600, color: '#8b949e', fontSize: 11, textTransform: 'uppercase' }}>Status</th>
                <th style={{ padding: '12px 16px', textAlign: 'center', fontWeight: 600, color: '#8b949e', fontSize: 11, textTransform: 'uppercase' }}>Progress</th>
                <th style={{ padding: '12px 16px', textAlign: 'center', fontWeight: 600, color: '#8b949e', fontSize: 11, textTransform: 'uppercase' }}>Sources</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontWeight: 600, color: '#8b949e', fontSize: 11, textTransform: 'uppercase' }}>Agent</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontWeight: 600, color: '#8b949e', fontSize: 11, textTransform: 'uppercase' }}>Started</th>
                <th style={{ padding: '12px 16px', textAlign: 'right', fontWeight: 600, color: '#8b949e', fontSize: 11, textTransform: 'uppercase' }}>Duration</th>
              </tr>
            </thead>
            <tbody>
              {filteredTasks.map(t => (
                <tr key={t.id} style={{ borderBottom: '1px solid #21262d' }}>
                  <td style={{ padding: '12px 16px', maxWidth: 250 }}>{t.query}</td>
                  <td style={{ padding: '12px 16px' }}>
                    <span style={{ padding: '2px 8px', borderRadius: 4, fontSize: 10, fontWeight: 500, background: t.status === 'completed' ? 'rgba(63,185,80,0.15)' : t.status === 'running' ? 'rgba(210,153,34,0.15)' : 'rgba(139,148,158,0.15)', color: t.status === 'completed' ? '#3fb950' : t.status === 'running' ? '#d29922' : '#8b949e', textTransform: 'uppercase' }}>{t.status}</span>
                  </td>
                  <td style={{ padding: '12px 16px', textAlign: 'center' }}>
                    <div style={{ width: 80, height: 4, background: '#21262d', borderRadius: 2, overflow: 'hidden' }}>
                      <div style={{ width: t.progress + '%', height: '100%', background: t.status === 'completed' ? '#3fb950' : '#d29922' }} />
                    </div>
                  </td>
                  <td style={{ padding: '12px 16px', textAlign: 'center', fontWeight: 500 }}>{t.sources}</td>
                  <td style={{ padding: '12px 16px' }}>{t.agent}</td>
                  <td style={{ padding: '12px 16px', fontSize: 12, color: '#8b949e', fontFamily: 'monospace' }}>{t.started}</td>
                  <td style={{ padding: '12px 16px', textAlign: 'right', fontSize: 12, color: '#8b949e' }}>{t.duration}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (

      <div style={{ marginBottom: 32 }}>
        <textarea value={query} onChange={e => setQuery(e.target.value)} placeholder="What would you like to research? e.g., Compare multimodal AI models for enterprise use cases..." style={{ width: '100%', minHeight: 100, padding: 14, background: '#161b22', border: '1px solid #30363d', borderRadius: 8, color: '#e6edf3', fontSize: 15, fontFamily: 'inherit', resize: 'vertical', marginBottom: 12 }} />
        <button onClick={startResearch} disabled={!query.trim() || researching} style={{ padding: '12px 24px', background: !query.trim() || researching ? '#21262d' : 'linear-gradient(135deg, #238636, #2ea043)', border: 'none', borderRadius: 8, color: '#fff', fontSize: 14, fontWeight: 600, cursor: query.trim() && !researching ? 'pointer' : 'default' }}>
          {researching ? '⟳ Researching...' : 'Start Deep Research →'}
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: 24, marginBottom: 32 }}>
        <div>
          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 16 }}>Research Pipeline</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {stages.map(stage => (
              <div key={stage.id} style={{ padding: 16, background: '#161b22', borderRadius: 8, border: `2px solid ${statusColors[stage.status].text}33`, opacity: stage.status === 'pending' ? 0.5 : 1 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <span style={{ color: statusColors[stage.status].text, fontSize: 16 }}>{stage.status === 'running' ? '⟳' : stage.status === 'completed' ? '✓' : stage.status === 'failed' ? '✕' : '○'}</span>
                  <div style={{ flex: 1 }}>
                    <strong style={{ fontSize: 14, color: '#f0f6fc' }}>{stage.name}</strong>
                    {stage.result && <p style={{ fontSize: 12, color: '#8b949e', marginTop: 4 }}>{stage.result}</p>}
                  </div>
                  {stage.status === 'running' && (
                    <div style={{ width: 100, height: 4, background: '#21262d', borderRadius: 2 }}>
                      <div style={{ width: '60%', height: '100%', background: '#3fb950', borderRadius: 2, animation: 'pulse 1s infinite' }} />
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 16 }}>Sources Found</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {sources.map(s => (
              <div key={s.name} style={{ padding: 12, background: '#161b22', borderRadius: 8, display: 'flex', justifyContent: 'space-between', alignItems: 'center', opacity: s.status === 'pending' ? 0.5 : 1 }}>
                <span style={{ fontSize: 13 }}>{s.name}</span>
                <span style={{ fontSize: 12, color: s.status === 'found' ? '#3fb950' : '#8b949e' }}>
                  {s.status === 'found' ? `✓ ${s.relevance}%` : s.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </div>
  );
}