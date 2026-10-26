import React, { useState } from 'react';
import { 
  Vote, 
  Check, 
  X, 
  Minus, 
  Plus, 
  Clock, 
  Users, 
  CheckCircle2, 
  Sparkles,
  Award
} from 'lucide-react';
import { Proposal } from '../types';

interface GovernanceViewProps {
  proposals: Proposal[];
  onVote: (proposalId: string, choice: 'for' | 'against' | 'abstain') => void;
  onCreateProposal: (proposal: {
    title: string;
    description: string;
    category: Proposal['category'];
  }) => void;
}

export const GovernanceView: React.FC<GovernanceViewProps> = ({
  proposals,
  onVote,
  onCreateProposal
}) => {
  const [isCreatingProposal, setIsCreatingProposal] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [newCategory, setNewCategory] = useState<Proposal['category']>('Monetary Policy');

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
    setIsCreatingProposal(false);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 rounded text-[11px] font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40 uppercase">
              Liquid Democracy DAO
            </span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1 flex items-center gap-2">
            <Vote className="w-5 h-5 text-amber-400" />
            Pioneer Decentralized Governance
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Cast weighted votes on SANO monetary policy, NPAS bridge upgrades, and ecosystem incentive distribution.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-center space-x-2 text-xs">
            <Award className="w-4 h-4 text-purple-400" />
            <div>
              <div className="text-[10px] text-slate-500 font-semibold uppercase">Your Voting Power</div>
              <div className="font-mono font-bold text-white">31,415.92 vπ PI (1.42x Multiplier)</div>
            </div>
          </div>

          <button
            onClick={() => setIsCreatingProposal(true)}
            className="flex items-center space-x-1.5 px-4 py-2.5 rounded-xl bg-amber-600 hover:bg-amber-500 text-xs font-semibold text-white transition shadow-md shadow-amber-600/20"
          >
            <Plus className="w-4 h-4" />
            <span>Create Proposal</span>
          </button>
        </div>
      </div>

      {/* Proposals List */}
      <div className="space-y-4">
        {proposals.map((prop) => {
          const totalVotes = prop.votesFor + prop.votesAgainst + prop.votesAbstain;
          const forPercent = totalVotes > 0 ? (prop.votesFor / totalVotes) * 100 : 0;
          const againstPercent = totalVotes > 0 ? (prop.votesAgainst / totalVotes) * 100 : 0;
          const abstainPercent = totalVotes > 0 ? (prop.votesAbstain / totalVotes) * 100 : 0;

          return (
            <div
              key={prop.id}
              className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 hover:border-slate-700 transition"
            >
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-3">
                <div className="flex items-center space-x-2">
                  <span className="font-mono text-xs font-bold text-amber-400">{prop.id}</span>
                  <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                    {prop.category}
                  </span>
                  <span
                    className={`text-[10px] font-semibold px-2 py-0.5 rounded uppercase font-mono ${
                      prop.status === 'passed'
                        ? 'bg-emerald-950 text-emerald-300 border border-emerald-800/50'
                        : prop.status === 'active'
                        ? 'bg-blue-950 text-blue-300 border border-blue-800/50'
                        : 'bg-rose-950 text-rose-300 border border-rose-800/50'
                    }`}
                  >
                    {prop.status}
                  </span>
                </div>

                <div className="flex items-center space-x-3 text-xs text-slate-400 font-mono">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" /> {prop.deadline}
                  </span>
                  <span>Proposer: {prop.proposer}</span>
                </div>
              </div>

              <h3 className="text-base font-bold text-white mb-2">{prop.title}</h3>
              <p className="text-xs text-slate-300 leading-relaxed mb-5">{prop.description}</p>

              {/* Voting Bar */}
              <div className="space-y-1.5 mb-5">
                <div className="flex justify-between text-xs font-mono font-medium">
                  <span className="text-emerald-400 flex items-center gap-1">
                    <Check className="w-3.5 h-3.5" /> For: {forPercent.toFixed(1)}% ({prop.votesFor.toLocaleString()} π PI)
                  </span>
                  <span className="text-rose-400 flex items-center gap-1">
                    <X className="w-3.5 h-3.5" /> Against: {againstPercent.toFixed(1)}% ({prop.votesAgainst.toLocaleString()} π PI)
                  </span>
                </div>

                <div className="h-2.5 w-full bg-slate-950 rounded-full overflow-hidden flex border border-slate-800">
                  <div style={{ width: `${forPercent}%` }} className="bg-emerald-500 h-full" />
                  <div style={{ width: `${abstainPercent}%` }} className="bg-slate-500 h-full" />
                  <div style={{ width: `${againstPercent}%` }} className="bg-rose-500 h-full" />
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-800/60">
                <div className="text-xs text-slate-400">
                  {prop.userVoted ? (
                    <span className="text-emerald-400 flex items-center gap-1 font-semibold">
                      <CheckCircle2 className="w-4 h-4" /> You voted {prop.userVoted.toUpperCase()} on this proposal
                    </span>
                  ) : (
                    <span>Cast your Pioneer vote:</span>
                  )}
                </div>

                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => onVote(prop.id, 'for')}
                    className={`flex items-center space-x-1 px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                      prop.userVoted === 'for'
                        ? 'bg-emerald-600 text-white'
                        : 'bg-emerald-950/40 text-emerald-400 hover:bg-emerald-600 hover:text-white border border-emerald-800/40'
                    }`}
                  >
                    <Check className="w-3.5 h-3.5" />
                    <span>Vote For</span>
                  </button>
                  <button
                    onClick={() => onVote(prop.id, 'against')}
                    className={`flex items-center space-x-1 px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                      prop.userVoted === 'against'
                        ? 'bg-rose-600 text-white'
                        : 'bg-rose-950/40 text-rose-400 hover:bg-rose-600 hover:text-white border border-rose-800/40'
                    }`}
                  >
                    <X className="w-3.5 h-3.5" />
                    <span>Vote Against</span>
                  </button>
                  <button
                    onClick={() => onVote(prop.id, 'abstain')}
                    className={`flex items-center space-x-1 px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                      prop.userVoted === 'abstain'
                        ? 'bg-slate-700 text-white'
                        : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white border border-slate-700'
                    }`}
                  >
                    <Minus className="w-3.5 h-3.5" />
                    <span>Abstain</span>
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Create Proposal Modal */}
      {isCreatingProposal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-lg w-full p-6 shadow-2xl">
            <h3 className="text-base font-bold text-white mb-2">Submit Pioneer DAO Proposal</h3>
            <p className="text-xs text-slate-400 mb-4">
              Requires 100 π PI stake deposit. If quorum is met, your proposal triggers autonomous smart contract execution.
            </p>
            <form onSubmit={handleCreateSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Proposal Title</label>
                <input
                  type="text"
                  placeholder="e.g. Allocate Community Grants for Regional Relays"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-amber-500"
                  autoFocus
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Category</label>
                <select
                  value={newCategory}
                  onChange={(e) => setNewCategory(e.target.value as Proposal['category'])}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:ring-1 focus:ring-amber-500"
                >
                  <option value="Monetary Policy">Monetary Policy</option>
                  <option value="Orchestration">Orchestration</option>
                  <option value="Network Upgrade">Network Upgrade</option>
                  <option value="Community Fund">Community Fund</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Detailed Description & Motivation</label>
                <textarea
                  rows={4}
                  placeholder="Provide background, technical specification, and economic rationale..."
                  value={newDescription}
                  onChange={(e) => setNewDescription(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-amber-500"
                />
              </div>

              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsCreatingProposal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!newTitle.trim() || !newDescription.trim()}
                  className="px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-500 text-xs font-semibold text-white disabled:opacity-50"
                >
                  Submit to On-Chain Ballot
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
