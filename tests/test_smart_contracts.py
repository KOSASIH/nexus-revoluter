import unittest
import json
import os
from smart_contracts import SmartContract, SmartContractManager, ExpiringSmartContract

class TestSmartContract(unittest.TestCase):
    def setUp(self):
        """Set up the SmartContractManager and a test contract for testing."""
        self.manager = SmartContractManager()
        self.contract_name = "TestContract"
        self.owner = "Alice"
        self.contract = self.manager.deploy_contract(self.contract_name, self.owner)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(f"{self.contract_name}.json"):
            os.remove(f"{self.contract_name}.json")

    def test_deploy_contract(self):
        """Test deploying a new smart contract."""
        self.assertIsInstance(self.contract, SmartContract, "The deployed contract should be an instance of SmartContract.")
        self.assertEqual(self.contract.contract_name, self.contract_name, "Contract name should match.")
        self.assertEqual(self.contract.owner, self.owner, "Contract owner should match.")

    def test_add_function(self):
        """Test adding a function to the smart contract."""
        def test_function(contract: SmartContract, value: str):
            contract.set_state("test_key", value)

        self.contract.add_function("test_function", test_function)
        self.assertIn("test_function", self.contract.functions, "Function should be added to the contract.")

    def test_call_function(self):
        """Test calling a function in the smart contract."""
        def set_value(contract: SmartContract, key: str, value: str):
            contract.set_state(key, value)

        self.contract.add_function("set_value", set_value, roles=[self.owner])
        self.contract.call_function("set_value", self.owner, "my_key", "my_value")

        self.assertEqual(self.contract.get_state("my_key"), "my_value", "State should be updated correctly.")

    def test_call_function_access_control(self):
        """Test access control for calling a function."""
        def set_value(contract: SmartContract, key: str, value: str):
            contract.set_state(key, value)

        self.contract.add_function("set_value", set_value, roles=["Bob"])  # Only Bob can call this function

        with self.assertRaises(PermissionError):
            self.contract.call_function("set_value", "Alice", "my_key", "my_value")

    def test_save_load_contract_state(self):
        """Test saving and loading contract state."""
        self.contract.set_state("my_key", "my_value")
        self.manager.save_contract_state(self.contract_name)

        # Create a new manager and load the contract state
        new_manager = SmartContractManager()
        new_manager.load_contract_state(self.contract_name)
        loaded_contract = new_manager.get_contract(self.contract_name)

        self.assertEqual(loaded_contract.get_state("my_key"), "my_value", "Loaded state should match saved state.")

    def test_expiring_contract(self):
        """Test the functionality of an expiring smart contract."""
        expiring_contract = ExpiringSmartContract("ExpiringContract", "Alice", expiration_time=5)

        self.assertFalse(expiring_contract.is_expired(), "Contract should not be expired immediately.")

        # Wait for the contract to expire
        import time
        time.sleep(6)

        self.assertTrue(expiring_contract.is_expired(), "Contract should be expired after waiting.")

    def test_event_logging(self):
        """Test event logging functionality."""
        def set_value(contract: SmartContract, key: str, value: str):
            contract.set_state(key, value)

        self.contract.add_function("set_value", set_value, roles=[self.owner])
        self.contract.call_function("set_value", self.owner, "event_key", "event_value")

        events = self.contract.get_events()
        self.assertIn("State updated: event_key = event_value", events, "Event should be logged correctly.")

    def test_batch_set_state(self):
        """Test batch state updates."""
        def batch_set_state(contract: SmartContract, updates: Dict[str, Any]):
            for key, value in updates.items():
                contract.set_state(key, value)

        self.contract.add_function("batch_set_state", batch_set_state, roles=[self.owner])
        updates = {"key1": "value1", "key2": "value2"}
        self.contract.call_function("batch_set_state", self.owner, updates)

        self.assertEqual(self.contract.get_state("key1"), "value1", "State for key1 should be updated correctly.")
        self.assertEqual(self.contract.get_state("key2"), "value2", "State for key2 should be updated correctly.")

if __name__ == "__main__":
    unittest.main()
