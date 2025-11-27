from pydantic import BaseModel
from datetime import date
from typing import Optional

# ---------------- Members ----------------
class MemberCreate(BaseModel):
    name: str
    phone: str
    status: Optional[str] = "active"

class MemberOut(BaseModel):
    id: int
    name: str
    phone: str
    join_date: date
    status: str
    total_check_ins: int

    class Config:
        from_attributes = True

# ---------------- Plans ----------------
class PlanCreate(BaseModel):
    name: str
    price: int
    duration_days: int

class PlanOut(BaseModel):
    id: int
    name: str
    price: int
    duration_days: int

    class Config:
        from_attributes = True

# ---------------- Subscriptions ----------------
class SubscriptionCreate(BaseModel):
    member_id: int
    plan_id: int
    start_date: date

class SubscriptionOut(BaseModel):
    id: int
    member_id: int
    plan_id: int
    start_date: date
    end_date: date

    class Config:
        from_attributes = True

# ---------------- Attendance ----------------
class AttendanceCreate(BaseModel):
    member_id: int

class AttendanceOut(BaseModel):
    id: int
    member_id: int
    check_in_date: date  # Using date to match your model

    class Config:
        from_attributes = True