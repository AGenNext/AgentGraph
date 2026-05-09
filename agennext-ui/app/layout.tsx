// app/layout.tsx
// Root layout - provides metadata and base HTML structure

import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AGenNext - AI Agent Platform",
  description: "Intelligent AI agent orchestration and management platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "'DM Sans', -apple-system, sans-serif" }}>
        {children}
      </body>
    </html>
  );
}