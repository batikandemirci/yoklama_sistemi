import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
import sys
import os

# Modül yolunu ayarlama
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.config import DATABASE_URL
from database.models import Base

def create_database():
    # Veritabanı bağlantı bilgileri
    db_name = "yoklama_db"
    db_user = "postgres"
    db_password = "postgres"
    db_host = "localhost"
    db_port = "5432"

    # PostgreSQL sunucusuna bağlanma
    conn = psycopg2.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Cursor oluşturma
    cursor = conn.cursor()

    try:
        # Veritabanını oluşturma
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Veritabanı '{db_name}' başarıyla oluşturuldu.")
    except psycopg2.errors.DuplicateDatabase:
        print(f"Veritabanı '{db_name}' zaten mevcut.")
    except Exception as e:
        print(f"Veritabanı oluşturulurken hata oluştu: {e}")
    finally:
        cursor.close()
        conn.close()

def create_tables():
    try:
        # SQLAlchemy engine oluşturma
        engine = create_engine(DATABASE_URL)
        
        # Tabloları oluşturma
        Base.metadata.create_all(bind=engine)
        print("Tablolar başarıyla oluşturuldu.")
    except Exception as e:
        print(f"Tablolar oluşturulurken hata oluştu: {e}")

if __name__ == "__main__":
    print("Veritabanı oluşturuluyor...")
    create_database()
    
    print("\nTablolar oluşturuluyor...")
    create_tables() 