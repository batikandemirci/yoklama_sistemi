from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
import os
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# Modül yolunu ayarlama
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import crud, models, schemas
from database.config import engine, get_db
from backend.face_recognition_router import router as face_recognition_router

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="Yoklama Sistemi API",
    description="Yüz tanıma tabanlı yoklama sistemi için REST API",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend'in adresi
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP metodlarına izin ver
    allow_headers=["*"],  # Tüm başlıklara izin ver
)

# Router'ları ekle
app.include_router(face_recognition_router)

# Ana sayfa
@app.get("/")
def read_root():
    return {"message": "Yoklama Sistemi API'sine Hoş Geldiniz"}

# Kullanıcı işlemleri
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email zaten kayıtlı")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.UserWithDetails)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    return db_user

# Yüz özellikleri işlemleri
@app.post("/users/{user_id}/face-features/", response_model=schemas.FaceFeatures)
def create_user_face_features(
    user_id: int,
    face_features: schemas.FaceFeaturesCreate,
    db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    return crud.create_face_features(db=db, face_features=face_features)

@app.get("/users/{user_id}/face-features/", response_model=schemas.FaceFeatures)
def read_user_face_features(user_id: int, db: Session = Depends(get_db)):
    face_features = crud.get_face_features(db, user_id=user_id)
    if face_features is None:
        raise HTTPException(status_code=404, detail="Yüz özellikleri bulunamadı")
    return face_features

# Yoklama işlemleri
@app.post("/attendances/", response_model=schemas.Attendance)
def create_attendance(
    attendance: schemas.AttendanceCreate,
    db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=attendance.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    return crud.create_attendance(db=db, attendance=attendance)

@app.get("/users/{user_id}/attendances/", response_model=list[schemas.Attendance])
def read_user_attendances(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    attendances = crud.get_user_attendances(db, user_id=user_id, skip=skip, limit=limit)
    return attendances

@app.get("/attendances/daily/{date}", response_model=list[schemas.Attendance])
def read_daily_attendances(
    date: str,
    db: Session = Depends(get_db)
):
    try:
        # Tarih formatını kontrol et ve datetime nesnesine dönüştür
        attendance_date = datetime.strptime(date, "%Y-%m-%d")
        attendances = crud.get_daily_attendances(db, date=attendance_date)
        return attendances
    except ValueError:
        raise HTTPException(status_code=400, detail="Geçersiz tarih formatı. Beklenen format: YYYY-MM-DD")

@app.put("/attendances/{attendance_id}", response_model=schemas.Attendance)
def update_attendance(
    attendance_id: int,
    attendance: schemas.AttendanceUpdate,
    db: Session = Depends(get_db)
):
    db_attendance = crud.update_attendance(db, attendance_id=attendance_id, attendance=attendance)
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Yoklama kaydı bulunamadı")
    return db_attendance 