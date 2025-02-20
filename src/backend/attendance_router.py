from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
import sys
import os
from pathlib import Path

# Modül yolunu ayarlama
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import crud, schemas
from database.config import get_db

router = APIRouter(
    prefix="/attendances",
    tags=["attendances"],
    responses={404: {"description": "Not found"}},
)

def format_attendance(attendance, user):
    """Yoklama kaydını formatla"""
    return {
        "id": attendance.id,
        "user_id": attendance.user_id,
        "user": {
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "role": user.role
        },
        "check_in_time": attendance.check_in_time.isoformat(),
        "check_out_time": attendance.check_out_time.isoformat() if attendance.check_out_time else None,
        "confidence_score": attendance.confidence_score,
        "status": attendance.status
    }

@router.get("/today")
def get_today_attendances(db: Session = Depends(get_db)):
    """Bugünün yoklama kayıtlarını getir"""
    try:
        today = datetime.now(timezone.utc)
        
        # Günlük yoklamaları getir
        daily_attendances = crud.get_daily_attendances(db, today)
        
        # Yoklama kayıtlarını formatla
        formatted_attendances = []
        for attendance in daily_attendances:
            user = crud.get_user(db, attendance.user_id)
            if user:
                formatted_attendances.append(format_attendance(attendance, user))
        
        # Tarihe göre sırala (en yeni en üstte)
        formatted_attendances.sort(key=lambda x: x["check_in_time"], reverse=True)
        
        return formatted_attendances
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/daily/{date}")
def get_daily_attendances(date: str, db: Session = Depends(get_db)):
    """Belirli bir güne ait yoklama kayıtlarını getir"""
    try:
        # Tarih string'ini datetime objesine çevir
        try:
            attendance_date = datetime.strptime(date, "%Y-%m-%d")
            # UTC timezone ekle
            attendance_date = attendance_date.replace(tzinfo=timezone.utc)
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail="Geçersiz tarih formatı. Tarih YYYY-MM-DD formatında olmalıdır."
            )
        
        # Günlük yoklamaları getir
        daily_attendances = crud.get_daily_attendances(db, attendance_date)
        
        # Yoklama kayıtlarını formatla
        formatted_attendances = []
        for attendance in daily_attendances:
            user = crud.get_user(db, attendance.user_id)
            if user:
                formatted_attendances.append(format_attendance(attendance, user))
        
        # Tarihe göre sırala (en yeni en üstte)
        formatted_attendances.sort(key=lambda x: x["check_in_time"], reverse=True)
        
        return formatted_attendances
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}")
def get_user_attendances(
    user_id: int, 
    start_date: str = None, 
    end_date: str = None, 
    db: Session = Depends(get_db)
):
    """Belirli bir kullanıcının yoklama kayıtlarını getir"""
    try:
        # Kullanıcıyı kontrol et
        user = crud.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
            
        # Yoklama kayıtlarını getir
        attendances = crud.get_user_attendances(db, user_id)
        
        # Yoklama kayıtlarını formatla
        formatted_attendances = [format_attendance(attendance, user) for attendance in attendances]
        
        # Tarihe göre sırala (en yeni en üstte)
        formatted_attendances.sort(key=lambda x: x["check_in_time"], reverse=True)
        
        return formatted_attendances
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 