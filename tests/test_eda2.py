import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # Add this import
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from py_scripts.eda2 import clean_data, plot_co2_over_time

@pytest.fixture
def sample_df():
    """Create sample DataFrame for testing"""
    return pd.DataFrame({
        'Country': ['Afghanistan', 'Brazil'],
        'ISO_Code': ['AFG', 'BRA'],
        'Year': [2020, 2020],
        'Population': [1000, 2000],
        'CO2': [100, 200]
    })

def test_clean_data(sample_df):
    """Test data cleaning function"""
    cleaned_df = clean_data(sample_df)
    
    assert 'ISO_Code' not in cleaned_df.columns
    assert 'CO2_per_capita' in cleaned_df.columns
    assert not cleaned_df.isnull().any().any()

def test_plot_co2_over_time(sample_df):
    """Test plotting function"""
    cleaned_df = clean_data(sample_df)
    fig = plot_co2_over_time(cleaned_df)
    assert isinstance(fig, plt.Figure)
    plt.close(fig)  # Clean up the plot after test