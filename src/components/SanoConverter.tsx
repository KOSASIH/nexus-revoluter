import React, { useState } from 'react';
import { Calculator, ArrowRightLeft, ShoppingBag, Coffee, Smartphone, Sun, Car, Home, Info, Sparkles } from 'lucide-react';

interface SanoConverterProps {
  livePrice: number;
  communityGcv: number;
}

export const SanoConverter: React.FC<SanoConverterProps> = ({ livePrice, communityGcv }) => {
  const [piAmount, setPiAmount] = useState<string>('10');
  const [customGoodPrice, setCustomGoodPrice] = useState<number>(1200);

  const numPi = parseFloat(piAmount) || 0;
  const marketUsd = numPi * livePrice;
  const gcvUsd = numPi * communityGcv;
  const xlmEquivalent = (numPi * livePrice) / 0.14; // assuming XLM ~$0.14

  const PRESET_GOODS = [
    { name: 'Specialty Coffee', priceUsd: 4.5, icon: Coffee, category: 'Micro Barter' },
    { name: 'Flagship Smartphone', priceUsd: 1200, icon: Smartphone, category: 'Electronics' },
    { name: 'Solar Inverter Kit (5kW)', priceUsd: 4800, icon: Sun, category: 'Clean Energy' },
    { name: 'Electric Vehicle (EV)', priceUsd: 38000, icon: Car, category: 'Transport' },
    { name: 'Pioneer Eco-Apartment', priceUsd: 157000, icon: Home, category: 'Real Estate' },
  ];

  return (
    <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Calculator className="w-5 h-5 text-blue-400" />
            Interactive $\pi\text{ PI}$ Valuation & Barter Calculator
          </h3>
          <p className="text-xs text-slate-400">
            Real-time mathematical simulator contrasting live market exchange rates vs. Community GCV purchasing power
          </p>
        </div>

        <span className="text-[11px] font-mono px-2.5 py-1 rounded-lg bg-blue-950 text-blue-300 border border-blue-800/40">
          Formula: 1 π PI = ${livePrice.toFixed(4)} MKT | ${communityGcv.toLocaleString()} GCV
        </span>
      </div>

      {/* Calculator Input & Conversions Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Input */}
        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
          <label className="text-[10px] uppercase font-bold text-slate-400 flex items-center justify-between">
            <span>Enter π PI Amount</span>
            <span className="text-purple-400">π PI</span>
          </label>
          <input
            type="number"
            step="any"
            value={piAmount}
            onChange={(e) => setPiAmount(e.target.value)}
            className="w-full bg-transparent text-xl font-mono font-bold text-white focus:outline-none placeholder-slate-600"
            placeholder="0.00"
          />
          <div className="text-[10px] text-slate-500">Pioneer Balance Unit</div>
        </div>

        {/* Live Market Value */}
        <div className="p-4 rounded-xl bg-slate-950 border border-blue-900/40 space-y-1">
          <div className="text-[10px] uppercase font-bold text-blue-400">Live Market Valuation</div>
          <div className="text-xl font-mono font-bold text-white">
            ${marketUsd.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 4 })}
          </div>
          <div className="text-[10px] text-slate-500 font-mono">Rate: ${livePrice.toFixed(4)} / π PI</div>
        </div>

        {/* GCV Community Value */}
        <div className="p-4 rounded-xl bg-slate-950 border border-purple-900/40 space-y-1">
          <div className="text-[10px] uppercase font-bold text-purple-400">Community GCV Valuation</div>
          <div className="text-xl font-mono font-bold text-purple-300">
            ${gcvUsd.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
          </div>
          <div className="text-[10px] text-slate-500 font-mono">Target: ${communityGcv.toLocaleString()} / π PI</div>
        </div>

        {/* XLM Native Equivalent */}
        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
          <div className="text-[10px] uppercase font-bold text-slate-400">Stellar Horizon (XLM)</div>
          <div className="text-xl font-mono font-bold text-slate-200">
            {xlmEquivalent.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} XLM
          </div>
          <div className="text-[10px] text-slate-500 font-mono">P2P Bridge Equivalent</div>
        </div>
      </div>

      {/* Real-World Goods Barter Matrix */}
      <div className="pt-2">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-3 flex items-center gap-1.5">
          <ShoppingBag className="w-4 h-4 text-emerald-400" />
          Real-World Goods Barter Comparison Matrix
        </h4>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          {PRESET_GOODS.map((item) => {
            const Icon = item.icon;
            const piMarket = item.priceUsd / (livePrice || 0.0756);
            const piGcv = item.priceUsd / communityGcv;

            return (
              <div
                key={item.name}
                className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <div className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-blue-400">
                      <Icon className="w-4 h-4" />
                    </div>
                    <span className="text-[10px] text-slate-500 font-medium">{item.category}</span>
                  </div>
                  <div className="text-xs font-bold text-white line-clamp-1">{item.name}</div>
                  <div className="text-[11px] font-mono text-slate-400">${item.priceUsd.toLocaleString()} USD</div>
                </div>

                <div className="mt-3 pt-2.5 border-t border-slate-800/80 space-y-1.5 font-mono text-[11px]">
                  <div>
                    <span className="text-[9px] uppercase text-slate-500 block">At Market Price:</span>
                    <span className="text-white font-semibold">
                      {piMarket >= 1000 ? (piMarket / 1000).toFixed(1) + 'k' : piMarket.toFixed(2)} π PI
                    </span>
                  </div>
                  <div>
                    <span className="text-[9px] uppercase text-purple-400 block">At Community GCV:</span>
                    <span className="text-purple-300 font-bold">
                      {piGcv < 0.001 ? piGcv.toFixed(6) : piGcv.toFixed(4)} π PI
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
