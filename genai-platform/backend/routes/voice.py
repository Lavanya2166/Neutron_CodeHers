from fastapi import APIRouter

router = APIRouter()

@router.get("/sample")
def test_route():
    return {"message": "Themes router is working"}
