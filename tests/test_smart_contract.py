import unittest
from unittest.mock import patch, MagicMock
import json
import os
from smart_contract import SmartContract, SmartContractManager  # Assuming your classes are in a file named smart_contract.py

class TestSmartContract(unittest.TestCase):
    def setUp(self):
        """Set up a new SmartContract instance for testing."""
        self.contract = SmartContract("TestContract", "Alice")

    def test_initialization(self):
        """Test the initialization of the SmartContract."""
        self.assertEqual(self.contract.contract_name, "TestContract")
        self.assertEqual(self.contract.owner, "Alice")
        self.assertEqual(self.contract.state, {})
        self.assertEqual(self.contract.events, [])
        self.assertEqual(self.contract.functions, {})
        self.assertEqual(self.contract.access_control, {})

    def test_add_function(self):
        """Test adding a function to the SmartContract."""
        def dummy_function(contract, arg):
            return arg

        self.contract.add_function("dummy_function", dummy_function, roles=["Alice"])
        self.assertIn("dummy_function", self.contract.functions)
        self.assertIn("dummy_function", self.contract.access_control)

    def test_call_function_with_access(self):
        """Test calling a function with the correct access."""
        def set_value(contract, key, value):
            contract.set_state(key, value)

        self.contract.add_function("set_value", set_value, roles=["Alice"])
        result = self.contract.call_function("set_value", "Alice", "my_key", "my_value")
        self.assertIsNone(result)  # The function does not return anything
        self.assertEqual(self.contract.get_state("my_key"), "my_value")

    def test_call_function_without_access(self):
        """Test calling a function without the correct access."""
        def set_value(contract, key, value):
            contract.set_state(key, value)

        self.contract.add_function("set_value", set_value, roles=["Alice"])
        with self.assertRaises(PermissionError):
            self.contract.call_function("set_value", "Bob", "my_key", "my_value")

    def test_emit_event(self):
        """Test emitting an event."""
        self.contract.emit_event("Test event")
        self.assertIn("Test event", self.contract.get_events())

    def test_get_state(self):
        """Test getting a state value."""
        self.contract.set_state("my_key", "my_value")
        self.assertEqual(self.contract.get_state("my_key"), "my_value")
        self.assertIsNone(self.contract.get_state("non_existent_key"))

    def test_to_dict(self):
        """Test converting the contract to a dictionary."""
        self.contract.set_state("my_key", "my_value")
        self.contract.emit_event("Test event")
        expected_dict = {
            "contract_name": "TestContract",
            "owner": "Alice",
            "state": {"my_key": "my_value"},
            "events": ["Test event"]
        }
        self.assertEqual(self.contract.to_dict(), expected_dict)

class TestSmartContractManager(unittest.TestCase):
    def setUp(self):
        """Set up a new SmartContractManager instance for testing."""
        self.manager = SmartContractManager()

    def test_deploy_contract(self):
        """Test deploying a new smart contract."""
        contract = self.manager.deploy_contract("MyContract", "Alice")
        self.assertIn("MyContract", self.manager.contracts)
        self.assertEqual(self.manager.contracts["MyContract"], contract)

    def test_deploy_existing_contract(self):
        """Test deploying an existing smart contract."""
        self.manager.deploy_contract("MyContract", "Alice")
        with self.assertRaises(ValueError):
            self.manager.deploy_contract("MyContract", "Bob")

    def test_get_contract(self):
        """Test retrieving a smart contract."""
        contract = self.manager.deploy_contract("MyContract", "Alice")
        retrieved_contract = self.manager.get_contract("MyContract")
        self.assertEqual(contract, retrieved_contract)

    def test_get_non_existent_contract(self):
        """Test retrieving a non-existent smart contract."""
        with self.assertRaises(ValueError):
            self.manager.get_contract("NonExistentContract")

    @patch("builtins.open", new_callable=MagicMock)
    def test_save_contract_state(self, mock_open):
        """Test saving the contract state to a file."""
        contract = self.manager.deploy_contract("MyContract", "Alice")
        contract.set_state("my_key", "my_value")
        contract.emit_event("Test event")
        self.manager.save_contract_state("MyContract")

        # Check that the file was opened and written to
        mock_open.assert_called_once_with("MyContract.json", "w")
        handle = mock_open()
        handle.write.assert_called_once()

    @patch("builtins.open", new_callable=MagicMock)
    def test_load_contract_state(self, mock_open):
        """Test loading the contract state from a file."""
        contract = self.manager.deploy_contract("MyContract", "Alice")
        contract.set_state("my_key", "my_value")
        contract.emit_event("Test event")

        # Simulate saving the contract state
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(contract.to_dict())
        self.manager.load_contract_state("MyContract")

        loaded_contract = self.manager.get_contract("MyContract")
        self.assertEqual(loaded_contract.get_state("my_key"), "my_value")
        self.assertIn("Test event", loaded_contract.get_events())

    @patch("builtins.open", new_callable=MagicMock)
    def test_load_non_existent_contract(self, mock_open):
        """Test loading a non-existent contract."""
        mock_open.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            self.manager.load_contract_state("NonExistentContract")

if __name__ == '__main__':
    unittest.main()
