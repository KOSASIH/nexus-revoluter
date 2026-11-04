import { useEffect, useRef, useState } from 'react';

/** Bump when the shape of persisted data changes; older payloads are discarded. */
const SCHEMA_VERSION = 1;
const PREFIX = 'nexus-revoluter:v' + SCHEMA_VERSION + ':';

export interface StorageLike {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
  removeItem(key: string): void;
}

function safeStorage(): StorageLike | null {
  try {
    return typeof localStorage === 'undefined' ? null : localStorage;
  } catch {
    return null; // blocked (private mode / disabled cookies)
  }
}

/** Reads and validates a persisted value; returns `fallback` on any problem. */
export function loadPersisted<T>(
  key: string,
  fallback: T,
  validate: (v: unknown) => v is T,
  storage: StorageLike | null = safeStorage()
): T {
  if (!storage) return fallback;
  try {
    const raw = storage.getItem(PREFIX + key);
    if (raw === null) return fallback;
    const parsed: unknown = JSON.parse(raw);
    return validate(parsed) ? parsed : fallback;
  } catch {
    return fallback;
  }
}

export function savePersisted(key: string, value: unknown, storage: StorageLike | null = safeStorage()): void {
  if (!storage) return;
  try {
    storage.setItem(PREFIX + key, JSON.stringify(value));
  } catch {
    // quota exceeded or storage blocked: persistence is best-effort
  }
}

export function clearAllPersisted(storage: StorageLike | null = safeStorage()): void {
  if (!storage) return;
  try {
    const s = storage as unknown as Storage;
    const keys: string[] = [];
    for (let i = 0; i < (s.length ?? 0); i++) {
      const k = s.key(i);
      if (k && k.startsWith('nexus-revoluter:')) keys.push(k);
    }
    keys.forEach((k) => storage.removeItem(k));
  } catch {
    // ignore
  }
}

/** Validator for "array of objects that each have the given string fields". */
export function isRecordArray<T>(requiredStringKeys: string[]) {
  return (v: unknown): v is T[] =>
    Array.isArray(v) &&
    v.every(
      (item) =>
        item !== null &&
        typeof item === 'object' &&
        requiredStringKeys.every((k) => typeof (item as Record<string, unknown>)[k] === 'string')
    );
}

/** useState that persists to localStorage (validated on read, written after first change). */
export function usePersistentState<T>(
  key: string,
  initial: T,
  validate: (v: unknown) => v is T
): [T, React.Dispatch<React.SetStateAction<T>>] {
  const [value, setValue] = useState<T>(() => loadPersisted(key, initial, validate));
  const first = useRef(true);
  useEffect(() => {
    if (first.current) {
      first.current = false;
      return;
    }
    savePersisted(key, value);
  }, [key, value]);
  return [value, setValue];
}
