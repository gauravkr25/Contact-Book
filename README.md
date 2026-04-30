# 📇 Contact Manager Pro (2026 Edition)

A professional, full-stack Contact Management System built with **Python (Flask)**. It features secure user authentication, automatic Gmail notifications, and a modern dashboard UI using Tailwind CSS.

---

## ✨ Features

- **🔐 User Authentication**: Secure Register/Login system with password hashing.
- **📱 Modern UI**: Fully responsive dashboard built with Tailwind CSS.
- **📧 Auto-Email Notifications**: Sends a welcome email to new contacts using Gmail SMTP.
- **🔍 Live Search**: Quickly filter through your contacts by name or phone number.
- **📂 Data Persistence**: Uses JSON file handling for lightweight data storage.
- **🛡️ Privacy**: Each user only sees and manages their own private contact list.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, Tailwind CSS
- **Database**: JSON (File-based)
- **Libraries**: Flask-Login, Flask-Mail, python-dotenv

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed on your system.

### 2. Installation
Install all the required Python libraries:
`pip install flask flask-login flask-mail python-dotenv`

### 3. Gmail Configuration
To enable the email feature, you need a **Google App Password**:
1. Go to your Google Account Security settings.
2. Enable 2-Step Verification.
3. Search for "App Passwords" and create one.
4. Copy the 16-character code provided.

### 4. Setup Environment Variables
Create a file named `.env` in the root directory and add:
`MAIL_USER=your_email@gmail.com`
`MAIL_PASS=your_16_character_app_password`

### 5. Run the Application
Start the Flask server:
`python app.py`

### 6. Access the App
Open your web browser and navigate to:
- **Register**: http://127.0.0.1:5000/register
- **Login**: http://127.0.0.1:5000/login

---

## 📂 Project Structure
- `app.py`: Main Application Logic
- `.env`: Private Credentials
- `contacts.json`: Contact Database
- `users.json`: User Credentials Database
- `templates/`: Folder containing HTML files (index, login, register)

---

## 🛡️ Security Note
This project uses `.gitignore` to ensure your `.env` (passwords) and local JSON databases are not uploaded to public platforms like GitHub.# Contact-Book