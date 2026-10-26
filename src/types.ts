export type NavTab = 
  | 'wallet'
  | 'node'
  | 'npas'
  | 'sano'
  | 'assets-iot'
  | 'governance'
  | 'compliance';

export interface WalletAddress {
  address: string;
  label: string;
  balance: number;
  piBalance: number;
  isPrimary?: boolean;
  createdAt: string;
}

export interface Transaction {
  id: string;
  from: string;
  to: string;
  amount: number;
  asset: 'PI' | 'XLM' | 'NRV';
  timestamp: string;
  memo?: string;
  status: 'confirmed' | 'pending' | 'failed';
  fee: number;
  complianceChecked: boolean;
  blockNumber: number;
}

export interface Block {
  height: number;
  hash: string;
  previousHash: string;
  validator: string;
  txCount: number;
  timestamp: string;
  sizeKb: number;
  gasUsed: number;
}

export interface PeerNode {
  id: string;
  name: string;
  ip: string;
  location: string;
  role: 'Validator' | 'SANO Orchestrator' | 'NPAS Relayer' | 'Archive Node';
  pingMs: number;
  uptime: string;
  status: 'active' | 'syncing' | 'offline';
  version: string;
}

export interface IoTDevice {
  deviceId: string;
  deviceType: string;
  location: string;
  status: 'online' | 'standby' | 'warning';
  lastPing: string;
  metrics: {
    battery: number;
    signal: number;
    temperature: number;
    powerKw?: number;
    telemetryRate: string;
    reading: string;
  };
}

export interface TokenizedAsset {
  assetId: string;
  name: string;
  owner: string;
  tokenizedValue: number;
  valuationUsd: number;
  tokenSymbol: string;
  category: 'Renewable Energy' | 'Real Estate' | 'Carbon Credit' | 'Compute Cluster';
  auditDate: string;
  status: 'active' | 'pending_audit' | 'locked';
}

export interface Proposal {
  id: string;
  title: string;
  description: string;
  proposer: string;
  category: 'Orchestration' | 'Monetary Policy' | 'Network Upgrade' | 'Community Fund';
  votesFor: number;
  votesAgainst: number;
  votesAbstain: number;
  status: 'active' | 'passed' | 'rejected';
  deadline: string;
  userVoted?: 'for' | 'against' | 'abstain';
}

export interface SyncLog {
  id: string;
  timestamp: string;
  target: 'minepi.com' | 'wallet.pinet.com' | 'ecosystem.pinet.com' | 'Stellar Horizon';
  operation: string;
  status: 'synced' | 'verifying' | 'queued' | 'warning';
  latencyMs: number;
  verifiedByZk: boolean;
}

export interface ComplianceReport {
  reportId: string;
  userPublicKey: string;
  status: 'verified' | 'flagged' | 'under_review';
  zkProofHash: string;
  riskScore: number;
  checks: {
    amlCheck: boolean;
    sanctionList: boolean;
    velocityRisk: boolean;
    geoCompliance: boolean;
  };
  timestamp: string;
  empathyFeedback: string;
}
