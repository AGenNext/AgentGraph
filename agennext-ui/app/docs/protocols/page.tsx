export default function ProtocolDocsPage() {
  return (
    <main className="min-h-screen bg-white px-6 py-16 text-slate-950 sm:px-10 lg:px-16">
      <section className="mx-auto max-w-5xl">
        <a href="/docs" className="text-sm text-cyan-700">← Docs</a>
        <p className="mt-12 font-semibold text-cyan-700">Protocols Documentation</p>
        <h1 className="mt-4 text-5xl font-black tracking-tight">Protocol interoperability for enterprise AI agents.</h1>
        <p className="mt-6 text-lg leading-8 text-slate-700">AGenNext protocols provide a shared language for tool use, agent-to-agent communication, identity, discovery, authorization, commerce, UI streaming, and governed runtime integration.</p>

        <div className="mt-12 grid gap-6 md:grid-cols-2">
          {[
            ['MCP', 'Tool and data connectivity'],
            ['A2A', 'Agent-to-agent communication'],
            ['ACP', 'Agent commerce and payments'],
            ['AuthZen', 'Authorization interoperability'],
            ['Agent ID', 'Identity and authentication'],
            ['Registry', 'Agent discovery and federation'],
          ].map(([title, description]) => (
            <div key={title} className="rounded-3xl bg-slate-100 p-7">
              <h2 className="text-2xl font-black">{title}</h2>
              <p className="mt-4 text-slate-700">{description}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}
