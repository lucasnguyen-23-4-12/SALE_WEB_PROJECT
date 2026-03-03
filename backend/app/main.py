from fastapi import FastAPI
from app.database import engine, Base
from app.models import *
from app.routers import customer

app = FastAPI(
    title="Retail Management API",
    version="1.0.0"
)
app.include_router(customer.router)
@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}
from sqlalchemy import text

@app.get("/test-db")
def test_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"result": result.scalar()}
