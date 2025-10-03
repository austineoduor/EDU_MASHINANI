Management system for techncal courses and can be customized to fit all learning systems
To use the admin account please use details below:

The admin details are:
    username: austi
    password: austi123@#

The user details are:
    username: student1@gmail.com
    password: test123Aa

for a sample user use
register with your names, email and a password
login with your email and password
Welcome (:-


# EDU_MASHINANI

A Django-based learning management system (LMS) prototype where users can register, log in, manage profiles, and apply for available courses. The project includes course application tracking, profile management, and an admin interface for managing users and courses.

---

## 🚀 Features

### ✅ Current Functionality
- **User Authentication**
  - Register, login, and logout functionality
  - Profile auto-creation for every new user
- **Dashboard**
  - Displays all available courses
  - Shows description, components, and application status
  - Prevents multiple applications for the same course
- **Course Application**
  - Users can apply for courses only once
  - Application status tracked: `applied`, `in_progress`, `completed`
  - Location and "about" fields required during application
- **Profile Page**
  - Displays username, location (with Google Maps link), and about section
  - Shows list of courses with progress and scores
- **Admin**
  - Manage courses, users, and applications via Django admin

---

## 📌 Next Steps / Suggested Improvements
Here are ideas to enhance the system further:

### 🔒 Security / Authorization
- Restrict access so only authenticated users see dashboard/profile
- Add staff-only views to manage course applications

### 🎓 Course Features
- Add progress tracking (user updates % complete)
- Upload course materials (PDFs, videos, etc.)
- Add prerequisites (course A must be completed before course B)

### 📑 Profile Enhancements
- Profile picture upload
- Editable profile fields (location, about, middle name)
- Show "member since" date

### 📬 Notifications
- Email confirmation after application
- Dashboard notifications (future: real-time using Django Channels)

### 🖥 Dashboard UX
- Add search and filtering for courses
- Separate applied courses from available ones
- Collapsible course details with JS enhancements

### 📊 Admin & Analytics
- Add filters and search for UserCourse in Django Admin
- Export applicants to CSV/Excel
- Show number of applicants per course on dashboard

### 🌐 Extras
- Multi-language support (using Django’s i18n)
- REST API (with Django REST Framework)
- Charts for progress tracking (using Chart.js)

---

## ⚙️ Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd EDU_MASHINANI
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run migrations:

bash
Copy code
python manage.py migrate
Create a superuser for admin access:

bash
Copy code
python manage.py createsuperuser
Run the development server:

bash
Copy code
python manage.py runserver
Visit:

Dashboard: http://127.0.0.1:8000/dashboard/

Admin Panel: http://127.0.0.1:8000/admin/

🏗 Tech Stack
Backend: Django 4.x

Database: SQLite (default, can be swapped for PostgreSQL/MySQL)

Frontend: HTML, CSS, JS (custom)

Auth: Django’s built-in authentication system

📜 License
This project is for learning purposes. Modify and expand as needed.