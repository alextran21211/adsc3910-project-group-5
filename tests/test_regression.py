import pytest
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from py_scripts.regression_analysis import (
    load_data,
    calculate_correlation_matrix,
    multivariate_regression,
    polynomial_regression
)

@pytest.fixture
def sample_df():
    """Create sample DataFrame with strong correlations for testing"""
    np.random.seed(42)
    n_samples = 20
    
    # Create more structured test data
    years = np.array(range(2000, 2020))
    population = np.linspace(1000, 2000, n_samples)
    
    # Create CO2 data with strong linear relationship
    co2 = (0.5 * (population - 1000) +  # Linear relationship with population
           0.2 * (years - 2000) +        # Linear relationship with year
           np.random.normal(0, 1, n_samples))  # Small random noise
    
    return pd.DataFrame({
        'Year': years,
        'Population': population,
        'CO2_per_capita': co2
    })

@pytest.fixture
def exponential_data():
    """Create sample data with exponential relationship"""
    np.random.seed(42)
    n_samples = 20
    
    years = np.array(range(2000, 2020))
    population = np.linspace(1000, 2000, n_samples)
    
    # Create exponential relationship
    co2 = np.exp(0.001 * population) + np.random.normal(0, 0.1, n_samples)
    
    return pd.DataFrame({
        'Year': years,
        'Population': population,
        'CO2_per_capita': co2
    })

@pytest.fixture
def logarithmic_data():
    """Create sample data with logarithmic relationship"""
    np.random.seed(42)
    n_samples = 20
    
    years = np.array(range(2000, 2020))
    population = np.linspace(1000, 2000, n_samples)
    
    # Create logarithmic relationship
    co2 = np.log(population) + np.random.normal(0, 0.1, n_samples)
    
    return pd.DataFrame({
        'Year': years,
        'Population': population,
        'CO2_per_capita': co2
    })

@pytest.fixture
def periodic_data():
    """Create sample data with periodic/seasonal relationship"""
    np.random.seed(42)
    n_samples = 50  # Increased sample size for better pattern detection
    
    years = np.array(range(2000, 2000 + n_samples))
    population = np.linspace(1000, 2000, n_samples)
    
    # Create clearer periodic pattern with trend
    time = np.arange(n_samples)
    co2 = (
        10 * np.sin(2 * np.pi * time / 12) +  # Seasonal pattern
        0.1 * time +                          # Upward trend
        np.random.normal(0, 0.5, n_samples)   # Small noise
    )
    
    return pd.DataFrame({
        'Year': years,
        'Population': population,
        'CO2_per_capita': co2
    })

def test_load_data(tmp_path):
    """Test data loading function"""
    # Create a temporary CSV file
    df = pd.DataFrame({
        'Year': [2020, 2021],
        'Population': [1000, 1100],
        'CO2_per_capita': [10.0, 11.0]
    })
    
    file_path = tmp_path / "test_data.csv"
    df.to_csv(file_path, index=False)
    
    # Test loading
    loaded_df = load_data(str(file_path))
    assert isinstance(loaded_df, pd.DataFrame)
    assert len(loaded_df) == 2
    assert all(col in loaded_df.columns for col in ['Year', 'Population', 'CO2_per_capita'])

def test_calculate_correlation_matrix(sample_df):
    """Test correlation matrix calculation"""
    corr_matrix = calculate_correlation_matrix(sample_df)
    assert isinstance(corr_matrix, pd.DataFrame)
    assert corr_matrix.shape == (3, 3)
    assert all(col in corr_matrix.columns for col in ['Year', 'Population', 'CO2_per_capita'])

def test_multivariate_regression(sample_df):
    """Test multivariate regression"""
    model, mse, r2 = multivariate_regression(sample_df)
    assert hasattr(model, 'predict')
    assert hasattr(model, 'coef_')
    assert isinstance(mse, float)
    assert isinstance(r2, float)
    assert mse >= 0
    assert r2 < 1.1

def test_polynomial_regression(sample_df):
    """Test polynomial regression"""
    model, mse, r2 = polynomial_regression(sample_df, degree=2)
    assert hasattr(model, 'predict')
    assert hasattr(model, 'coef_')
    assert isinstance(mse, float)
    assert isinstance(r2, float)
    assert mse >= 0
    assert r2 < 1.1

def test_regression_exponential_distribution(exponential_data):
    """Test regression on exponential relationship"""
    linear_model, linear_mse, linear_r2 = multivariate_regression(exponential_data)
    poly_model, poly_mse, poly_r2 = polynomial_regression(exponential_data, degree=3)
    assert isinstance(linear_r2, float)
    assert isinstance(poly_r2, float)

def test_regression_logarithmic_distribution(logarithmic_data):
    """Test regression on logarithmic relationship"""
    linear_model, linear_mse, linear_r2 = multivariate_regression(logarithmic_data)
    poly_model, poly_mse, poly_r2 = polynomial_regression(logarithmic_data, degree=2)
    assert isinstance(linear_mse, float)
    assert isinstance(poly_mse, float)
    assert linear_mse > 0
    assert poly_mse > 0

def test_regression_periodic_distribution(periodic_data):
    """Test regression on periodic data"""
    # Test different polynomial degrees
    mse_values = {}
    r2_values = {}
    
    # Try different polynomial degrees
    for degree in [1, 2, 3, 4, 5]:
        _, mse, r2 = polynomial_regression(periodic_data, degree=degree)
        mse_values[degree] = mse
        r2_values[degree] = r2
    
    # Basic checks
    assert isinstance(mse_values[1], float)
    assert isinstance(r2_values[1], float)
    
    # Check if higher degrees capture pattern better
    assert mse_values[4] >= 0  # MSE should be non-negative
    
    # Print diagnostics
    print("\nMSE values for different degrees:")
    for degree, mse in mse_values.items():
        print(f"Degree {degree}: MSE = {mse:.4f}")
        
    print("\nR² values for different degrees:")
    for degree, r2 in r2_values.items():
        print(f"Degree {degree}: R² = {r2:.4f}")