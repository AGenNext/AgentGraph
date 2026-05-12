'use client';

import { usePathname } from 'next/navigation';

interface HeaderProps {
  actions?: React.ReactNode;
}

const routeTitles: Record<string, string> = {
  '/': 'Dashboard',
  '/agents': 'Agent Builder',
  '/workspace': 'Workspaces',
  '/lifecycle': 'Lifecycle',
  '/approvals': 'Approvals',
  '/tasks': 'Tasks',
  '/team': 'Teams',
  '/rag': 'Knowledge Base',
  '/admin': 'Admin',
  '/integrations': 'Integrations',
  '/automation': 'Automations',
  '/search': 'Search',
  '/contracts': 'Contracts',
  '/finance': 'Finance',
  '/settings': 'Settings',
  '/notifications': 'Notifications',
};

export function Header({ actions }: HeaderProps) {
  const pathname = usePathname();
  const title = routeTitles[pathname] || 'AGenNext';

  return (
    <header style={{ 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'space-between',
      padding: '16px 24px',
      background: '#fff',
      borderBottom: '1px solid #E5E5E5',
      height: 64,
    }}>
      {/* Breadcrumb */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <span style={{ fontSize: 13, color: '#8C8C8C' }}>AGenNext</span>
        <span style={{ color: '#C5C5C5' }}>/</span>
        <span style={{ fontSize: 15, fontWeight: 600, color: '#161616' }}>{title}</span>
      </div>

      {/* Actions */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <button style={{ 
          background: 'transparent', 
          border: '1px solid #E5E5E5', 
          borderRadius: 6, 
          padding: '8px 12px',
          fontSize: 13,
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: 6,
        }}>
          <span>🔔</span>
          <span style={{ width: 8, height: 8, background: '#DA1E28', borderRadius: '50%', position: 'absolute', top: 8, right: 8 }} />
        </button>
        <button style={{ 
          background: 'transparent', 
          border: '1px solid #E5E5E5', 
          borderRadius: 6, 
          padding: '8px 12px',
          fontSize: 13,
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: 6,
        }}>
          <span>❓</span>
          Help
        </button>
        {actions}
      </div>
    </header>
  );
}