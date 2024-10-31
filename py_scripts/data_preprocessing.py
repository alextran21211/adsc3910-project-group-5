import json
from pymongo import MongoClient
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import urllib.parse

def process_co2_emission_data():
    with open("credentials_mongodb.json") as f:
        creds = json.load(f)
    
    username = urllib.parse.quote_plus(creds['username'])
    password = urllib.parse.quote_plus(creds['password'])
    host = creds['host']
    db_name = creds['database']

    client = MongoClient(f"mongodb://{username}:{password}@{host}/{db_name}")
    db = client[db_name]
    collection = db["co2_emission"]

    pipeline = [
        {"$unwind": "$data"},
        {"$project": {
            "Country": "$_id",
            "ISO_Code": "$iso_code",
            "Year": "$data.year",
            "Population": {"$ifNull": ["$data.population", 0]},  
            "CO2": {"$ifNull": ["$data.cumulative_luc_co2", 0]}  

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
            "CO2_per_capita": {"$cond": {"if": {"$gt": ["$Population", 0]}, "then": {"$divide": ["$CO2", "$Population"]}, "else": 0}}
        }}
    ]

    results = collection.aggregate(pipeline)

    df = pd.DataFrame(list(results))

    df.drop(columns=['ISO_Code'], inplace=True)

    scaler = MinMaxScaler()
    df[['Population', 'CO2', 'CO2_per_capita']] = scaler.fit_transform(df[['Population', 'CO2', 'CO2_per_capita']])

    df.to_csv("co2_emission_preprocessed.csv", index=False)
    print("Data preprocessing completed and saved to 'co2_emission_preprocessed.csv'.")

if __name__ == "__main__":
    process_co2_emission_data()
