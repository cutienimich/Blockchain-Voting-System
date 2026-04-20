from fastapi import FastAPI
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Voting Backend API")

@app.get("/")
def root():
    return {"message": "E-Voting Backend API"}