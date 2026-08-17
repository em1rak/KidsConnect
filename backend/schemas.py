from pydantic import BaseModel
from typing import Optional

class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    age_group: Optional[str] = None
    address: Optional[str] = None
    place: Optional[str] = None
    image_url: Optional[str] = None            # <-- Поле для картинки
    lat: Optional[float] = None
    lng: Optional[float] = None
    is_free: bool = False
    is_first_free: bool = False
    gender_male: Optional[bool] = True
    gender_female: Optional[bool] = True
    price: Optional[str] = None
    schedule: Optional[str] = None
    group_subtitle: Optional[str] = None
    teacher_name: Optional[str] = None
    spots_info: Optional[str] = None
    duration: Optional[str] = None
    base_level_info: Optional[str] = None
    advanced_level_info: Optional[str] = None
    owner_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    pass

class ActivityResponse(ActivityBase):
    id: int

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    parent_name: str
    child_name: str
    child_age: int
    phone: str
    activity_id: int
    user_id: Optional[int] = None

class BookingResponse(BookingCreate):
    id: int
    status: str
    created_at: Optional[str] = None
    activity: Optional[ActivityResponse] = None

    class Config:
        from_attributes = True

class BookingStatusUpdate(BaseModel):
    status: str

# --- АВТОРИЗАЦИЯ И ПОЛЬЗОВАТЕЛИ ---
class UserRegister(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    role: Optional[str] = "parent"  # "parent" или "leader"
    password: str

class UserLogin(BaseModel):
    login: str  # e-mail или телефон
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    role: str = "parent"

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
