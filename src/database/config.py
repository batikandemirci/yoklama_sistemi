from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL bağlantı bilgileri
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/yoklama_db"

# SQLAlchemy engine oluşturma
engine = create_engine(DATABASE_URL)

# Session oluşturucu
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Temel model sınıfı
Base = declarative_base()

# Veritabanı bağlantısı için yardımcı fonksiyon
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 