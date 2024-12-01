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
│   ├── project_proposal.pdf #the final project proposal
│   └── teamwork contract # Agreement for teamwork management         
├── notebooks/           # Jupyter notebooks for analysis and preprocessing
│   ├── .gitkeep         
│   ├── analysis_co2_sources.ipynb  
|   ├── data_preprocessing.ipynb
|   ├── eda.ipynb
|   ├── mlflow_models.ipynb
|   ├── regression_analysis.ipynb
│   └── time_series_analysis.ipynb
├── plots/               # plots to understand the emissions through visualization
├── py_scripts/          # Python scripts for running the project
│   ├── _init_.py
│   ├── data_preprocessing.py
│   ├── eda.py
│   ├── regression_analysis.py
│   └── time_series_analysis.py
├── references/          # Relevant papers, articles, or external documentation
│   └── .gitkeep         
├── reports/             # Generated reports and figures
│   ├── figures/         # Plots and figures for the final report
│   └── .gitkeep
├── tests/
│   ├── data_preprocessing_tests.py
│   ├── eda_tests.py
│   ├── regression_analysis_tests.py
│   └── time_series_analysis_tests.py
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
### 1. How to run Notebooks

Browse to the ```notebooks\``` folder, there are in total six notebooks:

**A.** ```notebooks\analysis_co2_sources.ipynb```: The analysis examines CO₂ emission trends, key sources, and per capita metrics. It highlights coal as the top contributor, clusters countries by emission patterns, and reveals income-based disparities, with high-income nations reducing emissions and low-income nations facing clean energy challenges. Insights guide sustainable policies. We'll utilize various MongoDB operators to clean and transform data before it’s analyzed in PySpark. 

We have tested this script on Databrick Pyspark and then on our local system using Jupyter notebook.


**STEP 1 :** To test the notebook, go to ```notebooks\analysis_co2_sources.ipynb``` using your code editing platforms like **pycharm** or **visual studio code** or **jupyter notebook**

**STEP 2 :** Select the existing environment for kernel selection.

**STEP 3 :** Run each cell to see the what are the functions doing!

---

**B.** ```notebooks\data_preprocessing.ipynb``` : This notebook outlines the preprocessing steps necessary to clean and prepare the text data from our MongoDB collection for further analysis and modeling. We will focus on the 'body' field, addressing various forms of redundant data such as HTML tags, URLs, emojis, stopwords, and punctuations.

**STEP 1 :** To test the notebook, go to ```notebooks\data_preprocessing.ipynb``` using your code editing platforms like **pycharm** or **visual studio code** or **jupyter notebook**

**STEP 2 :** Select the existing environment "group2_env" as kernel selection. As we did for notebook mentioned in *A* point above.

**STEP 3 :** Run each cell to see the what are the functions doing!

---

**C.** ```notebooks\eda.ipynb``` : This notebook demonstrates the meaningful application of MongoDB's query language for data analysis. We'll utilize various MongoDB operators to clean and transform data before it’s analyzed in PySpark. 

We have tested this script on Databrick Pyspark and then on our local system using Jupyter notebook.


**STEP 1 :** To test the notebook, go to ```notebooks\eda.ipynb``` using your code editing platforms like **pycharm** or **visual studio code** or **jupyter notebook**

**STEP 2 :** Select the existing environment for kernel selection.

**STEP 3 :** Run each cell to see the what are the functions doing!

---

**D.** ```notebooks\mlflow_models.ipynb``` : This notebook compares the model's performance to get insight into the best-performing model.

**STEP 1 :** To test the notebook, go to ```notebooks\mlflow_models.ipynb``` using your code editing platforms like **pycharm** or **visual studio code** or **jupyter notebook**

**STEP 2 :** Select the existing environment as kernel selection.

**STEP 3 :** Run each cell to see the what are the functions doing!

---

**E.** ```notebooks\regression_analysis.ipynb``` : This notebook performs regression analysis on CO₂ emissions per capita. A linear regression model is built and evaluated using metrics like Mean Squared Error (MSE) and R². Additionally, polynomial regression is applied to capture nonlinear trends, with results compared to the linear model.

**STEP 1 :** To test the notebook, go to ```notebooks\regression_analysis.ipynb``` using your code editing platforms like **pycharm** or **visual studio code** or **jupyter notebook**

**STEP 2 :** Select the existing environment as kernel selection.

**STEP 3 :** Run each cell to see the what are the functions doing!

--- 

**F.** ```notebooks\time_series_analysis.ipynb``` : This notebook performs time series analysis of CO₂ emissions per capita for the top 10 and bottom 10 countries based on their average emissions. It calculates a 10-year moving average to smooth trends over time and visualizes both raw data and moving averages using line plots. The analysis highlights trends and patterns in emissions for high- and low-emitting countries.

**STEP 1 :** To test the notebook, go to ```notebooks\time_series_analysis.ipynb``` using your code editing platforms like **pycharm** or **visual studio code** or **jupyter notebook**

**STEP 2 :** Select the existing environment as kernel selection.

**STEP 3 :** Run each cell to see the what are the functions doing!
---

### 2. How to run python scripts and unit test

**A. Data Preprocessing Script :**  ```py_scripts\data_preprocessing.py``` is all about data preprocessing step, it is very important for next steps in data analysis

To run this script, first open the terminal and navigate to the location of the GitHub repository folder you just cloned, then type this command go py_scripts folder:

```bash
>> cd py_scripts
```

After that run this command to run data preprocessing py script:

```bash
>> python ./data_preprocessing.py
```

***Run Data Preprocessing Unit Test***  
To run data preprocessing unit test, you need to go back to main GitHub reporsitory folder, and then go to tests folder:  

Used this command to go back to main folder of repo:  

```bash
>> cd ..
```
And use this command to go to tests folder:  

```bash
>> cd tests
```

To run unit test for data preprocessing, you run this command below:  

```bash
>> python -m unittest data_preprocessing_tests.py
```

**B. EDA Script :**  ```py_scripts\eda.py``` is all about data analysis that was done in the notebook ```notebooks\eda.ipynb```.

To run the eda via terminal, use the following code:
Note: you need to stay py_scripts folder location to run this  

```bash
>> python ./eda.py
```

***Run EDA Unit Test***  
To run EDA unit test, you also need to stay main GitHub reporsitory folder, and then go to tests folder:  

Used this command to go back to main folder of repo:  

```bash
>> cd ..
```
And use this command to go to tests folder:  

```bash
>> cd tests
```

To run unit test for data preprocessing, you run this command below:  

```bash
>> python -m unittest data_preprocessing_tests.py
```

**C. Regression Analysis Script :**  ```py_scripts\regression_analysis.py``` is all about regression analysis of the project

To run the regression analysis script via terminal, use the following code:
Note: you need to stay py_scripts folder location to run this  

```bash
>> python ./regression_analysis.py
```

***Run Regression Analysis Unit Test***  
To run Regression Analysis unit test, you also need to stay main GitHub reporsitory folder, and then go to tests folder:  

Used this command to go back to main folder of repo:  

```bash
>> cd ..
```
And use this command to go to tests folder:  

```bash
>> cd tests
```

To run unit test for data preprocessing, you run this command below:  

```bash
>> python -m unittest regression_analysis_tests.py
```

**D. Time Series Analysis Script :**  ```py_scripts\regression_analysis.py``` is all about time series analysis of the project

To run the regression analysis script via terminal, use the following code:  
Note: you need to stay py_scripts folder location to run this  

```bash
>> python ./time_series_analysis.py
```

***Run Time Series Analysis Unit Test***  
To run Time Series Analysis unit test, you also need to stay main GitHub reporsitory folder, and then go to tests folder:  

Used this command to go back to main folder of repo:  

```bash
>> cd ..
```
And use this command to go to tests folder:  

```bash
>> cd tests
```

To run unit test for data preprocessing, you run this command below:  

```bash
>> python -m unittest time_series_analysis_tests.py
```

**All the plots that are going to popup during the eda, will also be saved in ```reports\figures\```.**

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
