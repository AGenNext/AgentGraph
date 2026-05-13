export default function ResearchDocsPage() {
  return (
    <main className="min-h-screen bg-white px-6 py-16 text-slate-950 sm:px-10 lg:px-16">
      <section className="mx-auto max-w-5xl">
        <a href="/docs" className="text-sm text-cyan-700">← Docs</a>
        <p className="mt-12 font-semibold text-cyan-700">Research Documentation</p>
        <h1 className="mt-4 text-5xl font-black tracking-tight">Experimental runtime and kernel research.</h1>

        <div className="mt-12 space-y-8 text-lg leading-8 text-slate-700">
          <p>AGenNext research investigates a unified runtime where agents, multimodal context, memory, orchestration, and execution are coordinated together through kernel-inspired infrastructure.</p>

          <p>The current research track explores schema-driven runtime systems, combined data/runtime execution, persistent memory models, autonomous orchestration, and experimental database/runtime integration concepts.</p>

          <div className="rounded-3xl bg-slate-100 p-8 font-mono text-sm leading-8">
            Agent + Context + Policy + Runtime + Memory + Execution
          </div>
        </div>
      </section>
    </main>
  )
}
