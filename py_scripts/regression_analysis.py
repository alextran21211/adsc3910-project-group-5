# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

# Load dataset function
def load_data(file_path):
    """Load the dataset from a specified CSV file."""
    return pd.read_csv(file_path)

# Calculate correlation matrix
def calculate_correlation_matrix(df):
    """Calculate and print the correlation matrix of numerical columns in the dataset."""
    correlation_matrix = df.select_dtypes(include=[np.number]).corr()
    print("Correlation Matrix:\n", correlation_matrix)
    return correlation_matrix

# Perform multivariate regression analysis
def multivariate_regression(df):
    """Perform multivariate linear regression and evaluate the model."""
    # Prepare features and target
    X = df[['Population', 'Year']]
    y = df['CO2_per_capita']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and fit the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predictions and evaluation
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Output results
    print("\nMultivariate Linear Regression Results:")
    print("Mean Squared Error:", mse)
    print("R-squared:", r2)
    print("Intercept:", model.intercept_)
    print("Coefficients:", model.coef_)
    
    return model, mse, r2

# Perform polynomial regression analysis
def polynomial_regression(df, degree=2):
    """Perform polynomial regression with a specified degree and evaluate the model."""
    # Prepare features and target
    X = df[['Population', 'Year']]
    y = df['CO2_per_capita']
    
    # Transform features to polynomial features
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)
    
    # Split the data
    X_train_poly, X_test_poly, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)
    
    # Initialize and fit the polynomial regression model
    model_poly = LinearRegression()
    model_poly.fit(X_train_poly, y_train)
    
    # Predictions and evaluation
    y_pred_poly = model_poly.predict(X_test_poly)
    mse_poly = mean_squared_error(y_test, y_pred_poly)
    r2_poly = r2_score(y_test, y_pred_poly)
    
    # Output results
    print(f"\nPolynomial Regression Results (Degree {degree}):")
    print("Polynomial Mean Squared Error:", mse_poly)
    print("Polynomial R-squared:", r2_poly)
    
    return model_poly, mse_poly, r2_poly

# Main function
def main(file_path):
    # Load and analyze data
    df = load_data(file_path)
    calculate_correlation_matrix(df)
    
    # Perform multivariate regression
    multivariate_model, multivariate_mse, multivariate_r2 = multivariate_regression(df)
    
    # Perform polynomial regression
    polynomial_model, poly_mse, poly_r2 = polynomial_regression(df, degree=2)

# Run the main function
if __name__ == "__main__":
    main('co2_emission_preprocessed.csv')  # Replace with your preprocessed file 
