# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the dataset
def load_data(file_path):
    """Load the dataset from the specified CSV file."""
    return pd.read_csv(file_path)

# Preprocess the data
def preprocess_data(df):
    """Sort data by 'Country' and 'Year'."""
    return df.sort_values(by=['Country', 'Year'])

# Calculate the average CO2 per capita for each country and identify top/bottom countries
def get_top_bottom_countries(df, num_countries=10):
    """Return the top and bottom countries based on average CO2 per capita."""
    average_co2_per_capita = df.groupby('Country')['CO2_per_capita'].mean()
    top_countries = average_co2_per_capita.nlargest(num_countries).index
    bottom_countries = average_co2_per_capita.nsmallest(num_countries).index
    return top_countries, bottom_countries

# Filter the dataset for selected countries and compute the moving average
def filter_and_calculate_moving_average(df, countries, window_size=10):
    """Filter the DataFrame for specified countries and calculate the moving average."""
    filtered_df = df[df['Country'].isin(countries)].copy()
    filtered_df['CO2_per_capita_MA'] = (
        filtered_df.groupby('Country')['CO2_per_capita']
        .transform(lambda x: x.rolling(window=window_size, min_periods=1).mean())
    )
    return filtered_df

# Plotting functions
def plot_raw_data(df, top_countries, bottom_countries, colors):
    """Plot raw CO2 per capita data for the top 10 and bottom 10 countries."""
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot top countries
    for i, country in enumerate(top_countries):
        country_df = df[df['Country'] == country]
        ax.plot(country_df['Year'], country_df['CO2_per_capita'], 
                label=country, color=colors[i], linestyle='-', alpha=0.7)
    
    # Plot bottom countries
    for i, country in enumerate(bottom_countries):
        country_df = df[df['Country'] == country]
        ax.plot(country_df['Year'], country_df['CO2_per_capita'], 
                label=country, color=colors[len(top_countries) + i], linestyle='--', alpha=0.7)
    
    ax.set_title('Raw CO2 per Capita Data (Top 10 and Bottom 10 Countries)')
    ax.set_ylabel('CO2 per Capita')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)
    ax.grid(True)
    plt.tight_layout()
    plt.show()

def plot_moving_average(df, top_countries, bottom_countries, colors, window_size):
    """Plot the moving average CO2 per capita for the top 10 and bottom 10 countries."""
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot top countries
    for i, country in enumerate(top_countries):
        country_df = df[df['Country'] == country]
        ax.plot(country_df['Year'], country_df['CO2_per_capita_MA'], 
                label=f'{country} MA', color=colors[i], linestyle='-', alpha=0.8)
    
    # Plot bottom countries
    for i, country in enumerate(bottom_countries):
        country_df = df[df['Country'] == country]
        ax.plot(country_df['Year'], country_df['CO2_per_capita_MA'], 
                label=f'{country} MA', color=colors[len(top_countries) + i], linestyle='--', alpha=0.8)
    
    ax.set_title(f'{window_size}-Year Moving Average of CO2 per Capita Data (Top 10 and Bottom 10 Countries)')
    ax.set_xlabel('Year')
    ax.set_ylabel('CO2 per Capita (10-Year MA)')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)
    ax.grid(True)
    plt.tight_layout()
    plt.show()

# Main function
def main(file_path):
    # Load and preprocess data
    df = load_data(file_path)
    df = preprocess_data(df)
    
    # Get top and bottom countries
    top_countries, bottom_countries = get_top_bottom_countries(df)
    countries = top_countries.union(bottom_countries)
    
    # Filter and calculate moving average
    filtered_df = filter_and_calculate_moving_average(df, countries)
    
    # Set up color palette with distinct colors
    colors = sns.color_palette("hsv", len(top_countries) + len(bottom_countries))
    
    # Plot raw data and moving average data
    plot_raw_data(filtered_df, top_countries, bottom_countries, colors)
    plot_moving_average(filtered_df, top_countries, bottom_countries, colors, window_size=10)

# Run the main function
if __name__ == "__main__":
    main('co2_emission_preprocessed.csv')  # Replace with your file path
