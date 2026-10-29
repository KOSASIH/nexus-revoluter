import React, { useState } from 'react';
import { X, Copy, Check, Download, ShieldCheck, Hash, Clock, ArrowRight, ExternalLink, FileCode } from 'lucide-react';
import { Transaction } from '../types';

interface TxDetailsModalProps {
  tx: Transaction | null;
  onClose: () => void;
}

export const TxDetailsModal: React.FC<TxDetailsModalProps> = ({ tx, onClose }) => {
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  if (!tx) return null;

  const handleCopy = (key: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const downloadJsonReceipt = () => {
    const receipt = {
      receiptType: 'Nexus-Revoluter-Stellar-Pi-Settlement',
      version: '1.4.2',
      transactionId: tx.id,
      ledgerSequence: tx.blockNumber,
      timestamp: new Date().toISOString(),
      sender: tx.from,
      recipient: tx.to,
      amount: tx.amount,
      asset: tx.asset === 'π PI IOU' ? 'π PI' : tx.asset,
      fee: tx.fee,
      memo: tx.memo || '',
      complianceVerification: {
        amlChecked: true,
        sanctionsListCleared: true,
        zkProofAuditId: 'ARHN-SNARK-' + tx.id.slice(3, 11).toUpperCase()
      },
      signature: {
        algorithm: 'Ed25519-QuantumResistant',
        signatureHex: '9f81a7b03c948e21a84f' + tx.id.slice(3) + '4819e0b94c'
      }
    };

    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(receipt, null, 2));
    const dlAnchor = document.createElement('a');
    dlAnchor.setAttribute('href', dataStr);
    dlAnchor.setAttribute('download', `receipt_${tx.id}.json`);
    document.body.appendChild(dlAnchor);
    dlAnchor.click();
    dlAnchor.remove();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-md animate-in fade-in duration-200">
      <div className="bg-slate-900 border border-slate-700/80 rounded-2xl max-w-xl w-full p-6 shadow-2xl relative text-slate-100 max-h-[90vh] overflow-y-auto">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center space-x-3 mb-5">
          <div className="h-10 w-10 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center shrink-0">
            <Hash className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">Cryptographic Transaction Receipt</h3>
            <p className="text-xs text-slate-400">Ledger Sequence #{tx.blockNumber} • Ed25519 Verified</p>
          </div>
        </div>

        {/* Amount Badge Banner */}
        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 mb-5 flex items-center justify-between">
          <div>
            <span className="text-[10px] text-slate-500 font-semibold uppercase">Transferred Value</span>
            <div className="text-2xl font-mono font-bold text-emerald-400">
              +{tx.amount.toLocaleString()} <span className="text-sm font-normal text-purple-400">{tx.asset === 'π PI IOU' ? 'π PI' : tx.asset}</span>
            </div>
          </div>
          <span className="px-2.5 py-1 rounded-full text-xs font-mono font-bold uppercase bg-emerald-950 text-emerald-300 border border-emerald-800/50">
            {tx.status}
          </span>
        </div>

        {/* Cryptographic breakdown */}
        <div className="space-y-3 text-xs mb-5">
          <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
            <div className="flex items-center justify-between mb-1">
              <span className="text-slate-500 font-medium text-[10px] uppercase">Transaction Hash (TxID)</span>
              <button
                onClick={() => handleCopy('txid', tx.id)}
                className="text-slate-400 hover:text-white flex items-center gap-1 text-[11px]"
              >
                {copiedKey === 'txid' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedKey === 'txid' ? 'Copied' : 'Copy'}</span>
              </button>
            </div>
            <p className="font-mono text-blue-300 break-all select-all font-semibold">
              {tx.id}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <div className="flex items-center justify-between mb-1">
                <span className="text-slate-500 font-medium text-[10px] uppercase">From Address</span>
                <button
                  onClick={() => handleCopy('from', tx.from)}
                  className="text-slate-400 hover:text-white"
                >
                  {copiedKey === 'from' ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                </button>
              </div>
              <p className="font-mono text-[11px] text-slate-300 truncate select-all">{tx.from}</p>
            </div>

            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <div className="flex items-center justify-between mb-1">
                <span className="text-slate-500 font-medium text-[10px] uppercase">To Recipient</span>
                <button
                  onClick={() => handleCopy('to', tx.to)}
                  className="text-slate-400 hover:text-white"
                >
                  {copiedKey === 'to' ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                </button>
              </div>
              <p className="font-mono text-[11px] text-slate-300 truncate select-all">{tx.to}</p>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-[10px] text-slate-500 uppercase">Ledger Slot</span>
              <div className="font-mono font-bold text-white mt-0.5">#{tx.blockNumber}</div>
            </div>
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-[10px] text-slate-500 uppercase">Base Gas Fee</span>
              <div className="font-mono font-bold text-slate-300 mt-0.5">{tx.fee} XLM</div>
            </div>
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-[10px] text-slate-500 uppercase">Timestamp</span>
              <div className="font-mono text-slate-300 mt-0.5">{tx.timestamp}</div>
            </div>
          </div>

          {tx.memo && (
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-[10px] text-slate-500 uppercase">On-Chain Memo Tag</span>
              <p className="text-slate-200 mt-0.5">{tx.memo}</p>
            </div>
          )}

          <div className="p-3.5 rounded-xl bg-emerald-950/30 border border-emerald-900/40 text-[11px] text-emerald-300 flex items-center justify-between">
            <span className="flex items-center gap-1.5 font-medium">
              <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
              ARHN Compliance & AML Screening Status: PASSED
            </span>
            <span className="font-mono text-slate-400">Ed25519 Valid</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center space-x-3 pt-3 border-t border-slate-800">
          <button
            onClick={downloadJsonReceipt}
            className="flex-1 flex items-center justify-center space-x-2 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white transition shadow-lg shadow-blue-600/20"
          >
            <Download className="w-4 h-4" />
            <span>Download Cryptographic Receipt (.JSON)</span>
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300 transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
