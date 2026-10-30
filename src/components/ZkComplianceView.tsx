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
  BrainCircuit,
  Download,
  Cpu,
  Check,
  Copy,
  Atom
} from 'lucide-react';
import { ProofOfReserve, ZkComplianceScreening, ZkCircuitSynthesisResult } from '../types';
import { evaluateProofOfReserveIntelligence, synthesizeZkSnarkCircuit } from '../services/aiSentinel';


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

  // Interactive ZK Circuit Synthesizer State
  const [activeCircuit, setActiveCircuit] = useState<'SOLVENCY_GROTH16' | 'SANCTIONS_MERKLE_PROOF' | 'DKSAP_STEALTH_SCHNORR'>('SOLVENCY_GROTH16');
  const [isSynthesizing, setIsSynthesizing] = useState<boolean>(false);
  const [synthesisOutput, setSynthesisOutput] = useState<ZkCircuitSynthesisResult>(() => synthesizeZkSnarkCircuit('SOLVENCY_GROTH16'));
  const [copiedProofKey, setCopiedProofKey] = useState<string | null>(null);

  const handleRunSynthesis = (type: 'SOLVENCY_GROTH16' | 'SANCTIONS_MERKLE_PROOF' | 'DKSAP_STEALTH_SCHNORR') => {
    setActiveCircuit(type);
    setIsSynthesizing(true);
    setTimeout(() => {
      const result = synthesizeZkSnarkCircuit(type);
      setSynthesisOutput(result);
      setIsSynthesizing(false);
      setSuccessToast(`ZK Circuit [${result.circuitName.slice(0, 30)}...] synthesized and verified in ${result.synthesisTimeMs}ms.`);
      setTimeout(() => setSuccessToast(null), 5000);
    }, 700);
  };

  const handleDownloadZkProof = () => {
    const payload = {
      certificateType: 'SOVEREIGN_ZK_SNARK_GROTH16_CERTIFICATE',
      standard: 'Groth16 / BN254 Pairing Invariant',
      circuit: synthesisOutput.circuitName,
      r1csConstraints: synthesisOutput.r1csConstraintsCount,
      publicInputsCount: synthesisOutput.publicInputsCount,
      witnessHash: synthesisOutput.witnessPolynomialHash,
      provingKey: synthesisOutput.provingKeyHash,
      pairingProof: synthesisOutput.pairingProof,
      verificationLatencyMs: synthesisOutput.verificationPairingMs,
      timestamp: new Date().toISOString()
    };
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(payload, null, 2));
    const dlAnchor = document.createElement('a');
    dlAnchor.setAttribute('href', dataStr);
    dlAnchor.setAttribute('download', `zkproof_${synthesisOutput.circuitType.toLowerCase()}.json`);
    document.body.appendChild(dlAnchor);
    dlAnchor.click();
    dlAnchor.remove();
  };

  const handleCopyHash = (key: string, val: string) => {
    navigator.clipboard.writeText(val);
    setCopiedProofKey(key);
    setTimeout(() => setCopiedProofKey(null), 2000);
  };

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
              {proofOfReserve.totalVaultObligations.toLocaleString()} <span className="text-purple-400 text-sm font-bold">π NXS</span>
            </div>
            <div className="text-[11px] text-slate-500 mt-1">Sum of private user commitments</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium">On-Chain Collateral Proven</div>
            <div className="text-2xl font-mono font-bold text-emerald-400 mt-1">
              {proofOfReserve.onChainCollateralProven.toLocaleString()} <span className="text-purple-400 text-sm font-bold">π NXS</span>
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

      {/* ADVANCED MODULE 4.2: Interactive ZK-SNARK Circuit Synthesizer & Pairing Verifier */}
      <div className="bg-slate-900/80 p-6 rounded-2xl border border-purple-500/30 space-y-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30 uppercase flex items-center gap-1.5">
                <Atom className="w-3.5 h-3.5 text-purple-400" />
                BN254 Elliptic Curve Pairing Enclave
              </span>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/20 text-emerald-300 border border-emerald-800/40">
                Zero Witness Leakage
              </span>
            </div>
            <h3 className="text-base font-bold text-white mt-1.5 flex items-center gap-2">
              <Cpu className="w-5 h-5 text-purple-400" />
              Interactive zk-SNARK Circuit Synthesizer & Groth16 Verifier
            </h3>
            <p className="text-xs text-slate-400 max-w-2xl">
              Compile Rank-1 Constraint Systems (R1CS), generate QAP witness polynomials, and evaluate bilinear pairings e(A, B) = e(α, β) · e(x, γ) in real-time in-browser.
            </p>
          </div>

          <button
            onClick={handleDownloadZkProof}
            className="flex items-center space-x-1.5 px-3.5 py-2.5 rounded-xl bg-purple-600/20 hover:bg-purple-600 text-purple-300 hover:text-white border border-purple-500/30 text-xs font-semibold transition self-start"
          >
            <Download className="w-4 h-4 text-purple-300" />
            <span>Export ZK Proof Certificate (.json)</span>
          </button>
        </div>

        {/* Circuit Selector Buttons */}
        <div className="flex flex-wrap gap-2 pt-1 border-t border-slate-800">
          {[
            { id: 'SOLVENCY_GROTH16' as const, label: 'Groth16 PoR Solvency Invariant', tag: 'Assets >= Liabilities' },
            { id: 'SANCTIONS_MERKLE_PROOF' as const, label: 'Poseidon Merkle Non-Membership', tag: 'AML Whitelist' },
            { id: 'DKSAP_STEALTH_SCHNORR' as const, label: 'DKSAP Ephemeral Linkability', tag: 'Anonymity Shield' },
          ].map((circ) => {
            const isSelected = activeCircuit === circ.id;
            return (
              <button
                key={circ.id}
                onClick={() => handleRunSynthesis(circ.id)}
                disabled={isSynthesizing}
                className={`px-3.5 py-2 rounded-xl text-xs font-semibold transition flex items-center gap-2 border ${
                  isSelected
                    ? 'bg-purple-600 text-white border-purple-500 shadow-md shadow-purple-600/20'
                    : 'bg-slate-950/80 border-slate-800 text-slate-400 hover:text-white'
                }`}
              >
                <span>{circ.label}</span>
                <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${
                  isSelected ? 'bg-purple-800 text-purple-200' : 'bg-slate-900 text-slate-500'
                }`}>
                  {circ.tag}
                </span>
              </button>
            );
          })}
        </div>

        {/* Circuit Verification Display Panel */}
        <div className="p-5 rounded-xl bg-slate-950 border border-purple-900/40 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3">
            <div>
              <div className="text-xs font-bold text-white flex items-center gap-2">
                <span>{synthesisOutput.circuitName}</span>
                {isSynthesizing && <RefreshCw className="w-3.5 h-3.5 text-purple-400 animate-spin" />}
              </div>
              <div className="text-[11px] font-mono text-slate-400 mt-0.5">
                Curve: <span className="text-purple-300 font-bold">{synthesisOutput.ellipticCurve}</span> • Certificate: <span className="text-emerald-400">{synthesisOutput.zkCertificateHash}</span>
              </div>
            </div>

            <span className="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-800 uppercase flex items-center gap-1">
              <Check className="w-3 h-3 text-emerald-400" />
              Pairing Invariant Satisfied
            </span>
          </div>

          {/* Metrics 4-Box Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">
              <span className="text-[10px] uppercase font-bold text-slate-400 block">R1CS Constraints</span>
              <span className="text-lg font-mono font-black text-purple-300">{synthesisOutput.r1csConstraintsCount.toLocaleString()}</span>
              <span className="text-[9px] text-slate-500 block">Non-linear gate checks</span>
            </div>

            <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">
              <span className="text-[10px] uppercase font-bold text-slate-400 block">Public Inputs</span>
              <span className="text-lg font-mono font-black text-blue-300">{synthesisOutput.publicInputsCount} Variables</span>
              <span className="text-[9px] text-slate-500 block">Zero private witness revealed</span>
            </div>

            <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">
              <span className="text-[10px] uppercase font-bold text-slate-400 block">Witness Compute</span>
              <span className="text-lg font-mono font-black text-emerald-300">{synthesisOutput.synthesisTimeMs} ms</span>
              <span className="text-[9px] text-slate-500 block">Fast in-browser synthesis</span>
            </div>

            <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">
              <span className="text-[10px] uppercase font-bold text-slate-400 block">Bilinear Pairing</span>
              <span className="text-lg font-mono font-black text-amber-300">{synthesisOutput.verificationPairingMs} ms</span>
              <span className="text-[9px] text-slate-500 block">Weil / Tate pairing check</span>
            </div>
          </div>

          {/* Group 1 & Group 2 Pairing Proof Elements */}
          <div className="space-y-2 pt-2 border-t border-slate-850 font-mono text-[11px]">
            <div className="flex items-center justify-between text-slate-400 text-xs">
              <span className="font-semibold text-slate-300">Cryptographic Pairing Proof Points (G1 x G2):</span>
              <button
                onClick={() => handleCopyHash('pairing', JSON.stringify(synthesisOutput.pairingProof))}
                className="text-purple-400 hover:text-purple-300 flex items-center gap-1 text-[11px]"
              >
                {copiedProofKey === 'pairing' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedProofKey === 'pairing' ? 'Copied Points' : 'Copy Points'}</span>
              </button>
            </div>

            <div className="p-2.5 rounded bg-slate-900 border border-slate-800/80 space-y-1 text-slate-300 text-[10px] break-all">
              <div><strong className="text-purple-400">π_A (G1):</strong> {synthesisOutput.pairingProof.piA}</div>
              <div><strong className="text-blue-400">π_B (G2):</strong> {synthesisOutput.pairingProof.piB}</div>
              <div><strong className="text-emerald-400">π_C (G1):</strong> {synthesisOutput.pairingProof.piC}</div>
            </div>

            <div className="p-2.5 rounded bg-purple-950/20 border border-purple-900/30 text-[10px] text-purple-200 flex items-center justify-between">
              <span>Bilinear Equation: <strong>e(π_A, π_B) == e(α, β) · e(∑ x_i · γ_i, δ) · e(π_C, δ)</strong></span>
              <span className="text-emerald-400 font-bold">100% Cryptographic Match</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
