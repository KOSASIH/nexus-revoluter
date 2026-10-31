import React, { useState } from 'react';
import { X, Copy, Check, QrCode, Key, ShieldCheck } from 'lucide-react';
import { VaultAccount } from '../types';

interface QrModalProps {
  address: VaultAccount | null;
  onClose: () => void;
}

export const QrModal: React.FC<QrModalProps> = ({ address, onClose }) => {
  const [copied, setCopied] = useState(false);

  if (!address) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(address.address);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-slate-900 border border-slate-700/80 rounded-2xl max-w-md w-full p-6 shadow-2xl relative text-slate-100">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="text-center mb-5">
          <div className="inline-flex p-3 rounded-2xl bg-blue-500/10 border border-blue-500/20 text-blue-400 mb-2">
            <QrCode className="w-7 h-7" />
          </div>
          <h3 className="text-base font-bold text-white">{address.name}</h3>
          <p className="text-xs text-slate-400">Scan to receive π NXS or Stellar assets</p>
        </div>

        {/* QR Code Graphic (SVG generated) */}
        <div className="bg-white p-5 rounded-2xl flex flex-col items-center justify-center mx-auto w-56 h-56 shadow-inner mb-5">
          <svg viewBox="0 0 100 100" className="w-full h-full text-slate-950">
            {/* Corner Markers */}
            <rect x="5" y="5" width="26" height="26" fill="black" rx="3" />
            <rect x="9" y="9" width="18" height="18" fill="white" rx="2" />
            <rect x="13" y="13" width="10" height="10" fill="black" rx="1" />

            <rect x="69" y="5" width="26" height="26" fill="black" rx="3" />
            <rect x="73" y="9" width="18" height="18" fill="white" rx="2" />
            <rect x="77" y="13" width="10" height="10" fill="black" rx="1" />

            <rect x="5" y="69" width="26" height="26" fill="black" rx="3" />
            <rect x="9" y="73" width="18" height="18" fill="white" rx="2" />
            <rect x="13" y="77" width="10" height="10" fill="black" rx="1" />

            {/* Pattern data blocks */}
            <rect x="37" y="7" width="6" height="6" fill="black" />
            <rect x="47" y="11" width="8" height="6" fill="black" />
            <rect x="59" y="7" width="6" height="8" fill="black" />
            
            <rect x="7" y="37" width="8" height="6" fill="black" />
            <rect x="19" y="47" width="6" height="8" fill="black" />
            <rect x="7" y="57" width="8" height="6" fill="black" />

            <rect x="32" y="35" width="36" height="30" fill="#0f172a" rx="6" />
            <text x="50" y="54" fontSize="9" fontWeight="bold" textAnchor="middle" fill="#c084fc" fontFamily="monospace">π NXS</text>

            <rect x="69" y="37" width="8" height="6" fill="black" />
            <rect x="81" y="45" width="6" height="8" fill="black" />
            <rect x="71" y="57" width="8" height="6" fill="black" />

            <rect x="37" y="71" width="8" height="6" fill="black" />
            <rect x="49" y="77" width="6" height="8" fill="black" />
            <rect x="59" y="69" width="8" height="8" fill="black" />
            <rect x="73" y="73" width="6" height="6" fill="black" />
            <rect x="83" y="81" width="8" height="8" fill="black" />
          </svg>
        </div>

        {/* Address String */}
        <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 mb-4">
          <div className="text-[11px] text-slate-400 font-medium mb-1">Public Address (Ed25519)</div>
          <p className="font-mono text-xs text-blue-300 break-all select-all font-semibold">
            {address.address}
          </p>
        </div>

        {/* Balance tags */}
        <div className="grid grid-cols-2 gap-3 mb-5">
          <div className="bg-slate-800/80 p-2.5 rounded-xl border border-slate-700/60">
            <div className="text-[10px] text-slate-400">π NXS Balance</div>
            <div className="text-sm font-mono font-bold text-purple-400">
              {address.piBalance.toLocaleString()} π NXS
            </div>
          </div>
          <div className="bg-slate-800/80 p-2.5 rounded-xl border border-slate-700/60">
            <div className="text-[10px] text-slate-400">Native XLM Balance</div>
            <div className="text-sm font-mono font-bold text-slate-200">
              {address.xlmBalance.toFixed(2)} XLM
            </div>
          </div>
        </div>

        {/* Action button */}
        <button
          onClick={handleCopy}
          className="w-full flex items-center justify-center space-x-2 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 font-semibold text-xs text-white transition shadow-lg shadow-blue-600/20"
        >
          {copied ? <Check className="w-4 h-4 text-emerald-300" /> : <Copy className="w-4 h-4" />}
          <span>{copied ? 'Address Copied to Clipboard!' : 'Copy Full Address'}</span>
        </button>
      </div>
    </div>
  );
};
