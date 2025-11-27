Service Membership API

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![PyPI version](https://img.shields.io/pypi/v/your-package-name)
![codecov](https://img.shields.io/codecov/c/github/shrutigajbe/service-membership-api)
![Build Status](https://img.shields.io/github/workflow/status/shrutigajbe/service-membership-api/CI)

A robust, scalable, and modern backend API for managing service memberships. Built with FastAPI, PostgreSQL, and SQLAlchemy, this system is the perfect foundation for businesses like gyms, coaching centers, or salons to manage members, plans, subscriptions, and attendance with ease.

📑 Table of Contents

✨ Features
🛠️ Tech Stack
🚀 Quick Start
⚙️ Setup Instructions
🗄️ Database Setup
📡 API Endpoints & Usage
🧠 Database Trigger
📁 Project Structure
🤝 Contributing
📜 License

✨ Features

🔐 Secure Member Check-ins: Automatically validates against active subscriptions.
📊 Automated Reporting: A database trigger keeps member check-in counts perfectly in sync.
🗂️ Clean Resource Management: Full CRUD operations for members, plans, and subscriptions.
🎯 Smart Business Logic: Automatic calculation of subscription end dates.
🏗️ Modern Architecture: Well-structured project using routers, Pydantic schemas, and ORM models.
📚 Auto-Generated Docs: Interactive API documentation available at /docs.

🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Framework** | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) |
| **Language** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white) |
| **ORM** | ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy) |

🚀 Quick Start
Prerequisites: Python 3.9+, PostgreSQL, and pip.

Clone the repository
git clone https://github.com/shrutigajbe/service-membership-api.git
cd service-membership-api

Set up and activate a virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Configure your database URL in app/database.py
DATABASE_URL = "postgresql+psycopg://your_user:your_password@localhost:5432/your_db"

Run the application
uvicorn app.main:app --reload

The API will be available at http://127.0.0.1:8000 and the docs at http://127.0.0.1:8000/docs.

⚙️ Setup Instructions
For a detailed breakdown, please refer to the Quick Start section above. The steps cover creating a virtual environment, installing dependencies, and configuring the database connection.

🗄️ Database Setup
The database schema is managed automatically by SQLAlchemy.

Table Creation: All required tables (members, plans, subscriptions, attendances) are created automatically on the first application run.

Trigger Application: The database trigger to increment total_check_ins is defined in app/triggers.sql. It is automatically applied to the database on application startup, ensuring it's always active without manual intervention.

📡 API Endpoints & Usage

Members
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/members/` | Create a new member. |
| `GET` | `/members/` | List all members (optional `?status=active` filter). |
| `GET` | `/members/{member_id}/current-subscription` | Get the current active subscription for a member. |
| `GET` | `/members/{member_id}/attendance` | Get the attendance history for a member. |

Example: Create a Member
curl -X POST "http://127.0.0.1:8000/members/" \
-H "Content-Type: application/json" \
-d '{
  "name": "Jane Doe",
  "phone": "9876543210"
}'

Plans
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/plans/` | Create a new subscription plan. |
| `GET` | `/plans/` | List all available plans. |

Example: Create a Plan
curl -X POST "http://127.0.0.1:8000/plans/" \
-H "Content-Type: application/json" \
-d '{
  "name": "Quarterly",
  "price": 12999,
  "duration_days": 90
}'

Subscriptions
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/subscriptions/` | Create a new subscription for a member. |

Example: Create a Subscription
curl -X POST "http://127.0.0.1:8000/subscriptions/" \
-H "Content-Type: application/json" \
-d '{
  "member_id": 1,
  "plan_id": 1,
  "start_date": "2023-11-01"
}'

Attendance
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/attendance/check-in` | Check in a member (validates active subscription). |
| `GET` | `/attendance/` | List all attendance records. |

Example: Member Check-in
curl -X POST "http://127.0.0.1:8000/attendance/check-in" \
-H "Content-Type: application/json" \
-d '{
  "member_id": 1
}'

🧠 Database Trigger
What it does: Automatically increments the total_check_ins column in the members table whenever a new record is inserted into the attendances table.
Where it's defined: app/triggers.sql.
How it's applied: The trigger SQL is executed automatically on application startup via the startup_event in app/main.py.

📁 Project Structure

service-membership-api/
├── 📂 app/                     # Main application package
│   ├── 🐍 __init__.py
│   ├── 🗄️ database.py          # Database session and engine configuration
│   ├── 🚀 main.py              # FastAPI app instance and startup events
│   ├── 📊 models.py            # SQLAlchemy ORM models (database tables)
│   ├── ✅ schemas.py           # Pydantic models for request/response validation
│   ├── 🔧 triggers.sql         # PostgreSQL trigger for automatic check-in counting
│   └── 📂 routers/             # API route handlers
│       ├── 🐍 __init__.py
│       ├── 📅 attendance.py    # Attendance tracking endpoints
│       ├── 👥 members.py       # Member management endpoints
│       ├── 📋 plans.py         # Subscription plan endpoints
│       └── 🔄 subscriptions.py # Subscription management endpoints
├── 🚫 .gitignore               # Files and folders to ignore in Git
├── 📦 requirements.txt         # Python dependencies
└── 📖 README.md               # This file

📁 File Descriptions

| File/Folder | Purpose |
|-------------|---------|
| **app/main.py** | Entry point of the application, configures FastAPI and includes routers |
| **app/database.py** | Database connection setup and session management |
| **app/models.py** | SQLAlchemy models defining the database schema |
| **app/schemas.py** | Pydantic models for data validation and serialization |
| **app/routers/** | Organized API endpoints by functionality |
| **app/triggers.sql** | Database trigger definition for automatic check-in counting |
| **requirements.txt** | List of Python dependencies for the project |
| **.gitignore** | Specifies files and directories that Git should ignore |



Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
