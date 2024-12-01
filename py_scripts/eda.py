from pymongo import MongoClient  # import mongo client to connect
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

username = "alextran21211"
password = urllib.parse.quote("database12345")
host = "cluster0.zsych.mongodb.net"
url = f"mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority"

client = MongoClient(url)

db = client['group_5_project']
collection = db["co2_emission"]

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

df = pd.DataFrame(data)

# Data Cleaning and Transformation
print(df.isnull().sum()) 
df['Population'] = df['Population'].fillna(df['Population'].mean()) 
df['CO2'] = df['CO2'].fillna(df['CO2'].mean())  
df['CO2_per_capita'] = df['CO2'] / df['Population']
df.drop_duplicates(inplace=True)
df = df.drop(columns=['ISO_Code'])
print(df.head())

# 1. CO₂ Emissions Over Time
plt.figure(figsize=(12, 6))
sns.lineplot(data=df[df['Country'] == "Afghanistan"], x='Year', y='CO2', color="b")
plt.title("CO₂ Emissions Over Time for Afghanistan")
plt.xlabel("Year")
plt.ylabel("Total CO₂ Emissions")
plt.show()
plt.close()

# 2. CO₂ Emissions Per Capita Over Time
plt.figure(figsize=(12, 6))
sns.lineplot(data=df[df['Country'] == "Afghanistan"], x='Year', y='CO2_per_capita', color="g")
plt.title("CO₂ Emissions Per Capita Over Time for Afghanistan")
plt.xlabel("Year")
plt.ylabel("CO₂ Emissions Per Capita")
plt.show()
plt.close()

# 3. Population Growth Over Time
plt.figure(figsize=(12, 6))
sns.lineplot(data=df[df['Country'] == "Afghanistan"], x='Year', y='Population', color="purple")
plt.title("Population Growth Over Time for Afghanistan")
plt.xlabel("Year")
plt.ylabel("Population")
plt.show()
plt.close()

# 4. Relationship CO₂ Emissions vs. Population (Scatter Plot)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Population', y='CO2', hue='Country', palette="coolwarm", legend=None)
plt.title("Relationship Between Population and CO₂ Emissions")
plt.xlabel("Population")
plt.ylabel("Total CO₂ Emissions")
plt.show()
plt.close()

# 5. Correlation Heatmap
plt.figure(figsize=(8, 6))
correlation_matrix = df[['Population', 'CO2', 'CO2_per_capita']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap="YlGnBu", fmt=".2f")
plt.title("Correlation Matrix")
plt.show()
plt.close()

# 6. CO₂ Emissions Over Time for Different Countries
plt.figure(figsize=(14, 8))
sns.lineplot(data=df, x='Year', y='CO2', hue='Country', legend='full', palette='tab10')
plt.title("CO₂ Emissions Over Time for Each Country")
plt.xlabel("Year")
plt.ylabel("Total CO₂ Emissions")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
plt.close()

# 7. Top 5 CO₂ Emissions Per Capita Over Time
non_countries = ["World", "High-income countries", "Low-income countries", "Upper-middle-income countries", 
                 "Lower-middle-income countries", "Africa", "Europe", "Asia", "Oceania", "Americas", "North America",
                 "South America", "Asia (excl. China and India)", "Europe (excl. EU-27)", "Europe (excl. EU-28)", "North America (excl. USA)" ]
df_filtered = df[~df['Country'].isin(non_countries)]
top_countries = df_filtered.groupby('Country')['CO2'].mean().nlargest(5).index

plt.figure(figsize=(14, 8))
sns.lineplot(data=df_filtered[df_filtered['Country'].isin(top_countries)], x='Year', y='CO2_per_capita', hue='Country', palette='Dark2')
plt.title("CO₂ Emissions Per Capita Over Time for Top 5 CO₂ Emitting Countries")
plt.xlabel("Year")
plt.ylabel("CO₂ Emissions Per Capita")
plt.legend(title="Country", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
plt.close()

# 8. Heatmap of CO₂ Emissions Over Time for Selected Countries
selected_countries = ["Afghanistan", "Brazil", "China", "India", "United States"]
df_selected = df[df['Country'].isin(selected_countries)]
heatmap_data = df_selected.pivot_table(index='Country', columns='Year', values='CO2', aggfunc='mean').fillna(0)

plt.figure(figsize=(14, 8))
sns.heatmap(heatmap_data, cmap='YlGnBu', cbar_kws={'label': 'CO₂ Emissions'}, fmt=".1f")
plt.title("CO₂ Emissions Over Time for Selected Countries")
plt.xlabel("Year")
plt.ylabel("Country")
plt.show()
plt.close()

# 9. Boxplot of CO₂ Emissions Per Capita by Country for Selected Countries
plt.figure(figsize=(12, 8))
sns.boxplot(data=df_selected, x='Country', y='CO2_per_capita', palette="Set3")
plt.title("Distribution of CO₂ Emissions Per Capita by Country")
plt.xlabel("Country")
plt.ylabel("CO₂ Emissions Per Capita")
plt.show()
plt.close()

# 10. Facet Grid of CO₂ Emissions Over Time for Selected Countries
g = sns.FacetGrid(df_selected, col="Country", col_wrap=3, height=4, aspect=1.5)
g.map(sns.lineplot, "Year", "CO2", color="b")
g.set_titles("{col_name}")
g.set_axis_labels("Year", "Total CO₂ Emissions")
g.fig.suptitle("CO₂ Emissions Over Time by Country", y=1.05)
plt.show()
