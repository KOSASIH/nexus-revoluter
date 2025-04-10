import unittest
from unittest.mock import patch
from dynamic_fee_structure import DynamicFeeStructure

class TestDynamicFeeStructure(unittest.TestCase):
    def setUp(self):
        """Set up a new DynamicFeeStructure instance for testing."""
        self.fee_structure = DynamicFeeStructure()

    @patch('random.uniform')
    @patch('random.randint')
    def test_calculate_fee_high_priority(self, mock_randint, mock_uniform):
        """Test fee calculation for high priority transactions."""
        # Simulate network conditions
        mock_uniform.side_effect = [50, 5]  # congestion, average_transaction_time
        mock_randint.return_value = 500  # transaction_volume

        fee = self.fee_structure.calculate_fee("high")
        expected_fee = self.fee_structure.base_fee * 1.5 * 1.5 * 1.0  # congestion factor 1.5, volume factor 1.0
        self.assertAlmostEqual(fee, expected_fee)

    @patch('random.uniform')
    @patch('random.randint')
    def test_calculate_fee_low_priority(self, mock_randint, mock_uniform):
        """Test fee calculation for low priority transactions."""
        # Simulate network conditions
        mock_uniform.side_effect = [80, 3]  # congestion, average_transaction_time
        mock_randint.return_value = 300  # transaction_volume

        fee = self.fee_structure.calculate_fee("low")
        expected_fee = self.fee_structure.base_fee * 0.5 * 2.0 * 1.0  # congestion factor 2.0, volume factor 1.0
        self.assertAlmostEqual(fee, expected_fee)

    @patch('random.uniform')
    @patch('random.randint')
    def test_calculate_fee_medium_priority(self, mock_randint, mock_uniform):
        """Test fee calculation for medium priority transactions."""
        # Simulate network conditions
        mock_uniform.side_effect = [20, 2]  # congestion, average_transaction_time
        mock_randint.return_value = 200  # transaction_volume

        fee = self.fee_structure.calculate_fee("medium")
        expected_fee = self.fee_structure.base_fee * 1.0 * 1.0 * 1.0  # congestion factor 1.0, volume factor 1.0
        self.assertAlmostEqual(fee, expected_fee)

    @patch('random.uniform')
    @patch('random.randint')
    def test_calculate_congestion_factor(self, mock_randint, mock_uniform):
        """Test the calculation of congestion factor."""
        self.fee_structure.network_conditions["congestion"] = 75
        congestion_factor = self.fee_structure.calculate_congestion_factor()
        self.assertEqual(congestion_factor, 2.0)

        self.fee_structure.network_conditions["congestion"] = 50
        congestion_factor = self.fee_structure.calculate_congestion_factor()
        self.assertEqual(congestion_factor, 1.5)

        self.fee_structure.network_conditions["congestion"] = 10
        congestion_factor = self.fee_structure.calculate_congestion_factor()
        self.assertEqual(congestion_factor, 1.0)

    @patch('random.uniform')
    @patch('random.randint')
    def test_calculate_volume_factor(self, mock_randint, mock_uniform):
        """Test the calculation of volume factor."""
        self.fee_structure.network_conditions["transaction_volume"] = 900
        volume_factor = self.fee_structure.calculate_volume_factor()
        self.assertEqual(volume_factor, 1.5)

        self.fee_structure.network_conditions["transaction_volume"] = 500
        volume_factor = self.fee_structure.calculate_volume_factor()
        self.assertEqual(volume_factor, 1.2)

        self.fee_structure.network_conditions["transaction_volume"] = 100
        volume_factor = self.fee_structure.calculate_volume_factor()
        self.assertEqual(volume_factor, 1.0)

if __name__ == '__main__':
    unittest.main()
