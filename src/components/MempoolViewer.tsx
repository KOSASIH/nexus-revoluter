import React, { useState } from 'react';
import { Database, Zap, Clock, ShieldCheck, ArrowRight, CheckCircle2, SlidersHorizontal } from 'lucide-react';

interface MempoolTx {
  txId: string;
  from: string;
  to: string;
  amount: number;
  asset: 'π PI' | 'XLM' | 'NRV';
  fee: number;
  priority: 'low' | 'standard' | 'high';
  ageSec: number;
}

export const MempoolViewer: React.FC = () => {
  const [gasPriority, setGasPriority] = useState<'low' | 'standard' | 'high'>('standard');
  const [clearingMempool, setClearingMempool] = useState(false);
  const [clearedNotice, setClearedNotice] = useState<string | null>(null);

  const [pendingTxs, setPendingTxs] = useState<MempoolTx[]>([
    {
      txId: '0x9fa102b4819e...881',
      from: 'GDZX94K2...KOSASIH88',
      to: 'GDF71029...VALIDTR',
      amount: 45.0,
      asset: 'π PI',
      fee: 0.00012,
      priority: 'high',
      ageSec: 2
    },
    {
      txId: '0x3c819a7102b5...719',
      from: 'GABR72K1...REVOLUTER01',
      to: 'GCXP4491...NPASBRIDGE',
      amount: 150.0,
      asset: 'π PI',
      fee: 0.00010,
      priority: 'standard',
      ageSec: 4
    },
    {
      txId: '0x7b21908a1c94...302',
      from: 'GDZX94K2...KOSASIH88',
      to: 'GABR72K1...REVOLUTER01',
      amount: 25.0,
      asset: 'XLM',
      fee: 0.00008,
      priority: 'low',
      ageSec: 7
    },
    {
      txId: '0x10b94819a7b0...991',
      from: 'GCXP4491...NPASBRIDGE',
      to: 'GDF71029...VALIDTR',
      amount: 500.0,
      asset: 'NRV',
      fee: 0.00015,
      priority: 'high',
      ageSec: 1
    }
  ]);

  const handleSimulateMineMempool = () => {
    setClearingMempool(true);
    setTimeout(() => {
      const count = pendingTxs.length;
      setPendingTxs([]);
      setClearingMempool(false);
      setClearedNotice(`Validated & mined ${count} transactions from memory pool into local ledger sequence.`);
      setTimeout(() => {
        setClearedNotice(null);
        // Replenish with new pending transactions
        setPendingTxs([
          {
            txId: '0x' + Array.from({ length: 12 }, () => Math.floor(Math.random() * 16).toString(16)).join('') + '...',
            from: 'GDZX94K2...KOSASIH88',
            to: 'GABR72K1...REVOLUTER01',
            amount: 88.0,
            asset: 'π PI',
            fee: 0.00011,
            priority: 'standard',
            ageSec: 1
          }
        ]);
      }, 4000);
    }, 1000);
  };

  return (
    <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Database className="w-5 h-5 text-amber-400" />
            Unconfirmed Memory Pool (Mempool)
          </h3>
          <p className="text-xs text-slate-400">
            Transient queue of broadcast transactions awaiting SCP validation & ledger commitment
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <div className="flex bg-slate-950 p-1 rounded-lg border border-slate-800 text-[11px] font-medium">
            {(['low', 'standard', 'high'] as const).map((tier) => (
              <button
                key={tier}
                onClick={() => setGasPriority(tier)}
                className={`px-2.5 py-1 rounded-md capitalize transition ${
                  gasPriority === tier
                    ? 'bg-amber-600 text-white font-semibold'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {tier} Gas
              </button>
            ))}
          </div>

          <button
            onClick={handleSimulateMineMempool}
            disabled={clearingMempool || pendingTxs.length === 0}
            className="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-xs font-semibold text-white transition disabled:opacity-40 flex items-center gap-1.5"
          >
            <Zap className="w-3.5 h-3.5" />
            <span>{clearingMempool ? 'Mining...' : 'Mine Batch'}</span>
          </button>
        </div>
      </div>

      {clearedNotice && (
        <div className="p-3 rounded-xl bg-emerald-950/40 border border-emerald-800/60 text-emerald-300 text-xs flex items-center space-x-2">
          <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-400" />
          <span>{clearedNotice}</span>
        </div>
      )}

      {/* Mempool Stats Bar */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
        <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
          <span className="text-[10px] text-slate-500 uppercase font-semibold">Queued TXs</span>
          <div className="text-base font-mono font-bold text-white mt-0.5">{pendingTxs.length} pending</div>
        </div>
        <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
          <span className="text-[10px] text-slate-500 uppercase font-semibold">Mempool Size</span>
          <div className="text-base font-mono font-bold text-amber-400 mt-0.5">38.4 KB</div>
        </div>
        <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
          <span className="text-[10px] text-slate-500 uppercase font-semibold">Recommended Base Fee</span>
          <div className="text-base font-mono font-bold text-emerald-400 mt-0.5">
            {gasPriority === 'low' ? '0.00008' : gasPriority === 'standard' ? '0.00010' : '0.00018'} XLM
          </div>
        </div>
        <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
          <span className="text-[10px] text-slate-500 uppercase font-semibold">Avg Time in Pool</span>
          <div className="text-base font-mono font-bold text-blue-400 mt-0.5">3.2 seconds</div>
        </div>
      </div>

      {/* Pending TX list */}
      <div className="space-y-2">
        {pendingTxs.length === 0 ? (
          <div className="text-center py-8 text-xs text-slate-500 bg-slate-950/40 rounded-xl border border-slate-800">
            Memory pool is empty. All submitted transactions have been finalized on-chain.
          </div>
        ) : (
          pendingTxs.map((ptx) => (
            <div
              key={ptx.txId}
              className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 flex items-center justify-between text-xs"
            >
              <div className="flex items-center space-x-3 min-w-0">
                <span className="h-2 w-2 rounded-full bg-amber-400 animate-ping shrink-0" />
                <div className="min-w-0">
                  <div className="font-mono font-bold text-slate-200 truncate">{ptx.txId}</div>
                  <div className="text-[11px] text-slate-400 truncate">
                    {ptx.from} <span className="text-slate-600">→</span> {ptx.to}
                  </div>
                </div>
              </div>

              <div className="text-right shrink-0 ml-3">
                <div className="font-mono font-bold text-white">
                  +{ptx.amount.toLocaleString()} <span className="text-purple-400">{ptx.asset}</span>
                </div>
                <div className="text-[10px] text-slate-500 font-mono">
                  Fee: {ptx.fee} XLM • {ptx.ageSec}s ago
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
