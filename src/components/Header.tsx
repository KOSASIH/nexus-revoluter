import React from 'react';
import { ShieldCheck, Cpu, Wifi, Activity, Wallet, RefreshCw, ChevronDown, TrendingUp } from 'lucide-react';

interface HeaderProps {
  currentNetwork: string;
  onNetworkChange: (network: string) => void;
  piPrice: number;
  livePrice?: number;
  blockHeight: number;
  totalPiBalance: number;
  totalXlmBalance: number;
}

export const Header: React.FC<HeaderProps> = ({
  currentNetwork,
  onNetworkChange,
  piPrice,
  livePrice = 0.0756,
  blockHeight,
  totalPiBalance,
  totalXlmBalance
}) => {
  return (
    <header className="border-b border-slate-800 bg-slate-900/90 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Project Title */}
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-600 p-0.5 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <div className="h-full w-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                <span className="font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400 text-lg">
                  π
                </span>
              </div>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h1 className="text-lg font-bold tracking-tight text-white flex items-center gap-1.5">
                  Nexus Revoluter
                  <span className="text-[10px] font-semibold uppercase px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30">
                    SANO Monitor • NPAS v1.0
                  </span>
                </h1>
              </div>
              <p className="text-xs text-slate-400">Autonomous Pi Network & Stellar Blockchain Node</p>
            </div>
          </div>

          {/* Quick Metrics & Live Status */}
          <div className="hidden lg:flex items-center space-x-4 text-xs">
            {/* Live Market Price */}
            <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-slate-400 font-medium">Live Market:</span>
              <span className="font-mono font-bold text-white">
                ${livePrice.toFixed(4)}
              </span>
            </div>

            {/* Community GCV Target */}
            <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-purple-950/40 border border-purple-800/40 text-purple-200">
              <span className="text-purple-300 font-medium">Community GCV:</span>
              <span className="font-mono font-bold text-purple-300">
                ${piPrice.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
              </span>
            </div>

            {/* Block Height */}
            <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60">
              <Activity className="w-3.5 h-3.5 text-blue-400" />
              <span className="text-slate-400 font-medium">Block:</span>
              <span className="font-mono font-semibold text-slate-200">#{blockHeight.toLocaleString()}</span>
            </div>

            {/* Node Sync Status */}
            <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-emerald-950/40 border border-emerald-800/40 text-emerald-300">
              <Wifi className="w-3.5 h-3.5" />
              <span className="font-medium">P2P Mesh: Synced</span>
            </div>
          </div>

          {/* Right Controls: Network & Wallet Snapshot */}
          <div className="flex items-center space-x-3">
            {/* Network Selector */}
            <div className="relative">
              <select
                value={currentNetwork}
                onChange={(e) => onNetworkChange(e.target.value)}
                className="appearance-none bg-slate-800 hover:bg-slate-700/80 text-slate-200 text-xs font-medium py-1.5 pl-3 pr-8 rounded-lg border border-slate-700 cursor-pointer focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                <option value="pi-mainnet">Pi Network Mainnet (314159)</option>
                <option value="pi-testnet">Pi Network Testnet (314158)</option>
                <option value="stellar-horizon">Stellar Horizon Public</option>
              </select>
              <ChevronDown className="w-3.5 h-3.5 text-slate-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
            </div>

            {/* Wallet Snapshot Pill with correct π PI symbol */}
            <div className="hidden sm:flex items-center space-x-3 bg-gradient-to-r from-slate-800 to-slate-850 px-3 py-1.5 rounded-lg border border-slate-700/80">
              <Wallet className="w-3.5 h-3.5 text-purple-400" />
              <div className="text-right">
                <div className="text-[11px] font-mono font-bold text-white leading-tight">
                  {totalPiBalance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}{' '}
                  <span className="text-purple-400">π <span className="text-[9px] uppercase font-mono">PI</span></span>
                </div>
                <div className="text-[9px] font-mono text-slate-400 leading-tight">
                  {totalXlmBalance.toFixed(2)} XLM
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
