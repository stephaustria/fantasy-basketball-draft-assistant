from typing import Dict

# Default scoring weights
default_scoring_weights: Dict[str, float] = {
    "PTS": 1.0,
    "FG": 2.0,
    "FGA": -1.0,
    "FT": 1.0,
    "FTA": -1.0,
    "3P": 1.0,
    "TRB": 1.0,
    "AST": 2.0,
    "STL": 4.0,
    "BLK": 4.0,
    "TOV": -2.0
}


# Calculate fantasy score for a player row
def calculate_fantasy_score(row, weights: Dict[str, float]) -> float:
    return (
            row["PTS"] * weights["PTS"] +
            row["FG"] * weights["FG"] +
            row["FGA"] * weights["FGA"] +
            row["FT"] * weights["FT"] +
            row["FTA"] * weights["FTA"] +
            row["3P"] * weights["3P"] +
            row["TRB"] * weights["TRB"] +
            row["AST"] * weights["AST"] +
            row["STL"] * weights["STL"] +
            row["BLK"] * weights["BLK"] +
            row["TOV"] * weights["TOV"]
    )
