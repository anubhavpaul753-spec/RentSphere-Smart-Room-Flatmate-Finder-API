from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/bookmarks",
    tags=['Bookmarks']
)


@router.post("/{room_id}", status_code=status.HTTP_200_OK, response_model=schemas.BookmarkToggleResponse)
def toggle_bookmark(
    room_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """
    Protected Endpoint: Smart Toggle bookmark for a room.
    If already bookmarked by the current user -> removes it.
    If not bookmarked -> adds it.
    """
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id: {room_id} does not exist"
        )

    bookmark_query = db.query(models.Bookmark).filter(
        models.Bookmark.room_id == room_id,
        models.Bookmark.user_id == current_user.id
    )
    found_bookmark = bookmark_query.first()

    if found_bookmark:
        bookmark_query.delete(synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_200_OK
        return {
            "message": "Bookmark removed successfully",
            "bookmarked": False,
            "room_id": room_id
        }
    else:
        new_bookmark = models.Bookmark(room_id=room_id, user_id=current_user.id)
        db.add(new_bookmark)
        db.commit()
        response.status_code = status.HTTP_201_CREATED
        return {
            "message": "Room bookmarked successfully",
            "bookmarked": True,
            "room_id": room_id
        }


@router.post("/", status_code=status.HTTP_200_OK, response_model=schemas.BookmarkToggleResponse)
def bookmark_room_legacy(
    bookmark: schemas.BookmarkCreate,
    response: Response,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """
    Protected Endpoint: Explicit bookmark management by room_id and dir flag.
    dir=1 -> add bookmark, dir=0 -> remove bookmark.
    """
    room = db.query(models.Room).filter(models.Room.id == bookmark.room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id: {bookmark.room_id} does not exist"
        )

    bookmark_query = db.query(models.Bookmark).filter(
        models.Bookmark.room_id == bookmark.room_id,
        models.Bookmark.user_id == current_user.id
    )
    found_bookmark = bookmark_query.first()

    if bookmark.dir == 1:
        if found_bookmark:
            return {
                "message": "Room already bookmarked",
                "bookmarked": True,
                "room_id": bookmark.room_id
            }
        new_bookmark = models.Bookmark(room_id=bookmark.room_id, user_id=current_user.id)
        db.add(new_bookmark)
        db.commit()
        response.status_code = status.HTTP_201_CREATED
        return {
            "message": "Room bookmarked successfully",
            "bookmarked": True,
            "room_id": bookmark.room_id
        }
    else:
        if not found_bookmark:
            return {
                "message": "Bookmark does not exist",
                "bookmarked": False,
                "room_id": bookmark.room_id
            }
        bookmark_query.delete(synchronize_session=False)
        db.commit()
        return {
            "message": "Bookmark removed successfully",
            "bookmarked": False,
            "room_id": bookmark.room_id
        }


@router.get("/me", response_model=List[schemas.RoomOut])
def get_user_bookmarks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """
    Protected Endpoint: Fetch all rooms bookmarked by the authenticated user,
    with full room details, live bookmark counts, and rating aggregations.
    """
    user_saved_rooms = db.query(
        models.Room,
        func.count(func.distinct(models.Bookmark.user_id)).label("bookmarks"),
        func.coalesce(func.avg(models.Review.rating), 0.0).label("avg_rating"),
        func.count(func.distinct(models.Review.id)).label("reviews_count")
    ).join(
        models.Bookmark, models.Bookmark.room_id == models.Room.id, isouter=True
    ).join(
        models.Review, models.Review.room_id == models.Room.id, isouter=True
    ).filter(
        models.Room.id.in_(
            db.query(models.Bookmark.room_id).filter(models.Bookmark.user_id == current_user.id)
        )
    ).group_by(models.Room.id).order_by(models.Room.created_at.desc()).all()

    return user_saved_rooms


@router.get("/check/{room_id}")
def check_bookmark_status(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """
    Protected Endpoint: Fast boolean check if current user has saved this room.
    """
    exists = db.query(models.Bookmark).filter(
        models.Bookmark.room_id == room_id,
        models.Bookmark.user_id == current_user.id
    ).first() is not None

    return {"room_id": room_id, "bookmarked": exists}
