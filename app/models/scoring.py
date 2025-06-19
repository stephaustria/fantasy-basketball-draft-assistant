from typing import Dict


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
