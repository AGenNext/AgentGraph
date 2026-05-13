export default function SecurityDocsPage() {
  return (
    <main className="min-h-screen bg-slate-950 px-6 py-16 text-white sm:px-10 lg:px-16">
      <section className="mx-auto max-w-5xl">
        <a href="/docs" className="text-sm text-cyan-300">← Docs</a>
        <p className="mt-12 font-semibold text-cyan-300">Security and Governance</p>
        <h1 className="mt-4 text-5xl font-black tracking-tight">Governable enterprise AI infrastructure.</h1>

        <div className="mt-12 grid gap-6 md:grid-cols-2">
          {[
            'Agent identity',
            'Lifecycle management',
            'OPA and policy enforcement',
            'OpenFGA and Zanzibar-style authorization',
            'Immutable audit logs',
            'Cryptographic signing',
            'Air-gapped deployment support',
            'Compliance and audit workflows',
          ].map((item) => (
            <div key={item} className="rounded-3xl border border-white/10 bg-white/[.04] p-6">
              {item}
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}
