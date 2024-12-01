import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the module to test
from py_scripts.regression_analysis import (
    load_data,
    calculate_correlation_matrix)

class TestRegressionAnalysis(unittest.TestCase):
    @patch("pandas.read_csv")
    def test_load_data(self, mock_read_csv):
        """Test loading dataset from a CSV file."""
        mock_data = pd.DataFrame({
            "Population": [1000, 2000, 3000],
            "Year": [2000, 2001, 2002],
            "CO2_per_capita": [1.2, 1.4, 1.6]
        })
        mock_read_csv.return_value = mock_data

        df = load_data("mock_file.csv")
        mock_read_csv.assert_called_once_with("mock_file.csv")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(list(df.columns), ["Population", "Year", "CO2_per_capita"])

    def test_calculate_correlation_matrix(self):
        """Test correlation matrix calculation."""
        data = {
            "Population": [1000, 2000, 3000],
            "Year": [2000, 2001, 2002],
            "CO2_per_capita": [1.2, 1.4, 1.6]
        }
        df = pd.DataFrame(data)
        correlation_matrix = calculate_correlation_matrix(df)
        self.assertIsInstance(correlation_matrix, pd.DataFrame)
        self.assertIn("Population", correlation_matrix.columns)

if __name__ == "__main__":
    unittest.main()
