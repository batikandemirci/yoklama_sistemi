from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, LargeBinary
from sqlalchemy.orm import relationship
from .config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String)
    email = Column(String, unique=True, index=True)
    role = Column(String)  # student, teacher, admin
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # İlişkiler
    face_features = relationship("FaceFeatures", back_populates="user", uselist=False)
    attendances = relationship("Attendance", back_populates="user")

class FaceFeatures(Base):
    __tablename__ = "face_features"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    embedding = Column(LargeBinary)  # Yüz özellik vektörü
    confidence_score = Column(Float)  # Yüz tanıma güven skoru
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # İlişkiler
    user = relationship("User", back_populates="face_features")

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    check_in_time = Column(DateTime, default=datetime.utcnow)
    check_out_time = Column(DateTime, nullable=True)
    confidence_score = Column(Float)  # Yüz tanıma güven skoru
    status = Column(String)  # present, late, absent
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # İlişkiler
    user = relationship("User", back_populates="attendances") 