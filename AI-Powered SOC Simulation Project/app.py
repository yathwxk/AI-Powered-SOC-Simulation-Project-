import json
from flask import Flask, request, render_template
from datetime import datetime
import os

app = Flask(__name__)

# Function to load users from the JSON file
def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    else:
        return {}

# Function to save users to the JSON file (used for future updates if needed)
def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

# Make sure logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Function to log login attempts
def log_login_attempt(username, ip, status, user_agent):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/login_attempts.log", "a") as log_file:
        log_file.write(f"[{timestamp}] LOGIN user={username} ip={ip} status={status} agent=\"{user_agent}\"\n")

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    # Load users from JSON file
    users = load_users()

    # Log the attempt
    log_login_attempt(username, ip, "FAILURE", user_agent)  # Log even invalid users

    # Check if the username exists and password matches
    if username in users and users[username] == password:
        log_login_attempt(username, ip, "SUCCESS", user_agent)
        return f"<h2>Welcome, {username}!</h2><p><a href='/'>Logout</a></p>"
    else:
        return f"<h2>Login Failed</h2><p><a href='/'>Try again</a></p>"

if __name__ == "__main__":
    app.run(debug=True)
