from fastapi import FastAPI
from sqlalchemy import text
from app.database import SessionLocal

from app.database import engine
from app import models


app = FastAPI()

@app.get("/db-check")
def check_db():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))  # ✅ Fix: wrap SQL in text()
        return {"status": "connected to database"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)

