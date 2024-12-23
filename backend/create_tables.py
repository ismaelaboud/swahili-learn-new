from app.services.database import engine
from app.models import lesson, course, user, assessment  # Only import available models

def create_tables():
    """
    Create all database tables defined in the models
    """
    # Import Base from the correct location
    from app.services.database import Base
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")

if __name__ == "__main__":
    create_tables()
