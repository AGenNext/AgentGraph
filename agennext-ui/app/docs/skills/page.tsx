export default function SkillsDocsPage() {
  return (
    <main className="min-h-screen bg-white px-6 py-16 text-slate-950 sm:px-10 lg:px-16">
      <section className="mx-auto max-w-5xl">
        <a href="/docs" className="text-sm text-cyan-700">← Docs</a>
        <p className="mt-12 font-semibold text-cyan-700">Skills Documentation</p>
        <h1 className="mt-4 text-5xl font-black tracking-tight">Portable skills, prompts, workflows, and playbooks.</h1>

        <div className="mt-12 space-y-8 text-lg leading-8 text-slate-700">
          <p>AGenNext Skills package prompts, workflows, tools, playbooks, and operational knowledge into reusable runtime-portable units.</p>

          <p>Skills support versioning, signing, governance, auditability, approvals, and enterprise lifecycle management.</p>

          <div className="rounded-3xl bg-slate-100 p-8 font-mono text-sm leading-8">
            Skill → Version → Signature → Policy → Runtime
          </div>
        </div>
      </section>
    </main>
  )
}
