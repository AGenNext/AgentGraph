const pillars = ['Visual agent workflow builder', 'SDK and model gateway configuration', 'Framework and runtime bridge selection', 'Tenant-aware governance and policy', 'Execution status, traces, usage, and billing', 'Runner and Kernel handoff']

export default function PlatformPage() {
  return (
    <main className="min-h-screen bg-slate-950 px-6 py-16 text-white sm:px-10 lg:px-16">
      <section className="mx-auto max-w-7xl">
        <a href="/" className="text-sm text-cyan-300">← AGenNext</a>
        <p className="mt-12 font-semibold text-cyan-300">AGenNext Platform</p>
        <h1 className="mt-4 max-w-5xl text-5xl font-black tracking-tight sm:text-7xl">The control plane for production AI agent products.</h1>
        <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-300">Design, configure, evaluate, monitor, govern, and monetize agents from one cloud-native surface. Platform owns user-facing configuration for SDKs, models, frameworks, policies, workflows, observability, and enterprise controls.</p>
        <div className="mt-10 flex flex-col gap-4 sm:flex-row">
          <a href="https://github.com/AGenNext/Platform" className="rounded-full bg-white px-6 py-3 text-center font-semibold text-slate-950">GitHub repo</a>
          <a href="/docs/platform" className="rounded-full border border-white/20 px-6 py-3 text-center font-semibold">Read docs</a>
        </div>
        <div className="mt-16 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {pillars.map((item) => <div key={item} className="rounded-3xl border border-white/10 bg-white/[.04] p-6 text-slate-200">{item}</div>)}
        </div>
      </section>
    </main>
  )
}
