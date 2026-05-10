// app/layout.tsx
// Root layout - Enterprise Grade AI Agent Platform

import './globals.css';
import type { Metadata } from "next";
import { Sidebar } from '@/components/Sidebar';

export const metadata: Metadata = {
  title: "AGenNext Enterprise - AI Agent Platform",
  description: "Enterprise-grade multi-agent orchestration and management platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body style={{ margin: 0, fontFamily: "'IBM Plex Sans', -apple-system, sans-serif", display: 'flex', minHeight: '100vh', background: '#F8F9FA' }}>
        <Sidebar />
        <main style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          {children}
        </main>
      </body>
    </html>
  );
}