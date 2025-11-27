from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from app import models, schemas
from app.database import get_db

router = APIRouter(tags=["Subscriptions"])

@router.post("/", response_model=schemas.SubscriptionOut)
def create_subscription(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    try:
        # Check if member exists
        member = db.query(models.Member).filter(models.Member.id == subscription.member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        # Check if plan exists
        plan = db.query(models.Plan).filter(models.Plan.id == subscription.plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        # Calculate end_date
        end_date = subscription.start_date + timedelta(days=plan.duration_days)
        
        # Create subscription
        new_subscription = models.Subscription(
            member_id=subscription.member_id,
            plan_id=subscription.plan_id,
            start_date=subscription.start_date,
            end_date=end_date  # Calculate this here
        )
        db.add(new_subscription)
        db.commit()
        db.refresh(new_subscription)
        return new_subscription
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/members/{member_id}/current-subscription")
def get_current_subscription(member_id: int, db: Session = Depends(get_db)):
    from datetime import date
    
    # Check if member exists
    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Get current date
    today = date.today()
    
    # Find active subscription
    subscription = db.query(models.Subscription).filter(
        models.Subscription.member_id == member_id,
        models.Subscription.start_date <= today,
        models.Subscription.end_date >= today
    ).first()
    
    if not subscription:
        return {"message": "No active subscription for this member"}
    
    plan = db.query(models.Plan).filter(models.Plan.id == subscription.plan_id).first()
    
    return {
        "id": subscription.id,
        "member_id": subscription.member_id,
        "member_name": member.name,
        "plan_id": subscription.plan_id,
        "plan_name": plan.name,
        "plan_price": plan.price,
        "start_date": subscription.start_date,
        "end_date": subscription.end_date
    }