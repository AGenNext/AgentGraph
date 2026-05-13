export default function RuntimeDocsPage() {
  return (
    <main className="min-h-screen bg-white px-6 py-16 text-slate-950 sm:px-10 lg:px-16">
      <section className="mx-auto max-w-5xl">
        <a href="/docs" className="text-sm text-cyan-700">← Docs</a>
        <p className="mt-12 font-semibold text-cyan-700">Runtime Documentation</p>
        <h1 className="mt-4 text-5xl font-black tracking-tight">Framework-agnostic orchestration runtime.</h1>

        <div className="mt-12 space-y-8 text-lg leading-8 text-slate-700">
          <p>AGenNext Runtime is responsible for loading framework bridges, managing orchestration state, coordinating execution, handling memory and context, and connecting workloads to the Kernel layer.</p>

          <p>Supported runtime concepts include LangGraph, CrewAI, AutoGen, LangChain, OpenHands, Mastra, custom runtimes, multimodal execution, persistent memory, branching workflows, HITL loops, and self-improving agents.</p>

          <div className="rounded-3xl bg-slate-100 p-8 font-mono text-sm leading-8">
            Agent + Data + Code + Multimodal Context + Runtime State
          </div>
        </div>
      </section>
    </main>
  )
}
