import unittest
from unittest.mock import patch, MagicMock
from reputation_enforcement import ReputationEnforcement

class TestReputationEnforcement(unittest.TestCase):

    @patch('reputation_enforcement.ComplianceChecker')
    @patch('reputation_enforcement.RewardsManager')
    @patch('reputation_enforcement.GovernanceManager')
    def setUp(self, mock_governance_manager, mock_rewards_manager, mock_compliance_checker):
        # Mock the managers
        self.mock_compliance_checker = mock_compliance_checker.return_value
        self.mock_rewards_manager = mock_rewards_manager.return_value
        self.mock_governance_manager = mock_governance_manager.return_value

        # Initialize the ReputationEnforcement class
        self.reputation_enforcer = ReputationEnforcement()

    def test_evaluate_partners_compliant(self):
        # Mock compliance score for a compliant partner
        self.mock_compliance_checker.check_compliance.return_value = 1.0

        # Example partner
        partner = {'id': 'partner1'}

        # Call evaluate_partners
        self.reputation_enforcer.evaluate_partners([partner])

        # Check that rewards were awarded
        self.mock_rewards_manager.award_staking_rewards.assert_called_once_with(partner['id'])

    def test_evaluate_partners_partially_compliant(self):
        # Mock compliance score for a partially compliant partner
        self.mock_compliance_checker.check_compliance.return_value = 0.5

        # Example partner
        partner = {'id': 'partner2'}

        # Call evaluate_partners
        self.reputation_enforcer.evaluate_partners([partner])

        # Check that no rewards or penalties were applied
        self.mock_rewards_manager.award_staking_rewards.assert_not_called()

    def test_evaluate_partners_non_compliant(self):
        # Mock compliance score for a non-compliant partner
        self.mock_compliance_checker.check_compliance.return_value = 0.0

        # Example partner
        partner = {'id': 'partner3'}

        # Call evaluate_partners
        self.reputation_enforcer.evaluate_partners([partner])

        # Check that penalties were applied
        self.mock_governance_manager.reduce_api_access.assert_called_once_with(partner['id'])

    def test_update_reputation_compliant(self):
        # Mock a compliant partner
        partner = {'id': 'partner1'}
        compliance_score = 1.0

        # Call update_reputation
        self.reputation_enforcer.update_reputation(partner, compliance_score)

        # Check that rewards were awarded
        self.mock_rewards_manager.award_staking_rewards.assert_called_once_with(partner['id'])

    def test_update_reputation_non_compliant(self):
        # Mock a non-compliant partner
        partner = {'id': 'partner2'}
        compliance_score = 0.0

        # Call update_reputation
        self.reputation_enforcer.update_reputation(partner, compliance_score)

        # Check that penalties were applied
        self.mock_governance_manager.reduce_api_access.assert_called_once_with(partner['id'])

if __name__ == '__main__':
    unittest.main()
