import type { Metadata } from "next"
import Link from "next/link"
import "./globals.css"

export const metadata: Metadata = {
  title: "AGenNext Enterprise | AI Agent Platform",
  description: "Enterprise AI agent platform built on Schema.org framework with verified credentials and entity security.",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-background font-sans antialiased">
        <header className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="container flex h-16 items-center justify-between px-4">
            <Link href="/" className="flex items-center gap-2 font-semibold">
              <span className="text-xl">AGenNext</span>
            </Link>
            <nav className="hidden md:flex gap-6 text-sm">
              <Link href="/docs" className="text-muted-foreground hover:text-foreground transition-colors">
                Docs
              </Link>
              <Link href="/api" className="text-muted-foreground hover:text-foreground transition-colors">
                API
              </Link>
              <Link href="/pricing" className="text-muted-foreground hover:text-foreground transition-colors">
                Pricing
              </Link>
              <Link href="/about" className="text-muted-foreground hover:text-foreground transition-colors">
                About
              </Link>
            </nav>
            <div className="flex items-center gap-4">
              <Link 
                href="https://github.com/AGenNext" 
                target="_blank"
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                GitHub
              </Link>
              <Link 
                href="/contact" 
                className="bg-primary text-primary-foreground px-4 py-2 text-sm font-medium rounded-md hover:bg-primary/90 transition-colors"
              >
                Get Started
              </Link>
            </div>
          </div>
        </header>
        <main className="flex-1">
          {children}
        </main>
        <footer className="border-t border-border py-8">
          <div className="container flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
            <p>© 2024 AGenNext. All rights reserved.</p>
            <div className="flex gap-6">
              <Link href="/privacy" className="hover:text-foreground transition-colors">Privacy</Link>
              <Link href="/terms" className="hover:text-foreground transition-colors">Terms</Link>
              <Link href="/contact" className="hover:text-foreground transition-colors">Contact</Link>
            </div>
          </div>
        </footer>
      </body>
    </html>
  )
}