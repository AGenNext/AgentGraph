import { test, expect } from '@playwright/test';

test('registry list loads', async ({ page }) => {
  await page.goto('http://localhost:3000/registry');
  await expect(page.locator('h1')).toContainText('Agent Registry');
});

test('new agent page loads', async ({ page }) => {
  await page.goto('http://localhost:3000/registry/new');
  await expect(page.locator('h1')).toContainText('New Agent');
});
