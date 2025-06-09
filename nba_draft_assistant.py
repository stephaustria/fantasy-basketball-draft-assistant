import pandas as pd


class FantasyDraftAssistant:
    def __init__(self, csv_path, use_custom_score=False):
        self.df = pd.read_csv("data/nba_fantasy_stats.csv")

        if use_custom_score:
            self.df['FantasyScore'] = self.df.apply(self.calculate_fantasy_score, axis=1)

        self.available_players = self.df.copy()

    def calculate_fantasy_score(self, row):
        return (row['PTS'] +
                2 * row['FG'] -
                row['FGA'] +
                row['FT'] -
                row['FTA'] +
                row['3P'] +
                row['TRB'] +
                2 * row['AST'] +
                4 * row['STL'] +
                4 * row['BLK'] -
                2 * row['TOV'])

    def exclude_drafted_players(self, drafted_players):
        """Removes drafted players from the available player pool."""
        self.available_players = self.available_players[~self.available_players['Player'].isin(drafted_players)]

    def recommend_players(self, top_n=10, position=None):
        """Returns top N players (optionally filtered by position)."""
        candidates = self.available_players
        if position:
            candidates = candidates[candidates['Pos'].str.contains(position, case=False, na=False)]

        recommended = candidates.sort_values(by='FantasyScore', ascending=False).head(top_n)
        return recommended[['Player', 'Team', 'Pos', 'FantasyScore']]


# -------------------------------
# Example usage:
# -------------------------------
if __name__ == "__main__":
    # Load data
    assistant = FantasyDraftAssistant("fantasy_players.csv", use_custom_score=True)

    # List of already drafted players
    drafted_players = [
        "Nikola Jokic",
        "Luka Doncic"
    ]

    assistant.exclude_drafted_players(drafted_players)

    # Show top 10 overall recommendations
    print("\n📋 Top 10 Available Players:")
    print(assistant.recommend_players(top_n=10))

    # Show top 5 guards (e.g. "G" or "PG", "SG")
    print("\n🛡 Top 5 Guards:")
    print(assistant.recommend_players(top_n=5, position="G"))

    # Show top 5 forwards
    print("\n🏀 Top 5 Forwards:")
    print(assistant.recommend_players(top_n=5, position="F"))

    # Show top 5 centers
    print("\n🐶 Top 5 Centers:")
    print(assistant.recommend_players(top_n=5, position="C"))
