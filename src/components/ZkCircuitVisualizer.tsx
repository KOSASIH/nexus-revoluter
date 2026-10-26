import React, { useState } from 'react';
import { Lock, Sparkles, CheckCircle2, Play, RefreshCw, Key, ShieldCheck, Binary, ChevronRight } from 'lucide-react';

export const ZkCircuitVisualizer: React.FC = () => {
  const [activeStep, setActiveStep] = useState<number>(1);
  const [isSynthesizing, setIsSynthesizing] = useState<boolean>(false);
  const [proofGenerated, setProofGenerated] = useState<boolean>(false);

  const handleRunPipeline = () => {
    setIsSynthesizing(true);
    setProofGenerated(false);
    setActiveStep(1);

    setTimeout(() => {
      setActiveStep(2);
      setTimeout(() => {
        setActiveStep(3);
        setTimeout(() => {
          setActiveStep(4);
          setIsSynthesizing(false);
          setProofGenerated(true);
        }, 600);
      }, 600);
    }, 600);
  };

  return (
    <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Binary className="w-5 h-5 text-emerald-400" />
            Groth16 Zero-Knowledge SNARK Circuit Pipeline
          </h3>
          <p className="text-xs text-slate-400">
            Interactive R1CS constraint system validating Pioneer identity credentials without plaintext disclosure
          </p>
        </div>

        <button
          onClick={handleRunPipeline}
          disabled={isSynthesizing}
          className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-xs font-semibold text-white shadow-lg shadow-emerald-600/20 transition disabled:opacity-50 flex items-center gap-1.5"
        >
          <Play className={`w-3.5 h-3.5 ${isSynthesizing ? 'animate-spin' : ''}`} />
          <span>{isSynthesizing ? 'Synthesizing Circuit...' : 'Run ZK Pipeline Test'}</span>
        </button>
      </div>

      {/* 4 Pipeline Steps */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
        {/* Step 1 */}
        <div className={`p-4 rounded-xl border transition-all ${
          activeStep >= 1 ? 'bg-slate-950 border-emerald-500/60' : 'bg-slate-950/40 border-slate-800/80 opacity-60'
        }`}>
          <div className="flex items-center justify-between mb-2">
            <span className="font-mono text-[10px] text-emerald-400 font-bold uppercase">Phase 01</span>
            {activeStep > 1 ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> : <Lock className="w-3.5 h-3.5 text-slate-500" />}
          </div>
          <div className="font-bold text-white mb-1">Private Inputs</div>
          <p className="text-[11px] text-slate-400">
            Pioneer Keypair, Biometric Hash, and Age constraint kept private in client enclave.
          </p>
        </div>

        {/* Step 2 */}
        <div className={`p-4 rounded-xl border transition-all ${
          activeStep >= 2 ? 'bg-slate-950 border-emerald-500/60' : 'bg-slate-950/40 border-slate-800/80 opacity-60'
        }`}>
          <div className="flex items-center justify-between mb-2">
            <span className="font-mono text-[10px] text-emerald-400 font-bold uppercase">Phase 02</span>
            {activeStep > 2 ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> : <Sparkles className="w-3.5 h-3.5 text-slate-500" />}
          </div>
          <div className="font-bold text-white mb-1">R1CS Arithmetic Gates</div>
          <p className="text-[11px] text-slate-400">
            Transforms compliance conditions into Quadratic Arithmetic Programs (QAP).
          </p>
        </div>

        {/* Step 3 */}
        <div className={`p-4 rounded-xl border transition-all ${
          activeStep >= 3 ? 'bg-slate-950 border-emerald-500/60' : 'bg-slate-950/40 border-slate-800/80 opacity-60'
        }`}>
          <div className="flex items-center justify-between mb-2">
            <span className="font-mono text-[10px] text-emerald-400 font-bold uppercase">Phase 03</span>
            {activeStep > 3 ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> : <Key className="w-3.5 h-3.5 text-slate-500" />}
          </div>
          <div className="font-bold text-white mb-1">BN254 Curve Pairing</div>
          <p className="text-[11px] text-slate-400">
            Generates 128-byte mathematical proof vectors (πA, πB, πC) in elliptic curve group.
          </p>
        </div>

        {/* Step 4 */}
        <div className={`p-4 rounded-xl border transition-all ${
          activeStep >= 4 ? 'bg-slate-950 border-emerald-500/60' : 'bg-slate-950/40 border-slate-800/80 opacity-60'
        }`}>
          <div className="flex items-center justify-between mb-2">
            <span className="font-mono text-[10px] text-emerald-400 font-bold uppercase">Phase 04</span>
            {proofGenerated ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> : <ShieldCheck className="w-3.5 h-3.5 text-slate-500" />}
          </div>
          <div className="font-bold text-white mb-1">On-Chain Verification</div>
          <p className="text-[11px] text-slate-400">
            Smart contract validates pairing equation in 1.4ms with zero plaintext exposure.
          </p>
        </div>
      </div>

      {proofGenerated && (
        <div className="p-4 rounded-xl bg-slate-950 border border-emerald-800/70 font-mono text-xs space-y-1.5 animate-in fade-in">
          <div className="text-[10px] text-emerald-400 uppercase font-bold flex items-center justify-between">
            <span>Synthesized Proof Vector Output</span>
            <span className="text-slate-400">Time: 1.42ms • Gas: 42,100</span>
          </div>
          <div className="text-slate-300 break-all text-[11px]">
            πA = [0x194fa8...981, 0x8a102c...310] | πB = [[0x981...], [0x304...]] | πC = [0x501...]
          </div>
        </div>
      )}
    </div>
  );
};
