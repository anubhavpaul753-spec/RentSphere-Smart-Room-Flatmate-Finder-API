from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/reviews",
    tags=['Reviews']
)


@router.post("/{room_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.ReviewOut)
def create_or_update_review(
    room_id: int,
    review: schemas.ReviewCreate,
    response: Response,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """
    Protected Endpoint: Submit a rating (1-5 stars) and comment for a room.
    - Ensures room exists (404 Not Found)
    - Prevents landlords/owners from reviewing their own listings (400 Bad Request)
    - Validates rating range 1 to 5
    - If user already reviewed, seamlessly updates the existing review (eliminates spam duplicates)
    """
    # 1. Validate rating range
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Rating must be an integer between 1 and 5 stars"
        )

    # 2. Check if room exists
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id: {room_id} does not exist"
        )

    # 3. Check if current user is owner of the room
    if room.owner_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Landlords cannot review their own room listings"
        )

    # 4. Check for existing review from this user
    existing_review = db.query(models.Review).filter(
        models.Review.room_id == room_id,
        models.Review.user_id == current_user.id
    ).first()

    if existing_review:
        existing_review.rating = review.rating
        existing_review.comment = review.comment
        db.commit()
        db.refresh(existing_review)
        response.status_code = status.HTTP_200_OK
        return existing_review

    # 5. Create new review
    new_review = models.Review(
        room_id=room_id,
        user_id=current_user.id,
        rating=review.rating,
        comment=review.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    response.status_code = status.HTTP_201_CREATED
    return new_review


@router.get("/{room_id}", response_model=schemas.RoomReviewsSummary)
def get_room_reviews(
    room_id: int,
    db: Session = Depends(get_db)
):
    """
    Public Endpoint: Fetch all verified reviews for a room along with aggregated
    average rating and total count, ordered newest first.
    """
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id: {room_id} does not exist"
        )

    reviews = db.query(models.Review).filter(
        models.Review.room_id == room_id
    ).order_by(models.Review.created_at.desc()).all()

    avg_calc = db.query(
        func.coalesce(func.avg(models.Review.rating), 0.0)
    ).filter(models.Review.room_id == room_id).scalar()

    return {
        "room_id": room_id,
        "avg_rating": round(float(avg_calc), 1),
        "total_reviews": len(reviews),
        "reviews": reviews
    }


@router.get("/list/{room_id}", response_model=List[schemas.ReviewOut])
def list_raw_reviews(
    room_id: int,
    db: Session = Depends(get_db)
):
    """
    Public Endpoint: Direct array list of reviews for a room.
    """
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id: {room_id} does not exist"
        )

    return db.query(models.Review).filter(
        models.Review.room_id == room_id
    ).order_by(models.Review.created_at.desc()).all()


@router.put("/{id}", response_model=schemas.ReviewOut)
def update_review(
    id: int,
    review_update: schemas.ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """
    Protected Endpoint: Update existing review comment or rating.
    Enforces author ownership check (403 Forbidden if not the author).
    """
    if review_update.rating < 1 or review_update.rating > 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Rating must be an integer between 1 and 5 stars"
        )

    review_query = db.query(models.Review).filter(models.Review.id == id)
    review = review_query.first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id: {id} does not exist"
        )

    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to edit this review"
        )

    review.rating = review_update.rating
    review.comment = review_update.comment
    db.commit()
    db.refresh(review)
    return review


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """
    Protected Endpoint: Delete a review.
    Enforces author ownership check (403 Forbidden if not the author).
    """
    review_query = db.query(models.Review).filter(models.Review.id == id)
    review = review_query.first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id: {id} does not exist"
        )

    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this review"
        )

    review_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
