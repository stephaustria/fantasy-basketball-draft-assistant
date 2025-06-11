from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.models.scoring import calculate_fantasy_score
from app.services.fantasy import df, scoring_weights, drafted_players
from app.config import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
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


@router.post("/draft")
def draft_player(player_name: str = Form(...)):
    drafted_players.append(player_name)
    return RedirectResponse(url="/", status_code=303)


@router.post("/update-scoring")
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
