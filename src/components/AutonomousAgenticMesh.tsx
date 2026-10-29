import React, { useState } from 'react';
import { 
  Bot, 
  BrainCircuit, 
  Sparkles, 
  ShieldCheck, 
  CheckCircle2, 
  Activity, 
  Flame, 
  Lock, 
  Cpu, 
  Terminal, 
  ArrowRight, 
  RefreshCw,
  Copy,
  Check,
  FileCode2,
  Atom
} from 'lucide-react';
import { SovereignAgent, AgentInferenceResponse } from '../types';
import { SOVEREIGN_AGENTS, inferSovereignAgent } from '../services/aiSentinel';

interface AutonomousAgenticMeshProps {
  nodesCount?: number;
  qThermoBacking?: number;
  vaultAddress?: string;
}

export const AutonomousAgenticMesh: React.FC<AutonomousAgenticMeshProps> = ({
  nodesCount = 5,
  qThermoBacking = 3.14159,
  vaultAddress
}) => {
  const [selectedAgent, setSelectedAgent] = useState<SovereignAgent>(SOVEREIGN_AGENTS[0]);
  const [customPrompt, setCustomPrompt] = useState<string>(SOVEREIGN_AGENTS[0].samplePrompts[0]);
  const [isInferring, setIsInferring] = useState<boolean>(false);
  const [inferenceResult, setInferenceResult] = useState<AgentInferenceResponse | null>(() => 
    inferSovereignAgent(SOVEREIGN_AGENTS[0].id, SOVEREIGN_AGENTS[0].samplePrompts[0], {
      nodesCount,
      qThermoBacking,
      vaultAddress
    })
  );
  const [copiedSignature, setCopiedSignature] = useState<boolean>(false);

  const handleSelectAgent = (agent: SovereignAgent) => {
    setSelectedAgent(agent);
    setCustomPrompt(agent.samplePrompts[0]);
  };

  const handleRunInference = (promptText?: string) => {
    const query = promptText || customPrompt;
    if (!query.trim()) return;

    setIsInferring(true);
    setInferenceResult(null);

    setTimeout(() => {
      const response = inferSovereignAgent(selectedAgent.id, query.trim(), {
        nodesCount,
        qThermoBacking,
        vaultAddress
      });
      setInferenceResult(response);
      setIsInferring(false);
    }, 750);
  };

  const handleCopySignature = () => {
    if (!inferenceResult) return;
    navigator.clipboard.writeText(JSON.stringify(inferenceResult, null, 2));
    setCopiedSignature(true);
    setTimeout(() => setCopiedSignature(false), 2000);
  };

  return (
    <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-6 shadow-xl">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 rounded text-[11px] font-mono font-bold bg-blue-500/20 text-blue-300 border border-blue-500/40 uppercase flex items-center gap-1.5">
              <BrainCircuit className="w-3.5 h-3.5 text-blue-400" />
              Web4 ASANN • Sovereign Agentic Mesh
            </span>
            <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
              Zero-Custodian In-Browser AI
            </span>
          </div>

          <h3 className="text-xl font-bold text-white mt-1.5 flex items-center gap-2">
            Autonomous Sovereign Agent Neural Network
          </h3>
          <p className="text-xs text-slate-300 max-w-3xl mt-1 leading-relaxed">
            4 decentralized cognitive agents execute autonomous real-time heuristics across consensus slices, physical thermodynamic backing in <strong className="text-white">π PI</strong>, Amanah equity, and post-quantum zero-knowledge cryptography.
          </p>
        </div>

        <div className="flex items-center space-x-3 text-xs font-mono">
          <div className="px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-slate-300">
            Active Agents: <span className="font-bold text-emerald-400">4 / 4 Online</span>
          </div>
        </div>
      </div>

      {/* 4 Agent Selector Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {SOVEREIGN_AGENTS.map((agent) => {
          const isSelected = selectedAgent.id === agent.id;
          return (
            <div
              key={agent.id}
              onClick={() => handleSelectAgent(agent)}
              className={`p-4 rounded-xl border cursor-pointer transition flex flex-col justify-between space-y-3 ${
                isSelected
                  ? 'bg-gradient-to-br from-indigo-950/90 to-slate-900 border-indigo-500 ring-1 ring-indigo-500/50 shadow-lg shadow-indigo-500/10'
                  : 'bg-slate-950/70 border-slate-800 hover:border-slate-700 hover:bg-slate-900'
              }`}
            >
              <div>
                <div className="flex items-center justify-between">
                  <div className={`w-8 h-8 rounded-lg bg-gradient-to-tr ${agent.avatarColor} flex items-center justify-center text-white shadow-md`}>
                    {agent.id === 'ARHANA' && <Activity className="w-4 h-4" />}
                    {agent.id === 'AGNI_Q' && <Flame className="w-4 h-4" />}
                    {agent.id === 'DHARMA_AI' && <ShieldCheck className="w-4 h-4" />}
                    {agent.id === 'VAJRA_ZK' && <Atom className="w-4 h-4" />}
                  </div>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800/40 font-semibold">
                    {agent.confidenceScore}% Acc.
                  </span>
                </div>

                <h4 className="text-sm font-bold text-white mt-2.5">
                  {agent.name}
                </h4>
                <div className="text-[10px] font-mono text-indigo-400">
                  {agent.codename}
                </div>
                <p className="text-[11px] text-slate-400 mt-1 line-clamp-2">
                  {agent.role}
                </p>
              </div>

              <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[10px] font-mono text-slate-500">
                <span>{agent.heuristicHeuristicsCount} heuristics</span>
                <span className="text-emerald-400">● Active</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Interactive Inference Terminal */}
      <div className="p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div className="flex items-center space-x-2 text-xs font-bold text-white">
            <Terminal className="w-4 h-4 text-blue-400" />
            <span>Interactive Inference Console • {selectedAgent.name} ({selectedAgent.cognitiveLayer})</span>
          </div>
          <span className="text-[11px] text-slate-400 font-mono">
            Pure client-side zero-knowledge execution
          </span>
        </div>

        {/* Quick Sample Prompts */}
        <div className="flex flex-wrap gap-1.5">
          {selectedAgent.samplePrompts.map((prompt, i) => (
            <button
              key={i}
              onClick={() => {
                setCustomPrompt(prompt);
                handleRunInference(prompt);
              }}
              className="text-[11px] px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-850 text-slate-300 border border-slate-800 hover:border-indigo-500/40 transition text-left"
            >
              &ldquo;{prompt}&rdquo;
            </button>
          ))}
        </div>

        {/* Query Input Box */}
        <div className="flex gap-2">
          <input
            type="text"
            value={customPrompt}
            onChange={(e) => setCustomPrompt(e.target.value)}
            placeholder={`Inquire with ${selectedAgent.name}...`}
            className="flex-1 bg-slate-900 border border-slate-800 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-500 font-mono focus:outline-none"
          />
          <button
            onClick={() => handleRunInference()}
            disabled={isInferring || !customPrompt.trim()}
            className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-bold shadow-md shadow-blue-600/20 transition flex items-center gap-1.5 disabled:opacity-50"
          >
            <Sparkles className={`w-3.5 h-3.5 ${isInferring ? 'animate-spin' : ''}`} />
            <span>{isInferring ? 'Synthesizing...' : 'Infer'}</span>
          </button>
        </div>

        {/* Inference Output Card */}
        {inferenceResult && (
          <div className="mt-4 p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-4 animate-in fade-in">
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3">
              <div className="flex items-center space-x-2">
                <span className="text-xs font-bold text-white">Agent Output:</span>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-800 uppercase">
                  {inferenceResult.verdict}
                </span>
                <span className="text-[10px] font-mono text-slate-500">{inferenceResult.timestamp}</span>
              </div>

              <button
                onClick={handleCopySignature}
                className="flex items-center space-x-1 px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-[11px] font-mono text-slate-300 transition"
                title="Copy attestation proof as JSON"
              >
                {copiedSignature ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                <span>{copiedSignature ? 'Copied' : 'Copy Proof JSON'}</span>
              </button>
            </div>

            {/* Cognitive Reasoning Chain */}
            <div className="space-y-1.5">
              <div className="text-[11px] font-mono font-bold text-indigo-300 uppercase tracking-wider">
                Cognitive Reasoning Chain:
              </div>
              <div className="space-y-1 font-mono text-[11px] text-slate-300">
                {inferenceResult.reasoningChain.map((step, idx) => (
                  <div key={idx} className="p-2 rounded bg-slate-950/70 border border-slate-850 flex items-start gap-2">
                    <span className="text-indigo-400 font-bold shrink-0">{idx + 1}.</span>
                    <span>{step}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Mathematical Metrics Table */}
            <div className="space-y-1.5">
              <div className="text-[11px] font-mono font-bold text-emerald-300 uppercase tracking-wider">
                Mathematical Verification Metrics:
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2 text-xs font-mono">
                {Object.entries(inferenceResult.mathematicalMetrics).map(([key, val]) => (
                  <div key={key} className="p-2.5 bg-slate-950 rounded-lg border border-slate-800">
                    <div className="text-[10px] text-slate-400 uppercase truncate">{key}</div>
                    <div className="text-sm font-bold text-white mt-0.5">{val}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Cryptographic Signature Attestation */}
            <div className="p-2.5 bg-slate-950 rounded-lg border border-slate-800 flex items-center justify-between text-[11px] font-mono">
              <span className="text-slate-400">Ed25519 Proof Hash:</span>
              <span className="text-purple-300 font-semibold truncate max-w-xs">{inferenceResult.cryptographicSignature}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
