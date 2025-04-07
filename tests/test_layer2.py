import unittest
from unittest.mock import patch, MagicMock
from layer2 import PaymentChannel

class TestPaymentChannel(unittest.TestCase):
    def setUp(self):
        """Set up a new PaymentChannel instance for testing."""
        self.channel = PaymentChannel("Alice", "Bob", 100.0)

    def test_channel_creation(self):
        """Test the creation of a payment channel."""
        self.assertEqual(self.channel.party_a, "Alice")
        self.assertEqual(self.channel.party_b, "Bob")
        self.assertEqual(self.channel.capacity, 100.0)
        self.assertTrue(self.channel.is_open)

    def test_fund_channel(self):
        """Test funding the payment channel."""
        self.channel.fund_channel(50.0)
        self.assertEqual(self.channel.balance_a, 150.0)

    def test_fund_channel_exceeds_capacity(self):
        """Test funding the channel with an amount that exceeds capacity."""
        with self.assertRaises(ValueError) as context:
            self.channel.fund_channel(200.0)
        self.assertTrue("Amount exceeds channel capacity." in str(context.exception))

    def test_make_payment(self):
        """Test making a payment through the channel."""
        self.channel.make_payment(20.0, "Alice")
        self.assertEqual(self.channel.balance_a, 80.0)
        self.assertEqual(self.channel.balance_b, 20.0)

    def test_make_payment_insufficient_balance(self):
        """Test making a payment with insufficient balance."""
        with self.assertRaises(ValueError) as context:
            self.channel.make_payment(200.0, "Alice")
        self.assertTrue("Insufficient balance for payment." in str(context.exception))

    def test_make_payment_invalid_party(self):
        """Test making a payment from an invalid party."""
        with self.assertRaises(ValueError) as context:
            self.channel.make_payment(10.0, "Charlie")
        self.assertTrue("Invalid party." in str(context.exception))

    def test_close_channel(self):
        """Test closing the payment channel."""
        final_settlement = self.channel.close_channel()
        self.assertFalse(self.channel.is_open)
        self.assertEqual(final_settlement["final_balance_a"], 100.0)
        self.assertEqual(final_settlement["final_balance_b"], 20.0)

    @patch('layer2.time.sleep', return_value=None)  # Mock sleep to speed up tests
    def test_settle_on_chain(self, mock_sleep):
        """Test settling the channel on-chain."""
        final_settlement = self.channel.settle_on_chain()
        self.assertEqual(final_settlement["channel_id"], self.channel.channel_id)
        self.assertEqual(final_settlement["final_balance_a"], 100.0)
        self.assertEqual(final_settlement["final_balance_b"], 20.0)

    @patch('layer2.time.sleep', return_value=None)  # Mock sleep to speed up tests
    def test_dispute_resolution(self, mock_sleep):
        """Test dispute resolution."""
        self.channel.dispute_resolution(timeout=1)
        self.assertFalse(self.channel.is_open)  # Ensure the channel is closed after timeout

if __name__ == "__main__":
    unittest.main()
