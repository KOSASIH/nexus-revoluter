import { describe, it, expect } from 'vitest';
import { loadPersisted, savePersisted, isRecordArray, StorageLike } from './persist';

function memoryStorage(): StorageLike & { data: Map<string, string> } {
  const data = new Map<string, string>();
  return {
    data,
    getItem: (k) => data.get(k) ?? null,
    setItem: (k, v) => void data.set(k, v),
    removeItem: (k) => void data.delete(k),
  };
}

const isVaults = isRecordArray<{ id: string; address: string }>(['id', 'address']);
const fallback = [{ id: 'default', address: 'GDEFAULT' }];

describe('persist', () => {
  it('round-trips a valid value', () => {
    const s = memoryStorage();
    const v = [{ id: 'a', address: 'GA' }];
    savePersisted('vaults', v, s);
    expect(loadPersisted('vaults', fallback, isVaults, s)).toEqual(v);
  });

  it('returns the fallback when nothing is stored', () => {
    expect(loadPersisted('vaults', fallback, isVaults, memoryStorage())).toBe(fallback);
  });

  it('rejects corrupted JSON and wrong shapes', () => {
    const s = memoryStorage();
    s.setItem('nexus-revoluter:v1:vaults', '{not json');
    expect(loadPersisted('vaults', fallback, isVaults, s)).toBe(fallback);
    s.setItem('nexus-revoluter:v1:vaults', JSON.stringify([{ id: 1, address: 'x' }]));
    expect(loadPersisted('vaults', fallback, isVaults, s)).toBe(fallback);
  });

  it('ignores data from an older schema version', () => {
    const s = memoryStorage();
    s.setItem('nexus-revoluter:v0:vaults', JSON.stringify([{ id: 'a', address: 'GA' }]));
    expect(loadPersisted('vaults', fallback, isVaults, s)).toBe(fallback);
  });

  it('survives unavailable or throwing storage', () => {
    const throwing: StorageLike = {
      getItem: () => { throw new Error('blocked'); },
      setItem: () => { throw new Error('quota'); },
      removeItem: () => {},
    };
    expect(loadPersisted('vaults', fallback, isVaults, throwing)).toBe(fallback);
    expect(() => savePersisted('vaults', fallback, throwing)).not.toThrow();
    expect(loadPersisted('vaults', fallback, isVaults, null)).toBe(fallback);
  });
});
