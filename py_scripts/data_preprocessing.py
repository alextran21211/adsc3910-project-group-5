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