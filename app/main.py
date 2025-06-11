from fastapi import FastAPI
from app.routes import player_routes

app = FastAPI()
app.include_router(player_routes.router)
