const { expect } = require('chai');
const { ethers, upgrades } = require('hardhat');

describe('Nexus Contract', function () {
  let Nexus, nexus, owner, minter, user1, user2, admin, upgrader;
  const NAME = 'Nexus Revoluter';
  const SYMBOL = 'NEXUS';
  const REWARD_RATE = ethers.parseEther('0.0001'); // 0.0001 Pi per second
  const MIN_STAKE = ethers.parseEther('1'); // 1 Pi
  const MIN_LOCK_PERIOD = 30 * 24 * 60 * 60; // 30 days in seconds
  const VOTING_PERIOD = 7 * 24 * 60 * 60; // 7 days in seconds
  const MIN_VOTE_THRESHOLD = ethers.parseEther('1000'); // 1000 Pi
  const TOKEN_URI = 'https://api.nexus-revoluter.io/nft/1';

  beforeEach(async () => {
    // Get signers
    [owner, minter, user1, user2, admin, upgrader] = await ethers.getSigners();

    // Deploy Nexus contract as UUPS proxy
    Nexus = await ethers.getContractFactory('Nexus');
    nexus = await upgrades.deployProxy(Nexus, [NAME, SYMBOL, REWARD_RATE], {
      initializer: 'initialize',
      kind: 'uups',
    });
    await nexus.waitForDeployment();

    // Assign roles
    await nexus.grantRole(await nexus.ADMIN_ROLE(), admin.address);
    await nexus.grantRole(await nexus.MINTER_ROLE(), minter.address);
    await nexus.grantRole(await nexus.UPGRADER_ROLE(), upgrader.address);
  });

  describe('Initialization', () => {
    it('should initialize with correct parameters', async () => {
      expect(await nexus.name()).to.equal(NAME);
      expect(await nexus.symbol()).to.equal(SYMBOL);
      expect(await nexus.rewardRate()).to.equal(REWARD_RATE);
      expect(await nexus.hasRole(await nexus.DEFAULT_ADMIN_ROLE(), owner.address)).to.be.true;
      expect(await nexus.hasRole(await nexus.ADMIN_ROLE(), admin.address)).to.be.true;
      expect(await nexus.hasRole(await nexus.MINTER_ROLE(), minter.address)).to.be.true;
      expect(await nexus.hasRole(await nexus.UPGRADER_ROLE(), upgrader.address)).to.be.true;
    });
  });

  describe('NFT Minting', () => {
    it('should allow minter to mint NFT', async () => {
      await expect(nexus.connect(minter).mintNFT(user1.address, TOKEN_URI))
        .to.emit(nexus, 'NFTMinted')
        .withArgs(user1.address, 1, TOKEN_URI);
      expect(await nexus.ownerOf(1)).to.equal(user1.address);
      expect(await nexus.tokenURI(1)).to.equal(TOKEN_URI);
    });

    it('should revert if non-minter tries to mint', async () => {
      await expect(nexus.connect(user1).mintNFT(user1.address, TOKEN_URI))
        .to.be.revertedWithCustomError(nexus, 'AccessControlUnauthorizedAccount');
    });

    it('should revert if paused', async () => {
      await nexus.connect(admin).pause();
      await expect(nexus.connect(minter).mintNFT(user1.address, TOKEN_URI))
        .to.be.revertedWithCustomError(nexus, 'EnforcedPause');
    });
  });

  describe('Staking', () => {
    it('should allow staking with valid amount and lock period', async () => {
      await expect(nexus.connect(user1).stake(MIN_LOCK_PERIOD, { value: MIN_STAKE }))
        .to.emit(nexus, 'Staked')
        .withArgs(user1.address, MIN_STAKE, MIN_LOCK_PERIOD);
      const stake = await nexus.stakes(user1.address);
      expect(stake.amount).to.equal(MIN_STAKE);
      expect(stake.lockPeriod).to.equal(MIN_LOCK_PERIOD);
      expect(stake.active).to.be.true;
    });

    it('should revert if stake amount is too low', async () => {
      await expect(nexus.connect(user1).stake(MIN_LOCK_PERIOD, { value: MIN_STAKE - 1n }))
        .to.be.revertedWith('Stake amount too low');
    });

    it('should revert if lock period is too short', async () => {
      await expect(nexus.connect(user1).stake(MIN_LOCK_PERIOD - 1, { value: MIN_STAKE }))
        .to.be.revertedWith('Lock period too short');
    });

    it('should revert if user already has active stake', async () => {
      await nexus.connect(user1).stake(MIN_LOCK_PERIOD, { value: MIN_STAKE });
      await expect(nexus.connect(user1).stake(MIN_LOCK_PERIOD, { value: MIN_STAKE }))
        .to.be.revertedWith('Already staking');
    });

    it('should calculate rewards correctly', async () => {
      await nexus.connect(user1).stake(MIN_LOCK_PERIOD, { value: MIN_STAKE });
      // Simulate time passing (1 day = 86400 seconds)
      await ethers.provider.send('evm_increaseTime', [86400]);
      await ethers.provider.send('evm_mine');
      const reward = await nexus.calculateReward(user1.address);
      const expectedReward = (MIN_STAKE * REWARD_RATE * 86400n) / BigInt(1e18);
      expect(reward).to.equal(expectedReward);
    });

    it('should allow unstaking after lock period', async () => {
      await nexus.connect(user1).stake(MIN_LOCK_PERIOD, { value: MIN_STAKE });
      await ethers.provider.send('evm_increaseTime', [MIN_LOCK_PERIOD]);
      await ethers.provider.send('evm_mine');
      const initialBalance = await ethers.provider.getBalance(user1.address);
      await expect(nexus.connect(user1).unstake())
        .to.emit(nexus, 'Unstaked')
        .withArgs(user1.address, MIN_STAKE, (MIN_STAKE * REWARD_RATE * BigInt(MIN_LOCK_PERIOD)) / BigInt(1e18));
      const finalBalance = await ethers.provider.getBalance(user1.address);
      expect(finalBalance).to.be.gt(initialBalance);
    });

    it('should revert unstaking before lock period', async () => {
      await nexus.connect(user1).stake(MIN_LOCK_PERIOD, { value: MIN_STAKE });
      await expect(nexus.connect(user1).unstake()).to.be.revertedWith('Stake still locked');
    });
  });

  describe('Governance', () => {
    beforeEach(async () => {
      // Stake enough for user1 to propose and vote
      await nexus.connect(user1).stake(MIN_LOCK_PERIOD, { value: MIN_VOTE_THRESHOLD });
    });

    it('should allow creating a proposal', async () => {
      const description = 'Increase reward rate';
      await expect(nexus.connect(user1).createProposal(description))
        .to.emit(nexus, 'ProposalCreated')
        .withArgs(1, user1.address, description);
      const proposal = await nexus.proposals(1);
      expect(proposal.description).to.equal(description);
      expect(proposal.deadline).to.be.gt(0);
    });

    it('should revert proposal creation if stake is insufficient', async () => {
      await expect(nexus.connect(user2).createProposal('Test proposal'))
        .to.be.revertedWith('Insufficient stake to propose');
    });

    it('should allow voting on a proposal', async () => {
      await nexus.connect(user1).createProposal('Test proposal');
      await expect(nexus.connect(user1).vote(1, true))
        .to.emit(nexus, 'Voted')
        .withArgs(user1.address, 1, true);
      const proposal = await nexus.proposals(1);
      expect(proposal.votesFor).to.equal(MIN_VOTE_THRESHOLD);
    });

    it('should revert voting if already voted', async () => {
      await nexus.connect(user1).createProposal('Test proposal');
      await nexus.connect(user1).vote(1, true);
      await expect(nexus.connect(user1).vote(1, true)).to.be.revertedWith('Already voted');
    });

    it('should revert voting if stake is insufficient', async () => {
      await nexus.connect(user1).createProposal('Test proposal');
      await expect(nexus.connect(user2).vote(1, true))
        .to.be.revertedWith('Insufficient stake to vote');
    });

    it('should execute a proposal after voting period', async () => {
      await nexus.connect(user1).createProposal('Test proposal');
      await nexus.connect(user1).vote(1, true);
      await ethers.provider.send('evm_increaseTime', [VOTING_PERIOD]);
      await ethers.provider.send('evm_mine');
      await expect(nexus.connect(admin).executeProposal(1))
        .to.emit(nexus, 'ProposalExecuted')
        .withArgs(1, true);
      const proposal = await nexus.proposals(1);
      expect(proposal.executed).to.be.true;
      expect(proposal.passed).to.be.true;
    });
  });

  describe('Access Control', () => {
    it('should allow admin to update reward rate', async () => {
      const newRewardRate = ethers.parseEther('0.0002');
      await nexus.connect(admin).updateRewardRate(newRewardRate);
      expect(await nexus.rewardRate()).to.equal(newRewardRate);
    });

    it('should revert if non-admin tries to update reward rate', async () => {
      await expect(nexus.connect(user1).updateRewardRate(ethers.parseEther('0.0002')))
        .to.be.revertedWithCustomError(nexus, 'AccessControlUnauthorizedAccount');
    });

    it('should allow admin to pause and unpause', async () => {
      await nexus.connect(admin).pause();
      expect(await nexus.paused()).to.be.true;
      await nexus.connect(admin).unpause();
      expect(await nexus.paused()).to.be.false;
    });

    it('should revert if non-admin tries to pause', async () => {
      await expect(nexus.connect(user1).pause())
        .to.be.revertedWithCustomError(nexus, 'AccessControlUnauthorizedAccount');
    });
  });

  describe('Pi Network KYC Integration', () => {
    it('should return true for KYC verification (placeholder)', async () => {
      expect(await nexus.verifyKYC(user1.address)).to.be.true; // Placeholder test
    });
  });

  describe('Upgradeability', () => {
    it('should allow upgrader to upgrade contract', async () => {
      const NexusV2 = await ethers.getContractFactory('Nexus');
      await expect(upgrades.upgradeProxy(nexus.target, NexusV2, { kind: 'uups' }))
        .to.not.be.reverted;
    });

    it('should revert if non-upgrader tries to upgrade', async () => {
      const NexusV2 = await ethers.getContractFactory('Nexus', user1);
      await expect(upgrades.upgradeProxy(nexus.target, NexusV2, { kind: 'uups' }))
        .to.be.revertedWithCustomError(nexus, 'AccessControlUnauthorizedAccount');
    });
  });
});
