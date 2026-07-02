import pandas as pd
from collections import defaultdict

from feature_utils import (
    LAST_N_MATCHES,
    get_team_stats,
    get_match_result,
    add_match
)


# load up all the cleaned data in data_exploration.py 
def load_data():
    df = pd.read_csv("../data/processed/clean_matches.csv")
    return df

def save_dataset(df):
    df.to_csv(
        "../data/processed/features.csv",
        index=False
    )





#creating dictionary to store data regarding the matches played until now
#remember to not include todays match couse it will mean data leaked
def create_match_features(df):
    team_history = defaultdict(list)

    #store row features
    feature_rows = []


    #We first make sure we can read one match correctly before writing more complex logic.
    for _, row in df.iterrows():

        home = row["HomeTeam"]
        away = row["AwayTeam"]

        if len(team_history[home]) < 5 or len(team_history[away]) < 5:
            # Update home history
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

            continue

        home_stats = get_team_stats(team_history[home])
        away_stats = get_team_stats(team_history[away])

        #combine home team and away team stats
        feature_rows.append({
            "home_win_rate": home_stats["win_rate"],
            "away_win_rate": away_stats["win_rate"],

            "home_avg_goals": home_stats["avg_goals"],
            "away_avg_goals": away_stats["avg_goals"],

            "home_last5_points": home_stats["last5_points"],
            "away_last5_points": away_stats["last5_points"],

            "home_form": home_stats["home_form"],
            "away_form": away_stats["away_form"],

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

    return pd.DataFrame(feature_rows)


def main():

    df = load_data()

    df["Date"] = pd.to_datetime(df["Date"])

    df = df.sort_values("Date").reset_index(drop=True)

    features_df = create_match_features(df)

    save_dataset(features_df)

    print(features_df.shape)
    print(features_df.head())
    print(features_df.describe())
    print(features_df.isnull().sum())


if __name__ == "__main__":
    main()