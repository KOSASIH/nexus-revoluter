// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SyncVerifier {
    struct SyncRecord {
        string id;
        string content;
        uint256 timestamp;
    }
    
    address public admin;
    mapping(address => bool) public authorizedAdmins;
    mapping(string => SyncRecord) public records;
    
    event SyncRecorded(string indexed id, string content, uint256 timestamp);
    event AdminAdded(address indexed newAdmin);
    event AdminRemoved(address indexed removedAdmin);
    
    constructor() {
        admin = msg.sender;
        authorizedAdmins[admin] = true; // Grant admin rights to the contract deployer
    }
    
    modifier onlyAdmin() {
        require(authorizedAdmins[msg.sender], "Only admin allowed");
        _;
    }
    
    modifier recordExists(string memory id) {
        require(bytes(records[id].id).length != 0, "Record does not exist");
        _;
    }
    
    modifier recordDoesNotExist(string memory id) {
        require(bytes(records[id].id).length == 0, "Record already exists");
        _;
    }
    
    function addAdmin(address newAdmin) external onlyAdmin {
        require(newAdmin != address(0), "Invalid address");
        authorizedAdmins[newAdmin] = true;
        emit AdminAdded(newAdmin);
    }
    
    function removeAdmin(address adminToRemove) external onlyAdmin {
        require(adminToRemove != address(0), "Invalid address");
        require(adminToRemove != admin, "Cannot remove contract deployer");
        authorizedAdmins[adminToRemove] = false;
        emit AdminRemoved(adminToRemove);
    }
    
    function recordSync(string memory id, string memory content, uint256 timestamp) 
        external 
        onlyAdmin 
        recordDoesNotExist(id) 
    {
        records[id] = SyncRecord(id, content, timestamp);
        emit SyncRecorded(id, content, timestamp);
    }
    
    function recordSyncBatch(string[] memory ids, string[] memory contents, uint256[] memory timestamps) 
        external 
        onlyAdmin 
    {
        require(ids.length == contents.length && contents.length == timestamps.length, "Array lengths must match");
        
        for (uint256 i = 0; i < ids.length; i++) {
            recordSync(ids[i], contents[i], timestamps[i]);
        }
    }
    
    function getSyncRecord(string memory id) 
        external 
        view 
        returns (SyncRecord memory) 
    {
        return records[id];
    }
    
    function getAllRecords() external view returns (SyncRecord[] memory) {
        uint256 recordCount = 0;
        for (uint256 i = 0; i < 2**256 - 1; i++) { // Arbitrary large number for demonstration
            if (bytes(records[uint2str(i)].id).length != 0) {
                recordCount++;
            }
        }
        
        SyncRecord[] memory allRecords = new SyncRecord[](recordCount);
        uint256 index = 0;
        for (uint256 i = 0; i < 2**256 - 1; i++) {
            if (bytes(records[uint2str(i)].id).length != 0) {
                allRecords[index] = records[uint2str(i)];
                index++;
            }
        }
        
        return allRecords;
    }
    
    function uint2str(uint256 _i) internal pure returns (string memory str) {
        if (_i == 0) {
            return "0";
        }
        uint256 j = _i;
        uint256 len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint256 k = len;
        while (_i != 0) {
            bstr[--k] = bytes1(uint8(48 + _i % 10));
            _i /= 10;
        }
        return string(bstr);
    }
}
