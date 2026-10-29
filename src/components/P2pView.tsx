import React, { useState } from 'react';
import { 
  Radio, 
  Activity, 
  Wifi, 
  ShieldCheck, 
  Zap, 
  RefreshCw, 
  Server, 
  CheckCircle2, 
  Play,
  Globe2,
  Lock,
  Layers
} from 'lucide-react';
import { SentinelNode } from '../types';

interface P2pViewProps {
  sentinels: SentinelNode[];
}

export const P2pView: React.FC<P2pViewProps> = ({ sentinels }) => {
  const [activeBroadcastingHop, setActiveBroadcastingHop] = useState<number | null>(null);
  const [isQuorumChecking, setIsQuorumChecking] = useState<boolean>(false);
  const [quorumCheckResult, setQuorumCheckResult] = useState<string | null>(null);
  const [gossipPacketsSent, setGossipPacketsSent] = useState<number>(1420);
  const [lastBroadcastTimestamp, setLastBroadcastTimestamp] = useState<string>('12s ago');

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
              <div className={`flex flex-col items-center min-w-[90px] p-2.5 rounded-lg border transition ${
                activeBroadcastingHop === node.hop
                  ? 'bg-blue-600/20 border-blue-500 text-white shadow-lg shadow-blue-500/20'
                  : 'bg-slate-900 border-slate-800 text-slate-300'
              }`}>
                <div className="text-[10px] font-mono font-bold text-blue-400 uppercase">Hop {node.hop}</div>
                <div className="text-[11px] font-semibold mt-0.5 truncate max-w-[80px]">{node.region.split(',')[0]}</div>
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
