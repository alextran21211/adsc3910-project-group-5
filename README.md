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
The primary goal of this project is to analyze global CO2 emissions on a per capita basis. By focusing on emissions normalized to population size, we aim to uncover trends and patterns across countries, regions, and income groups. This will allow us to identify key contributors to emissions, track progress over time, and assess the fairness and effectiveness of climate policies.

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
├── models/              # Trained models and serialized model files
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
└── makefile             # Automate tasks like data download, preprocessing, etc.
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
Run the data_preprocessing.ipynb notebook from the notebooks/ directory to clean and prepare the dataset.

### Explanatory Data Analysis
Use the data-eda.ipynb notebook in the docs/ directory to visualize patterns and trends.

### EDA with some visualizations
Run eda.py script in py_script folder from your environment to get some visualizations of the data.
When you close the graph, it will automatically open another graph.

`>python ./py_scripts/eda.py`

### Model Training
Save trained models in the models/ directory. You can extend the makefile to automate the model training process.

### Generate reports and figures
Store figures in the reports/figures/ directory and use them in the final report.

## Reports
All figures, analysis outputs, and summaries will be available in the reports/ directory.
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
