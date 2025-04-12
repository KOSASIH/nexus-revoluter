// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract IdentityVault is Ownable {
    mapping(address => bytes32) private identityProofs;

    event IdentityStored(address indexed user, bytes32 proof);
    event IdentityUpdated(address indexed user, bytes32 oldProof, bytes32 newProof);
    event IdentityRemoved(address indexed user, bytes32 proof);

    modifier validProof(bytes32 proof) {
        require(proof != bytes32(0), "Invalid proof: cannot be zero");
        _;
    }

    function storeIdentityProof(address user, bytes32 proof) external onlyOwner validProof(proof) {
        bytes32 oldProof = identityProofs[user];
        identityProofs[user] = proof;
        
        if (oldProof == bytes32(0)) {
            emit IdentityStored(user, proof);
        } else {
            emit IdentityUpdated(user, oldProof, proof);
        }
    }

    function removeIdentityProof(address user) external onlyOwner {
        bytes32 proof = identityProofs[user];
        require(proof != bytes32(0), "No proof found for this user");
        
        delete identityProofs[user];
        emit IdentityRemoved(user, proof);
    }

    function getIdentityProof(address user) external view returns (bytes32) {
        return identityProofs[user];
    }

    function storeIdentityProofBatch(address[] calldata users, bytes32[] calldata proofs) external onlyOwner {
        require(users.length == proofs.length, "Users and proofs length mismatch");
        
        for (uint256 i = 0; i < users.length; i++) {
            storeIdentityProof(users[i], proofs[i]);
        }
    }
}
