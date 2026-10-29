export type NavTab = 
  | 'vault'
  | 'transaction'
  | 'p2p'
  | 'bridge'
  | 'zk-compliance'
  | 'sano'
  | 'dao'
  | 'treasury'
  | 'guard'
  | 'god-chain';

export interface VaultAccount {
  id: string;
  name: string;
  address: string;
  piBalance: number;
  xlmBalance: number;
  isPrimary?: boolean;
  role: 'primary' | 'reserve' | 'bridge';
  keyType: 'Ed25519-QuantumResistant';
  createdAt: string;
  vaultAgeDays: number;
}

export interface Transaction {
  id: string;
  from: string;
  to: string;
  amount: number;
  asset: 'π PI IOU' | 'XLM' | 'NRV';
  timestamp: string;
  memo?: string;
  status: 'confirmed' | 'pending' | 'flagged';
  fee: number;
  complianceChecked: boolean;
  blockNumber: number;
  aiRiskScore?: number;
  aiRiskVerdict?: 'SAFE' | 'SUSPICIOUS' | 'FLAGGED';
}

export interface SentinelNode {
  id: string;
  name: string;
  hop: number;
  ip: string;
  port: number;
  region: string;
  pingMs: number;
  uptime: string;
  active: boolean;
  quorumAck: boolean;
  role: string;
}

export interface BridgeSigner {
  id: string;
  name: string;
  pubKey: string;
  signed: boolean;
  role: string;
}

export interface BridgeReleaseRequest {
  id: string;
  requestedAmount: number;
  recipient: string;
  requiredSignatures: number;
  currentSignatures: number;
  formalVerificationStatus: 'PROVEN_SAFE' | 'VERIFYING' | 'REJECTED';
  formalProofHash: string;
  status: 'pending' | 'authorized' | 'rejected';
  signers: BridgeSigner[];
}

export interface ProofOfReserve {
  asset: string;
  totalVaultObligations: number;
  onChainCollateralProven: number;
  coverageRatio: number;
  solvencyStatus: 'SOLVENT_100%' | 'OVERCOLLATERALIZED';
  zkProofHash: string;
  timestamp: string;
}

export interface ZkComplianceScreening {
  userAddress: string;
  arhnPassed: boolean;
  ahcewPassed: boolean;
  sanctionCheckZk: 'CLEARED' | 'FLAGGED';
  riskScore: number;
  zkProofToken: string;
  timestamp: string;
}

export interface HeaderAttribution {
  source: string;
  latestLedgerSequence: number;
  headerHash: string;
  verifiedInBrowser: boolean;
  timestamp: string;
  status: 'VERIFIED' | 'WARNING_CACHED';
  latencyMs: number;
}

export interface GuardianContact {
  id: string;
  name: string;
  address: string;
  status: 'confirmed' | 'pending';
}

export interface SocialRecoveryState {
  enabled: boolean;
  guardians: GuardianContact[];
  threshold: string; // "2 of 3"
  recoveryInProgress: boolean;
  approvalsReceived: number;
}

export interface DaoProposal {
  id: string;
  title: string;
  description: string;
  proposer: string;
  category: 'Bridge Fee' | 'Guardian List' | 'Sentinel Rules' | 'Shura Treasury';
  votesFor: number;
  votesAgainst: number;
  timelockEndsAt: string;
  timelockActive: boolean;
  status: 'active' | 'in_timelock' | 'executed' | 'rejected';
  userVoted?: 'for' | 'against';
}

export interface TreasuryAuditEntry {
  id: string;
  timestamp: string;
  prevHash: string;
  entryHash: string;
  movementType: 'FEE_COLLECTION' | 'ESCROW_ALLOCATION' | 'COMMUNITY_GRANT';
  amount: number;
  asset: 'π PI';
  destination: string;
  proofSignature: string;
}

export interface AiDiagnosticReport {
  timestamp: string;
  threatLevel: 'NOMINAL' | 'ELEVATED' | 'CRITICAL';
  quorumHealth: number;
  byzantineRisk: 'LOW' | 'MEDIUM' | 'HIGH';
  solvencyIndex: number;
  recommendations: string[];
  anomalousNodesDetected: number;
  sybilResistanceScore: number;
  latencyJitterMs: number;
  autonomousRemediations: string[];
}

export interface ShuraAiAnalysis {
  proposalId: string;
  shuraScore: number;
  ethicalAlignment: 'EXCELLENT' | 'FAIR' | 'RISKY';
  economicSustainability: string;
  welfareImpact: string;
  sybilVulnerability: string;
  recommendedAction: 'RATIFY' | 'TIMELOCK_AUDIT' | 'REJECT';
  keyInsights: string[];
}

export interface TransactionThreatDetail {
  entropyScore: number;
  honeypotProbability: number;
  phishingRisk: 'NONE' | 'LOW' | 'HIGH';
  quantumResistance: boolean;
  verdictReason: string;
  simulatedExecution: 'SUCCESS_NO_REVERT' | 'FLAG_ANOMALOUS_MEMO' | 'HIGH_GAS_DRAIN';
}

export interface DimensionVector {
  id: number;
  name: string;
  sanskritName: string;
  category: 'LIFE_SOVEREIGNTY' | 'THERMODYNAMICS' | 'CONSENSUS_COMPUTE' | 'SECURITY_PROOF';
  status: 'SYNCHRONIZED' | 'CALIBRATING' | 'RESONATING';
  resonanceScore: number; // 0-100
  invariantRule: string;
  tensorHash: string;
  realWorldMetric: string;
}

export interface SuperCalculator {
  id: string;
  name: string;
  role: 'Cash Calculator' | 'Contract Calculator' | 'KYC Calculator' | 'Privacy Calculator' | 'Storage Calculator';
  chainTarget: string;
  tensorProofType: string;
  coordinationStatus: 'SYNCHRONIZED' | 'OBSERVING' | 'VERIFYING';
  lastBlockSync: number;
  tpsEquivalent: number;
  latencyToGodChain: number;
}

export interface QThermoMetrics {
  currentEntropy: number; // Joules/Kelvin
  energyBackingPerPi: number; // kWh equivalent per π PI
  biospherePurityIndex: number; // 0-100%
  thermoEquilibriumRatio: number;
  poutwHash: string; // Proof of Useful Thermodynamic Work
  agenticGdpVelocity: number; // V = GDP / M
  zeroRentEfficiency: number; // %
}

export interface SelfHealingEvent {
  id: string;
  timestamp: string;
  incidentType: 'BYZANTINE_DRIFT' | 'ECLIPSE_ATTACK_ATTEMPT' | 'MEMPOOL_FLOOD' | 'FORK_ANOMALY';
  affectedTarget: string;
  severity: 'WARNING' | 'CRITICAL' | 'RESOLVED';
  remediationAction: string;
  recoveryLatencyMs: number;
  autonomousAgent: string;
}

export interface PredictiveGasForecast {
  minuteSlot: string;
  predictedCongestion: number; // 0-100%
  recommendedFeePi: number; // π PI
  optimalTransferWindow: boolean;
  expectedTps: number;
}

export interface QuantumAuditReport {
  address: string;
  shannonEntropy: number;
  saltUniformity: number;
  pbkdf2Rounds: number;
  shorResistanceYears: number;
  kyberDilithiumWrapper: boolean;
  securityVerdict: 'QUANTUM_IMPERVIOUS' | 'REINFORCED' | 'UPGRADE_RECOMMENDED';
}

export interface SovereignAgent {
  id: 'ARHANA' | 'AGNI_Q' | 'DHARMA_AI' | 'VAJRA_ZK';
  name: string;
  codename: string;
  role: string;
  specialization: string;
  cognitiveLayer: string;
  status: 'ACTIVE_OBSERVING' | 'SYNTHESIZING' | 'ATTENDING';
  confidenceScore: number;
  heuristicHeuristicsCount: number;
  avatarColor: string;
  samplePrompts: string[];
}

export interface AgentInferenceResponse {
  agentId: string;
  prompt: string;
  timestamp: string;
  verdict: 'CONFIRMED_OPTIMAL' | 'VERIFIED_SOUND' | 'ATTENTION_REQUIRED';
  reasoningChain: string[];
  mathematicalMetrics: { [key: string]: string | number };
  cryptographicSignature: string;
}

export interface StealthAddressProof {
  ephemeralPublicKey: string; // R = r * G
  stealthRecipientAddress: string; // P = H(r * K_view) * G + K_spend
  viewTag: string; // 1-byte fast scanner prefix
  zkBlindFactor: string;
  derivationTimestamp: string;
}



