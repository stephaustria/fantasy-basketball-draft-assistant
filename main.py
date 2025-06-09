from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load player data
df = pd.read_csv("data/nba_fantasy_stats.csv")
drafted_players = set()
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
    "TOV": -1.0
}


def compute_scores():
    temp_df = df[~df["Player"].isin(drafted_players)].copy()
    temp_df["FantasyScore"] = (
        temp_df["PTS"] * scoring_weights["PTS"] +
        temp_df["FG"] * scoring_weights["FG"] +
        temp_df["FGA"] * scoring_weights["FGA"] +
        temp_df["FT"] * scoring_weights["FT"] +
        temp_df["FTA"] * scoring_weights["FTA"] +
        temp_df["3P"] * scoring_weights["3P"] +
        temp_df["TRB"] * scoring_weights["TRB"] +
        temp_df["AST"] * scoring_weights["AST"] +
        temp_df["STL"] * scoring_weights["STL"] +
        temp_df["BLK"] * scoring_weights["BLK"] +
        temp_df["TOV"] * scoring_weights["TOV"]
    )
    return temp_df.sort_values(by="FantasyScore", ascending=False)


def get_top_by_position(position, top_n=5):
    all_players = compute_scores()
    return all_players[all_players["Pos"].str.contains(position, case=False, na=False)].head(top_n)


@app.get("/")
def home(request: Request):
    ranked_players = compute_scores().head(20)
    top_guards = get_top_by_position("G")
    top_forwards = get_top_by_position("F")
    top_centers = get_top_by_position("C")

    return templates.TemplateResponse("index.html", {
        "request": request,
        "players": ranked_players,
        "top_guards": top_guards,
        "top_forwards": top_forwards,
        "top_centers": top_centers
    })


@app.post("/draft")
def draft_player(request: Request, player_name: str = Form(...)):
    drafted_players.add(player_name)
    return RedirectResponse("/", status_code=303)


@app.post("/update-scoring")
def update_scoring(
    request: Request,
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
    global scoring_weights
    scoring_weights = {
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
    }
    return RedirectResponse("/", status_code=303)
