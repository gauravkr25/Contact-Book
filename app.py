from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import json, os, uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_super_secret_key'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USER') 
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASS')
mail = Mail(app)

# --- AUTH SETUP ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    users = load_db('users.json')
    user_data = next((u for u in users if u['id'] == user_id), None)
    if user_data:
        return User(user_data['id'], user_data['email'])
    return None

def load_db(file):
    if not os.path.exists(file): return []
    with open(file, 'r') as f: return json.load(f)

def save_db(file, data):
    with open(file, 'w') as f: json.dump(data, f, indent=4)

# --- ROUTES ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        users = load_db('users.json')
        if any(u['email'] == email for u in users):
            flash('Email already exists!')
            return redirect(url_for('register'))
        
        new_user = {'id': str(uuid.uuid4()), 'email': email, 'password': generate_password_hash(password)}
        users.append(new_user)
        save_db('users.json', users)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        users = load_db('users.json')
        user = next((u for u in users if u['email'] == email), None)
        
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['email'])
            login_user(user_obj)
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    contacts = load_db('contacts.json')
    # Show only contacts belonging to this user
    user_contacts = [c for c in contacts if c.get('owner') == current_user.id]
    return render_template('index.html', contacts=user_contacts)

@app.route('/send_email/<email_address>')
@login_required
def send_email(email_address):
    try:
        msg = Message("Hello from Contact Book",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email_address])
        msg.body = "This is a test email sent from your Python Contact Manager!"
        mail.send(msg)
        flash(f'Email sent to {email_address}!')
    except Exception as e:
        flash(f'Error: {str(e)}')
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
@login_required
def add_contact():
    contacts = load_db('contacts.json')
    contacts.append({
        'owner': current_user.id,
        'name': request.form.get('name'),
        'phone': request.form.get('phone'),
        'email': request.form.get('email'),
        'category': request.form.get('category')
    })
    save_db('contacts.json', contacts)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)