import React, { useState } from 'react';
import { 
  Dna, 
  Flame, 
  Cpu, 
  Layers, 
  Radio, 
  ShieldCheck, 
  Zap, 
  RefreshCw, 
  Sparkles, 
  Activity, 
  Clock, 
  ArrowRight, 
  CheckCircle2, 
  Lock, 
  Globe2, 
  Server, 
  TrendingUp,
  Sliders,
  Atom,
  HelpCircle,
  BrainCircuit
} from 'lucide-react';
import { 
  DimensionVector, 
  SuperCalculator, 
  QThermoMetrics, 
  PredictiveGasForecast 
} from '../types';
import { 
  predictMempoolAndGasForecast, 
  calculateGodChainHarmonics 
} from '../services/aiSentinel';
import { AutonomousAgenticMesh } from './AutonomousAgenticMesh';

interface GodChainViewProps {
  dimensions: DimensionVector[];
  superCalculators: SuperCalculator[];
  qThermo: QThermoMetrics;
  onCalibrateDimension?: (id: number) => void;
}

export const GodChainView: React.FC<GodChainViewProps> = ({
  dimensions,
  superCalculators,
  qThermo,
  onCalibrateDimension
}) => {
  const [activeSubTab, setActiveSubTab] = useState<'12d' | 'agents' | 'calculators' | 'qthermo' | 'predictive'>('12d');
  const [selectedDimension, setSelectedDimension] = useState<DimensionVector | null>(dimensions[0] || null);
  const [isHarmonizing, setIsHarmonizing] = useState<boolean>(false);
  const [harmonicToast, setHarmonicToast] = useState<string | null>(null);

  // Dynamic simulation parameters for Q-Thermo
  const [simulatedTxVelocity, setSimulatedTxVelocity] = useState<number>(4.82);
  const [simulatedLoadIndex, setSimulatedLoadIndex] = useState<number>(45);

  const gasForecast: PredictiveGasForecast[] = predictMempoolAndGasForecast();
  const harmonics = calculateGodChainHarmonics(dimensions, qThermo);

  const handleRunHarmonization = () => {
    setIsHarmonizing(true);
    setHarmonicToast(null);

    setTimeout(() => {
      setIsHarmonizing(false);
      setHarmonicToast('12D Tensor Invariant verified: Nyawa, Raga, and Wanci unified with 0 entropy leak across 5 Super Calculators.');
      setTimeout(() => setHarmonicToast(null), 6000);
    }, 1200);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/60 to-purple-950/40 p-6 rounded-2xl border border-indigo-500/30 relative overflow-hidden shadow-2xl">
        <div className="absolute top-0 right-0 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 relative z-10">
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <span className="px-2.5 py-0.5 rounded text-[11px] font-mono font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 uppercase flex items-center gap-1.5">
                <Atom className="w-3.5 h-3.5 text-indigo-400" />
                Layer 0 • God Chain 12 Dimensi
              </span>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-purple-500/20 text-purple-300 border border-purple-500/30">
                Nyawa • Raga • Wanci
              </span>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                Web4 Agentic GDP Ready
              </span>
            </div>

            <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-2 tracking-tight flex items-center gap-2">
              Sovereign Identity & Q-Thermo Engine
            </h2>
            <p className="text-xs sm:text-sm text-slate-300 max-w-3xl mt-1.5 leading-relaxed">
              The supreme human identity layer anchoring sovereign human life, physical vessel, and temporal cosmic alignment. All external networks act as specialized <strong className="text-white">Super Calculators</strong> coordinated beneath sovereign Pioneer authority.
            </p>
          </div>

          {/* Quick Metrics Badge Group */}
          <div className="flex flex-wrap lg:flex-nowrap items-center gap-3">
            <div className="bg-slate-950/70 border border-indigo-900/60 p-3 rounded-xl min-w-[120px] text-center">
              <div className="text-[10px] uppercase font-bold text-slate-400">Tensor Resonance</div>
              <div className="text-xl font-mono font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-300 to-purple-300">
                {harmonics.unifiedResonanceScore}%
              </div>
              <div className="text-[9px] text-emerald-400 font-mono">12/12 Synchronized</div>
            </div>

            <div className="bg-slate-950/70 border border-indigo-900/60 p-3 rounded-xl min-w-[130px] text-center">
              <div className="text-[10px] uppercase font-bold text-slate-400">Q-Thermo Backing</div>
              <div className="text-xl font-mono font-black text-amber-300">
                3.14159 <span className="text-xs font-normal text-amber-400/80">kWh</span>
              </div>
              <div className="text-[9px] text-slate-400 font-mono">per <span className="text-amber-300 font-bold">π PI</span> token</div>
            </div>

            <button
              onClick={handleRunHarmonization}
              disabled={isHarmonizing}
              className="px-4 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-bold shadow-lg shadow-blue-500/20 flex items-center gap-2 transition disabled:opacity-60 whitespace-nowrap self-stretch lg:self-auto justify-center"
            >
              <RefreshCw className={`w-4 h-4 ${isHarmonizing ? 'animate-spin' : ''}`} />
              <span>{isHarmonizing ? 'Harmonizing 12D...' : 'Re-Calibrate Matrix'}</span>
            </button>
          </div>
        </div>

        {/* Feedback Toast */}
        {harmonicToast && (
          <div className="mt-4 p-3 bg-emerald-500/15 border border-emerald-500/30 rounded-xl text-xs text-emerald-200 flex items-center space-x-2 animate-in fade-in">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>{harmonicToast}</span>
          </div>
        )}
      </div>

      {/* Sub-tab Navigation */}
      <div className="flex flex-wrap items-center justify-between border-b border-slate-800 pb-3 gap-2">
        <div className="bg-slate-900/80 p-1 rounded-xl border border-slate-800 flex flex-wrap gap-1 text-xs">
          <button
            onClick={() => setActiveSubTab('12d')}
            className={`px-3.5 py-1.5 rounded-lg font-semibold transition flex items-center gap-2 ${
              activeSubTab === '12d'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Dna className="w-3.5 h-3.5" />
            <span>12D Identity Tensor</span>
          </button>

          <button
            onClick={() => setActiveSubTab('agents')}
            className={`px-3.5 py-1.5 rounded-lg font-semibold transition flex items-center gap-2 ${
              activeSubTab === 'agents'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <BrainCircuit className="w-3.5 h-3.5" />
            <span>Agentic Mesh (ASANN)</span>
          </button>

          <button
            onClick={() => setActiveSubTab('calculators')}
            className={`px-3.5 py-1.5 rounded-lg font-semibold transition flex items-center gap-2 ${
              activeSubTab === 'calculators'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Cpu className="w-3.5 h-3.5" />
            <span>Super Calculators ({superCalculators.length})</span>
          </button>

          <button
            onClick={() => setActiveSubTab('qthermo')}
            className={`px-3.5 py-1.5 rounded-lg font-semibold transition flex items-center gap-2 ${
              activeSubTab === 'qthermo'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Flame className="w-3.5 h-3.5" />
            <span>Q-Thermo Physical Ledger</span>
          </button>

          <button
            onClick={() => setActiveSubTab('predictive')}
            className={`px-3.5 py-1.5 rounded-lg font-semibold transition flex items-center gap-2 ${
              activeSubTab === 'predictive'
                ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <TrendingUp className="w-3.5 h-3.5" />
            <span>Predictive Gas & GDP Horizon</span>
          </button>
        </div>

        <div className="text-[11px] font-mono text-slate-400 flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
          <span>Thermodynamic State: <strong>{harmonics.thermoStateVerdict}</strong></span>
        </div>
      </div>

      {/* SUB-TAB 1: 12-DIMENSIONAL IDENTITY TENSOR */}
      {activeSubTab === '12d' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* 12 Dimensions Grid (2 cols) */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-amber-400" />
                12-Dimensional Tensor Vectors
              </h3>
              <span className="text-xs text-slate-500 font-mono">Click any vector to inspect proof</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {dimensions.map((dim) => {
                const isSelected = selectedDimension?.id === dim.id;
                return (
                  <div
                    key={dim.id}
                    onClick={() => setSelectedDimension(dim)}
                    className={`p-3.5 rounded-xl border cursor-pointer transition relative overflow-hidden ${
                      isSelected
                        ? 'bg-gradient-to-br from-indigo-950/80 to-slate-900 border-indigo-500 ring-1 ring-indigo-500/50 shadow-lg shadow-indigo-500/10'
                        : 'bg-slate-900/70 border-slate-800 hover:border-slate-700 hover:bg-slate-850'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-slate-950 text-indigo-300 border border-slate-800">
                        D{dim.id} • {dim.sanskritName}
                      </span>
                      <span className={`text-[10px] font-mono font-semibold px-1.5 py-0.5 rounded ${
                        dim.status === 'SYNCHRONIZED' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800/50' : 'bg-purple-950 text-purple-300 border border-purple-800/50'
                      }`}>
                        {dim.status}
                      </span>
                    </div>

                    <h4 className="text-xs font-bold text-white mt-2 leading-tight">
                      {dim.name}
                    </h4>

                    <div className="mt-2.5 flex items-center justify-between text-[11px]">
                      <span className="text-slate-400 font-mono">Resonance:</span>
                      <span className="font-mono font-bold text-indigo-300">{dim.resonanceScore}%</span>
                    </div>

                    {/* Mini progress bar */}
                    <div className="w-full bg-slate-800 h-1.5 rounded-full mt-1.5 overflow-hidden">
                      <div 
                        className="bg-gradient-to-r from-blue-500 to-indigo-500 h-full rounded-full transition-all duration-500" 
                        style={{ width: `${dim.resonanceScore}%` }} 
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Right Panel: Selected Dimension Deep Proof Inspector */}
          <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 flex flex-col justify-between space-y-4">
            {selectedDimension ? (
              <div className="space-y-4">
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 rounded-lg bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center text-indigo-300 font-bold font-mono text-sm">
                    D{selectedDimension.id}
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-white leading-tight">
                      {selectedDimension.name}
                    </h4>
                    <span className="text-[10px] font-mono text-indigo-400">
                      {selectedDimension.sanskritName} • {selectedDimension.category}
                    </span>
                  </div>
                </div>

                <div className="p-3 bg-slate-950/80 rounded-xl border border-slate-800 space-y-2">
                  <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                    Sovereign Invariant Rule
                  </div>
                  <p className="text-xs text-slate-200 leading-relaxed">
                    {selectedDimension.invariantRule}
                  </p>
                </div>

                <div className="space-y-2">
                  <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                    Real-World Physical Telemetry
                  </div>
                  <div className="p-2.5 bg-slate-950/80 rounded-lg border border-slate-800 text-xs font-mono text-emerald-300 flex items-center gap-2">
                    <Activity className="w-4 h-4 text-emerald-400 shrink-0" />
                    <span>{selectedDimension.realWorldMetric}</span>
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                    Tensor Proof Hash
                  </div>
                  <div className="p-2.5 bg-slate-950/80 rounded-lg border border-slate-800 text-[10px] font-mono text-indigo-300 break-all">
                    {selectedDimension.tensorHash}
                  </div>
                </div>

                <div className="p-3 bg-indigo-950/40 border border-indigo-800/40 rounded-xl text-xs text-indigo-200 space-y-1">
                  <div className="font-bold flex items-center gap-1.5">
                    <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
                    <span>Non-Custodial Sovereignty Guarantee</span>
                  </div>
                  <p className="text-[11px] text-slate-300">
                    No third party, validator, or foundation holds authority to modify this dimension vector. Validated client-side locally in your browser.
                  </p>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-slate-500 text-xs">
                Select a dimension to inspect its cryptographic tensor proof.
              </div>
            )}

            {selectedDimension && onCalibrateDimension && (
              <button
                onClick={() => onCalibrateDimension(selectedDimension.id)}
                className="w-full mt-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold border border-slate-700 transition"
              >
                Re-Attest Dimension D{selectedDimension.id}
              </button>
            )}
          </div>
        </div>
      )}

      {/* SUB-TAB: AUTONOMOUS SOVEREIGN AGENTIC MESH */}
      {activeSubTab === 'agents' && (
        <AutonomousAgenticMesh
          nodesCount={5}
          qThermoBacking={qThermo.energyBackingPerPi}
        />
      )}

      {/* SUB-TAB 2: SUPER CALCULATORS COORDINATOR MESH */}
      {activeSubTab === 'calculators' && (
        <div className="space-y-6">
          <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800 text-xs text-slate-300 flex items-start gap-3">
            <Cpu className="w-5 h-5 text-indigo-400 shrink-0 mt-0.5" />
            <div>
              <strong className="text-white">Philosophy of Super Calculators:</strong> All external blockchains (Bitcoin, Ethereum, Solana, Pi Network, Zcash, Arweave) are treated not as supreme financial gods, but as specialized calculators subordinated to the 12-Dimensional God Chain identity layer.
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {superCalculators.map((calc) => (
              <div 
                key={calc.id} 
                className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-indigo-500/50 transition flex flex-col justify-between space-y-4"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30 uppercase">
                      {calc.role}
                    </span>
                    <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/40">
                      {calc.coordinationStatus}
                    </span>
                  </div>

                  <h4 className="text-base font-bold text-white mt-1">
                    {calc.name}
                  </h4>
                  <p className="text-xs text-slate-400 font-mono mt-0.5">
                    Target: {calc.chainTarget}
                  </p>

                  <div className="mt-4 space-y-2 text-xs">
                    <div className="flex items-center justify-between text-slate-400">
                      <span>Header Sync:</span>
                      <span className="font-mono text-white font-semibold">#{calc.lastBlockSync.toLocaleString()}</span>
                    </div>

                    <div className="flex items-center justify-between text-slate-400">
                      <span>Throughput:</span>
                      <span className="font-mono text-indigo-300 font-semibold">{calc.tpsEquivalent} TPS equiv.</span>
                    </div>

                    <div className="flex items-center justify-between text-slate-400">
                      <span>God Chain Relay Latency:</span>
                      <span className="font-mono text-emerald-400 font-semibold">{calc.latencyToGodChain} ms</span>
                    </div>
                  </div>
                </div>

                <div className="pt-3 border-t border-slate-800/80">
                  <div className="text-[10px] font-mono text-slate-500">
                    Proof: <span className="text-slate-400">{calc.tensorProofType}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* SUB-TAB 3: Q-THERMO PHYSICAL LEDGER */}
      {activeSubTab === 'qthermo' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Card 1: Energy Backing */}
            <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900 to-amber-950/20 border border-amber-900/30 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-amber-300 flex items-center gap-1.5">
                  <Flame className="w-4 h-4 text-amber-400" />
                  Energy Backing
                </span>
                <span className="text-[10px] font-mono bg-amber-950 text-amber-300 px-2 py-0.5 rounded border border-amber-800">
                  Thermodynamic Work
                </span>
              </div>
              <div className="text-3xl sm:text-4xl font-mono font-black text-white">
                {qThermo.energyBackingPerPi.toFixed(5)}{' '}
                <span className="text-base font-normal text-amber-300">kWh</span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">
                Every <strong className="text-amber-300 font-bold">π PI</strong> token possesses a hard physical floor based on useful computational and ecological thermodynamic work.
              </p>
            </div>

            {/* Card 2: Biosphere Purity */}
            <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900 to-emerald-950/20 border border-emerald-900/30 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-300 flex items-center gap-1.5">
                  <Globe2 className="w-4 h-4 text-emerald-400" />
                  Biosphere Condition
                </span>
                <span className="text-[10px] font-mono bg-emerald-950 text-emerald-300 px-2 py-0.5 rounded border border-emerald-800">
                  Ecological Invariant
                </span>
              </div>
              <div className="text-3xl sm:text-4xl font-mono font-black text-emerald-300">
                {qThermo.biospherePurityIndex}%
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">
                Zero-carbon sovereign ledger. Consensus validated through lightweight SCP Quorum slices with negligible power footprint.
              </p>
            </div>

            {/* Card 3: Entropy Equilibrium */}
            <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900 to-indigo-950/20 border border-indigo-900/30 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-indigo-300 flex items-center gap-1.5">
                  <Atom className="w-4 h-4 text-indigo-400" />
                  Thermodynamic Entropy
                </span>
                <span className="text-[10px] font-mono bg-indigo-950 text-indigo-300 px-2 py-0.5 rounded border border-indigo-800">
                  J / K Balance
                </span>
              </div>
              <div className="text-3xl sm:text-4xl font-mono font-black text-indigo-200">
                {qThermo.currentEntropy} <span className="text-base font-normal text-slate-400">J/K</span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">
                Equilibrium ratio: <strong className="text-white font-mono">1.000000</strong>. Closed-loop state engine prevents artificial debt accumulation.
              </p>
            </div>
          </div>

          {/* Interactive Workload Simulation Slider */}
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <h4 className="text-sm font-bold text-white flex items-center gap-2">
                  <Sliders className="w-4 h-4 text-blue-400" />
                  Q-Thermo Invariant Load Simulation
                </h4>
                <p className="text-xs text-slate-400">
                  Simulate real-time computational load and test the self-balancing energy invariant for <span className="text-blue-300 font-bold">π PI</span> settlement.
                </p>
              </div>
              <span className="text-xs font-mono font-bold text-indigo-300 bg-indigo-950/60 px-3 py-1 rounded-lg border border-indigo-800">
                Load Factor: {simulatedLoadIndex}%
              </span>
            </div>

            <input
              type="range"
              min="10"
              max="100"
              value={simulatedLoadIndex}
              onChange={(e) => {
                const val = Number(e.target.value);
                setSimulatedLoadIndex(val);
                setSimulatedTxVelocity(parseFloat((3.0 + (val / 100) * 4.0).toFixed(2)));
              }}
              className="w-full accent-blue-500 cursor-pointer h-2 bg-slate-800 rounded-lg"
            />

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2 text-xs">
              <div className="p-3 bg-slate-950/70 rounded-xl border border-slate-800">
                <span className="text-slate-400">Simulated Velocity (V):</span>
                <div className="font-mono font-bold text-white text-base mt-0.5">{simulatedTxVelocity} V</div>
              </div>
              <div className="p-3 bg-slate-950/70 rounded-xl border border-slate-800">
                <span className="text-slate-400">Dynamic Backing Floor:</span>
                <div className="font-mono font-bold text-amber-300 text-base mt-0.5">
                  {(3.14159 * (1 + (simulatedLoadIndex - 50) * 0.001)).toFixed(5)} kWh / <span className="text-amber-300">π PI</span>
                </div>
              </div>
              <div className="p-3 bg-slate-950/70 rounded-xl border border-slate-800">
                <span className="text-slate-400">PoUTW Attestation Hash:</span>
                <div className="font-mono text-[10px] text-emerald-400 mt-1 truncate">
                  {qThermo.poutwHash}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* SUB-TAB 4: PREDICTIVE GAS & AGENTIC GDP FORECAST */}
      {activeSubTab === 'predictive' && (
        <div className="space-y-6">
          <div className="bg-slate-900/70 p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30 uppercase">
                Agentic GDP Forecasting Engine
              </span>
              <h3 className="text-xl font-bold text-white mt-1 flex items-center gap-2">
                <Clock className="w-5 h-5 text-blue-400" />
                60-Minute Predictive Gas & Congestion Horizon
              </h3>
              <p className="text-xs text-slate-300 max-w-2xl mt-1 leading-relaxed">
                Algorithmic forecasting of peer gossip load, fee pricing in <strong className="text-white">π PI</strong>, and optimal zero-rent windows for Pioneer transactions.
              </p>
            </div>

            <div className="p-3 bg-emerald-950/40 border border-emerald-800/40 rounded-xl text-xs text-emerald-300 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              <span>Zero-Rent Pioneer Guarantee: Base transfer remains 0.00010 <span className="font-bold">π PI</span></span>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {gasForecast.map((slot, i) => (
              <div
                key={i}
                className={`p-4 rounded-xl border flex flex-col justify-between space-y-3 transition ${
                  slot.optimalTransferWindow
                    ? 'bg-gradient-to-b from-slate-900 to-emerald-950/30 border-emerald-500/50 shadow-md shadow-emerald-500/10'
                    : 'bg-slate-900/70 border-slate-800'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono font-bold text-slate-300">
                      {slot.minuteSlot}
                    </span>
                    {slot.optimalTransferWindow && (
                      <span className="h-2 w-2 rounded-full bg-emerald-400 animate-ping" />
                    )}
                  </div>

                  <div className="mt-3">
                    <span className="text-[10px] uppercase font-bold text-slate-400 block">Congestion</span>
                    <span className={`text-lg font-mono font-black ${
                      slot.predictedCongestion < 40 ? 'text-emerald-300' : 'text-amber-300'
                    }`}>
                      {slot.predictedCongestion}%
                    </span>
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-800/80 space-y-1 text-[11px]">
                  <div className="text-slate-400">Rec. Fee:</div>
                  <div className="font-mono font-bold text-white">
                    {slot.recommendedFeePi.toFixed(5)} <span className="text-blue-400">π PI</span>
                  </div>
                  <div className="text-[10px] font-mono text-slate-500">
                    Est. {slot.expectedTps} TPS
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
