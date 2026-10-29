import React from 'react';
import { 
  Wallet, 
  Send,
  Radio, 
  GitBranch,
  ShieldCheck, 
  Sliders, 
  Vote, 
  Landmark,
  ShieldAlert
} from 'lucide-react';
import { NavTab } from '../types';

interface NavigationProps {
  activeTab: NavTab;
  onTabChange: (tab: NavTab) => void;
}

export const Navigation: React.FC<NavigationProps> = ({
  activeTab,
  onTabChange
}) => {
  const tabs = [
    {
      id: 'vault' as NavTab,
      label: 'Pioneer Vault',
      icon: Wallet,
      badge: null
    },
    {
      id: 'transaction' as NavTab,
      label: 'Execute IOU',
      icon: Send,
      badge: null
    },
    {
      id: 'p2p' as NavTab,
      label: 'P2P Gossip & SCP',
      icon: Radio,
      badge: '5 Sentinels'
    },
    {
      id: 'bridge' as NavTab,
      label: 'NPAS Bridge',
      icon: GitBranch,
      badge: 'MPC 3/5'
    },
    {
      id: 'zk-compliance' as NavTab,
      label: 'ZK Compliance',
      icon: ShieldCheck,
      badge: 'Verified'
    },
    {
      id: 'sano' as NavTab,
      label: 'SANO Target Monitor',
      icon: Sliders,
      badge: 'Read-Only'
    },
    {
      id: 'dao' as NavTab,
      label: 'Pioneer DAO',
      icon: Vote,
      badge: '3 Active'
    },
    {
      id: 'treasury' as NavTab,
      label: 'Transparent Treasury',
      icon: Landmark,
      badge: 'Immutable'
    },
    {
      id: 'guard' as NavTab,
      label: 'AI Sentinel & Legal',
      icon: ShieldAlert,
      badge: '24h Shield'
    }
  ];

  return (
    <nav className="border-b border-slate-800 bg-slate-900/60 sticky top-[89px] z-30 overflow-x-auto scrollbar-none">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex space-x-1 sm:space-x-1.5 py-2">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;

            return (
              <button
                key={tab.id}
                onClick={() => onTabChange(tab.id)}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-xs font-semibold whitespace-nowrap transition-all duration-150 relative ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/80'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{tab.label}</span>
                {tab.badge && (
                  <span
                    className={`ml-1.5 px-1.5 py-0.5 text-[9px] font-mono rounded-full font-bold uppercase ${
                      isActive
                        ? 'bg-blue-700 text-blue-100'
                        : tab.badge === 'Verified' || tab.badge === '3 Active'
                        ? 'bg-emerald-950 text-emerald-300 border border-emerald-800/50'
                        : 'bg-slate-800 text-slate-400 border border-slate-700'
                    }`}
                  >
                    {tab.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>
    </nav>
  );
};
