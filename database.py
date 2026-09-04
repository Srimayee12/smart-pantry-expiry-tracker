from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This creates a local file named 'pantry.db' in your project folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./pantry.db"

# Engine manages the connections to the SQLite file
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is what we use to actually talk to the database tables
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class used to create our database models
Base = declarative_base()

# Dependency helper to safely open and close database connections
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()