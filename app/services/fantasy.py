import pandas as pd
from typing import List
import os
from app.models.scoring import default_scoring_weights

csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "nba_fantasy_stats.csv")
df = pd.read_csv(csv_path)

drafted_players: List[str] = []
scoring_weights = default_scoring_weights.copy()
