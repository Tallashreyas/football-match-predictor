import joblib
import numpy as np
import pandas as pd
import torch

from collections import defaultdict

from model import FootballPredictor
from feature_utils import (
    LAST_N_MATCHES,
    get_team_stats,
    get_match_result,
    add_match
)

checkpoint = torch.load("../models/football_model.pth")

model = FootballPredictor(input_size = 16)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

model.eval()

scaler = joblib.load("../models/scaler.pkl")


df = pd.read_csv("../data/processed/clean_matches.csv")

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date").reset_index(drop=True)

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

print("\nAvailable Teams:\n")

for team in teams:
    print(team)


home_team = input("\nEnter Home Team: ")

away_team = input("Enter Away Team: ")


if home_team not in team_history:
    print("Invalid Home Team!")
    exit()

if away_team not in team_history:
    print("Invalid Away Team!")
    exit()


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

print("\nPrediction")
print("----------")
print(labels[prediction])

print("\nProbabilities")

print(f"Home Win : {probabilities[0][0]*100:.2f}%")
print(f"Draw     : {probabilities[0][1]*100:.2f}%")
print(f"Away Win : {probabilities[0][2]*100:.2f}%")






