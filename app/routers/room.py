from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/rooms",
    tags=['Rooms']
)


@router.get("/", response_model=List[schemas.RoomOut])
def get_rooms(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
    city: Optional[str] = None,
    min_rent: Optional[int] = None,
    max_rent: Optional[int] = None,
    room_type: Optional[str] = None,
    is_available: Optional[bool] = None
):
    """
    Public Endpoint: Discover available rooms with multi-parameter filtering,
    case-insensitive keyword search, pagination, and live bookmark counts via SQL outer join.
    """
    query = db.query(
        models.Room,
        func.count(func.distinct(models.Bookmark.user_id)).label("bookmarks"),
        func.coalesce(func.avg(models.Review.rating), 0.0).label("avg_rating"),
        func.count(func.distinct(models.Review.id)).label("reviews_count")
    ).join(
        models.Bookmark, models.Bookmark.room_id == models.Room.id, isouter=True
    ).join(
        models.Review, models.Review.room_id == models.Room.id, isouter=True
    ).group_by(models.Room.id)

    # Keyword search across title and description (case-insensitive)
    if search:
        query = query.filter(
            or_(
                models.Room.title.ilike(f"%{search}%"),
                models.Room.description.ilike(f"%{search}%")
            )
        )

    # City filter (case-insensitive)
    if city:
        query = query.filter(models.Room.city.ilike(f"%{city}%"))

    # Rent range filters
    if min_rent is not None:
        query = query.filter(models.Room.rent_amount >= min_rent)

    if max_rent is not None:
        query = query.filter(models.Room.rent_amount <= max_rent)

    # Room type filter (e.g. single, shared)
    if room_type:
        query = query.filter(models.Room.room_type == room_type)

    # Availability filter
    if is_available is not None:
        query = query.filter(models.Room.is_available == is_available)

    # Sort newest listings first, apply pagination limit & skip
    rooms = query.order_by(models.Room.created_at.desc()).limit(limit).offset(skip).all()
    return rooms


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RoomResponse)
def create_room(
    room: schemas.RoomCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """
    Protected Endpoint: Create a new room listing linked to the authenticated user.
    """
    room_data = room.model_dump() if hasattr(room, "model_dump") else room.dict()
    new_room = models.Room(owner_id=current_user.id, **room_data)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


@router.get("/{id}", response_model=schemas.RoomOut)
def get_room(id: int, db: Session = Depends(get_db)):
    """
    Public Endpoint: Retrieve single room specifications with owner details and bookmark count.
    """
    room = db.query(
        models.Room,
        func.count(func.distinct(models.Bookmark.user_id)).label("bookmarks"),
        func.coalesce(func.avg(models.Review.rating), 0.0).label("avg_rating"),
        func.count(func.distinct(models.Review.id)).label("reviews_count")
    ).join(
        models.Bookmark, models.Bookmark.room_id == models.Room.id, isouter=True
    ).join(
        models.Review, models.Review.room_id == models.Room.id, isouter=True
    ).group_by(models.Room.id).filter(models.Room.id == id).first()

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id: {id} does not exist"
        )
    return room


@router.put("/{id}", response_model=schemas.RoomResponse)
def update_room(
    id: int,
    updated_room: schemas.RoomUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """
    Protected Endpoint: Update existing room attributes.
    Enforces row-level ownership check (403 Forbidden if user is not the owner).
    """
    room_query = db.query(models.Room).filter(models.Room.id == id)
    room = room_query.first()

    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id: {id} does not exist"
        )

    if room.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    room_data = updated_room.model_dump() if hasattr(updated_room, "model_dump") else updated_room.dict()
    room_query.update(room_data, synchronize_session=False)
    db.commit()
    db.refresh(room)
    return room


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """
    Protected Endpoint: Delete an existing room listing.
    Enforces row-level ownership check (403 Forbidden if user is not the owner).
    """
    room_query = db.query(models.Room).filter(models.Room.id == id)
    room = room_query.first()

    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id: {id} does not exist"
        )

    if room.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    room_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
