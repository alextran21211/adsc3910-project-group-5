# Analyzing CO₂ Emissions: Global Patterns and Insights
  

This repository contains all the necessary code, data, models, and documentation for ADSC 3910 Group 5's Data Science Project. It follows a well-organized structure to ensure reproducibility, collaboration, and efficient development. Below you'll find a comprehensive guide to setting up, using, and contributing to the project.
## Table of Contents

- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Data Description](#data-description)
- [Usage](#usage)
- [Reports](#reports)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

## Project Overview

The primary goal of this project is to analyze global CO2 emissions, focusing on trends and contributions from different energy sources across countries and regions. By examining historical data from 1750 to 2022, we aim to identify key contributors to emissions, assess the impact of various energy sources—such as coal, oil, gas, and cement—and explore per capita emissions to provide a fair comparison of contributions across nations. This analysis will help uncover patterns, track progress over time, and provide insights to guide effective climate policies.

## Directory Structure

```bash
ADSC3910-PROJECT-GROUP-5/
├── data/
│   ├── external/        # Data from third-party sources
│   ├── interim/         # Intermediate datasets used during data processing
│   ├── processed/       # Final cleaned data ready for modeling
│   └── raw/             # Original, unmodified datasets
├── docs/                # Documentation files (code of conduct, teamwork contract, etc.)
│   ├── .gitkeep         
│   ├── code of conduct  # Rules for collaboration within the project
│   ├── credentials_mongodb.json # MongoDB credentials file
│   ├── data-eda.ipynb   # Exploratory Data Analysis notebook
│   └── teamwork contract # Agreement for teamwork management         
├── notebooks/           # Jupyter notebooks for analysis and preprocessing
│   ├── .gitkeep         
│   ├── co2_emission_preprocessed.csv # Preprocessed dataset used for analysis
│   ├── data_analysis.ipynb  # Main analysis notebook
│   └── data_preprocessing.ipynb # Data cleaning and transformation steps
├── py_scripts/          # Python scripts for running the project
├── references/          # Relevant papers, articles, or external documentation
│   └── .gitkeep         
├── reports/             # Generated reports and figures
│   ├── figures/         # Plots and figures for the final report
│   └── .gitkeep         
├── .gitignore           # Files and directories to be ignored by Git
├── environment.yml      # Conda environment dependencies
```

## Setup and Installation
### 1. Clone the Repository  
First, clone the project to your local machine:  

```bash
git clone https://github.com/TRU-PBADS/adsc3910-project-group-5.git
cd adsc3910-project-group-5
```

### 2. Set up environment

```bash
conda env create -f environment.yml
conda activate adsc3910-project-group-5
```

### Add your MongoDB credentials

Update the docs/credentials_mongodb.json file with your MongoDB access details.

## Usage

### Preprocess the data
Run the data_preprocessing.ipynb notebook from the notebooks/ directory to clean and prepare the dataset. This notebook preprocesses CO₂ emission data by retrieving it from MongoDB, cleaning missing values, and creating a structured dataset. Key features include emissions from various sources, population, and CO2_per_capita. The data is standardized using MinMax scaling and saved as a CSV file (co2_emission_preprocessed.csv) for analysis.


### Explanatory Data Analysis
Use the data-eda.ipynb notebook in the notebook/ directory to visualize patterns and trends. This generates plots for CO2 emission overtime, top 5 countries emitting CO2, sources of CO2.


### Analysis
1. Run the *regression_analysis.ipynb* - This notebook performs regression analysis on CO₂ emissions per capita. A linear regression model is built and evaluated using metrics like Mean Squared Error (MSE) and R². Additionally, polynomial regression is applied to capture nonlinear trends, with results compared to the linear model.

2. Run *time_series_analysis.ipynb* - This notebook performs time series analysis of CO₂ emissions per capita for the top 10 and bottom 10 countries based on their average emissions. It calculates a 10-year moving average to smooth trends over time and visualizes both raw data and moving averages using line plots. The analysis highlights trends and patterns in emissions for high- and low-emitting countries.

3. Run *CO2_sources_analysis.ipynb* - This notebook conducts a comprehensive analysis of CO₂ emissions, including:
- Emission Trends by Source: Examining historical trends in CO₂ emissions from coal, oil, gas, and cement.
- Per Capita Analysis: Calculating and visualizing average CO₂ emissions per capita over time.
- Correlation Analysis: Using a heatmap to identify relationships between features like emissions and population.
- Feature Importance: Training a Random Forest model to evaluate the relative contribution of factors like energy sources and population to total CO₂ emissions.
- Clustering: Applying K-means clustering to group countries based on emissions patterns, visualized through scatter plots.
- Country Group Comparisons: Comparing CO₂ emissions for income-based country groups to understand disparities.

The insights derived help identify key contributors and trends in global CO₂ emissions.



## Reports
All figures, analysis outputs, and summaries will be available in the reports/ directory.

Plots generated from EDA can be found in /plots directory

Use makefile commands to generate or automate certain steps:

```bash
make preprocess
make report
```

## Contributing
Please follow the code of conduct and ensure all contributions align with the agreed teamwork contract. If you wish to contribute:

-  Fork the repository.
-  Create a feature branch (git checkout -b feature/your-feature-name).
-  Commit your changes (git commit -m "Add feature").
-  Push to your branch (git push origin feature/your-feature-name).
-  Open a Pull Request.

## Acknowledgments

-  Thompson Rivers University (TRU) for course guidance and support
-  Group members for their collaborative efforts
