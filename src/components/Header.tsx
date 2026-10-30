import React from 'react';
import { Activity, Wallet, ChevronDown, AlertTriangle, Flame } from 'lucide-react';

interface HeaderProps {
  currentNetwork: string;
  onNetworkChange: (network: string) => void;
  piPrice?: number;
  livePrice?: number;
  blockHeight: number;
  totalPiBalance: number;
  totalXlmBalance: number;
}

export const Header: React.FC<HeaderProps> = ({
  currentNetwork,
  onNetworkChange,
  livePrice = 0.1142,
  blockHeight,
  totalPiBalance,
  totalXlmBalance
}) => {
  return (
    <>
      {/* Automatic Trademark Firewall Banner on every page */}
      <div className="bg-amber-500/10 border-b border-amber-500/20 px-4 py-1.5 text-center text-[11px] text-amber-300 font-medium flex items-center justify-center gap-1.5">
        <AlertTriangle className="w-3.5 h-3.5 text-amber-400 shrink-0" />
        <span>
          <strong>Trademark Firewall:</strong> Independent community project, not affiliated with Pi Core Team, Stellar Development Foundation, or any L1 team. All assets are sovereign or legacy IOU, not native mainnet coins.
        </span>
      </div>

      <header className="border-b border-slate-800 bg-slate-900/90 backdrop-blur-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo & Subtitle */}
            <div className="flex items-center space-x-3">
              <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-600 p-0.5 flex items-center justify-center shadow-lg shadow-blue-500/20">
                <div className="h-full w-full bg-slate-950 rounded-[10px] flex items-center justify-center font-bold text-white text-base">
                  NR
                </div>
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <h1 className="text-base sm:text-lg font-bold tracking-tight text-white flex items-center gap-1.5">
                    Nexus Revoluter
                    <span className="text-[10px] font-mono font-semibold uppercase px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30">
                      SOVEREIGN MONITOR • NPAS V2.0
                    </span>
                  </h1>
                </div>
                <p className="text-xs text-slate-400">Autonomous Stellar & Sovereign Nexus Infrastructure Node</p>
              </div>
            </div>

            {/* Quick Metrics */}
            <div className="hidden lg:flex items-center space-x-4 text-xs">
              {/* Live Stellar XLM Price */}
              <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60">
                <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
                <span className="text-slate-400 font-medium">Stellar XLM:</span>
                <span className="font-mono font-bold text-white">
                  ${livePrice.toFixed(4)}
                </span>
              </div>

              {/* Q-Thermo Floor */}
              <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-amber-950/40 border border-amber-800/40 text-amber-200">
                <Flame className="w-3.5 h-3.5 text-amber-400" />
                <span className="text-amber-300 font-medium">Q-Thermo Floor:</span>
                <span className="font-mono font-bold text-amber-300">
                  3.14159 kWh / π NXS
                </span>
              </div>

              {/* Block Height */}
              <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60">
                <Activity className="w-3.5 h-3.5 text-blue-400" />
                <span className="text-slate-400 font-medium">Slot:</span>
                <span className="font-mono font-semibold text-slate-200">#{blockHeight.toLocaleString()}</span>
              </div>
            </div>

            {/* Right Controls: Dropdown & Vault Total */}
            <div className="flex items-center space-x-3">
              {/* Top right dropdown: Nexus Ledger (Sovereign) */}
              <div className="relative">
                <select
                  value={currentNetwork}
                  onChange={(e) => onNetworkChange(e.target.value)}
                  className="appearance-none bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium py-1.5 pl-3 pr-8 rounded-lg border border-slate-700 cursor-pointer focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option value="nexus-ledger">Nexus Ledger (Sovereign)</option>
                  <option value="stellar-horizon">Stellar Horizon Public</option>
                  <option value="community-testnet">Community Testnet</option>
                </select>
                <ChevronDown className="w-3.5 h-3.5 text-slate-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
              </div>

              {/* Balance Total with π NXS symbol */}
              <div className="hidden sm:flex items-center space-x-3 bg-gradient-to-r from-slate-800 to-slate-850 px-3 py-1.5 rounded-lg border border-slate-700/80">
                <Wallet className="w-3.5 h-3.5 text-purple-400" />
                <div className="text-right">
                  <div className="text-[11px] font-mono font-bold text-white leading-tight">
                    {totalPiBalance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}{' '}
                    <span className="text-purple-400 font-bold">π NXS</span>
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
    </>
  );
};
