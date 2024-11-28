import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from py_scripts.time_series_analysis import (
    load_data,
    preprocess_data,
    get_top_bottom_countries,
    filter_and_calculate_moving_average
)

@pytest.fixture
def sample_df():
    """Create sample DataFrame for testing"""
    return pd.DataFrame({
        'Country': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
        'Year': [2000, 2001, 2002, 2000, 2001, 2002, 2000, 2001, 2002],
        'CO2_per_capita': [10, 11, 12, 1, 2, 3, 5, 6, 7]
    })

def test_preprocess_data(sample_df):
    """Test if data is properly sorted by Country and Year"""
    # Shuffle the DataFrame
    shuffled_df = sample_df.sample(frac=1, random_state=42)
    
    # Preprocess the shuffled data
    processed_df = preprocess_data(shuffled_df)
    
    # Check if sorted correctly
    assert processed_df.iloc[0]['Country'] == 'A'
    assert processed_df.iloc[0]['Year'] == 2000
    assert list(processed_df.groupby('Country').first().index) == ['A', 'B', 'C']
    assert all(processed_df.groupby('Country')['Year'].is_monotonic_increasing)

def test_get_top_bottom_countries(sample_df):
    """Test identification of top and bottom countries"""
    top_countries, bottom_countries = get_top_bottom_countries(sample_df, num_countries=2)
    
    # Check return types
    assert isinstance(top_countries, pd.Index)
    assert isinstance(bottom_countries, pd.Index)
    
    # Check correct countries identified
    assert 'A' in top_countries  # Highest CO2 per capita
    assert 'B' in bottom_countries  # Lowest CO2 per capita
    assert len(top_countries) == 2
    assert len(bottom_countries) == 2

def test_filter_and_calculate_moving_average(sample_df):
    """Test filtering and moving average calculation"""
    countries = ['A', 'B']
    window_size = 2
    
    filtered_df = filter_and_calculate_moving_average(
        sample_df, 
        countries, 
        window_size=window_size
    )
    
    # Check if only specified countries are included
    assert set(filtered_df['Country'].unique()) == set(countries)
    
    # Check if moving average column exists
    assert 'CO2_per_capita_MA' in filtered_df.columns
    
    # Check moving average calculation
    country_a_ma = filtered_df[filtered_df['Country'] == 'A']['CO2_per_capita_MA'].tolist()
    assert abs(country_a_ma[-1] - np.mean([11, 12])) < 0.001  # Last MA for country A

def test_load_data(tmp_path):
    """Test data loading functionality"""
    # Create a temporary CSV file
    test_df = pd.DataFrame({
        'Country': ['A', 'B'],
        'Year': [2000, 2000],
        'CO2_per_capita': [10, 20]
    })
    
    file_path = tmp_path / "test_data.csv"
    test_df.to_csv(file_path, index=False)
    
    # Test loading
    loaded_df = load_data(str(file_path))
    assert isinstance(loaded_df, pd.DataFrame)
    assert all(col in loaded_df.columns for col in ['Country', 'Year', 'CO2_per_capita'])
    assert len(loaded_df) == 2

def test_moving_average_edge_cases(sample_df):
    """Test moving average calculation with edge cases"""
    # Test with window size larger than data points
    large_window = filter_and_calculate_moving_average(sample_df, ['A'], window_size=5)
    assert not large_window['CO2_per_capita_MA'].isna().any()
    
    # Test with single data point
    single_point_df = sample_df.iloc[[0]]
    single_result = filter_and_calculate_moving_average(single_point_df, ['A'], window_size=3)
    assert not single_result['CO2_per_capita_MA'].isna().any()

def test_invalid_inputs():
    """Test handling of invalid inputs"""
    invalid_df = pd.DataFrame({
        'Country': ['A', 'A'],
        'Year': [2000, 2000],  # Duplicate years for same country
        'CO2_per_capita': [10, 20]
    })
    
    # Test with invalid window size
    with pytest.raises(Exception):
        filter_and_calculate_moving_average(invalid_df, ['A'], window_size=0)
    
    # Test with non-existent country
    filtered_df = filter_and_calculate_moving_average(invalid_df, ['NonExistentCountry'])
    assert len(filtered_df) == 0

def test_data_consistency(sample_df):
    """Test data consistency through the processing pipeline"""
    top_countries, bottom_countries = get_top_bottom_countries(sample_df, num_countries=1)
    all_countries = top_countries.union(bottom_countries)
    
    filtered_df = filter_and_calculate_moving_average(sample_df, all_countries)
    
    # Check that original values are preserved
    for country in all_countries:
        original_values = sample_df[sample_df['Country'] == country]['CO2_per_capita']
        filtered_values = filtered_df[filtered_df['Country'] == country]['CO2_per_capita']
        assert all(original_values.values == filtered_values.values)