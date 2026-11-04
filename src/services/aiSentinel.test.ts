import { describe, it, expect } from 'vitest';
import { analyzeTransactionRisk, auditQuantumResistance } from './aiSentinel';

const GOOD_ADDR = 'GDZXAB12CD34EF56GH78IJ90KL12MN34OP56QR78ST90UV12WX34YZ56';

describe('analyzeTransactionRisk', () => {
  it('flags official-trademark impersonation', () => {
    expect(analyzeTransactionRisk('pi-core-team-deposit', 10).phishingRisk).toBe('HIGH');
  });
  it('flags short addresses', () => {
    expect(analyzeTransactionRisk('GSHORT', 10).phishingRisk).toBe('HIGH');
  });
  it('flags credential-harvesting memos', () => {
    expect(analyzeTransactionRisk(GOOD_ADDR, 10, 'urgent: verify seed').phishingRisk).toBe('HIGH');
  });
  it('flags sends above balance', () => {
    expect(analyzeTransactionRisk(GOOD_ADDR, 500, '', 100).phishingRisk).toBe('LOW');
  });
  it('passes a normal transfer', () => {
    expect(analyzeTransactionRisk(GOOD_ADDR, 10, 'rent', 100).phishingRisk).toBe('NONE');
  });
});

describe('auditQuantumResistance', () => {
  it('never claims Ed25519 keys are quantum-impervious', () => {
    const r = auditQuantumResistance(GOOD_ADDR);
    expect(r.securityVerdict).not.toBe('QUANTUM_IMPERVIOUS');
    expect(r.kyberDilithiumWrapper).toBe(false);
    expect(r.shorResistanceYears).toBe(0);
  });
});
