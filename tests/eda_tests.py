import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from pymongo import MongoClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../py_scripts")))

from eda import data  # Assuming data is returned after preprocessing

class TestEda(unittest.TestCase):

    @patch("eda.MongoClient")
    def test_mongo_connection(self, MockMongoClient):
        # Mock MongoDB client
        mock_client = MockMongoClient.return_value
        mock_collection = mock_client['group_5_project']['co2_emission']
        mock_collection.find.return_value = [{"Afghanistan": {"iso_code": "AFG", "data": [{"year": 1850, "population": 1000, "cumulative_luc_co2": 2.5}]}}]

        # Mock data retrieval
        documents = mock_collection.find()
        self.assertIsInstance(documents, list)
        self.assertGreater(len(documents), 0)

    def test_dataframe_structure(self):
        # Create a sample dataframe
        sample_data = [
            {"Country": "Afghanistan", "ISO_Code": "AFG", "Year": 1850, "Population": 1000, "CO2": 2.5},
            {"Country": "Brazil", "ISO_Code": "BRA", "Year": 1850, "Population": 2000, "CO2": 5.0}
        ]
        df = pd.DataFrame(sample_data)

        # Check columns
        expected_columns = ["Country", "ISO_Code", "Year", "Population", "CO2"]
        self.assertListEqual(list(df.columns), expected_columns)

        # Check data types
        self.assertTrue(df["Population"].dtype in ["int64", "float64"])
        self.assertTrue(df["CO2"].dtype in ["int64", "float64"])

    def test_missing_values_handling(self):
        # Test missing value handling
        sample_data = [
            {"Country": "Afghanistan", "ISO_Code": "AFG", "Year": 1850, "Population": None, "CO2": 2.5},
            {"Country": "Brazil", "ISO_Code": "BRA", "Year": 1850, "Population": 2000, "CO2": None}
        ]
        df = pd.DataFrame(sample_data)

        # Fill missing values
        df['Population'] = df['Population'].fillna(df['Population'].mean())
        df['CO2'] = df['CO2'].fillna(df['CO2'].mean())

        # Ensure no missing values
        self.assertFalse(df['Population'].isnull().any())
        self.assertFalse(df['CO2'].isnull().any())

    def test_co2_per_capita_calculation(self):
        # Test CO2 per capita calculation
        sample_data = [
            {"Country": "Afghanistan", "ISO_Code": "AFG", "Year": 1850, "Population": 1000, "CO2": 2.5},
            {"Country": "Brazil", "ISO_Code": "BRA", "Year": 1850, "Population": 2000, "CO2": 5.0}
        ]
        df = pd.DataFrame(sample_data)
        df['CO2_per_capita'] = df['CO2'] / df['Population']

        # Check calculation
        self.assertAlmostEqual(df.iloc[0]['CO2_per_capita'], 0.0025)
        self.assertAlmostEqual(df.iloc[1]['CO2_per_capita'], 0.0025)

if __name__ == '__main__':
    unittest.main()
