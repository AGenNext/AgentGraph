const runtimeFeatures = [
  'Framework-agnostic orchestration',
  'Persistent state and memory',
  'Multimodal execution runtime',
  'Branching workflows and HITL loops',
  'Self-improving agents',
  'Runtime bridge loading',
  'Context-aware decision systems',
  'Agent lifecycle persistence',
  'Kernel-level orchestration research',
]

export default function RuntimePage() {
  return (
    <main className="min-h-screen bg-white px-6 py-16 text-slate-950 sm:px-10 lg:px-16">
      <section className="mx-auto max-w-7xl">
        <a href="/" className="text-sm text-cyan-700">← AGenNext</a>
        <p className="mt-12 font-semibold text-cyan-700">Runtime + Kernel</p>
        <h1 className="mt-4 max-w-5xl text-5xl font-black tracking-tight sm:text-7xl">A unified runtime for agents, data, memory, tools, and code.</h1>
        <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-700">AGenNext Runtime coordinates orchestration, memory, multimodal context, policy, and execution across frameworks, runtimes, clouds, and deployment environments.</p>

        <div className="mt-16 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {runtimeFeatures.map((feature) => (
            <div key={feature} className="rounded-3xl bg-slate-100 p-6">
              {feature}
            </div>
          ))}
        </div>

        <div className="mt-12 flex gap-4">
          <a href="/docs/runtime" className="rounded-full bg-slate-950 px-6 py-3 font-semibold text-white">Runtime docs</a>
        </div>
      </section>
    </main>
  )
}
