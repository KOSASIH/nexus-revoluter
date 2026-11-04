/// <reference types="vitest/config" />
import { readFileSync } from 'node:fs';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

// Serve the exact production security headers (vercel.json) from `vite preview`,
// so local runs and e2e tests exercise the same CSP that ships.
function productionHeaders(): Record<string, string> {
  try {
    const cfg = JSON.parse(readFileSync(new URL('./vercel.json', import.meta.url), 'utf8'));
    const all = cfg.headers.find((h: { source: string }) => h.source === '/(.*)');
    return Object.fromEntries(all.headers.map((h: { key: string; value: string }) => [h.key, h.value]));
  } catch {
    return {};
  }
}

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: '0.0.0.0',
    port: 3000,
  },
  preview: {
    headers: productionHeaders(),
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          react: ['react', 'react-dom'],
          icons: ['lucide-react'],
        },
      },
    },
  },
  test: {
    include: ['src/**/*.test.ts'],
  },
});
