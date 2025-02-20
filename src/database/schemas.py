from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

# User şemaları
class UserBase(BaseModel):
    name: str
    surname: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# FaceFeatures şemaları
class FaceFeaturesBase(BaseModel):
    confidence_score: float

class FaceFeaturesCreate(FaceFeaturesBase):
    user_id: int
    embedding: bytes

class FaceFeatures(FaceFeaturesBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Attendance şemaları
class AttendanceBase(BaseModel):
    user_id: int
    confidence_score: float
    status: str

class AttendanceCreate(AttendanceBase):
    check_in_time: datetime

class AttendanceUpdate(BaseModel):
    check_out_time: datetime

class Attendance(AttendanceBase):
    id: int
    check_in_time: datetime
    check_out_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Genişletilmiş User şeması (ilişkiler dahil)
class UserWithDetails(User):
    face_features: Optional[FaceFeatures] = None
    attendances: List[Attendance] = []

    class Config:
        from_attributes = True 