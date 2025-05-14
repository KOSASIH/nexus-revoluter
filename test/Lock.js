const { expect } = require('chai');
const { ethers, upgrades } = require('hardhat');

describe('Lock Contract', function () {
  let Lock, lock, Nexus, nexus, owner, approver, user1, user2, admin, upgrader;
  const MIN_LOCK_PERIOD = 1 * 24 * 60 * 60; // 1 day in seconds
  const MAX_APPROVALS = 10;
  const TOKEN_URI = 'https://api.nexus-revoluter.io/nft/1';

  beforeEach(async () => {
    // Get signers
    [owner, approver, user1, user2, admin, upgrader] = await ethers.getSigners();

    // Deploy Nexus contract
    Nexus = await ethers.getContractFactory('Nexus');
    nexus = await upgrades.deployProxy(Nexus, ['Nexus Revoluter', 'NEXUS', ethers.parseEther('0.0001')], {
      initializer: 'initialize',
      kind: 'uups',
    });
    await nexus.waitForDeployment();

    // Deploy Lock contract
    Lock = await ethers.getContractFactory('Lock');
    lock = await upgrades.deployProxy(Lock, [nexus.target], {
      initializer: 'initialize',
      kind: 'uups',
    });
    await lock.waitForDeployment();

    // Assign roles
    await lock.grantRole(await lock.ADMIN_ROLE(), admin.address);
    await lock.grantRole(await lock.APPROVER_ROLE(), approver.address);
    await lock.grantRole(await lock.UPGRADER_ROLE(), upgrader.address);
    await nexus.grantRole(await nexus.MINTER_ROLE(), owner.address);
  });

  describe('Initialization', () => {
    it('should initialize with correct parameters', async () => {
      expect(await lock.nexusContract()).to.equal(nexus.target);
      expect(await lock.hasRole(await lock.DEFAULT_ADMIN_ROLE(), owner.address)).to.be.true;
      expect(await lock.hasRole(await lock.ADMIN_ROLE(), admin.address)).to.be.true;
      expect(await lock.hasRole(await lock.APPROVER_ROLE(), approver.address)).to.be.true;
      expect(await lock.hasRole(await lock.UPGRADER_ROLE(), upgrader.address)).to.be.true;
    });
  });

  describe('Locking Native Pi Tokens', () => {
    it('should lock Pi tokens with valid parameters', async () => {
      const releaseTime = Math.floor(Date.now() / 1000) + MIN_LOCK_PERIOD;
      const amount = ethers.parseEther('1');
      await expect(lock.connect(user1).lock(user1.address, releaseTime, true, 1, { value: amount }))
        .to.emit(lock, 'Locked')
        .withArgs(1, user1.address, amount, 0, ethers.ZeroAddress, releaseTime, true, 1);
      const lockInfo = await lock.locks(1);
      expect(lockInfo.beneficiary).to.equal(user1.address);
      expect(lockInfo.amount).to.equal(amount);
      expect(lockInfo.tokenAddress).to.equal(ethers.ZeroAddress);
      expect(lockInfo.releaseTime).to.equal(releaseTime);
      expect(lockInfo.requiresKYC).to.be.true;
      expect(lockInfo.approvalsRequired).to.equal(1);
    });

    it('should revert if no funds sent', async () => {
      const releaseTime = Math.floor(Date.now() / 1000) + MIN_LOCK_PERIOD;
      await expect(lock.connect(user1).lock(user1.address, releaseTime, true, 1))
        .to.be.revertedWith('No funds sent');
    });

    it('should revert if release time is too soon', async () => {
      const releaseTime = Math.floor(Date.now() / 1000);
      await expect(lock.connect(user1).lock(user1.address, releaseTime, true, 1, { value: ethers.parseEther('1') }))
        .to.be.revertedWith('Release time too soon');
    });

    it('should revert if too many approvals required', async () => {
      const releaseTime = Math.floor(Date.now() / 1000) + MIN_LOCK_PERIOD;
      await expect(
        lock.connect(user1).lock(user1.address, releaseTime, true, MAX_APPROVALS + 1, { value: ethers.parseEther('1') })
      ).to.be.revertedWith('Too many approvals required');
    });
  });

  describe('Locking NFTs', () => {
    it('should lock an NFT from Nexus', async () => {
      // Mint NFT
      await nexus.mintNFT(user1.address, TOKEN_URI);
      await nexus.connect(user1).approve(lock.target, 1);
      const releaseTime = Math.floor(Date.now() / 1000) + MIN_LOCK_PERIOD;
      await expect(lock.connect(user1).lockNFT(1, user2.address, releaseTime, true, 1))
        .to.emit(lock, 'Locked')
        .withArgs(1, user2.address, 0, 1, nexus.target, releaseTime, true, 1);
      const lockInfo = await lock.locks(1);
      expect(lockInfo.beneficiary).to.equal(user2.address);
      expect(lockInfo.tokenId).to.equal(1);
      expect(lockInfo.tokenAddress).to.equal(nexus.target);
      expect(await nexus.ownerOf(1)).to.equal(lock.target);
    });

    it('should revert if not NFT owner', async () => {
      await nexus.mintNFT(user1.address, TOKEN_URI);
      const releaseTime = Math.floor(Date.now() / 1000) + MIN_LOCK_PERIOD;
      await expect(lock.connect(user2).lockNFT(1, user2.address, releaseTime, true, 1))
        .to.be.revertedWith('Not NFT owner');
    });

    it('should revert if Nexus contract not set', async () => {
      // Deploy new Lock with zero address for Nexus
      const LockNew = await ethers.getContractFactory('Lock');
      const lockNew = await upgrades.deployProxy(LockNew, [ethers.ZeroAddress], {
        initializer: 'initialize',
        kind: 'uups',
      });
      await lockNew.waitForDeployment();
      const releaseTime = Math.floor(Date.now() / 1000) + MIN_LOCK_PERIOD;
      await expect(lockNew.connect(user1).lockNFT(1, user2.address, releaseTime, true, 1))
        .to.be.revertedWith('Nexus contract not set');
    });
  });

  describe('Locking ERC20 Tokens', () => {
    let token;

    beforeEach(async () => {
      // Deploy mock ERC20 token
      const Token = await ethers.getContractFactory('MockERC20');
      token = await Token.deploy('Mock Pi', 'MPI', ethers.parseEther('10000'));
      await token.waitForDeployment();
      await token.transfer(user1.address, ethers.parseEther('1000'));
      await token.connect(user1).approve(lock.target, ethers.parseEther('1000'));
    });

    it('should lock ERC20 tokens', async () => {
      const releaseTime = Math.floor(Date.now() / 1000) + MIN_LOCK_PERIOD;
      const amount = ethers.parseEther('100');
      await expect(lock.connect(user1).lockERC20(token.target, amount, user1.address, releaseTime, true, 1))
        .to.emit(lock, 'Locked')
        .withArgs(1, user1.address, amount, 0, token.target, releaseTime, true, 1);
      const lockInfo = await lock.locks(1);
      expect(lockInfo.amount).to.equal(amount);
      expect(lockInfo.tokenAddress).to.equal(token.target);
    });

    it('should revert if token transfer fails', async () => {
      const releaseTime = Math.floor(Date.now() / 1000) + MIN_LOCK_PERIOD;
      await expect(lock.connect(user2).lockERC20(token.target, ethers.parseEther('100'), user2.address, releaseTime, true, 1))
        .to.be.revertedWith('Token transfer failed');
    });
  });

  describe('Unlocking', () => {
    it('should unlock Pi tokens after release time and approval', async () => {
      const releaseTime = Math.floor(Date.now() / 1000) + MIN_LOCK_PERIOD;
      const amount = ethers.parseEther('1');
      await lock.connect(user1).lock(user1.address, releaseTime, false, 1, { value: amount });
      await lock.connect(approver).approveLock(1);
      await ethers.provider.send('evm_increaseTime', [MIN_LOCK_PERIOD]);
      await ethers.provider.send('evm_mine');
      const initialBalance = await ethers.provider.getBalance(user1.address);
      await expect(lock.connect(user1).unlock(1))
        .to.emit(lock, 'Unlocked')
        .withArgs(1, user1.address, amount, 0);
      expect(await ethers.provider.getBalance(user1.address)).to.be.gt(initialBalance);
    });

    it('should unlock NFT after release time and approval', async () => {
      await nexus.mintNFT(user1.address, TOKEN_URI);
      await nexus.connect(user1).approve(lock.target, 1);
      const releaseTime = Math.floor(Date.now() / 1000) + MIN_LOCK_PERIOD;
      await lock.connect(user1).lockNFT(1, user2.address, releaseTime, false, 1);
      await lock.connect(approver).approveLock(1);
      await ethers.provider.send('evm_increaseTime', [MIN_LOCK_PERIOD]);
      await ethers.provider.send('evm_mine');
      await expect(lock.connect(user2).unlock(1))
        .to.emit(lock, 'Unlocked')
        .withArgs(1, user2.address, 0, 1);
      expect(await nexus.ownerOf(1)).to.equal(user2.address);
    });

    it('should revert if not beneficiary', async () => {
      const releaseTime = Math.floor(Date.now() / 1000) + MIN_LOCK_PERIOD;
      await lock.connect(user1).lock(user1.address, releaseTime, false, 1, { value: ethers.parseEther('1') });
      await lock.connect(approver).approveLock(1);
      await ethers.provider.send('evm_increaseTime', [MIN_LOCK_PERIOD]);
      await ethers.provider.send('evm_mine');
      await expect(lock.connect(user2).unlock(1)).to.be.revertedWith('Not beneficiary');
    });

    it('should revert if lock already released', async () => {
      const releaseTime = Math.floor(Date.now() / 1000) + MIN_LOCK_PERIOD;
      await lock.connect(user1).lock(user1.address, releaseTime, false, 1, { value: ethers.parseEther('1') });
      await lock.connect(approver).approveLock(1);
      await ethers.provider.send('evm_increaseTime', [MIN_LOCK_PERIOD]);
      await ethers.provider.send('evm_mine');
      await lock.connect(user1).unlock(1);
      await expect(lock.connect(user1).unlock(1)).to.be.revertedWith('Lock already released');
    });
  });

  describe('Batch Locking', () => {
    it('should batch lock Pi tokens', async () => {
      const releaseTime = Math.floor(Date.now() / 1000) + MIN_LOCK_PERIOD;
      const beneficiaries = [user1.address, user2.address];
      const amounts = [ethers.parseEther('1'), ethers.parseEther('2')];
      const releaseTimes = [releaseTime, releaseTime];
      const requiresKYCs = [true, false];
      const approvalsRequired = [1, 1];
      await expect(lock.batchLock(beneficiaries, amounts, releaseTimes, requiresKYCs, approvalsRequired, { value: ethers.parseEther('3') }))
        .to.emit(lock, 'Locked')
        .withArgs(1, user1.address, ethers.parseEther('1'), 0, ethers.ZeroAddress, releaseTime, true, 1)
        .to.emit(lock, 'Locked')
        .withArgs(2, user2.address, ethers.parseEther('2'), 0, ethers.ZeroAddress, releaseTime, false, 1);
    });

    it('should revert if arrays mismatch', async () => {
      const releaseTime = Math.floor(Date.now() / 1000) + MIN_LOCK_PERIOD;
      await expect(lock.batchLock([user1.address], [ethers.parseEther('1'), ethers.parseEther('2')], [releaseTime], [true], [1]))
        .to.be.revertedWith('Array length mismatch');
    });
  });

  describe('Approvals', () => {
    it('should allow approver to approve a lock', async () => {
      const releaseTime = Math.floor(Date.now() / 1000) + MIN_LOCK_PERIOD;
      await lock.connect(user1).lock(user1.address, releaseTime, false, 1, { value: ethers.parseEther('1') });
      await expect(lock.connect(approver).approveLock(1))
        .to.emit(lock, 'ApprovalGiven')
        .withArgs(1, approver.address);
      const lockInfo = await lock.locks(1);
      expect(lockInfo.approvalsReceived).to.equal(1);
    });

    it('should revert if non-approver tries to approve', async () => {
      const releaseTime = Math.floor(Date.now() / 1000) + MIN_LOCK_PERIOD;
      await lock.connect(user1).lock(user1.address, releaseTime, false, 1, { value: ethers.parseEther('1') });
      await expect(lock.connect(user1).approveLock(1))
        .to.be.revertedWithCustomError(lock, 'AccessControlUnauthorizedAccount');
    });
  });

  describe('Access Control', () => {
    it('should allow admin to update Nexus contract', async () => {
      const newNexus = ethers.Wallet.createRandom().address;
      await expect(lock.connect(admin).updateNexusContract(newNexus))
        .to.emit(lock, 'NexusContractUpdated')
        .withArgs(nexus.target, newNexus);
      expect(await lock.nexusContract()).to.equal(newNexus);
    });

    it('should revert if non-admin tries to update Nexus', async () => {
      await expect(lock.connect(user1).updateNexusContract(ethers.Wallet.createRandom().address))
        .to.be.revertedWithCustomError(lock, 'AccessControlUnauthorizedAccount');
    });

    it('should allow admin to pause and unpause', async () => {
      await lock.connect(admin).pause();
      expect(await lock.paused()).to.be.true;
      await lock.connect(admin).unpause();
      expect(await lock.paused()).to.be.false;
    });
  });

  describe('Pi Network KYC Integration', () => {
    it('should return true for KYC verification (placeholder)', async () => {
      expect(await lock.verifyKYC(user1.address)).to.be.true; // Placeholder
    });
  });

  describe('Upgradeability', () => {
    it('should allow upgrader to upgrade contract', async () => {
      const LockV2 = await ethers.getContractFactory('Lock');
      await expect(upgrades.upgradeProxy(lock.target, LockV2, { kind: 'uups' }))
        .to.not.be.reverted;
    });

    it('should revert if non-upgrader tries to upgrade', async () => {
      const LockV2 = await ethers.getContractFactory('Lock', user1);
      await expect(upgrades.upgradeProxy(lock.target, LockV2, { kind: 'uups' }))
        .to.be.revertedWithCustomError(lock, 'AccessControlUnauthorizedAccount');
    });
  });
});

// Mock ERC20 for testing
const { AbiCoder } = require('ethers');
const { Interface } = require('@ethersproject/abi');

const MockERC20Artifact = {
  contractName: 'MockERC20',
  sourceName: 'contracts/MockERC20.sol',
  abi: [
    {
      inputs: [
        { internalType: 'string', name: 'name', type: 'string' },
        { internalType: 'string', name: 'symbol', type: 'string' },
        { internalType: 'uint256', name: 'initialSupply', type: 'uint256' },
      ],
      stateMutability: 'nonpayable',
      type: 'constructor',
    },
    {
      anonymous: false,
      inputs: [
        { indexed: true, internalType: 'address', name: 'owner', type: 'address' },
        { indexed: true, internalType: 'address', name: 'spender', type: 'address' },
        { indexed: false, internalType: 'uint256', name: 'value', type: 'uint256' },
      ],
      name: 'Approval',
      type: 'event',
    },
    {
      anonymous: false,
      inputs: [
        { indexed: true, internalType: 'address', name: 'from', type: 'address' },
        { indexed: true, internalType: 'address', name: 'to', type: 'address' },
        { indexed: false, internalType: 'uint256', name: 'value', type: 'uint256' },
      ],
      name: 'Transfer',
      type: 'event',
    },
    {
      inputs: [
        { internalType: 'address', name: 'owner', type: 'address' },
        { internalType: 'address', name: 'spender', type: 'address' },
      ],
      name: 'allowance',
      outputs: [{ internalType: 'uint256', name: '', type: 'uint256' }],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [
        { internalType: 'address', name: 'spender', type: 'address' },
        { internalType: 'uint256', name: 'amount', type: 'uint256' },
      ],
      name: 'approve',
      outputs: [{ internalType: 'bool', name: '', type: 'bool' }],
      stateMutability: 'nonpayable',
      type: 'function',
    },
    {
      inputs: [{ internalType: 'address', name: 'account', type: 'address' }],
      name: 'balanceOf',
      outputs: [{ internalType: 'uint256', name: '', type: 'uint256' }],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [],
      name: 'decimals',
      outputs: [{ internalType: 'uint8', name: '', type: 'uint8' }],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [],
      name: 'name',
      outputs: [{ internalType: 'string', name: '', type: 'string' }],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [],
      name: 'symbol',
      outputs: [{ internalType: 'string', name: '', type: 'string' }],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [],
      name: 'totalSupply',
      outputs: [{ internalType: 'uint256', name: '', type: 'uint256' }],
      stateMutability: 'view',
      type: 'function',
    },
    {
      inputs: [
        { internalType: 'address', name: 'to', type: 'address' },
        { internalType: 'uint256', name: 'amount', type: 'uint256' },
      ],
      name: 'transfer',
      outputs: [{ internalType: 'bool', name: '', type: 'bool' }],
      stateMutability: 'nonpayable',
      type: 'function',
    },
    {
      inputs: [
        { internalType: 'address', name: 'from', type: 'address' },
        { internalType: 'address', name: 'to', type: 'address' },
        { internalType: 'uint256', name: 'amount', type: 'uint256' },
      ],
      name: 'transferFrom',
      outputs: [{ internalType: 'bool', name: '', type: 'bool' }],
      stateMutability: 'nonpayable',
      type: 'function',
    },
  ],
  bytecode: '...', // Omitted for brevity
};

ethers.getContractFactory('MockERC20').then((factory) => {
  factory.interface = new Interface(MockERC20Artifact.abi);
  factory.bytecode = MockERC20Artifact.bytecode;
});
