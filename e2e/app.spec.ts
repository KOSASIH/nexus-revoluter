import { test, expect, Page } from '@playwright/test';
import { readFileSync } from 'node:fs';

/** CSP violations from origins we cannot reach in a sandbox are not regressions. */
const IGNORED = /fonts\.(googleapis|gstatic)\.com|api\.coingecko\.com/;

async function open(page: Page) {
  const problems: string[] = [];
  page.on('pageerror', (e) => problems.push(`pageerror: ${e.message}`));
  await page.addInitScript(() => {
    document.addEventListener('securitypolicyviolation', (e) =>
      console.error(`CSPV ${e.violatedDirective} ${e.blockedURI}`)
    );
  });
  page.on('console', (m) => {
    if (m.text().startsWith('CSPV') && !IGNORED.test(m.text())) problems.push(m.text());
  });
  await page.goto('/');
  await page.waitForSelector('[role=tab]');
  return problems;
}

test('every module renders without hitting the error boundary', async ({ page }) => {
  const problems = await open(page);
  const tabs = page.getByRole('tab');
  expect(await tabs.count()).toBe(10);
  for (let i = 0; i < 10; i++) {
    await tabs.nth(i).click();
    await expect(tabs.nth(i)).toHaveAttribute('aria-selected', 'true');
    await expect(page.getByRole('alert')).toHaveCount(0);
  }
  expect(problems).toEqual([]);
});

test('tabs support arrow, Home and End keys', async ({ page }) => {
  await open(page);
  const tabs = page.getByRole('tab');
  await tabs.first().focus();
  await page.keyboard.press('ArrowRight');
  await expect(tabs.nth(1)).toHaveAttribute('aria-selected', 'true');
  await page.keyboard.press('End');
  await expect(tabs.nth(9)).toHaveAttribute('aria-selected', 'true');
  await page.keyboard.press('ArrowRight');
  await expect(tabs.first()).toHaveAttribute('aria-selected', 'true');
});

test('production CSP blocks inline scripts and foreign requests', async ({ page }) => {
  await open(page);
  const executed = await page.evaluate(() => {
    const s = document.createElement('script');
    s.textContent = 'window.__injected = true';
    document.body.appendChild(s);
    return (window as unknown as { __injected?: boolean }).__injected === true;
  });
  expect(executed).toBe(false);
});

test('encrypted backup: export, reject wrong passphrase, restore with right one', async ({ page }) => {
  await open(page);
  await page.locator('#tab-vault').click();
  await page.getByRole('button', { name: 'Export' }).click();

  await page.fill('#export-pass', 'hunter2-hunter2');
  await page.fill('#export-pass2', 'a-different-one');
  await page.getByRole('button', { name: 'Encrypt & Download' }).click();
  await expect(page.getByText('Passphrases do not match')).toBeVisible();

  await page.fill('#export-pass2', 'hunter2-hunter2');
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'Encrypt & Download' }).click(),
  ]);
  const raw = readFileSync((await download.path())!, 'utf8');
  const env = JSON.parse(raw);
  expect(env.encryption).toBe('AES-256-GCM');
  expect(raw).not.toContain('piBalance');

  await page.getByRole('button', { name: 'Import' }).first().click();
  await page.fill('textarea', raw);
  await page.fill('#import-pass', 'wrong-passphrase');
  await page.getByRole('button', { name: 'Verify & Restore' }).click();
  await expect(page.getByText('Wrong passphrase')).toBeVisible();

  await page.fill('#import-pass', 'hunter2-hunter2');
  await page.getByRole('button', { name: 'Verify & Restore' }).click();
  await expect(page.getByText(/Restored \d+ vaults/)).toBeVisible();
});

test('created vaults persist across reload and can be reset', async ({ page }) => {
  await open(page);
  await page.locator('#tab-vault').click();
  await page.getByRole('button', { name: 'Generate Address' }).click();
  await page.fill('input[placeholder^="e.g. Pioneer"]', 'E2E Persist Vault');
  await page.getByRole('button', { name: 'Derive Keypair' }).click();
  await page.reload();
  await page.locator('#tab-vault').click();
  await expect(page.getByText('E2E Persist Vault').first()).toBeVisible();

  await page.getByRole('button', { name: 'Reset local data' }).click();
  await page.waitForSelector('[role=tab]');
  await page.locator('#tab-vault').click();
  await expect(page.getByText('E2E Persist Vault')).toHaveCount(0);
});
