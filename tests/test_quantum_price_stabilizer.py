import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import pandas as pd
from quantum_price_stabilizer import QuantumPriceStabilizer

class TestQuantumPriceStabilizer(unittest.TestCase):

    @patch('quantum_price_stabilizer.PiCoinSmartContract')
    @patch('quantum_price_stabilizer.fetch_global_economic_data')
    @patch('quantum_price_stabilizer.QuantumPredictor')
    def setUp(self, MockQuantumPredictor, MockFetchGlobalEconomicData, MockPiCoinSmartContract):
        # Mock the smart contract
        self.mock_smart_contract = MockPiCoinSmartContract.return_value
        self.mock_smart_contract.get_current_supply.return_value = 100_000_000_000  # Set initial supply to total supply

        # Mock the quantum predictor
        self.mock_quantum_predictor = MockQuantumPredictor.return_value

        # Mock the economic data
        self.mock_economic_data = pd.DataFrame({
            'inflation_rate': [2.5, 3.0, 2.8],
            'interest_rate': [1.5, 1.75, 1.6],
            'demand': [100, 150, 120],
            'price': [314000, 314200, 314100]
        })
        MockFetchGlobalEconomicData.return_value = self.mock_economic_data

        # Initialize the QuantumPriceStabilizer
        self.stabilizer = QuantumPriceStabilizer()

    def test_initialization(self):
        self.assertIsNotNone(self.stabilizer.quantum_predictor)
        self.assertIsNotNone(self.stabilizer.smart_contract)
        self.assertEqual(self.stabilizer.current_supply, 100_000_000_000)
        self.assertEqual(self.stabilizer.target_value, 314159.00)

    def test_analyze_market(self):
        economic_data = self.stabilizer.analyze_market()
        pd.testing.assert_frame_equal(economic_data, self.mock_economic_data)

    @patch('quantum_price_stabilizer.StandardScaler')
    def test_predict_price_fluctuations(self, MockStandardScaler):
        mock_scaler = MockStandardScaler.return_value
        mock_scaler.fit_transform.return_value = np.array([[0, 0], [1, 1], [0.5, 0.5]])
        
        # Mock the model's predict method
        self.stabilizer.model.predict = MagicMock(return_value=np.array([314200]))

        predicted_fluctuations = self.stabilizer.predict_price_fluctuations(self.mock_economic_data)
        self.assertEqual(predicted_fluctuations, 314200)

    def test_adjust_supply_burn(self):
        self.stabilizer.current_supply = 100_000_000_000  # Set current supply to total supply
        self.stabilizer.adjust_supply(314300)  # Above target value
        self.mock_smart_contract.burn_tokens.assert_called_once_with(141.0)  # 314300 - 314159

    def test_adjust_supply_mint(self):
        self.stabilizer.current_supply = 100_000_000_000  # Set current supply to total supply
        self.stabilizer.adjust_supply(314000)  # Below target value
        self.mock_smart_contract.mint_tokens.assert_called_once_with(159.0)  # 314159 - 314000

    @patch('quantum_price_stabilizer.time.sleep', return_value=None)  # Mock sleep to avoid delays
    def test_run(self, mock_sleep):
        with patch.object(self.stabilizer, 'analyze_market', return_value=self.mock_economic_data), \
             patch.object(self.stabilizer, 'predict_price_fluctuations', return_value=314200), \
             patch.object(self.stabilizer, 'adjust_supply') as mock_adjust_supply:

            # Run the stabilizer for a single iteration
            self.stabilizer.run()
            mock_adjust_supply.assert_called_once_with(314200)

if __name__ == '__main__':
    unittest.main()
