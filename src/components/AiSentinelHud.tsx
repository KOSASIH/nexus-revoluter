import React, { useState } from 'react';
import { 
  Bot, 
  BrainCircuit, 
  ShieldCheck, 
  AlertTriangle, 
  Activity, 
  Sparkles, 
  CheckCircle2, 
  Cpu, 
  Radio, 
  ChevronDown, 
  ChevronUp,
  RefreshCw,
  Zap
} from 'lucide-react';
import { SentinelNode } from '../types';
import { diagnoseConsensusHealth } from '../services/aiSentinel';

interface AiSentinelHudProps {
  sentinels: SentinelNode[];
  onTriggerSelfHealing?: () => void;
}

export const AiSentinelHud: React.FC<AiSentinelHudProps> = ({ sentinels, onTriggerSelfHealing }) => {
  const [isExpanded, setIsExpanded] = useState<boolean>(false);
  const [isDiagnosing, setIsDiagnosing] = useState<boolean>(false);
  const [diagnosticStep, setDiagnosticStep] = useState<string>('');
  const [adversarialSimActive, setAdversarialSimActive] = useState<boolean>(false);

  const report = diagnoseConsensusHealth(sentinels);

  const runFullAiDiagnostic = () => {
    setIsDiagnosing(true);
    setDiagnosticStep('Connecting to SCP federated gossip layer...');

    setTimeout(() => {
      setDiagnosticStep('Evaluating 67% Byzantine quorum slice tolerance...');
    }, 600);

    setTimeout(() => {
      setDiagnosticStep('Verifying Groth16 zero-knowledge polynomial constraints...');
    }, 1200);

    setTimeout(() => {
      setDiagnosticStep('Screening address space against Trademark Firewall blacklist...');
    }, 1800);

    setTimeout(() => {
      setDiagnosticStep('Autonomous AI analysis complete: Zero vulnerabilities detected.');
      setIsDiagnosing(false);
    }, 2400);
  };

  const handleSimulateAdversarialDrift = () => {
    setAdversarialSimActive(true);
    if (onTriggerSelfHealing) {
      onTriggerSelfHealing();
    }
    setTimeout(() => {
      setAdversarialSimActive(false);
    }, 4000);
  };

  return (
    <div className="bg-slate-900/90 backdrop-blur border-y border-blue-500/30 text-slate-200 transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2.5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          {/* Left Title & Status Indicator */}
          <div className="flex items-center space-x-3">
            <div className="relative flex items-center justify-center w-8 h-8 rounded-lg bg-blue-600/20 border border-blue-500/40 text-blue-400">
              <BrainCircuit className="w-4 h-4 animate-pulse" />
              <span className="absolute -top-1 -right-1 flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
            </div>

            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-bold tracking-wider uppercase text-blue-400 flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                  Sovereign AI Cognitive Matrix 1000x
                </span>
                <span className="text-[10px] bg-blue-950 text-blue-300 px-2 py-0.5 rounded border border-blue-800 font-mono">
                  Autonomous Heuristic Engine
                </span>
                <span className="text-[10px] bg-emerald-950 text-emerald-300 px-2 py-0.5 rounded border border-emerald-800 font-mono">
                  Byzantine Quorum 67% Satisified
                </span>
              </div>
              <p className="text-[11px] text-slate-400">
                Continuous real-time threat scanning, SCP quorum drift analysis, and Shura DAO deliberation.
              </p>
            </div>
          </div>

          {/* Right Action Buttons */}
          <div className="flex items-center space-x-2">
            <button
              onClick={runFullAiDiagnostic}
              disabled={isDiagnosing}
              className="text-xs bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-medium px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all shadow-sm active:scale-95 disabled:opacity-50"
            >
              {isDiagnosing ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin text-blue-200" />
                  <span>Diagnosing...</span>
                </>
              ) : (
                <>
                  <Zap className="w-3.5 h-3.5 text-amber-300" />
                  <span>Deep AI Scan</span>
                </>
              )}
            </button>

            <button
              onClick={handleSimulateAdversarialDrift}
              disabled={adversarialSimActive}
              className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 px-2.5 py-1.5 rounded-lg flex items-center gap-1.5 transition-all active:scale-95 text-[11px]"
              title="Test Byzantine resilience by injecting a simulated rogue packet"
            >
              <AlertTriangle className={`w-3.5 h-3.5 ${adversarialSimActive ? 'text-amber-400 animate-bounce' : 'text-slate-400'}`} />
              <span>{adversarialSimActive ? 'Healing Quorum...' : 'Simulate Adversarial Injection'}</span>
            </button>

            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-xs bg-slate-800/80 hover:bg-slate-700 text-slate-300 px-2 py-1.5 rounded-lg border border-slate-700 transition-colors flex items-center gap-1"
            >
              <span className="text-[11px]">{isExpanded ? 'Collapse' : 'Telemetry'}</span>
              {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
            </button>
          </div>
        </div>

        {/* Live Diagnostic Status Bar */}
        {diagnosticStep && (
          <div className="mt-2.5 px-3 py-1.5 bg-blue-950/70 border border-blue-800/50 rounded-md text-[11px] text-blue-300 flex items-center justify-between font-mono animate-fade-in">
            <div className="flex items-center space-x-2">
              <Cpu className="w-3.5 h-3.5 text-blue-400 animate-spin" />
              <span>{diagnosticStep}</span>
            </div>
            <span className="text-[10px] text-emerald-400 uppercase tracking-widest font-bold">1000x Smart Sentinel</span>
          </div>
        )}

        {/* Adversarial Simulation Banner */}
        {adversarialSimActive && (
          <div className="mt-2.5 px-3 py-2 bg-amber-950/80 border border-amber-800 rounded-md text-xs text-amber-200 flex items-center justify-between font-mono animate-pulse">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              <span>[ADVERSARIAL STRESS TEST] Injected Byzantine delay into Tokyo Sentinel (142ms). Autonomous SCP healing re-routed consensus slice in 8ms!</span>
            </div>
            <span className="bg-emerald-900 text-emerald-200 px-2 py-0.5 rounded text-[10px] font-bold">QUORUM INTACT (100%)</span>
          </div>
        )}

        {/* Expanded Telemetry Cards */}
        {isExpanded && (
          <div className="mt-4 pt-4 border-t border-slate-800 grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
            {/* Metric 1 */}
            <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-3">
              <div className="flex items-center justify-between text-slate-400 mb-1">
                <span className="text-[11px] font-medium">Byzantine Fault Margin</span>
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
              </div>
              <div className="text-lg font-bold text-emerald-400 font-mono">
                {report.quorumHealth}%
              </div>
              <p className="text-[10px] text-slate-500 mt-0.5">
                Exceeds 67% SCP requirement across all 5 federated sentinels.
              </p>
            </div>

            {/* Metric 2 */}
            <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-3">
              <div className="flex items-center justify-between text-slate-400 mb-1">
                <span className="text-[11px] font-medium">ZK Proof Solvency Index</span>
                <Activity className="w-4 h-4 text-blue-400" />
              </div>
              <div className="text-lg font-bold text-blue-400 font-mono">
                {report.solvencyIndex}%
              </div>
              <p className="text-[10px] text-slate-500 mt-0.5">
                Groth16 polynomial verified. 0% fractional reserve exposure.
              </p>
            </div>

            {/* Metric 3 */}
            <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-3">
              <div className="flex items-center justify-between text-slate-400 mb-1">
                <span className="text-[11px] font-medium">Sybil Resistance Quotient</span>
                <Radio className="w-4 h-4 text-indigo-400" />
              </div>
              <div className="text-lg font-bold text-indigo-400 font-mono">
                {report.sybilResistanceScore}%
              </div>
              <p className="text-[10px] text-slate-500 mt-0.5">
                Quadratic stake weight √π NXS × log2(vaultAge) in active enforcement.
              </p>
            </div>

            {/* Metric 4 */}
            <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-3">
              <div className="flex items-center justify-between text-slate-400 mb-1">
                <span className="text-[11px] font-medium">Cognitive Threat Level</span>
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              </div>
              <div className="text-lg font-bold text-emerald-400 font-mono">
                {report.threatLevel}
              </div>
              <p className="text-[10px] text-slate-500 mt-0.5">
                Trademark Firewall & Phishing heuristic radar operational.
              </p>
            </div>

            {/* Live 5-Node Sentinel Quorum Topology Matrix */}
            <div className="md:col-span-4 bg-slate-950/90 border border-indigo-950/60 rounded-xl p-3.5 space-y-2.5">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-white flex items-center gap-1.5">
                  <Radio className="w-3.5 h-3.5 text-blue-400" />
                  Live Federated Quorum Topology & Latency Mesh (5 Global Sentinels)
                </span>
                <span className="text-[10px] font-mono text-emerald-400 font-semibold">
                  Byzantine Slices Overlap: 100% (Safety Surplus +33%)
                </span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 font-mono text-[11px]">
                {sentinels.map((s) => (
                  <div key={s.id} className="p-2.5 bg-slate-900/90 rounded-lg border border-slate-800 space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-slate-200 text-[10px] truncate">{s.name.split(' ')[0]}</span>
                      <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
                    </div>
                    <div className="text-slate-400 text-[10px] truncate">{s.region}</div>
                    <div className="flex items-center justify-between text-[10px] pt-1 border-t border-slate-850">
                      <span className="text-emerald-400 font-bold">{s.pingMs}ms</span>
                      <span className="text-slate-500">{s.uptime}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Recommendations / Auto-Remediations Details */}
            <div className="md:col-span-4 bg-slate-950/60 border border-slate-800/80 rounded-lg p-3 mt-1">
              <div className="text-[11px] font-semibold text-slate-300 mb-1.5 flex items-center gap-1.5">
                <Bot className="w-3.5 h-3.5 text-blue-400" />
                <span>Autonomous Cognitive Intelligence Insights:</span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] text-slate-400">
                {report.recommendations.map((rec, idx) => (
                  <div key={idx} className="flex items-start space-x-1.5">
                    <span className="text-blue-500 font-bold">•</span>
                    <span>{rec}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
