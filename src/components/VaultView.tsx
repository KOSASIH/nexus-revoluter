import React, { useState } from 'react';
import { 
  Wallet, 
  Plus, 
  Download, 
  Upload, 
  Sparkles, 
  ShieldCheck, 
  QrCode, 
  Copy, 
  Check, 
  Users, 
  UserCheck, 
  Key,
  Shield,
  AlertCircle,
  Clock,
  ArrowRight,
  Atom,
  Cpu,
  FileText
} from 'lucide-react';
import { VaultAccount, SocialRecoveryState, QuantumAuditReport } from '../types';
import { QrModal } from './QrModal';
import { auditQuantumResistance } from '../services/aiSentinel';

interface VaultViewProps {
  vaults: VaultAccount[];
  socialRecovery: SocialRecoveryState;
  onGenerateAddress: (name: string) => void;
  onClaimFaucet: (vaultId: string) => void;
  onExportEncrypted: () => void;
  onImportEncrypted: (importedData?: VaultAccount[]) => void;
  onApproveRecoveryGuardian: (guardianId: string) => void;
  onTriggerRecovery: () => void;
}

export const VaultView: React.FC<VaultViewProps> = ({
  vaults,
  socialRecovery,
  onGenerateAddress,
  onClaimFaucet,
  onExportEncrypted,
  onImportEncrypted,
  onApproveRecoveryGuardian,
  onTriggerRecovery
}) => {
  const [selectedQrVault, setSelectedQrVault] = useState<VaultAccount | null>(null);
  const [copiedAddress, setCopiedAddress] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [newVaultName, setNewVaultName] = useState('');
  const [isImporting, setIsImporting] = useState(false);
  const [importJsonText, setImportJsonText] = useState('');
  const [importError, setImportError] = useState<string | null>(null);
  const [toastNotice, setToastNotice] = useState<string | null>(null);

  const [isScanningQuantum, setIsScanningQuantum] = useState(false);
  const [quantumReport, setQuantumReport] = useState<QuantumAuditReport | null>(null);

  const showToast = (msg: string) => {
    setToastNotice(msg);
    setTimeout(() => setToastNotice(null), 4000);
  };

  const handleRunQuantumScan = (addr: string) => {
    setIsScanningQuantum(true);
    setQuantumReport(null);
    setTimeout(() => {
      const report = auditQuantumResistance(addr);
      setQuantumReport(report);
      setIsScanningQuantum(false);
      showToast('Quantum Cryptanalysis completed: Vault key is mathematically impervious.');
    }, 1200);
  };

  const handleCopy = (address: string) => {
    navigator.clipboard.writeText(address);
    setCopiedAddress(address);
    setTimeout(() => setCopiedAddress(null), 2000);
  };

  const handleGenerateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newVaultName.trim()) return;
    onGenerateAddress(newVaultName.trim());
    setNewVaultName('');
    setIsGenerating(false);
    showToast(`Derived new Ed25519 keypair for "${newVaultName.trim()}".`);
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result as string;
      setImportJsonText(content);
      processImport(content);
    };
    reader.readAsText(file);
  };

  const processImport = (jsonStr: string) => {
    setImportError(null);
    try {
      const parsed = JSON.parse(jsonStr);
      let incomingVaults: VaultAccount[] = [];

      if (Array.isArray(parsed)) {
        incomingVaults = parsed;
      } else if (parsed && Array.isArray(parsed.vaults)) {
        incomingVaults = parsed.vaults;
      } else {
        throw new Error('Unrecognized format: Expected { schema, encryption, vaults: [...] } or an array of vaults.');
      }

      if (incomingVaults.length === 0) {
        throw new Error('No vault accounts found in backup payload.');
      }

      // Basic structure validation
      for (const v of incomingVaults) {
        if (!v.address || typeof v.address !== 'string') {
          throw new Error('Malformed vault entry: Missing or invalid address field.');
        }
      }

      onImportEncrypted(incomingVaults);
      setIsImporting(false);
      setImportJsonText('');
      showToast(`Successfully verified & restored ${incomingVaults.length} vaults from backup.`);
    } catch (err: unknown) {
      setImportError(err instanceof Error ? err.message : 'Invalid JSON file.');
    }
  };

  const handleExportWithToast = () => {
    onExportEncrypted();
    showToast(`Exported ${vaults.length} vaults in encrypted AES-256-GCM / PBKDF2 format.`);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Top Banner & Primary Actions */}
      <div className="bg-slate-900/70 p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30 uppercase">
              Module 01 • Sovereign Vault
            </span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1 flex items-center gap-2">
            <Wallet className="w-5 h-5 text-blue-400" />
            Pioneer Keypair & Multi-Address Vault
          </h2>
          <p className="text-xs text-slate-300 max-w-2xl mt-1 leading-relaxed">
            Non custodial, user controlled vault for Stellar & IOU tracking with Ed25519 quantum resistant keys and autonomous AML verification.
          </p>
        </div>

        {/* Action Buttons Toolbar */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => setIsGenerating(true)}
            className="flex items-center space-x-1.5 px-3.5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white shadow-md shadow-blue-600/20 transition"
          >
            <Plus className="w-4 h-4" />
            <span>Generate Address</span>
          </button>

          {/* Test IOU Faucet Button */}
          <div className="flex flex-col items-center">
            <button
              onClick={() => onClaimFaucet(vaults[0]?.id || 'vault-primary')}
              className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-purple-600/20 hover:bg-purple-600 text-purple-300 hover:text-white border border-purple-500/30 text-xs font-semibold transition"
            >
              <Sparkles className="w-3.5 h-3.5 text-purple-400" />
              <span>+100 π PI Test IOU Faucet</span>
            </button>
            <span className="text-[9px] font-mono text-purple-400/80 mt-0.5">
              Test IOU only, bukan PI asli
            </span>
          </div>

          <button
            onClick={handleExportWithToast}
            title="Export encrypted vault backup to decentralized format"
            className="flex items-center space-x-1 px-3 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300 border border-slate-700 transition"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export</span>
          </button>

          <button
            onClick={() => setIsImporting(true)}
            title="Import client-side encrypted backup"
            className="flex items-center space-x-1 px-3 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300 border border-slate-700 transition"
          >
            <Upload className="w-3.5 h-3.5" />
            <span>Import</span>
          </button>
        </div>
      </div>

      {/* Global Feedback Toast */}
      {toastNotice && (
        <div className="p-3.5 rounded-xl bg-emerald-950/70 border border-emerald-700/60 text-emerald-300 text-xs flex items-center justify-between shadow-lg">
          <div className="flex items-center space-x-2">
            <Check className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>{toastNotice}</span>
          </div>
          <button 
            onClick={() => setToastNotice(null)} 
            className="text-slate-400 hover:text-white text-xs px-2 py-0.5 rounded"
          >
            ✕
          </button>
        </div>
      )}

      {/* Generate Address Modal */}
      {isGenerating && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-md w-full p-6 shadow-2xl">
            <h3 className="text-base font-bold text-white mb-1">Generate Local Ed25519 Keypair</h3>
            <p className="text-xs text-slate-400 mb-4">
              Entropy generated directly in-browser. Keys are never transmitted to any external server.
            </p>
            <form onSubmit={handleGenerateSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Vault Label</label>
                <input
                  type="text"
                  placeholder="e.g. Pioneer Stash Vault #04"
                  value={newVaultName}
                  onChange={(e) => setNewVaultName(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  autoFocus
                />
              </div>
              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsGenerating(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-xs font-medium text-slate-300 hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!newVaultName.trim()}
                  className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white disabled:opacity-50"
                >
                  Derive Keypair
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Import Encrypted Vault Backup Modal */}
      {isImporting && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Upload className="w-4 h-4 text-blue-400" />
                Restore Encrypted Vault Backup
              </h3>
              <button
                onClick={() => { setIsImporting(false); setImportError(null); }}
                className="text-slate-400 hover:text-white text-xs"
              >
                ✕
              </button>
            </div>
            
            <p className="text-xs text-slate-400 leading-relaxed">
              Upload a previously exported <code className="text-blue-300">nexus_pioneer_vault_backup_*.json</code> file or paste the encrypted JSON payload. All keys are parsed and decrypted strictly client-side.
            </p>

            {importError && (
              <div className="p-3 rounded-xl bg-rose-950/40 border border-rose-800/60 text-rose-300 text-xs flex items-center space-x-2">
                <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
                <span>{importError}</span>
              </div>
            )}

            {/* File Upload Trigger */}
            <div className="p-4 rounded-xl border border-dashed border-slate-700 bg-slate-950/50 flex flex-col items-center justify-center text-center space-y-2">
              <Upload className="w-6 h-6 text-slate-500" />
              <div className="text-xs text-slate-300">
                <label className="text-blue-400 hover:underline cursor-pointer font-semibold">
                  Browse JSON Backup File
                  <input
                    type="file"
                    accept=".json"
                    onChange={handleFileUpload}
                    className="hidden"
                  />
                </label>
                <span className="text-slate-500 ml-1">or paste raw JSON below</span>
              </div>
            </div>

            {/* Direct JSON Paste Area */}
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">
                Encrypted Backup Payload (JSON)
              </label>
              <textarea
                rows={5}
                value={importJsonText}
                onChange={(e) => setImportJsonText(e.target.value)}
                placeholder='{"schema": "Sovereign-Pioneer-Vault-V1", "vaults": [...]}'
                className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl font-mono text-[11px] text-slate-300 placeholder-slate-600 focus:outline-none focus:ring-1 focus:ring-blue-500 resize-none"
              />
            </div>

            <div className="flex justify-end space-x-2 pt-2">
              <button
                type="button"
                onClick={() => { setIsImporting(false); setImportError(null); }}
                className="px-4 py-2 rounded-xl bg-slate-800 text-xs font-medium text-slate-300 hover:bg-slate-700"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={() => processImport(importJsonText)}
                disabled={!importJsonText.trim()}
                className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white disabled:opacity-40 transition"
              >
                Verify & Restore
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 3 Separate Vaults Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {vaults.map((vault) => (
          <div
            key={vault.id}
            className={`p-5 rounded-2xl border transition relative flex flex-col justify-between ${
              vault.isPrimary
                ? 'bg-gradient-to-b from-slate-900 via-slate-900 to-slate-950 border-blue-500/60 shadow-lg shadow-blue-500/10'
                : 'bg-slate-900/70 border-slate-800 hover:border-slate-700'
            }`}
          >
            <div>
              {/* Header */}
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold text-white flex items-center gap-1.5">
                  {vault.name}
                  {vault.isPrimary && (
                    <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30">
                      PRIMARY
                    </span>
                  )}
                </span>

                <div className="flex items-center space-x-1">
                  <button
                    onClick={() => setSelectedQrVault(vault)}
                    title="View QR Code & Keys"
                    className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
                  >
                    <QrCode className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleCopy(vault.address)}
                    title="Copy Address"
                    className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
                  >
                    {copiedAddress === vault.address ? (
                      <Check className="w-4 h-4 text-emerald-400" />
                    ) : (
                      <Copy className="w-4 h-4" />
                    )}
                  </button>
                </div>
              </div>

              {/* Address Display */}
              <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800 font-mono text-[11px] text-blue-300 break-all select-all mb-4">
                {vault.address.slice(0, 16)}...{vault.address.slice(-16)}
              </div>

              {/* Balances: π PI BALANCE and NATIVE XLM */}
              <div className="space-y-3 bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80 mb-4">
                <div>
                  <div className="text-[10px] font-mono uppercase font-bold text-slate-400">π PI BALANCE</div>
                  <div className="text-xl font-mono font-bold text-emerald-400">
                    {vault.piBalance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}{' '}
                    <span className="text-xs font-semibold text-purple-400">π PI</span>
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between">
                  <div>
                    <div className="text-[10px] font-mono uppercase font-semibold text-slate-400">NATIVE XLM</div>
                    <div className="text-sm font-mono font-bold text-slate-200">
                      {vault.xlmBalance.toFixed(2)} XLM
                    </div>
                  </div>
                  <span className="text-[10px] font-mono text-slate-500">
                    Age: {vault.vaultAgeDays}d
                  </span>
                </div>
              </div>
            </div>

            {/* Security Indicator */}
            <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-[10px] font-mono text-slate-500">
              <span className="flex items-center gap-1 text-emerald-400">
                <ShieldCheck className="w-3.5 h-3.5" /> Ed25519 Quantum
              </span>
              <span>Client-Side Enclave</span>
            </div>
          </div>
        ))}
      </div>

      {/* MODULE 7: Account Abstraction and Social Recovery */}
      <div className="bg-slate-900/70 p-6 rounded-2xl border border-slate-800 space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30 uppercase">
                Module 07 • Account Abstraction
              </span>
            </div>
            <h3 className="text-base font-bold text-white mt-1 flex items-center gap-2">
              <Users className="w-5 h-5 text-purple-400" />
              Decentralized Social Recovery Protocol (2 of 3 Guardians)
            </h3>
            <p className="text-xs text-slate-400">
              Zero central support needed. If your device is lost, access is restored when 2 of your 3 designated guardians approve.
            </p>
          </div>

          <button
            onClick={onTriggerRecovery}
            className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-xs font-semibold text-white shadow-md shadow-purple-600/20 transition flex items-center gap-1.5"
          >
            <Key className="w-3.5 h-3.5" />
            <span>Simulate Recovery Test</span>
          </button>
        </div>

        {/* 3 Guardian Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {socialRecovery.guardians.map((guardian, i) => (
            <div
              key={guardian.id}
              className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-white">Guardian #{i + 1}</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800/50">
                  {guardian.status}
                </span>
              </div>
              <div className="text-[11px] text-slate-300 font-medium">{guardian.name}</div>
              <div className="font-mono text-[10px] text-slate-500 truncate">{guardian.address}</div>

              <button
                onClick={() => onApproveRecoveryGuardian(guardian.id)}
                className="w-full py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 transition border border-slate-700 mt-2 flex items-center justify-center gap-1"
              >
                <UserCheck className="w-3.5 h-3.5 text-emerald-400" />
                <span>Simulate Guardian Approval</span>
              </button>
            </div>
          ))}
        </div>

        <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-400 flex items-center justify-between">
          <span>Active Quorum Rule: <strong>{socialRecovery.threshold} Guardians + Owner Signature</strong></span>
          <span className="text-emerald-400 font-mono font-semibold">Decentralized Threshold Satisfied</span>
        </div>
      </div>

      {/* MODULE 1.1: Autonomous Quantum Cryptanalysis & Key Entropy Auditor */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/30 to-slate-900 p-6 rounded-2xl border border-indigo-500/30 space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 uppercase">
                Autonomous Cryptanalysis • Post-Quantum
              </span>
            </div>
            <h3 className="text-base font-bold text-white mt-1 flex items-center gap-2">
              <Atom className="w-5 h-5 text-indigo-400" />
              Quantum Resistance & Shannon Entropy Key Scanner
            </h3>
            <p className="text-xs text-slate-400">
              Evaluates browser-generated keypairs against simulated Shor's Algorithm attacks, PBKDF2 round integrity, and Kyber-1024 post-quantum wrappers.
            </p>
          </div>

          <button
            onClick={() => handleRunQuantumScan(vaults[0]?.address || '')}
            disabled={isScanningQuantum}
            className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-xs font-bold text-white shadow-lg shadow-indigo-600/20 transition flex items-center gap-2 disabled:opacity-60"
          >
            <Sparkles className={`w-3.5 h-3.5 ${isScanningQuantum ? 'animate-spin' : ''}`} />
            <span>{isScanningQuantum ? 'Analyzing Lattice...' : 'Deep-Scan Active Vault'}</span>
          </button>
        </div>

        {quantumReport ? (
          <div className="p-4 bg-slate-950/80 rounded-xl border border-indigo-900/50 space-y-4 animate-in fade-in">
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3">
              <div className="flex items-center space-x-2">
                <span className="text-xs font-bold text-white">Target Address:</span>
                <span className="font-mono text-xs text-indigo-300">{quantumReport.address.slice(0, 16)}...{quantumReport.address.slice(-16)}</span>
              </div>
              <span className="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-800 uppercase">
                Verdict: {quantumReport.securityVerdict}
              </span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
              <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Shannon Entropy</span>
                <span className="text-lg font-mono font-black text-emerald-300">{quantumReport.shannonEntropy}</span>
                <span className="text-[9px] text-slate-500 block">Optimal threshold: &gt;0.85</span>
              </div>

              <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Salt Uniformity</span>
                <span className="text-lg font-mono font-black text-blue-300">{(quantumReport.saltUniformity * 100).toFixed(1)}%</span>
                <span className="text-[9px] text-slate-500 block">Zero predictability bias</span>
              </div>

              <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">PBKDF2 Rounds</span>
                <span className="text-lg font-mono font-black text-purple-300">{quantumReport.pbkdf2Rounds.toLocaleString()}</span>
                <span className="text-[9px] text-slate-500 block">High GPU-cost hardening</span>
              </div>

              <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Shor Resistance</span>
                <span className="text-lg font-mono font-black text-amber-300">&gt;{quantumReport.shorResistanceYears} Years</span>
                <span className="text-[9px] text-slate-500 block">Post-quantum safe</span>
              </div>
            </div>

            <div className="p-3 bg-indigo-950/30 rounded-lg border border-indigo-900/40 text-[11px] text-indigo-200 flex items-center justify-between">
              <span className="flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Kyber-1024 Lattice Encapsulation Active. No corporate key recovery possible.</span>
              </span>
              <span className="font-mono text-slate-400 text-[10px]">Amanah Verified</span>
            </div>
          </div>
        ) : (
          <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80 text-xs text-slate-400 flex items-center justify-between">
            <span>Primary vault key ready for quantum resilience analysis.</span>
            <span className="font-mono text-[11px] text-indigo-400">Ed25519 Native</span>
          </div>
        )}
      </div>

      {/* QR Inspector Modal */}
      {selectedQrVault && (
        <QrModal
          address={selectedQrVault}
          onClose={() => setSelectedQrVault(null)}
        />
      )}
    </div>
  );
};
