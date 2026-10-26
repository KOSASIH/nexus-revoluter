import React, { useState } from 'react';
import { Globe, Radio, Play, CheckCircle2, RefreshCw, Zap, Shield, ArrowRight } from 'lucide-react';
import { PeerNode } from '../types';

interface NodeMeshVisualizerProps {
  peers: PeerNode[];
}

export const NodeMeshVisualizer: React.FC<NodeMeshVisualizerProps> = ({ peers }) => {
  const [broadcastMessage, setBroadcastMessage] = useState('SCP Quorum Check #4920');
  const [isBroadcasting, setIsBroadcasting] = useState(false);
  const [broadcastProgress, setBroadcastProgress] = useState<Record<string, number>>({});

  const handleTriggerBroadcast = () => {
    setIsBroadcasting(true);
    setBroadcastProgress({});

    peers.forEach((peer, index) => {
      setTimeout(() => {
        setBroadcastProgress(prev => ({
          ...prev,
          [peer.id]: Date.now()
        }));

        if (index === peers.length - 1) {
          setTimeout(() => setIsBroadcasting(false), 500);
        }
      }, (index + 1) * 350);
    });
  };

  return (
    <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Radio className="w-5 h-5 text-purple-400" />
            P2P Gossip Protocol & SCP Propagation Simulator
          </h3>
          <p className="text-xs text-slate-400">
            Simulate Byzantine-resilient epidemic routing across global validator sentinels
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <input
            type="text"
            value={broadcastMessage}
            onChange={(e) => setBroadcastMessage(e.target.value)}
            placeholder="Broadcast payload..."
            className="px-3 py-1.5 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono text-white focus:outline-none focus:ring-1 focus:ring-purple-500 w-48"
          />
          <button
            onClick={handleTriggerBroadcast}
            disabled={isBroadcasting}
            className="px-3.5 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-500 text-xs font-semibold text-white shadow-md shadow-purple-600/20 transition disabled:opacity-50 flex items-center gap-1.5"
          >
            <Play className={`w-3.5 h-3.5 ${isBroadcasting ? 'animate-spin' : ''}`} />
            <span>{isBroadcasting ? 'Propagating...' : 'Broadcast'}</span>
          </button>
        </div>
      </div>

      {/* Node Mesh Visual Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {peers.map((peer, idx) => {
          const reachedAt = broadcastProgress[peer.id];
          const isReached = !!reachedAt;

          return (
            <div
              key={peer.id}
              className={`p-4 rounded-xl border transition-all duration-300 relative overflow-hidden ${
                isReached
                  ? 'bg-gradient-to-b from-purple-950/40 to-slate-950 border-purple-500/60 shadow-lg shadow-purple-500/10'
                  : 'bg-slate-950/60 border-slate-800/80'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-white flex items-center gap-1.5">
                  <span className={`h-2 w-2 rounded-full ${isReached ? 'bg-emerald-400' : 'bg-slate-600'}`} />
                  {peer.name}
                </span>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800">
                  Hop #{idx + 1}
                </span>
              </div>

              <div className="text-[11px] font-mono text-slate-400 mb-2">
                <div>IP: <span className="text-slate-300">{peer.ip}</span></div>
                <div>Region: <span className="text-slate-300">{peer.location}</span></div>
              </div>

              <div className="pt-2 border-t border-slate-800/60 flex items-center justify-between text-[10px] font-mono">
                <span className="text-emerald-400">Ping: {peer.pingMs}ms</span>
                {isReached ? (
                  <span className="text-purple-300 font-bold flex items-center gap-1">
                    <CheckCircle2 className="w-3 h-3 text-purple-400" /> Quorum Ack
                  </span>
                ) : (
                  <span className="text-slate-500">Idle Listener</span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Network Health & Byzantine Resiliency */}
      <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-slate-400">
        <div className="flex items-center space-x-2">
          <Shield className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>
            Byzantine Quorum Slice: <strong className="text-white">67% Agreement Threshold</strong> satisfied across all global peer groups.
          </span>
        </div>
        <div className="font-mono text-[11px] text-purple-400">
          Epidemic Fanout Factor: 3 Peers / Cycle
        </div>
      </div>
    </div>
  );
};
