# Import necessary libraries
import pandas as pd
from pymongo import MongoClient
from sklearn.preprocessing import MinMaxScaler
import urllib.parse

# MongoDB connection
def connect_to_mongodb():
    """Establish connection to MongoDB using hardcoded credentials."""
    username = "alextran21211"
    password = urllib.parse.quote("database12345")
    host = "cluster0.zsych.mongodb.net"
    url = f"mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority"

    client = MongoClient(url)
    db = client['group_5_project']
    collection = db["co2_emission"]
    return collection

# MongoDB aggregation pipeline
def get_co2_emission_data(collection):
    """Retrieve CO2 emission data with additional features."""
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
                coal_co2 = entry.get('coal_co2')
                oil_co2 = entry.get('oil_co2')
                gas_co2 = entry.get('gas_co2')
                cement_co2 = entry.get('cement_co2')
                flaring_co2 = entry.get('flaring_co2')
                other_industry_co2 = entry.get('other_industry_co2')

                data.append({
                    'Country': country,
                    'ISO_Code': iso_code,
                    'Year': year,
                    'Population': population,
                    'CO2': co2,
                    'Coal_CO2': coal_co2,
                    'Oil_CO2': oil_co2,
                    'Gas_CO2': gas_co2,
                    'Cement_CO2': cement_co2,
                    'Flaring_CO2': flaring_co2,
                    'Other_Industry_CO2': other_industry_co2
                })

    df = pd.DataFrame(data)
    return df

# Preprocess data
def preprocess_data(df):
    """Preprocess the DataFrame and scale numerical columns."""
    # Handle missing values
    df['Population'] = df['Population'].fillna(df['Population'].mean())
    df['CO2'] = df['CO2'].fillna(df['CO2'].mean())
    df['Coal_CO2'] = df['Coal_CO2'].fillna(0)
    df['Oil_CO2'] = df['Oil_CO2'].fillna(0)
    df['Gas_CO2'] = df['Gas_CO2'].fillna(0)
    df['Cement_CO2'] = df['Cement_CO2'].fillna(0)
    df['Flaring_CO2'] = df['Flaring_CO2'].fillna(0)
    df['Other_Industry_CO2'] = df['Other_Industry_CO2'].fillna(0)

    # Calculate CO₂ per capita
    df['CO2_per_capita'] = df['CO2'] / df['Population']

    # Drop duplicate and unnecessary columns
    df.drop(columns=['ISO_Code'], inplace=True, errors='ignore')
    df.drop_duplicates(inplace=True)

    # Filter countries and years
    countries_list = [
        'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Argentina', 'Armenia',
        'Australia', 'Austria', 'Azerbaijan', 'Bangladesh', 'Belarus', 'Belgium', 'Brazil',
        'Canada', 'China', 'Colombia', 'Czechia', 'Denmark', 'Egypt', 'France', 'Germany',
        'Greece', 'India', 'Indonesia', 'Iran', 'Italy', 'Japan', 'Mexico', 'Netherlands',
        'Norway', 'Pakistan', 'Poland', 'Portugal', 'Russia', 'Saudi Arabia', 'South Africa',
        'South Korea', 'Spain', 'Sweden', 'Switzerland', 'Thailand', 'Turkey', 'Ukraine',
        'United Kingdom', 'United States', 'Vietnam', 'Zimbabwe'
    ]
    df = df[(df['Country'].isin(countries_list)) & (df['Year'] > 1950)]

    # Scale numerical columns
    scaler = MinMaxScaler()
    df[['Population', 'CO2', 'CO2_per_capita', 'Coal_CO2', 'Oil_CO2', 'Gas_CO2',
        'Cement_CO2', 'Flaring_CO2', 'Other_Industry_CO2']] = scaler.fit_transform(
        df[['Population', 'CO2', 'CO2_per_capita', 'Coal_CO2', 'Oil_CO2', 'Gas_CO2',
            'Cement_CO2', 'Flaring_CO2', 'Other_Industry_CO2']]
    )

    return df

# Save data to CSV
def save_to_csv(df, file_path):
    """Save the DataFrame to a CSV file."""
    df.to_csv(file_path, index=False)
    print(f"Data preprocessing completed and saved to '{file_path}'.")

# Main function
def main():
    try:
        # Connect to MongoDB
        collection = connect_to_mongodb()
        print("Connected to MongoDB.")

        # Retrieve data from MongoDB
        df = get_co2_emission_data(collection)
        print("Data retrieved from MongoDB. Here are the first few rows:\n", df.head())

        # Preprocess data
        df = preprocess_data(df)
        print("Data preprocessing completed.")

        # Save to CSV
        save_to_csv(df, "../data/processed/co2_emission_preprocessed.csv")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the main function
if __name__ == "__main__":
    main()
