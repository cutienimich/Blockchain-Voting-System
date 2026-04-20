from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import auth, users, elections, votes


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Voting API")

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Voting API")

# ─── ROUTERS ─────────────────────────────────────
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(elections.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"message": "E-Voting backend alive 🗿"}