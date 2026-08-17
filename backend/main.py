import sys
import os

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from db import models
from db.database import engine
from api.routers import router

from sqlalchemy import inspect, text

# Принудительно создаем папку для картинок при запуске
os.makedirs("uploads", exist_ok=True)

# Автоматическое добавление отсутствующих колонок в SQLite
def run_migrations():
    with engine.connect() as conn:
        inspector = inspect(engine)
        if "activities" in inspector.get_table_names():
            columns = [c["name"] for c in inspector.get_columns("activities")]
            if "owner_id" not in columns:
                conn.execute(text("ALTER TABLE activities ADD COLUMN owner_id INTEGER"))
                conn.commit()
            if "group_subtitle" not in columns:
                conn.execute(text("ALTER TABLE activities ADD COLUMN group_subtitle TEXT"))
                conn.commit()
            if "teacher_name" not in columns:
                conn.execute(text("ALTER TABLE activities ADD COLUMN teacher_name TEXT"))
                conn.commit()
            if "spots_info" not in columns:
                conn.execute(text("ALTER TABLE activities ADD COLUMN spots_info TEXT"))
                conn.commit()
            if "duration" not in columns:
                conn.execute(text("ALTER TABLE activities ADD COLUMN duration TEXT"))
                conn.commit()
            if "base_level_info" not in columns:
                conn.execute(text("ALTER TABLE activities ADD COLUMN base_level_info TEXT"))
                conn.commit()
            if "advanced_level_info" not in columns:
                conn.execute(text("ALTER TABLE activities ADD COLUMN advanced_level_info TEXT"))
                conn.commit()
            if "is_first_free" not in columns:
                conn.execute(text("ALTER TABLE activities ADD COLUMN is_first_free BOOLEAN DEFAULT 0"))
                conn.commit()
            if "gender_male" not in columns:
                conn.execute(text("ALTER TABLE activities ADD COLUMN gender_male BOOLEAN DEFAULT 1"))
                conn.commit()
            if "gender_female" not in columns:
                conn.execute(text("ALTER TABLE activities ADD COLUMN gender_female BOOLEAN DEFAULT 1"))
                conn.commit()
        if "bookings" in inspector.get_table_names():
            columns = [c["name"] for c in inspector.get_columns("bookings")]
            if "user_id" not in columns:
                conn.execute(text("ALTER TABLE bookings ADD COLUMN user_id INTEGER"))
                conn.commit()
            if "created_at" not in columns:
                conn.execute(text("ALTER TABLE bookings ADD COLUMN created_at TEXT"))
                conn.commit()

run_migrations()
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="KidsConnect API", description="Бэкенд для поиска и записи в кружки")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Разрешаем фронтенду доступ к файлам внутри папки uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(router, prefix="/api")