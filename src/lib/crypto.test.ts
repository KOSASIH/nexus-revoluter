import { describe, it, expect } from 'vitest';
import { secureHex, encryptJson, decryptJson, isEncryptedEnvelope } from './crypto';

describe('secureHex', () => {
  it('returns hex of the requested length, including odd lengths', () => {
    for (const n of [1, 5, 8, 16, 40]) {
      const h = secureHex(n);
      expect(h).toHaveLength(n);
      expect(h).toMatch(/^[0-9a-f]+$/);
    }
  });
  it('does not repeat across calls', () => {
    expect(new Set(Array.from({ length: 200 }, () => secureHex(16))).size).toBe(200);
  });
});

describe('encryptJson / decryptJson', () => {
  const payload = { vaults: [{ address: 'GABC', piBalance: 12.5 }] };

  it('round-trips with the right passphrase', async () => {
    const env = await encryptJson(payload, 'correct horse battery');
    expect(isEncryptedEnvelope(env)).toBe(true);
    expect(await decryptJson(env, 'correct horse battery')).toEqual(payload);
  });

  it('does not leak plaintext into the envelope', async () => {
    const env = await encryptJson(payload, 'correct horse battery');
    expect(JSON.stringify(env)).not.toContain('GABC');
  });

  it('rejects a wrong passphrase', async () => {
    const env = await encryptJson(payload, 'correct horse battery');
    await expect(decryptJson(env, 'wrong passphrase!!')).rejects.toThrow(/Wrong passphrase/);
  });

  it('rejects tampered ciphertext (GCM authentication)', async () => {
    const env = await encryptJson(payload, 'correct horse battery');
    const bytes = atob(env.ciphertext).split('');
    bytes[0] = String.fromCharCode(bytes[0].charCodeAt(0) ^ 1);
    await expect(decryptJson({ ...env, ciphertext: btoa(bytes.join('')) }, 'correct horse battery')).rejects.toThrow();
  });

  it('refuses short passphrases and absurd KDF parameters', async () => {
    await expect(encryptJson(payload, 'short')).rejects.toThrow(/8 characters/);
    const env = await encryptJson(payload, 'correct horse battery');
    await expect(decryptJson({ ...env, iterations: 1 }, 'correct horse battery')).rejects.toThrow(/Unsupported/);
  });

  it('uses a fresh salt and IV each time', async () => {
    const a = await encryptJson(payload, 'correct horse battery');
    const b = await encryptJson(payload, 'correct horse battery');
    expect(a.salt).not.toBe(b.salt);
    expect(a.iv).not.toBe(b.iv);
  });
});
