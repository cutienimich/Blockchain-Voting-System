from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routers import auth, users, elections, votes, websocket

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Voting API")

# ─── CORS ────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── ROUTERS ─────────────────────────────────────
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(elections.router)
app.include_router(votes.router)
app.include_router(websocket.router)

@app.get("/")
def root():
    return {"message": "E-Voting backend alive 🗿"}