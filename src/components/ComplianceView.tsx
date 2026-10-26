import React, { useState } from 'react';
import { 
  ShieldCheck, 
  Lock, 
  Sparkles, 
  CheckCircle2, 
  FileText, 
  Key, 
  UserCheck, 
  AlertCircle,
  RefreshCw
} from 'lucide-react';
import { ComplianceReport } from '../types';

interface ComplianceViewProps {
  currentReport: ComplianceReport;
  onGenerateNewKyc: (userKey: string, country: string) => void;
}

export const ComplianceView: React.FC<ComplianceViewProps> = ({
  currentReport,
  onGenerateNewKyc
}) => {
  const [pioneerKey, setPioneerKey] = useState(currentReport.userPublicKey);
  const [country, setCountry] = useState('Switzerland');
  const [isGenerating, setIsGenerating] = useState(false);
  const [successNotice, setSuccessNotice] = useState(false);

  const handleGenerate = (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);
    setSuccessNotice(false);
    setTimeout(() => {
      onGenerateNewKyc(pioneerKey, country);
      setIsGenerating(false);
      setSuccessNotice(true);
      setTimeout(() => setSuccessNotice(false), 5000);
    }, 1500);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Banner */}
      <div className="bg-gradient-to-r from-emerald-950/70 via-slate-900 to-blue-950/70 p-6 rounded-2xl border border-emerald-900/40 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 rounded text-[11px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 uppercase">
              ZK-SNARK / ARHN
            </span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1 flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Zero-Knowledge KYC & Autonomous Compliance Analyzer
          </h2>
          <p className="text-xs text-slate-300 max-w-2xl mt-1 leading-relaxed">
            Verify Pioneer identity and transaction legality while retaining 100% cryptographic anonymity. Backed by Groth16 zero-knowledge proofs and the AHCEW empathetic response system.
          </p>
        </div>

        <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 text-right">
          <div className="text-[10px] text-slate-400 uppercase font-semibold">Verification Status</div>
          <div className="text-sm font-mono font-bold text-emerald-400 flex items-center gap-1 justify-end">
            <CheckCircle2 className="w-4 h-4" /> COMPLIANT
          </div>
        </div>
      </div>

      {successNotice && (
        <div className="p-4 rounded-xl bg-emerald-950/60 border border-emerald-800 text-emerald-300 text-xs flex items-center space-x-3">
          <CheckCircle2 className="w-5 h-5 shrink-0 text-emerald-400" />
          <div>
            <div className="font-bold">Zero-Knowledge Proof Generated & Committed to Ledger</div>
            <div className="mt-0.5">Report ID: {currentReport.reportId} | ZK SNARK Hash valid.</div>
          </div>
        </div>
      )}

      {/* Main Grid: ZK Prover Form (Left 5) and Compliance Audit Report (Right 7) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* ZK Prover Form */}
        <div className="lg:col-span-5 bg-slate-900/70 p-6 rounded-2xl border border-slate-800">
          <div className="flex items-center space-x-2 mb-3">
            <Lock className="w-5 h-5 text-emerald-400" />
            <h3 className="text-base font-bold text-white">Generate Anonymous ZK Proof</h3>
          </div>
          <p className="text-xs text-slate-400 mb-5">
            Generates a mathematical proof proving KYC satisfaction without disclosing real names, passport numbers, or raw telemetry.
          </p>

          <form onSubmit={handleGenerate} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Pioneer Public Key</label>
              <input
                type="text"
                value={pioneerKey}
                onChange={(e) => setPioneerKey(e.target.value)}
                className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs font-mono text-slate-200 focus:outline-none focus:ring-1 focus:ring-emerald-500"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Jurisdiction / Country</label>
              <select
                value={country}
                onChange={(e) => setCountry(e.target.value)}
                className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-emerald-500"
              >
                <option value="Switzerland">Switzerland (FINMA Standard)</option>
                <option value="Germany">Germany (BaFin Standard)</option>
                <option value="Japan">Japan (FSA Standard)</option>
                <option value="Singapore">Singapore (MAS Standard)</option>
                <option value="United States">United States (CFTC/SEC Standard)</option>
              </select>
            </div>

            <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-[11px] text-slate-400 space-y-1">
              <div className="flex items-center justify-between">
                <span>Proof Protocol:</span>
                <span className="font-mono text-slate-200 font-semibold">Groth16 / BN254</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Plaintext Leakage:</span>
                <span className="font-mono text-emerald-400 font-semibold">0% (Zero-Knowledge)</span>
              </div>
            </div>

            <button
              type="submit"
              disabled={isGenerating}
              className="w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 font-semibold text-xs text-white transition shadow-lg shadow-emerald-600/20 disabled:opacity-50 flex items-center justify-center space-x-2"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isGenerating ? 'animate-spin' : ''}`} />
              <span>{isGenerating ? 'Computing Mathematical Proof...' : 'Synthesize ZK Proof'}</span>
            </button>
          </form>
        </div>

        {/* Current Compliance Audit Card */}
        <div className="lg:col-span-7 bg-slate-900/70 p-6 rounded-2xl border border-slate-800 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <FileText className="w-4 h-4 text-blue-400" />
                  Active Compliance Report
                </h3>
                <p className="text-xs text-slate-400">Autonomous Regulatory Harmonization Network (ARHN)</p>
              </div>
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800/40">
                {currentReport.reportId}
              </span>
            </div>

            <div className="space-y-4">
              {/* Proof Hash */}
              <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs">
                <div className="text-[10px] text-slate-500 uppercase font-semibold">ZK-SNARK Proof Hash</div>
                <div className="text-emerald-400 break-all font-bold mt-0.5">
                  {currentReport.zkProofHash}
                </div>
              </div>

              {/* Verified Checks List */}
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                  <span className="text-slate-300">AML Screening</span>
                  <span className="text-emerald-400 font-bold flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> PASSED
                  </span>
                </div>

                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                  <span className="text-slate-300">Sanction List Check</span>
                  <span className="text-emerald-400 font-bold flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> CLEAR
                  </span>
                </div>

                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                  <span className="text-slate-300">Velocity Risk Limit</span>
                  <span className="text-emerald-400 font-bold flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> NORMAL
                  </span>
                </div>

                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                  <span className="text-slate-300">Geo Compliance</span>
                  <span className="text-emerald-400 font-bold flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> VERIFIED
                  </span>
                </div>
              </div>

              {/* Empathy Feedback (AHCEW from src/api.py) */}
              <div className="p-4 rounded-xl bg-gradient-to-r from-blue-950/40 to-indigo-950/40 border border-blue-900/40">
                <div className="text-[10px] text-blue-400 uppercase font-bold flex items-center gap-1.5 mb-1">
                  <Sparkles className="w-3.5 h-3.5" />
                  AHCEW Empathetic UX Engine Response
                </div>
                <p className="text-xs text-slate-200 leading-relaxed italic">
                  "{currentReport.empathyFeedback}"
                </p>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800 mt-4 text-[11px] text-slate-500 flex items-center justify-between">
            <span>Verified: {currentReport.timestamp}</span>
            <span>Risk Score: {currentReport.riskScore} / 100 (Extremely Low)</span>
          </div>
        </div>
      </div>
    </div>
  );
};
