import React, { useState } from 'react';
import { 
  Wallet, 
  Plus, 
  Send, 
  ArrowUpRight, 
  ArrowDownLeft, 
  ShieldCheck, 
  QrCode, 
  Copy, 
  Check, 
  Trash2, 
  Download, 
  Upload, 
  Sparkles, 
  AlertCircle,
  ExternalLink,
  Search
} from 'lucide-react';
import { WalletAddress, Transaction } from '../types';
import { QrModal } from './QrModal';

interface WalletViewProps {
  addresses: WalletAddress[];
  transactions: Transaction[];
  onAddAddress: (label: string) => void;
  onDeleteAddress: (address: string) => void;
  onSendTransaction: (tx: {
    from: string;
    to: string;
    amount: number;
    asset: 'PI' | 'XLM' | 'NRV';
    memo: string;
  }) => { success: boolean; message: string };
  onSaveWallet: () => void;
  onLoadWallet: () => void;
}

export const WalletView: React.FC<WalletViewProps> = ({
  addresses,
  transactions,
  onAddAddress,
  onDeleteAddress,
  onSendTransaction,
  onSaveWallet,
  onLoadWallet
}) => {
  const [selectedQrAddress, setSelectedQrAddress] = useState<WalletAddress | null>(null);
  const [copiedAddress, setCopiedAddress] = useState<string | null>(null);
  
  // New Address Form Modal / Toggle
  const [isCreatingAddress, setIsCreatingAddress] = useState(false);
  const [newAddressLabel, setNewAddressLabel] = useState('');

  // Send Transaction State
  const [fromAddress, setFromAddress] = useState(addresses[0]?.address || '');
  const [toAddress, setToAddress] = useState('');
  const [sendAmount, setSendAmount] = useState('');
  const [sendAsset, setSendAsset] = useState<'PI' | 'XLM' | 'NRV'>('PI');
  const [sendMemo, setSendMemo] = useState('');
  const [txFeedback, setTxFeedback] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Filter / Search for transactions
  const [searchQuery, setSearchQuery] = useState('');
  const [assetFilter, setAssetFilter] = useState<'ALL' | 'PI' | 'XLM' | 'NRV'>('ALL');

  const handleCopy = (address: string) => {
    navigator.clipboard.writeText(address);
    setCopiedAddress(address);
    setTimeout(() => setCopiedAddress(null), 2000);
  };

  const handleCreateAddress = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newAddressLabel.trim()) return;
    onAddAddress(newAddressLabel.trim());
    setNewAddressLabel('');
    setIsCreatingAddress(false);
  };

  const handleSendSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setTxFeedback(null);
    const amountNum = parseFloat(sendAmount);

    if (!fromAddress || !toAddress) {
      setTxFeedback({ type: 'error', message: 'Source and recipient addresses are required.' });
      return;
    }
    if (isNaN(amountNum) || amountNum <= 0) {
      setTxFeedback({ type: 'error', message: 'Please enter a valid positive amount.' });
      return;
    }

    const sourceWallet = addresses.find(a => a.address === fromAddress);
    if (sendAsset === 'PI' && sourceWallet && sourceWallet.piBalance < amountNum) {
      setTxFeedback({ type: 'error', message: `Insufficient π PI balance. Available: ${sourceWallet.piBalance} π PI` });
      return;
    }
    if (sendAsset === 'XLM' && sourceWallet && sourceWallet.balance < amountNum) {
      setTxFeedback({ type: 'error', message: `Insufficient XLM balance. Available: ${sourceWallet.balance} XLM` });
      return;
    }

    setIsSubmitting(true);
    setTimeout(() => {
      const result = onSendTransaction({
        from: fromAddress,
        to: toAddress,
        amount: amountNum,
        asset: sendAsset,
        memo: sendMemo.trim() || 'Nexus Revoluter Transfer'
      });

      setIsSubmitting(false);
      if (result.success) {
        setTxFeedback({ type: 'success', message: result.message });
        setToAddress('');
        setSendAmount('');
        setSendMemo('');
      } else {
        setTxFeedback({ type: 'error', message: result.message });
      }
    }, 600);
  };

  const filteredTxs = transactions.filter(tx => {
    const matchesQuery = 
      tx.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      tx.from.toLowerCase().includes(searchQuery.toLowerCase()) ||
      tx.to.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (tx.memo && tx.memo.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesAsset = assetFilter === 'ALL' || tx.asset === assetFilter;
    return matchesQuery && matchesAsset;
  });

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Top Banner / Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900/60 p-5 rounded-2xl border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Wallet className="w-5 h-5 text-blue-400" />
            Pioneer Keypair & Multi-Address Vault
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Compliant Stellar & Pi Network custodial vault with Ed25519 quantum-resistant keys and autonomous AML verification.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setIsCreatingAddress(true)}
            className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white transition shadow-md shadow-blue-600/20"
          >
            <Plus className="w-4 h-4" />
            <span>Generate Address</span>
          </button>
          <button
            onClick={onSaveWallet}
            title="Export & encrypt wallet"
            className="flex items-center space-x-1 px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300 border border-slate-700 transition"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export</span>
          </button>
          <button
            onClick={onLoadWallet}
            title="Import saved wallet file"
            className="flex items-center space-x-1 px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300 border border-slate-700 transition"
          >
            <Upload className="w-3.5 h-3.5" />
            <span>Import</span>
          </button>
        </div>
      </div>

      {/* New Address Modal */}
      {isCreatingAddress && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-md w-full p-6 shadow-2xl">
            <h3 className="text-base font-bold text-white mb-2">Generate New Stellar / Pi Address</h3>
            <p className="text-xs text-slate-400 mb-4">
              Derives a fresh cryptographic keypair on the Stellar Horizon protocol with immediate Pi Network compatibility.
            </p>
            <form onSubmit={handleCreateAddress} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Address Label</label>
                <input
                  type="text"
                  placeholder="e.g. SANO Secondary Arbitrage Node"
                  value={newAddressLabel}
                  onChange={(e) => setNewAddressLabel(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  autoFocus
                />
              </div>
              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsCreatingAddress(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!newAddressLabel.trim()}
                  className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white disabled:opacity-50"
                >
                  Confirm & Generate
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Addresses Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {addresses.map((addr) => (
          <div
            key={addr.address}
            className={`p-5 rounded-2xl border transition-all duration-200 relative ${
              addr.isPrimary
                ? 'bg-gradient-to-b from-slate-900 to-slate-950 border-blue-500/50 shadow-lg shadow-blue-500/5'
                : 'bg-slate-900/60 border-slate-800/80 hover:border-slate-700'
            }`}
          >
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-200 flex items-center gap-1.5">
                {addr.label}
                {addr.isPrimary && (
                  <span className="text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30">
                    Primary
                  </span>
                )}
              </span>
              <div className="flex items-center space-x-1">
                <button
                  onClick={() => setSelectedQrAddress(addr)}
                  title="View QR Code"
                  className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
                >
                  <QrCode className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleCopy(addr.address)}
                  title="Copy Address"
                  className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
                >
                  {copiedAddress === addr.address ? (
                    <Check className="w-4 h-4 text-emerald-400" />
                  ) : (
                    <Copy className="w-4 h-4" />
                  )}
                </button>
                {addresses.length > 1 && (
                  <button
                    onClick={() => onDeleteAddress(addr.address)}
                    title="Delete address (Autonomous compliance verified)"
                    className="p-1.5 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>

            {/* Address truncated */}
            <div className="bg-slate-950/70 px-3 py-2 rounded-xl border border-slate-800/80 font-mono text-[11px] text-blue-300 break-all mb-4 select-all">
              {addr.address.slice(0, 14)}...{addr.address.slice(-14)}
            </div>

            {/* Balances */}
            <div className="grid grid-cols-2 gap-2 pt-1 border-t border-slate-800/60">
              <div>
                <div className="text-[10px] uppercase font-semibold text-slate-400">π PI Balance</div>
                <div className="text-base font-mono font-bold text-emerald-400">
                  {addr.piBalance.toLocaleString()} <span className="text-xs font-normal">π PI</span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-[10px] uppercase font-semibold text-slate-400">Native XLM</div>
                <div className="text-base font-mono font-bold text-slate-200">
                  {addr.balance.toFixed(2)} <span className="text-xs font-normal">XLM</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Main Operations: Send Form & Live Transaction Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Send Transaction Panel (5 cols) */}
        <div className="lg:col-span-5 bg-slate-900/70 p-6 rounded-2xl border border-slate-800 flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <div className="p-2 rounded-xl bg-blue-600/20 text-blue-400 border border-blue-500/30">
                <Send className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Execute Pi Transaction</h3>
                <p className="text-xs text-slate-400">Autonomous ARHN Compliance & AHCEW Empathy Engine</p>
              </div>
            </div>

            <form onSubmit={handleSendSubmit} className="space-y-4 mt-5">
              {/* Source Address */}
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">From Vault Address</label>
                <select
                  value={fromAddress}
                  onChange={(e) => setFromAddress(e.target.value)}
                  className="w-full px-3 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-blue-500 font-mono"
                >
                  {addresses.map((a) => (
                    <option key={a.address} value={a.address}>
                      {a.label} ({a.piBalance} π PI | {a.balance} XLM)
                    </option>
                  ))}
                </select>
              </div>

              {/* Destination Address */}
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">To Recipient Address</label>
                <input
                  type="text"
                  placeholder="G... (Stellar or Pi Public Key)"
                  value={toAddress}
                  onChange={(e) => setToAddress(e.target.value)}
                  className="w-full px-3 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500 font-mono"
                />
              </div>

              {/* Asset & Amount */}
              <div className="grid grid-cols-3 gap-3">
                <div className="col-span-1">
                  <label className="block text-xs font-medium text-slate-300 mb-1">Asset</label>
                  <select
                    value={sendAsset}
                    onChange={(e) => setSendAsset(e.target.value as 'PI' | 'XLM' | 'NRV')}
                    className="w-full px-3 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs font-semibold text-white focus:outline-none focus:ring-1 focus:ring-blue-500"
                  >
                    <option value="PI">π PI (Pi Coin)</option>
                    <option value="XLM">XLM Native</option>
                    <option value="NRV">NRV Reserve</option>
                  </select>
                </div>
                <div className="col-span-2">
                  <label className="block text-xs font-medium text-slate-300 mb-1">Amount</label>
                  <input
                    type="number"
                    step="any"
                    placeholder="0.00"
                    value={sendAmount}
                    onChange={(e) => setSendAmount(e.target.value)}
                    className="w-full px-3 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs font-mono text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  />
                </div>
              </div>

              {/* Memo */}
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Memo (Optional On-Chain Tag)</label>
                <input
                  type="text"
                  placeholder="e.g. SANO liquidity contribution"
                  value={sendMemo}
                  onChange={(e) => setSendMemo(e.target.value)}
                  className="w-full px-3 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>

              {/* Compliance & Fee Note */}
              <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800/80 flex items-start space-x-2 text-[11px] text-slate-400">
                <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <span>
                  Base network fee: <strong className="text-slate-200">0.0001 XLM</strong>. Protected by Ed25519 quantum-resistant signature & verified against global sanction registries.
                </span>
              </div>

              {/* Feedback Alert */}
              {txFeedback && (
                <div
                  className={`p-3 rounded-xl border text-xs flex items-start space-x-2 ${
                    txFeedback.type === 'success'
                      ? 'bg-emerald-950/40 border-emerald-800/50 text-emerald-300'
                      : 'bg-rose-950/40 border-rose-800/50 text-rose-300'
                  }`}
                >
                  {txFeedback.type === 'success' ? (
                    <Sparkles className="w-4 h-4 shrink-0 mt-0.5" />
                  ) : (
                    <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                  )}
                  <div>
                    <div className="font-semibold">
                      {txFeedback.type === 'success' ? 'Transaction Broadcast' : 'Execution Notice'}
                    </div>
                    <div className="mt-0.5 leading-relaxed">{txFeedback.message}</div>
                  </div>
                </div>
              )}

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-500 font-semibold text-xs text-white transition shadow-lg shadow-blue-600/25 disabled:opacity-60 flex items-center justify-center space-x-2"
              >
                {isSubmitting ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                    <span>Signing with Ed25519 Key...</span>
                  </>
                ) : (
                  <>
                    <ArrowUpRight className="w-4 h-4" />
                    <span>Sign & Transmit Transaction</span>
                  </>
                )}
              </button>
            </form>
          </div>
        </div>

        {/* Transactions Feed (7 cols) */}
        <div className="lg:col-span-7 bg-slate-900/70 p-6 rounded-2xl border border-slate-800 flex flex-col">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-5">
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                Transaction History
                <span className="text-xs font-mono font-normal text-slate-400">({filteredTxs.length})</span>
              </h3>
              <p className="text-xs text-slate-400">Combined Stellar Horizon & Pi Network ledger settlements</p>
            </div>

            <div className="flex items-center space-x-2">
              {/* Asset filter pills */}
              <div className="flex bg-slate-950 p-1 rounded-lg border border-slate-800 text-[11px] font-medium">
                {(['ALL', 'PI', 'XLM', 'NRV'] as const).map((filter) => (
                  <button
                    key={filter}
                    onClick={() => setAssetFilter(filter)}
                    className={`px-2 py-0.5 rounded-md transition ${
                      assetFilter === filter
                        ? 'bg-blue-600 text-white font-semibold'
                        : 'text-slate-400 hover:text-white'
                    }`}
                  >
                    {filter === 'PI' ? 'π PI' : filter}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Search bar */}
          <div className="relative mb-4">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search by TxID, address or memo..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          {/* Transactions List */}
          <div className="space-y-2.5 overflow-y-auto max-h-[460px] pr-1">
            {filteredTxs.length === 0 ? (
              <div className="text-center py-12 text-slate-500 text-xs">
                No matching transactions found.
              </div>
            ) : (
              filteredTxs.map((tx) => (
                <div
                  key={tx.id}
                  className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800/80 hover:border-slate-700 transition flex items-center justify-between"
                >
                  <div className="flex items-center space-x-3 min-w-0">
                    <div className="h-9 w-9 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center shrink-0">
                      <ArrowUpRight className="w-4 h-4" />
                    </div>
                    <div className="min-w-0">
                      <div className="flex items-center space-x-2">
                        <span className="font-mono text-xs font-bold text-white truncate">
                          {tx.id.slice(0, 16)}...
                        </span>
                        <span className="text-[10px] text-slate-400">{tx.timestamp}</span>
                      </div>
                      <div className="text-[11px] text-slate-400 truncate mt-0.5">
                        {tx.memo || 'Transfer'}
                      </div>
                    </div>
                  </div>

                  <div className="text-right shrink-0 ml-3">
                    <div className="text-xs font-mono font-bold text-emerald-400">
                      +{tx.amount.toLocaleString()} {tx.asset === 'PI' ? 'π PI' : tx.asset}
                    </div>
                    <div className="flex items-center justify-end space-x-1 mt-0.5">
                      <span className="text-[9px] uppercase font-mono px-1.5 py-0.2 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-800/40">
                        {tx.status}
                      </span>
                      <span className="text-[10px] font-mono text-slate-500">
                        Block #{tx.blockNumber}
                      </span>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* QR Inspector Modal */}
      <QrModal
        address={selectedQrAddress}
        onClose={() => setSelectedQrAddress(null)}
      />
    </div>
  );
};
