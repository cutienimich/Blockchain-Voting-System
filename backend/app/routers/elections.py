from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import ElectionCreate, ElectionResponse, CandidateCreate, CandidateResponse
from app.dependencies import admin_only, get_current_user
from typing import List

router = APIRouter(prefix="/elections", tags=["Elections"])

# ─── CREATE ELECTION (admin only) ────────────────
@router.post("/", response_model=ElectionResponse)
def create_election(
    data: ElectionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    election = models.Election(
        title=data.title,
        description=data.description,
        start_time=data.start_time,
        end_time=data.end_time,
        is_active=False
    )
    db.add(election)
    db.commit()
    db.refresh(election)
    return election

# ─── GET ALL ELECTIONS ───────────────────────────
@router.get("/", response_model=List[ElectionResponse])
def get_elections(db: Session = Depends(get_db)):
    return db.query(models.Election).all()

# ─── GET ONE ELECTION ────────────────────────────
@router.get("/{election_id}", response_model=ElectionResponse)
def get_election(election_id: int, db: Session = Depends(get_db)):
    election = db.query(models.Election).filter(models.Election.id == election_id).first()
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")
    return election

# ─── ACTIVATE ELECTION (admin only) ──────────────
@router.patch("/{election_id}/activate")
def activate_election(
    election_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    election = db.query(models.Election).filter(models.Election.id == election_id).first()
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")
    election.is_active = True
    db.commit()
    return {"message": "Election activated"}

# ─── ADD CANDIDATE (admin only) ──────────────────
@router.post("/{election_id}/candidates", response_model=CandidateResponse)
def add_candidate(
    election_id: int,
    data: CandidateCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    election = db.query(models.Election).filter(models.Election.id == election_id).first()
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")

    candidate = models.Candidate(
        election_id=election_id,
        name=data.name,
        description=data.description
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

# ─── GET CANDIDATES ──────────────────────────────
@router.get("/{election_id}/candidates", response_model=List[CandidateResponse])
def get_candidates(election_id: int, db: Session = Depends(get_db)):
    return db.query(models.Candidate).filter(models.Candidate.election_id == election_id).all()