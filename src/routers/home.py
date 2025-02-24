from fastapi import APIRouter

router = APIRouter(prefix="/home", tags=["Home"])


@router.get("/health")
async def home():
    return {"message": "Welcome to Bookmarks API"}
