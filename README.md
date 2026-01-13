# 🔐 Secure Login System (Flask + MySQL)

A secure authentication system built using **Flask** and **MySQL**, implementing essential security controls such as **password hashing**, **brute-force attack protection**, and **account lockout mechanisms**.

---

## 🚀 Features

* User Registration & Login
* Secure password hashing (Werkzeug)
* Brute-force attack protection
* Temporary account lock after failed attempts
* Session-based authentication
* Flash messaging for user feedback
* Clean and simple database schema

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Database:** MySQL
* **Security:** Werkzeug password hashing
* **Frontend:** HTML,CSS

---

## 📌 Database Information

* **Database Name:** `secure_logins`
* **Table Name:** `users`

---

## 🗄️ Database Schema

```sql
-- =============================================
-- Secure Login System Database Schema
-- Database: secure_logins
-- =============================================

CREATE DATABASE IF NOT EXISTS secure_logins;
USE secure_logins;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, -- hashed password only
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    failed_attempts INT DEFAULT 0,
    lock_until DATETIME DEFAULT NULL
);
```

---

## 🔐 Security Logic Implemented

### Password Security

* Passwords are hashed using `generate_password_hash()`
* Password verification uses `check_password_hash()`
* Plaintext passwords are never stored

### Brute-force Protection

* Maximum login attempts: **3**
* Account lock duration: **15 minutes**
* Failed attempts tracked per user

### Account Lock Logic

* Account is temporarily locked after consecutive failures
* Login blocked until `lock_until` expires

---

## 📂 Project Structure

```bash
secure_login/
│
├── app.py
├── templates/
│   ├── login.html
│   ├── register.html
│   └── home.html
├── static/
│   └── styles.css
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Ak786s/secure_login.git
cd secure_login
```

### 2️⃣ Install Dependencies

```bash
pip install flask mysql-connector-python werkzeug
```

### 3️⃣ Configure Database

Update database credentials in `app.py`:

```python
db = mysql.connector.connect(
    host="hostname",
    user="username",
    password="password",
    database="secure_logins"
)
```

### 4️⃣ Run Application

```bash
python app.py
```

Access the app at:

```
http://127.0.0.1:5000/
```

---

## 🧪 Sample SQL Queries Used in Application

```sql
-- Fetch user for login
SELECT * FROM users WHERE email = ?;

-- Insert new user
INSERT INTO users (username, email, password) VALUES (?, ?, ?);

-- Update failed attempts
UPDATE users SET failed_attempts = failed_attempts + 1 WHERE email = ?;

-- Lock user account
UPDATE users SET lock_until = ? WHERE email = ?;

-- Reset attempts after successful login
UPDATE users SET failed_attempts = 0, lock_until = NULL WHERE email = ?;
```

---

## ⚠️ Security Notes

* Always use **prepared statements** (implemented)
* Do not hardcode secret keys in production
* Disable `debug=True` in production
* Use HTTPS in real deployments

---

## 🌱 Future Enhancements

* Role-based access control (RBAC)
* Password reset via email
* Login audit logs
* CAPTCHA integration
* Multi-Factor Authentication (MFA)

---

## 👨‍💻 Author

**Amir Mulla**
Cybersecurity Enthusiast

---

