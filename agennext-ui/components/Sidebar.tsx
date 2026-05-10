'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navItems = [
  { href: '/', icon: '🏠', label: 'Dashboard' },
  { href: '/agents', icon: '🤖', label: 'Agent Builder' },
  { href: '/workspace', icon: '📁', label: 'Workspaces' },
  { href: '/lifecycle', icon: '🔄', label: 'Lifecycle' },
  { href: '/approvals', icon: '✅', label: 'Approvals' },
  { href: '/tasks', icon: '📋', label: 'Tasks' },
  { href: '/team', icon: '👥', label: 'Teams' },
  { href: '/rag', icon: '📚', label: 'Knowledge' },
  { href: '/search', icon: '🔍', label: 'Search' },
  { href: '/admin', icon: '⚙️', label: 'Admin' },
  { href: '/integrations', icon: '🔗', label: 'Integrations' },
  { href: '/automation', icon: '⚡', label: 'Automations' },
  { href: '/contracts', icon: '📜', label: 'Contracts' },
  { href: '/finance', icon: '💰', label: 'Finance' },
  { href: '/settings', icon: '🎛️', label: 'Settings' },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside style={{ 
      width: 240, 
      background: '#1A1A2E', 
      color: '#fff',
      display: 'flex', 
      flexDirection: 'column',
      height: '100vh',
      position: 'sticky',
      top: 0,
      overflow: 'auto',
    }}>
      {/* Logo */}
      <div style={{ padding: '20px 24px', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{ width: 36, height: 36, background: 'linear-gradient(135deg, #667EEA 0%, #764BA2 100%)', borderRadius: 10, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: 18 }}>
            A
          </div>
          <div>
            <div style={{ fontWeight: 600, fontSize: 15, letterSpacing: '-0.3px' }}>AGenNext</div>
            <div style={{ fontSize: 10, color: '#8B8BA7', letterSpacing: '0.5px', textTransform: 'uppercase' }}>Enterprise</div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav style={{ flex: 1, padding: '16px 12px', overflow: 'auto' }}>
        {navItems.map(item => {
          const isActive = pathname === item.href;
          return (
            <Link 
              key={item.href} 
              href={item.href}
              style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: 12,
                padding: '10px 12px', 
                borderRadius: 8,
                color: isActive ? '#fff' : '#A0A0B8',
                background: isActive ? 'rgba(102, 126, 234, 0.2)' : 'transparent',
                textDecoration: 'none',
                fontSize: 13,
                fontWeight: isActive ? 500 : 400,
                marginBottom: 2,
                transition: 'all 0.15s ease',
              }}
            >
              <span style={{ fontSize: 16 }}>{item.icon}</span>
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* User */}
      <div style={{ padding: '16px 24px', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{ width: 32, height: 32, borderRadius: '50%', background: '#667EEA', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 12, fontWeight: 500 }}>
            JD
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 13, fontWeight: 500 }}>John Doe</div>
            <div style={{ fontSize: 11, color: '#8B8BA7' }}>Admin</div>
          </div>
        </div>
      </div>
    </aside>
  );
}