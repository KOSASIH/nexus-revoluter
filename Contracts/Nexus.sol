// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/security/PausableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/security/ReentrancyGuardUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC721/ERC721Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC721/extensions/ERC721URIStorageUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/utils/CountersUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/utils/StringsUpgradeable.sol";

/// @title Nexus - Advanced Smart Contract for Pi Network
/// @notice A feature-rich, upgradeable contract for NFT minting, staking, and governance on Pi Network
/// @dev Uses UUPS proxy pattern, OpenZeppelin libraries, and Pi Network-compatible features
contract Nexus is
    Initializable,
    UUPSUpgradeable,
    AccessControlUpgradeable,
    PausableUpgradeable,
    ReentrancyGuardUpgradeable,
    ERC721Upgradeable,
    ERC721URIStorageUpgradeable
{
    using CountersUpgradeable for CountersUpgradeable.Counter;
    using StringsUpgradeable for uint256;

    // Roles for access control
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant UPGRADER_ROLE = keccak256("UPGRADER_ROLE");

    // NFT and staking counters
    CountersUpgradeable.Counter private _tokenIdCounter;
    CountersUpgradeable.Counter private _proposalIdCounter;

    // Staking structures
    struct Stake {
        uint256 amount;
        uint256 startTime;
        uint256 lockPeriod;
        bool active;
    }

    // Governance structures
    struct Proposal {
        uint256 id;
        address proposer;
        string description;
        uint256 votesFor;
        uint256 votesAgainst;
        uint256 deadline;
        bool executed;
        bool passed;
    }

    // Mappings
    mapping(address => Stake) public stakes;
    mapping(uint256 => Proposal) public proposals;
    mapping(address => mapping(uint256 => bool)) public hasVoted;
    mapping(uint256 => string) private _tokenURIs;

    // Staking parameters
    uint256 public constant MIN_STAKE = 1 ether; // 1 Pi token (adjust for Pi Network)
    uint256 public constant MIN_LOCK_PERIOD = 30 days;
    uint256 public rewardRate; // Reward rate per second (in wei)

    // Governance parameters
    uint256 public constant VOTING_PERIOD = 7 days;
    uint256 public constant MIN_VOTE_THRESHOLD = 1000 ether; // Minimum staked Pi for voting

    // Events
    event Staked(address indexed user, uint256 amount, uint256 lockPeriod);
    event Unstaked(address indexed user, uint256 amount, uint256 reward);
    event ProposalCreated(uint256 indexed proposalId, address indexed proposer, string description);
    event Voted(address indexed voter, uint256 indexed proposalId, bool support);
    event ProposalExecuted(uint256 indexed proposalId, bool passed);
    event NFTMinted(address indexed owner, uint256 indexed tokenId, string tokenURI);

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers(); // Prevent initialization outside proxy
    }

    /// @notice Initializes the contract with initial settings
    /// @param _name NFT collection name
    /// @param _symbol NFT collection symbol
    /// @param _rewardRate Initial reward rate for staking (wei per second)
    function initialize(string memory _name, string memory _symbol, uint256 _rewardRate) public initializer {
        __ERC721_init(_name, _symbol);
        __ERC721URIStorage_init();
        __AccessControl_init();
        __Pausable_init();
        __ReentrancyGuard_init();
        __UUPSUpgradeable_init();

        // Set up roles
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        _grantRole(UPGRADER_ROLE, msg.sender);

        rewardRate = _rewardRate;
    }

    /// @notice Authorizes contract upgrades (UUPS pattern)
    /// @dev Only UPGRADER_ROLE can call this
    function _authorizeUpgrade(address newImplementation) internal override onlyRole(UPGRADER_ROLE) {}

    // --- NFT Minting ---
    /// @notice Mints a new NFT with metadata
    /// @param recipient Address to receive the NFT
    /// @param tokenURI Metadata URI for the NFT
    /// @return tokenId The ID of the minted NFT
    function mintNFT(address recipient, string memory tokenURI)
        public
        onlyRole(MINTER_ROLE)
        whenNotPaused
        nonReentrant
        returns (uint256)
    {
        _tokenIdCounter.increment();
        uint256 tokenId = _tokenIdCounter.current();
        _safeMint(recipient, tokenId);
        _setTokenURI(tokenId, tokenURI);
        emit NFTMinted(recipient, tokenId, tokenURI);
        return tokenId;
    }

    // --- Staking ---
    /// @notice Stakes Pi tokens for rewards
    /// @param lockPeriod Duration to lock the stake (in seconds)
    function stake(uint256 lockPeriod) public payable whenNotPaused nonReentrant {
        require(msg.value >= MIN_STAKE, "Stake amount too low");
        require(lockPeriod >= MIN_LOCK_PERIOD, "Lock period too short");
        require(!stakes[msg.sender].active, "Already staking");

        stakes[msg.sender] = Stake({
            amount: msg.value,
            startTime: block.timestamp,
            lockPeriod: lockPeriod,
            active: true
        });

        emit Staked(msg.sender, msg.value, lockPeriod);
    }

    /// @notice Unstakes and claims rewards
    function unstake() public nonReentrant {
        Stake memory userStake = stakes[msg.sender];
        require(userStake.active, "No active stake");
        require(block.timestamp >= userStake.startTime + userStake.lockPeriod, "Stake still locked");

        uint256 reward = calculateReward(msg.sender);
        uint256 total = userStake.amount + reward;

        stakes[msg.sender].active = false;
        (bool success, ) = msg.sender.call{value: total}("");
        require(success, "Transfer failed");

        emit Unstaked(msg.sender, userStake.amount, reward);
    }

    /// @notice Calculates staking rewards
    /// @param user Address of the staker
    /// @return reward The calculated reward amount
    function calculateReward(address user) public view returns (uint256) {
        Stake memory userStake = stakes[user];
        if (!userStake.active) return 0;
        uint256 stakingDuration = block.timestamp - userStake.startTime;
        return (userStake.amount * rewardRate * stakingDuration) / 1e18;
    }

    // --- Governance ---
    /// @notice Creates a new governance proposal
    /// @param description Description of the proposal
    function createProposal(string memory description) public whenNotPaused {
        require(stakes[msg.sender].amount >= MIN_VOTE_THRESHOLD, "Insufficient stake to propose");
        _proposalIdCounter.increment();
        uint256 proposalId = _proposalIdCounter.current();

        proposals[proposalId] = Proposal({
            id: proposalId,
            proposer: msg.sender,
            description: description,
            votesFor: 0,
            votesAgainst: 0,
            deadline: block.timestamp + VOTING_PERIOD,
            executed: false,
            passed: false
        });

        emit ProposalCreated(proposalId, msg.sender, description);
    }

    /// @notice Votes on a proposal
    /// @param proposalId ID of the proposal
    /// @param support True for supporting, false for opposing
    function vote(uint256 proposalId, bool support) public whenNotPaused {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp < proposal.deadline, "Voting period ended");
        require(stakes[msg.sender].amount >= MIN_VOTE_THRESHOLD, "Insufficient stake to vote");
        require(!hasVoted[msg.sender][proposalId], "Already voted");

        hasVoted[msg.sender][proposalId] = true;
        if (support) {
            proposal.votesFor += stakes[msg.sender].amount;
        } else {
            proposal.votesAgainst += stakes[msg.sender].amount;
        }

        emit Voted(msg.sender, proposalId, support);
    }

    /// @notice Executes a proposal after voting
    /// @param proposalId ID of the proposal
    function executeProposal(uint256 proposalId) public onlyRole(ADMIN_ROLE) nonReentrant {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp >= proposal.deadline, "Voting period not ended");
        require(!proposal.executed, "Proposal already executed");

        proposal.executed = true;
        proposal.passed = proposal.votesFor > proposal.votesAgainst;

        // Placeholder for proposal execution logic (e.g., update contract parameters)
        emit ProposalExecuted(proposalId, proposal.passed);
    }

    // --- Admin Functions ---
    /// @notice Updates the staking reward rate
    /// @param newRewardRate New reward rate (wei per second)
    function updateRewardRate(uint256 newRewardRate) public onlyRole(ADMIN_ROLE) {
        require(newRewardRate > 0, "Invalid reward rate");
        rewardRate = newRewardRate;
    }

    /// @notice Pauses the contract
    function pause() public onlyRole(ADMIN_ROLE) {
        _pause();
    }

    /// @notice Unpauses the contract
    function unpause() public onlyRole(ADMIN_ROLE) {
        _unpause();
    }

    // --- ERC721 Overrides ---
    function _baseURI() internal view override returns (string memory) {
        return "https://api.nexus-revoluter.io/nft/"; // Replace with Pi Network-compatible metadata API
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721Upgradeable, ERC721URIStorageUpgradeable)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function _burn(uint256 tokenId) internal override(ERC721Upgradeable, ERC721URIStorageUpgradeable) {
        super._burn(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721Upgradeable, AccessControlUpgradeable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    // --- Pi Network Integration ---
    /// @notice Placeholder for Pi Network-specific KYC verification
    /// @dev To be implemented based on Pi Network's KYC API
    function verifyKYC(address user) public view returns (bool) {
        // Placeholder: Integrate with Pi Network's KYC API
        return true; // Assume KYC verified for demo purposes
    }

    // --- Fallback Function ---
    receive() external payable {
        // Allow receiving Pi tokens for staking or contract funding
    }
}
