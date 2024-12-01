import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../py_scripts")))
from data_preprocessing import connect_to_mongodb, get_co2_emission_data, preprocess_data, save_to_csv

class TestDataPreprocessing(unittest.TestCase):

    @patch('data_preprocessing.MongoClient')
    def test_connect_to_mongodb(self, mock_mongo_client):
        """Test MongoDB connection."""
        mock_client = MagicMock()
        mock_db = mock_client['group_5_project']
        mock_collection = mock_db["co2_emission"]
        mock_mongo_client.return_value = mock_client
        
        collection = connect_to_mongodb()
        self.assertEqual(collection, mock_collection)
        print("MongoDB connection test passed.")

    def test_get_co2_emission_data(self):
        """Test retrieval of CO2 emission data."""
        mock_documents = [
            {
                "_id": "Afghanistan",
                "iso_code": "AFG",
                "data": [
                    {"year": 2000, "population": 1000, "cumulative_luc_co2": 2.5, "coal_co2": 0.5,
                     "oil_co2": 1.0, "gas_co2": 0.5, "cement_co2": 0.2, "flaring_co2": 0.1,
                     "other_industry_co2": 0.2}
                ]
            }
        ]
        mock_collection = MagicMock()
        mock_collection.find.return_value = [{"Afghanistan": mock_documents[0]}]

        df = get_co2_emission_data(mock_collection)

        self.assertEqual(len(df), 1)
        self.assertIn('Country', df.columns)
        self.assertIn('Population', df.columns)
        self.assertEqual(df.iloc[0]['Country'], "Afghanistan")
        print("Data retrieval test passed.")

    def test_preprocess_data(self):
        """Test data preprocessing."""
        data = {
            'Country': ['Afghanistan', 'Afghanistan', 'Afghanistan'],
            'ISO_Code': ['AFG', 'AFG', 'AFG'],
            'Year': [2000, 2001, 2000],
            'Population': [1000, None, 1000],
            'CO2': [2.5, None, 2.5],
            'Coal_CO2': [0.5, None, 0.5],
            'Oil_CO2': [1.0, None, 1.0],
            'Gas_CO2': [0.5, None, 0.5],
            'Cement_CO2': [0.2, None, 0.2],
            'Flaring_CO2': [0.1, None, 0.1],
            'Other_Industry_CO2': [0.2, None, 0.2]
        }
        df = pd.DataFrame(data)

        processed_df = preprocess_data(df)

        self.assertEqual(len(processed_df), 2)  # One duplicate should be removed
        self.assertIn('CO2_per_capita', processed_df.columns)
        print("Data preprocessing test passed.")

    @patch('data_preprocessing.pd.DataFrame.to_csv')
    def test_save_to_csv(self, mock_to_csv):
        """Test saving to CSV."""
        df = pd.DataFrame({'A': [1, 2, 3]})
        save_to_csv(df, "mock_path.csv")
        mock_to_csv.assert_called_once_with("mock_path.csv", index=False)
        print("Save to CSV test passed.")

if __name__ == '__main__':
    unittest.main()
