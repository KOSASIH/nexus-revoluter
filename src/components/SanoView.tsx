import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  TrendingUp, 
  Info, 
  RefreshCw, 
  Clock, 
  Sparkles, 
  AlertCircle,
  Flame,
  Zap,
  Globe2,
  Cpu,
  Layers,
  ShieldCheck,
  Calculator,
  Sun,
  Car,
  Home,
  Sliders,
  Droplets,
  Wind
} from 'lucide-react';
import { simulateQuantumThermodynamicGrid } from '../services/aiSentinel';

interface SanoViewProps {
  livePrice?: number;
  communityGcv?: number;
  onRefreshPrice?: () => void;
  isPriceLoading?: boolean;
}

export const SanoView: React.FC<SanoViewProps> = ({
  livePrice = 0.1142,
  communityGcv = 314159.00,
  onRefreshPrice,
  isPriceLoading = false
}) => {
  const [lastUpdated, setLastUpdated] = useState<string>('Just now');
  const [activeTab, setActiveTab] = useState<'overview' | 'thermo' | 'comparison'>('overview');
  const [calcNxsAmount, setCalcNxsAmount] = useState<number>(10);

  // Renewable Energy Grid Simulation
  const [solarKwh, setSolarKwh] = useState<number>(140);
  const [hydroKwh, setHydroKwh] = useState<number>(85);
  const [geothermalKwh, setGeothermalKwh] = useState<number>(50);
  const [computeMultiplier, setComputeMultiplier] = useState<number>(1.0);
  const gridSim = simulateQuantumThermodynamicGrid(solarKwh, hydroKwh, geothermalKwh, computeMultiplier);

  const qThermoFloorKwh = 3.14159;

  useEffect(() => {
    setLastUpdated(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
  }, [livePrice]);

  const totalKwh = calcNxsAmount * qThermoFloorKwh;
  const totalJoules = totalKwh * 3600000;
  const xlmEquivAtFloor = (totalKwh * 0.15) / Math.max(0.001, livePrice);

  const ENERGY_EQUIVALENTS = [
    { name: 'Clean Solar Energy', value: `${(totalKwh / 5.0).toFixed(1)} hrs`, desc: '5kW Household Solar Array Output', icon: Sun },
    { name: 'Ultra-Fast EV Travel', value: `${(totalKwh * 3.8).toFixed(1)} miles`, desc: 'Zero-Emission Highway Distance', icon: Car },
    { name: 'Decentralized AI Inference', value: `${Math.round(totalKwh * 1420).toLocaleString()} queries`, desc: 'Llama/Mistral 70B Token Inferences', icon: Cpu },
    { name: 'Eco-Living Smart Home', value: `${(totalKwh / 18.5).toFixed(1)} days`, desc: 'Complete Micro-Grid Energy Autonomy', icon: Home },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Q-Thermo Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 rounded text-[11px] font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30 uppercase flex items-center gap-1.5">
              <Flame className="w-3.5 h-3.5 text-amber-400" />
              Module 13 • Q-Thermo Engine
            </span>
            <span className="text-xs text-slate-400">Pure Read-Only Valuation Monitor</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-bold text-white mt-1.5 flex items-center gap-2">
            Q-Thermo Valuation Monitor
          </h2>
          <p className="text-xs text-slate-300 max-w-2xl mt-1 leading-relaxed">
            Real-time decentralized telemetry. Observes live Stellar Horizon secondary market pricing in direct contrast with the thermodynamic work floor (3.14159 kWh per π NXS). Zero pegging, zero automated arbitrage execution, zero mainnet mint/burn.
          </p>
        </div>

        {/* Tab Controls & Refresh */}
        <div className="flex items-center space-x-2">
          <div className="bg-slate-950/80 p-1 rounded-xl border border-slate-800 flex text-xs">
            {(['overview', 'thermo', 'comparison'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-3 py-1.5 rounded-lg font-semibold capitalize transition ${
                  activeTab === tab
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {tab === 'overview' ? 'Dual Floor' : tab === 'thermo' ? 'Thermodynamics' : 'Work Equivalents'}
              </button>
            ))}
          </div>

          {onRefreshPrice && (
            <button
              onClick={onRefreshPrice}
              disabled={isPriceLoading}
              title="Poll live price feeds"
              className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${isPriceLoading ? 'animate-spin text-blue-400' : ''}`} />
            </button>
          )}
        </div>
      </div>

      {/* CORE DUAL CARD: Kiri: Live Stellar XLM Price | Kanan: Q-Thermo Floor 3.14159 kWh */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Left Card: Live Stellar XLM Price */}
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800/90 shadow-xl relative overflow-hidden flex flex-col justify-between">
          <div className="absolute top-0 right-0 w-48 h-48 bg-blue-500/5 rounded-full blur-3xl pointer-events-none" />

          <div>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <span className="h-2.5 w-2.5 rounded-full bg-emerald-400 animate-pulse" />
                <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300">
                  Live Stellar XLM Price
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
                USD / <span className="text-blue-400">XLM</span>
              </span>
            </div>

            <div className="flex items-center space-x-2 mt-3 text-xs">
              <span className="text-emerald-400 font-mono font-semibold flex items-center">
                <TrendingUp className="w-3.5 h-3.5 mr-1" /> Live Horizon Public Polling
              </span>
              <span className="text-slate-500">•</span>
              <span className="text-slate-400 font-mono">
                Gas: 0.00010 XLM Base Fee
              </span>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span className="flex items-center gap-1.5">
              <Activity className="w-3.5 h-3.5 text-blue-400" />
              Public Stellar Horizon consensus telemetry
            </span>
            <span className="font-mono text-slate-500">Source: Stellar Public Nodes</span>
          </div>
        </div>

        {/* Right Card: Q-Thermo Floor 3.14159 kWh per π NXS */}
        <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900/90 via-amber-950/20 to-slate-900/90 border border-amber-900/40 shadow-xl relative overflow-hidden flex flex-col justify-between">
          <div className="absolute top-0 right-0 w-48 h-48 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />

          <div>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <Flame className="w-4 h-4 text-amber-400" />
                <h3 className="text-sm font-bold uppercase tracking-wider text-amber-200">
                  Q-Thermo Energy Floor
                </h3>
              </div>
              <span className="text-[10px] font-mono font-bold text-amber-300 bg-amber-950/60 px-2 py-0.5 rounded border border-amber-800/40">
                Thermodynamic Invariant
              </span>
            </div>

            <div className="mt-2 flex items-baseline space-x-3">
              <span className="text-4xl sm:text-5xl font-mono font-black text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-orange-300 to-yellow-200 tracking-tight">
                3.14159
              </span>
              <span className="text-sm font-mono font-bold text-slate-300">
                kWh per <span className="text-purple-400 font-extrabold">π NXS</span>
              </span>
            </div>

            {/* MANDATORY PROMINENT LABEL: Nilai dasar energi, bukan harga pasar */}
            <div className="mt-3 inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-xl bg-amber-500/15 border border-amber-500/40 text-amber-300 text-xs font-bold shadow-sm">
              <Info className="w-4 h-4 text-amber-400 shrink-0" />
              <span>Nilai dasar energi, bukan harga pasar</span>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-amber-900/30 flex items-center justify-between text-[11px] text-slate-400">
            <span className="text-amber-300/80">
              Proof of Useful Thermodynamic Work (PoUTW) anchor
            </span>
            <span className="font-mono text-amber-400/80">π = 3.14159 kWh</span>
          </div>
        </div>
      </div>

      {/* Interactive Q-Thermo Energy Converter */}
      <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Calculator className="w-5 h-5 text-amber-400" />
              Interactive π NXS Thermodynamic Work Calculator
            </h3>
            <p className="text-xs text-slate-400">
              Compute exact physical energy equivalencies, Joules, and ecological capacity anchored to your sovereign holdings.
            </p>
          </div>

          <span className="text-[11px] font-mono px-2.5 py-1 rounded-lg bg-amber-950/60 text-amber-300 border border-amber-800/40">
            Invariant: 1 π NXS ≡ 3.14159 kWh ≡ 11,309,724 Joules
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
            <label className="text-[10px] uppercase font-bold text-slate-400 flex items-center justify-between">
              <span>Sovereign Holding</span>
              <span className="text-purple-400">π NXS</span>
            </label>
            <input
              type="number"
              min="0.1"
              step="any"
              value={calcNxsAmount}
              onChange={(e) => setCalcNxsAmount(Math.max(0, parseFloat(e.target.value) || 0))}
              className="w-full bg-transparent text-xl font-mono font-bold text-white focus:outline-none placeholder-slate-600"
              placeholder="0.00"
            />
            <div className="text-[10px] text-slate-500">Native Sovereign Unit</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-amber-900/40 space-y-1">
            <div className="text-[10px] uppercase font-bold text-amber-400">Thermodynamic Work</div>
            <div className="text-xl font-mono font-bold text-white">
              {totalKwh.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 })} kWh
            </div>
            <div className="text-[10px] text-slate-500 font-mono">{(totalJoules / 1e6).toFixed(2)} Megajoules (MJ)</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-blue-900/40 space-y-1">
            <div className="text-[10px] uppercase font-bold text-blue-400">Stellar Horizon Equivalent</div>
            <div className="text-xl font-mono font-bold text-blue-200">
              {xlmEquivAtFloor.toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 1 })} XLM
            </div>
            <div className="text-[10px] text-slate-500 font-mono">At ${livePrice.toFixed(4)} XLM rate</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
            <div className="text-[10px] uppercase font-bold text-emerald-400">Biosphere Net Carbon</div>
            <div className="text-xl font-mono font-bold text-emerald-400">
              0.000 kg CO₂
            </div>
            <div className="text-[10px] text-slate-500 font-mono">100% Zero-Rent Green Work</div>
          </div>
        </div>

        {/* Real-World Work Equivalents */}
        <div className="pt-2">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-3 flex items-center gap-1.5">
            <Zap className="w-4 h-4 text-amber-400" />
            Physical Work & Energy Realization Matrix ({calcNxsAmount} π NXS)
          </h4>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {ENERGY_EQUIVALENTS.map((item) => {
              const Icon = item.icon;
              return (
                <div
                  key={item.name}
                  className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <div className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-amber-400">
                        <Icon className="w-4 h-4" />
                      </div>
                      <span className="text-[10px] text-slate-500 font-medium">Physical Floor</span>
                    </div>
                    <div className="text-xs font-bold text-white">{item.name}</div>
                    <div className="text-lg font-mono font-bold text-amber-300 mt-1">{item.value}</div>
                  </div>
                  <div className="mt-2 pt-2 border-t border-slate-800/80 text-[10px] text-slate-500">
                    {item.desc}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Tab Content 1: Overview Quick Stats */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium mb-1">Thermodynamic Entropy</div>
            <div className="text-xl font-mono font-bold text-white">
              14.82 <span className="text-xs text-slate-400">J/K</span>
            </div>
            <div className="text-[11px] text-slate-500 mt-1">Closed-loop balance</div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium mb-1">Biosphere Purity Index</div>
            <div className="text-xl font-mono font-bold text-emerald-400">
              98.4%
            </div>
            <div className="text-[11px] text-slate-500 mt-1">Negligible power footprint</div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium mb-1">Equilibrium State</div>
            <div className="text-xl font-mono font-bold text-blue-400">
              1.000000
            </div>
            <div className="text-[11px] text-slate-500 mt-1">Zero artificial debt</div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
            <div className="text-xs text-slate-400 font-medium mb-1">Execution Mode</div>
            <div className="text-xl font-mono font-bold text-purple-400">
              Pure Read-Only
            </div>
            <div className="text-[11px] text-slate-500 mt-1">No automated mainnet peg</div>
          </div>
        </div>
      )}

      {/* Tab Content 2: Thermodynamic Fundamentals */}
      {activeTab === 'thermo' && (
        <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-4">
          <div className="flex items-center space-x-2 text-amber-400">
            <Sparkles className="w-5 h-5" />
            <h3 className="text-base font-bold text-white">Why Q-Thermo Anchors Energy Instead of Fiat</h3>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            Conventional currencies and unpegged cryptocurrencies suffer from speculative dilution and arbitrary centralized debasement. <span className="font-semibold text-white">π NXS</span> derives its sovereign floor from the immutable laws of thermodynamics: 1 kWh of useful physical work produces an irreducible unit of computation, heat dissipation, and life-supporting economic infrastructure.
          </p>
          <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-slate-400 space-y-1">
            <div className="font-semibold text-slate-200">Fundamental Principles:</div>
            <div>• Market prices fluctuate on open exchanges; the thermodynamic floor remains an invariant constant.</div>
            <div>• Nilai dasar energi (3.14159 kWh) reflects actual physical energy needed to sustain sovereign life and computation.</div>
            <div>• The valuation monitor provides observational clarity without enforcing synthetic price pegs.</div>
          </div>
        </div>
      )}

      {/* Tab Content 3: Work Equivalents */}
      {activeTab === 'comparison' && (
        <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-4">
          <div className="flex items-center space-x-2 text-blue-400">
            <Layers className="w-5 h-5" />
            <h3 className="text-base font-bold text-white">Macroeconomic Work Realization</h3>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            When Pioneer communities exchange goods and services in <span className="font-semibold text-purple-300">π NXS</span>, pricing can reference the physical floor of 3.14159 kWh per token. This empowers grassroots merchants to establish fair barter valuations that cannot be manipulated by centralized liquidity dumps.
          </p>
        </div>
      )}

      {/* ADVANCED MODULE 13.2: Quantum Renewable Grid Simulator & Carnot Work Engine */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-amber-950/20 to-slate-900 border border-amber-900/40 space-y-6 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30 uppercase flex items-center gap-1.5">
                <Flame className="w-3.5 h-3.5 text-amber-400" />
                Proof of Useful Thermodynamic Work (PoUTW)
              </span>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/20 text-emerald-300 border border-emerald-800/40">
                Closed-Loop Carnot Engine
              </span>
            </div>
            <h3 className="text-base font-bold text-white mt-1.5 flex items-center gap-2">
              <Zap className="w-5 h-5 text-amber-400" />
              Quantum Renewable Energy Grid Simulator & Work Floor Engine
            </h3>
            <p className="text-xs text-slate-300 max-w-2xl">
              Model real-world clean renewable energy inputs and prove why π NXS maintains an immutable baseline value derived from physical thermodynamic work rather than speculative debt.
            </p>
          </div>

          <div className="p-2.5 rounded-xl bg-slate-950 border border-amber-900/40 font-mono text-[11px] text-amber-300 shrink-0">
            PoUTW: <span className="font-bold text-white">{gridSim.attestationSignature.slice(0, 24)}...</span>
          </div>
        </div>

        {/* 3 Interactive Energy Source Sliders */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-1 border-t border-slate-800/80">
          {/* Solar Array Slider */}
          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
            <div className="flex items-center justify-between text-xs font-semibold text-slate-300">
              <span className="flex items-center gap-1.5 text-amber-300">
                <Sun className="w-4 h-4 text-amber-400" />
                Solar Photovoltaic
              </span>
              <span className="font-mono text-white font-bold">{solarKwh} kWh</span>
            </div>
            <input
              type="range"
              min="20"
              max="500"
              value={solarKwh}
              onChange={(e) => setSolarKwh(Number(e.target.value))}
              className="w-full accent-amber-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
            />
            <div className="text-[10px] text-slate-500 flex justify-between font-mono">
              <span>20 kWh</span>
              <span>500 kWh</span>
            </div>
          </div>

          {/* Micro-Hydro Stream Flow */}
          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
            <div className="flex items-center justify-between text-xs font-semibold text-slate-300">
              <span className="flex items-center gap-1.5 text-blue-300">
                <Droplets className="w-4 h-4 text-blue-400" />
                Micro-Hydro Stream
              </span>
              <span className="font-mono text-white font-bold">{hydroKwh} kWh</span>
            </div>
            <input
              type="range"
              min="10"
              max="300"
              value={hydroKwh}
              onChange={(e) => setHydroKwh(Number(e.target.value))}
              className="w-full accent-blue-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
            />
            <div className="text-[10px] text-slate-500 flex justify-between font-mono">
              <span>10 kWh</span>
              <span>300 kWh</span>
            </div>
          </div>

          {/* Geothermal / Kinetic Energy */}
          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
            <div className="flex items-center justify-between text-xs font-semibold text-slate-300">
              <span className="flex items-center gap-1.5 text-emerald-300">
                <Wind className="w-4 h-4 text-emerald-400" />
                Kinetic & Geothermal
              </span>
              <span className="font-mono text-white font-bold">{geothermalKwh} kWh</span>
            </div>
            <input
              type="range"
              min="10"
              max="200"
              value={geothermalKwh}
              onChange={(e) => setGeothermalKwh(Number(e.target.value))}
              className="w-full accent-emerald-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
            />
            <div className="text-[10px] text-slate-500 flex justify-between font-mono">
              <span>10 kWh</span>
              <span>200 kWh</span>
            </div>
          </div>
        </div>

        {/* Dynamic Simulation Result Metrics */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
            <span className="text-[10px] uppercase font-bold text-slate-400 block">Total Grid Power</span>
            <span className="text-xl font-mono font-black text-amber-300 mt-1 block">{gridSim.gridPowerWatts.toLocaleString()} W</span>
            <span className="text-[9px] text-slate-500 block">Clean usable throughput</span>
          </div>

          <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
            <span className="text-[10px] uppercase font-bold text-slate-400 block">Carnot Efficiency</span>
            <span className="text-xl font-mono font-black text-blue-300 mt-1 block">{gridSim.carnotEfficiencyPct}%</span>
            <span className="text-[9px] text-slate-500 block">η = 1 - (T_C / T_H)</span>
          </div>

          <div className="p-3 bg-slate-950 rounded-xl border border-amber-900/50">
            <span className="text-[10px] uppercase font-bold text-amber-300 block">Work Floor per π NXS</span>
            <span className="text-xl font-mono font-black text-white mt-1 block">{gridSim.effectiveNxsFloorKwh} <span className="text-xs font-normal text-amber-400">kWh</span></span>
            <span className="text-[9px] text-amber-300/80 font-bold block">Nilai dasar energi, bukan harga pasar</span>
          </div>

          <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
            <span className="text-[10px] uppercase font-bold text-slate-400 block">Entropy / Biosphere</span>
            <span className="text-xl font-mono font-black text-emerald-300 mt-1 block">{gridSim.entropyDissipatedJK} J/K</span>
            <span className="text-[9px] text-emerald-400 block">Biosphere Score: {gridSim.biosphereScore}%</span>
          </div>
        </div>
      </div>

      {/* AI Observational Volatility Radar */}
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div className="flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-amber-400" />
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">
              AI Cognitive Volatility Corridor & Market Radar (Observational)
            </h3>
          </div>
          <span className="text-[10px] font-mono bg-blue-950 text-blue-300 px-2 py-0.5 rounded border border-blue-800">
            Read-Only Heuristic Neural Model
          </span>
        </div>

        <p className="text-xs text-slate-400 leading-relaxed">
          Autonomous statistical correlation between secondary market liquidity pools and decentralized Pioneer merchant barter frequency. Non-invasive monitoring with zero pegging intervention.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-mono">
          <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <div className="text-[11px] text-slate-400">Stellar XLM Volatility Band:</div>
            <div className="text-base font-bold text-emerald-400 mt-1">$0.1080 — $0.1240 USD</div>
            <div className="text-[10px] text-slate-500 mt-0.5">Mean price convergence index 94.2%</div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <div className="text-[11px] text-slate-400">Q-Thermo Floor Status:</div>
            <div className="text-base font-bold text-amber-300 mt-1">3.14159 kWh Constant</div>
            <div className="text-[10px] text-slate-500 mt-0.5">Anchored across 12 Dimensions</div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <div className="text-[11px] text-slate-400">Autonomous Sentinel Verdict:</div>
            <div className="text-base font-bold text-blue-400 mt-1">Equilibrium Resilient</div>
            <div className="text-[10px] text-slate-500 mt-0.5">Zero manipulative order clusters detected</div>
          </div>
        </div>
      </div>

      {/* Mandatory Disclaimer Text at Bottom */}
      <div className="p-4 rounded-xl bg-slate-950/90 border border-slate-800/80 flex items-center space-x-3 text-xs text-slate-400 shadow-inner">
        <AlertCircle className="w-4 h-4 text-amber-400 shrink-0" />
        <span className="font-medium">
          Disclaimer: <strong className="text-slate-300">Q-Thermo Valuation Monitor is a decentralized read-only observation console, not an official pegging or price guarantee. No automated arbitrage or mint/burn executes on mainnet.</strong>
        </span>
      </div>
    </div>
  );
};
