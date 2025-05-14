// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/security/PausableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/security/ReentrancyGuardUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC20/IERC20Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC721/IERC721Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/utils/CountersUpgradeable.sol";

/// @title Lock - Advanced Timelock Contract for Pi Network
/// @notice A feature-rich, upgradeable contract for locking and managing funds/assets with governance and KYC integration
/// @dev Uses UUPS proxy pattern, integrates with Nexus.sol, and supports Pi Network
contract Lock is
    Initializable,
    UUPSUpgradeable,
    AccessControlUpgradeable,
    PausableUpgradeable,
    ReentrancyGuardUpgradeable
{
    using CountersUpgradeable for CountersUpgradeable.Counter;

    // Roles for access control
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant APPROVER_ROLE = keccak256("APPROVER_ROLE");
    bytes32 public constant UPGRADER_ROLE = keccak256("UPGRADER_ROLE");

    // Lock structure
    struct LockInfo {
        address beneficiary;
        uint256 amount; // For ERC20 or native tokens (Pi)
        uint256 tokenId; // For ERC721 (NFTs, 0 if not used)
        address tokenAddress; // Address of ERC20/ERC721 contract (0 if native Pi)
        uint256 releaseTime;
        bool requiresKYC;
        uint256 approvalsRequired;
        uint256 approvalsReceived;
        mapping(address => bool) approvedBy;
        bool released;
    }

    // Mappings
    mapping(uint256 => LockInfo) public locks;
    CountersUpgradeable.Counter private _lockIdCounter;

    // Nexus contract interface (for NFT/staking integration)
    address public nexusContract;

    // Constants
    uint256 public constant MIN_LOCK_PERIOD = 1 days;
    uint256 public constant MAX_APPROVALS = 10; // Max approvers for multi-party locks

    // Events
    event Locked(
        uint256 indexed lockId,
        address indexed beneficiary,
        uint256 amount,
        uint256 tokenId,
        address tokenAddress,
        uint256 releaseTime,
        bool requiresKYC,
        uint256 approvalsRequired
    );
    event Unlocked(uint256 indexed lockId, address indexed beneficiary, uint256 amount, uint256 tokenId);
    event ApprovalGiven(uint256 indexed lockId, address indexed approver);
    event NexusContractUpdated(address indexed oldNexus, address indexed newNexus);

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    /// @notice Initializes the contract
    /// @param _nexusContract Address of the Nexus contract
    function initialize(address _nexusContract) public initializer {
        __AccessControl_init();
        __Pausable_init();
        __ReentrancyGuard_init();
        __UUPSUpgradeable_init();

        nexusContract = _nexusContract;

        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ADMIN_ROLE, msg.sender);
        _grantRole(APPROVER_ROLE, msg.sender);
        _grantRole(UPGRADER_ROLE, msg.sender);
    }

    /// @notice Authorizes contract upgrades
    function _authorizeUpgrade(address newImplementation) internal override onlyRole(UPGRADER_ROLE) {}

    // --- Locking Functions ---
    /// @notice Locks native Pi tokens
    /// @param beneficiary Address to receive funds after release
    /// @param releaseTime Timestamp when funds can be released
    /// @param requiresKYC Whether KYC is required for release
    /// @param approvalsRequired Number of approvals needed
    function lock(
        address beneficiary,
        uint256 releaseTime,
        bool requiresKYC,
        uint256 approvalsRequired
    ) public payable whenNotPaused nonReentrant returns (uint256) {
        require(msg.value > 0, "No funds sent");
        require(beneficiary != address(0), "Invalid beneficiary");
        require(releaseTime >= block.timestamp + MIN_LOCK_PERIOD, "Release time too soon");
        require(approvalsRequired <= MAX_APPROVALS, "Too many approvals required");

        _lockIdCounter.increment();
        uint256 lockId = _lockIdCounter.current();

        LockInfo storage lockInfo = locks[lockId];
        lockInfo.beneficiary = beneficiary;
        lockInfo.amount = msg.value;
        lockInfo.tokenId = 0; // No NFT
        lockInfo.tokenAddress = address(0); // Native Pi
        lockInfo.releaseTime = releaseTime;
        lockInfo.requiresKYC = requiresKYC;
        lockInfo.approvalsRequired = approvalsRequired;
        lockInfo.approvalsReceived = 0;
        lockInfo.released = false;

        emit Locked(lockId, beneficiary, msg.value, 0, address(0), releaseTime, requiresKYC, approvalsRequired);
        return lockId;
    }

    /// @notice Locks ERC20 tokens
    /// @param tokenAddress Address of the ERC20 token
    /// @param amount Amount to lock
    /// @param beneficiary Address to receive tokens
    /// @param releaseTime Timestamp for release
    /// @param requiresKYC Whether KYC is required
    /// @param approvalsRequired Number of approvals needed
    function lockERC20(
        address tokenAddress,
        uint256 amount,
        address beneficiary,
        uint256 releaseTime,
        bool requiresKYC,
        uint256 approvalsRequired
    ) public whenNotPaused nonReentrant returns (uint256) {
        require(amount > 0, "No tokens sent");
        require(tokenAddress != address(0), "Invalid token address");
        require(beneficiary != address(0), "Invalid beneficiary");
        require(releaseTime >= block.timestamp + MIN_LOCK_PERIOD, "Release time too soon");
        require(approvalsRequired <= MAX_APPROVALS, "Too many approvals required");

        IERC20Upgradeable token = IERC20Upgradeable(tokenAddress);
        require(token.transferFrom(msg.sender, address(this), amount), "Token transfer failed");

        _lockIdCounter.increment();
        uint256 lockId = _lockIdCounter.current();

        LockInfo storage lockInfo = locks[lockId];
        lockInfo.beneficiary = beneficiary;
        lockInfo.amount = amount;
        lockInfo.tokenId = 0;
        lockInfo.tokenAddress = tokenAddress;
        lockInfo.releaseTime = releaseTime;
        lockInfo.requiresKYC = requiresKYC;
        lockInfo.approvalsRequired = approvalsRequired;
        lockInfo.approvalsReceived = 0;
        lockInfo.released = false;

        emit Locked(lockId, beneficiary, amount, 0, tokenAddress, releaseTime, requiresKYC, approvalsRequired);
        return lockId;
    }

    /// @notice Locks an NFT from Nexus.sol
    /// @param tokenId ID of the NFT to lock
    /// @param beneficiary Address to receive NFT
    /// @param releaseTime Timestamp for release
    /// @param requiresKYC Whether KYC is required
    /// @param approvalsRequired Number of approvals needed
    function lockNFT(
        uint256 tokenId,
        address beneficiary,
        uint256 releaseTime,
        bool requiresKYC,
        uint256 approvalsRequired
    ) public whenNotPaused nonReentrant returns (uint256) {
        require(nexusContract != address(0), "Nexus contract not set");
        require(beneficiary != address(0), "Invalid beneficiary");
        require(releaseTime >= block.timestamp + MIN_LOCK_PERIOD, "Release time too soon");
        require(approvalsRequired <= MAX_APPROVALS, "Too many approvals required");

        IERC721Upgradeable nexus = IERC721Upgradeable(nexusContract);
        require(nexus.ownerOf(tokenId) == msg.sender, "Not NFT owner");
        nexus.transferFrom(msg.sender, address(this), tokenId);

        _lockIdCounter.increment();
        uint256 lockId = _lockIdCounter.current();

        LockInfo storage lockInfo = locks[lockId];
        lockInfo.beneficiary = beneficiary;
        lockInfo.amount = 0;
        lockInfo.tokenId = tokenId;
        lockInfo.tokenAddress = nexusContract;
        lockInfo.releaseTime = releaseTime;
        lockInfo.requiresKYC = requiresKYC;
        lockInfo.approvalsRequired = approvalsRequired;
        lockInfo.approvalsReceived = 0;
        lockInfo.released = false;

        emit Locked(lockId, beneficiary, 0, tokenId, nexusContract, releaseTime, requiresKYC, approvalsRequired);
        return lockId;
    }

    // --- Unlocking Functions ---
    /// @notice Unlocks a lock if conditions are met
    /// @param lockId ID of the lock
    function unlock(uint256 lockId) public nonReentrant {
        LockInfo storage lockInfo = locks[lockId];
        require(!lockInfo.released, "Lock already released");
        require(msg.sender == lockInfo.beneficiary, "Not beneficiary");
        require(block.timestamp >= lockInfo.releaseTime, "Lock not yet releasable");
        require(!lockInfo.requiresKYC || verifyKYC(msg.sender), "KYC not verified");
        require(lockInfo.approvalsReceived >= lockInfo.approvalsRequired, "Insufficient approvals");

        lockInfo.released = true;

        if (lockInfo.tokenAddress == address(0)) {
            // Native Pi tokens
            (bool success, ) = lockInfo.beneficiary.call{value: lockInfo.amount}("");
            require(success, "Transfer failed");
        } else if (lockInfo.tokenId == 0) {
            // ERC20 tokens
            IERC20Upgradeable token = IERC20Upgradeable(lockInfo.tokenAddress);
            require(token.transfer(lockInfo.beneficiary, lockInfo.amount), "Token transfer failed");
        } else {
            // NFT
            IERC721Upgradeable nexus = IERC721Upgradeable(lockInfo.tokenAddress);
            nexus.transferFrom(address(this), lockInfo.beneficiary, lockInfo.tokenId);
        }

        emit Unlocked(lockId, lockInfo.beneficiary, lockInfo.amount, lockInfo.tokenId);
    }

    // --- Approval Functions ---
    /// @notice Approves a lock for release
    /// @param lockId ID of the lock
    function approveLock(uint256 lockId) public onlyRole(APPROVER_ROLE) {
        LockInfo storage lockInfo = locks[lockId];
        require(!lockInfo.released, "Lock already released");
        require(!lockInfo.approvedBy[msg.sender], "Already approved");
        require(lockInfo.approvalsRequired > 0, "No approvals required");

        lockInfo.approvedBy[msg.sender] = true;
        lockInfo.approvalsReceived += 1;

        emit ApprovalGiven(lockId, msg.sender);
    }

    // --- Batch Operations ---
    /// @notice Locks multiple native Pi token amounts
    /// @param beneficiaries Array of beneficiaries
    /// @param amounts Array of amounts
    /// @param releaseTimes Array of release times
    /// @param requiresKYCs Array of KYC requirements
    /// @param approvalsRequired Array of approval requirements
    function batchLock(
        address[] calldata beneficiaries,
        uint256[] calldata amounts,
        uint256[] calldata releaseTimes,
        bool[] calldata requiresKYCs,
        uint256[] calldata approvalsRequired
    ) public payable whenNotPaused nonReentrant returns (uint256[] memory) {
        require(beneficiaries.length == amounts.length, "Array length mismatch");
        require(beneficiaries.length == releaseTimes.length, "Array length mismatch");
        require(beneficiaries.length == requiresKYCs.length, "Array length mismatch");
        require(beneficiaries.length == approvalsRequired.length, "Array length mismatch");

        uint256 totalAmount = 0;
        for (uint256 i = 0; i < amounts.length; i++) {
            totalAmount += amounts[i];
        }
        require(msg.value >= totalAmount, "Insufficient funds sent");

        uint256[] memory lockIds = new uint256[](beneficiaries.length);
        for (uint256 i = 0; i < beneficiaries.length; i++) {
            lockIds[i] = lock(beneficiaries[i], releaseTimes[i], requiresKYCs[i], approvalsRequired[i]);
        }

        return lockIds;
    }

    // --- Admin Functions ---
    /// @notice Updates the Nexus contract address
    /// @param newNexusContract New Nexus contract address
    function updateNexusContract(address newNexusContract) public onlyRole(ADMIN_ROLE) {
        require(newNexusContract != address(0), "Invalid Nexus address");
        address oldNexus = nexusContract;
        nexusContract = newNexusContract;
        emit NexusContractUpdated(oldNexus, newNexusContract);
    }

    /// @notice Pauses the contract
    function pause() public onlyRole(ADMIN_ROLE) {
        _pause();
    }

    /// @notice Unpauses the contract
    function unpause() public onlyRole(ADMIN_ROLE) {
        _unpause();
    }

    // --- Pi Network Integration ---
    /// @notice Placeholder for Pi Network KYC verification
    /// @dev Implement with Pi Network's KYC API
    function verifyKYC(address user) public view returns (bool) {
        // Placeholder: Replace with actual Pi Network KYC API call
        return true;
    }

    // --- Fallback Function ---
    receive() external payable {
        // Allow receiving Pi tokens for locking
    }
}
