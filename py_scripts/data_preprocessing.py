# Import necessary libraries
import json
import urllib.parse
import pandas as pd
from pymongo import MongoClient
from sklearn.preprocessing import MinMaxScaler

# Load MongoDB credentials function
def load_credentials(file_path):
    """Load MongoDB credentials from a JSON file."""
    with open(file_path) as f:
        creds = json.load(f)
    return creds

# Connect to MongoDB function
def connect_to_mongodb(creds):
    """Establish a MongoDB connection using credentials."""
    username = urllib.parse.quote_plus(creds['username'])
    password = urllib.parse.quote_plus(creds['password'])
    host = creds['host']
    db_name = creds['database']
    
    client = MongoClient(f"mongodb://{username}:{password}@{host}/{db_name}")
    return client[db_name]

# Define MongoDB aggregation pipeline function
def get_co2_emission_data(collection):
    """Retrieve CO2 emission data using an aggregation pipeline."""
    pipeline = [
        {"$unwind": "$data"},
        {"$project": {
            "Country": "$_id",
            "ISO_Code": "$iso_code",
            "Year": "$data.year",
            "Population": {"$ifNull": ["$data.population", 0]},
            "CO2": {"$ifNull": ["$data.cumulative_luc_co2", 0]}
        }},
        {"$group": {
            "_id": {"Country": "$Country", "Year": "$Year"},
            "ISO_Code": {"$first": "$ISO_Code"},
            "Population": {"$avg": "$Population"},
            "CO2": {"$avg": "$CO2"}
        }},
        {"$project": {
            "Country": "$_id.Country",
            "Year": "$_id.Year",
            "ISO_Code": 1,
            "Population": 1,
            "CO2": 1,
            "CO2_per_capita": {
                "$cond": {
                    "if": {"$gt": ["$Population", 0]},
                    "then": {"$divide": ["$CO2", "$Population"]},
                    "else": 0
                }
            }
        }}
    ]
    
    results = collection.aggregate(pipeline)
    return pd.DataFrame(list(results))

# Preprocess and scale data function
def preprocess_data(df):
    """Preprocess the DataFrame and scale numerical columns."""
    df.drop(columns=['ISO_Code'], inplace=True)
    
    scaler = MinMaxScaler()
    df[['Population', 'CO2', 'CO2_per_capita']] = scaler.fit_transform(df[['Population', 'CO2', 'CO2_per_capita']])
    
    return df

# Save data to CSV function
def save_to_csv(df, file_path):
    """Save the DataFrame to a CSV file."""
    df.to_csv(file_path, index=False)
    print(f"Data preprocessing completed and saved to '{file_path}'.")

# Main function
def main():
    # Load credentials and connect to MongoDB
    creds = load_credentials("credentials_mongodb.json")
    db = connect_to_mongodb(creds)
    collection = db["co2_emission"]
    
    # Retrieve and process data
    df = get_co2_emission_data(collection)
    df = preprocess_data(df)
    
    # Save the processed data
    save_to_csv(df, "co2_emission_preprocessed.csv")

# Run the main function
if __name__ == "__main__":
    main()
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def process_co2_emission_data(collection):
    try:
        pipeline = [
            {"$unwind": "$data"},
            {"$project": {
                "Country": "$_id",
                "ISO_Code": "$iso_code",
                "Year": "$data.year",
                "Population": {"$ifNull": ["$data.population", 0]},
                "CO2": {"$ifNull": ["$data.cumulative_luc_co2", 0]}
            }},
            {"$group": {
                "_id": {"Country": "$Country", "Year": "$Year"},
                "ISO_Code": {"$first": "$ISO_Code"},
                "Population": {"$avg": "$Population"},
                "CO2": {"$avg": "$CO2"}
            }},
            {"$project": {
                "Country": "$_id.Country",
                "Year": "$_id.Year",
                "ISO_Code": 1,
                "Population": 1,
                "CO2": 1,
                "CO2_per_capita": {
                    "$cond": {
                        "if": {"$gt": ["$Population", 0]},
                        "then": {"$divide": ["$CO2", "$Population"]},
                        "else": 0
                    }
                }
            }}
        ]
        print("Pipeline created.")

        results = list(collection.aggregate(pipeline))
        if not results:
            print("No results returned from aggregation pipeline.")
            return
        print("Aggregation pipeline executed. Number of results:", len(results))

        df = pd.DataFrame(results)
        print("Data loaded into DataFrame. Here are the first few rows:\n", df.head())

        df.drop(columns=['ISO_Code'], inplace=True)
        print("ISO_Code column dropped.")

        scaler = MinMaxScaler()
        df[['Population', 'CO2', 'CO2_per_capita']] = scaler.fit_transform(df[['Population', 'CO2', 'CO2_per_capita']])
        print("Data scaling completed.")

        # Save the processed data to a CSV file
        df.to_csv("co2_emission_preprocessed.csv", index=False)
        print("Data preprocessing completed and saved to 'co2_emission_preprocessed.csv'.")

    except Exception as e:
        print("An error occurred:", e)