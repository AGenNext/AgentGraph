const researchAreas = [
  'Kernel-level orchestration research',
  'Unified runtime for agents and code',
  'Multimodal execution systems',
  'Schema-driven runtime architecture',
  'Time-space database concepts',
  'SurrealDB runtime experiments',
  'Persistent autonomous memory systems',
  'Context-native runtime coordination',
]

export default function ResearchPage() {
  return (
    <main className="min-h-screen bg-slate-950 px-6 py-16 text-white sm:px-10 lg:px-16">
      <section className="mx-auto max-w-7xl">
        <a href="/" className="text-sm text-cyan-300">← AGenNext</a>
        <p className="mt-12 font-semibold text-cyan-300">Research</p>
        <h1 className="mt-4 max-w-5xl text-5xl font-black tracking-tight sm:text-7xl">Experimental runtime systems for autonomous AI infrastructure.</h1>
        <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-300">AGenNext research explores foundational runtime systems where agents, memory, multimodal data, code, policy, orchestration, and execution operate together at a kernel-inspired layer.</p>

        <div className="mt-16 grid gap-5 md:grid-cols-2 lg:grid-cols-4">
          {researchAreas.map((item) => (
            <div key={item} className="rounded-3xl border border-white/10 bg-white/[.04] p-6 text-slate-200">
              {item}
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}
