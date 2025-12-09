# Workshop Management System (WMS) Backend

Production-ready backend for WMS using Python + Django.

## Tech Stack
- **Python**: 3.14.0
- **Framework**: Django 6.0 + Django REST Framework
- **Database**: SQLite (Configurable to PostgreSQL)
- **Auth**: Token Authentication (JWT/Session ready)
- **Other Libs**: ReportLab (PDF), Pillow (Image), QRCode

## Project Setup

### 1. Prerequisites
- Python 3.10+ installed.

### 2. Environment Setup
```bash
# Clone repository
cd wms

# Install Dependencies
pip install -r ../requirements.txt
```

### 3. Database Migration
```bash
python manage.py makemigrations accounts workshops attendance certificates dashboard
python manage.py migrate
```

### 4. Create Admin User
Auto-create the default admin (`nitindaswani771@gmail.com` / `nitin1234`):
```bash
python manage.py ensure_admin
```

### 5. Run Server
```bash
python manage.py runserver
```

## API Documentation

### Authentication
- **Login**: `POST /api/auth/login/` (`username`(email), `password`) -> Returns `token`
- **Signup**: `POST /api/auth/signup/` (`email`, `password`, `full_name`, `role`=[student, speaker])
- **User Profile**: `GET /api/auth/user/`

### Workshops
- **List/Create**: `GET/POST /api/workshops/`
- **Detail**: `GET/PUT/DELETE /api/workshops/<id>/`
- **Sessions**: `GET/POST /api/workshops/<id>/sessions/`
- **Register**: `POST /api/workshops/<id>/register/<type>/` (`type` = student/speaker)

### Attendance
- **My Registrations**: `GET /api/user/registrations/`
- **Generate QR**: `GET /api/attendance/qr/<registration_id>/`
- **Mark Attendance**: `POST /api/attendance/mark/` (Body: `qr_content`)
- **My Attendance**: `GET /api/attendance/user/`

### Certificates
- **Generate**: `POST /api/certificates/generate/<registration_id>/`
- **List**: `GET /api/certificates/user/`

### Dashboard
- **Global**: `GET /api/dashboard/global/`
- **Workshop**: `GET /api/dashboard/workshop/<id>/`

## Admin Panel
Access at `/admin/`. Login with admin credentials.
Features:
- Manage Users (Speakers, Students)
- Manage Workshops & Sessions
- View Registrations & Attendance
- Generate/View Certificates
