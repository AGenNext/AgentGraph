const enterprise = [
  'Private cloud deployments',
  'Local and air-gapped AI',
  'Tenant-aware governance',
  'Enterprise audit and compliance',
  'Secure agent lifecycle management',
  'Cross-team orchestration',
  'Runtime observability',
  'Enterprise monetization and operations',
]

export default function EnterprisePage() {
  return (
    <main className="min-h-screen bg-white px-6 py-16 text-slate-950 sm:px-10 lg:px-16">
      <section className="mx-auto max-w-7xl">
        <a href="/" className="text-sm text-cyan-700">← AGenNext</a>
        <p className="mt-12 font-semibold text-cyan-700">Enterprise AI Cloud</p>
        <h1 className="mt-4 max-w-5xl text-5xl font-black tracking-tight sm:text-7xl">Enterprise-grade AI agents with governance, security, and operational control.</h1>
        <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-700">Run AI agents with policy enforcement, observability, auditability, runtime governance, lifecycle management, and cloud-native deployment flexibility.</p>

        <div className="mt-16 grid gap-5 md:grid-cols-2 lg:grid-cols-4">
          {enterprise.map((item) => (
            <div key={item} className="rounded-3xl bg-slate-100 p-6 font-semibold">
              {item}
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}
