from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv('DATABASE_URL')

try:
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Test connection
    with engine.connect() as connection:
        print("Database connection successful!")
        result = connection.execute(text("SELECT version()"))
        print("PostgreSQL Version:", result.scalar())
except Exception as e:
    print(f"Connection failed: {e}")
    import traceback
    traceback.print_exc()
