from fastapi import FastAPI
from app.routers import members, plans, subscriptions, attendance
from app.database import engine
from sqlalchemy import text
import os

app = FastAPI()

@app.on_event("startup")
def startup_event():
    try:
        with open(os.path.join("app", "triggers.sql"), "r") as f:
            trigger_sql = f.read()
        
        with engine.connect() as connection:
            connection.execute(text(trigger_sql))
            connection.commit()
    except Exception as e:
        print(f"Error applying trigger: {e}")

app.include_router(members.router, prefix="/members", tags=["Members"])
app.include_router(plans.router, prefix="/plans", tags=["Plans"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])

@app.get("/")
def read_root():
    return {"message": "API is working!"}