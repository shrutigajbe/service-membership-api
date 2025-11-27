Service Membership API
A robust and scalable backend API for managing service memberships, built with FastAPI, PostgreSQL, and SQLAlchemy. This system is ideal for businesses like gyms, coaching centers, or salons to manage members, plans, subscriptions, and attendance.

🌟 Features

👤 Member Management — Create, view, update, and track members
📝 Plan Management — Monthly, Weekly, and Custom plans
🕒 Subscription Management — Auto-calculates subscription end dates
🎫 Attendance Tracking — Each check-in automatically updates total_check_ins
⚙ PostgreSQL Triggers — Ensures attendance count always stays correct
🚀 FastAPI-Powered — Clean, documented API with Swagger UI
🗄 SQLAlchemy ORM — Robust database models & relationships

🛠 Tech Stack
| Component             | Technology                      |
| --------------------- | ------------------------------- |
| **Backend Framework** | FastAPI                         |
| **Database**          | PostgreSQL                      |
| **ORM**               | SQLAlchemy                      |
| **Trigger Logic**     | PostgreSQL Functions + Triggers |
| **Validation**        | Pydantic v2                     |
| **Server**            | Uvicorn                         |


1. Clone the Repository
git clone <https://github.com/shrutigajbe/service-membership-api>
cd service_membership_api

2. Set Up a Virtual Environment
On Windows:
python -m venv venv
.\venv\Scripts\activate

3. Install Dependencies
Install all required Python packages from the requirements.txt file.
pip install -r requirements.txt

4. Configure the Database
You need to set up a database and configure the connection string.

For PostgreSQL (Preferred):
Create a database in your PostgreSQL server (e.g., service_membership_db).
Open app/database.py.
Update the DATABASE_URL with your PostgreSQL credentials:

# Example for PostgreSQL
DATABASE_URL = "postgresql+psycopg://your_user:your_password@localhost:5432/service_membership_db"

Running the Application
Once the setup is complete, you can start the FastAPI server using Uvicorn.
uvicorn app.main:app --reload

The API will be available at http://127.0.0.1:8000.

You can view the interactive API documentation at http://127.0.0.1:8000/docs.

Database Initialization
The database tables and trigger are handled automatically:

Table Creation: SQLAlchemy will automatically create all tables (members, plans, subscriptions, attendances) the first time the application runs and connects to the database.
Trigger Application: The database trigger to increment total_check_ins is defined in app/triggers.sql. The application automatically reads and applies this SQL script on startup, ensuring the trigger is always active.
API Endpoints & Usage Examples
Here are the key endpoints and how to use them.

Members
Create a new member

curl -X POST "http://127.0.0.1:8000/members/" \
-H "Content-Type: application/json" \
-d '{
  "name": "John Doe",
  "phone": "1234567890",
  "status": "active"
}'

List all members (with optional status filter)
# Get all members
curl "http://127.0.0.1:8000/members/"

# Get only active members
curl "http://127.0.0.1:8000/members/?status=active"

Plans
Create a new plan
curl -X POST "http://127.0.0.1:8000/plans/" \
-H "Content-Type: application/json" \
-d '{
  "name": "Monthly Premium",
  "price": 4999,
  "duration_days": 30
}'

List all plans
curl "http://127.0.0.1:8000/plans/"

Subscriptions
Create a subscription for a member
curl -X POST "http://127.0.0.1:8000/subscriptions/" \
-H "Content-Type: application/json" \
-d '{
  "member_id": 1,
  "plan_id": 1,
  "start_date": "2023-10-27"
}'

Get current active subscription for a member
curl "http://127.0.0.1:8000/members/1/current-subscription"

Attendance
Check-in a member
This will fail if the member has no active subscription.
# Successful check-in
curl -X POST "http://127.0.0.1:8000/attendance/check-in" \
-H "Content-Type: application/json" \
-d '{
  "member_id": 1
}'

# Failed check-in (no active subscription)
curl -X POST "http://127.0.0.1:8000/attendance/check-in" \
-H "Content-Type: application/json" \
-d '{
  "member_id": 2
}'
# Expected Response: {"detail":"No active subscription for this member"}

Get attendance history for a member
curl "http://127.0.0.1:8000/members/1/attendance"

Database Trigger
This project includes a database-level trigger to maintain data integrity.

What it does: Automatically increments the total_check_ins column in the members table whenever a new record is inserted into the attendances table.
Where it's defined: app/triggers.sql.
How it's applied: The trigger SQL is executed automatically on application startup via the startup_event in app/main.py. This ensures it's always in place without manual intervention.

service_membership_api/
├── app/
│   ├── __init__.py
│   ├── database.py         # Database session and engine configuration
│   ├── main.py             # FastAPI application instance and startup events
│   ├── models.py           # SQLAlchemy ORM models
│   ├── schemas.py          # Pydantic models for request/response validation
│   ├── triggers.sql        # SQL for the database trigger
│   └── routers/
│       ├── __init__.py
│       ├── attendance.py   # Routes for attendance logic
│       ├── members.py      # Routes for member management
│       ├── plans.py        # Routes for plan management
│       └── subscriptions.py # Routes for subscription management
├── requirements.txt        # Project dependencies
└── README.md              # This file


