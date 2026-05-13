const capabilities = [
  'Multimodal RAG',
  'Speech to text',
  'Text to speech',
  'Text to image',
  'OCR and PDF workflows',
  'File conversion pipelines',
  'Notebook environments',
  'Data labeling and AI datasets',
]

export default function MultimodalPage() {
  return (
    <main className="min-h-screen bg-slate-950 px-6 py-16 text-white sm:px-10 lg:px-16">
      <section className="mx-auto max-w-7xl">
        <a href="/" className="text-sm text-cyan-300">← AGenNext</a>
        <p className="mt-12 font-semibold text-cyan-300">Multimodal AI</p>
        <h1 className="mt-4 max-w-5xl text-5xl font-black tracking-tight sm:text-7xl">One platform for text, speech, images, documents, and multimodal context.</h1>
        <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-300">AGenNext combines multimodal RAG, OCR, notebook workflows, dataset operations, audio pipelines, document tooling, and retrieval systems into a unified runtime for AI agents.</p>

        <div className="mt-16 grid gap-5 md:grid-cols-2 lg:grid-cols-4">
          {capabilities.map((item) => (
            <div key={item} className="rounded-3xl border border-white/10 bg-white/[.04] p-6 text-slate-200">
              {item}
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}
