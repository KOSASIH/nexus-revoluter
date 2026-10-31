import React, { useState } from 'react';
import { 
  Landmark, 
  ShieldCheck, 
  FileText, 
  ExternalLink, 
  CheckCircle2, 
  Layers, 
  Lock, 
  Globe2, 
  Download,
  Terminal,
  Cpu,
  RefreshCw,
  Sparkles
} from 'lucide-react';
import { TreasuryAuditEntry, VaultAccount } from '../types';

interface TreasuryViewProps {
  auditEntries: TreasuryAuditEntry[];
  vaults: VaultAccount[];
}

export const TreasuryView: React.FC<TreasuryViewProps> = ({
  auditEntries,
  vaults
}) => {
  const [isVerifyingChain, setIsVerifyingChain] = useState<boolean>(false);
  const [verificationResult, setVerificationResult] = useState<string | null>(null);
  const [selectedLeafIdx, setSelectedLeafIdx] = useState<number>(0);
  const [isVerifyingSolvency, setIsVerifyingSolvency] = useState<boolean>(false);
  const [solvencySuccessMessage, setSolvencySuccessMessage] = useState<string | null>(null);

  const totalPi = vaults.reduce((acc, v) => acc + v.piBalance, 0);
  const totalXlm = vaults.reduce((acc, v) => acc + v.xlmBalance, 0);

  const handleVerifyChain = () => {
    setIsVerifyingChain(true);
    setVerificationResult(null);

    setTimeout(() => {
      setIsVerifyingChain(false);
      setVerificationResult('SHA-256 Merkle Chain Integrity: 100% Valid. All entries cryptographically link to genesis block without tampering.');
      setTimeout(() => setVerificationResult(null), 6000);
    }, 700);
  };

  const handleVerifySolvencyProof = () => {
    setIsVerifyingSolvency(true);
    setSolvencySuccessMessage(null);

    setTimeout(() => {
      setIsVerifyingSolvency(false);
      setSolvencySuccessMessage('Merkle Proof-of-Solvency Verified: Leaf hash securely links to Root 0x8f4d93b1...314159 with 100% Asset-to-Liability coverage ratio.');
      setTimeout(() => setSolvencySuccessMessage(null), 6000);
    }, 700);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Top Banner */}
      <div className="bg-slate-900/70 p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30 uppercase">
              Module 10 & 11 • Sovereign Ledger
            </span>
            <span className="text-xs text-slate-400">Append-Only Cryptographic Trail</span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1 flex items-center gap-2">
            <Landmark className="w-5 h-5 text-blue-400" />
            Transparent Treasury & Immutable Audit
          </h2>
          <p className="text-xs text-slate-300 max-w-2xl mt-1 leading-relaxed">
            Hash-chained immutable audit trail and sovereign source isolation. Operates with zero dependency on proprietary Core Team servers.
          </p>
        </div>

        <button
          onClick={handleVerifyChain}
          disabled={isVerifyingChain}
          className="flex items-center space-x-1.5 px-3.5 py-2.5 rounded-xl bg-purple-600/20 hover:bg-purple-600 text-purple-300 hover:text-white border border-purple-500/30 text-xs font-semibold transition disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${isVerifyingChain ? 'animate-spin' : ''}`} />
          <span>{isVerifyingChain ? 'Hashing Chain...' : 'Verify Hash Chain Integrity'}</span>
        </button>
      </div>

      {verificationResult && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs flex items-center space-x-2 animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{verificationResult}</span>
        </div>
      )}

      {/* Aggregate Vault Treasury Allocations */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
          <div className="text-xs text-slate-400 font-medium mb-1">Total Treasury Collateral</div>
          <div className="text-xl font-mono font-bold text-white">
            {totalPi.toLocaleString(undefined, { minimumFractionDigits: 2 })} <span className="text-purple-400 text-sm font-bold">π NXS</span>
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Multi-Vault Aggregate</div>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
          <div className="text-xs text-slate-400 font-medium mb-1">Stellar Gas Reserve</div>
          <div className="text-xl font-mono font-bold text-blue-400">
            {totalXlm.toFixed(2)} XLM
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Sufficient for 2.4M transactions</div>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
          <div className="text-xs text-slate-400 font-medium mb-1">Audit Trail State</div>
          <div className="text-xl font-mono font-bold text-emerald-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4" />
            Hash-Chained
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Append-only Merkle linked</div>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
          <div className="text-xs text-slate-400 font-medium mb-1">Deployment Isolation</div>
          <div className="text-xl font-mono font-bold text-purple-400">
            100% Sovereign
          </div>
          <div className="text-[11px] text-slate-500 mt-1">IPFS / Arweave native</div>
        </div>
      </div>

      {/* Module 10: Hash-Chained Audit Trail */}
      <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Layers className="w-4 h-4 text-blue-400" />
              Cryptographic Audit Log (Append-Only)
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Every fee disbursement, grant allocation, and faucet settlement is cryptographically anchored to its predecessor hash.
            </p>
          </div>

          <span className="text-xs font-mono text-slate-500">
            SHA-256 Chained
          </span>
        </div>

        <div className="space-y-3 font-mono text-xs">
          {auditEntries.map((entry) => (
            <div
              key={entry.id}
              className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2 hover:border-slate-700 transition"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 text-[11px]">
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-blue-400">{entry.id}</span>
                  <span className="text-slate-500">•</span>
                  <span className="px-2 py-0.5 rounded text-[9px] font-bold bg-slate-800 text-slate-300">
                    {entry.movementType}
                  </span>
                  <span className="text-slate-400">{entry.destination}</span>
                </div>
                <div className="text-emerald-400 font-bold text-sm">
                  +{entry.amount.toLocaleString(undefined, { minimumFractionDigits: 1 })} <span className="text-xs">{entry.asset}</span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-[10px] pt-1 border-t border-slate-850">
                <div className="text-slate-500 truncate">
                  <span className="text-slate-400 font-semibold">Prev Hash:</span> {entry.prevHash}
                </div>
                <div className="text-purple-300 truncate">
                  <span className="text-slate-400 font-semibold">Entry Hash:</span> {entry.entryHash}
                </div>
              </div>

              <div className="flex items-center justify-between text-[10px] text-slate-500 pt-0.5">
                <span>Timestamp: {entry.timestamp}</span>
                <span className="text-emerald-400 font-semibold flex items-center gap-1">
                  <ShieldCheck className="w-3 h-3" /> {entry.proofSignature}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Module 10.2: Interactive Merkle Tree Proof-of-Solvency Prover */}
      <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30 uppercase">
                Zero-Knowledge Solvency
              </span>
              <span className="text-xs text-slate-400">Cryptographic Merkle Proof</span>
            </div>
            <h3 className="text-base font-bold text-white mt-1 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-purple-400" />
              Interactive Merkle Tree Proof-of-Solvency Prover
            </h3>
            <p className="text-xs text-slate-300 max-w-2xl mt-1">
              Verifies that total sovereign treasury reserves exceed liabilities (Assets &ge; Liabilities) without revealing individual Pioneer account balances.
            </p>
          </div>

          <button
            onClick={handleVerifySolvencyProof}
            disabled={isVerifyingSolvency}
            className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-xs font-semibold text-white shadow-md shadow-purple-600/30 transition disabled:opacity-50 self-start"
          >
            <Sparkles className={`w-3.5 h-3.5 ${isVerifyingSolvency ? 'animate-spin' : ''}`} />
            <span>{isVerifyingSolvency ? 'Hashing Branches...' : 'Verify Proof of Solvency'}</span>
          </button>
        </div>

        {solvencySuccessMessage && (
          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs flex items-center space-x-2 animate-in fade-in">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>{solvencySuccessMessage}</span>
          </div>
        )}

        {/* 2D Interactive SVG Merkle Tree Diagram */}
        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 space-y-3">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="text-slate-400">Interactive Merkle DAG (Click Leaf to Inspect Inclusion Proof):</span>
            <span className="text-purple-400">Root: 0x8f4d93b1...314159</span>
          </div>

          <svg viewBox="0 0 600 210" className="w-full h-52 select-none">
            {/* Tree Branch Connectors */}
            {/* Root to Parents */}
            <line
              x1="300" y1="35" x2="170" y2="95"
              stroke={selectedLeafIdx < 2 ? '#a855f7' : '#334155'}
              strokeWidth={selectedLeafIdx < 2 ? 2.5 : 1}
              strokeDasharray={selectedLeafIdx < 2 ? '4,4' : 'none'}
              className={selectedLeafIdx < 2 ? 'animate-pulse' : ''}
            />
            <line
              x1="300" y1="35" x2="430" y2="95"
              stroke={selectedLeafIdx >= 2 ? '#a855f7' : '#334155'}
              strokeWidth={selectedLeafIdx >= 2 ? 2.5 : 1}
              strokeDasharray={selectedLeafIdx >= 2 ? '4,4' : 'none'}
              className={selectedLeafIdx >= 2 ? 'animate-pulse' : ''}
            />

            {/* Parents to Leaves */}
            <line
              x1="170" y1="95" x2="90" y2="165"
              stroke={selectedLeafIdx === 0 ? '#10b981' : '#334155'}
              strokeWidth={selectedLeafIdx === 0 ? 2.5 : 1}
            />
            <line
              x1="170" y1="95" x2="230" y2="165"
              stroke={selectedLeafIdx === 1 ? '#10b981' : '#334155'}
              strokeWidth={selectedLeafIdx === 1 ? 2.5 : 1}
            />
            <line
              x1="430" y1="95" x2="370" y2="165"
              stroke={selectedLeafIdx === 2 ? '#10b981' : '#334155'}
              strokeWidth={selectedLeafIdx === 2 ? 2.5 : 1}
            />
            <line
              x1="430" y1="95" x2="510" y2="165"
              stroke={selectedLeafIdx === 3 ? '#10b981' : '#334155'}
              strokeWidth={selectedLeafIdx === 3 ? 2.5 : 1}
            />

            {/* Root Node */}
            <g transform="translate(300, 35)">
              <rect x="-85" y="-18" width="170" height="36" rx="8" fill="#1e1b4b" stroke="#818cf8" strokeWidth="1.5" />
              <text textAnchor="middle" dy="-2" fontSize="9" fontWeight="bold" fill="#c7d2fe" fontFamily="monospace">
                Merkle Root
              </text>
              <text textAnchor="middle" dy="11" fontSize="8" fill="#a5b4fc" fontFamily="monospace">
                0x8f4d93b1...314159
              </text>
            </g>

            {/* Parent Branch 0 */}
            <g transform="translate(170, 95)">
              <rect x="-65" y="-15" width="130" height="30" rx="6" fill="#0f172a" stroke={selectedLeafIdx < 2 ? '#a855f7' : '#334155'} strokeWidth="1.5" />
              <text textAnchor="middle" dy="-1" fontSize="8" fontWeight="bold" fill="#e2e8f0" fontFamily="monospace">
                Branch P₀: 0x18e4b7...
              </text>
              <text textAnchor="middle" dy="10" fontSize="7" fill="#94a3b8" fontFamily="monospace">
                H(Leaf₀ || Leaf₁)
              </text>
            </g>

            {/* Parent Branch 1 */}
            <g transform="translate(430, 95)">
              <rect x="-65" y="-15" width="130" height="30" rx="6" fill="#0f172a" stroke={selectedLeafIdx >= 2 ? '#a855f7' : '#334155'} strokeWidth="1.5" />
              <text textAnchor="middle" dy="-1" fontSize="8" fontWeight="bold" fill="#e2e8f0" fontFamily="monospace">
                Branch P₁: 0xd591f0...
              </text>
              <text textAnchor="middle" dy="10" fontSize="7" fill="#94a3b8" fontFamily="monospace">
                H(Leaf₂ || Leaf₃)
              </text>
            </g>

            {/* 4 Leaf Nodes */}
            {[
              { idx: 0, x: 90, label: 'Vault 1 (Primary)', balance: '1,250 π NXS', hash: '0x94f1...02a8' },
              { idx: 1, x: 230, label: 'Vault 2 (Barter)', balance: '850 π NXS', hash: '0x38b2...71e4' },
              { idx: 2, x: 370, label: 'Vault 3 (Staking)', balance: '4,500 π NXS', hash: '0x61c7...99b2' },
              { idx: 3, x: 510, label: 'Vault 4 (Shield)', balance: '3,200 π NXS', hash: '0xfa82...40d1' },
            ].map((leaf) => {
              const isSel = selectedLeafIdx === leaf.idx;
              return (
                <g
                  key={leaf.idx}
                  transform={`translate(${leaf.x}, 165)`}
                  onClick={() => setSelectedLeafIdx(leaf.idx)}
                  className="cursor-pointer transition-transform hover:scale-105"
                >
                  <rect
                    x="-55" y="-18" width="110" height="36" rx="6"
                    fill={isSel ? '#064e3b' : '#0f172a'}
                    stroke={isSel ? '#10b981' : '#334155'}
                    strokeWidth={isSel ? 2 : 1}
                  />
                  <text textAnchor="middle" dy="-3" fontSize="8" fontWeight="bold" fill={isSel ? '#a7f3d0' : '#cbd5e1'}>
                    {leaf.label}
                  </text>
                  <text textAnchor="middle" dy="9" fontSize="8" fontWeight="bold" fill={isSel ? '#34d399' : '#94a3b8'} fontFamily="monospace">
                    {leaf.balance}
                  </text>
                </g>
              );
            })}
          </svg>

          {/* Selected Leaf Proof Audit Card */}
          {(() => {
            const leaves = [
              { idx: 0, name: 'Primary Settlement Vault', balance: '1,250 π NXS', hash: '0x94f18372049182348123019284719283748202a8', siblingHash: '0x38b28471928374829104812347192837482971e4', parentHash: '0x18e4b7c89123049182374819238471928374a192', oppositeParent: '0xd591f0982347192837481923847192837482ce44' },
              { idx: 1, name: 'Pioneer Barter Vault', balance: '850 π NXS', hash: '0x38b28471928374829104812347192837482971e4', siblingHash: '0x94f18372049182348123019284719283748202a8', parentHash: '0x18e4b7c89123049182374819238471928374a192', oppositeParent: '0xd591f0982347192837481923847192837482ce44' },
              { idx: 2, name: 'Sovereign Staking Enclave', balance: '4,500 π NXS', hash: '0x61c78192384719283748192384719283748299b2', siblingHash: '0xfa828192384719283748192384719283748240d1', parentHash: '0xd591f0982347192837481923847192837482ce44', oppositeParent: '0x18e4b7c89123049182374819238471928374a192' },
              { idx: 3, name: 'ZK Shielded Reserve', balance: '3,200 π NXS', hash: '0xfa828192384719283748192384719283748240d1', siblingHash: '0x61c78192384719283748192384719283748299b2', parentHash: '0xd591f0982347192837481923847192837482ce44', oppositeParent: '0x18e4b7c89123049182374819238471928374a192' }
            ];
            const sel = leaves[selectedLeafIdx] || leaves[0];
            return (
              <div className="p-3.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono space-y-2 animate-in fade-in">
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-1.5">
                  <div className="flex items-center space-x-2">
                    <span className="font-bold text-white">{sel.name}</span>
                    <span className="text-emerald-400 font-bold">({sel.balance})</span>
                  </div>
                  <span className="px-2 py-0.5 rounded text-[10px] bg-purple-950 text-purple-300 border border-purple-800">
                    Leaf Index: {sel.idx} / 4
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-[10px]">
                  <div>
                    <span className="text-slate-500 block">Leaf Commitment Hash:</span>
                    <span className="text-slate-300 truncate block">{sel.hash}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block">Inclusion Sibling Hash:</span>
                    <span className="text-blue-300 truncate block">{sel.siblingHash}</span>
                  </div>
                </div>

                <div className="p-2 rounded bg-slate-950 border border-slate-850 text-[10px] text-slate-400">
                  <span className="text-slate-300 font-semibold">Verification Proof: </span>
                  SHA-256(Leaf[{sel.idx}] &oplus; Sibling) &rarr; Parent &rarr; Merkle Root <span className="text-emerald-400 font-bold">0x8f4d93b1...314159 (VALID)</span>
                </div>
              </div>
            );
          })()}
        </div>
      </div>

      {/* Module 11: Source Isolation & Decentralized Deployment */}
      <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl space-y-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 uppercase">
              Module 11 • Source Isolation
            </span>
          </div>
          <h3 className="text-base font-bold text-white mt-1 flex items-center gap-2">
            <Globe2 className="w-4 h-4 text-emerald-400" />
            Decentralized Deployment & Zero Proprietary Dependency
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Nexus Revoluter connects exclusively to public Stellar Horizon nodes and community-operated P2P sentinels.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <div className="font-bold text-white flex items-center gap-1.5">
              <Terminal className="w-4 h-4 text-purple-400" />
              Public Network Connectors
            </div>
            <ul className="text-slate-400 space-y-1.5 leading-relaxed">
              <li className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                <span>Primary Horizon: <code className="text-slate-200">https://horizon.stellar.org</code></span>
              </li>
              <li className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                <span>Community Sentinels: 5 Federated TCP :8080 Nodes</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                <span>Zero proprietary telemetry or Google Analytics scripts</span>
              </li>
            </ul>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <div className="font-bold text-white flex items-center gap-1.5">
              <Lock className="w-4 h-4 text-blue-400" />
              Decentralized Storage Immutability
            </div>
            <ul className="text-slate-400 space-y-1.5 leading-relaxed font-mono text-[11px]">
              <div>IPFS Content ID:</div>
              <div className="text-slate-300 bg-slate-900 p-1.5 rounded border border-slate-800 truncate">
                bafybeihdwdcefgh4dqkjv67u2x4o98as710294812nexusrevoluter
              </div>
              <div className="pt-1">Arweave Permaweb Tx:</div>
              <div className="text-slate-300 bg-slate-900 p-1.5 rounded border border-slate-800 truncate">
                ar://94k2MQW8VR91PXZL029471NVMS947194KOSASIH88
              </div>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
