import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from py_scripts.eda import connect_to_mongo, fetch_and_transform_data, clean_data

from py_scripts.eda import (
            plot_co2_emissions_over_time,
            plot_co2_per_capita_over_time,
            plot_population_growth_over_time,
            plot_relationship_population_co2,
            plot_correlation_heatmap,
            plot_co2_emissions_multiple_countries,
            plot_top_5_co2_per_capita
        )

class TestCO2Analysis(unittest.TestCase):


    def test_clean_data(self):
        """Test data cleaning and preprocessing."""
        test_data = {
            "Country": ["A", "B", "A"],
            "ISO_Code": ["A1", "B1", "A1"],
            "Year": [2000, 2001, 2001],
            "Population": [1000, np.nan, 1100],
            "CO2": [500, 800, np.nan]
        }
        test_df = pd.DataFrame(test_data)
        cleaned_df = clean_data(test_df)
        
        expected_data = {
            "Country": ["A", "B", "A"],
            "Year": [2000, 2001, 2001],
            "Population": [1000, 1050, 1100],  # 1050 is the mean population
            "CO2": [500, 800, 650],  # 650 is the mean CO2
            "CO2_per_capita": [0.5, 0.7619, 0.5909]  # Computed CO2 per capita
        }
        expected_df = pd.DataFrame(expected_data)
        
        pd.testing.assert_frame_equal(cleaned_df.reset_index(drop=True), expected_df.reset_index(drop=True), check_less_precise=3)

    def test_plot_functions(self):
        """Test that plot functions run without error."""
        df = pd.DataFrame({
            "Country": ["A", "A", "B", "B"],
            "Year": [2000, 2001, 2000, 2001],
            "Population": [1000, 1100, 2000, 2100],
            "CO2": [500, 550, 1000, 1050],
            "CO2_per_capita": [0.5, 0.5, 0.5, 0.5]
        })

        try:
         
            plot_co2_emissions_over_time(df, "A")
            plot_co2_per_capita_over_time(df, "A")
            plot_population_growth_over_time(df, "A")
            plot_relationship_population_co2(df)
            plot_correlation_heatmap(df)
            plot_co2_emissions_multiple_countries(df)
            plot_top_5_co2_per_capita(df)
        except Exception as e:
            self.fail(f"Plot functions raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
