import unittest
import numpy as np
from qiskit import Aer
from quantum_predictor import QuantumPredictor  # Assuming the class is in quantum_predictor.py

class TestQuantumPredictor(unittest.TestCase):
    def setUp(self):
        """Set up the QuantumPredictor instance for testing."""
        self.predictor = QuantumPredictor()
        self.metrics = [0.1, 0.5, 0.9, 1.2]  # Example latency metrics

    def test_preprocess_data(self):
        """Test the data preprocessing method."""
        processed_data = self.predictor.preprocess_data(self.metrics)
        self.assertEqual(processed_data.shape, (4, 1), "Processed data shape is incorrect.")
        self.assertTrue(np.all(processed_data >= 0) and np.all(processed_data <= 1), "Data not scaled properly.")

    def test_create_quantum_circuit(self):
        """Test the quantum circuit creation method."""
        num_qubits = len(self.metrics)
        circuit = self.predictor.create_quantum_circuit(num_qubits)
        self.assertEqual(circuit.num_qubits, num_qubits, "Quantum circuit qubit count is incorrect.")
        self.assertEqual(circuit.num_clbits, num_qubits, "Quantum circuit classical bit count is incorrect.")

    def test_predict_issue_high_latency(self):
        """Test prediction of high latency issue."""
        # Simulate high latency metrics
        high_latency_metrics = [1.5, 1.6, 1.7, 1.8]
        prediction = self.predictor.predict_issue(high_latency_metrics)
        self.assertEqual(prediction['issue'], "high_latency", "Prediction for high latency failed.")
        self.assertGreater(prediction['confidence'], 0.7, "Confidence level for high latency is too low.")

    def test_predict_issue_no_issue(self):
        """Test prediction when no issue is detected."""
        low_latency_metrics = [0.1, 0.2, 0.3, 0.4]
        prediction = self.predictor.predict_issue(low_latency_metrics)
        self.assertIsNone(prediction['issue'], "Prediction should indicate no issue.")
        self.assertLess(prediction['confidence'], 0.7, "Confidence level should be low when no issue is present.")

    def test_recommend_fix_high_latency(self):
        """Test the recommendation for high latency issue."""
        fix = self.predictor.recommend_fix("high_latency")
        self.assertEqual(fix['action'], "redistribute_nodes", "Fix action for high latency is incorrect.")
        self.assertEqual(fix['priority'], "high", "Priority for high latency fix is incorrect.")

    def test_recommend_fix_no_issue(self):
        """Test the recommendation when no issue is detected."""
        fix = self.predictor.recommend_fix(None)
        self.assertEqual(fix['action'], "monitor", "Fix action when no issue should be 'monitor'.")
        self.assertEqual(fix['priority'], "low", "Priority when no issue should be low.")

    def test_visualize_prediction(self):
        """Test the visualization method (this will not be assertable)."""
        prediction = self.predictor.predict_issue(self.metrics)
        try:
            self.predictor.visualize_prediction(prediction)
        except Exception as e:
            self.fail(f"Visualization raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
