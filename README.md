This repository contains all the necessary code, data, models, and documentation for ADSC 3910 Group 5's Data Science Project. It follows a well-organized structure to ensure reproducibility, collaboration, and efficient development. Below you'll find a comprehensive guide to setting up, using, and contributing to the project.
## Table of Contents

- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Data Description](#data-description)
- [Usage](#usage)
- [Reports](#reports)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Project Overview
The primary goal of this project is to analyze global CO2 emissions on a per capita basis. By focusing on emissions normalized to population size, we aim to uncover trends and patterns across countries, regions, and income groups. This will allow us to identify key contributors to emissions, track progress over time, and assess the fairness and effectiveness of climate policies.

## Directory Structure

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
├── models/              # Trained models and serialized model files
├── notebooks/           # Jupyter notebooks for analysis and preprocessing
│   ├── .gitkeep         
│   ├── co2_emission_preprocessed.csv # Preprocessed dataset used for analysis
│   ├── data_analysis.ipynb  # Main analysis notebook
│   └── data_preprocessing.ipynb # Data cleaning and transformation steps
├── references/          # Relevant papers, articles, or external documentation
│   └── .gitkeep         
├── reports/             # Generated reports and figures
│   ├── figures/         # Plots and figures for the final report
│   └── .gitkeep         
├── .gitignore           # Files and directories to be ignored by Git
├── environment.yml      # Conda environment dependencies
└── makefile             # Automate tasks like data download, preprocessing, etc.


## Setup and Installation
### 1. Clone the Repository  
First, clone the project to your local machine:  

```bash
git clone https://github.com/your-username/adsc_3910_group_5.git
cd adsc_3910_group_5
```

### 2. Set up a virtual environment (recommended):

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```


