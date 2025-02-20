from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from typing import List, Optional

# User CRUD işlemleri
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_name(db: Session, name: str):
    """İsme göre kullanıcı bul"""
    return db.query(models.User).filter(models.User.name == name).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user: schemas.UserCreate) -> Optional[models.User]:
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user.model_dump().items():
            setattr(db_user, key, value)
        db_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

# FaceFeatures CRUD işlemleri
def create_face_features(db: Session, face_features: schemas.FaceFeaturesCreate) -> models.FaceFeatures:
    db_face_features = models.FaceFeatures(**face_features.model_dump())
    db.add(db_face_features)
    db.commit()
    db.refresh(db_face_features)
    return db_face_features

def get_face_features(db: Session, user_id: int) -> Optional[models.FaceFeatures]:
    return db.query(models.FaceFeatures).filter(models.FaceFeatures.user_id == user_id).first()

def update_face_features(db: Session, user_id: int, face_features: schemas.FaceFeaturesCreate) -> Optional[models.FaceFeatures]:
    db_face_features = get_face_features(db, user_id)
    if db_face_features:
        for key, value in face_features.model_dump().items():
            setattr(db_face_features, key, value)
        db_face_features.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_face_features)
    return db_face_features

# Attendance CRUD işlemleri
def create_attendance(db: Session, attendance: schemas.AttendanceCreate) -> models.Attendance:
    db_attendance = models.Attendance(**attendance.model_dump())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def get_attendance(db: Session, attendance_id: int) -> Optional[models.Attendance]:
    return db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()

def get_user_attendances(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Attendance]:
    return db.query(models.Attendance).filter(
        models.Attendance.user_id == user_id
    ).offset(skip).limit(limit).all()

def update_attendance(db: Session, attendance_id: int, attendance: schemas.AttendanceUpdate) -> Optional[models.Attendance]:
    db_attendance = get_attendance(db, attendance_id)
    if db_attendance:
        for key, value in attendance.model_dump().items():
            setattr(db_attendance, key, value)
        db_attendance.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_attendance)
    return db_attendance

def get_daily_attendances(db: Session, date: datetime) -> List[models.Attendance]:
    return db.query(models.Attendance).filter(
        models.Attendance.check_in_time >= date.replace(hour=0, minute=0, second=0),
        models.Attendance.check_in_time < date.replace(hour=23, minute=59, second=59)
    ).all() 