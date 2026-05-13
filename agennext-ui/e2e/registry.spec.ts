import { test, expect } from '@playwright/test';

test('Agent List loads', async ({ page }) => {
  await page.goto('http://localhost:3000/registry');
  await expect(page.locator('h1')).toContainText('Agent Registry');
});

test('Create new agent form', async ({ page }) => {
  await page.goto('http://localhost:3000/registry/new');
  await expect(page.locator('h1')).toContainText('New Agent');
  await page.fill('input[placeholder="Agent name"]', 'Test Agent');
  await page.click('button:has-text("Save")');
});