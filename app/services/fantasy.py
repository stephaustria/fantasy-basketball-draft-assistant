import pandas as pd
import os

csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "nba_fantasy_stats.csv")
df = pd.read_csv(csv_path)
