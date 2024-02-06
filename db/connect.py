from mysql import connector
from fastapi import HTTPException


# Connect to database
def get_db():
    try:
        db = connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="driver_tracker",
        )
        return db
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
