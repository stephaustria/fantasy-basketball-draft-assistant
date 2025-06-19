from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db.mongo import drafted_collection, scoring_collection
from app.models.scoring import calculate_fantasy_score
from app.services.fantasy import df
from app.config import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    drafted_names = [doc["player_name"] for doc in drafted_collection.find()]
    scoring_weights = scoring_collection.find_one()["weights"]

    available_df = df[~df["Player"].isin(drafted_names)].copy()
    available_df["FantasyScore"] = available_df.apply(lambda row: calculate_fantasy_score(row, scoring_weights), axis=1)
    available_df["TotalFantasyPoints"] = available_df["FantasyScore"] * available_df["G"]
    sorted_df = available_df.sort_values(by="FantasyScore", ascending=False)

    def top_by_position(pos_keyword):
        return sorted_df[sorted_df["Pos"].str.contains(pos_keyword)].head(5)

    drafted_df = df[df["Player"].isin(drafted_names)].copy()
    drafted_df["FantasyScore"] = drafted_df.apply(lambda row: calculate_fantasy_score(row, scoring_weights), axis=1)
    drafted_df["TotalFantasyPoints"] = drafted_df["FantasyScore"] * drafted_df["G"]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "players": sorted_df.head(15).to_dict(orient="records"),
        "top_guards": top_by_position("G").to_dict(orient="records"),
        "top_forwards": top_by_position("F").to_dict(orient="records"),
        "top_centers": top_by_position("C").to_dict(orient="records"),
        "weights": scoring_weights,
        "drafted_players_list": drafted_df.to_dict(orient="records"),
    })


@router.post("/draft")
def draft_player(player_name: str = Form(...)):
    if not drafted_collection.find_one({"player_name": player_name}):
        drafted_collection.insert_one({"player_name": player_name})
    return RedirectResponse(url="/", status_code=303)


@router.post("/undo-draft")
def undo_draft(player_name: str = Form(...)):
    drafted_collection.delete_one({"player_name": player_name})
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
    new_weights = {
        "PTS": points, "FG": field_goal_made, "FGA": field_goal_attempted,
        "FT": free_throw_made, "FTA": free_throw_attempted, "3P": three_point_made,
        "TRB": rebounds, "AST": assists, "STL": steals, "BLK": blocks, "TOV": turnovers
    }
    scoring_collection.update_one({}, {"$set": {"weights": new_weights}})
    return RedirectResponse(url="/", status_code=303)
