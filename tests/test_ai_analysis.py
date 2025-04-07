import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from ai_analysis import TransactionAnalyzer

class TestTransactionAnalyzer(unittest.TestCase):
    def setUp(self):
        """Set up a new TransactionAnalyzer instance for testing."""
        self.analyzer = TransactionAnalyzer()
        self.mock_data = pd.DataFrame({
            'transaction_id': range(1, 101),
            'amount': np.random.normal(100, 20, 100).tolist(),
            'transaction_type': np.random.choice(['deposit', 'withdrawal'], 100),
            'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H')
        })

        # Introduce some anomalies
        self.mock_data.loc[::10, 'amount'] = np.random.normal(500, 50, 10)  # Outliers

    def test_ingest_data(self):
        """Test data ingestion."""
        self.analyzer.ingest_data(self.mock_data)
        self.assertEqual(len(self.analyzer.transaction_data), 100)

    def test_preprocess_data(self):
        """Test data preprocessing."""
        self.analyzer.ingest_data(self.mock_data)
        processed_data = self.analyzer.preprocess_data()
        self.assertEqual(processed_data.shape[1], 3)  # Check number of features

    def test_train_model(self):
        """Test model training."""
        self.analyzer.ingest_data(self.mock_data)
        self.analyzer.train_model()
        self.assertIsNotNone(self.analyzer.model)

    def test_detect_anomalies(self):
        """Test anomaly detection."""
        self.analyzer.ingest_data(self.mock_data)
        self.analyzer.train_model()
        anomalies = self.analyzer.detect_anomalies()
        self.assertGreater(len(anomalies), 0)  # Expect some anomalies to be detected

    def test_generate_report(self):
        """Test report generation."""
        self.analyzer.ingest_data(self.mock_data)
        self.analyzer.train_model()
        anomalies = self.analyzer.detect_anomalies()
        self.analyzer.generate_report(anomalies)
        report = pd.read_csv('anomaly_report.csv')
        self.assertEqual(len(report), len(anomalies))  # Check report length

    @patch('ai_analysis.plt.savefig')
    @patch('ai_analysis.plt.show')
    def test_visualize_anomalies(self, mock_show, mock_savefig):
        """Test anomaly visualization."""
        self.analyzer.ingest_data(self.mock_data)
        self.analyzer.train_model()
        anomalies = self.analyzer.detect_anomalies()
        self.analyzer.visualize_anomalies(anomalies)
        mock_savefig.assert_called_once_with('anomaly_visualization.png')
        mock_show.assert_called_once()

    @patch('ai_analysis.GridSearchCV')
    def test_tune_hyperparameters(self, mock_grid_search):
        """Test hyperparameter tuning."""
        self.analyzer.ingest_data(self.mock_data)
        self.analyzer.train_model()
        self.analyzer.tune_hyperparameters({'n_estimators': [50, 100]})
        self.assertIsNotNone(self.analyzer.model)

    @patch('ai_analysis.joblib.dump')
    def test_save_model(self, mock_dump):
        """Test model saving."""
        self.analyzer.ingest_data(self.mock_data)
        self.analyzer.train_model()
        self.analyzer.save_model('test_model.pkl')
        mock_dump.assert_called_once()

    @patch('ai_analysis.joblib.load')
    def test_load_model(self, mock_load):
        """Test model loading."""
        self.analyzer.load_model('test_model.pkl')
        mock_load.assert_called_once()

    @patch('ai_analysis.smtplib.SMTP')
    def test_send_alert(self, mock_smtp):
        """Test sending alert email."""
        self.analyzer.ingest_data(self.mock_data)
        self.analyzer.train_model()
        anomalies = self.analyzer.detect_anomalies()
        self.analyzer.send_alert(anomalies)
        mock_smtp.assert_called_once()  # Check if SMTP was called

if __name__ == "__main__":
    unittest.main()
