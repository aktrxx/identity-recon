from fastapi import FastAPI
from sqlalchemy import text
from app.database import SessionLocal

from app.database import engine
from app import models
from app.api import router


app = FastAPI()

# @app.get("/db-check")
# def check_db():
#     try:
#         db = SessionLocal()
#         db.execute(text("SELECT 1"))
#         return {"status": "connected to database"}
#     except Exception as e:
#         return {"error": str(e)}
#     finally:
#         db.close()


app.include_router(router)