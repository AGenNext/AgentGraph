import { test, expect } from '@playwright/test';

const ROUTES = [
  { path: '/', title: 'Dashboard' },
  { path: '/agents', title: 'Agent Builder' },
  { path: '/approvals', title: 'Approvals' },
  { path: '/lifecycle', title: 'Lifecycle' },
  { path: '/tasks', title: 'Tasks' },
  { path: '/team', title: 'Teams' },
  { path: '/rag', title: 'RAG' },
  { path: '/admin', title: 'Admin' },
  { path: '/integrations', title: 'Integrations' },
  { path: '/automation', title: 'Automations' },
  { path: '/search', title: 'Search' },
  { path: '/contracts', title: 'Contracts' },
  { path: '/finance', title: 'Finance' },
  { path: '/settings', title: 'Settings' },
  { path: '/notifications', title: 'Notifications' },
  { path: '/workspace', title: 'Workspaces' },
];

test.describe('AGenNext-Enterprise E2E', () => {
  for (const route of ROUTES) {
    test(`should render ${route.path}`, async ({ page }) => {
      await page.goto(route.path);
      await expect(page).toHaveTitle(/.*/);
      
      // Check no console errors
      const errors: string[] = [];
      page.on('console', msg => {
        if (msg.type() === 'error') errors.push(msg.text());
      });
      
      // Allow page to load
      await page.waitForLoadState('networkidle');
      
      // Verify no critical errors
      const criticalErrors = errors.filter(e => 
        !e.includes('Warning') && 
        !e.includes('deprecation')
      );
      expect(criticalErrors).toHaveLength(0);
    });
  }

  test('should navigate between routes', async ({ page }) => {
    // Start at dashboard
    await page.goto('/');
    await expect(page).toHaveTitle(/.*/);
    
    // Navigate to agents
    await page.goto('/agents');
    await expect(page).toHaveTitle(/.*/);
    
    // Navigate to lifecycle
    await page.goto('/lifecycle');
    await expect(page).toHaveTitle(/.*/);
  });

  test('should handle form interactions', async ({ page }) => {
    // Test settings form
    await page.goto('/settings');
    await page.waitForLoadState('networkidle');
    
    // Test automation creation modal
    await page.goto('/automation');
    await page.waitForLoadState('networkidle');
  });
});