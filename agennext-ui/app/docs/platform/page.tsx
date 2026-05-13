export default function PlatformDocsPage() {
  return (
    <main className="min-h-screen bg-white px-6 py-16 text-slate-950 sm:px-10 lg:px-16">
      <section className="mx-auto max-w-5xl">
        <a href="/docs" className="text-sm text-cyan-700">← Docs</a>
        <p className="mt-12 font-semibold text-cyan-700">Platform Documentation</p>
        <h1 className="mt-4 text-5xl font-black tracking-tight">Platform Architecture</h1>

        <div className="mt-12 space-y-10">
          <section>
            <h2 className="text-3xl font-black">Overview</h2>
            <p className="mt-4 text-lg leading-8 text-slate-700">AGenNext Platform is the user-facing control plane for enterprise AI agents. It owns SDK selection, model gateways, framework configuration, workflow orchestration, governance, evaluation, billing, tracing, and runtime handoff.</p>
          </section>

          <section>
            <h2 className="text-3xl font-black">Architecture</h2>
            <div className="mt-6 rounded-3xl bg-slate-100 p-8 font-mono text-sm leading-8">
              Platform → Runner → Kernel
            </div>
          </section>

          <section>
            <h2 className="text-3xl font-black">Core responsibilities</h2>
            <ul className="mt-6 list-disc space-y-3 pl-6 text-lg text-slate-700">
              <li>Framework and runtime configuration</li>
              <li>Policy and governance management</li>
              <li>Agent lifecycle management</li>
              <li>Model and provider abstraction</li>
              <li>Workflow orchestration</li>
              <li>Observability and auditability</li>
              <li>Enterprise controls and compliance</li>
            </ul>
          </section>
        </div>
      </section>
    </main>
  )
}
