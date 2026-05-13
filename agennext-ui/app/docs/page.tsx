const docs = [
  ['Platform Docs', '/docs/platform', 'Architecture, configuration, governance, and deployment documentation.'],
  ['Protocols Docs', '/docs/protocols', 'Protocol interoperability, identity, authorization, and discovery documentation.'],
  ['Security Docs', '/docs/security', 'Governance, audit, policy, compliance, and secure runtime documentation.'],
  ['Runtime Docs', '/docs/runtime', 'Runner, Kernel, orchestration, memory, state, and runtime lifecycle documentation.'],
]

export default function DocsPage() {
  return (
    <main className="min-h-screen bg-slate-950 px-6 py-16 text-white sm:px-10 lg:px-16">
      <section className="mx-auto max-w-7xl">
        <a href="/" className="text-sm text-cyan-300">← AGenNext</a>
        <p className="mt-12 font-semibold text-cyan-300">Documentation</p>
        <h1 className="mt-4 text-5xl font-black tracking-tight sm:text-7xl">AGenNext Docs</h1>
        <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-300">Technical documentation for the AGenNext ecosystem including Platform, Protocols, Runtime, Governance, Security, Agent Lifecycle, and Enterprise AI operations.</p>
        <div className="mt-16 grid gap-6 md:grid-cols-2">
          {docs.map(([title, href, description]) => (
            <a key={title} href={href} className="rounded-3xl border border-white/10 bg-white/[.04] p-7 transition hover:bg-white/[.08]">
              <h2 className="text-2xl font-bold">{title}</h2>
              <p className="mt-4 text-slate-300">{description}</p>
            </a>
          ))}
        </div>
      </section>
    </main>
  )
}
