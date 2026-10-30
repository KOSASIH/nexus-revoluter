import React, { useState } from 'react';
import { 
  Vote, 
  Clock, 
  CheckCircle2, 
  ShieldCheck, 
  TrendingUp, 
  Users, 
  AlertCircle, 
  Sparkles,
  Lock,
  ChevronRight,
  ChevronDown,
  BrainCircuit,
  Bot,
  Plus
} from 'lucide-react';
import { DaoProposal, VaultAccount } from '../types';
import { generateShuraDeliberation } from '../services/aiSentinel';

interface DaoViewProps {
  proposals: DaoProposal[];
  vaults: VaultAccount[];
  onVote: (proposalId: string, support: 'for' | 'against') => void;
  onCreateProposal: (proposal: {
    title: string;
    description: string;
    category: 'Bridge Fee' | 'Guardian List' | 'Sentinel Rules' | 'Shura Treasury';
  }) => void;
}

export const DaoView: React.FC<DaoViewProps> = ({
  proposals,
  vaults,
  onVote,
  onCreateProposal
}) => {
  const [showCreateModal, setShowCreateModal] = useState<boolean>(false);
  const [newTitle, setNewTitle] = useState<string>('');
  const [newDescription, setNewDescription] = useState<string>('');
  const [newCategory, setNewCategory] = useState<'Bridge Fee' | 'Guardian List' | 'Sentinel Rules' | 'Shura Treasury'>('Bridge Fee');
  const [expandedDeliberationId, setExpandedDeliberationId] = useState<string | null>(null);

  // Compute Quadratic Voting Power
  // Primary vault age + total pi
  const primaryVault = vaults.find(v => v.isPrimary) || vaults[0];
  const totalPi = vaults.reduce((acc, v) => acc + v.piBalance, 0);
  const vaultAge = primaryVault?.vaultAgeDays || 365;

  // Quadratic formula: sqrt(π NXS) * log2(vaultAgeDays + 2)
  const quadraticPower = Math.floor(Math.sqrt(totalPi) * Math.log2(vaultAge + 2));

  const handleCreateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newDescription.trim()) return;

    onCreateProposal({
      title: newTitle.trim(),
      description: newDescription.trim(),
      category: newCategory
    });

    setNewTitle('');
    setNewDescription('');
    setShowCreateModal(false);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Top Banner */}
      <div className="bg-slate-900/70 p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30 uppercase">
              Module 09 • Shura Governance
            </span>
            <span className="text-xs text-slate-400">Pioneer DAO 3 Active</span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1 flex items-center gap-2">
            <Vote className="w-5 h-5 text-blue-400" />
            Pioneer DAO with Shura Governance & Timelock
          </h2>
          <p className="text-xs text-slate-300 max-w-2xl mt-1 leading-relaxed">
            Democratic, equitable community stewardship. Quadratic voting balances token holdings with vault longevity to prevent plutocratic dominance.
          </p>
        </div>

        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center space-x-1.5 px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold shadow-md shadow-blue-600/30 transition self-start"
        >
          <Plus className="w-4 h-4" />
          <span>New Proposal</span>
        </button>
      </div>

      {/* Voting Power & Shura Principles Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Your Quadratic Voting Power */}
        <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900 via-indigo-950/30 to-slate-900 border border-slate-800 shadow-xl flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                Your Voting Weight
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
                Quadratic
              </span>
            </div>

            <div className="mt-2 text-3xl font-mono font-bold text-white">
              {quadraticPower.toLocaleString()}{' '}
              <span className="text-sm font-bold text-purple-400">π NXS Power</span>
            </div>

            <div className="mt-3 text-xs text-slate-400 space-y-1">
              <div className="flex justify-between">
                <span>Total Vault Holding:</span>
                <span className="font-mono text-white font-semibold">{totalPi.toLocaleString()} π NXS</span>
              </div>
              <div className="flex justify-between">
                <span>Primary Vault Age:</span>
                <span className="font-mono text-white font-semibold">{vaultAge} Days</span>
              </div>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-800 text-[11px] font-mono text-slate-400">
            Formula: √Balance × log₂(Days + 2)
          </div>
        </div>

        {/* 48-Hour Timelock Safety */}
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 text-amber-400 mb-2">
              <Clock className="w-4 h-4" />
              <span className="text-xs font-bold uppercase tracking-wider">
                48-Hour Timelock Shield
              </span>
            </div>

            <div className="text-sm font-bold text-white mt-1">
              Zero Instantaneous Execution
            </div>

            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              Every approved governance action is held in a public on-chain timelock for 48 hours before execution. Pioneers can review changes and withdraw if consensus is breached.
            </p>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-850 flex items-center justify-between text-[11px] font-mono text-emerald-400">
            <span>Byzantine Safe: Active</span>
            <Lock className="w-3.5 h-3.5" />
          </div>
        </div>

        {/* Shura Ethical Principles */}
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 text-emerald-400 mb-2">
              <ShieldCheck className="w-4 h-4" />
              <span className="text-xs font-bold uppercase tracking-wider">
                Shura Amanah Verification
              </span>
            </div>

            <div className="text-sm font-bold text-white mt-1">
              Ethical & Transparent Rules
            </div>

            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              All proposals must respect anti-usury guidelines, non-predatory fees, and transparent community stewardship without hidden admin backdoors.
            </p>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-850 text-[11px] font-mono text-slate-400">
            Amanah Consensus Standard V1.0
          </div>
        </div>
      </div>

      {/* Active Proposals Feed */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <Vote className="w-4 h-4 text-blue-400" />
            Active Pioneer Proposals ({proposals.length})
          </h3>
          <span className="text-xs text-slate-400 font-mono">Tally in π NXS Power</span>
        </div>

        <div className="space-y-4">
          {proposals.map((prop) => {
            const totalVotes = prop.votesFor + prop.votesAgainst;
            const pctFor = totalVotes > 0 ? (prop.votesFor / totalVotes) * 100 : 50;

            return (
              <div
                key={prop.id}
                className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div className="flex items-center space-x-3">
                    <span className="text-xs font-mono font-bold text-blue-400 px-2 py-0.5 rounded bg-blue-500/10 border border-blue-500/20">
                      {prop.id}
                    </span>
                    <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                      {prop.category}
                    </span>
                    <span className="text-[11px] font-mono text-slate-500">
                      Proposer: {prop.proposer}
                    </span>
                  </div>

                  {prop.timelockActive ? (
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-amber-950 text-amber-300 border border-amber-800/50 flex items-center gap-1 self-start">
                      <Clock className="w-3 h-3" /> Timelock: {prop.timelockEndsAt}
                    </span>
                  ) : prop.status === 'executed' ? (
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-800/50 flex items-center gap-1 self-start">
                      <CheckCircle2 className="w-3 h-3" /> Executed
                    </span>
                  ) : (
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-blue-950 text-blue-300 border border-blue-800/50 self-start">
                      Active Voting
                    </span>
                  )}
                </div>

                <div>
                  <h4 className="text-base font-bold text-white">{prop.title}</h4>
                  <p className="text-xs text-slate-300 mt-1 leading-relaxed">
                    {prop.description}
                  </p>
                </div>

                {/* Tally Bar in π NXS notation */}
                <div className="space-y-1.5">
                  <div className="flex justify-between text-xs font-mono">
                    <span className="text-emerald-400 font-semibold">
                      FOR: {prop.votesFor.toLocaleString()} π NXS ({pctFor.toFixed(1)}%)
                    </span>
                    <span className="text-rose-400 font-semibold">
                      AGAINST: {prop.votesAgainst.toLocaleString()} π NXS ({(100 - pctFor).toFixed(1)}%)
                    </span>
                  </div>

                  <div className="h-2 rounded-full bg-slate-950 overflow-hidden flex border border-slate-800">
                    <div
                      className="bg-emerald-500 transition-all duration-500"
                      style={{ width: `${pctFor}%` }}
                    />
                    <div
                      className="bg-rose-500 transition-all duration-500"
                      style={{ width: `${100 - pctFor}%` }}
                    />
                  </div>
                </div>

                {/* AI Shura Deliberation Toggle Button */}
                <div className="pt-2">
                  <button
                    type="button"
                    onClick={() => setExpandedDeliberationId(expandedDeliberationId === prop.id ? null : prop.id)}
                    className="text-xs text-blue-400 hover:text-blue-300 font-medium flex items-center gap-1.5 transition"
                  >
                    <BrainCircuit className="w-3.5 h-3.5 text-blue-400" />
                    <span>{expandedDeliberationId === prop.id ? 'Hide AI Shura Cognitive Deliberation' : 'AI Shura Deliberation & Ethical Impact'}</span>
                    {expandedDeliberationId === prop.id ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
                  </button>

                  {expandedDeliberationId === prop.id && (() => {
                    const analysis = generateShuraDeliberation(prop);
                    return (
                      <div className="mt-3 p-4 rounded-xl bg-slate-950 border border-blue-900/40 text-xs space-y-3 animate-fade-in">
                        <div className="flex flex-wrap items-center justify-between gap-2">
                          <div className="flex items-center space-x-2">
                            <Bot className="w-4 h-4 text-purple-400" />
                            <span className="font-bold text-slate-200">Shura Consensus Diagnostic:</span>
                            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-950 text-blue-300 border border-blue-800">
                              Score {analysis.shuraScore}/100
                            </span>
                          </div>
                          <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase ${
                            analysis.recommendedAction === 'RATIFY' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' : 'bg-amber-950 text-amber-300 border border-amber-800'
                          }`}>
                            Recommendation: {analysis.recommendedAction}
                          </span>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] text-slate-300">
                          <div className="p-2 rounded bg-slate-900 border border-slate-800">
                            <span className="text-slate-400 font-medium block">Economic Sustainability:</span>
                            <span className="text-slate-200">{analysis.economicSustainability}</span>
                          </div>
                          <div className="p-2 rounded bg-slate-900 border border-slate-800">
                            <span className="text-slate-400 font-medium block">Community Welfare:</span>
                            <span className="text-slate-200">{analysis.welfareImpact}</span>
                          </div>
                        </div>

                        <div className="text-[11px] text-slate-400 space-y-1">
                          <div className="font-semibold text-slate-300">Key Shura Insights:</div>
                          {analysis.keyInsights.map((ins, i) => (
                            <div key={i} className="flex items-start space-x-1.5 pl-1">
                              <span className="text-blue-400">•</span>
                              <span>{ins}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    );
                  })()}
                </div>

                {/* Vote Action Buttons */}
                <div className="flex items-center justify-between pt-2 border-t border-slate-800/80">
                  <div className="text-xs text-slate-400">
                    {prop.userVoted ? (
                      <span className="text-blue-400 font-semibold">
                        You cast your quadratic ballot ({prop.userVoted.toUpperCase()})
                      </span>
                    ) : (
                      <span>Cast your {quadraticPower.toLocaleString()} π NXS ballot:</span>
                    )}
                  </div>

                  <div className="flex space-x-2">
                    <button
                      onClick={() => onVote(prop.id, 'for')}
                      disabled={!!prop.userVoted || prop.status === 'executed'}
                      className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition ${
                        prop.userVoted === 'for'
                          ? 'bg-emerald-600 text-white'
                          : 'bg-emerald-950/60 hover:bg-emerald-800 text-emerald-300 border border-emerald-800/60 disabled:opacity-40'
                      }`}
                    >
                      Vote FOR
                    </button>
                    <button
                      onClick={() => onVote(prop.id, 'against')}
                      disabled={!!prop.userVoted || prop.status === 'executed'}
                      className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition ${
                        prop.userVoted === 'against'
                          ? 'bg-rose-600 text-white'
                          : 'bg-rose-950/60 hover:bg-rose-800 text-rose-300 border border-rose-800/60 disabled:opacity-40'
                      }`}
                    >
                      Vote AGAINST
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* New Proposal Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-lg w-full p-6 shadow-2xl">
            <h3 className="text-base font-bold text-white mb-1">Create Pioneer Shura Proposal</h3>
            <p className="text-xs text-slate-400 mb-4">
              Requires min 100 π NXS balance to submit. Approved motions enter 48-hour timelock.
            </p>

            <form onSubmit={handleCreateSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Proposal Title</label>
                <input
                  type="text"
                  placeholder="e.g. Optimize Sentinel Gossip Fanout to 4 Peers"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:ring-1 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Category</label>
                <select
                  value={newCategory}
                  onChange={(e) => setNewCategory(e.target.value as any)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option value="Bridge Fee">Bridge Fee Calibration</option>
                  <option value="Sentinel Rules">Sentinel Mesh Rules</option>
                  <option value="Guardian List">Guardian List / Social Recovery</option>
                  <option value="Shura Treasury">Shura Treasury Grant</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Detailed Rationale</label>
                <textarea
                  rows={3}
                  placeholder="Explain why this proposal benefits the Pioneer sovereign infrastructure..."
                  value={newDescription}
                  onChange={(e) => setNewDescription(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:ring-1 focus:ring-blue-500"
                  required
                />
              </div>

              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-xs font-medium text-slate-300 hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white"
                >
                  Submit to DAO
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
