import React from 'react';
import { 
  Wallet, 
  Layers, 
  RefreshCw, 
  Sliders, 
  Cpu, 
  Vote, 
  ShieldCheck 
} from 'lucide-react';
import { NavTab } from '../types';

interface NavigationProps {
  activeTab: NavTab;
  onTabChange: (tab: NavTab) => void;
  syncBadgeCount?: number;
}

export const Navigation: React.FC<NavigationProps> = ({
  activeTab,
  onTabChange,
  syncBadgeCount = 0
}) => {
  const tabs = [
    {
      id: 'wallet' as NavTab,
      label: 'Pioneer Wallet',
      icon: Wallet,
      badge: null
    },
    {
      id: 'node' as NavTab,
      label: 'Nexus Node & Explorer',
      icon: Layers,
      badge: 'Live'
    },
    {
      id: 'npas' as NavTab,
      label: 'NPAS Synchronizer',
      icon: RefreshCw,
      badge: syncBadgeCount > 0 ? `${syncBadgeCount} auto` : 'Auto'
    },
    {
      id: 'sano' as NavTab,
      label: 'SANO Target Monitor',
      icon: Sliders,
      badge: 'GCV Monitor'
    },
    {
      id: 'assets-iot' as NavTab,
      label: 'IoT & Tokenized Assets',
      icon: Cpu,
      badge: null
    },
    {
      id: 'governance' as NavTab,
      label: 'Pioneer DAO',
      icon: Vote,
      badge: '3 Active'
    },
    {
      id: 'compliance' as NavTab,
      label: 'ZK Compliance',
      icon: ShieldCheck,
      badge: 'Verified'
    }
  ];

  return (
    <nav className="border-b border-slate-800 bg-slate-900/60 sticky top-16 z-30 overflow-x-auto scrollbar-none">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex space-x-1 sm:space-x-2 py-2">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;

            return (
              <button
                key={tab.id}
                onClick={() => onTabChange(tab.id)}
                className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-xs font-semibold whitespace-nowrap transition-all duration-150 relative ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30 font-medium'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/80'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{tab.label}</span>
                {tab.badge && (
                  <span
                    className={`ml-1.5 px-1.5 py-0.5 text-[10px] rounded-full font-mono ${
                      isActive
                        ? 'bg-blue-700 text-blue-100'
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
