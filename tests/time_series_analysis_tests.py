import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../py_scripts")))
from time_series_analysis import (
    load_data,
    preprocess_data,
    get_top_bottom_countries,
    filter_and_calculate_moving_average,
)


class TestTimeSeriesAnalysis(unittest.TestCase):

    @patch("pandas.read_csv")
    def test_load_data(self, mock_read_csv):
        """Test loading data from a CSV file."""
        mock_data = pd.DataFrame({
            'Country': ['Afghanistan', 'Afghanistan', 'Brazil', 'Brazil'],
            'Year': [2000, 2001, 2000, 2001],
            'CO2_per_capita': [1.2, 1.3, 2.4, 2.5]
        })
        mock_read_csv.return_value = mock_data
        
        df = load_data("mock_file.csv")
        mock_read_csv.assert_called_once_with("mock_file.csv")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(list(df.columns), ['Country', 'Year', 'CO2_per_capita'])

    def test_preprocess_data(self):
        """Test preprocessing of data."""
        data = {
            'Country': ['Brazil', 'Afghanistan', 'Afghanistan', 'Brazil'],
            'Year': [2001, 2000, 2001, 2000],
            'CO2_per_capita': [2.4, 1.2, 1.3, 2.5]
        }
        df = pd.DataFrame(data)
        preprocessed_df = preprocess_data(df)
        self.assertTrue(preprocessed_df['Year'].is_monotonic_increasing)

    def test_get_top_bottom_countries(self):
        """Test identifying top and bottom countries based on average CO2 per capita."""
        data = {
            'Country': ['Afghanistan', 'Brazil', 'China', 'Denmark'],
            'CO2_per_capita': [1.2, 2.4, 3.6, 0.5]
        }
        df = pd.DataFrame(data)
        top_countries, bottom_countries = get_top_bottom_countries(df, num_countries=2)
        self.assertListEqual(list(top_countries), ['China', 'Brazil'])
        self.assertListEqual(list(bottom_countries), ['Denmark', 'Afghanistan'])

    def test_filter_and_calculate_moving_average(self):
        """Test filtering data and calculating the moving average."""
        data = {
            'Country': ['Afghanistan', 'Afghanistan', 'Brazil', 'Brazil'],
            'Year': [2000, 2001, 2000, 2001],
            'CO2_per_capita': [1.2, 1.3, 2.4, 2.5]
        }
        df = pd.DataFrame(data)
        filtered_df = filter_and_calculate_moving_average(df, ['Afghanistan', 'Brazil'], window_size=2)
        self.assertIn('CO2_per_capita_MA', filtered_df.columns)
        self.assertAlmostEqual(filtered_df[filtered_df['Country'] == 'Afghanistan']['CO2_per_capita_MA'].iloc[1], 1.25)

    @patch("matplotlib.pyplot.show")
    def test_plot_raw_data(self, mock_show):
        """Test plotting raw data (mock plt.show)."""
        data = {
            'Country': ['Afghanistan', 'Afghanistan', 'Brazil', 'Brazil'],
            'Year': [2000, 2001, 2000, 2001],
            'CO2_per_capita': [1.2, 1.3, 2.4, 2.5]
        }
        df = pd.DataFrame(data)
        top_countries = ['Brazil']
        bottom_countries = ['Afghanistan']
        colors = ['blue', 'red']
        
        from time_series_analysis import plot_raw_data
        plot_raw_data(df, top_countries, bottom_countries, colors)
        mock_show.assert_called_once()

    @patch("matplotlib.pyplot.show")
    def test_plot_moving_average(self, mock_show):
        """Test plotting moving average data (mock plt.show)."""
        data = {
            'Country': ['Afghanistan', 'Afghanistan', 'Brazil', 'Brazil'],
            'Year': [2000, 2001, 2000, 2001],
            'CO2_per_capita': [1.2, 1.3, 2.4, 2.5],
            'CO2_per_capita_MA': [1.2, 1.25, 2.4, 2.45]
        }
        df = pd.DataFrame(data)
        top_countries = ['Brazil']
        bottom_countries = ['Afghanistan']
        colors = ['blue', 'red']
        
        from time_series_analysis import plot_moving_average
        plot_moving_average(df, top_countries, bottom_countries, colors, window_size=2)
        mock_show.assert_called_once()


if __name__ == "__main__":
    unittest.main()
