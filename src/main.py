from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
from pathlib import Path

# Modül yolunu ayarlama
sys.path.append(str(Path(__file__).parent))

from backend.face_recognition_router import router as face_recognition_router
from backend.user_router import router as user_router
from backend.attendance_router import router as attendance_router

app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(face_recognition_router)
app.include_router(user_router)
app.include_router(attendance_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 