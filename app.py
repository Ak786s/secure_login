from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "f3b2c1a4d5e6f7g8h9i0j1k2l3m4n5o6"  # Strong key in real apps

# 🔐 Brute-force protection settings
MAX_ATTEMPTS = 3
LOCK_TIME_MINUTES = 15

# MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="secure_logins"
)
cursor = db.cursor(dictionary=True)

# Home route
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            flash("Email already registered!", "danger")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        db.commit()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# Login route with brute-force protection
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        # Generic invalid message
        invalid_msg = "Invalid email or password!"

        if not user:
            flash(invalid_msg, "danger")
            return redirect(url_for('login'))

        # Check if account is locked
        if user['lock_until'] and datetime.now() < user['lock_until']:
            flash(f"Account locked due to multiple failed attempts. Try again later.", "danger")
            return redirect(url_for('login'))

        # Password check
        if check_password_hash(user['password'], password):
            # Reset failed attempts on success
            cursor.execute(
                "UPDATE users SET failed_attempts=0, lock_until=NULL WHERE email=%s",
                (email,)
            )
            db.commit()
            session['username'] = user['username']
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            # Increase failed attempts
            failed_attempts = user['failed_attempts'] + 1

            if failed_attempts >= MAX_ATTEMPTS:
                lock_until = datetime.now() + timedelta(minutes=LOCK_TIME_MINUTES)
                cursor.execute(
                    "UPDATE users SET failed_attempts=%s, lock_until=%s WHERE email=%s",
                    (failed_attempts, lock_until, email)
                )
                flash(f"Your account is locked for {LOCK_TIME_MINUTES} minutes due to multiple failed attempts.", "danger")
            else:
                cursor.execute(
                    "UPDATE users SET failed_attempts=%s WHERE email=%s",
                    (failed_attempts, email)
                )
                flash(invalid_msg, "danger")  # Only generic message, no attempts shown

            db.commit()
            return redirect(url_for('login'))

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "danger")  # 🔴 Red alert for logout
    return redirect(url_for('login'))

# Favicon fix
@app.route('/favicon.ico')
def favicon():
    return "", 204

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)