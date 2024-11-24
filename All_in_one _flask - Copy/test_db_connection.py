from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Replace with your actual database URI
DATABASE_URI = 'postgresql://postgres:python@localhost:5432/planner_db'

try:
    engine = create_engine(DATABASE_URI)
    with engine.connect() as connection:
        # Use text() to create an executable SQL statement
        result = connection.execute(text("SELECT 1"))
        print("Database connection successful!")
except SQLAlchemyError as e:
    print(f"Database connection failed: {str(e)}")
