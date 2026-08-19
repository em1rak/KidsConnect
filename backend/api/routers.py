from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import shutil
import uuid
import re
from db import models
import schemas
from db.database import get_db
from auth_utils import hash_password, verify_password, generate_token

router = APIRouter()

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ АВТОРИЗАЦИИ ---
def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)) -> models.User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Требуется авторизация")
    token = authorization.split(" ")[1]
    user = db.query(models.User).filter(models.User.token == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Недействительный или истекший токен")
    return user

def get_optional_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)) -> Optional[models.User]:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ")[1]
    return db.query(models.User).filter(models.User.token == token).first()

# --- АВТОРИЗАЦИЯ И ПОЛЬЗОВАТЕЛИ ---
@router.post("/auth/register", response_model=schemas.TokenResponse)
def register(user_data: schemas.UserRegister, db: Session = Depends(get_db)):
    email = user_data.email.strip().lower()
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким e-mail уже зарегистрирован")
    
    token = generate_token()
    hashed_pwd = hash_password(user_data.password)
    
    role_val = user_data.role if user_data.role in ["parent", "leader"] else "parent"
    
    new_user = models.User(
        name=user_data.name.strip(),
        email=email,
        phone=user_data.phone.strip() if user_data.phone else None,
        role=role_val,
        hashed_password=hashed_pwd,
        token=token
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": new_user
    }

@router.post("/auth/login", response_model=schemas.TokenResponse)
def login(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    login_str = login_data.login.strip()
    user = db.query(models.User).filter(
        (models.User.email == login_str.lower()) | (models.User.phone == login_str)
    ).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный логин (e-mail/телефон) или пароль")
    
    token = generate_token()
    user.token = token
    db.commit()
    db.refresh(user)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/auth/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.post("/auth/logout")
def logout(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.token = None
    db.commit()
    return {"message": "Успешный выход из системы"}

# --- ЗАГРУЗКА ФАЙЛОВ ---
@router.post("/upload/")
def upload_image(file: UploadFile = File(...)):
    # Вытаскиваем расширение файла (например, .jpg или .png)
    file_extension = file.filename.split(".")[-1]
    
    # Создаем уникальное имя (например, 550e8400-e29b-41d4-a716-446655440000.jpg)
    file_name = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"uploads/{file_name}"
    
    # Сохраняем файл на жесткий диск
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"image_url": f"/{file_path}"}

# --- КРУЖКИ И ЗАПИСЬ ---
@router.post("/activities/", response_model=schemas.ActivityResponse)
def create_activity(
    activity: schemas.ActivityCreate, 
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
):
    activity_dict = activity.model_dump()
    if current_user and current_user.role == "leader":
        activity_dict["owner_id"] = current_user.id

    db_activity = models.Activity(**activity_dict)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@router.get("/activities/", response_model=List[schemas.ActivityResponse])
def get_activities(
    category: Optional[str] = None, 
    is_free: Optional[bool] = None, 
    db: Session = Depends(get_db)
):
    query = db.query(models.Activity)
    if category:
        query = query.filter(models.Activity.category == category)
    if is_free is not None:
        query = query.filter(models.Activity.is_free == is_free)
    
    return query.all()

@router.get("/activities/{activity_id}", response_model=schemas.ActivityResponse)
def get_activity_by_id(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Кружок не найден")
    return activity

@router.post("/bookings/", response_model=schemas.BookingResponse)
def create_booking(
    booking: schemas.BookingCreate, 
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
):
    activity = db.query(models.Activity).filter(models.Activity.id == booking.activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Выбранный кружок не существует")
    
    booking_dict = booking.model_dump()
    if current_user and not booking_dict.get("user_id"):
        booking_dict["user_id"] = current_user.id
    
    if not booking_dict.get("created_at"):
        booking_dict["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        
    db_booking = models.Booking(**booking_dict)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 1. Уведомление для родителя
    parent_user_id = db_booking.user_id
    if not parent_user_id and db_booking.phone:
        user_by_phone = db.query(models.User).filter(models.User.phone == db_booking.phone).first()
        if user_by_phone:
            parent_user_id = user_by_phone.id

    if parent_user_id:
        db.add(models.Notification(
            text=f"Заявка для ребенка {booking.child_name} на кружок '{activity.title}' успешно отправлена.",
            is_read=False,
            created_at=now_str,
            user_id=parent_user_id
        ))

    # 2. Уведомление для руководителя(ей) кружка
    leader_ids = []
    if activity.owner_id:
        leader_ids.append(activity.owner_id)
    else:
        all_leaders = db.query(models.User).filter(models.User.role == "leader").all()
        leader_ids = [l.id for l in all_leaders]

    for lid in leader_ids:
        db.add(models.Notification(
            text=f"Новая заявка на кружок '{activity.title}': {booking.child_name} (тел: {booking.phone}).",
            is_read=False,
            created_at=now_str,
            user_id=lid
        ))

    db.commit()
    return db_booking


# --- УПРАВЛЕНИЕ ЗАЯВКАМИ И ИСТОРИЯ ---
@router.get("/bookings/my", response_model=List[schemas.BookingResponse])
def get_my_bookings(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.Booking).filter(
        (models.Booking.user_id == current_user.id) | 
        ((models.Booking.phone == current_user.phone) & (models.Booking.user_id.is_(None)))
    ).order_by(models.Booking.id.desc())
    return query.all()

@router.get("/leader/bookings", response_model=List[schemas.BookingResponse])
def get_leader_bookings(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "leader":
        raise HTTPException(status_code=403, detail="Доступно только для руководителей")
    
    # Ищем кружки, принадлежащие данному руководителю (или не задействованные никем другим)
    leader_activities = db.query(models.Activity).filter(
        (models.Activity.owner_id == current_user.id) | (models.Activity.owner_id.is_(None))
    ).all()
    activity_ids = [a.id for a in leader_activities]
    
    if not activity_ids:
        return []
    
    return db.query(models.Booking).filter(models.Booking.activity_id.in_(activity_ids)).order_by(models.Booking.id.desc()).all()

@router.get("/leader/activities", response_model=List[schemas.ActivityResponse])
def get_leader_activities(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "leader":
        raise HTTPException(status_code=403, detail="Доступно только для руководителей")
    
    # Привязываем кружки без владельца к текущему руководителю
    unowned = db.query(models.Activity).filter(models.Activity.owner_id.is_(None)).all()
    if unowned:
        for act in unowned:
            act.owner_id = current_user.id
        db.commit()

    return db.query(models.Activity).filter(models.Activity.owner_id == current_user.id).order_by(models.Activity.id.desc()).all()

@router.get("/activities/{activity_id}/bookings", response_model=List[schemas.BookingResponse])
def get_activity_bookings(
    activity_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "leader":
        raise HTTPException(status_code=403, detail="Доступно только для руководителей")
    
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Кружок не найден")
        
    bookings = db.query(models.Booking).filter(models.Booking.activity_id == activity_id).order_by(models.Booking.id.desc()).all()
    return bookings

@router.patch("/bookings/{booking_id}/status", response_model=schemas.BookingResponse)
def update_booking_status(
    booking_id: int,
    status_update: schemas.BookingStatusUpdate,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "leader":
        raise HTTPException(status_code=403, detail="Доступно только для руководителей")
    
    allowed_statuses = ["Ожидает", "Принято", "Отклонено"]
    if status_update.status not in allowed_statuses:
        raise HTTPException(status_code=400, detail=f"Недопустимый статус. Разрешенные статусы: {', '.join(allowed_statuses)}")
    
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    
    booking.status = status_update.status
    db.commit()
    db.refresh(booking)
    
    activity_title = booking.activity.title if booking.activity else "Кружок"
    
    # Отправка уведомления родителю об изменении статуса (Принято / Отклонено)
    parent_user_id = booking.user_id
    if not parent_user_id and booking.phone:
        user_by_phone = db.query(models.User).filter(models.User.phone == booking.phone).first()
        if user_by_phone:
            parent_user_id = user_by_phone.id

    if parent_user_id:
        if booking.status == "Принято":
            status_msg = f"Ваша заявка на кружок '{activity_title}' для {booking.child_name} принята!"
        elif booking.status == "Отклонено":
            status_msg = f"Ваша заявка на кружок '{activity_title}' для {booking.child_name} отклонена."
        else:
            status_msg = f"Статус вашей заявки на кружок '{activity_title}' для {booking.child_name} изменен на '{booking.status}'."
            
        db_notification = models.Notification(
            text=status_msg,
            is_read=False,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
            user_id=parent_user_id
        )
        db.add(db_notification)
        db.commit()

    return booking


@router.put("/activities/{activity_id}", response_model=schemas.ActivityResponse)
def update_activity(
    activity_id: int,
    activity_update: schemas.ActivityCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "leader":
        raise HTTPException(status_code=403, detail="Доступно только для руководителей")
    
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Кружок не найден")
    
    if activity.owner_id and activity.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Вы не являетесь владельцем этого кружка")
    
    update_data = activity_update.model_dump()
    # Сохраняем истинного владельца кружка
    update_data["owner_id"] = activity.owner_id or current_user.id

    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    return activity

@router.delete("/activities/{activity_id}")
def delete_activity(
    activity_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "leader":
        raise HTTPException(status_code=403, detail="Доступно только для руководителей")
    
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Кружок не найден")
    
    if activity.owner_id and activity.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Вы не являетесь владельцем этого кружка")
    
    db.query(models.Booking).filter(models.Booking.activity_id == activity_id).delete()
    db.delete(activity)
    db.commit()
    return {"message": "Кружок успешно удален"}

# --- ОТЗЫВЫ ---
@router.post("/reviews/", response_model=schemas.ReviewResponse)
def create_review(
    review: schemas.ReviewCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="Оценка должна быть от 1 до 5")
    
    activity = db.query(models.Activity).filter(models.Activity.id == review.activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Кружок не найден")
    
    # Проверка: пользователь может выставить только 1 отзыв к кружку
    existing_review = db.query(models.Review).filter(
        models.Review.user_id == current_user.id,
        models.Review.activity_id == review.activity_id
    ).first()
    if existing_review:
        raise HTTPException(status_code=400, detail="Вы уже оставили отзыв к этому кружку")

    review_dict = review.model_dump()

    review_dict["user_id"] = current_user.id
    review_dict["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    db_review = models.Review(**review_dict)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/activities/{activity_id}/reviews", response_model=List[schemas.ReviewResponse])
def get_activity_reviews(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Кружок не найден")
    
    reviews = db.query(models.Review).filter(models.Review.activity_id == activity_id).order_by(models.Review.id.desc()).all()
    return reviews

# --- РЕКОМЕНДАЦИИ ---
def is_age_in_group(age_group: Optional[str], target_age: int) -> bool:
    # Проверка соответствия возраста диапазону
    if not age_group:
        return True
    if str(target_age) in age_group:
        return True
    numbers = [int(n) for n in re.findall(r'\d+', age_group)]
    if not numbers:
        return True
    if ("от" in age_group.lower() or "+" in age_group) and len(numbers) == 1:
        return target_age >= numbers[0]
    if "до" in age_group.lower() and len(numbers) == 1:
        return target_age <= numbers[0]
    if len(numbers) >= 2:
        return numbers[0] <= target_age <= numbers[1]
    if len(numbers) == 1:
        return target_age == numbers[0]
    return False

@router.get("/recommendations/", response_model=List[schemas.ActivityResponse])
def get_recommendations(
    age: Optional[int] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Activity)
    
    # Фильтр по категории
    if category and category.strip():
        query = query.filter(models.Activity.category.ilike(f"%{category.strip()}%"))
        
    activities = query.all()
    
    # Фильтр по возрасту
    if age is not None:
        activities = [act for act in activities if is_age_in_group(act.age_group, age)]
        
    return activities

# --- УВЕДОМЛЕНИЯ ---
@router.get("/notifications/", response_model=List[schemas.NotificationResponse])
def get_notifications(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id
    ).order_by(models.Notification.id.desc()).all()

@router.patch("/notifications/{notification_id}/read", response_model=schemas.NotificationResponse)
def mark_notification_read(
    notification_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notif = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == current_user.id
    ).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    
    notif.is_read = True
    db.commit()
    db.refresh(notif)
    return notif



