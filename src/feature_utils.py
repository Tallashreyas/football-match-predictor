from collections import defaultdict
LAST_N_MATCHES = 5

def get_team_stats(history):
    recent = history[-LAST_N_MATCHES:]

    home_matches = [
        match for match in recent
        if match["is_home"]
    ]

    away_matches = [
        match for match in recent
        if not match["is_home"]
    ]

    home_form = sum(
        3 if match["result"] == "W"
        else 1 if match["result"] == "D"
        else 0
        for match in home_matches
    )

    away_form = sum(
        3 if match["result"] == "W"
        else 1 if match["result"] == "D"
        else 0
        for match in away_matches
    )

    # choosing last 5 mathces because teams performance depends on current 
    #play not how they played months before
    wins = sum(match["result"] == "W" for match in recent)
    win_rate = wins / len(recent)
    last5_points = sum(
        3 if match["result"] == "W"
        else 1 if match["result"] == "D"
        else 0
        for match in recent
    )


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
        "streak": streak,
        "last5_points": last5_points,
        "home_form": home_form,
        "away_form": away_form
    }


def get_match_result(row):

    if row["FTR"] == "H":
        return "W", "L"

    elif row["FTR"] == "A":
        return "L", "W"

    return "D", "D"



def add_match(history, result, gf, ga, shots, is_home):

    history.append({
        "result": result,
        "goals_for": gf,
        "goals_against": ga,
        "shots": shots,
        "is_home": is_home
    })
