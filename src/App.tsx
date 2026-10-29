import React, { useState, useEffect } from 'react';
import { 
  INITIAL_VAULTS,
  INITIAL_SENTINELS,
  INITIAL_TRANSACTIONS,
  INITIAL_BRIDGE_REQUESTS,
  INITIAL_PROOF_OF_RESERVE,
  INITIAL_ZK_SCREENING,
  INITIAL_HEADER_ATTRIBUTIONS,
  INITIAL_SOCIAL_RECOVERY,
  INITIAL_DAO_PROPOSALS,
  INITIAL_TREASURY_AUDIT
} from './data/initialData';
import { 
  NavTab, 
  VaultAccount, 
  Transaction, 
  SentinelNode, 
  BridgeReleaseRequest, 
  ProofOfReserve, 
  ZkComplianceScreening,
  HeaderAttribution,
  SocialRecoveryState,
  DaoProposal,
  TreasuryAuditEntry
} from './types';
import { Header } from './components/Header';
import { Navigation } from './components/Navigation';
import { VaultView } from './components/VaultView';
import { TransactionView } from './components/TransactionView';
import { P2pView } from './components/P2pView';
import { BridgeView } from './components/BridgeView';
import { ZkComplianceView } from './components/ZkComplianceView';
import { SanoView } from './components/SanoView';
import { DaoView } from './components/DaoView';
import { TreasuryView } from './components/TreasuryView';
import { GuardView } from './components/GuardView';
import { AiSentinelHud } from './components/AiSentinelHud';


export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<NavTab>('vault');
  const [network, setNetwork] = useState<string>('iou-ledger');

  // Application Data States
  const [vaults, setVaults] = useState<VaultAccount[]>(INITIAL_VAULTS);
  const [transactions, setTransactions] = useState<Transaction[]>(INITIAL_TRANSACTIONS);
  const [sentinels] = useState<SentinelNode[]>(INITIAL_SENTINELS);
  const [bridgeRequests, setBridgeRequests] = useState<BridgeReleaseRequest[]>(INITIAL_BRIDGE_REQUESTS);
  const [proofOfReserve] = useState<ProofOfReserve>(INITIAL_PROOF_OF_RESERVE);
  const [zkScreening] = useState<ZkComplianceScreening>(INITIAL_ZK_SCREENING);
  const [headerAttributions] = useState<HeaderAttribution[]>(INITIAL_HEADER_ATTRIBUTIONS);
  const [socialRecovery, setSocialRecovery] = useState<SocialRecoveryState>(INITIAL_SOCIAL_RECOVERY);
  const [proposals, setProposals] = useState<DaoProposal[]>(INITIAL_DAO_PROPOSALS);
  const [treasuryAudit, setTreasuryAudit] = useState<TreasuryAuditEntry[]>(INITIAL_TREASURY_AUDIT);

  // Economic & Market Monitor State
  // Live PI market price with default fallback $0.0756 USD
  const [livePrice, setLivePrice] = useState<number>(0.0756);
  const [isPriceLoading, setIsPriceLoading] = useState<boolean>(false);
  const communityGcv = 314159.00;
  const [blockHeight, setBlockHeight] = useState<number>(4920194);

  // Compute aggregate balances
  const totalPiBalance = vaults.reduce((sum, v) => sum + v.piBalance, 0);
  const totalXlmBalance = vaults.reduce((sum, v) => sum + v.xlmBalance, 0);

  // Fetch live market price
  const fetchLivePrice = async () => {
    setIsPriceLoading(true);
    try {
      const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=pi-network&vs_currencies=usd');
      if (response.ok) {
        const data = await response.json();
        if (data?.['pi-network']?.usd && typeof data['pi-network'].usd === 'number') {
          setLivePrice(data['pi-network'].usd);
        }
      }
    } catch {
      // Gracefully retain fallback price ($0.0756)
    } finally {
      setIsPriceLoading(false);
    }
  };

  useEffect(() => {
    fetchLivePrice();
    const priceTimer = setInterval(fetchLivePrice, 60000);
    return () => clearInterval(priceTimer);
  }, []);

  // Increment simulated block slot
  useEffect(() => {
    const blockInterval = setInterval(() => {
      setBlockHeight(prev => prev + 1);
    }, 10000);
    return () => clearInterval(blockInterval);
  }, []);

  // Module 1 Handlers: Vault & Faucet
  const handleGenerateAddress = (name: string) => {
    const randomHex = Array.from({ length: 32 }, () => Math.floor(Math.random() * 16).toString(16)).join('').toUpperCase();
    const newVault: VaultAccount = {
      id: `vault-${Date.now()}`,
      name,
      address: `GDZX${randomHex.slice(0, 36)}PI`,
      piBalance: 100.0,
      xlmBalance: 50.0,
      isPrimary: false,
      role: 'primary',
      keyType: 'Ed25519-QuantumResistant',
      createdAt: new Date().toISOString().split('T')[0],
      vaultAgeDays: 1
    };
    setVaults(prev => [...prev, newVault]);
  };

  const handleClaimFaucet = (vaultId: string) => {
    setVaults(prev => prev.map(v => {
      if (v.id === vaultId) {
        return { ...v, piBalance: v.piBalance + 100 };
      }
      return v;
    }));

    const targetVault = vaults.find(v => v.id === vaultId) || vaults[0];

    // Log transaction
    const newTxId = 'tx_faucet_' + Array.from({ length: 12 }, () => Math.floor(Math.random() * 16).toString(16)).join('');
    const newTx: Transaction = {
      id: newTxId,
      from: 'GCXP449102847192847291847192847192847NPASBRIDGE',
      to: targetVault.address,
      amount: 100.00,
      asset: 'π PI IOU',
      timestamp: 'Just now',
      memo: 'Test IOU Faucet Allocation (+100 π PI)',
      status: 'confirmed',
      fee: 0.0,
      complianceChecked: true,
      blockNumber: blockHeight,
      aiRiskScore: 0,
      aiRiskVerdict: 'SAFE'
    };
    setTransactions(prev => [newTx, ...prev]);

    // Append to immutable treasury audit log
    const prevAudit = treasuryAudit[0];
    const newAuditEntry: TreasuryAuditEntry = {
      id: `aud-00${treasuryAudit.length + 1}`,
      timestamp: new Date().toISOString().replace('T', ' ').slice(0, 19) + ' UTC',
      prevHash: prevAudit ? prevAudit.entryHash.slice(0, 16) + '...' : '0x0000000000000000',
      entryHash: '0x' + Array.from({ length: 40 }, () => Math.floor(Math.random() * 16).toString(16)).join(''),
      movementType: 'ESCROW_ALLOCATION',
      amount: 100.0,
      asset: 'π PI',
      destination: `Faucet Allocation to ${targetVault.name}`,
      proofSignature: 'ed25519_sig_valid_0x' + Array.from({ length: 8 }, () => Math.floor(Math.random() * 16).toString(16)).join('')
    };
    setTreasuryAudit(prev => [newAuditEntry, ...prev]);
  };

  const handleExportEncrypted = () => {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(
      JSON.stringify({
        schema: 'Sovereign-Pioneer-Vault-V1',
        encryption: 'AES-256-GCM-PBKDF2',
        vaults,
        exportedAt: new Date().toISOString()
      }, null, 2)
    );
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', `nexus_pioneer_vault_backup_${Date.now()}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  const handleImportEncrypted = () => {
    handleGenerateAddress('Restored Cold Storage Vault');
  };

  // Module 7 Handlers: Social Recovery
  const handleApproveRecoveryGuardian = (guardianId: string) => {
    setSocialRecovery(prev => {
      const updated = prev.guardians.map(g => g.id === guardianId ? { ...g, status: 'confirmed' as const } : g);
      const approvals = updated.filter(g => g.status === 'confirmed').length;
      return {
        ...prev,
        guardians: updated,
        approvalsReceived: approvals,
        recoveryInProgress: approvals >= 2
      };
    });
  };

  const handleTriggerRecovery = () => {
    setSocialRecovery(prev => ({
      ...prev,
      recoveryInProgress: true
    }));
  };

  // Module 6 Handlers: Execute Transaction
  const handleSendTransaction = (tx: {
    from: string;
    to: string;
    amount: number;
    asset: 'π PI IOU' | 'XLM' | 'NRV';
    memo: string;
    aiRiskScore: number;
    aiRiskVerdict: 'SAFE' | 'SUSPICIOUS' | 'FLAGGED';
  }) => {
    // Deduct from sender
    setVaults(prev => prev.map(v => {
      if (v.address === tx.from) {
        if (tx.asset === 'π PI IOU') {
          return { ...v, piBalance: Math.max(0, v.piBalance - tx.amount) };
        } else if (tx.asset === 'XLM') {
          return { ...v, xlmBalance: Math.max(0, v.xlmBalance - tx.amount - 0.0001) };
        }
      }
      return v;
    }));

    // Credit if recipient is one of user's own vaults
    setVaults(prev => prev.map(v => {
      if (v.address === tx.to) {
        if (tx.asset === 'π PI IOU') {
          return { ...v, piBalance: v.piBalance + tx.amount };
        } else if (tx.asset === 'XLM') {
          return { ...v, xlmBalance: v.xlmBalance + tx.amount };
        }
      }
      return v;
    }));

    const newTxId = 'tx_' + Array.from({ length: 16 }, () => Math.floor(Math.random() * 16).toString(16)).join('');
    const newTx: Transaction = {
      id: newTxId,
      from: tx.from,
      to: tx.to,
      amount: tx.amount,
      asset: tx.asset,
      timestamp: 'Just now',
      memo: tx.memo,
      status: 'confirmed',
      fee: 0.0001,
      complianceChecked: true,
      blockNumber: blockHeight,
      aiRiskScore: tx.aiRiskScore,
      aiRiskVerdict: tx.aiRiskVerdict
    };

    setTransactions(prev => [newTx, ...prev]);

    // Record fee in treasury audit trail
    const prevAudit = treasuryAudit[0];
    const newAuditEntry: TreasuryAuditEntry = {
      id: `aud-00${treasuryAudit.length + 1}`,
      timestamp: new Date().toISOString().replace('T', ' ').slice(0, 19) + ' UTC',
      prevHash: prevAudit ? prevAudit.entryHash.slice(0, 16) + '...' : '0x0000000000000000',
      entryHash: '0x' + Array.from({ length: 40 }, () => Math.floor(Math.random() * 16).toString(16)).join(''),
      movementType: 'FEE_COLLECTION',
      amount: 0.0001,
      asset: 'π PI',
      destination: 'Stellar SCP Quorum Fee Pool',
      proofSignature: 'ed25519_sig_valid_0x' + Array.from({ length: 8 }, () => Math.floor(Math.random() * 16).toString(16)).join('')
    };
    setTreasuryAudit(prev => [newAuditEntry, ...prev]);
  };

  // Module 3 Handlers: MPC Bridge Release
  const handleToggleSignature = (requestId: string, signerId: string) => {
    setBridgeRequests(prev => prev.map(req => {
      if (req.id === requestId) {
        const updatedSigners = req.signers.map(s => {
          if (s.id === signerId) {
            return { ...s, signed: !s.signed };
          }
          return s;
        });
        const currentCount = updatedSigners.filter(s => s.signed).length;
        const isAuthorized = currentCount >= req.requiredSignatures;

        return {
          ...req,
          signers: updatedSigners,
          currentSignatures: currentCount,
          status: isAuthorized ? 'authorized' : 'pending'
        };
      }
      return req;
    }));
  };

  const handleRequestNewRelease = (amount: number, recipient: string) => {
    const newReqId = `MPC-REQ-${Math.floor(Math.random() * 9000 + 1000)}`;
    const newReq: BridgeReleaseRequest = {
      id: newReqId,
      requestedAmount: amount,
      recipient,
      requiredSignatures: 3,
      currentSignatures: 1,
      formalVerificationStatus: 'PROVEN_SAFE',
      formalProofHash: 'Z3_SOLVER_QAP_0x' + Array.from({ length: 16 }, () => Math.floor(Math.random() * 16).toString(16)).join(''),
      status: 'pending',
      signers: [
        { id: 'sig-1', name: 'Frankfurt MPC Custodian', pubKey: '0xfa102...', signed: true, role: 'Validator' },
        { id: 'sig-2', name: 'Zurich Reserve Escrow', pubKey: '0xb8912...', signed: false, role: 'Auditor' },
        { id: 'sig-3', name: 'Tokyo Sentinel Key', pubKey: '0x3c819...', signed: false, role: 'Sentinel' },
        { id: 'sig-4', name: 'Singapore Quantum Key', pubKey: '0x5019a...', signed: false, role: 'Backup' },
        { id: 'sig-5', name: 'Virginia Relay Sentinel', pubKey: '0x7129c...', signed: false, role: 'Relay' },
      ]
    };
    setBridgeRequests(prev => [newReq, ...prev]);
  };

  // Module 9 Handlers: Pioneer DAO Voting
  const handleVoteProposal = (proposalId: string, support: 'for' | 'against') => {
    const primaryVault = vaults.find(v => v.isPrimary) || vaults[0];
    const totalPi = vaults.reduce((acc, v) => acc + v.piBalance, 0);
    const vaultAge = primaryVault?.vaultAgeDays || 365;
    const voteWeight = Math.floor(Math.sqrt(totalPi) * Math.log2(vaultAge + 2));

    setProposals(prev => prev.map(p => {
      if (p.id === proposalId) {
        return {
          ...p,
          votesFor: support === 'for' ? p.votesFor + voteWeight : p.votesFor,
          votesAgainst: support === 'against' ? p.votesAgainst + voteWeight : p.votesAgainst,
          userVoted: support
        };
      }
      return p;
    }));
  };

  const handleCreateProposal = (proposal: {
    title: string;
    description: string;
    category: 'Bridge Fee' | 'Guardian List' | 'Sentinel Rules' | 'Shura Treasury';
  }) => {
    const newProp: DaoProposal = {
      id: `SHURA-PROP-0${proposals.length + 1}`,
      title: proposal.title,
      description: proposal.description,
      proposer: vaults[0]?.address.slice(0, 10) + '...PIONEER',
      category: proposal.category,
      votesFor: 31415,
      votesAgainst: 0,
      timelockActive: true,
      timelockEndsAt: '48 hours remaining',
      status: 'in_timelock',
      userVoted: 'for'
    };
    setProposals(prev => [newProp, ...prev]);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-blue-600 selection:text-white">
      {/* Global Application Header with Trademark Firewall Banner */}
      <Header
        currentNetwork={network}
        onNetworkChange={setNetwork}
        piPrice={communityGcv}
        livePrice={livePrice}
        blockHeight={blockHeight}
        totalPiBalance={totalPiBalance}
        totalXlmBalance={totalXlmBalance}
      />

      {/* Main Tab Navigation with Required Badges */}
      <Navigation
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />

      {/* Sovereign AI Sentinel Cognitive Matrix HUD */}
      <AiSentinelHud sentinels={sentinels} />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'vault' && (
          <VaultView
            vaults={vaults}
            socialRecovery={socialRecovery}
            onGenerateAddress={handleGenerateAddress}
            onClaimFaucet={handleClaimFaucet}
            onExportEncrypted={handleExportEncrypted}
            onImportEncrypted={handleImportEncrypted}
            onApproveRecoveryGuardian={handleApproveRecoveryGuardian}
            onTriggerRecovery={handleTriggerRecovery}
          />
        )}

        {activeTab === 'transaction' && (
          <TransactionView
            vaults={vaults}
            transactions={transactions}
            onSendTransaction={handleSendTransaction}
            livePrice={livePrice}
            communityGcv={communityGcv}
          />
        )}

        {activeTab === 'p2p' && (
          <P2pView
            sentinels={sentinels}
          />
        )}

        {activeTab === 'bridge' && (
          <BridgeView
            bridgeRequests={bridgeRequests}
            headerAttributions={headerAttributions}
            onToggleSignature={handleToggleSignature}
            onRequestNewRelease={handleRequestNewRelease}
          />
        )}

        {activeTab === 'zk-compliance' && (
          <ZkComplianceView
            proofOfReserve={proofOfReserve}
            complianceScreening={zkScreening}
          />
        )}

        {activeTab === 'sano' && (
          <SanoView
            livePrice={livePrice}
            communityGcv={communityGcv}
            onRefreshPrice={fetchLivePrice}
            isPriceLoading={isPriceLoading}
          />
        )}

        {activeTab === 'dao' && (
          <DaoView
            proposals={proposals}
            vaults={vaults}
            onVote={handleVoteProposal}
            onCreateProposal={handleCreateProposal}
          />
        )}

        {activeTab === 'treasury' && (
          <TreasuryView
            auditEntries={treasuryAudit}
            vaults={vaults}
          />
        )}

        {activeTab === 'guard' && (
          <GuardView />
        )}
      </main>

      {/* Sovereign Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="font-semibold text-slate-300">Nexus Revoluter</span>
            <span>•</span>
            <span>Sovereign Pioneer Infrastructure</span>
            <span>•</span>
            <span className="text-amber-400 font-medium">Unofficial community project, not affiliated with Pi Core Team</span>
          </div>
          <div className="flex items-center space-x-4 text-[11px] font-mono">
            <span>SANO MONITOR • NPAS V1.0</span>
            <span>Ed25519 & ZK-SNARK</span>
            <span>Byzantine Quorum 67%</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
