import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../py_scripts")))
from regression_analysis import (
    load_data,
    calculate_correlation_matrix,
    multivariate_regression,
    polynomial_regression,
)


class TestRegressionAnalysis(unittest.TestCase):

    @patch("pandas.read_csv")
    def test_load_data(self, mock_read_csv):
        """Test loading dataset from a CSV file."""
        mock_data = pd.DataFrame({
            'Population': [1000, 2000, 3000],
            'Year': [2000, 2001, 2002],
            'CO2_per_capita': [1.2, 1.4, 1.6]
        })
        mock_read_csv.return_value = mock_data
        
        df = load_data("mock_file.csv")
        mock_read_csv.assert_called_once_with("mock_file.csv")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(list(df.columns), ['Population', 'Year', 'CO2_per_capita'])

    def test_calculate_correlation_matrix(self):
        """Test correlation matrix calculation."""
        data = {
            'Population': [1000, 2000, 3000],
            'Year': [2000, 2001, 2002],
            'CO2_per_capita': [1.2, 1.4, 1.6]
        }
        df = pd.DataFrame(data)
        correlation_matrix = calculate_correlation_matrix(df)
        self.assertIsInstance(correlation_matrix, pd.DataFrame)
        self.assertTrue('Population' in correlation_matrix.columns)

    @patch("regression_analysis.train_test_split")
    @patch("regression_analysis.LinearRegression")
    def test_multivariate_regression(self, mock_linear_regression, mock_train_test_split):
        """Test multivariate regression."""
        mock_data = pd.DataFrame({
            'Population': [1000, 2000, 3000],
            'Year': [2000, 2001, 2002],
            'CO2_per_capita': [1.2, 1.4, 1.6]
        })
        mock_model = MagicMock()
        mock_model.predict.return_value = [1.3, 1.5]
        mock_model.intercept_ = 0.5
        mock_model.coef_ = [0.1, 0.01]
        mock_linear_regression.return_value = mock_model
        
        mock_train_test_split.return_value = (
            mock_data[['Population', 'Year']][:2],
            mock_data[['Population', 'Year']][2:],
            mock_data['CO2_per_capita'][:2],
            mock_data['CO2_per_capita'][2:]
        )
        
        model, mse, r2 = multivariate_regression(mock_data)
        self.assertEqual(mock_model.predict.call_count, 1)
        self.assertIsInstance(mse, float)
        self.assertIsInstance(r2, float)

    @patch("regression_analysis.train_test_split")
    @patch("regression_analysis.PolynomialFeatures")
    @patch("regression_analysis.LinearRegression")
    def test_polynomial_regression(self, mock_linear_regression, mock_polynomial_features, mock_train_test_split):
        """Test polynomial regression."""
        mock_data = pd.DataFrame({
            'Population': [1000, 2000, 3000],
            'Year': [2000, 2001, 2002],
            'CO2_per_capita': [1.2, 1.4, 1.6]
        })
        mock_poly = MagicMock()
        mock_poly.fit_transform.return_value = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        mock_polynomial_features.return_value = mock_poly
        
        mock_model = MagicMock()
        mock_model.predict.return_value = [1.3, 1.5]
        mock_linear_regression.return_value = mock_model
        
        mock_train_test_split.return_value = (
            np.array([[1, 2], [3, 4]]),
            np.array([[5, 6]]),
            mock_data['CO2_per_capita'][:2],
            mock_data['CO2_per_capita'][2:]
        )
        
        model, mse, r2 = polynomial_regression(mock_data, degree=2)
        self.assertEqual(mock_poly.fit_transform.call_count, 1)
        self.assertEqual(mock_model.predict.call_count, 1)
        self.assertIsInstance(mse, float)
        self.assertIsInstance(r2, float)


if __name__ == "__main__":
    unittest.main()
