from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app import models, schemas
from app.database import get_db

router = APIRouter(tags=["Members"])

@router.post("/", response_model=schemas.MemberOut)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    try:
        existing_member = db.query(models.Member).filter(models.Member.phone == member.phone).first()
        if existing_member:
            raise HTTPException(status_code=400, detail="Phone number already registered")
        
        new_member = models.Member(
            name=member.name, 
            phone=member.phone,
            status=member.status
        )
        db.add(new_member)
        db.commit()
        db.refresh(new_member)
        return new_member
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/", response_model=list[schemas.MemberOut])
def get_members(status: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(models.Member)
        if status:
            query = query.filter(models.Member.status == status)
        return query.all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")