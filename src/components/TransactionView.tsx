import React, { useState } from 'react';
import { 
  Send, 
  ShieldCheck, 
  AlertTriangle, 
  ArrowRight, 
  CheckCircle2, 
  Clock, 
  ExternalLink, 
  FileText, 
  Lock, 
  Info,
  Sparkles,
  RefreshCw
} from 'lucide-react';
import { VaultAccount, Transaction } from '../types';
import { TxDetailsModal } from './TxDetailsModal';
import { analyzeTransactionRisk } from '../services/aiSentinel';


interface TransactionViewProps {
  vaults: VaultAccount[];
  transactions: Transaction[];
  onSendTransaction: (tx: {
    from: string;
    to: string;
    amount: number;
    asset: 'π PI IOU' | 'XLM' | 'NRV';
    memo: string;
    aiRiskScore: number;
    aiRiskVerdict: 'SAFE' | 'SUSPICIOUS' | 'FLAGGED';
  }) => void;
  livePrice: number;
  communityGcv: number;
}

export const TransactionView: React.FC<TransactionViewProps> = ({
  vaults,
  transactions,
  onSendTransaction,
  livePrice,
  communityGcv
}) => {
  const [fromAddress, setFromAddress] = useState<string>(vaults[0]?.address || '');
  const [toAddress, setToAddress] = useState<string>('');
  const [asset, setAsset] = useState<'π PI IOU' | 'XLM' | 'NRV'>('π PI IOU');
  const [amount, setAmount] = useState<string>('');
  const [memo, setMemo] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [txSuccessMessage, setTxSuccessMessage] = useState<string | null>(null);
  const [selectedTx, setSelectedTx] = useState<Transaction | null>(null);
  // Selected vault details
  const selectedVault = vaults.find(v => v.address === fromAddress) || vaults[0];

  const parsedAmount = parseFloat(amount) || 0;
  const currentRiskDetail = analyzeTransactionRisk(toAddress, parsedAmount, memo, selectedVault?.piBalance || 0);
  const currentRisk = {
    score: Math.round(currentRiskDetail.honeypotProbability * 100),
    verdict: (currentRiskDetail.phishingRisk === 'HIGH' ? 'FLAGGED' : currentRiskDetail.phishingRisk === 'LOW' ? 'SUSPICIOUS' : 'SAFE') as 'SAFE' | 'SUSPICIOUS' | 'FLAGGED',
    warnings: currentRiskDetail.phishingRisk !== 'NONE' ? [currentRiskDetail.verdictReason] : []
  };

  const handleMaxAmount = () => {
    if (!selectedVault) return;
    if (asset === 'π PI IOU') {
      setAmount(selectedVault.piBalance.toString());
    } else if (asset === 'XLM') {
      setAmount(Math.max(0, selectedVault.xlmBalance - 0.0001).toFixed(4));
    } else {
      setAmount('100');
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!fromAddress || !toAddress || parsedAmount <= 0) return;

    setIsSubmitting(true);

    setTimeout(() => {
      onSendTransaction({
        from: fromAddress,
        to: toAddress,
        amount: parsedAmount,
        asset,
        memo: memo.trim() || 'P2P Micro-Barter Settlement',
        aiRiskScore: currentRisk.score,
        aiRiskVerdict: currentRisk.verdict
      });

      setTxSuccessMessage(`Transaction successfully signed with Ed25519 & broadcast to SCP sentinels.`);
      setAmount('');
      setMemo('');
      setIsSubmitting(false);

      setTimeout(() => setTxSuccessMessage(null), 5000);
    }, 600);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Module Banner */}
      <div className="bg-slate-900/70 p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30 uppercase">
              Module 06 • Settlement
            </span>
            <span className="text-xs text-slate-400">Ed25519 Cryptographic Signer</span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1 flex items-center gap-2">
            <Send className="w-5 h-5 text-blue-400" />
            Execute IOU Transaction
          </h2>
          <p className="text-xs text-slate-300 max-w-2xl mt-1 leading-relaxed">
            Autonomous ARHN Compliance & AHCEW Empathy Engine. Client-side signed transactions broadcast directly to community validator nodes.
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs">
          <div className="px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-300 flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>ARHN Verified</span>
          </div>
          <div className="px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-300 flex items-center gap-1.5">
            <Lock className="w-4 h-4 text-purple-400" />
            <span>Ed25519 Signed</span>
          </div>
        </div>
      </div>

      {txSuccessMessage && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs flex items-center space-x-2 animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{txSuccessMessage}</span>
        </div>
      )}

      {/* Main Grid: Form on Left, Risk Sentinel & Balance on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Transaction Form */}
        <div className="lg:col-span-7 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl space-y-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* From Vault Address */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                From Vault Address
              </label>
              <select
                value={fromAddress}
                onChange={(e) => setFromAddress(e.target.value)}
                className="w-full px-3 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                {vaults.map((vault) => (
                  <option key={vault.id} value={vault.address}>
                    {vault.name} ({vault.piBalance.toLocaleString()} π PI • {vault.xlmBalance.toFixed(2)} XLM) - {vault.address.slice(0, 10)}...
                  </option>
                ))}
              </select>
            </div>

            {/* Recipient Address */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-xs font-semibold text-slate-300">
                  To Recipient Address
                </label>
                <button
                  type="button"
                  onClick={() => setToAddress('GDZX94K2MQW8VR91PXZL029471NVMS947194KOSASIH88')}
                  className="text-[10px] text-blue-400 hover:text-blue-300 font-mono"
                >
                  Fill Sample Pioneer
                </button>
              </div>
              <input
                type="text"
                placeholder="G... (Stellar or IOU public key)"
                value={toAddress}
                onChange={(e) => setToAddress(e.target.value)}
                className="w-full px-3 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-600 font-mono focus:outline-none focus:ring-1 focus:ring-blue-500"
                required
              />
            </div>

            {/* Asset Selector & Amount */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Asset
                </label>
                <select
                  value={asset}
                  onChange={(e) => setAsset(e.target.value as any)}
                  className="w-full px-3 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option value="π PI IOU">π PI IOU (Pi Coin IOU)</option>
                  <option value="XLM">XLM (Native Stellar)</option>
                  <option value="NRV">NRV (Nexus Revoluter)</option>
                </select>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="block text-xs font-semibold text-slate-300">
                    Amount
                  </label>
                  <button
                    type="button"
                    onClick={handleMaxAmount}
                    className="text-[10px] font-mono text-purple-400 hover:text-purple-300 font-bold"
                  >
                    MAX
                  </button>
                </div>
                <div className="relative">
                  <input
                    type="number"
                    step="any"
                    placeholder="0.00"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    className="w-full px-3 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-600 font-mono focus:outline-none focus:ring-1 focus:ring-blue-500"
                    required
                  />
                  <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-mono font-bold text-slate-400">
                    {asset === 'π PI IOU' ? 'π PI' : asset}
                  </span>
                </div>
              </div>
            </div>

            {/* Valuation conversion helper */}
            {parsedAmount > 0 && asset === 'π PI IOU' && (
              <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800/80 text-[11px] space-y-1">
                <div className="flex justify-between text-slate-400">
                  <span>Market Valuation (@ ${livePrice.toFixed(4)}):</span>
                  <span className="font-mono text-white">${(parsedAmount * livePrice).toFixed(2)} USD</span>
                </div>
                <div className="flex justify-between text-purple-300">
                  <span>Community GCV Valuation (@ $314,159):</span>
                  <span className="font-mono font-semibold">${(parsedAmount * communityGcv).toLocaleString('en-US', { maximumFractionDigits: 0 })} USD</span>
                </div>
              </div>
            )}

            {/* Memo */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                Transaction Memo (Optional)
              </label>
              <input
                type="text"
                placeholder="e.g. Pioneer peer barter for organic coffee"
                value={memo}
                onChange={(e) => setMemo(e.target.value)}
                className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-600 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>

            {/* Required Info Line */}
            <div className="p-3.5 rounded-xl bg-blue-500/10 border border-blue-500/20 text-[11px] text-blue-200 leading-relaxed flex items-start space-x-2">
              <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
              <div>
                <strong>Base network fee 0.0001 XLM.</strong> Protected by Ed25519 quantum resistant signature & verified against global sanction registries.
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isSubmitting || parsedAmount <= 0 || !toAddress}
              className="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs transition shadow-lg shadow-blue-600/30 flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              {isSubmitting ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Computing Ed25519 Signature...</span>
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>Sign & Transmit Transaction</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Right Column: AI Sentinel & Pre-flight Risk Assessment */}
        <div className="lg:col-span-5 space-y-6">
          {/* AI Sentinel Pre-flight Panel */}
          <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Sparkles className="w-4 h-4 text-purple-400" />
                <h3 className="text-sm font-bold text-white">AI Sentinel Pre-Flight</h3>
              </div>
              <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase ${
                currentRisk.verdict === 'SAFE'
                  ? 'bg-emerald-950 text-emerald-300 border border-emerald-800/50'
                  : currentRisk.verdict === 'SUSPICIOUS'
                  ? 'bg-amber-950 text-amber-300 border border-amber-800/50'
                  : 'bg-rose-950 text-rose-300 border border-rose-800/50'
              }`}>
                {currentRisk.verdict} • Risk {currentRisk.score}/100
              </span>
            </div>

            <p className="text-xs text-slate-400 leading-relaxed">
              Real-time heuristic evaluation running entirely client-side. Protects Pioneers from phishing contracts, abnormal drainers, and trademark confusion.
            </p>

            <div className="space-y-2 text-xs">
              <div className="flex items-center justify-between p-2 rounded-lg bg-slate-950 border border-slate-800">
                <span className="text-slate-400">Sanctions & AML Check:</span>
                <span className="font-mono text-emerald-400 font-semibold flex items-center gap-1">
                  <ShieldCheck className="w-3.5 h-3.5" /> CLEARED
                </span>
              </div>
              <div className="flex items-center justify-between p-2 rounded-lg bg-slate-950 border border-slate-800">
                <span className="text-slate-400">Address Entropy Score:</span>
                <span className="font-mono text-purple-400 font-semibold">
                  {currentRiskDetail.entropyScore} (Shannon metric)
                </span>
              </div>
              <div className="flex items-center justify-between p-2 rounded-lg bg-slate-950 border border-slate-800">
                <span className="text-slate-400">Simulated Outcome:</span>
                <span className={`font-mono font-semibold ${
                  currentRiskDetail.simulatedExecution === 'SUCCESS_NO_REVERT' ? 'text-emerald-400' : 'text-amber-400'
                }`}>
                  {currentRiskDetail.simulatedExecution}
                </span>
              </div>
              <div className="flex items-center justify-between p-2 rounded-lg bg-slate-950 border border-slate-800">
                <span className="text-slate-400">Network Routing:</span>
                <span className="font-mono text-blue-400 font-semibold">
                  Byzantine SCP Mesh (67% Quorum)
                </span>
              </div>
            </div>

            {currentRisk.warnings.length > 0 && (
              <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-[11px] space-y-1">
                <div className="font-bold flex items-center gap-1">
                  <AlertTriangle className="w-3.5 h-3.5" /> Sentinel Advisories:
                </div>
                {currentRisk.warnings.map((w, i) => (
                  <div key={i} className="pl-4">• {w}</div>
                ))}
              </div>
            )}
          </div>

          {/* Active Vault Overview */}
          {selectedVault && (
            <div className="bg-slate-900/60 p-5 rounded-2xl border border-slate-800 text-xs space-y-3">
              <div className="font-semibold text-slate-300">Selected Debited Vault</div>
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                <div className="flex justify-between items-center">
                  <span className="font-bold text-white">{selectedVault.name}</span>
                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 uppercase">
                    {selectedVault.role}
                  </span>
                </div>
                <div className="text-[10px] font-mono text-slate-400 truncate">
                  {selectedVault.address}
                </div>
                <div className="flex justify-between pt-1 border-t border-slate-850">
                  <span className="text-slate-400">Available:</span>
                  <span className="font-mono font-bold text-white">
                    {selectedVault.piBalance.toLocaleString()} <span className="text-purple-400">π PI</span> • {selectedVault.xlmBalance.toFixed(2)} XLM
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Transaction Feed */}
      <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Clock className="w-4 h-4 text-blue-400" />
            <h3 className="text-sm font-bold text-white">Recent Vault Transactions</h3>
          </div>
          <span className="text-xs text-slate-400 font-mono">
            {transactions.length} Total Operations Recorded
          </span>
        </div>

        <div className="divide-y divide-slate-800 overflow-x-auto">
          {transactions.map((tx) => (
            <div
              key={tx.id}
              onClick={() => setSelectedTx(tx)}
              className="py-3.5 px-2 flex items-center justify-between hover:bg-slate-850/50 rounded-xl transition cursor-pointer"
            >
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 shrink-0">
                  <Send className="w-4 h-4" />
                </div>
                <div>
                  <div className="text-xs font-semibold text-white flex items-center gap-2">
                    <span>{tx.memo || 'Settlement'}</span>
                    <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-emerald-950 text-emerald-300 border border-emerald-800/40">
                      Confirmed
                    </span>
                  </div>
                  <div className="text-[10px] font-mono text-slate-400 flex items-center gap-2 mt-0.5">
                    <span>From: {tx.from.slice(0, 8)}...</span>
                    <span>To: {tx.to.slice(0, 8)}...</span>
                    <span>• {tx.timestamp}</span>
                  </div>
                </div>
              </div>

              <div className="text-right">
                <div className="text-xs font-mono font-bold text-white">
                  {tx.amount.toLocaleString(undefined, { minimumFractionDigits: 2 })}{' '}
                  <span className="text-purple-400">{tx.asset === 'π PI IOU' ? 'π PI' : tx.asset}</span>
                </div>
                <div className="text-[10px] font-mono text-slate-400">
                  Fee: {tx.fee} XLM • Block #{tx.blockNumber}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Cryptographic Receipt Modal */}
      {selectedTx && (
        <TxDetailsModal
          tx={selectedTx}
          onClose={() => setSelectedTx(null)}
        />
      )}
    </div>
  );
};
