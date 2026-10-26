import React, { useState } from 'react';
import { 
  Layers, 
  Activity, 
  Server, 
  Wifi, 
  Globe, 
  Radio, 
  Zap, 
  ShieldCheck, 
  Clock, 
  ChevronRight,
  RefreshCw,
  Plus,
  CheckCircle2
} from 'lucide-react';
import { Block, PeerNode } from '../types';
import { MempoolViewer } from './MempoolViewer';
import { NodeMeshVisualizer } from './NodeMeshVisualizer';

interface NodeViewProps {
  blockHeight: number;
  blocks: Block[];
  peers: PeerNode[];
  onAddPeer: (peer: { name: string; ip: string; location: string; role: PeerNode['role'] }) => void;
  onOptimizeLatency: () => void;
}

export const NodeView: React.FC<NodeViewProps> = ({
  blockHeight,
  blocks,
  peers,
  onAddPeer,
  onOptimizeLatency
}) => {
  const [selectedBlock, setSelectedBlock] = useState<Block | null>(null);
  const [isAddingPeer, setIsAddingPeer] = useState(false);
  const [peerName, setPeerName] = useState('');
  const [peerIp, setPeerIp] = useState('');
  const [peerLocation, setPeerLocation] = useState('');
  const [peerRole, setPeerRole] = useState<PeerNode['role']>('Validator');
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [optimizationMessage, setOptimizationMessage] = useState<string | null>(null);

  const handleAddPeerSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!peerName || !peerIp) return;
    onAddPeer({
      name: peerName,
      ip: peerIp,
      location: peerLocation || 'Global Cloud Region',
      role: peerRole
    });
    setPeerName('');
    setPeerIp('');
    setPeerLocation('');
    setIsAddingPeer(false);
  };

  const handleRunLatencyOptimizer = () => {
    setIsOptimizing(true);
    setOptimizationMessage(null);
    setTimeout(() => {
      onOptimizeLatency();
      setIsOptimizing(false);
      setOptimizationMessage('Gossip protocol routes refreshed: Average P2P latency reduced by 14.8ms across 5 regional clusters.');
      setTimeout(() => setOptimizationMessage(null), 5000);
    }, 1200);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Node Metrics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Consensus */}
        <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
            <span className="font-medium">Consensus Engine</span>
            <Zap className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-lg font-bold text-white">Quantum Swarm</div>
          <div className="text-[11px] text-amber-400 font-medium mt-1">
            Hybrid SCP + Pi Byz-Fault
          </div>
        </div>

        {/* Throughput */}
        <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
            <span className="font-medium">Live Throughput</span>
            <Activity className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-lg font-mono font-bold text-white">1,480 TPS</div>
          <div className="text-[11px] text-blue-400 font-medium mt-1">
            Peak Capacity: 45,000 TPS
          </div>
        </div>

        {/* Dynamic Fee Oracle */}
        <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
            <span className="font-medium">Dynamic Fee Oracle</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-lg font-mono font-bold text-emerald-400">0.00010 XLM</div>
          <div className="text-[11px] text-slate-400 font-medium mt-1">
            0.0000314 π PI equivalent
          </div>
        </div>

        {/* Gossip Mesh */}
        <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
            <span className="font-medium">Active Peers</span>
            <Radio className="w-4 h-4 text-purple-400 animate-pulse" />
          </div>
          <div className="text-lg font-bold text-white">{peers.length} Nodes</div>
          <div className="text-[11px] text-purple-400 font-medium mt-1">
            Mesh Topology: Fully Interconnected
          </div>
        </div>
      </div>

      {/* Latency Optimization Banner */}
      {optimizationMessage && (
        <div className="p-3.5 rounded-xl bg-emerald-950/40 border border-emerald-800/60 text-emerald-300 text-xs flex items-center space-x-2">
          <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-400" />
          <span>{optimizationMessage}</span>
        </div>
      )}

      {/* Main Section: Block Explorer (Left 7) and Gossip Peers (Right 5) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Blocks Feed */}
        <div className="lg:col-span-7 bg-slate-900/70 p-6 rounded-2xl border border-slate-800">
          <div className="flex items-center justify-between mb-5">
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Layers className="w-4 h-4 text-blue-400" />
                Live Block Explorer
              </h3>
              <p className="text-xs text-slate-400">Sequential cryptographically verified ledger sequences</p>
            </div>
            <div className="flex items-center space-x-2 text-xs font-mono px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 text-slate-300">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-ping" />
              <span>Slot #{blockHeight}</span>
            </div>
          </div>

          <div className="space-y-3">
            {blocks.map((block) => (
              <div
                key={block.height}
                onClick={() => setSelectedBlock(block)}
                className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 hover:border-blue-500/50 hover:bg-slate-900/80 transition cursor-pointer"
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-sm font-bold text-blue-400">
                      Block #{block.height}
                    </span>
                    <span className="text-[10px] text-slate-400 flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {block.timestamp}
                    </span>
                  </div>
                  <div className="text-right">
                    <span className="text-xs font-mono font-semibold text-slate-200">
                      {block.txCount} txs
                    </span>
                  </div>
                </div>

                <div className="text-[11px] font-mono text-slate-400 truncate mb-2">
                  <span className="text-slate-500">Hash: </span>
                  {block.hash}
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-800/60">
                  <span className="text-slate-300 font-medium">Validator: {block.validator}</span>
                  <span className="text-slate-500">{block.sizeKb} KB</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Peer Nodes & Gossip Mesh */}
        <div className="lg:col-span-5 bg-slate-900/70 p-6 rounded-2xl border border-slate-800 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <Globe className="w-4 h-4 text-purple-400" />
                  P2P Node Mesh
                </h3>
                <p className="text-xs text-slate-400">Global Gossip protocol peers</p>
              </div>

              <button
                onClick={() => setIsAddingPeer(true)}
                className="p-1.5 rounded-lg bg-blue-600/20 text-blue-400 hover:bg-blue-600 hover:text-white border border-blue-500/30 transition text-xs flex items-center gap-1"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Add Peer</span>
              </button>
            </div>

            {/* Peers List */}
            <div className="space-y-3 max-h-[420px] overflow-y-auto pr-1">
              {peers.map((peer) => (
                <div
                  key={peer.id}
                  className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-bold text-white">{peer.name}</span>
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800/40">
                      {peer.role}
                    </span>
                  </div>

                  <div className="flex items-center justify-between text-[11px] text-slate-400 mb-2">
                    <span className="font-mono text-slate-300">{peer.ip}</span>
                    <span>{peer.location}</span>
                  </div>

                  <div className="flex items-center justify-between text-[10px] text-slate-400 pt-1.5 border-t border-slate-800/60 font-mono">
                    <span className="flex items-center gap-1">
                      <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                      Ping: <strong className="text-emerald-400">{peer.pingMs}ms</strong>
                    </span>
                    <span>Uptime: {peer.uptime}</span>
                    <span className="text-slate-500">{peer.version}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Action button */}
          <div className="pt-4 border-t border-slate-800 mt-4">
            <button
              onClick={handleRunLatencyOptimizer}
              disabled={isOptimizing}
              className="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 font-semibold text-xs text-slate-200 transition border border-slate-700 flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isOptimizing ? 'animate-spin' : ''}`} />
              <span>{isOptimizing ? 'Running Latency Optimizer...' : 'Optimize P2P Gossip Routes'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Unconfirmed Memory Pool (Mempool) */}
      <MempoolViewer />

      {/* P2P Gossip Protocol & SCP Propagation Simulator */}
      <NodeMeshVisualizer peers={peers} />

      {/* Add Peer Modal */}
      {isAddingPeer && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-md w-full p-6 shadow-2xl">
            <h3 className="text-base font-bold text-white mb-2">Connect New P2P Node</h3>
            <p className="text-xs text-slate-400 mb-4">
              Register a validator, SANO sentinel, or NPAS bridge relay into your local peer discovery routing table.
            </p>
            <form onSubmit={handleAddPeerSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Node Identifier / Name</label>
                <input
                  type="text"
                  placeholder="e.g. São Paulo Gateway #02"
                  value={peerName}
                  onChange={(e) => setPeerName(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  autoFocus
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">IP & Port</label>
                <input
                  type="text"
                  placeholder="e.g. 177.18.92.11:8080"
                  value={peerIp}
                  onChange={(e) => setPeerIp(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 font-mono focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Geographic Region</label>
                <input
                  type="text"
                  placeholder="e.g. São Paulo, Brazil"
                  value={peerLocation}
                  onChange={(e) => setPeerLocation(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Node Role</label>
                <select
                  value={peerRole}
                  onChange={(e) => setPeerRole(e.target.value as PeerNode['role'])}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option value="Validator">Validator</option>
                  <option value="SANO Orchestrator">SANO Orchestrator</option>
                  <option value="NPAS Relayer">NPAS Relayer</option>
                  <option value="Archive Node">Archive Node</option>
                </select>
              </div>

              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsAddingPeer(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!peerName || !peerIp}
                  className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white disabled:opacity-50"
                >
                  Register Node
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Block Details Modal */}
      {selectedBlock && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-lg w-full p-6 shadow-2xl text-slate-100">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Layers className="w-5 h-5 text-blue-400" />
                Ledger Sequence #{selectedBlock.height}
              </h3>
              <button
                onClick={() => setSelectedBlock(null)}
                className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300"
              >
                Close
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 font-mono">
                <div className="text-[10px] text-slate-500 uppercase">Block Hash</div>
                <div className="text-blue-300 break-all">{selectedBlock.hash}</div>
              </div>

              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 font-mono">
                <div className="text-[10px] text-slate-500 uppercase">Previous Ledger Hash</div>
                <div className="text-slate-400 break-all">{selectedBlock.previousHash}</div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                  <div className="text-[10px] text-slate-500 uppercase">Validator Node</div>
                  <div className="text-slate-200 font-semibold truncate">{selectedBlock.validator}</div>
                </div>
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                  <div className="text-[10px] text-slate-500 uppercase">Transactions Confirmed</div>
                  <div className="text-emerald-400 font-mono font-bold">{selectedBlock.txCount} txs</div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                  <div className="text-[10px] text-slate-500 uppercase">Block Size</div>
                  <div className="text-slate-300 font-mono">{selectedBlock.sizeKb} KB</div>
                </div>
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                  <div className="text-[10px] text-slate-500 uppercase">Gas Consumed</div>
                  <div className="text-slate-300 font-mono">{selectedBlock.gasUsed.toLocaleString()}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
