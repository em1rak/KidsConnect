KidsConnect 

Платформа для поиска и удобной записи в детские кружки и спортивные секции. 

Проект состоит из двух частей:
* **Frontend:** Vue.js + Vite
* **Backend:** FastAPI (Python) + SQLite

---

## Требования для запуска
Убедитесь, что у вас установлены:
* [Python 3.9+]
* [Node.js 18+]

---

## Шаг 1: Запуск Backend (Сервер и База данных)

1. Откройте терминал и перейдите в папку бэкенда:
```bash
   cd backend
```
2. активируйте виртуальное окружение:
```bash
   python -m venv venv
   .venv\Scripts\activate 
```
3. установите зависимости:
```bash
   pip install fastapi uvicorn sqlalchemy pydantic python-multipart
```
4. запустите сервер:
```bash
   uvicorn main:app --reload
```

Бэкенд запустится на http://localhost:8000. Интерактивная документация (Swagger) доступна по адресу http://localhost:8000/docs.


## Шаг 2: Запуск Frontend (Клиент)
1. Откройте новое окно терминала и перейдите в папку фронтенда:
```bash
   npm install
```
2. запустите клиент:
```bash 
   npm run dev
```
Фронтенд запустится на http://localhost:5173.

## Структура проекта
* backend/ — API сервера, логика базы данных и сохранение загруженных картинок (/uploads).
* src/ — компоненты Vue, стили и API-клиент для связи с бэкендом.
* kidsconnect.db — локальная база данных SQLite (создается автоматически при первом запуске сервера).

