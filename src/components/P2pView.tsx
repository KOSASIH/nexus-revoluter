import React, { useState } from 'react';
import { 
  Radio, 
  Activity, 
  Wifi, 
  ShieldCheck, 
  Zap, 
  RefreshCw, 
  Server, 
  Globe2,
  Layers,
  AlertTriangle,
  BrainCircuit,
  ShieldAlert,
  Sparkles,
  Sliders,
  CheckCircle2
} from 'lucide-react';
import { SentinelNode, SelfHealingEvent } from '../types';
import { INITIAL_SELF_HEALING_LOGS } from '../data/initialData';
import { simulateSelfHealingRemediation } from '../services/aiSentinel';
import { MempoolViewer } from './MempoolViewer';

interface P2pViewProps {
  sentinels: SentinelNode[];
}

export const P2pView: React.FC<P2pViewProps> = ({ sentinels }) => {
  const [activeBroadcastingHop, setActiveBroadcastingHop] = useState<number | null>(null);
  const [isQuorumChecking, setIsQuorumChecking] = useState<boolean>(false);
  const [quorumCheckResult, setQuorumCheckResult] = useState<string | null>(null);
  const [gossipPacketsSent, setGossipPacketsSent] = useState<number>(1420);
  const [lastBroadcastTimestamp, setLastBroadcastTimestamp] = useState<string>('12s ago');
  const [healingLogs, setHealingLogs] = useState<SelfHealingEvent[]>(INITIAL_SELF_HEALING_LOGS);
  const [isSimulatingAttack, setIsSimulatingAttack] = useState<boolean>(false);
  const [anomalyStatusMessage, setAnomalyStatusMessage] = useState<string | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>('node-fra');

  const handleSimulateAttack = (type: 'BYZANTINE_DRIFT' | 'ECLIPSE_ATTACK_ATTEMPT' | 'MEMPOOL_FLOOD') => {
    setIsSimulatingAttack(true);
    setAnomalyStatusMessage(`Injecting synthetic ${type} vector into P2P gossip mesh...`);

    setTimeout(() => {
      const remediation = simulateSelfHealingRemediation(type);
      setHealingLogs(prev => [remediation, ...prev.slice(0, 9)]);
      setAnomalyStatusMessage(`Autonomous remediation completed in ${remediation.recoveryLatencyMs}ms: ${remediation.remediationAction}`);
      setIsSimulatingAttack(false);
      setTimeout(() => setAnomalyStatusMessage(null), 6000);
    }, 900);
  };

  // Sequential animated epidemic broadcast simulation
  const handleBroadcastGossip = () => {
    setActiveBroadcastingHop(1);
    setGossipPacketsSent(prev => prev + 5);
    setLastBroadcastTimestamp('Just now');

    let currentHop = 1;
    const interval = setInterval(() => {
      currentHop++;
      if (currentHop <= 5) {
        setActiveBroadcastingHop(currentHop);
      } else {
        clearInterval(interval);
        setTimeout(() => setActiveBroadcastingHop(null), 1000);
      }
    }, 600);
  };

  const handleQuorumCheck = () => {
    setIsQuorumChecking(true);
    setQuorumCheckResult(null);

    setTimeout(() => {
      setIsQuorumChecking(false);
      setQuorumCheckResult('Federated Byzantine Agreement (FBA) Verified: 100% of slices overlap with 0 blocking sets.');
      setTimeout(() => setQuorumCheckResult(null), 6000);
    }, 800);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Top Banner */}
      <div className="bg-slate-900/70 p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30 uppercase">
              Module 02 • Consensus Mesh
            </span>
            <span className="text-xs text-slate-400">Federated Byzantine Agreement</span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1 flex items-center gap-2">
            <Radio className="w-5 h-5 text-blue-400" />
            P2P Gossip Protocol and SCP Propagation Simulator
          </h2>
          <p className="text-xs text-slate-300 max-w-2xl mt-1 leading-relaxed">
            Simulate Byzantine resilient epidemic routing across global validator sentinels. Real-time topology with zero centralized coordinators.
          </p>
        </div>

        {/* Action Controls: SCP Quorum Check & Broadcast */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={handleQuorumCheck}
            disabled={isQuorumChecking}
            className="flex items-center space-x-1.5 px-3.5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 transition disabled:opacity-50"
          >
            <ShieldCheck className={`w-4 h-4 text-emerald-400 ${isQuorumChecking ? 'animate-spin' : ''}`} />
            <span>{isQuorumChecking ? 'Evaluating Slices...' : 'SCP Quorum Check'}</span>
          </button>

          <button
            onClick={handleBroadcastGossip}
            disabled={activeBroadcastingHop !== null}
            className="flex items-center space-x-1.5 px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white shadow-md shadow-blue-600/30 transition disabled:opacity-50"
          >
            <Zap className={`w-4 h-4 text-amber-300 ${activeBroadcastingHop !== null ? 'animate-bounce' : ''}`} />
            <span>{activeBroadcastingHop !== null ? `Gossip Propagation (Hop ${activeBroadcastingHop}/5)...` : 'Broadcast'}</span>
          </button>
        </div>
      </div>

      {quorumCheckResult && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs flex items-center space-x-2 animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{quorumCheckResult}</span>
        </div>
      )}

      {/* Network Health Overview Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
          <div className="text-xs text-slate-400 font-medium mb-1">Global Sentinels Active</div>
          <div className="text-2xl font-mono font-bold text-white flex items-center gap-2">
            5 / 5
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-400 animate-pulse" />
          </div>
          <div className="text-[11px] text-slate-500 mt-1">100% Byzantine Quorum Slices</div>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
          <div className="text-xs text-slate-400 font-medium mb-1">Average Peer Latency</div>
          <div className="text-2xl font-mono font-bold text-blue-400">
            35.4 ms
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Sub-100ms global convergence</div>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
          <div className="text-xs text-slate-400 font-medium mb-1">Gossip Packets Propagated</div>
          <div className="text-2xl font-mono font-bold text-purple-400">
            {gossipPacketsSent.toLocaleString()}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Last broadcast: {lastBroadcastTimestamp}</div>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
          <div className="text-xs text-slate-400 font-medium mb-1">Consensus Algorithm</div>
          <div className="text-2xl font-mono font-bold text-emerald-400">
            SCP / FBA
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Stellar Consensus Protocol</div>
        </div>
      </div>

      {/* 5 Sentinel Nodes Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <Server className="w-4 h-4 text-blue-400" />
            Federated Validator Sentinels (5 Global Hop Nodes)
          </h3>
          <span className="text-xs text-slate-400 font-mono">Port 8080 Gossip Listeners</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sentinels.map((node) => {
            const isHopActive = activeBroadcastingHop === node.hop;

            return (
              <div
                key={node.id}
                className={`p-5 rounded-2xl border transition-all duration-300 relative overflow-hidden ${
                  isHopActive
                    ? 'bg-blue-900/30 border-blue-500 shadow-xl shadow-blue-500/20 scale-[1.02]'
                    : 'bg-slate-900/80 border-slate-800 hover:border-slate-700'
                }`}
              >
                {/* Visual pulse line during gossip wave */}
                {isHopActive && (
                  <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-purple-500 to-emerald-400 animate-pulse" />
                )}

                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-2.5">
                    {/* Active Pulsing Dot */}
                    <span className="relative flex h-3 w-3">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                      <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
                    </span>

                    <div>
                      <h4 className="text-xs font-bold text-white leading-tight">
                        {node.name}
                      </h4>
                      <p className="text-[11px] text-slate-400 flex items-center gap-1 mt-0.5">
                        <Globe2 className="w-3 h-3 text-slate-500" />
                        {node.region}
                      </p>
                    </div>
                  </div>

                  {/* Hop Badge */}
                  <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase ${
                    isHopActive
                      ? 'bg-blue-600 text-white animate-pulse'
                      : 'bg-slate-800 text-blue-400 border border-slate-700'
                  }`}>
                    Hop {node.hop}
                  </span>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-800/80 space-y-2 text-xs">
                  {/* IP with port 8080 */}
                  <div className="flex justify-between items-center font-mono">
                    <span className="text-slate-400">Endpoint:</span>
                    <span className="text-slate-200 font-semibold">{node.ip}:{node.port}</span>
                  </div>

                  {/* Ping in ms */}
                  <div className="flex justify-between items-center font-mono">
                    <span className="text-slate-400">Latency:</span>
                    <span className="text-emerald-400 font-semibold flex items-center gap-1">
                      <Wifi className="w-3 h-3" />
                      {node.pingMs} ms
                    </span>
                  </div>

                  {/* Quorum Ack Badge */}
                  <div className="flex justify-between items-center">
                    <span className="text-slate-400">Quorum Ack:</span>
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-800/50 flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" /> ACKNOWLEDGED
                    </span>
                  </div>

                  <div className="flex justify-between items-center text-[11px] text-slate-400 pt-1">
                    <span>Role:</span>
                    <span className="text-slate-300">{node.role}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Live Epidemic Wave Visualizer */}
      <div className="bg-slate-900/60 p-5 rounded-2xl border border-slate-800 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 text-xs font-semibold text-slate-300">
            <Activity className="w-4 h-4 text-purple-400" />
            <span>Epidemic Gossip Mesh Propagation</span>
          </div>
          <span className="text-[11px] font-mono text-slate-500">Fanout: 3 Peers/Round</span>
        </div>

        {/* Visual Topology Graph */}
        <div className="flex items-center justify-between p-4 bg-slate-950 rounded-xl border border-slate-800/80 overflow-x-auto gap-2">
          {sentinels.map((node, idx) => (
            <React.Fragment key={node.id}>
              <div 
                onClick={() => setSelectedNodeId(node.id)}
                className={`flex flex-col items-center min-w-[95px] p-2.5 rounded-lg border cursor-pointer transition ${
                  selectedNodeId === node.id
                    ? 'bg-indigo-600/25 border-indigo-500 text-white shadow-lg shadow-indigo-500/20 ring-1 ring-indigo-500/50'
                    : activeBroadcastingHop === node.hop
                    ? 'bg-blue-600/20 border-blue-500 text-white shadow-lg shadow-blue-500/20'
                    : 'bg-slate-900 border-slate-800 text-slate-300 hover:border-slate-700'
                }`}
              >
                <div className="text-[10px] font-mono font-bold text-blue-400 uppercase">Hop {node.hop}</div>
                <div className="text-[11px] font-semibold mt-0.5 truncate max-w-[85px]">{node.region.split(',')[0]}</div>
                <div className="text-[9px] font-mono text-slate-500">{node.pingMs}ms</div>
              </div>
              {idx < sentinels.length - 1 && (
                <div className={`h-0.5 flex-1 min-w-[20px] transition ${
                  activeBroadcastingHop !== null && activeBroadcastingHop > idx
                    ? 'bg-blue-500 shadow-md shadow-blue-500'
                    : 'bg-slate-800'
                }`} />
              )}
            </React.Fragment>
          ))}
        </div>

        {/* Selected Node Slice Overlay Inspector */}
        {selectedNodeId && (() => {
          const selNode = sentinels.find(n => n.id === selectedNodeId) || sentinels[0];
          return (
            <div className="p-3.5 bg-slate-950/80 rounded-xl border border-indigo-900/40 text-xs font-mono space-y-2 animate-in fade-in">
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-2">
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-white">{selNode.name}</span>
                  <span className="text-[10px] text-indigo-400">({selNode.region})</span>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-950 text-emerald-300 border border-emerald-800">
                  Quorum Weight: 1.00 • Zero Blocking Sets
                </span>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px]">
                <div>
                  <span className="text-slate-500 block text-[10px]">SCP Slice Set:</span>
                  <span className="text-slate-200">4 of 5 Federated Nodes</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px]">Ping Stability:</span>
                  <span className="text-emerald-400">{selNode.pingMs} ms (Sub-50ms)</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px]">Byzantine Threshold:</span>
                  <span className="text-purple-300">67% Required (100% Satisfied)</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px]">Sybil Signature:</span>
                  <span className="text-blue-300">Amanah Validated</span>
                </div>
              </div>
            </div>
          );
        })()}
      </div>

      {/* Mempool Transaction Queue */}
      <MempoolViewer />

      {/* Autonomous Byzantine Resilience & Self-Healing Matrix */}
      <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 uppercase flex items-center gap-1.5">
                <BrainCircuit className="w-3.5 h-3.5 text-indigo-400" />
                Autonomous Heuristic Matrix
              </span>
              <span className="text-xs text-slate-400">SCP Quorum Auto-Healer</span>
            </div>
            <h3 className="text-base font-bold text-white mt-1 flex items-center gap-2">
              Byzantine Fault Tolerance & Self-Healing Simulator
            </h3>
            <p className="text-xs text-slate-400 max-w-2xl">
              Simulate adversarial Byzantine conditions against the federated quorum. Watch the Sentinel Mesh autonomously isolate rogue nodes, dynamically re-weight quorum slices, and self-heal in sub-second latency.
            </p>
          </div>

          <div className="flex items-center gap-2 font-mono text-xs">
            <span className="px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-300">
              Tolerance: <strong>N &ge; 3f + 1 (f=1)</strong>
            </span>
          </div>
        </div>

        {/* Anomaly Trigger Controls */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <button
            onClick={() => handleSimulateAttack('BYZANTINE_DRIFT')}
            disabled={isSimulatingAttack}
            className="p-3.5 rounded-xl bg-slate-950 hover:bg-slate-850 border border-slate-800 hover:border-amber-500/40 text-left transition disabled:opacity-50 space-y-1.5"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-amber-300 flex items-center gap-1.5">
                <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
                Byzantine Latency Drift
              </span>
              <span className="text-[10px] font-mono text-slate-500">Inject +120ms</span>
            </div>
            <p className="text-[11px] text-slate-400 leading-snug">
              Simulates packet desync on Virginia relay node. Tests gossip fanout elevation.
            </p>
          </button>

          <button
            onClick={() => handleSimulateAttack('ECLIPSE_ATTACK_ATTEMPT')}
            disabled={isSimulatingAttack}
            className="p-3.5 rounded-xl bg-slate-950 hover:bg-slate-850 border border-slate-800 hover:border-red-500/40 text-left transition disabled:opacity-50 space-y-1.5"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-red-300 flex items-center gap-1.5">
                <ShieldAlert className="w-3.5 h-3.5 text-red-400" />
                Sybil Eclipse Attack
              </span>
              <span className="text-[10px] font-mono text-slate-500">Rogue Peer</span>
            </div>
            <p className="text-[11px] text-slate-400 leading-snug">
              Injects rogue peer attempting conflicting slot attestation. Tests Trademark Firewall auto-isolation.
            </p>
          </button>

          <button
            onClick={() => handleSimulateAttack('MEMPOOL_FLOOD')}
            disabled={isSimulatingAttack}
            className="p-3.5 rounded-xl bg-slate-950 hover:bg-slate-850 border border-slate-800 hover:border-purple-500/40 text-left transition disabled:opacity-50 space-y-1.5"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-purple-300 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-purple-400" />
                Mempool Micro-Spam
              </span>
              <span className="text-[10px] font-mono text-slate-500">Spam Burst</span>
            </div>
            <p className="text-[11px] text-slate-400 leading-snug">
              Tests dynamic zero-rent queueing to prioritize valid π PI Pioneer transfers.
            </p>
          </button>
        </div>

        {/* Dynamic Anomaly Feedback */}
        {anomalyStatusMessage && (
          <div className="p-3.5 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-xs text-indigo-200 flex items-center space-x-2 animate-in fade-in">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>{anomalyStatusMessage}</span>
          </div>
        )}

        {/* Live Self-Healing Event Log */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-slate-400">
            <span>Autonomous Self-Healing Event Log</span>
            <span className="text-[10px] font-mono text-slate-500">{healingLogs.length} Events Verified</span>
          </div>

          <div className="space-y-2">
            {healingLogs.slice(0, 3).map((log) => (
              <div 
                key={log.id} 
                className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs"
              >
                <div className="space-y-0.5">
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800/40">
                      {log.severity}
                    </span>
                    <span className="font-bold text-white">{log.incidentType}</span>
                    <span className="text-slate-500 font-mono text-[10px]">• {log.timestamp}</span>
                  </div>
                  <div className="text-[11px] text-slate-400">
                    Target: <span className="text-slate-300">{log.affectedTarget}</span>
                  </div>
                  <div className="text-[11px] text-indigo-300">
                    Remediation: {log.remediationAction}
                  </div>
                </div>

                <div className="text-right sm:shrink-0 font-mono text-[10px]">
                  <span className="text-emerald-400 font-bold block">{log.recoveryLatencyMs} ms</span>
                  <span className="text-slate-500">{log.autonomousAgent}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Mandatory Exact Bottom Text Container */}
      <div className="p-4 rounded-xl bg-slate-950/90 border border-slate-800/90 text-xs text-slate-300 leading-relaxed shadow-inner">
        <div className="flex items-start space-x-2.5">
          <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
          <p className="font-medium text-slate-200">
            Byzantine Quorum Slice 67 percent Agreement Threshold satisfied across all global peer groups. Epidemic Fanout Factor 3 Peers per Cycle
          </p>
        </div>
      </div>
    </div>
  );
};
