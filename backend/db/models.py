from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    category = Column(String, index=True)
    age_group = Column(String)
    address = Column(String)
    place = Column(String, nullable=True)
    image_url = Column(String, nullable=True)  # <-- Поле для картинки
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    is_free = Column(Boolean, default=False)
    is_first_free = Column(Boolean, default=False)
    gender_male = Column(Boolean, default=True, nullable=True)
    gender_female = Column(Boolean, default=True, nullable=True)
    price = Column(String, nullable=True)
    schedule = Column(String, nullable=True)
    group_subtitle = Column(String, nullable=True)
    teacher_name = Column(String, nullable=True)
    spots_info = Column(String, nullable=True)
    duration = Column(String, nullable=True)
    base_level_info = Column(String, nullable=True)
    advanced_level_info = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    owner = relationship("User", foreign_keys=[owner_id])
    bookings = relationship("Booking", back_populates="activity")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    parent_name = Column(String)
    child_name = Column(String)
    child_age = Column(Integer)
    phone = Column(String)
    status = Column(String, default="Ожидает")
    created_at = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    activity_id = Column(Integer, ForeignKey("activities.id"))
    
    activity = relationship("Activity", back_populates="bookings")
    user = relationship("User", foreign_keys=[user_id])

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True, index=True)
    role = Column(String, default="parent")  # "parent" (Родитель) или "leader" (Руководитель кружка)
    hashed_password = Column(String, nullable=False)
    token = Column(String, nullable=True, index=True)
