// app/layout.tsx
// Root layout - Friendly AI Agent Platform

import './globals.css';
import type { Metadata } from "next";
import { Sidebar } from '@/components/Sidebar';

export const metadata: Metadata = {
  title: "AGenNext - AI Agent Platform",
  description: "Multi-agent orchestration and management platform",
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
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body style={{ 
        margin: 0, 
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", 
        display: 'flex', 
        minHeight: '100vh', 
        background: 'linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%)',
        color: '#1a1a2e'
      }}>
        <Sidebar />
        <main style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          {children}
        </main>
      </body>
    </html>
  );
}