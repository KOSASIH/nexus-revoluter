import React, { useState, useEffect } from 'react';
import { 
  RefreshCw, 
  Cpu, 
  Database, 
  ShieldCheck, 
  Activity, 
  CheckCircle2, 
  AlertTriangle, 
  Play, 
  Pause, 
  ArrowRight, 
  Check, 
  FileCode,
  Sparkles,
  ExternalLink,
  X,
  Copy
} from 'lucide-react';
import { SyncLog } from '../types';

interface NpasViewProps {
  syncLogs: SyncLog[];
  onTriggerSync: () => void;
}

export const NpasView: React.FC<NpasViewProps> = ({
  syncLogs,
  onTriggerSync
}) => {
  const [autoSyncEnabled, setAutoSyncEnabled] = useState(true);
  const [cpuUsage, setCpuUsage] = useState(28);
  const [memoryUsage, setMemoryUsage] = useState(44);
  const [syncRate, setSyncRate] = useState(148);
  const [isSyncingNow, setIsSyncingNow] = useState(false);
  const [aiAnalysisResult, setAiAnalysisResult] = useState<string>(
    'AI Predictive Engine: Zero conflicts detected across 4 Pi Network endpoints. Invariant ledger consensus matched 100%.'
  );

  const [selectedEndpoint, setSelectedEndpoint] = useState<{
    name: string;
    url: string;
    ping: number;
    tls: string;
    merkleRoot: string;
    payload: string;
  } | null>(null);

  // Live fluctuating telemetry simulation to match npas/dashboard/dashboard.py
  useEffect(() => {
    const timer = setInterval(() => {
      setCpuUsage(prev => Math.min(85, Math.max(18, prev + (Math.random() * 8 - 4))));
      setMemoryUsage(prev => Math.min(80, Math.max(35, prev + (Math.random() * 4 - 2))));
      setSyncRate(prev => Math.floor(Math.min(220, Math.max(90, prev + (Math.random() * 16 - 8)))));
    }, 2000);
    return () => clearInterval(timer);
  }, []);

  const handleManualSync = () => {
    setIsSyncingNow(true);
    onTriggerSync();
    setTimeout(() => {
      setIsSyncingNow(false);
      setAiAnalysisResult('Autonomous sync cycle completed: Synchronized with minepi.com, wallet.pinet.com & ecosystem.pinet.com without latency delay.');
    }, 1200);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* NPAS Banner */}
      <div className="bg-gradient-to-r from-blue-950/70 via-slate-900 to-indigo-950/70 p-6 rounded-2xl border border-blue-900/40 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 rounded text-[11px] font-mono font-bold bg-blue-500/20 text-blue-300 border border-blue-500/40 uppercase">
              NPAS Core v2.1
            </span>
            <span className="text-xs text-slate-400">Autonomous Bridge</span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1">
            Nexus-Pi Autonomous Synchronizer
          </h2>
          <p className="text-xs text-slate-300 max-w-2xl mt-1 leading-relaxed">
            Continuously monitors Nexus Revoluter state, smart contracts, and token balances, seamlessly synchronizing them with official Pi Network platforms with zero manual intervention.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => setAutoSyncEnabled(!autoSyncEnabled)}
            className={`flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold border transition ${
              autoSyncEnabled
                ? 'bg-emerald-950/60 border-emerald-800 text-emerald-300'
                : 'bg-slate-800 border-slate-700 text-slate-300'
            }`}
          >
            {autoSyncEnabled ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
            <span>{autoSyncEnabled ? 'Auto-Sync: Active' : 'Auto-Sync: Paused'}</span>
          </button>

          <button
            onClick={handleManualSync}
            disabled={isSyncingNow}
            className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white shadow-lg shadow-blue-600/20 transition disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isSyncingNow ? 'animate-spin' : ''}`} />
            <span>{isSyncingNow ? 'Syncing...' : 'Sync Now'}</span>
          </button>
        </div>
      </div>

      {/* Target Pi Network Endpoints Status */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div 
          onClick={() => setSelectedEndpoint({
            name: 'minepi.com Gateway',
            url: 'https://minepi.com/api/v2/protocol-rules',
            ping: 18,
            tls: 'TLS 1.3 / ChaCha20-Poly1305',
            merkleRoot: '0x9d82f7103a8ec492ba37482910faecb891240182749102938471928374619283',
            payload: JSON.stringify({
              endpoint: "minepi.com",
              protocolVersion: "2.1.0-mainnet",
              invariantCheck: "CONSISTENT",
              syncedBlock: 4920194,
              consensusQuorum: "99.98% Healthy",
              rulesHash: "sha256:7b91c...88a"
            }, null, 2)
          })}
          className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-blue-500/50 hover:bg-slate-900/90 transition cursor-pointer group"
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-white group-hover:text-blue-300 transition">minepi.com Gateway</span>
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
          </div>
          <p className="text-[11px] text-slate-400">Main Portal & Whitepaper Protocol Rules</p>
          <div className="mt-3 flex items-center justify-between text-[11px] font-mono pt-2 border-t border-slate-800/80">
            <span className="text-emerald-400">Status: Healthy</span>
            <span className="text-blue-400 group-hover:underline">Inspect State →</span>
          </div>
        </div>

        <div 
          onClick={() => setSelectedEndpoint({
            name: 'wallet.pinet.com Bridge',
            url: 'https://wallet.pinet.com/api/v1/stellar-custody',
            ping: 24,
            tls: 'TLS 1.3 / AES-256-GCM',
            merkleRoot: '0x8c71e6092b7db381a926371809ebda7801390171638091827360817263508172',
            payload: JSON.stringify({
              endpoint: "wallet.pinet.com",
              bridgeType: "Stellar Horizon Bridge",
              accountNonceSync: "SYNCHRONIZED",
              keypairVerification: "Ed25519 Verified",
              unlockedSupply: "68,420,000 π PI",
              activeWallets: "14,890,210"
            }, null, 2)
          })}
          className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-blue-500/50 hover:bg-slate-900/90 transition cursor-pointer group"
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-white group-hover:text-blue-300 transition">wallet.pinet.com Bridge</span>
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
          </div>
          <p className="text-[11px] text-slate-400">Stellar Custodial Account Settlement</p>
          <div className="mt-3 flex items-center justify-between text-[11px] font-mono pt-2 border-t border-slate-800/80">
            <span className="text-emerald-400">Nonce: In-Sync</span>
            <span className="text-blue-400 group-hover:underline">Inspect State →</span>
          </div>
        </div>

        <div 
          onClick={() => setSelectedEndpoint({
            name: 'ecosystem.pinet.com DApps',
            url: 'https://ecosystem.pinet.com/api/v2/smart-contracts/registry',
            ping: 16,
            tls: 'TLS 1.3 / ChaCha20-Poly1305',
            merkleRoot: '0x7b60d5981a6ca2709815260798daca6790289060527980716259706152497061',
            payload: JSON.stringify({
              endpoint: "ecosystem.pinet.com",
              dAppRegistries: 420,
              verifiedContracts: ["KYCVerification.sol", "LiquidityPool.sol", "PiCoinStable.js"],
              zkProofVerifier: "0x7F2...b84",
              piSdkCompatibility: "v2.0-ready"
            }, null, 2)
          })}
          className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-blue-500/50 hover:bg-slate-900/90 transition cursor-pointer group"
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-white group-hover:text-blue-300 transition">ecosystem.pinet.com DApps</span>
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
          </div>
          <p className="text-[11px] text-slate-400">Smart Contract ABI & Metadata Relay</p>
          <div className="mt-3 flex items-center justify-between text-[11px] font-mono pt-2 border-t border-slate-800/80">
            <span className="text-emerald-400">ZK-Verified</span>
            <span className="text-blue-400 group-hover:underline">Inspect State →</span>
          </div>
        </div>
      </div>

      {/* Real-Time System Telemetry (CPU & Memory from npas/dashboard/dashboard.py) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-6 bg-slate-900/70 p-6 rounded-2xl border border-slate-800">
          <div className="flex items-center justify-between mb-5">
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Activity className="w-4 h-4 text-amber-400" />
                Real-Time NPAS Telemetry
              </h3>
              <p className="text-xs text-slate-400">Automated system load & worker thread utilization</p>
            </div>
            <span className="text-xs font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/40">
              Live Polling: 1000ms
            </span>
          </div>

          <div className="space-y-6">
            {/* CPU Bar */}
            <div>
              <div className="flex justify-between text-xs mb-1.5 font-medium">
                <span className="text-slate-300 flex items-center gap-1.5">
                  <Cpu className="w-4 h-4 text-blue-400" /> CPU Usage
                </span>
                <span className="font-mono text-blue-400 font-bold">{cpuUsage.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-slate-950 h-3 rounded-full overflow-hidden p-0.5 border border-slate-800">
                <div 
                  className="bg-gradient-to-r from-blue-500 to-indigo-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${cpuUsage}%` }}
                />
              </div>
            </div>

            {/* Memory Bar */}
            <div>
              <div className="flex justify-between text-xs mb-1.5 font-medium">
                <span className="text-slate-300 flex items-center gap-1.5">
                  <Database className="w-4 h-4 text-purple-400" /> Virtual Memory
                </span>
                <span className="font-mono text-purple-400 font-bold">{memoryUsage.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-slate-950 h-3 rounded-full overflow-hidden p-0.5 border border-slate-800">
                <div 
                  className="bg-gradient-to-r from-purple-500 to-pink-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${memoryUsage}%` }}
                />
              </div>
            </div>

            {/* Sync Throughput */}
            <div className="grid grid-cols-2 gap-3 pt-2">
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                <div className="text-[10px] text-slate-500 uppercase font-semibold">Sync Stream Rate</div>
                <div className="text-lg font-mono font-bold text-emerald-400 mt-0.5">
                  {syncRate} req/sec
                </div>
              </div>
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                <div className="text-[10px] text-slate-500 uppercase font-semibold">ZK Proof Latency</div>
                <div className="text-lg font-mono font-bold text-white mt-0.5">
                  18.4 ms
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* AI Predictive Conflict Analyzer & Verification */}
        <div className="lg:col-span-6 bg-slate-900/70 p-6 rounded-2xl border border-slate-800 flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="p-2 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
                <Sparkles className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">AI Predictive Conflict Engine</h3>
                <p className="text-xs text-slate-400">Pre-sync conflict detection and state invariant verifier</p>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800/90 text-xs text-slate-300 leading-relaxed mb-4">
              <div className="flex items-center space-x-2 text-emerald-400 font-semibold mb-2">
                <CheckCircle2 className="w-4 h-4 shrink-0" />
                <span>State Consistency Verified (Epoch 4920)</span>
              </div>
              {aiAnalysisResult}
            </div>

            <div className="space-y-2 text-xs">
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/60 border border-slate-800/70">
                <span className="text-slate-400">Pi Network Open Mainnet RPC Bridge:</span>
                <span className="font-mono text-emerald-400 font-semibold">CONNECTED</span>
              </div>
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/60 border border-slate-800/70">
                <span className="text-slate-400">Zero-Knowledge SyncVerifier.sol:</span>
                <span className="font-mono text-blue-400 font-semibold">0x7F2...b84</span>
              </div>
              <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950/60 border border-slate-800/70">
                <span className="text-slate-400">Data Integrity Checksum:</span>
                <span className="font-mono text-slate-300 font-semibold">SHA-256 (VALID)</span>
              </div>
            </div>
          </div>

          <div className="mt-5 p-3 rounded-xl bg-blue-950/30 border border-blue-900/40 text-[11px] text-blue-300 flex items-center justify-between">
            <span>NPAS Autonomous Daemon runs every 60s in the background</span>
            <span className="h-2 w-2 rounded-full bg-emerald-400" />
          </div>
        </div>
      </div>

      {/* Synchronization Audit Log */}
      <div className="bg-slate-900/70 p-6 rounded-2xl border border-slate-800">
        <h3 className="text-base font-bold text-white mb-1">Autonomous Synchronization Audit Log</h3>
        <p className="text-xs text-slate-400 mb-4">Historical verification trail stored on distributed ledger</p>

        <div className="space-y-2.5">
          {syncLogs.map((log) => (
            <div
              key={log.id}
              className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-center justify-between hover:border-slate-700 transition"
            >
              <div className="flex items-center space-x-3">
                <div className="h-8 w-8 rounded-lg bg-emerald-950 text-emerald-400 border border-emerald-800/40 flex items-center justify-center shrink-0">
                  <Check className="w-4 h-4" />
                </div>
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-bold text-white">{log.target}</span>
                    <span className="text-[10px] font-mono text-slate-400">{log.timestamp}</span>
                    {log.verifiedByZk && (
                      <span className="text-[9px] px-1.5 py-0.2 rounded bg-purple-950 text-purple-300 border border-purple-800/40 font-mono">
                        ZK-Proof
                      </span>
                    )}
                  </div>
                  <div className="text-[11px] text-slate-400 mt-0.5">{log.operation}</div>
                </div>
              </div>

              <div className="text-right shrink-0">
                <span className="text-xs font-mono font-semibold text-emerald-400">
                  {log.latencyMs} ms
                </span>
                <div className="text-[10px] text-slate-500 uppercase font-medium">Synchronized</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Endpoint Payload & Cryptographic State Inspector Modal */}
      {selectedEndpoint && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-xl w-full p-6 shadow-2xl relative text-slate-100 max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setSelectedEndpoint(null)}
              className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center space-x-3 mb-4">
              <div className="h-10 w-10 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center shrink-0">
                <FileCode className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">{selectedEndpoint.name}</h3>
                <p className="font-mono text-xs text-blue-400 break-all">{selectedEndpoint.url}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs mb-4">
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                <div className="text-[10px] text-slate-500 uppercase font-semibold">Latency / Round-Trip</div>
                <div className="text-emerald-400 font-mono font-bold mt-0.5">{selectedEndpoint.ping} ms</div>
              </div>
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                <div className="text-[10px] text-slate-500 uppercase font-semibold">TLS Protocol</div>
                <div className="text-slate-200 font-mono font-bold mt-0.5">{selectedEndpoint.tls}</div>
              </div>
            </div>

            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 mb-4">
              <div className="text-[10px] text-slate-500 uppercase font-semibold mb-1">State Merkle Root Hash</div>
              <p className="font-mono text-xs text-purple-300 break-all select-all font-semibold">
                {selectedEndpoint.merkleRoot}
              </p>
            </div>

            <div className="bg-slate-950 p-3.5 rounded-xl border border-slate-800 mb-4">
              <div className="flex items-center justify-between text-[10px] text-slate-500 uppercase font-semibold mb-1.5">
                <span>Synchronized JSON State Payload</span>
                <span className="text-emerald-400">HTTP/2 200 OK</span>
              </div>
              <pre className="text-xs font-mono text-slate-200 bg-slate-900/90 p-3 rounded-lg overflow-x-auto border border-slate-800/80">
                {selectedEndpoint.payload}
              </pre>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setSelectedEndpoint(null)}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300 transition"
              >
                Close Inspector
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
