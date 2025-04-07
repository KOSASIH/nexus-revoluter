import unittest
from identity import DecentralizedIdentity

class TestDecentralizedIdentity(unittest.TestCase):
    def setUp(self):
        """Set up a new DecentralizedIdentity instance for testing."""
        self.did_system = DecentralizedIdentity()
        self.user_id = "user123"
        self.credential_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "role": "admin"
        }
        self.identity = self.did_system.create_identity(self.user_id)

    def test_create_identity(self):
        """Test identity creation."""
        self.assertIn(self.user_id, self.did_system.identities)
        self.assertEqual(self.did_system.identities[self.user_id]["identity"]["user_id"], self.user_id)

    def test_issue_credential(self):
        """Test issuing a credential."""
        credential = self.did_system.issue_credential(self.user_id, self.credential_data)
        self.assertIn(credential["credential_id"], self.did_system.credentials)
        self.assertEqual(self.did_system.credentials[credential["credential_id"]]["data"], self.credential_data)

    def test_verify_credential(self):
        """Test verifying an issued credential."""
        credential = self.did_system.issue_credential(self.user_id, self.credential_data)
        is_verified = self.did_system.verify_credential(credential["credential_id"])
        self.assertTrue(is_verified)

    def test_revoke_credential(self):
        """Test revoking an issued credential."""
        credential = self.did_system.issue_credential(self.user_id, self.credential_data)
        self.assertTrue(self.did_system.revoke_credential(self.user_id, credential["credential_id"]))
        self.assertIn(credential["credential_id"], self.did_system.revocation_list)

    def test_verify_revoked_credential(self):
        """Test verifying a revoked credential."""
        credential = self.did_system.issue_credential(self.user_id, self.credential_data)
        self.did_system.revoke_credential(self.user_id, credential["credential_id"])
        is_verified = self.did_system.verify_credential(credential["credential_id"])
        self.assertFalse(is_verified)

    def test_present_credential(self):
        """Test presenting a credential."""
        credential = self.did_system.issue_credential(self.user_id, self.credential_data)
        presented_credential = self.did_system.present_credential(self.user_id, credential["credential_id"])
        self.assertEqual(presented_credential["credential_id"], credential["credential_id"])
        self.assertEqual(presented_credential["data"], self.credential_data)

    def test_present_revoked_credential(self):
        """Test presenting a revoked credential."""
        credential = self.did_system.issue_credential(self.user_id, self.credential_data)
        self.did_system.revoke_credential(self.user_id, credential["credential_id"])
        with self.assertRaises(Exception) as context:
            self.did_system.present_credential(self.user_id, credential["credential_id"])
        self.assertTrue("Credential not found or has been revoked." in str(context.exception))

    def test_verify_nonexistent_credential(self):
        """Test verifying a nonexistent credential."""
        with self.assertRaises(Exception) as context:
            self.did_system.verify_credential("nonexistent_id")
        self.assertTrue("Credential does not exist." in str(context.exception))

    def test_revoke_nonexistent_credential(self):
        """Test revoking a nonexistent credential."""
        with self.assertRaises(Exception) as context:
            self.did_system.revoke_credential(self.user_id, "nonexistent_id")
        self.assertTrue("Identity does not exist." in str(context.exception))

if __name__ == "__main__":
    unittest.main()
