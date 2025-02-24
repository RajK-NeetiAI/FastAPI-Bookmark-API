from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.models.schemas import BookmarkCreate, BookmarkUpdate, BookmarkResponse, UserInDb
from src.services.bookmarks import (
    create_bookmark,
    get_bookmarks,
    update_bookmark,
    delete_bookmark,
    get_bookmark
)
from src.utils.security import get_current_user

router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])


@router.post("/create", response_model=BookmarkResponse)
async def create_new_bookmark(
    bookmark: BookmarkCreate,
    current_user: Annotated[UserInDb, Depends(get_current_user)]
):
    return await create_bookmark(bookmark, current_user.id)


@router.get("/get", response_model=List[BookmarkResponse])
async def list_bookmarks(current_user: Annotated[UserInDb, Depends(get_current_user)]):
    return await get_bookmarks(current_user.id)


@router.get("/get/{bookmark_id}", response_model=BookmarkResponse)
async def list_bookmark(
    bookmark_id: str,
    current_user: Annotated[UserInDb, Depends(get_current_user)]
):
    return await get_bookmark(bookmark_id, current_user.id)


@router.put("/update/{bookmark_id}", response_model=BookmarkResponse)
async def update_existing_bookmark(
    bookmark_id: str,
    bookmark: BookmarkUpdate,
    current_user: Annotated[UserInDb, Depends(get_current_user)]
):
    return await update_bookmark(bookmark_id, current_user.id, bookmark)


@router.delete("delete/{bookmark_id}")
async def delete_existing_bookmark(
    bookmark_id: str,
    current_user: Annotated[UserInDb, Depends(get_current_user)]
):
    await delete_bookmark(bookmark_id, current_user.id)
    return {"message": "Bookmark deleted successfully"}
