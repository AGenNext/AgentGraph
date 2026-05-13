const protocols = [
  'A2A agent-to-agent runtime',
  'Registry-backed discovery',
  'Agent identity and authorization',
  'DID-ready governance layer',
];

const features = [
  {
    title: 'Protocol-native agents',
    description: 'Build agent systems around A2A, registry discovery, identity, authorization, and governance primitives.',
  },
  {
    title: 'Multi-agent orchestration',
    description: 'Coordinate specialized agents for research, writing, DevOps, sales, support, and enterprise workflows.',
  },
  {
    title: 'Enterprise control plane',
    description: 'Track tasks, approvals, memory, decisions, integrations, and runtime activity from one platform.',
  },
];

const stats = [
  { value: '13+', label: 'Protocol modules planned' },
  { value: 'A2A', label: 'Runtime implementation underway' },
  { value: 'OSS', label: 'Open protocol foundation' },
];

export default function LandingPage() {
  return (
    <main style={{ minHeight: '100vh', background: '#070B14', color: '#F8FAFC', fontFamily: 'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif' }}>
      <section style={{ position: 'relative', overflow: 'hidden', padding: '32px 24px 80px' }}>
        <div style={{ position: 'absolute', inset: 0, background: 'radial-gradient(circle at 20% 10%, rgba(59,130,246,0.28), transparent 34%), radial-gradient(circle at 80% 20%, rgba(168,85,247,0.22), transparent 30%), radial-gradient(circle at 50% 90%, rgba(16,185,129,0.12), transparent 32%)' }} />
        <div style={{ position: 'relative', maxWidth: 1180, margin: '0 auto' }}>
          <nav style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 96 }}>
            <a href="/" style={{ display: 'flex', alignItems: 'center', gap: 10, color: '#fff', textDecoration: 'none', fontWeight: 800, letterSpacing: -0.4 }}>
              <span style={{ width: 34, height: 34, borderRadius: 10, display: 'grid', placeItems: 'center', background: 'linear-gradient(135deg, #3B82F6, #8B5CF6)' }}>A</span>
              AGenNext AgentGraph
            </a>
            <div style={{ display: 'flex', gap: 16, alignItems: 'center', fontSize: 14 }}>
              <a href="https://github.com/AGenNext/AgentGraph" style={{ color: '#CBD5E1', textDecoration: 'none' }}>GitHub</a>
              <a href="https://github.com/AGenNext/AGenNext-Protocols" style={{ color: '#CBD5E1', textDecoration: 'none' }}>Protocols</a>
              <a href="#protocols" style={{ color: '#070B14', textDecoration: 'none', background: '#F8FAFC', padding: '10px 14px', borderRadius: 999, fontWeight: 700 }}>Explore</a>
            </div>
          </nav>

          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.1fr) minmax(320px, 0.9fr)', gap: 48, alignItems: 'center' }}>
            <div>
              <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, padding: '8px 12px', border: '1px solid rgba(148,163,184,0.28)', borderRadius: 999, background: 'rgba(15,23,42,0.65)', color: '#BFDBFE', fontSize: 13, marginBottom: 22 }}>
                Protocol runtime for enterprise AI agents
              </div>
              <h1 style={{ fontSize: 'clamp(42px, 7vw, 78px)', lineHeight: 0.95, letterSpacing: -3, margin: '0 0 24px', maxWidth: 780 }}>
                Build, govern, and connect agent networks.
              </h1>
              <p style={{ color: '#CBD5E1', fontSize: 20, lineHeight: 1.65, maxWidth: 690, margin: '0 0 34px' }}>
                AgentGraph is the AGenNext control plane for protocol-native multi-agent systems: A2A messaging, registry discovery, identity, authorization, and governance-ready orchestration.
              </p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 14 }}>
                <a href="https://github.com/AGenNext/AgentGraph" style={{ background: '#3B82F6', color: '#fff', padding: '14px 18px', borderRadius: 12, textDecoration: 'none', fontWeight: 800 }}>View repository</a>
                <a href="https://github.com/AGenNext/AGenNext-Protocols" style={{ background: 'rgba(255,255,255,0.08)', color: '#fff', padding: '14px 18px', borderRadius: 12, textDecoration: 'none', fontWeight: 800, border: '1px solid rgba(148,163,184,0.25)' }}>Protocol specs</a>
              </div>
            </div>

            <div style={{ border: '1px solid rgba(148,163,184,0.25)', borderRadius: 28, padding: 24, background: 'linear-gradient(180deg, rgba(15,23,42,0.9), rgba(15,23,42,0.56))', boxShadow: '0 28px 80px rgba(0,0,0,0.35)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 22 }}>
                <strong>Runtime snapshot</strong>
                <span style={{ color: '#34D399', fontSize: 13 }}>online</span>
              </div>
              <div style={{ display: 'grid', gap: 12 }}>
                {protocols.map((item, index) => (
                  <div key={item} style={{ display: 'flex', gap: 12, alignItems: 'center', padding: 14, borderRadius: 16, background: 'rgba(255,255,255,0.055)', border: '1px solid rgba(148,163,184,0.14)' }}>
                    <span style={{ width: 28, height: 28, borderRadius: 9, display: 'grid', placeItems: 'center', background: index === 0 ? '#2563EB' : 'rgba(148,163,184,0.18)', fontSize: 13 }}>{index + 1}</span>
                    <span style={{ color: '#E2E8F0' }}>{item}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="protocols" style={{ padding: '0 24px 72px' }}>
        <div style={{ maxWidth: 1180, margin: '0 auto' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 18 }}>
            {stats.map((stat) => (
              <div key={stat.label} style={{ padding: 24, borderRadius: 22, background: '#0F172A', border: '1px solid rgba(148,163,184,0.18)' }}>
                <div style={{ fontSize: 34, fontWeight: 900, marginBottom: 6 }}>{stat.value}</div>
                <div style={{ color: '#94A3B8', fontSize: 14 }}>{stat.label}</div>
              </div>
            ))}
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
            {features.map((feature) => (
              <article key={feature.title} style={{ padding: 26, borderRadius: 22, background: '#F8FAFC', color: '#0F172A' }}>
                <h2 style={{ margin: '0 0 10px', fontSize: 20 }}>{feature.title}</h2>
                <p style={{ margin: 0, color: '#475569', lineHeight: 1.65 }}>{feature.description}</p>
              </article>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
