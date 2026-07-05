import joblib
import pandas as pd
import torch

from collections import defaultdict

from model import FootballPredictor
from feature_utils import (
    get_team_stats,
    get_match_result,
    add_match
)

# -----------------------------
# Load Model
# -----------------------------

checkpoint = torch.load("../models/football_model.pth", map_location="cpu")

model = FootballPredictor(input_size=16)

model.load_state_dict(checkpoint["model_state_dict"])

model.eval()

# -----------------------------
# Load Scaler
# -----------------------------

scaler = joblib.load("../models/scaler.pkl")

# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv("../data/processed/clean_matches.csv")

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date").reset_index(drop=True)

# -----------------------------
# Build Team History
# -----------------------------

team_history = defaultdict(list)

for _, row in df.iterrows():

    home = row["HomeTeam"]
    away = row["AwayTeam"]

    home_result, away_result = get_match_result(row)

    add_match(
        team_history[home],
        home_result,
        row["FTHG"],
        row["FTAG"],
        row["HS"],
        True
    )

    add_match(
        team_history[away],
        away_result,
        row["FTAG"],
        row["FTHG"],
        row["AS"],
        False
    )

teams = sorted(team_history.keys())

# -----------------------------
# Prediction Function
# -----------------------------

def predict_match(home_team, away_team):

    if home_team not in team_history:
        raise ValueError("Invalid Home Team")

    if away_team not in team_history:
        raise ValueError("Invalid Away Team")

    home_stats = get_team_stats(team_history[home_team])
    away_stats = get_team_stats(team_history[away_team])

    features = [[
        home_stats["win_rate"],
        away_stats["win_rate"],

        home_stats["avg_goals"],
        away_stats["avg_goals"],

        home_stats["last5_points"],
        away_stats["last5_points"],

        home_stats["home_form"],
        away_stats["away_form"],

        home_stats["goal_difference"],
        away_stats["goal_difference"],

        home_stats["avg_conceded"],
        away_stats["avg_conceded"],

        home_stats["avg_shots"],
        away_stats["avg_shots"],

        home_stats["streak"],
        away_stats["streak"]
    ]]

    features = scaler.transform(features)

    features = torch.tensor(
        features,
        dtype=torch.float32
    )

    with torch.no_grad():

        outputs = model(features)

        probabilities = torch.softmax(outputs, dim=1)

        prediction = torch.argmax(probabilities, dim=1).item()

    labels = {
        0: "Home Win",
        1: "Draw",
        2: "Away Win"
    }

    return {

        "prediction": labels[prediction],

        "probabilities": {

            "home": round(float(probabilities[0][0]) * 100, 2),
            "draw": round(float(probabilities[0][1]) * 100, 2),
            "away": round(float(probabilities[0][2]) * 100, 2)

        },

        "home_stats": home_stats,

        "away_stats": away_stats

    }


# -----------------------------
# Run from Terminal
# -----------------------------

if __name__ == "__main__":

    print("\nAvailable Teams:\n")

    for team in teams:
        print(team)

    home_team = input("\nEnter Home Team: ")

    away_team = input("Enter Away Team: ")

    result = predict_match(home_team, away_team)

    print("\nPrediction")
    print("----------")
    print(result["prediction"])

    print("\nProbabilities")

    print(f'Home Win : {result["probabilities"]["home"]:.2f}%')
    print(f'Draw     : {result["probabilities"]["draw"]:.2f}%')
    print(f'Away Win : {result["probabilities"]["away"]:.2f}%')