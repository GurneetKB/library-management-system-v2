# 📚 The Library – Library Management System (V2)

A full-stack **Library Management System** with role-based access, automated background tasks, and structured database design. Built to manage books, users, borrowing workflows, and administrative operations efficiently.


---


## 🚀 Key Features

### 👤 User

* Register / Login
* Browse books by section
* Request & return books
* View borrowing history
* Rate & review books

### 🛠 Admin

* Manage sections & books
* Approve / reject requests
* Monitor users & transactions
* Export system data (CSV)


---


## ⚙️ Background Automation (Celery)

* 📩 Weekly inactivity reminders
* 📊 Monthly reading reports via email
* 📄 Automated CSV export for librarian


---


## 🗂 Core Models

* **User** (role-based access)
* **Book**
* **Section**
* **Register** (borrowing records)
* **Feedback**

Includes **soft delete**, borrowing status tracking (Pending / Approved / Rejected / Returned), and audit metadata.


---


## 🧠 Tech Stack

* **Flask**
* **SQLAlchemy**
* **SQLite**
* **Celery + Celery Beat**
* **Email Integration**


---


## ▶️ Run Locally

```bash
git clone https://github.com/GurneetKB/library-management-system-v2.git
cd library-management-system-v2

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
python run.py
```

Run Celery:

```bash
celery -A app.celery worker --loglevel=info
celery -A app.celery beat --loglevel=info
```


---


## 👩‍💻 Author

**Gurneet Kaur Bhuller**
IIT Madras – BS in Data Science


---
