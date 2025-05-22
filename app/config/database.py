from typing import Generator
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .settings_env import settings_objeto

engine = create_engine(settings_objeto.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Función para obtener la sesión de la base de datos
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()  # Crear una nueva sesión
    try:
        yield db  # Devolver la sesión para su uso
    finally:
        db.close()

        
