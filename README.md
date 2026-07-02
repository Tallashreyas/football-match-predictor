# ⚽ Football Match Outcome Predictor

A machine learning project that predicts the outcome of English Premier League football matches using historical match statistics and a neural network built with **PyTorch**.

The project processes historical match data, engineers team performance features, trains a classification model, and predicts whether a future match will result in a **Home Win**, **Draw**, or **Away Win**.

---

## Features

* Historical match data preprocessing
* Feature engineering using previous team performances
* Neural network classifier implemented in PyTorch
* Model training with learning rate scheduling
* Model evaluation on unseen data
* Interactive match prediction from the command line
* Feature scaling for improved model performance

---

## Tech Stack

* Python
* PyTorch
* Pandas
* NumPy
* Scikit-learn
* Joblib

---

## Dataset

The project uses historical **English Premier League** match data from multiple seasons.

Included seasons:

* 2020–21
* 2021–22
* 2022–23
* 2023–24
* 2024–25
* 2025–26

The raw data is stored in:

```text
data/raw/
```

Processed datasets are stored in:

```text
data/processed/
```

---

## Feature Engineering

For every match, the model only uses information available **before** that match was played to avoid data leakage.

Features include:

* Team win rate
* Average goals scored
* Average goals conceded
* Goal difference
* Last five match points
* Home form
* Away form
* Average shots
* Current winning/losing streak

These features are generated in chronological order so future information is never used.

---

## Model Architecture

The prediction model is a feed-forward neural network built with PyTorch.

Architecture:

```text
Input Features
      ↓
Linear (128)
      ↓
ReLU
      ↓
Dropout (0.3)
      ↓
Linear (64)
      ↓
ReLU
      ↓
Dropout (0.2)
      ↓
Linear (3 Outputs)
```

Output classes:

* Home Win
* Draw
* Away Win

---

## Project Structure

```text
football-match-predictor/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── data_exploration.ipynb
│
├── src/
│   ├── dataset.py
│   ├── feature_engineering.py
│   ├── feature_utils.py
│   ├── model.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/football-match-predictor.git
```

Navigate into the project:

```bash
cd football-match-predictor
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### 1. Generate Features

```bash
python src/feature_engineering.py
```

---

### 2. Train the Model

```bash
python src/train.py
```

The trained model is saved in the `models/` directory.

---

### 3. Evaluate Performance

```bash
python src/evaluate.py
```

---

### 4. Predict a Match

```bash
python src/predict.py
```

Example:

```text
Enter Home Team: Arsenal
Enter Away Team: Liverpool
```

Output:

```text
Prediction
----------
Home Win

Probabilities

Home Win : 63.45%
Draw     : 21.18%
Away Win : 15.37%
```

---

## Machine Learning Pipeline

```text
Historical Match Data
          │
          ▼
Data Cleaning
          │
          ▼
Feature Engineering
          │
          ▼
Feature Scaling
          │
          ▼
Neural Network Training
          │
          ▼
Model Evaluation
          │
          ▼
Match Outcome Prediction
```

---

## Future Improvements

* Add more advanced team statistics (Expected Goals, Possession, Pass Accuracy)
* Include player injury and suspension information
* Train on multiple football leagues
* Hyperparameter optimization
* Experiment with LSTM or Transformer-based models
* Build a web interface using FastAPI and React
* Deploy the model as a web application

---

## License

This project is intended for educational and learning purposes.
