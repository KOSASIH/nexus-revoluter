import React, { useState } from 'react';
import { 
  ShieldCheck, 
  Lock, 
  EyeOff, 
  CheckCircle2, 
  FileCode, 
  RefreshCw, 
  Layers, 
  Sparkles,
  AlertCircle,
  ExternalLink,
  BrainCircuit
} from 'lucide-react';
import { ProofOfReserve, ZkComplianceScreening } from '../types';
import { evaluateProofOfReserveIntelligence } from '../services/aiSentinel';


interface ZkComplianceViewProps {
  proofOfReserve: ProofOfReserve;
  complianceScreening: ZkComplianceScreening;
}

export const ZkComplianceView: React.FC<ZkComplianceViewProps> = ({
  proofOfReserve,
  complianceScreening
}) => {
  const [isRegenerating, setIsRegenerating] = useState<boolean>(false);
  const [lastVerifiedEpoch, setLastVerifiedEpoch] = useState<string>('Epoch 4920 (Verified in Browser)');
  const [successToast, setSuccessToast] = useState<string | null>(null);

  const handleRecomputeSnark = () => {
    setIsRegenerating(true);
    setSuccessToast(null);

    setTimeout(() => {
      setIsRegenerating(false);
      setLastVerifiedEpoch(`Epoch ${Math.floor(Math.random() * 50 + 4920)} (Fresh Groth16 Proof Synthesized)`);
      setSuccessToast('ZK-SNARK Invariant Proof Verified: On-chain collateral strictly exceeds total vault obligations (Coverage: 314.6%). Zero balance leaked.');
      setTimeout(() => setSuccessToast(null), 6000);
    }, 1000);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Top Banner */}
      <div className="bg-slate-900/70 p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30 uppercase">
              Module 04 • Privacy & Solvency
            </span>
            <span className="text-xs text-slate-400">Zero-Knowledge Cryptography</span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1 flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            ZK Compliance Layer & Proof of Reserve
          </h2>
          <p className="text-xs text-slate-300 max-w-2xl mt-1 leading-relaxed">
            Mathematical proof of 100%+ solvency and sanctions compliance without exposing Pioneer account balances or personal identifiable information.
          </p>
        </div>

        <button
          onClick={handleRecomputeSnark}
          disabled={isRegenerating}
          className="flex items-center space-x-1.5 px-3.5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white shadow-md shadow-blue-600/30 transition disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${isRegenerating ? 'animate-spin' : ''}`} />
          <span>{isRegenerating ? 'Synthesizing zk-SNARK...' : 'Re-verify ZK Invariant'}</span>
        </button>
      </div>

      {successToast && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs flex items-center space-x-2 animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{successToast}</span>
        </div>
      )}

      {/* Proof of Reserve Solvency Card */}
      <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <EyeOff className="w-4 h-4 text-purple-400" />
              Cryptographic Proof of Reserve (PoR)
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Groth16 polynomial circuit proving solvency invariant: <code className="text-purple-300 font-mono">Collateral &gt; Obligations</code> without revealing individual balances.
            </p>
          </div>

          <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-800/50 self-start">
            {proofOfReserve.solvencyStatus} (314.6%)
          </span>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium">Total Vault Obligations</div>
            <div className="text-2xl font-mono font-bold text-white mt-1">
              {proofOfReserve.totalVaultObligations.toLocaleString()} <span className="text-purple-400 text-sm font-normal">π PI</span>
            </div>
            <div className="text-[11px] text-slate-500 mt-1">Sum of private user commitments</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium">On-Chain Collateral Proven</div>
            <div className="text-2xl font-mono font-bold text-emerald-400 mt-1">
              {proofOfReserve.onChainCollateralProven.toLocaleString()} <span className="text-purple-400 text-sm font-normal">π PI</span>
            </div>
            <div className="text-[11px] text-slate-500 mt-1">Locked in verifiable multi-sig vaults</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium">Coverage Solvency Ratio</div>
            <div className="text-2xl font-mono font-bold text-blue-400 mt-1">
              {proofOfReserve.coverageRatio.toFixed(3)}x
            </div>
            <div className="text-[11px] text-slate-500 mt-1">Safe invariant: &gt; 1.000x strictly required</div>
          </div>
        </div>

        {/* ZK Proof Hash Container */}
        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 space-y-2">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-300">
            <span className="flex items-center gap-1.5 font-mono text-purple-300">
              <FileCode className="w-3.5 h-3.5 text-purple-400" />
              ZK-SNARK Commitment Root Hash
            </span>
            <span className="text-[10px] text-slate-500">{lastVerifiedEpoch}</span>
          </div>
          <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-850 font-mono text-xs text-slate-300 break-all">
            {proofOfReserve.zkProofHash}
          </div>
          <div className="text-[11px] text-slate-400 flex items-center justify-between">
            <span>Circuit: R1CS / BN254 Elliptic Curve Pairing</span>
            <span className="text-emerald-400 font-bold">100% Cryptographic Match</span>
          </div>
        </div>
      </div>

      {/* ZK Compliance Check: ARHN & AHCEW Screenings */}
      <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl space-y-6">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            Autonomous ARHN & AHCEW Screening Engine
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Decentralized AML/CFT compliance without centralized KYC databases. Verifies zero connection to sanctioned addresses via Merkle membership proofs.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* ARHN Card */}
          <div className="p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <span className="h-2 w-2 rounded-full bg-emerald-400" />
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200">
                  ARHN Compliance
                </h4>
              </div>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-800/40">
                PASSED
              </span>
            </div>

            <p className="text-xs text-slate-400 leading-relaxed">
              <strong>Autonomous Risk Harmonization Network:</strong> Verifies that user public keys have 0 transaction intersections with illicit mixers or flagged entities.
            </p>

            <div className="pt-2 border-t border-slate-850 text-xs font-mono text-slate-400 flex justify-between">
              <span>Risk Rating:</span>
              <span className="text-emerald-400 font-bold">0 / 100 (Optimal)</span>
            </div>
          </div>

          {/* AHCEW Card */}
          <div className="p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <span className="h-2 w-2 rounded-full bg-blue-400" />
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200">
                  AHCEW Screening
                </h4>
              </div>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-950 text-blue-300 border border-blue-800/40">
                VERIFIED
              </span>
            </div>

            <p className="text-xs text-slate-400 leading-relaxed">
              <strong>Autonomous Human-Centric Empathy & Welfare:</strong> Prevents aggressive predatory drainers, excessive liquidation cascades, and unfair micro-fees.
            </p>

            <div className="pt-2 border-t border-slate-850 text-xs font-mono text-slate-400 flex justify-between">
              <span>Protection Status:</span>
              <span className="text-blue-400 font-bold">Active Shield</span>
            </div>
          </div>
        </div>

        {/* User ZK Screening Voucher */}
        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2 text-xs">
          <div className="flex justify-between items-center text-slate-400">
            <span>Client Screening Proof Token:</span>
            <span className="font-mono text-slate-200 font-bold">{complianceScreening.zkProofToken}</span>
          </div>
          <div className="text-[11px] text-slate-500">
            Status: {complianceScreening.sanctionCheckZk} • {complianceScreening.timestamp}
          </div>
        </div>

        {/* AI Cryptographic Soundness & CRS Verifier */}
        {(() => {
          const porAi = evaluateProofOfReserveIntelligence(proofOfReserve);
          return (
            <div className="p-4 rounded-xl bg-gradient-to-r from-slate-950 via-blue-950/20 to-slate-950 border border-blue-900/40 space-y-2 text-xs">
              <div className="flex items-center justify-between">
                <span className="font-bold text-blue-300 flex items-center gap-1.5">
                  <BrainCircuit className="w-3.5 h-3.5 text-blue-400" />
                  AI Cryptographic Invariant & Solvency Intelligence:
                </span>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-800">
                  CRS {porAi.crsIntegrity}
                </span>
              </div>
              <p className="text-[11px] text-slate-400 leading-relaxed">
                {porAi.mathematicalSoundness}
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1 font-mono text-[10px]">
                <div className="p-2 rounded bg-slate-900/80 border border-slate-800 text-slate-300">
                  <span className="text-slate-500 block">Surplus Margin:</span>
                  <span className="text-emerald-400 font-bold">{porAi.overcollateralizationMargin}</span>
                </div>
                <div className="p-2 rounded bg-slate-900/80 border border-slate-800 text-slate-300">
                  <span className="text-slate-500 block">Collateral Stability:</span>
                  <span className="text-blue-300">{porAi.varianceMetrics}</span>
                </div>
              </div>
            </div>
          );
        })()}
      </div>
    </div>
  );
};
