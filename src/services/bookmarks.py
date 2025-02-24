from typing import List
from bson import ObjectId
from datetime import datetime, timezone

from fastapi import HTTPException, status

from src.database import db
from src.models.schemas import BookmarkCreate, BookmarkUpdate, BookmarkResponse


async def create_bookmark(
    bookmark: BookmarkCreate,
    user_id: str
) -> BookmarkResponse:
    bookmark_dict = bookmark.model_dump()
    bookmark_dict.update({
        "user_id": ObjectId(user_id),
        "created_at": datetime.now(tz=timezone.utc),
        "is_deleted": False
    })

    result = await db.bookmarks.insert_one(bookmark_dict)
    created_bookmark = await db.bookmarks.find_one({"_id": result.inserted_id})

    return BookmarkResponse(
        id=str(created_bookmark["_id"]),
        **created_bookmark
    )


async def get_bookmarks(user_id: str) -> List[BookmarkResponse]:
    cursor = db.bookmarks.find({
        "user_id": ObjectId(user_id),
        "is_deleted": False
    })
    bookmarks = await cursor.to_list(length=None)
    return [BookmarkResponse(id=str(b["_id"]), **b) for b in bookmarks]


async def get_bookmark(bookmark_id: str, user_id: str) -> BookmarkResponse:
    try:
        bookmark = await db.bookmarks.find_one({
            "user_id": ObjectId(user_id),
            "is_deleted": False,
            "_id": ObjectId(bookmark_id)
        })
        if bookmark == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bookmark not found"
            )
        return BookmarkResponse(id=str(bookmark["_id"]), **bookmark)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )


async def update_bookmark(
    bookmark_id: str,
    user_id: str,
    bookmark: BookmarkUpdate
) -> BookmarkResponse:
    update_data = bookmark.model_dump(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.now(tz=timezone.utc)
        result = await db.bookmarks.update_one(
            {
                "_id": ObjectId(bookmark_id),
                "user_id": ObjectId(user_id),
                "is_deleted": False
            },
            {"$set": update_data}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bookmark not found"
            )

    updated_bookmark = await db.bookmarks.find_one({"_id": ObjectId(bookmark_id)})
    return BookmarkResponse(id=str(updated_bookmark["_id"]), **updated_bookmark)


async def delete_bookmark(bookmark_id: str, user_id: str):
    result = await db.bookmarks.update_one(
        {
            "_id": ObjectId(bookmark_id),
            "user_id": ObjectId(user_id),
            "is_deleted": False
        },
        {"$set": {"is_deleted": True}}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )
