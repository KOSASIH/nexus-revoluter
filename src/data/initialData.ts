import { 
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
} from '../types';

export const INITIAL_VAULTS: VaultAccount[] = [
  {
    id: 'vault-primary',
    name: 'Primary Pioneer Node Vault',
    address: 'GDZX94K2MQW8VR91PXZL029471NVMS947194KOSASIH88',
    piBalance: 31415.92,
    xlmBalance: 1450.75,
    isPrimary: true,
    role: 'primary',
    keyType: 'Ed25519-QuantumResistant',
    createdAt: '2025-01-15',
    vaultAgeDays: 412
  },
  {
    id: 'vault-reserve',
    name: 'SANO Reserve Arbitrage Collateral',
    address: 'GABR72K1PLMZ82937NYVX729485LKS837194REVOLUTER01',
    piBalance: 125000.00,
    xlmBalance: 820.00,
    isPrimary: false,
    role: 'reserve',
    keyType: 'Ed25519-QuantumResistant',
    createdAt: '2025-02-01',
    vaultAgeDays: 320
  },
  {
    id: 'vault-bridge',
    name: 'NPAS Autonomous Bridge Escrow',
    address: 'GCXP449102847192847291847192847192847NPASBRIDGE',
    piBalance: 8840.50,
    xlmBalance: 314.16,
    isPrimary: false,
    role: 'bridge',
    keyType: 'Ed25519-QuantumResistant',
    createdAt: '2025-02-18',
    vaultAgeDays: 245
  }
];

export const INITIAL_SENTINELS: SentinelNode[] = [
  {
    id: 'node-fra',
    name: 'Frankfurt Core Validator',
    hop: 1,
    ip: '142.93.18.91',
    port: 8080,
    region: 'Frankfurt, Germany',
    pingMs: 14,
    uptime: '99.99%',
    active: true,
    quorumAck: true,
    role: 'Core SCP Validator'
  },
  {
    id: 'node-tyo',
    name: 'Tokyo SANO Orchestration Sentinel',
    hop: 2,
    ip: '133.242.17.84',
    port: 8080,
    region: 'Tokyo, Japan',
    pingMs: 42,
    uptime: '99.98%',
    active: true,
    quorumAck: true,
    role: 'SANO Target Sentinel'
  },
  {
    id: 'node-iad',
    name: 'Virginia NPAS Mainnet Bridge Relay',
    hop: 3,
    ip: '54.210.88.192',
    port: 8080,
    region: 'Virginia, USA',
    pingMs: 68,
    uptime: '99.95%',
    active: true,
    quorumAck: true,
    role: 'NPAS Bridge Relay'
  },
  {
    id: 'node-sin',
    name: 'Singapore Quantum Consensus Node',
    hop: 4,
    ip: '128.199.204.12',
    port: 8080,
    region: 'Singapore',
    pingMs: 31,
    uptime: '99.99%',
    active: true,
    quorumAck: true,
    role: 'Quantum Byzantine Sentinel'
  },
  {
    id: 'node-zrh',
    name: 'Zurich Stellar Archive Node',
    hop: 5,
    ip: '185.19.28.104',
    port: 8080,
    region: 'Zurich, Switzerland',
    pingMs: 22,
    uptime: '100.00%',
    active: true,
    quorumAck: true,
    role: 'Stellar Ledger Archive'
  }
];

export const INITIAL_TRANSACTIONS: Transaction[] = [
  {
    id: 'tx_7e93a04b12c84f67a',
    from: 'GDZX94K2MQW8VR91PXZL029471NVMS947194KOSASIH88',
    to: 'GABR72K1PLMZ82937NYVX729485LKS837194REVOLUTER01',
    amount: 314.15,
    asset: 'π PI IOU',
    timestamp: '2 mins ago',
    memo: 'P2P Micro-Barter Settlement',
    status: 'confirmed',
    fee: 0.0001,
    complianceChecked: true,
    blockNumber: 4920194,
    aiRiskScore: 0,
    aiRiskVerdict: 'SAFE'
  },
  {
    id: 'tx_982bf7210eac9312b',
    from: 'GCXP449102847192847291847192847192847NPASBRIDGE',
    to: 'GDZX94K2MQW8VR91PXZL029471NVMS947194KOSASIH88',
    amount: 100.00,
    asset: 'π PI IOU',
    timestamp: '18 mins ago',
    memo: 'Test IOU Faucet Allocation',
    status: 'confirmed',
    fee: 0.0,
    complianceChecked: true,
    blockNumber: 4920182,
    aiRiskScore: 0,
    aiRiskVerdict: 'SAFE'
  },
  {
    id: 'tx_31fa92019c8d3211e',
    from: 'GDZX94K2MQW8VR91PXZL029471NVMS947194KOSASIH88',
    to: 'GDF7102947192847192847192847192847192847VALIDTR',
    amount: 50.00,
    asset: 'XLM',
    timestamp: '1 hour ago',
    memo: 'Sentinel Node Hosting Lease',
    status: 'confirmed',
    fee: 0.00001,
    complianceChecked: true,
    blockNumber: 4920140,
    aiRiskScore: 2,
    aiRiskVerdict: 'SAFE'
  }
];

export const INITIAL_BRIDGE_REQUESTS: BridgeReleaseRequest[] = [
  {
    id: 'MPC-REQ-8841',
    requestedAmount: 5000,
    recipient: 'GCXP4491...NPASBRIDGE',
    requiredSignatures: 3,
    currentSignatures: 3,
    formalVerificationStatus: 'PROVEN_SAFE',
    formalProofHash: 'Z3_SOLVER_QAP_0x98124bc819e0a',
    status: 'authorized',
    signers: [
      { id: 'sig-1', name: 'Frankfurt MPC Custodian', pubKey: '0xfa102...', signed: true, role: 'Validator' },
      { id: 'sig-2', name: 'Zurich Reserve Escrow', pubKey: '0xb8912...', signed: true, role: 'Auditor' },
      { id: 'sig-3', name: 'Tokyo Sentinel Key', pubKey: '0x3c819...', signed: true, role: 'Sentinel' },
      { id: 'sig-4', name: 'Singapore Quantum Key', pubKey: '0x5019a...', signed: false, role: 'Backup' },
      { id: 'sig-5', name: 'Virginia Relay Sentinel', pubKey: '0x7129c...', signed: false, role: 'Relay' },
    ]
  }
];

export const INITIAL_PROOF_OF_RESERVE: ProofOfReserve = {
  asset: 'π PI IOU',
  totalVaultObligations: 165256.42,
  onChainCollateralProven: 520000.00,
  coverageRatio: 3.146,
  solvencyStatus: 'OVERCOLLATERALIZED',
  zkProofHash: 'zk_snark_por_0x7b60d5981a6ca2709815260798daca67',
  timestamp: 'Live Invariant Solvency Check (Epoch 4920)'
};

export const INITIAL_ZK_SCREENING: ZkComplianceScreening = {
  userAddress: 'GDZX94K2MQW8VR91PXZL029471NVMS947194KOSASIH88',
  arhnPassed: true,
  ahcewPassed: true,
  sanctionCheckZk: 'CLEARED',
  riskScore: 0,
  zkProofToken: 'zk_arhn_snark_proof_981a2f4c',
  timestamp: 'Verified without identity disclosure'
};

export const INITIAL_HEADER_ATTRIBUTIONS: HeaderAttribution[] = [
  {
    source: 'Stellar Horizon Public (horizon.stellar.org)',
    latestLedgerSequence: 54109822,
    headerHash: '0x9d82f7103a8ec492ba37482910faecb891240182749102938471928374619283',
    verifiedInBrowser: true,
    timestamp: '1s ago',
    status: 'VERIFIED',
    latencyMs: 19
  },
  {
    source: 'Community Sentinel Node (Frankfurt P2P)',
    latestLedgerSequence: 54109822,
    headerHash: '0x9d82f7103a8ec492ba37482910faecb891240182749102938471928374619283',
    verifiedInBrowser: true,
    timestamp: '2s ago',
    status: 'VERIFIED',
    latencyMs: 14
  },
  {
    source: 'Community Archive Gateway (Zurich Peer)',
    latestLedgerSequence: 54109821,
    headerHash: '0x8c71e6092b7db381a926371809ebda7801390171638091827360817263508172',
    verifiedInBrowser: true,
    timestamp: '5s ago',
    status: 'VERIFIED',
    latencyMs: 23
  }
];

export const INITIAL_SOCIAL_RECOVERY: SocialRecoveryState = {
  enabled: true,
  threshold: '2 of 3',
  recoveryInProgress: false,
  approvalsReceived: 2,
  guardians: [
    { id: 'g1', name: 'Pioneer Sentinel Trust (Family Hardware Key)', address: 'GDM81294...GUARDIAN1', status: 'confirmed' },
    { id: 'g2', name: 'Cold Storage Vault (Zurich Offline Paper Key)', address: 'GCP91028...GUARDIAN2', status: 'confirmed' },
    { id: 'g3', name: 'Local Shura Council Sentinel (Recovery Peer)', address: 'GAK38192...GUARDIAN3', status: 'confirmed' },
  ]
};

export const INITIAL_DAO_PROPOSALS: DaoProposal[] = [
  {
    id: 'SHURA-PROP-01',
    title: 'Cap NPAS Bridge Relay Base Fee to 0.00010 XLM',
    description: 'Ensure all micro-barter transactions remain accessible with zero fee gouging.',
    proposer: 'GDZX94K2...KOSASIH88',
    category: 'Bridge Fee',
    votesFor: 84210,
    votesAgainst: 120,
    timelockActive: true,
    timelockEndsAt: '42 hours remaining',
    status: 'in_timelock'
  },
  {
    id: 'SHURA-PROP-02',
    title: 'Ratify 5 Community Sentinel Nodes in Quorum Slice',
    description: 'Officially enroll Frankfurt, Tokyo, Virginia, Singapore, and Zurich in the Byzantine Quorum.',
    proposer: 'GABR72K1...REVOLUTER01',
    category: 'Sentinel Rules',
    votesFor: 128900,
    votesAgainst: 450,
    timelockActive: false,
    timelockEndsAt: 'Concluded',
    status: 'executed'
  },
  {
    id: 'SHURA-PROP-03',
    title: 'Rotate Social Recovery MPC Emergency Seed Enclave',
    description: 'Perform scheduled 6-month cryptographic key rotation without central server dependency.',
    proposer: 'GCXP4491...NPASBRIDGE',
    category: 'Guardian List',
    votesFor: 64100,
    votesAgainst: 2100,
    timelockActive: true,
    timelockEndsAt: '18 hours remaining',
    status: 'in_timelock'
  }
];

export const INITIAL_TREASURY_AUDIT: TreasuryAuditEntry[] = [
  {
    id: 'aud-004',
    timestamp: '2025-02-28 10:14 UTC',
    prevHash: '0x4f19b028c9a8...',
    entryHash: '0x8a91b2c3d4e5f67890123456789abcdef0123456',
    movementType: 'FEE_COLLECTION',
    amount: 14.8,
    asset: 'π PI',
    destination: 'NPAS Treasury Reserve',
    proofSignature: 'ed25519_sig_valid_0x99281a'
  },
  {
    id: 'aud-003',
    timestamp: '2025-02-28 08:30 UTC',
    prevHash: '0x3e18a917b897...',
    entryHash: '0x4f19b028c9a81234567890abcdef1234567890ab',
    movementType: 'ESCROW_ALLOCATION',
    amount: 500.0,
    asset: 'π PI',
    destination: 'Pioneer Community Faucet Pool',
    proofSignature: 'ed25519_sig_valid_0x88172c'
  },
  {
    id: 'aud-002',
    timestamp: '2025-02-27 22:10 UTC',
    prevHash: '0x2d179806a786...',
    entryHash: '0x3e18a917b8970123456789abcdef012345678901',
    movementType: 'COMMUNITY_GRANT',
    amount: 1000.0,
    asset: 'π PI',
    destination: 'Sentinel Node Hosting Grant (Frankfurt)',
    proofSignature: 'ed25519_sig_valid_0x77161b'
  }
];
