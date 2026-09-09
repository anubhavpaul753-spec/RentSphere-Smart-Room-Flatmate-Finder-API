from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


# ============ USER SCHEMAS ============

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    city: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    phone_number: Optional[str] = None
    city: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ============ AUTH / TOKEN SCHEMAS ============

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


# ============ ROOM SCHEMAS ============

class RoomBase(BaseModel):
    title: str
    description: str
    city: str
    rent_amount: int
    room_type: str = "single"
    is_available: bool = True


class RoomCreate(RoomBase):
    pass


class RoomUpdate(RoomBase):
    pass


class RoomResponse(RoomBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    model_config = ConfigDict(from_attributes=True)


class RoomOut(BaseModel):
    Room: RoomResponse
    bookmarks: int

    model_config = ConfigDict(from_attributes=True)


# ============ BOOKMARK SCHEMAS ============

class BookmarkCreate(BaseModel):
    room_id: int
    dir: int  # 1 = bookmark, 0 = remove bookmark


# ============ REVIEW SCHEMAS ============

class ReviewCreate(BaseModel):
    room_id: int
    rating: int
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    rating: int
    comment: Optional[str] = None
    created_at: datetime
    user_id: int
    room_id: int
    user: UserOut

    model_config = ConfigDict(from_attributes=True)
