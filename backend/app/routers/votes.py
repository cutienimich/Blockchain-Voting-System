from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import VoteCreate, VoteResponse
from app.dependencies import get_current_user, admin_only
from app.blockchain import send_vote_to_blockchain
from typing import List

router = APIRouter(prefix="/votes", tags=["Votes"])

# ─── CAST VOTE ───────────────────────────────────
@router.post("/", response_model=VoteResponse)
def cast_vote(
    data: VoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # check election exists
    election = db.query(models.Election).filter(
        models.Election.id == data.election_id
    ).first()
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")

    # check election is active
    if not election.is_active:
        raise HTTPException(status_code=400, detail="Election is not active")

    # check candidate exists in this election
    candidate = db.query(models.Candidate).filter(
        models.Candidate.id == data.candidate_id,
        models.Candidate.election_id == data.election_id
    ).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found in this election")

    # check already voted
    existing_vote = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id,
        models.Vote.election_id == data.election_id
    ).first()
    if existing_vote:
        raise HTTPException(status_code=400, detail="You already voted in this election")

    # ─── SEND TO BLOCKCHAIN ──────────────────────
    tx_hash = send_vote_to_blockchain(
        user_id=current_user.id,
        election_id=data.election_id,
        candidate_id=data.candidate_id
    )

    # save vote
    vote = models.Vote(
        user_id=current_user.id,
        election_id=data.election_id,
        candidate_id=data.candidate_id,
        transaction_hash=tx_hash,
        is_flagged=False
    )
    db.add(vote)
    db.commit()
    db.refresh(vote)
    return vote

# ─── GET RESULTS ─────────────────────────────────
@router.get("/{election_id}/results")
def get_results(election_id: int, db: Session = Depends(get_db)):
    election = db.query(models.Election).filter(
        models.Election.id == election_id
    ).first()
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")

    candidates = db.query(models.Candidate).filter(
        models.Candidate.election_id == election_id
    ).all()

    results = []
    for candidate in candidates:
        vote_count = db.query(models.Vote).filter(
            models.Vote.candidate_id == candidate.id,
            models.Vote.election_id == election_id
        ).count()
        results.append({
            "candidate_id": candidate.id,
            "candidate_name": candidate.name,
            "vote_count": vote_count
        })

    return {
        "election_id": election_id,
        "election_title": election.title,
        "results": results
    }

# ─── GET ALL VOTES (admin only) ──────────────────
@router.get("/", response_model=List[VoteResponse])
def get_all_votes(
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    return db.query(models.Vote).all()

# ─── CHECK IF USER VOTED ─────────────────────────
@router.get("/{election_id}/my-vote")
def my_vote(
    election_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    vote = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id,
        models.Vote.election_id == election_id
    ).first()
    if not vote:
        return {"voted": False}
    return {"voted": True, "candidate_id": vote.candidate_id}