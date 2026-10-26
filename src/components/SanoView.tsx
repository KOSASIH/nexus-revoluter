import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  TrendingUp, 
  Info, 
  ExternalLink, 
  RefreshCw, 
  ShieldCheck, 
  BarChart3, 
  Layers, 
  Globe2,
  Clock,
  Sparkles,
  AlertCircle
} from 'lucide-react';

import { SanoConverter } from './SanoConverter';

interface SanoViewProps {
  livePrice: number;
  communityGcv: number;
  onRefreshPrice?: () => void;
  isPriceLoading?: boolean;
}

export const SanoView: React.FC<SanoViewProps> = ({
  livePrice = 0.0756,
  communityGcv = 314159.00,
  onRefreshPrice,
  isPriceLoading = false
}) => {
  const [lastUpdated, setLastUpdated] = useState<string>('Just now');
  const [activeTab, setActiveTab] = useState<'overview' | 'comparison' | 'community'>('overview');

  useEffect(() => {
    setLastUpdated(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
  }, [livePrice]);

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* SANO Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 rounded text-[11px] font-mono font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30 uppercase">
              SANO v1.0 • Read-Only
            </span>
            <span className="text-xs text-slate-400">Target Monitoring Console</span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1.5 flex items-center gap-2">
            SANO Target Monitor
          </h2>
          <p className="text-xs text-slate-300 max-w-2xl mt-1 leading-relaxed">
            Real-time analytics and valuation monitoring console. Observes secondary market price indices in parallel with the decentralized Pioneer Community Global Consensus Value (GCV).
          </p>
        </div>

        {/* Tab Controls & Refresh */}
        <div className="flex items-center space-x-2">
          <div className="bg-slate-950/80 p-1 rounded-xl border border-slate-800 flex text-xs">
            {(['overview', 'comparison', 'community'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-3 py-1.5 rounded-lg font-semibold capitalize transition ${
                  activeTab === tab
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {tab === 'overview' ? 'Market Overview' : tab === 'comparison' ? 'Valuation Index' : 'GCV Context'}
              </button>
            ))}
          </div>

          {onRefreshPrice && (
            <button
              onClick={onRefreshPrice}
              disabled={isPriceLoading}
              title="Refresh live price feeds"
              className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${isPriceLoading ? 'animate-spin text-blue-400' : ''}`} />
            </button>
          )}
        </div>
      </div>

      {/* Primary Section: Dual Price Display */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Left Card: Live Market Price */}
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800/90 shadow-xl relative overflow-hidden flex flex-col justify-between">
          <div className="absolute top-0 right-0 w-48 h-48 bg-blue-500/5 rounded-full blur-3xl pointer-events-none" />

          <div>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <span className="h-2.5 w-2.5 rounded-full bg-emerald-400 animate-pulse" />
                <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300">
                  Live Market Price
                </h3>
              </div>
              <span className="text-[10px] font-mono text-slate-400 flex items-center gap-1 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
                <Clock className="w-3 h-3 text-slate-500" />
                Updated: {lastUpdated}
              </span>
            </div>

            <div className="mt-2 flex items-baseline space-x-3">
              <span className="text-4xl sm:text-5xl font-mono font-black text-white tracking-tight">
                ${livePrice.toFixed(4)}
              </span>
              <span className="text-xs font-mono font-bold text-slate-400">
                USD / <span className="text-blue-400">π PI</span>
              </span>
            </div>

            <div className="flex items-center space-x-2 mt-3 text-xs">
              <span className="text-emerald-400 font-mono font-semibold flex items-center">
                <TrendingUp className="w-3.5 h-3.5 mr-1" /> +2.48% (24h)
              </span>
              <span className="text-slate-500">•</span>
              <span className="text-slate-400 font-mono">
                24h Vol: ~$1.42M USD
              </span>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span className="flex items-center gap-1.5">
              <Activity className="w-3.5 h-3.5 text-blue-400" />
              Aggregated secondary market price index
            </span>
            <span className="font-mono text-slate-500">Source: Live Oracle Feed</span>
          </div>
        </div>

        {/* Right Card: Community GCV Target */}
        <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900/90 via-purple-950/20 to-slate-900/90 border border-purple-900/40 shadow-xl relative overflow-hidden flex flex-col justify-between">
          <div className="absolute top-0 right-0 w-48 h-48 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />

          <div>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <span className="h-2.5 w-2.5 rounded-full bg-purple-400" />
                <h3 className="text-sm font-bold uppercase tracking-wider text-purple-200">
                  Community GCV Target
                </h3>
              </div>
              <span className="text-[10px] font-mono font-bold text-purple-300 bg-purple-950/60 px-2 py-0.5 rounded border border-purple-800/40">
                GCV Consensus
              </span>
            </div>

            <div className="mt-2 flex items-baseline space-x-3">
              <span className="text-4xl sm:text-5xl font-mono font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-300 via-pink-300 to-indigo-200 tracking-tight">
                ${communityGcv.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </span>
              <span className="text-xs font-mono font-bold text-slate-400">
                USD / <span className="text-purple-400">π PI</span>
              </span>
            </div>

            {/* Required prominent label */}
            <div className="mt-3 inline-flex items-center space-x-1.5 px-3 py-1 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-semibold">
              <Info className="w-3.5 h-3.5 shrink-0" />
              <span>Target komunitas, bukan harga pasar</span>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-purple-900/30 flex items-center justify-between text-[11px] text-slate-400">
            <span className="text-purple-300/80">
              Pioneer community valuation standard for ecosystem barter
            </span>
            <span className="font-mono text-purple-400/80">π = 314,159</span>
          </div>
        </div>
      </div>

      {/* SANO Interactive Valuation & Barter Calculator */}
      <SanoConverter livePrice={livePrice} communityGcv={communityGcv} />

      {/* Tab Content 1: Overview */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium mb-1">Circulating Supply (Est.)</div>
            <div className="text-xl font-mono font-bold text-white">
              68,420,000 <span className="text-sm font-normal text-purple-400">π PI</span>
            </div>
            <div className="text-[11px] text-slate-500 mt-1">Unlocked Pioneer Wallets</div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium mb-1">Market Cap @ Live Price</div>
            <div className="text-xl font-mono font-bold text-blue-400">
              ${(68420000 * livePrice).toLocaleString('en-US', { maximumFractionDigits: 0 })} USD
            </div>
            <div className="text-[11px] text-slate-500 mt-1">Based on ${livePrice.toFixed(4)}</div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium mb-1">Community Ecosystem Nodes</div>
            <div className="text-xl font-mono font-bold text-emerald-400">
              240,000+
            </div>
            <div className="text-[11px] text-slate-500 mt-1">Active Global Test/Mainnet Nodes</div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium mb-1">Monitoring Mode</div>
            <div className="text-xl font-mono font-bold text-purple-400">
              Read-Only
            </div>
            <div className="text-[11px] text-slate-500 mt-1">Zero auto-execution logic</div>
          </div>
        </div>
      )}

      {/* Tab Content 2: Valuation Index */}
      {activeTab === 'comparison' && (
        <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-5">
          <div>
            <h3 className="text-base font-bold text-white mb-1">Market Price vs. Community GCV Benchmark</h3>
            <p className="text-xs text-slate-400">
              Side-by-side analytical comparison of market-driven exchange pricing and the community consensus valuation.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
              <div className="text-xs font-bold text-blue-400 uppercase">Live Secondary Market Pricing</div>
              <div className="text-2xl font-mono font-bold text-white">${livePrice.toFixed(4)} USD</div>
              <p className="text-xs text-slate-400 leading-relaxed">
                Determined by buyers and sellers on global cryptocurrency exchange platforms according to available liquidity, trading pairs, and order book depth.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
              <div className="text-xs font-bold text-purple-400 uppercase">Community Global Consensus Value (GCV)</div>
              <div className="text-2xl font-mono font-bold text-purple-300">${communityGcv.toLocaleString()} USD</div>
              <p className="text-xs text-slate-400 leading-relaxed">
                A consensus benchmark recognized by Pioneer communities worldwide for peer-to-peer commerce, goods exchange, and internal ecosystem barter valuation.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Tab Content 3: Community GCV Context */}
      {activeTab === 'community' && (
        <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-4">
          <div className="flex items-center space-x-2 text-purple-400">
            <Sparkles className="w-5 h-5" />
            <h3 className="text-base font-bold text-white">Understanding the Global Consensus Value (GCV)</h3>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            The $314,159.00 USD value (derived from the mathematical constant π ≈ 3.14159) is an aspirational valuation model championed by Pi Network Pioneers across Southeast Asia, Africa, Europe, and the Americas. It is utilized in grassroots merchant networks for pricing goods and services in <span className="font-semibold text-white">π PI</span>.
          </p>
          <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-slate-400 space-y-1">
            <div className="font-semibold text-slate-200">Key Distinctions:</div>
            <div>• Market price fluctuates based on open order books and external liquidity.</div>
            <div>• GCV is voluntary agreement among participating merchants and pioneers during ecosystem barter.</div>
            <div>• SANO serves strictly as a transparent monitoring tool to view both figures side-by-side.</div>
          </div>
        </div>
      )}

      {/* Mandatory Disclaimer Text at Bottom */}
      <div className="p-4 rounded-xl bg-slate-950/90 border border-slate-800/80 flex items-center space-x-3 text-xs text-slate-400 shadow-inner">
        <AlertCircle className="w-4 h-4 text-slate-400 shrink-0" />
        <span className="font-medium">
          Disclaimer: <strong className="text-slate-300">SANO is a monitoring dashboard, not a peg mechanism.</strong>
        </span>
      </div>
    </div>
  );
};
