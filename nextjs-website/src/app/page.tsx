import Link from "next/link"

export default function Home() {
  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="min-h-[80vh] flex items-center justify-center py-20">
        <div className="container px-4 text-center">
          <div className="inline-flex items-center gap-2 border border-border rounded-full px-4 py-2 text-sm text-muted-foreground mb-8">
            <span className="w-2 h-2 bg-primary rounded-full"></span>
            <span>Now with WaltID Integration</span>
          </div>
          
          <h1 className="text-h1 mb-6 max-w-3xl mx-auto">
            Build AI Agents with<br />
            <span className="text-primary">Enterprise</span> Security
          </h1>
          
          <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto">
            Comprehensive agent platform using Schema.org framework with canonical_id, 
            version control, immutable audit logs, and cryptographic signatures.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link 
              href="/contact" 
              className="bg-primary text-primary-foreground px-8 py-3 text-base font-medium rounded-md hover:bg-primary/90 transition-colors inline-flex items-center gap-2"
            >
              Start Building Free
              <span>→</span>
            </Link>
            <Link 
              href="/docs" 
              className="border border-border px-8 py-3 text-base font-medium rounded-md hover:bg-accent transition-colors inline-flex items-center gap-2"
            >
              Read Documentation
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 border-t border-border">
        <div className="container px-4">
          <h2 className="text-h2 text-center mb-16">Enterprise Features</h2>
          
          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {/* Feature 1 */}
            <div className="border border-border rounded-lg p-6 hover:bg-accent/50 transition-colors">
              <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">22 Domain Databases</h3>
              <p className="text-muted-foreground text-sm">
                Pre-built databases for automotive, banking, healthcare, retail, and more.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="border border-border rounded-lg p-6 hover:bg-accent/50 transition-colors">
              <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">Entity Security</h3>
              <p className="text-muted-foreground text-sm">
                canonical_id, version, audit_log, and crypto_signature on every entity.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="border border-border rounded-lg p-6 hover:bg-accent/50 transition-colors">
              <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">Verified Credentials</h3>
              <p className="text-muted-foreground text-sm">
                WaltID integration for issuing and verifying agent credentials.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="border border-border rounded-lg p-6 hover:bg-accent/50 transition-colors">
              <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">Policy Engine</h3>
              <p className="text-muted-foreground text-sm">
                Open Policy Agent (OPA) for fine-grained access control.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="border border-border rounded-lg p-6 hover:bg-accent/50 transition-colors">
              <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">Graph Database</h3>
              <p className="text-muted-foreground text-sm">
                SurrealDB knowledge graphs with React xyflow visualization.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="border border-border rounded-lg p-6 hover:bg-accent/50 transition-colors">
              <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-3.582 8-8 8s-8-3.582-8-8 3.582-8 8-8 8 3.582 8 8z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">A2A Protocol</h3>
              <p className="text-muted-foreground text-sm">
                Agent-to-agent communication and task delegation.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 border-t border-border">
        <div className="container px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-h2">22+</div>
              <div className="text-muted-foreground mt-2">Domain Databases</div>
            </div>
            <div>
              <div className="text-h2">100+</div>
              <div className="text-muted-foreground mt-2">Schema.org Types</div>
            </div>
            <div>
              <div className="text-h2">11</div>
              <div className="text-muted-foreground mt-2">Core Types</div>
            </div>
            <div>
              <div className="text-h2">∞</div>
              <div className="text-muted-foreground mt-2">Agent Possibilities</div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 border-t border-border">
        <div className="container px-4">
          <h2 className="text-h2 text-center mb-16">How It Works</h2>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="w-12 h-12 border border-border rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">1</div>
              <h3 className="text-lg font-semibold mb-2">Define Agent</h3>
              <p className="text-sm text-muted-foreground">
                Create agents as Schema.org SoftwareApplication with Person owner.
              </p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 border border-border rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">2</div>
              <h3 className="text-lg font-semibold mb-2">Add Credentials</h3>
              <p className="text-sm text-muted-foreground">
                Issue verified credentials via WaltID.
              </p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 border border-border rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">3</div>
              <h3 className="text-lg font-semibold mb-2">Deploy</h3>
              <p className="text-sm text-muted-foreground">
                Run with OPA policies and A2A protocol.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Code Example */}
      <section className="py-20 border-t border-border">
        <div className="container px-4">
          <h2 className="text-h2 text-center mb-8">Simple to Use</h2>
          <p className="text-center text-muted-foreground mb-12">Python SDK for building enterprise agents</p>
          
          <div className="max-w-2xl mx-auto bg-card border border-border rounded-lg p-6">
            <pre className="font-mono text-sm overflow-x-auto text-left">
              <code className="text-muted-foreground">from base_entity import Entity
from waltid_endpoints import WaltIDClient

agent = Entity()
client = WaltIDClient()
credential = client.issue_agent_credential(
    issuer_did="did:waltid:agennext",
    subject_did="did:waltid:agent:" + agent.canonical_id,
    skills=["coding", "data-analysis"]
)
result = client.verify_credential(credential)</code>
            </pre>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-20 border-t border-border">
        <div className="container px-4">
          <h2 className="text-h2 text-center mb-16">Simple Pricing</h2>
          
          <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {/* Free */}
            <div className="border border-border rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-2">Developer</h3>
              <div className="text-h2 mb-4">$0<span className="text-sm text-muted-foreground">/mo</span></div>
              <ul className="space-y-2 text-sm text-muted-foreground mb-6">
                <li>• 1 Agent</li>
                <li>• 1,000 messages/mo</li>
                <li>• Community Support</li>
              </ul>
              <Link href="/contact" className="block text-center border border-border py-2 rounded-md font-medium hover:bg-accent transition-colors">
                Get Started
              </Link>
            </div>

            {/* Pro */}
            <div className="border border-border rounded-lg p-6 relative">
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-3 py-1 text-xs font-medium rounded">
                Popular
              </div>
              <h3 className="text-lg font-semibold mb-2">Team</h3>
              <div className="text-h2 mb-4">$99<span className="text-sm text-muted-foreground">/mo</span></div>
              <ul className="space-y-2 text-sm text-muted-foreground mb-6">
                <li>• 10 Agents</li>
                <li>• 100,000 messages/mo</li>
                <li>• Priority Support</li>
              </ul>
              <Link href="/contact" className="block text-center bg-primary text-primary-foreground py-2 rounded-md font-medium hover:bg-primary/90 transition-colors">
                Start Trial
              </Link>
            </div>

            {/* Enterprise */}
            <div className="border border-border rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-2">Enterprise</h3>
              <div className="text-h2 mb-4">Custom</div>
              <ul className="space-y-2 text-sm text-muted-foreground mb-6">
                <li>• Unlimited Agents</li>
                <li>• Unlimited Messages</li>
                <li>• Dedicated Support</li>
              </ul>
              <Link href="/contact" className="block text-center border border-border py-2 rounded-md font-medium hover:bg-accent transition-colors">
                Contact Sales
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 border-t border-border">
        <div className="container px-4 text-center">
          <h2 className="text-h2 mb-4">Ready to Build Enterprise Agents?</h2>
          <p className="text-muted-foreground mb-8">Start building today with Schema.org and verified credentials.</p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link 
              href="https://github.com/AGenNext" 
              target="_blank"
              className="bg-primary text-primary-foreground px-8 py-3 font-medium rounded-md hover:bg-primary/90 transition-colors inline-flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.17 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.604-3.369-1.341-3.369-1.341-.454-1.155-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.113-4.555-4.951 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A11.764 11.764 0 0112 2c5.523 0 10 4.477 10 10 0 4.477-2.018 8.345-4.767 9.676-.426.093-.866.139-1.327.139-.462 0-.912-.042-1.335-.125 1.04-1.232 1.875-1.732 2.145-2.065.546-.856.365-1.627.168-1.966z" />
              </svg>
              Star on GitHub
            </Link>
            <Link href="/docs" className="border border-border px-8 py-3 font-medium rounded-md hover:bg-accent transition-colors inline-flex items-center gap-2">
              Read the Docs <span>→</span>
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}