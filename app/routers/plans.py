from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(tags=["Plans"])

@router.post("/", response_model=schemas.PlanOut)
def create_plan(plan: schemas.PlanCreate, db: Session = Depends(get_db)):
    new_plan = models.Plan(
        name=plan.name,
        price=plan.price,
        duration_days=plan.duration_days
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan

@router.get("/", response_model=list[schemas.PlanOut])
def get_plans(db: Session = Depends(get_db)):
    return db.query(models.Plan).all()