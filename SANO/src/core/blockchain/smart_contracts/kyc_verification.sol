// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract KYCVerification {
    address public admin;
    bool public paused;

    struct User {
        bool isVerified;
        string name;
        string email;
    }

    mapping(address => User) public users;
    uint256 public totalVerified;

    event UserVerified(address indexed user, uint256 timestamp);
    event UserRevoked(address indexed user, uint256 timestamp);
    event UserUpdated(address indexed user, string name, string email, uint256 timestamp);
    event ContractPaused(uint256 timestamp);
    event ContractUnpaused(uint256 timestamp);

    constructor() {
        admin = msg.sender;
        paused = false;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin is allowed");
        _;
    }

    modifier whenNotPaused() {
        require(!paused, "Contract is paused");
        _;
    }

    modifier whenPaused() {
        require(paused, "Contract is not paused");
        _;
    }

    function verifyUser (address user, string calldata name, string calldata email) external onlyAdmin whenNotPaused {
        require(!users[user].isVerified, "User  is already verified");
        users[user] = User(true, name, email);
        totalVerified++;
        emit UserVerified(user, block.timestamp);
    }

    function batchVerify(address[] calldata usersToVerify, string[] calldata names, string[] calldata emails) external onlyAdmin whenNotPaused {
        require(usersToVerify.length == names.length && names.length == emails.length, "Input arrays must have the same length");
        for (uint256 i = 0; i < usersToVerify.length; i++) {
            if (!users[usersToVerify[i]].isVerified) {
                users[usersToVerify[i]] = User(true, names[i], emails[i]);
                totalVerified++;
                emit UserVerified(usersToVerify[i], block.timestamp);
            }
        }
    }

    function revokeUser (address user) external onlyAdmin whenNotPaused {
        require(users[user].isVerified, "User  is not verified");
        users[user].isVerified = false;
        totalVerified--;
        emit UserRevoked(user, block.timestamp);
    }

    function batchRevoke(address[] calldata usersToRevoke) external onlyAdmin whenNotPaused {
        for (uint256 i = 0; i < usersToRevoke.length; i++) {
            if (users[usersToRevoke[i]].isVerified) {
                users[usersToRevoke[i]].isVerified = false;
                totalVerified--;
                emit UserRevoked(usersToRevoke[i], block.timestamp);
            }
        }
    }

    function isVerified(address user) external view returns (bool) {
        return users[user].isVerified;
    }

    function getUser Info(address user) external view returns (string memory name, string memory email, bool isVerified) {
        User memory userInfo = users[user];
        return (userInfo.name, userInfo.email, userInfo.isVerified);
    }

    function pauseContract() external onlyAdmin whenNotPaused {
        paused = true;
        emit ContractPaused(block.timestamp);
    }

    function unpauseContract() external onlyAdmin whenPaused {
        paused = false;
        emit ContractUnpaused(block.timestamp);
    }
}
