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
  TreasuryAuditEntry,
  DimensionVector,
  SuperCalculator,
  QThermoMetrics,
  SelfHealingEvent
} from '../types';

// Helper mock biar gak kena flag GitGuardian. Semua token di bawah ini dummy.
const mockProof = (prefix: string) => `${prefix}_mock_${Math.random().toString(36).substring(2, 10)}`;

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
    formalProofHash: 'Z3_MOCK_QAP_verified',
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
  zkProofHash: 'zk_mock_por_verified',
  timestamp: 'Live Invariant Solvency Check (Epoch 4920)'
};

export const INITIAL_ZK_SCREENING: ZkComplianceScreening = {
  userAddress: 'GDZX94K2MQW8VR91PXZL029471NVMS947194KOSASIH88',
  arhnPassed: true,
  ahcewPassed: true,
  sanctionCheckZk: 'CLEARED',
  riskScore: 0,
  zkProofToken: 'zk_mock_proof_981a2f4c',
  timestamp: 'Verified without identity disclosure'
};

export const INITIAL_HEADER_ATTRIBUTIONS: HeaderAttribution[] = [
  {
    source: 'Stellar Horizon Public (horizon.stellar.org)',
    latestLedgerSequence: 54109822,
    headerHash: 'PUBLIC_STELLAR_HEADER_9d82f7103a8e',
    verifiedInBrowser: true,
    timestamp: '1s ago',
    status: 'VERIFIED',
    latencyMs: 19
  },
  {
    source: 'Community Sentinel Node (Frankfurt P2P)',
    latestLedgerSequence: 54109822,
    headerHash: 'PUBLIC_STELLAR_HEADER_9d82f7103a8e',
    verifiedInBrowser: true,
    timestamp: '2s ago',
    status: 'VERIFIED',
    latencyMs: 14
  },
  {
    source: 'Community Archive Gateway (Zurich Peer)',
    latestLedgerSequence: 54109821,
    headerHash: 'PUBLIC_STELLAR_HEADER_8c71e6092b7d',
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
    prevHash: 'MOCK_PREV_HASH_4f19b028',
    entryHash: 'MOCK_ENTRY_HASH_8a91b2c3',
    movementType: 'FEE_COLLECTION',
    amount: 14.8,
    asset: 'π PI',
    destination: 'NPAS Treasury Reserve',
    proofSignature: 'ed25519_mock_sig_99281a'
  },
  {
    id: 'aud-003',
    timestamp: '2025-02-28 08:30 UTC',
    prevHash: 'MOCK_PREV_HASH_3e18a917',
    entryHash: 'MOCK_ENTRY_HASH_4f19b028',
    movementType: 'ESCROW_ALLOCATION',
    amount: 500.0,
    asset: 'π PI',
    destination: 'Pioneer Community Faucet Pool',
    proofSignature: 'ed25519_mock_sig_88172c'
  },
  {
    id: 'aud-002',
    timestamp: '2025-02-27 22:10 UTC',
    prevHash: 'MOCK_PREV_HASH_2d179806',
    entryHash: 'MOCK_ENTRY_HASH_3e18a917',
    movementType: 'COMMUNITY_GRANT',
    amount: 1000.0,
    asset: 'π PI',
    destination: 'Sentinel Node Hosting Grant (Frankfurt)',
    proofSignature: 'ed25519_mock_sig_77161b'
  }
];

export const INITIAL_DIMENSIONS: DimensionVector[] = [
  {
    id: 1,
    name: 'Life-Force Consciousness (Nyawa)',
    sanskritName: 'Prana / Nyawa',
    category: 'LIFE_SOVEREIGNTY',
    status: 'SYNCHRONIZED',
    resonanceScore: 99.8,
    invariantRule: 'Vault authorization strictly bound to living human consciousness without corporate custody.',
    tensorHash: 'tensor_mock_1_nyawa_sovereign',
    realWorldMetric: 'Heartbeat Entropy: 1.042 (Living Human Invariant)'
  },
  {
    id: 2,
    name: 'Physical Zero-Knowledge Vessel (Raga)',
    sanskritName: 'Kaya / Raga',
    category: 'LIFE_SOVEREIGNTY',
    status: 'SYNCHRONIZED',
    resonanceScore: 99.4,
    invariantRule: 'Biometric proof evaluated via zero-knowledge stealth circuit; raw biometric never stored.',
    tensorHash: 'tensor_mock_2_raga_zk_vessel',
    realWorldMetric: 'ZK Blinded Verification: 100% Cleared'
  },
  {
    id: 3,
    name: 'Temporal Cosmic Synchronizer (Wanci)',
    sanskritName: 'Kala / Wanci',
    category: 'LIFE_SOVEREIGNTY',
    status: 'RESONATING',
    resonanceScore: 100.0,
    invariantRule: 'Immutable time-lock sequence aligned with cosmological solar epoch and slot progression.',
    tensorHash: 'tensor_mock_3_wanci_cosmic_epoch',
    realWorldMetric: 'Slot Drift: ±0.002s (Atomic Horizon Sync)'
  },
  {
    id: 4,
    name: 'Thermodynamic Invariant (Q-Thermo)',
    sanskritName: 'Agni / Q-Thermo',
    category: 'THERMODYNAMICS',
    status: 'SYNCHRONIZED',
    resonanceScore: 98.9,
    invariantRule: 'Every π PI unit anchored to actual physical thermodynamic work (kWh equivalent), zero speculative inflation.',
    tensorHash: 'tensor_mock_4_qthermo_equilibrium',
    realWorldMetric: '3.14159 kWh backing per π PI verified'
  },
  {
    id: 5,
    name: 'Cognitive Sovereign Will (Niat)',
    sanskritName: 'Manas / Niat',
    category: 'LIFE_SOVEREIGNTY',
    status: 'SYNCHRONIZED',
    resonanceScore: 99.2,
    invariantRule: 'Autonomous intent verified through Ed25519 cryptographic key held solely by user browser.',
    tensorHash: 'tensor_mock_5_niat_ed25519',
    realWorldMetric: 'Local Key Entropy: 0.998 Shannon'
  },
  {
    id: 6,
    name: 'Zero-Knowledge Constraint Lattice',
    sanskritName: 'Shunya / ZK-Lattice',
    category: 'SECURITY_PROOF',
    status: 'SYNCHRONIZED',
    resonanceScore: 99.7,
    invariantRule: 'Groth16 QAP constraint polynomial evaluated over BN254 curve with zero private witness exposure.',
    tensorHash: 'tensor_mock_6_shunya_groth16',
    realWorldMetric: 'Circuit Verification Time: 28ms'
  },
  {
    id: 7,
    name: 'Federated Byzantine Quorum (SCP)',
    sanskritName: 'Sangha / Quorum',
    category: 'CONSENSUS_COMPUTE',
    status: 'SYNCHRONIZED',
    resonanceScore: 100.0,
    invariantRule: 'Quorum slices maintain >= 67% federated Byzantine overlap across global sentinel nodes.',
    tensorHash: 'tensor_mock_7_sangha_scp',
    realWorldMetric: '5/5 Sentinel Quorum Overlap'
  },
  {
    id: 8,
    name: 'Amanah Ethical Equilibrium',
    sanskritName: 'Dharma / Amanah',
    category: 'LIFE_SOVEREIGNTY',
    status: 'SYNCHRONIZED',
    resonanceScore: 99.9,
    invariantRule: 'Strict anti-usury invariant; zero predatory yield farming, zero synthetic liquidations.',
    tensorHash: 'tensor_mock_8_dharma_amanah',
    realWorldMetric: 'Usury Factor: 0.000% (Pure Sovereign Exchange)'
  },
  {
    id: 9,
    name: 'Decentralized IOU Liquidity Mesh',
    sanskritName: 'Vitta / Liquidity',
    category: 'CONSENSUS_COMPUTE',
    status: 'RESONATING',
    resonanceScore: 98.4,
    invariantRule: 'Peer-to-peer IOU transfer channel without centralized banking clearinghouse dependencies.',
    tensorHash: 'tensor_mock_9_vitta_liquidity',
    realWorldMetric: 'Active Channel Capacity: 156,415.92 π PI'
  },
  {
    id: 10,
    name: 'Post-Quantum Impervious Shield',
    sanskritName: 'Vajra / Quantum',
    category: 'SECURITY_PROOF',
    status: 'SYNCHRONIZED',
    resonanceScore: 99.9,
    invariantRule: 'Lattice-based cryptographic encapsulation resistant to Shor & Grover quantum algorithms.',
    tensorHash: 'tensor_mock_10_vajra_quantum',
    realWorldMetric: 'Shor Resistance Horizon: >50 Years'
  },
  {
    id: 11,
    name: 'Universal Super-Calculator Coordinator',
    sanskritName: 'Setu / Coordinator',
    category: 'CONSENSUS_COMPUTE',
    status: 'SYNCHRONIZED',
    resonanceScore: 99.1,
    invariantRule: 'Orchestrates external single-purpose chains as sub-ordinate calculators beneath God Chain identity.',
    tensorHash: 'tensor_mock_11_setu_coordinator',
    realWorldMetric: '5 Super Calculators Synchronized'
  },
  {
    id: 12,
    name: 'Absolute Pioneer Autonomy',
    sanskritName: 'Swaraj / Sovereign',
    category: 'LIFE_SOVEREIGNTY',
    status: 'SYNCHRONIZED',
    resonanceScore: 100.0,
    invariantRule: 'Zero dependency on Pi Core Team SDK, OAuth, or server approvals for sovereign wallet operations.',
    tensorHash: 'tensor_mock_12_swaraj_autonomy',
    realWorldMetric: 'Autonomous Index: 100% (Self-Contained Client)'
  }
];

export const INITIAL_SUPER_CALCULATORS: SuperCalculator[] = [
  {
    id: 'calc-btc',
    name: 'Bitcoin Core Mesh',
    role: 'Cash Calculator',
    chainTarget: 'BTC UTXO State',
    tensorProofType: 'SHA-256 Proof of Work Header Chain',
    coordinationStatus: 'SYNCHRONIZED',
    lastBlockSync: 885124,
    tpsEquivalent: 7,
    latencyToGodChain: 14
  },
  {
    id: 'calc-eth-sol',
    name: 'EVM & SVM Compute Matrix',
    role: 'Contract Calculator',
    chainTarget: 'Ethereum / Solana Virtual Machine',
    tensorProofType: 'Merkle Patricia Trie State Root Proof',
    coordinationStatus: 'SYNCHRONIZED',
    lastBlockSync: 21894210,
    tpsEquivalent: 3450,
    latencyToGodChain: 9
  },
  {
    id: 'calc-pi',
    name: 'Pi Network Pioneer Mesh',
    role: 'KYC Calculator',
    chainTarget: 'Pi SCP Ledger (Unofficial IOU Mirror)',
    tensorProofType: 'Stellar Consensus Protocol Quorum Slice',
    coordinationStatus: 'SYNCHRONIZED',
    lastBlockSync: 4920194,
    tpsEquivalent: 1000,
    latencyToGodChain: 4
  },
  {
    id: 'calc-privacy',
    name: 'Zcash & Worldcoin Verifier',
    role: 'Privacy Calculator',
    chainTarget: 'Zero-Knowledge Anonymity Pool',
    tensorProofType: 'Halo2 / Groth16 Recursive SNARK Proof',
    coordinationStatus: 'SYNCHRONIZED',
    lastBlockSync: 2450119,
    tpsEquivalent: 450,
    latencyToGodChain: 18
  },
  {
    id: 'calc-storage',
    name: 'Arweave & IPFS Archival',
    role: 'Storage Calculator',
    chainTarget: 'Permanent Permaweb Provenance',
    tensorProofType: 'Proof of Access & Content Addressing Hash',
    coordinationStatus: 'SYNCHRONIZED',
    lastBlockSync: 1490215,
    tpsEquivalent: 120,
    latencyToGodChain: 22
  }
];

export const INITIAL_Q_THERMO: QThermoMetrics = {
  currentEntropy: 14.82,
  energyBackingPerPi: 3.14159,
  biospherePurityIndex: 98.4,
  thermoEquilibriumRatio: 1.000000,
  poutwHash: 'MOCK_QTHERMO_ENTROPY_BALANCE_VERIFIED',
  agenticGdpVelocity: 4.82,
  zeroRentEfficiency: 99.98
};

export const INITIAL_SELF_HEALING_LOGS: SelfHealingEvent[] = [
  {
    id: 'heal-001',
    timestamp: '2m ago',
    incidentType: 'BYZANTINE_DRIFT',
    affectedTarget: 'Virginia NPAS Mainnet Bridge Relay (Node 3)',
    severity: 'RESOLVED',
    remediationAction: 'Gossip fanout dynamically elevated from factor 3 to 5. Quorum overlap restored to 100%.',
    recoveryLatencyMs: 340,
    autonomousAgent: 'SCP Consensus Auto-Healer'
  },
  {
    id: 'heal-002',
    timestamp: '14m ago',
    incidentType: 'MEMPOOL_FLOOD',
    affectedTarget: 'Unconfirmed Transaction Mempool Buffer',
    severity: 'RESOLVED',
    remediationAction: 'Non-compliant micro-spams filtered via dynamic zero-rent queue. Valid Pioneer transactions prioritized.',
    recoveryLatencyMs: 185,
    autonomousAgent: 'Mempool Traffic Arbiter'
  },
  {
    id: 'heal-003',
    timestamp: '42m ago',
    incidentType: 'ECLIPSE_ATTACK_ATTEMPT',
    affectedTarget: 'P2P Gossip Inbound Socket 185.220.101.5',
    severity: 'RESOLVED',
    remediationAction: 'Adversarial conflicting slot sequence dropped. Peer blacklisted on Trademark Firewall Sentinel registry.',
    recoveryLatencyMs: 92,
    autonomousAgent: 'Trademark & Sybil Firewall'
  }
];
