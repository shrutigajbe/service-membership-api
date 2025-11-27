from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import Optional

from app import models, schemas
from app.database import get_db

router = APIRouter(tags=["Attendance"])

@router.post("/check-in", response_model=schemas.AttendanceOut)
def check_in(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    try:
        # Check if member exists
        member = db.query(models.Member).filter(models.Member.id == attendance.member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        # Check if member has an active subscription
        today = date.today()
        active_subscription = db.query(models.Subscription).filter(
            models.Subscription.member_id == attendance.member_id,
            models.Subscription.start_date <= today,
            models.Subscription.end_date >= today
        ).first()
        
        if not active_subscription:
            raise HTTPException(status_code=400, detail="No active subscription for this member")
        
        # Create attendance record
        new_attendance = models.Attendance(
            member_id=attendance.member_id,
            check_in_date=date.today()  # Using date as per your current model
        )
        
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)
        return new_attendance
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/members/{member_id}/attendance", response_model=list[schemas.AttendanceOut])
def get_member_attendance(member_id: int, db: Session = Depends(get_db)):
    try:
        # Check if member exists
        member = db.query(models.Member).filter(models.Member.id == member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        # Get attendance records
        attendance_records = db.query(models.Attendance).filter(
            models.Attendance.member_id == member_id
        ).all()
        
        return attendance_records
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/", response_model=list[schemas.AttendanceOut])
def get_attendance(db: Session = Depends(get_db)):
    try:
        records = db.query(models.Attendance).all()
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))