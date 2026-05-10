'use client';

import { useState } from 'react';

interface ServiceMetric {
  name: string;
  p50: number;
  p95: number;
  p99: number;
  errorRate: number;
  requests: number;
}

interface Span {
  id: string;
  service: string;
  operation: string;
  duration: number;
  status: 'ok' | 'error';
  timestamp: number;
}

const services: ServiceMetric[] = [
  { name: 'agent-api', p50: 45, p95: 120, p99: 250, errorRate: 0.5, requests: 45200 },
  { name: 'llm-runtime', p50: 1200, p95: 3500, p99: 8000, errorRate: 1.2, requests: 28400 },
  { name: 'vector-store', p50: 25, p95: 80, p99: 150, errorRate: 0.1, requests: 89000 },
  { name: 'auth-service', p50: 15, p95: 45, p99: 80, errorRate: 0.2, requests: 156000 },
  { name: 'workflow-orch', p50: 3500, p95: 12000, p99: 25000, errorRate: 2.1, requests: 12400 },
];

const traces: Span[] = [
  { id: 't1', service: 'agent-api', operation: 'POST /agents/execute', duration: 1450, status: 'ok', timestamp: Date.now() - 5000 },
  { id: 't2', service: 'llm-runtime', operation: 'invoke:claude', duration: 1200, status: 'ok', timestamp: Date.now() - 4000 },
  { id: 't3', service: 'vector-store', operation: 'search', duration: 45, status: 'ok', timestamp: Date.now() - 3000 },
  { id: 't4', service: 'workflow-orch', operation: 'execute:parallel', duration: 2500, status: 'error', timestamp: Date.now() - 2000 },
  { id: 't5', service: 'llm-runtime', operation: 'invoke:bedrock', duration: 3500, status: 'ok', timestamp: Date.now() - 1000 },
];

const metrics = {
  requests: 156240,
  errorRate: 0.8,
  avgLatency: 180,
  apdex: 0.92,
};

export default function SigNozPage() {
  const [tab, setTab] = useState<'services' | 'traces' | 'metrics'>('services');
  
  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>SigNoz APM</h1>
          <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Distributed tracing & performance monitoring</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button style={{ background: '#fff', color: '#1A1A2E', border: '1px solid #E5E5E5', padding: '10px 16px', borderRadius: 6, fontSize: 13, cursor: 'pointer' }}>
            Live
          </button>
          <button style={{ background: '#DA1E28', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 6, fontSize: 13, cursor: 'pointer' }}>
            + New Service
          </button>
        </div>
      </div>

      {/* Overall Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{metrics.requests.toLocaleString()}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Requests/min</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#DA1E28' }}>{metrics.errorRate}%</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Error Rate</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#F59E0B' }}>{metrics.avgLatency}ms</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Avg Latency</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{metrics.apdex}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Apdex Score</div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        {(['services', 'traces', 'metrics'] as const).map(t => (
          <button
            key={t}
            onClick={() => setTab(t)}
            style={{
              background: tab === t ? '#1A1A2E' : '#fff',
              color: tab === t ? '#fff' : '#525252',
              border: '1px solid #E5E5E5',
              padding: '10px 20px',
              borderRadius: 8,
              fontSize: 13,
              cursor: 'pointer',
              textTransform: 'capitalize',
            }}
          >
            {t === 'services' ? 'Services' : t === 'traces' ? 'Traces' : 'Metrics'}
          </button>
        ))}
      </div>

      {tab === 'services' ? (
        <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#F8F9FA' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>SERVICE</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>REQUESTS</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>P50</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>P95</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>P99</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>ERROR RATE</th>
              </tr>
            </thead>
            <tbody>
              {services.map(s => (
                <tr key={s.name} style={{ borderTop: '1px solid #F4F4F4' }}>
                  <td style={{ padding: '14px 16px', fontWeight: 500 }}>{s.name}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12 }}>{s.requests.toLocaleString()}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12, fontFamily: 'monospace' }}>{s.p50}ms</td>
                  <td style={{ padding: '14px 16px', fontSize: 12, fontFamily: 'monospace' }}>{s.p95}ms</td>
                  <td style={{ padding: '14px 16px', fontSize: 12, fontFamily: 'monospace', fontWeight: 600 }}>{s.p99}ms</td>
                  <td style={{ padding: '14px 16px' }}>
                    <span style={{ color: s.errorRate > 1 ? '#DA1E28' : '#10B981', fontSize: 12, fontWeight: 500 }}>
                      {s.errorRate}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : tab === 'traces' ? (
        <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#F8F9FA' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>TRACE ID</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>SERVICE</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>OPERATION</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>DURATION</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>STATUS</th>
              </tr>
            </thead>
            <tbody>
              {traces.map(t => (
                <tr key={t.id} style={{ borderTop: '1px solid #F4F4F4' }}>
                  <td style={{ padding: '14px 16px', fontSize: 12, fontFamily: 'monospace', color: '#0F62FE' }}>{t.id}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12 }}>{t.service}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12 }}>{t.operation}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12, fontWeight: 600 }}>{t.duration}ms</td>
                  <td style={{ padding: '14px 16px' }}>
                    <span style={{ color: t.status === 'ok' ? '#10B981' : '#DA1E28', fontSize: 12, fontWeight: 500 }}>
                      {t.status === 'ok' ? '✓' : '✗'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 16 }}>
          {/* Latency Chart Placeholder */}
          <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', padding: 20 }}>
            <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>Latency (p50, p95, p99)</h3>
            <div style={{ height: 200, display: 'flex', alignItems: 'flex-end', gap: 32, padding: '0 20px' }}>
              {['p50', 'p95', 'p99'].map(p => (
                <div key={p} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <div style={{ 
                    width: 60, 
                    background: p === 'p50' ? '#10B981' : p === 'p95' ? '#F59E0B' : '#DA1E28',
                    borderRadius: '8px 8px 0 0',
                    height: p === 'p50' ? 80 : p === 'p95' ? 150 : 180,
                  }} />
                  <div style={{ fontSize: 12, marginTop: 8, color: '#6B7280' }}>{p.toUpperCase()}</div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Error Rate Chart Placeholder */}
          <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', padding: 20 }}>
            <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>Error Rate %</h3>
            <div style={{ height: 200, display: 'flex', alignItems: 'flex-end', justifyContent: 'center' }}>
              <div style={{ 
                width: 100, 
                height: 15, 
                background: '#DA1E2820',
                borderRadius: 8,
                display: 'flex',
                alignItems: 'flex-end',
              }}>
                <div style={{ width: '100%', height: '15%', background: '#DA1E28', borderRadius: 8 }} />
              </div>
            </div>
            <div style={{ textAlign: 'center', marginTop: 16, fontSize: 24, fontWeight: 600, color: '#DA1E28' }}>0.8%</div>
          </div>
        </div>
      )}

      {/* SDK Info */}
      <div style={{ marginTop: 24, background: '#1A1A2E', borderRadius: 8, padding: 20, color: '#fff' }}>
        <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>OpenTelemetry SDK</h3>
        <div style={{ background: '#0D0D14', padding: 16, borderRadius: 8, fontFamily: 'monospace', fontSize: 12 }}>
          <div style={{ color: '#10B981', marginBottom: 8 }}># Install</div>
          <div>npm install @opentelemetry/sdk-node</div>
          <div style={{ color: '#10B981', marginBottom: 8, marginTop: 16 }}># Environment</div>
          <div>OTEL_EXPORTER_OTLP_ENDPOINT=https://...</div>
          <div>NEXT_PUBLIC_OTEL_SERVICE_NAME=agent-api</div>
        </div>
      </div>
    </div>
  );
}