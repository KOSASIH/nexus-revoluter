/**
 * Real client-side cryptography helpers (WebCrypto).
 * - secureHex: CSPRNG-backed identifiers instead of Math.random.
 * - encryptJson / decryptJson: AES-256-GCM with a PBKDF2-SHA256 derived key.
 */

const PBKDF2_ITERATIONS = 600_000; // OWASP 2023 guidance for PBKDF2-HMAC-SHA256
const SALT_BYTES = 16;
const IV_BYTES = 12;

export interface EncryptedEnvelope {
  schema: 'Sovereign-Pioneer-Vault-V2';
  encryption: 'AES-256-GCM';
  kdf: 'PBKDF2-SHA256';
  iterations: number;
  salt: string; // base64
  iv: string; // base64
  ciphertext: string; // base64
  exportedAt: string;
}

/** Cryptographically secure random hex string of `length` characters. */
export function secureHex(length: number): string {
  const bytes = new Uint8Array(Math.ceil(length / 2));
  crypto.getRandomValues(bytes);
  return Array.from(bytes, (b) => b.toString(16).padStart(2, '0'))
    .join('')
    .slice(0, length);
}

function toBase64(bytes: Uint8Array): string {
  let bin = '';
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin);
}

function fromBase64(b64: string): Uint8Array<ArrayBuffer> {
  const bin = atob(b64);
  const out = new Uint8Array(new ArrayBuffer(bin.length));
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

async function deriveKey(passphrase: string, salt: Uint8Array<ArrayBuffer>, iterations: number): Promise<CryptoKey> {
  const material = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(passphrase) as Uint8Array<ArrayBuffer>,
    'PBKDF2',
    false,
    ['deriveKey']
  );
  return crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt, iterations, hash: 'SHA-256' },
    material,
    { name: 'AES-GCM', length: 256 },
    false,
    ['encrypt', 'decrypt']
  );
}

export async function encryptJson(data: unknown, passphrase: string): Promise<EncryptedEnvelope> {
  if (passphrase.length < 8) throw new Error('Passphrase must be at least 8 characters.');
  const salt = crypto.getRandomValues(new Uint8Array(new ArrayBuffer(SALT_BYTES)));
  const iv = crypto.getRandomValues(new Uint8Array(new ArrayBuffer(IV_BYTES)));
  const key = await deriveKey(passphrase, salt, PBKDF2_ITERATIONS);
  const plaintext = new TextEncoder().encode(JSON.stringify(data)) as Uint8Array<ArrayBuffer>;
  const ciphertext = new Uint8Array(await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, plaintext));
  return {
    schema: 'Sovereign-Pioneer-Vault-V2',
    encryption: 'AES-256-GCM',
    kdf: 'PBKDF2-SHA256',
    iterations: PBKDF2_ITERATIONS,
    salt: toBase64(salt),
    iv: toBase64(iv),
    ciphertext: toBase64(ciphertext),
    exportedAt: new Date().toISOString(),
  };
}

export function isEncryptedEnvelope(value: unknown): value is EncryptedEnvelope {
  const v = value as Partial<EncryptedEnvelope> | null;
  return (
    !!v &&
    typeof v === 'object' &&
    v.schema === 'Sovereign-Pioneer-Vault-V2' &&
    v.encryption === 'AES-256-GCM' &&
    typeof v.salt === 'string' &&
    typeof v.iv === 'string' &&
    typeof v.ciphertext === 'string' &&
    typeof v.iterations === 'number'
  );
}

export async function decryptJson<T = unknown>(envelope: EncryptedEnvelope, passphrase: string): Promise<T> {
  // Cap iterations so a crafted file cannot freeze the tab.
  if (envelope.iterations < 100_000 || envelope.iterations > 5_000_000) {
    throw new Error('Unsupported key-derivation parameters in backup file.');
  }
  const key = await deriveKey(passphrase, fromBase64(envelope.salt), envelope.iterations);
  try {
    const plain = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv: fromBase64(envelope.iv) },
      key,
      fromBase64(envelope.ciphertext)
    );
    return JSON.parse(new TextDecoder().decode(plain)) as T;
  } catch {
    throw new Error('Wrong passphrase or corrupted backup file.');
  }
}
