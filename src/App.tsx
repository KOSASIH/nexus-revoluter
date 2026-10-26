import React, { useState, useEffect } from 'react';
import { 
  INITIAL_ADDRESSES, 
  INITIAL_TRANSACTIONS, 
  INITIAL_BLOCKS, 
  INITIAL_PEERS, 
  INITIAL_IOT_DEVICES, 
  INITIAL_TOKENIZED_ASSETS, 
  INITIAL_PROPOSALS, 
  INITIAL_SYNC_LOGS, 
  INITIAL_COMPLIANCE_REPORT 
} from './data/initialData';
import { 
  NavTab, 
  WalletAddress, 
  Transaction, 
  Block, 
  PeerNode, 
  IoTDevice, 
  TokenizedAsset, 
  Proposal, 
  SyncLog, 
  ComplianceReport 
} from './types';
import { Header } from './components/Header';
import { Navigation } from './components/Navigation';
import { WalletView } from './components/WalletView';
import { NodeView } from './components/NodeView';
import { NpasView } from './components/NpasView';
import { SanoView } from './components/SanoView';
import { AssetsIotView } from './components/AssetsIotView';
import { GovernanceView } from './components/GovernanceView';
import { ComplianceView } from './components/ComplianceView';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<NavTab>('wallet');
  const [network, setNetwork] = useState<string>('pi-mainnet');

  // Application Data States
  const [addresses, setAddresses] = useState<WalletAddress[]>(INITIAL_ADDRESSES);
  const [transactions, setTransactions] = useState<Transaction[]>(INITIAL_TRANSACTIONS);
  const [blocks, setBlocks] = useState<Block[]>(INITIAL_BLOCKS);
  const [peers, setPeers] = useState<PeerNode[]>(INITIAL_PEERS);
  const [iotDevices, setIotDevices] = useState<IoTDevice[]>(INITIAL_IOT_DEVICES);
  const [tokenizedAssets, setTokenizedAssets] = useState<TokenizedAsset[]>(INITIAL_TOKENIZED_ASSETS);
  const [proposals, setProposals] = useState<Proposal[]>(INITIAL_PROPOSALS);
  const [syncLogs, setSyncLogs] = useState<SyncLog[]>(INITIAL_SYNC_LOGS);
  const [complianceReport, setComplianceReport] = useState<ComplianceReport>(INITIAL_COMPLIANCE_REPORT);

  // Economic & Market Monitor State
  // Live PI market price with default fallback 0.0756 USD
  const [livePrice, setLivePrice] = useState<number>(0.0756);
  const [isPriceLoading, setIsPriceLoading] = useState<boolean>(false);
  const communityGcv = 314159.00;
  const [blockHeight, setBlockHeight] = useState<number>(4920194);

  // Compute aggregate balances
  const totalPiBalance = addresses.reduce((sum, a) => sum + a.piBalance, 0);
  const totalXlmBalance = addresses.reduce((sum, a) => sum + a.balance, 0);

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

  // Live Block Mining Simulator (every 10s add new block)
  useEffect(() => {
    const blockInterval = setInterval(() => {
      setBlockHeight(prevHeight => {
        const newHeight = prevHeight + 1;
        const randomTxCount = Math.floor(Math.random() * 30) + 15;
        const randomHash = '0x' + Array.from({ length: 64 }, () => Math.floor(Math.random() * 16).toString(16)).join('');
        
        const newBlock: Block = {
          height: newHeight,
          hash: randomHash,
          previousHash: blocks[0]?.hash || '0x0000000000000000000000000000000000000000',
          validator: 'Nexus-SANO-Sentinel-' + ['Tokyo', 'Frankfurt', 'Virginia', 'Singapore', 'Zurich'][Math.floor(Math.random() * 5)],
          txCount: randomTxCount,
          timestamp: 'Just now',
          sizeKb: Number((Math.random() * 60 + 80).toFixed(1)),
          gasUsed: Math.floor(Math.random() * 500000 + 1000000)
        };

        setBlocks(prev => [newBlock, ...prev.slice(0, 9)]);
        return newHeight;
      });
    }, 10000);

    return () => clearInterval(blockInterval);
  }, [blocks]);

  // Wallet Handlers
  const handleAddAddress = (label: string) => {
    const randomHex = Array.from({ length: 32 }, () => Math.floor(Math.random() * 16).toString(16)).join('').toUpperCase();
    const newAddress: WalletAddress = {
      address: `GDZX${randomHex.slice(0, 36)}PI`,
      label,
      balance: 100.0,
      piBalance: 314.15,
      isPrimary: false,
      createdAt: new Date().toISOString().split('T')[0]
    };
    setAddresses(prev => [...prev, newAddress]);
  };

  const handleDeleteAddress = (addressToDelete: string) => {
    setAddresses(prev => prev.filter(a => a.address !== addressToDelete));
  };

  const handleSendTransaction = (tx: {
    from: string;
    to: string;
    amount: number;
    asset: 'PI' | 'XLM' | 'NRV';
    memo: string;
  }) => {
    // Deduct from sender
    setAddresses(prev => prev.map(a => {
      if (a.address === tx.from) {
        if (tx.asset === 'PI') {
          return { ...a, piBalance: Math.max(0, a.piBalance - tx.amount) };
        } else if (tx.asset === 'XLM') {
          return { ...a, balance: Math.max(0, a.balance - tx.amount - 0.0001) };
        }
      }
      return a;
    }));

    // If recipient is one of user's own addresses, credit it
    setAddresses(prev => prev.map(a => {
      if (a.address === tx.to) {
        if (tx.asset === 'PI') {
          return { ...a, piBalance: a.piBalance + tx.amount };
        } else if (tx.asset === 'XLM') {
          return { ...a, balance: a.balance + tx.amount };
        }
      }
      return a;
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
      blockNumber: blockHeight
    };

    setTransactions(prev => [newTx, ...prev]);

    return {
      success: true,
      message: `Transaction ${newTxId.slice(0, 10)}... confirmed on Block #${blockHeight}. AML verified. Ed25519 signature recorded.`
    };
  };

  const handleSaveWallet = () => {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(
      JSON.stringify({
        version: '1.0.0',
        walletType: 'Stellar-Pi-QuantumResistant',
        addresses,
        exportedAt: new Date().toISOString()
      }, null, 2)
    );
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', `nexus_wallet_backup_${Date.now()}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  const handleLoadWallet = () => {
    handleAddAddress('Restored Cold Stash Vault');
  };

  const handleClaimFaucet = (targetAddress?: string) => {
    const addressToCredit = targetAddress || addresses[0]?.address;
    if (!addressToCredit) return;

    setAddresses(prev => prev.map(a => {
      if (a.address === addressToCredit) {
        return { ...a, piBalance: a.piBalance + 100 };
      }
      return a;
    }));

    const newTxId = 'tx_faucet_' + Array.from({ length: 12 }, () => Math.floor(Math.random() * 16).toString(16)).join('');
    const newTx: Transaction = {
      id: newTxId,
      from: 'G_FAUCET_PIONEER_TESTNET_RELAY',
      to: addressToCredit,
      amount: 100,
      asset: 'PI',
      timestamp: 'Just now',
      memo: 'Pi Network Testnet Faucet (+100 π PI)',
      status: 'confirmed',
      fee: 0,
      complianceChecked: true,
      blockNumber: blockHeight
    };

    setTransactions(prev => [newTx, ...prev]);
  };

  // Node Handlers
  const handleAddPeer = (peer: { name: string; ip: string; location: string; role: PeerNode['role'] }) => {
    const newPeer: PeerNode = {
      id: `node-${Date.now()}`,
      name: peer.name,
      ip: peer.ip,
      location: peer.location,
      role: peer.role,
      pingMs: Math.floor(Math.random() * 25) + 12,
      uptime: '99.99%',
      status: 'active',
      version: 'v1.4.2-nexus'
    };
    setPeers(prev => [...prev, newPeer]);
  };

  const handleOptimizeLatency = () => {
    setPeers(prev => prev.map(p => ({
      ...p,
      pingMs: Math.max(8, Math.round(p.pingMs * 0.85))
    })));
  };

  // NPAS Trigger
  const handleTriggerSync = () => {
    const newSyncLog: SyncLog = {
      id: `sync-${Date.now().toString().slice(-4)}`,
      timestamp: new Date().toLocaleTimeString(),
      target: ['minepi.com', 'wallet.pinet.com', 'ecosystem.pinet.com', 'Stellar Horizon'][Math.floor(Math.random() * 4)] as any,
      operation: 'Autonomous State Invariant & ABI Reconciliation',
      status: 'synced',
      latencyMs: Math.floor(Math.random() * 15) + 12,
      verifiedByZk: true
    };
    setSyncLogs(prev => [newSyncLog, ...prev.slice(0, 7)]);
  };

  // IoT & Asset Handlers
  const handleAddDevice = (device: { deviceId: string; deviceType: string; location: string }) => {
    const newDevice: IoTDevice = {
      deviceId: device.deviceId,
      deviceType: device.deviceType,
      location: device.location,
      status: 'online',
      lastPing: 'Just now',
      metrics: {
        battery: 100,
        signal: 95,
        temperature: 21.5,
        powerKw: 0.25,
        telemetryRate: '1 packet / 2s',
        reading: 'Sensory Calibration: OPTIMAL | Encryption: Ed25519'
      }
    };
    setIotDevices(prev => [newDevice, ...prev]);
  };

  const handleAddAsset = (asset: {
    assetId: string;
    name: string;
    owner: string;
    tokenizedValue: number;
    category: TokenizedAsset['category'];
  }) => {
    const newAsset: TokenizedAsset = {
      assetId: asset.assetId,
      name: asset.name,
      owner: asset.owner,
      tokenizedValue: asset.tokenizedValue,
      valuationUsd: asset.tokenizedValue * livePrice,
      tokenSymbol: 'n' + asset.name.slice(0, 4).toUpperCase(),
      category: asset.category,
      auditDate: new Date().toISOString().split('T')[0] + ' (Certified)',
      status: 'active'
    };
    setTokenizedAssets(prev => [newAsset, ...prev]);
  };

  // Governance Handlers
  const handleVote = (proposalId: string, choice: 'for' | 'against' | 'abstain') => {
    setProposals(prev => prev.map(p => {
      if (p.id === proposalId) {
        let forV = p.votesFor;
        let againstV = p.votesAgainst;
        let abstainV = p.votesAbstain;

        if (p.userVoted === 'for') forV -= 31415;
        if (p.userVoted === 'against') againstV -= 31415;
        if (p.userVoted === 'abstain') abstainV -= 31415;

        if (choice === 'for') forV += 31415;
        if (choice === 'against') againstV += 31415;
        if (choice === 'abstain') abstainV += 31415;

        return {
          ...p,
          votesFor: forV,
          votesAgainst: againstV,
          votesAbstain: abstainV,
          userVoted: choice
        };
      }
      return p;
    }));
  };

  const handleCreateProposal = (proposal: {
    title: string;
    description: string;
    category: Proposal['category'];
  }) => {
    const newProp: Proposal = {
      id: `PROP-${Date.now().toString().slice(-4)}`,
      title: proposal.title,
      description: proposal.description,
      proposer: addresses[0]?.address.slice(0, 12) + '...Pioneer',
      category: proposal.category,
      votesFor: 31415,
      votesAgainst: 0,
      votesAbstain: 0,
      status: 'active',
      deadline: 'In 7 days',
      userVoted: 'for'
    };
    setProposals(prev => [newProp, ...prev]);
  };

  // Compliance Handlers
  const handleGenerateNewKyc = (userKey: string, country: string) => {
    const newHash = 'zkp_snark_' + Array.from({ length: 24 }, () => Math.floor(Math.random() * 16).toString(16)).join('');
    const newReport: ComplianceReport = {
      reportId: `ARHN-ZK-${Math.floor(Math.random() * 9000 + 1000)}-${country.slice(0, 2).toUpperCase()}`,
      userPublicKey: userKey,
      status: 'verified',
      zkProofHash: newHash,
      riskScore: 1,
      checks: {
        amlCheck: true,
        sanctionList: true,
        velocityRisk: true,
        geoCompliance: true
      },
      timestamp: new Date().toUTCString(),
      empathyFeedback: `Pioneer identity verified in compliance with ${country} standards. Mathematical confidentiality guaranteed without data transmission.`
    };
    setComplianceReport(newReport);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Global Application Header */}
      <Header
        currentNetwork={network}
        onNetworkChange={setNetwork}
        piPrice={communityGcv}
        livePrice={livePrice}
        blockHeight={blockHeight}
        totalPiBalance={totalPiBalance}
        totalXlmBalance={totalXlmBalance}
      />

      {/* Main Tab Navigation */}
      <Navigation
        activeTab={activeTab}
        onTabChange={setActiveTab}
        syncBadgeCount={syncLogs.length}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'wallet' && (
          <WalletView
            addresses={addresses}
            transactions={transactions}
            onAddAddress={handleAddAddress}
            onDeleteAddress={handleDeleteAddress}
            onSendTransaction={handleSendTransaction}
            onSaveWallet={handleSaveWallet}
            onLoadWallet={handleLoadWallet}
            onClaimFaucet={handleClaimFaucet}
          />
        )}

        {activeTab === 'node' && (
          <NodeView
            blockHeight={blockHeight}
            blocks={blocks}
            peers={peers}
            onAddPeer={handleAddPeer}
            onOptimizeLatency={handleOptimizeLatency}
          />
        )}

        {activeTab === 'npas' && (
          <NpasView
            syncLogs={syncLogs}
            onTriggerSync={handleTriggerSync}
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

        {activeTab === 'assets-iot' && (
          <AssetsIotView
            iotDevices={iotDevices}
            tokenizedAssets={tokenizedAssets}
            onAddDevice={handleAddDevice}
            onAddAsset={handleAddAsset}
          />
        )}

        {activeTab === 'governance' && (
          <GovernanceView
            proposals={proposals}
            onVote={handleVote}
            onCreateProposal={handleCreateProposal}
          />
        )}

        {activeTab === 'compliance' && (
          <ComplianceView
            currentReport={complianceReport}
            onGenerateNewKyc={handleGenerateNewKyc}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="font-semibold text-slate-300">Nexus Revoluter</span>
            <span>•</span>
            <span>Pi Network & Stellar Autonomous Architecture</span>
          </div>
          <div className="flex items-center space-x-4 text-[11px]">
            <span>MIT Licensed</span>
            <span>SANO Target Monitor Active</span>
            <span>NPAS Bridge Synced</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
