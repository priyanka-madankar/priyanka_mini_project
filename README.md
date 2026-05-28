# Job Scam Detector

A Streamlit web application that analyzes job postings and detects whether they are likely legitimate or fraudulent.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [How It Works](#how-it-works)
- [Dataset Loading](#dataset-loading)
- [Model Details](#model-details)
- [Troubleshooting](#troubleshooting)
- [Deployment](#deployment)
- [License](#license)

## Project Overview

This project combines natural language processing and machine learning to determine whether a job posting contains indicators of fraud. The app reads job title and description text, performs text cleaning and TF-IDF feature extraction, then classifies postings using a Naive Bayes model.

## Features

- Loads training data from a local dataset file if available
- Falls back to a small internal demo dataset when no valid dataset is found
- Trains a `MultinomialNB` classifier on text features
- Calculates and displays model metrics: Accuracy, Precision, Recall, F1 Score
- Provides an interactive UI for entering or selecting job postings
- Detects suspicious keywords associated with scams
- Displays fraud probability and confidence scores
- Supports both CSV and Excel dataset formats

## Repository Structure

- `app.py` — Main Streamlit application and model training code
- `fake_job_postings.csv` — Primary dataset used by the app
- `FakeJobPostings.xlsx` — Alternate dataset file if available
- `requirements.txt` — Python dependency list
- `runtime.txt` — Python runtime version for deployment
- `README.md` — Project documentation

## Dependencies

This app requires Python and the packages listed in `requirements.txt`:

- `streamlit==1.45.1`
- `pandas==2.2.3`
- `scikit-learn==1.6.1`
- `openpyxl==3.1.5`
- `numpy==2.2.6`

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd priyanka
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

Start the Streamlit application:

```bash
streamlit run app.py
```

Then open the URL shown in the terminal, usually `http://localhost:8501`.

## How It Works

### App flow

1. The app searches for dataset files in the project directory.
2. Valid datasets are loaded and validated for required columns.
3. Text fields are cleaned and combined into a single training text column.
4. A TF-IDF vectorizer converts text into numeric features.
5. A Multinomial Naive Bayes classifier is trained and evaluated.
6. The UI lets users input new job posting text.
7. The trained model predicts whether the posting is fraudulent.
8. Suspicious keywords are highlighted alongside the model result.

### Text processing

- Converts text to lowercase
- Removes non-alphabetic characters
- Uses TF-IDF to represent text as numeric features

## Dataset Loading

The app supports these dataset filenames in order of priority:

1. `FakeJobPostings.xlsx`
2. `FakeJobPostings .xlsx`
3. `fake_job_postings.csv`
4. `FakeJobPostings.csv`
5. `fake_job_postings.xlsx`

### Required dataset columns

The dataset must contain these columns:

- `title`
- `description`
- `fraudulent`

If a dataset file is missing, invalid, or missing required columns, the app will use a built-in demo dataset.

## Model Details

The app trains a `MultinomialNB` classifier using features from the combined job title and description text.

Performance metrics displayed in the UI include:

- Accuracy
- Precision
- Recall
- F1 Score

The model also calculates a fraud probability score and shows suspicious keyword matches to help explain the result.

## Troubleshooting

### App shows fallback dataset warning

If the app loads the built-in demo dataset, check:

- that the dataset file is present in the same folder as `app.py`
- that the file is one of the supported names
- that the dataset contains `title`, `description`, and `fraudulent`

### Dataset file format

- CSV files are read with UTF-8 encoding
- Excel files are read with `openpyxl`

### Streamlit errors

If `streamlit run app.py` fails, ensure the virtual environment is activated and dependencies are installed.

## Deployment

To deploy the app to Streamlit Cloud or a similar hosting service:

1. Push the repository to GitHub.
2. Ensure `app.py`, `requirements.txt`, and the dataset file are included.
3. Connect the repo to Streamlit Cloud and deploy.

## License

This repository is provided as-is for demo and educational purposes.
