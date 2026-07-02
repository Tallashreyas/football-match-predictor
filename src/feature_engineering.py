import pandas as pd
from collections import defaultdict

#exactly as the name says
def get_team_stats(history):
    if len(history) == 0:
        return {
            "win_rate": 0,
            "avg_goals": 0,
            "avg_conceded": 0,
            "avg_shots": 0,
            "streak": 0
        }
    recent = history[-5:]

    # choosing last 5 mathces because teams performance depends on current 
    #play not how they played months before
    wins = sum(match["result"] == "W" for match in recent)
    win_rate = wins / len(recent)


    #finding avg shots and goals etc
    avg_goals = sum(match["goals_for"] for match in recent) / len(recent)
    avg_conceded = sum(match["goals_against"] for match in recent) / len(recent)
    avg_shots = sum(match["shots"] for match in recent) / len(recent)
    goal_difference = avg_goals - avg_conceded

    # finding streak since team with win streak 5 is stronger than
    # team with alternates between win and loss
    streak = 0
    for match in reversed(recent):
        if match["result"] == "W":
            if streak >= 0:
                streak += 1
            else:
                break
        elif match["result"] == "L":
            if streak <= 0:
                streak -= 1
            else:
                break
        else:
            break
    
    return {
        "win_rate": win_rate,
        "avg_goals": avg_goals,
        "avg_conceded": avg_conceded,
        "goal_difference": goal_difference,
        "avg_shots": avg_shots,
        "streak": streak
    }



# load up all the cleaned data in data_exploration.py 
df = pd.read_csv("../data/processed/clean_matches.csv")

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date").reset_index(drop=True)


#creating dictionary to store data regarding the matches played until now
#remember to not include todays match couse it will mean data leaked
team_history = defaultdict(list)

#store row features
feature_rows = []


#We first make sure we can read one match correctly before writing more complex logic.
for _, row in df.iterrows():

    home = row["HomeTeam"]
    away = row["AwayTeam"]

    if len(team_history[home]) < 5 or len(team_history[away]) < 5:
        # Update home history
        if row["FTR"] == "H":
            home_result = "W"
            away_result = "L"
        elif row["FTR"] == "A":
            home_result = "L"
            away_result = "W"
        else:
            home_result = "D"
            away_result = "D"

        team_history[home].append({
            "result": home_result,
            "goals_for": row["FTHG"],
            "goals_against": row["FTAG"],
            "shots": row["HS"]
        })

        team_history[away].append({
            "result": away_result,
            "goals_for": row["FTAG"],
            "goals_against": row["FTHG"],
            "shots": row["AS"]
        })

        continue

    home_stats = get_team_stats(team_history[home])
    away_stats = get_team_stats(team_history[away])

    #combine home team and away team stats
    feature_rows.append({
        "home_win_rate": home_stats["win_rate"],
        "away_win_rate": away_stats["win_rate"],

        "home_avg_goals": home_stats["avg_goals"],
        "away_avg_goals": away_stats["avg_goals"],

        "home_goal_difference": home_stats["goal_difference"],
        "away_goal_difference": away_stats["goal_difference"],

        "home_avg_conceded": home_stats["avg_conceded"],
        "away_avg_conceded": away_stats["avg_conceded"],

        "home_avg_shots": home_stats["avg_shots"],
        "away_avg_shots": away_stats["avg_shots"],

        "home_streak": home_stats["streak"],
        "away_streak": away_stats["streak"],

        "target": row["FTR"]
    })

    if row["FTR"] == "H":
        home_result = "W"
        away_result = "L"
    elif row["FTR"] == "A":
        home_result = "L"
        away_result = "W"
    else:
        home_result = "D"
        away_result = "D"

    team_history[home].append({
        "result": home_result,
        "goals_for": row["FTHG"],
        "goals_against": row["FTAG"],
        "shots": row["HS"]
    })

    team_history[away].append({
        "result": away_result,
        "goals_for": row["FTAG"],
        "goals_against": row["FTHG"],
        "shots": row["AS"]
    })

#read one match ->calc stats ->save features ->add curr match to history -> next match
features_df = pd.DataFrame(feature_rows)

features_df.to_csv("../data/processed/features.csv", index=False)

print(features_df.shape)

print(features_df.head())

print(features_df.describe())

print(features_df.isnull().sum())