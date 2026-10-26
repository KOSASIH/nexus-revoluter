import { WalletAddress, Transaction, Block, PeerNode, IoTDevice, TokenizedAsset, Proposal, SyncLog, ComplianceReport } from '../types';

export const INITIAL_ADDRESSES: WalletAddress[] = [
  {
    address: 'GDZX94K2MQW8VR91PXZL029471NVMS947194KOSASIH88',
    label: 'Primary Pioneer Node Vault',
    balance: 1450.75,
    piBalance: 31415.92,
    isPrimary: true,
    createdAt: '2025-01-15'
  },
  {
    address: 'GABR72K1PLMZ82937NYVX729485LKS837194REVOLUTER01',
    label: 'SANO Reserve Arbitrage Collateral',
    balance: 820.00,
    piBalance: 125000.00,
    isPrimary: false,
    createdAt: '2025-02-01'
  },
  {
    address: 'GCXP449102847192847291847192847192847NPASBRIDGE',
    label: 'NPAS Autonomous Bridge Escrow',
    balance: 314.16,
    piBalance: 8840.50,
    isPrimary: false,
    createdAt: '2025-02-18'
  }
];

export const INITIAL_TRANSACTIONS: Transaction[] = [
  {
    id: 'tx_7e93a04b12c84f67a',
    from: 'GDZX94K2MQW8VR91PXZL029471NVMS947194KOSASIH88',
    to: 'GABR72K1PLMZ82937NYVX729485LKS837194REVOLUTER01',
    amount: 314.15,
    asset: 'PI',
    timestamp: '2 mins ago',
    memo: 'SANO Liquidity peg adjustment',
    status: 'confirmed',
    fee: 0.0001,
    complianceChecked: true,
    blockNumber: 4920194
  },
  {
    id: 'tx_982bf7210eac9312b',
    from: 'GCXP449102847192847291847192847192847NPASBRIDGE',
    to: 'GDZX94K2MQW8VR91PXZL029471NVMS947194KOSASIH88',
    amount: 120.00,
    asset: 'PI',
    timestamp: '18 mins ago',
    memo: 'NPAS Sync Reward: Epoch 884',
    status: 'confirmed',
    fee: 0.0001,
    complianceChecked: true,
    blockNumber: 4920182
  },
  {
    id: 'tx_31fa92019c8d3211e',
    from: 'GDZX94K2MQW8VR91PXZL029471NVMS947194KOSASIH88',
    to: 'GDF7102947192847192847192847192847192847VALIDTR',
    amount: 50.00,
    asset: 'XLM',
    timestamp: '1 hour ago',
    memo: 'Gossip protocol node lease fee',
    status: 'confirmed',
    fee: 0.00001,
    complianceChecked: true,
    blockNumber: 4920140
  },
  {
    id: 'tx_55ba890123efcba49',
    from: 'GABR72K1PLMZ82937NYVX729485LKS837194REVOLUTER01',
    to: 'GDZX94K2MQW8VR91PXZL029471NVMS947194KOSASIH88',
    amount: 1000.00,
    asset: 'NRV',
    timestamp: '3 hours ago',
    memo: 'Quantum-AI reserve yield settlement',
    status: 'confirmed',
    fee: 0.0002,
    complianceChecked: true,
    blockNumber: 4920089
  }
];

export const INITIAL_BLOCKS: Block[] = [
  {
    height: 4920194,
    hash: '0x9d82f7103a8ec492ba37482910faecb891240182749102938471928374619283',
    previousHash: '0x8c71e6092b7db381a926371809ebda7801390171638091827360817263508172',
    validator: 'Nexus-Pi-Genesis-01 (Frankfurt)',
    txCount: 42,
    timestamp: 'Just now',
    sizeKb: 128.4,
    gasUsed: 1420950
  },
  {
    height: 4920193,
    hash: '0x8c71e6092b7db381a926371809ebda7801390171638091827360817263508172',
    previousHash: '0x7b60d5981a6ca2709815260798daca6790289060527980716259706152497061',
    validator: 'Nexus-SANO-Core-Tokyo',
    txCount: 38,
    timestamp: '5s ago',
    sizeKb: 112.8,
    gasUsed: 1284500
  },
  {
    height: 4920192,
    hash: '0x7b60d5981a6ca2709815260798daca6790289060527980716259706152497061',
    previousHash: '0x6a5fc487095b916f8704159687cb9b568917895f416879605148695041386950',
    validator: 'Nexus-NPAS-Sync-Virginia',
    txCount: 57,
    timestamp: '11s ago',
    sizeKb: 164.2,
    gasUsed: 1892000
  },
  {
    height: 4920191,
    hash: '0x6a5fc487095b916f8704159687cb9b568917895f416879605148695041386950',
    previousHash: '0x594eb376f84a805e76f3048576ba8a457806784e3057685f4037584f3027584f',
    validator: 'Nexus-Stellar-Horizon-Zurich',
    txCount: 29,
    timestamp: '17s ago',
    sizeKb: 94.6,
    gasUsed: 984000
  }
];

export const INITIAL_PEERS: PeerNode[] = [
  {
    id: 'node-fra-01',
    name: 'Frankfurt Core Validator #1',
    ip: '142.93.18.91:8080',
    location: 'Frankfurt, Germany',
    role: 'Validator',
    pingMs: 14,
    uptime: '99.99%',
    status: 'active',
    version: 'v1.4.2-nexus'
  },
  {
    id: 'node-tyo-04',
    name: 'Tokyo SANO Orchestration Sentinel',
    ip: '133.242.17.84:8080',
    location: 'Tokyo, Japan',
    role: 'SANO Orchestrator',
    pingMs: 42,
    uptime: '99.98%',
    status: 'active',
    version: 'v1.4.2-nexus'
  },
  {
    id: 'node-iad-02',
    name: 'Virginia NPAS Mainnet Bridge Relay',
    ip: '54.210.88.192:8080',
    location: 'Virginia, USA',
    role: 'NPAS Relayer',
    pingMs: 68,
    uptime: '99.95%',
    status: 'active',
    version: 'v1.4.1-nexus'
  },
  {
    id: 'node-sin-09',
    name: 'Singapore Quantum Consensus Node',
    ip: '128.199.204.12:8080',
    location: 'Singapore',
    role: 'Validator',
    pingMs: 31,
    uptime: '99.99%',
    status: 'active',
    version: 'v1.4.2-nexus'
  },
  {
    id: 'node-zrh-03',
    name: 'Zurich Stellar Archive Node',
    ip: '185.19.28.104:8080',
    location: 'Zurich, Switzerland',
    role: 'Archive Node',
    pingMs: 22,
    uptime: '100.00%',
    status: 'active',
    version: 'v1.4.2-nexus'
  }
];

export const INITIAL_IOT_DEVICES: IoTDevice[] = [
  {
    deviceId: 'IOT-PI-WEATHER-9021',
    deviceType: 'Micro-Climate Environmental Station',
    location: 'Alpine Node Station #4, Valais (CH)',
    status: 'online',
    lastPing: '3s ago',
    metrics: {
      battery: 98,
      signal: 94,
      temperature: 14.2,
      powerKw: 0.12,
      telemetryRate: '1 packet / 5s',
      reading: 'Atmospheric: 1013.2 hPa | Humidity: 54% | Solar Irradiance: 720 W/m²'
    }
  },
  {
    deviceId: 'IOT-NX-SOLAR-414',
    deviceType: 'Smart Solar Inverter & Grid Gateway',
    location: 'Solar Farm Alpha, Zaragoza (ES)',
    status: 'online',
    lastPing: '8s ago',
    metrics: {
      battery: 100,
      signal: 89,
      temperature: 28.6,
      powerKw: 48.5,
      telemetryRate: '1 packet / 1s',
      reading: 'Generation: 48.5 kW | Grid Feed: 46.2 kW | Inverter Efficiency: 98.7%'
    }
  },
  {
    deviceId: 'IOT-GEO-WATER-882',
    deviceType: 'Aquifer & Hydro-Telemetry Sensor',
    location: 'Columbia River Basin (US)',
    status: 'online',
    lastPing: '22s ago',
    metrics: {
      battery: 84,
      signal: 78,
      temperature: 11.4,
      powerKw: 0.05,
      telemetryRate: '1 packet / 30s',
      reading: 'Flow Rate: 4.8 m³/s | Turbidity: 1.2 NTU | pH Level: 7.42'
    }
  },
  {
    deviceId: 'IOT-SEC-VAULT-109',
    deviceType: 'Biometric Hardware HSM Escrow',
    location: 'Singapore Secure Data Center Pod 3',
    status: 'online',
    lastPing: '1s ago',
    metrics: {
      battery: 100,
      signal: 99,
      temperature: 18.0,
      powerKw: 0.45,
      telemetryRate: 'Continuous Heartbeat',
      reading: 'Tamper Sensors: ARMED | ZK Hardware Enclave: ACTIVE | Ed25519 Keys: SECURE'
    }
  }
];

export const INITIAL_TOKENIZED_ASSETS: TokenizedAsset[] = [
  {
    assetId: 'ASSET-SOLAR-ZG-01',
    name: 'Zaragoza Photovoltaic Cluster A',
    owner: 'Pioneer Renewable Cooperative',
    tokenizedValue: 500000,
    valuationUsd: 157079500000,
    tokenSymbol: 'nSOLAR',
    category: 'Renewable Energy',
    auditDate: '2025-01-20 (DNV GL Certified)',
    status: 'active'
  },
  {
    assetId: 'ASSET-CARBON-AMAZON-88',
    name: 'Amazon Rainforest Bio-Resilience Carbon Credits',
    owner: 'Global Ecological Trust',
    tokenizedValue: 250000,
    valuationUsd: 78539750000,
    tokenSymbol: 'nBIO',
    category: 'Carbon Credit',
    auditDate: '2025-02-10 (Verra Gold Standard)',
    status: 'active'
  },
  {
    assetId: 'ASSET-QUANTUM-COMPUTE-09',
    name: 'Distributed GPU/Quantum Accelerator Pods',
    owner: 'Nexus Revoluter Decentralized Compute DAO',
    tokenizedValue: 120000,
    valuationUsd: 37699080000,
    tokenSymbol: 'nCOMP',
    category: 'Compute Cluster',
    auditDate: '2025-02-15 (IEEE Blockchain Spec)',
    status: 'active'
  },
  {
    assetId: 'ASSET-LOGISTICS-HUB-ROTT',
    name: 'Rotterdam Port Autonomous Logistics Hub',
    owner: 'North Sea Maritime Syndicate',
    tokenizedValue: 750000,
    valuationUsd: 235619250000,
    tokenSymbol: 'nPORT',
    category: 'Real Estate',
    auditDate: '2025-02-22 (RICS Verified)',
    status: 'active'
  }
];

export const INITIAL_PROPOSALS: Proposal[] = [
  {
    id: 'SANO-PROP-014',
    title: 'Increase SANO Arbitrage Liquidity Reserve Depth to 500,000 PI',
    description: 'Proposes expanding the automated liquidity reserve pool to dampen micro-volatility deviations from the $314,159.00 USD peg during sudden cross-chain liquidity surges.',
    proposer: 'GDZX94K2...KOSASIH88',
    category: 'Monetary Policy',
    votesFor: 84120,
    votesAgainst: 1230,
    votesAbstain: 450,
    status: 'active',
    deadline: 'In 3 days'
  },
  {
    id: 'NPAS-PROP-009',
    title: 'Deploy Dedicated High-Frequency RPC Relays for Pi Ecosystem DApps',
    description: 'Establishes three regional edge proxies in Tokyo, Frankfurt, and São Paulo to reduce synchronization latency between Pi Browser and Nexus Node to sub-20ms.',
    proposer: 'GABR72K1...REVOLUTER01',
    category: 'Network Upgrade',
    votesFor: 124900,
    votesAgainst: 340,
    votesAbstain: 120,
    status: 'passed',
    deadline: 'Concluded'
  },
  {
    id: 'DAO-PROP-042',
    title: 'Community Fault-Tolerance Incentive Tier Allocation (Epoch 2025-Q1)',
    description: 'Allocate 25,000 PI from the Pioneer Ecosystem Fund to reward node runners who report latency bottlenecks and validate zero-knowledge KYC state proofs.',
    proposer: 'Pioneer_Sentinel_Core',
    category: 'Community Fund',
    votesFor: 98310,
    votesAgainst: 4890,
    votesAbstain: 2100,
    status: 'active',
    deadline: 'In 5 days'
  }
];

export const INITIAL_SYNC_LOGS: SyncLog[] = [
  {
    id: 'sync-9012',
    timestamp: '10:42:15',
    target: 'minepi.com',
    operation: 'Repository & Mainnet Protocol Rules Synchronized',
    status: 'synced',
    latencyMs: 18,
    verifiedByZk: true
  },
  {
    id: 'sync-9011',
    timestamp: '10:42:01',
    target: 'wallet.pinet.com',
    operation: 'Stellar Keypair Balance & Nonce Reconciliation',
    status: 'synced',
    latencyMs: 24,
    verifiedByZk: true
  },
  {
    id: 'sync-9010',
    timestamp: '10:41:45',
    target: 'ecosystem.pinet.com',
    operation: 'Smart Contract ABI & Metadata Broadcast',
    status: 'synced',
    latencyMs: 16,
    verifiedByZk: true
  },
  {
    id: 'sync-9009',
    timestamp: '10:41:30',
    target: 'Stellar Horizon',
    operation: 'Ledger Sequence #4920194 State Commit',
    status: 'synced',
    latencyMs: 32,
    verifiedByZk: true
  }
];

export const INITIAL_COMPLIANCE_REPORT: ComplianceReport = {
  reportId: 'ARHN-ZK-8841-A',
  userPublicKey: 'GDZX94K2MQW8VR91PXZL029471NVMS947194KOSASIH88',
  status: 'verified',
  zkProofHash: 'zkp_snark_9f82bc710a34e569d128374a',
  riskScore: 2,
  checks: {
    amlCheck: true,
    sanctionList: true,
    velocityRisk: true,
    geoCompliance: true
  },
  timestamp: '2025-02-26 10:30 UTC',
  empathyFeedback: 'Pioneer identity verified with 100% zero-knowledge cryptographic privacy. All compliance standards satisfied.'
};
