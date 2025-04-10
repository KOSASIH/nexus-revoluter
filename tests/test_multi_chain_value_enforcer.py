import unittest
from unittest.mock import patch, MagicMock
from multi_chain_value_enforcer import MultiChainValueEnforcer

class TestMultiChainValueEnforcer(unittest.TestCase):

    @patch('multi_chain_value_enforcer.CrossChainInteroperability')
    @patch('multi_chain_value_enforcer.DAO')
    @patch('multi_chain_value_enforcer.SmartContractExecutor')
    def setUp(self, mock_smart_contract_executor, mock_dao, mock_cross_chain_interoperability):
        # Mock the managers
        self.mock_cross_chain_interoperability = mock_cross_chain_interoperability.return_value
        self.mock_dao = mock_dao.return_value
        self.mock_smart_contract_executor = mock_smart_contract_executor.return_value

        # Initialize the MultiChainValueEnforcer class
        self.value_enforcer = MultiChainValueEnforcer()

    def test_enforce_value_compliance(self):
        # Mock connected chains and their values
        self.mock_cross_chain_interoperability.get_connected_chains.return_value = ['Ethereum', 'BSC']
        self.mock_cross_chain_interoperability.get_chain_value.side_effect = [314159.00, 300000.00]

        # Call enforce_value
        self.value_enforcer.enforce_value()

        # Check that enforce_compliance was called for the non-compliant chain
        self.mock_cross_chain_interoperability.atomic_swap.assert_called_once_with('BSC', self.value_enforcer.target_value)

    def test_enforce_value_no_compliance_needed(self):
        # Mock connected chains and their values
        self.mock_cross_chain_interoperability.get_connected_chains.return_value = ['Ethereum']
        self.mock_cross_chain_interoperability.get_chain_value.return_value = 314159.00

        # Call enforce_value
        self.value_enforcer.enforce_value()

        # Check that atomic_swap was not called
        self.mock_cross_chain_interoperability.atomic_swap.assert_not_called()

    def test_check_compliance(self):
        # Mock the current value
        self.mock_cross_chain_interoperability.get_chain_value.return_value = 314159.00

        # Check compliance
        is_compliant = self.value_enforcer.check_compliance('Ethereum')
        self.assertTrue(is_compliant)

        # Mock a non-compliant value
        self.mock_cross_chain_interoperability.get_chain_value.return_value = 300000.00
        is_compliant = self.value_enforcer.check_compliance('Ethereum')
        self.assertFalse(is_compliant)

    def test_enforce_compliance(self):
        # Mock the atomic swap and compliance check
        self.mock_cross_chain_interoperability.get_chain_value.return_value = 300000.00
        self.mock_cross_chain_interoperability.atomic_swap = MagicMock()
        self.value_enforcer.check_compliance = MagicMock(return_value=False)

        # Call enforce_compliance
        self.value_enforcer.enforce_compliance('BSC')

        # Check that atomic_swap was called
        self.mock_cross_chain_interoperability.atomic_swap.assert_called_once_with('BSC', self.value_enforcer.target_value)

        # Check that DAO enforcement was invoked
        self.mock_dao.invoke_enforcement.assert_called_once_with('BSC')

if __name__ == '__main__':
    unittest.main()
