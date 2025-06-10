from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load player data
df = pd.read_csv("data/nba_fantasy_stats.csv")
drafted_players: List[str] = []
scoring_weights = {
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


def calculate_fantasy_score(row, weights):
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
        row["BLK"] * weights["STL"] +
        row["TOV"] * weights["TOV"]
    )


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    available_df = df[~df["Player"].isin(drafted_players)].copy()
    available_df["FantasyScore"] = available_df.apply(lambda row: calculate_fantasy_score(row, scoring_weights), axis=1)
    sorted_df = available_df.sort_values(by="FantasyScore", ascending=False)

    def top_by_position(pos_keyword):
        return sorted_df[sorted_df["Pos"].str.contains(pos_keyword)].head(5)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "players": sorted_df.head(15).to_dict(orient="records"),
        "top_guards": top_by_position("G").to_dict(orient="records"),
        "top_forwards": top_by_position("F").to_dict(orient="records"),
        "top_centers": top_by_position("C").to_dict(orient="records"),
        "weights": scoring_weights
    })


@app.post("/draft")
def draft_player(player_name: str = Form(...)):
    drafted_players.append(player_name)
    return RedirectResponse(url="/", status_code=303)


@app.post("/update-scoring")
def update_scoring(
    points: float = Form(...),
    field_goal_made: float = Form(...),
    field_goal_attempted: float = Form(...),
    free_throw_made: float = Form(...),
    free_throw_attempted: float = Form(...),
    three_point_made: float = Form(...),
    rebounds: float = Form(...),
    assists: float = Form(...),
    steals: float = Form(...),
    blocks: float = Form(...),
    turnovers: float = Form(...)
):
    scoring_weights.update({
        "PTS": points,
        "FG": field_goal_made,
        "FGA": field_goal_attempted,
        "FT": free_throw_made,
        "FTA": free_throw_attempted,
        "3P": three_point_made,
        "TRB": rebounds,
        "AST": assists,
        "STL": steals,
        "BLK": blocks,
        "TOV": turnovers
    })
    return RedirectResponse(url="/", status_code=303)
