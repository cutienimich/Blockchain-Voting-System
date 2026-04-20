from fastapi import APIRouter, Depends
from app.dependencies import get_current_user, admin_only

router = APIRouter(prefix="/users", tags=["Users"])

# ─── MY PROFILE ──────────────────────────────────
@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role,
        "is_verified": current_user.is_verified
    }

# ─── ADMIN ONLY ROUTE ────────────────────────────
@router.get("/admin-dashboard")
def admin_dashboard(current_user=Depends(admin_only)):
    return {"message": f"Welcome Admin {current_user.full_name}"}