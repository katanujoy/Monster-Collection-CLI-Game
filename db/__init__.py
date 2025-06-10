# db/__init__.py
from .models import Base
from .database import engine

# This will create tables based on models if they don't exist
def init_db():
    Base.metadata.create_all(bind=engine)
