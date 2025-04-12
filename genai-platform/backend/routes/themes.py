# backend/routes/themes.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_themes():
    return {"message": "Themes route is working"}
