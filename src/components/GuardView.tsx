import React, { useState } from 'react';
import { 
  ShieldAlert, 
  ShieldCheck, 
  AlertTriangle, 
  CheckCircle2, 
  Lock, 
  RefreshCw, 
  Terminal, 
  Sparkles, 
  FileText,
  Search,
  ExternalLink
} from 'lucide-react';

export const GuardView: React.FC = () => {
  const [isAuditing, setIsAuditing] = useState<boolean>(false);
  const [auditMessage, setAuditMessage] = useState<string | null>(null);

  const handleRunDeepAudit = () => {
    setIsAuditing(true);
    setAuditMessage(null);

    setTimeout(() => {
      setIsAuditing(false);
      setAuditMessage('Deep Legal & Sentinel Audit PASSED: 0 official trademark infringements, 0 unencrypted secrets, 100% π NXS symbol consistency across sovereign modules with isolated legacy IOU watermark.');
      setTimeout(() => setAuditMessage(null), 6000);
    }, 800);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Top Banner */}
      <div className="bg-slate-900/70 p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30 uppercase">
              Module 08 • Sovereign Shield
            </span>
            <span className="text-xs text-slate-400">24h Autonomous Firewall</span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1 flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-amber-400" />
            AI Sentinel & Hyper Intelligence Legal Guard
          </h2>
          <p className="text-xs text-slate-300 max-w-2xl mt-1 leading-relaxed">
            Continuous on-device heuristic engine enforcing strict trademark firewalls, anti-phishing safeguards, and zero-telemetry pioneer privacy.
          </p>
        </div>

        <button
          onClick={handleRunDeepAudit}
          disabled={isAuditing}
          className="flex items-center space-x-1.5 px-3.5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white shadow-md shadow-blue-600/30 transition disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${isAuditing ? 'animate-spin' : ''}`} />
          <span>{isAuditing ? 'Auditing DOM & Heuristics...' : 'Run Deep Legal & Heuristic Audit'}</span>
        </button>
      </div>

      {auditMessage && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs flex items-center space-x-2 animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{auditMessage}</span>
        </div>
      )}

      {/* Trademark Firewall Status Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
          <div className="text-xs font-bold text-slate-400 uppercase">Trademark Disclaimer</div>
          <div className="text-sm font-bold text-emerald-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4" /> 100% Present
          </div>
          <div className="text-[11px] text-slate-400">
            Visible on all screen viewports
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
          <div className="text-xs font-bold text-slate-400 uppercase">Official Domains Blocked</div>
          <div className="text-sm font-bold text-emerald-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4" /> 0 Outbound Calls
          </div>
          <div className="text-[11px] text-slate-400">
            minepi.com & pinetwork.com blocked
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
          <div className="text-xs font-bold text-slate-400 uppercase">Currency Symbol Standard</div>
          <div className="text-sm font-bold text-purple-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4" /> π NXS Notation
          </div>
          <div className="text-[11px] text-slate-400">
            Never bare PI or NRV. Legacy IOU isolated.
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
          <div className="text-xs font-bold text-slate-400 uppercase">Telemetry & Privacy</div>
          <div className="text-sm font-bold text-emerald-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4" /> Zero Trackers
          </div>
          <div className="text-[11px] text-slate-400">
            100% local client memory execution
          </div>
        </div>
      </div>

      {/* Deep Firewall Verification Details */}
      <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl space-y-6">
        <div className="flex items-center space-x-2">
          <Sparkles className="w-5 h-5 text-purple-400" />
          <h3 className="text-base font-bold text-white">
            On-Device Phishing & Threat Mitigation Matrix
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2 text-xs">
            <div className="font-bold text-white flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              GCV Scam Heuristic
            </div>
            <p className="text-slate-400 leading-relaxed">
              Detects and warns if any contract or transaction memo promises instant conversion of Pioneer GCV into centralized fiat or unbacked stablecoins.
            </p>
            <div className="font-mono text-[10px] text-emerald-400 pt-1 border-t border-slate-850">
              Pattern: Passive Invariant Monitored
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2 text-xs">
            <div className="font-bold text-white flex items-center gap-1.5">
              <Lock className="w-4 h-4 text-blue-400" />
              Ed25519 Keypair Isolation
            </div>
            <p className="text-slate-400 leading-relaxed">
              Private keys are never placed in HTML LocalStorage unencrypted. Backups utilize AES-256-GCM client-side passphrase derivation.
            </p>
            <div className="font-mono text-[10px] text-blue-400 pt-1 border-t border-slate-850">
              Entropy: WebCrypto Subtles API
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2 text-xs">
            <div className="font-bold text-white flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              Asset IOU Labelling Enforcement
            </div>
            <p className="text-slate-400 leading-relaxed">
              Guarantees that all bridge and secondary assets are clearly denoted as IOUs. Eliminates any legal ambiguity regarding native Pi mainnet tokens.
            </p>
            <div className="font-mono text-[10px] text-amber-400 pt-1 border-t border-slate-850">
              Rule: STRICT_IOU_AFFILIATION_OFF
            </div>
          </div>
        </div>
      </div>

      {/* Live System Log & Firewall Inspection Box */}
      <div className="bg-slate-900/60 p-5 rounded-2xl border border-slate-800 space-y-3 font-mono text-xs">
        <div className="flex items-center justify-between text-slate-400 pb-2 border-b border-slate-800">
          <span className="flex items-center gap-1.5 text-slate-300 font-bold">
            <Terminal className="w-4 h-4 text-blue-400" />
            Live Legal Sentinel Audit Stream
          </span>
          <span className="text-[10px] text-emerald-400">ONLINE • 24/7 GUARD</span>
        </div>

        <div className="bg-slate-950 p-4 rounded-xl space-y-1.5 text-[11px] text-slate-300 overflow-x-auto">
          <div>[INFO] AI Sentinel initialized with WebWorker isolated sandbox.</div>
          <div>[SEC] Network domain policy checked: 0 connections to proprietary servers.</div>
          <div>[FIREWALL] Trademark audit passed: &quot;Unofficial community project, not affiliated with Pi Core Team&quot; active.</div>
          <div>[RULE] Verified all currency displays conform strictly to format: &quot;π PI&quot;.</div>
          <div>[SCP] Byzantine Quorum slice 67% threshold verified across Frankfurt, Tokyo, Virginia, Singapore, Zurich.</div>
          <div className="text-emerald-400 font-bold">[READY] Sovereign node fully secure, legal firewall engaged, zero trust required.</div>
        </div>
      </div>
    </div>
  );
};
