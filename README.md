# AttendanceTrack

AttendanceTrack is a Django-based personnel attendance management system. It allows companies to monitor daily check-in/out times, manage employee leave requests, and generate monthly work hour reports.

## 🚀 Features

- Separate login pages for employees and admins
- Tracks daily check-in and check-out times
- Automatically deducts leave time for late arrivals
- Employees can request time off
- Admin can approve or reject leave requests
- Alerts when an employee’s annual leave drops below 3 days
- Monthly work hours reporting
- Admin dashboard to view all employees and their activities

## 🛠️ Technologies Used

- Python 3.x
- Django
- PostgreSQL
- HTML / CSS
- Django Template Engine

## ⚙️ Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/umitkisi/AttendanceTrack.git
   cd AttendanceTrack
   ```

2. Create a virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install required packages:

   ```bash
   pip install django
   pip install djangorestframework
   pip install psycopg2-binary

   ```

4. Apply migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create an admin user:

   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

7. Open in browser:

   ```
   http://127.0.0.1:8000/
   ```


## 📌 Notes

- UI is kept intentionally simple and functional
- Docker and Celery/WebSocket support can be added for production usage

---

## 👨‍💻 Developer

This project was developed by **Ümit Şahan**.  
🔗 GitHub: [github.com/umitkisi](https://github.com/umit-sahan)

---
