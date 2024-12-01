import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../py_scripts")))
from data_preprocessing import (
    load_credentials,
    connect_to_mongodb,
    get_co2_emission_data,
    preprocess_data,
    save_to_csv,
)

class TestDataPreprocessing(unittest.TestCase):

    def test_load_credentials(self):
        """Test loading credentials from a JSON file."""
        mock_json = '{"host": "localhost", "username": "test_user", "password": "test_pass", "database": "test_db"}'
        with patch("builtins.open", unittest.mock.mock_open(read_data=mock_json)):
            creds = load_credentials("mock_path.json")
        self.assertEqual(creds['host'], 'localhost')
        self.assertEqual(creds['username'], 'test_user')
        self.assertEqual(creds['password'], 'test_pass')
        self.assertEqual(creds['database'], 'test_db')

    @patch("data_preprocessing.MongoClient")
    def test_connect_to_mongodb(self, mock_client):
        """Test MongoDB connection."""
        mock_db = MagicMock()
        mock_client.return_value.__getitem__.return_value = mock_db
        creds = {'username': 'user', 'password': 'pass', 'host': 'host', 'database': 'db'}
        db = connect_to_mongodb(creds)
        self.assertEqual(db, mock_db)

    @patch("data_preprocessing.MongoClient")
    def test_get_co2_emission_data(self, mock_client):
        """Test retrieving CO2 emission data."""
        mock_collection = MagicMock()
        mock_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection
        mock_collection.aggregate.return_value = [
            {"Country": "Afghanistan", "ISO_Code": "AFG", "Year": 2020, "Population": 1000, "CO2": 2000, "CO2_per_capita": 2.0}
        ]
        df = get_co2_emission_data(mock_collection)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.loc[0, 'Country'], "Afghanistan")

    def test_preprocess_data(self):
        """Test preprocessing data."""
        data = {
            "Country": ["Afghanistan", "Afghanistan"],
            "Year": [2020, 2021],
            "ISO_Code": ["AFG", "AFG"],
            "Population": [1000, 2000],
            "CO2": [2000, 4000],
            "CO2_per_capita": [2.0, 2.0]
        }
        df = pd.DataFrame(data)
        processed_df = preprocess_data(df)
        self.assertNotIn("ISO_Code", processed_df.columns)
        self.assertAlmostEqual(processed_df["Population"].max(), 1.0)
        self.assertAlmostEqual(processed_df["Population"].min(), 0.0)

    @patch("data_preprocessing.pd.DataFrame.to_csv")
    def test_save_to_csv(self, mock_to_csv):
        """Test saving DataFrame to a CSV file."""
        data = {"Country": ["Afghanistan"], "Year": [2020], "Population": [1.0], "CO2": [1.0], "CO2_per_capita": [1.0]}
        df = pd.DataFrame(data)
        save_to_csv(df, "test.csv")
        mock_to_csv.assert_called_once_with("test.csv", index=False)

if __name__ == "__main__":
    unittest.main()
