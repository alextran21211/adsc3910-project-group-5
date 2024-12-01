from pymongo import MongoClient
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, isnan, mean, stddev, min, max, desc
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType
import urllib.parse
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for Seaborn plots and change font
sns.set(style="whitegrid")
plt.rcParams["font.family"] = "DejaVu Sans"

def connect_to_mongo(username, password, host, db_name, collection_name):
    """Connect to MongoDB and return the specified collection."""
    password = urllib.parse.quote(password)
    url = f"mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority"
    client = MongoClient(url)
    db = client[db_name]
    return db[collection_name]

def fetch_and_transform_data(collection):
    """Fetch data from MongoDB collection and transform it into a pandas DataFrame."""
    documents = collection.find()
    data = []
    for doc in documents:
        for country, country_data in doc.items():
            if country == "_id":
                continue
            iso_code = country_data.get('iso_code')
            for entry in country_data.get('data', []):
                year = entry.get('year')
                population = entry.get('population')
                co2 = entry.get('cumulative_luc_co2')
                data.append({
                    'Country': country,
                    'ISO_Code': iso_code,
                    'Year': year,
                    'Population': population,
                    'CO2': co2
                })
    return pd.DataFrame(data)

def clean_data(df):
    """Clean and preprocess the data."""
    df['Population'] = df['Population'].fillna(df['Population'].mean())
    df['CO2'] = df['CO2'].fillna(df['CO2'].mean())
    df['CO2_per_capita'] = df['CO2'] / df['Population']
    df.drop_duplicates(inplace=True)
    df = df.drop(columns=['ISO_Code'])
    return df

def plot_co2_emissions_over_time(df, country):
    """Plot CO₂ emissions over time for a specific country."""
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df[df['Country'] == country], x='Year', y='CO2', color="b")
    plt.title(f"CO₂ Emissions Over Time for {country}")
    plt.xlabel("Year")
    plt.ylabel("Total CO₂ Emissions")
    plt.show()

def plot_co2_per_capita_over_time(df, country):
    """Plot CO₂ emissions per capita over time for a specific country."""
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df[df['Country'] == country], x='Year', y='CO2_per_capita', color="g")
    plt.title(f"CO₂ Emissions Per Capita Over Time for {country}")
    plt.xlabel("Year")
    plt.ylabel("CO₂ Emissions Per Capita")
    plt.show()

def plot_population_growth_over_time(df, country):
    """Plot population growth over time for a specific country."""
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df[df['Country'] == country], x='Year', y='Population', color="purple")
    plt.title(f"Population Growth Over Time for {country}")
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.show()

def plot_relationship_population_co2(df):
    """Plot relationship between population and CO₂ emissions."""
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Population', y='CO2', hue='Country', palette="coolwarm", legend=None)
    plt.title("Relationship Between Population and CO₂ Emissions")
    plt.xlabel("Population")
    plt.ylabel("Total CO₂ Emissions")
    plt.show()

def plot_correlation_heatmap(df):
    """Plot correlation heatmap."""
    plt.figure(figsize=(8, 6))
    correlation_matrix = df[['Population', 'CO2', 'CO2_per_capita']].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="YlGnBu", fmt=".2f")
    plt.title("Correlation Matrix")
    plt.show()

def plot_co2_emissions_multiple_countries(df):
    """Plot CO₂ emissions over time for multiple countries."""
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=df, x='Year', y='CO2', hue='Country', legend='full', palette='tab10')
    plt.title("CO₂ Emissions Over Time for Each Country")
    plt.xlabel("Year")
    plt.ylabel("Total CO₂ Emissions")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

def plot_top_5_co2_per_capita(df):
    """Plot CO₂ emissions per capita over time for the top 5 emitting countries."""
    non_countries = ["World", "High-income countries", "Low-income countries", "Upper-middle-income countries", 
                     "Lower-middle-income countries", "Africa", "Europe", "Asia", "Oceania", "Americas", "North America",
                     "South America", "Asia (excl. China and India)", "Europe (excl. EU-27)", "Europe (excl. EU-28)", "North America (excl. USA)"]
    df_filtered = df[~df['Country'].isin(non_countries)]
    top_countries = df_filtered.groupby('Country')['CO2'].mean().nlargest(5).index
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=df_filtered[df_filtered['Country'].isin(top_countries)], x='Year', y='CO2_per_capita', hue='Country', palette='Dark2')
    plt.title("CO₂ Emissions Per Capita Over Time for Top 5 CO₂ Emitting Countries")
    plt.xlabel("Year")
    plt.ylabel("CO₂ Emissions Per Capita")
    plt.legend(title="Country", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

# Main entry point
def main():
    # MongoDB credentials
    username = "alextran21211"
    password = "database12345"
    host = "cluster0.zsych.mongodb.net"
    db_name = "group_5_project"
    collection_name = "co2_emission"

    # Connect to MongoDB and fetch data
    collection = connect_to_mongo(username, password, host, db_name, collection_name)
    df = fetch_and_transform_data(collection)

    # Clean and preprocess data
 
