from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import json, os, uuid, datetime

load_dotenv()

app = Flask(__name__)

app.secret_key = 'dev_key_2026_contact_manager_99'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASS')
mail = Mail(app)

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
    if user_data: return User(user_data['id'], user_data['email'])
    return None

def load_db(file):
    if not os.path.exists(file): 
        with open(file, 'w') as f: json.dump([], f)
        return []
    with open(file, 'r') as f: return json.load(f)

def save_db(file, data):
    with open(file, 'w') as f: json.dump(data, f, indent=4)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email, password = request.form.get('email'), request.form.get('password')
        users = load_db('users.json')
        if any(u['email'] == email for u in users):
            flash('Email already registered!')
            return redirect(url_for('register'))
        users.append({'id': str(uuid.uuid4()), 'email': email, 'password': generate_password_hash(password)})
        save_db('users.json', users)
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email, password = request.form.get('email'), request.form.get('password')
        users = load_db('users.json')
        user = next((u for u in users if u['email'] == email), None)
        if user and check_password_hash(user['password'], password):
            login_user(User(user['id'], user['email']))
            return redirect(url_for('index'))
        flash('Invalid email or password.')
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    query = request.args.get('search', '').lower()
    all_contacts = load_db('contacts.json')
    contacts = [c for c in all_contacts if c.get('owner') == current_user.id]
    if query:
        contacts = [c for c in contacts if query in c['name'].lower() or query in c['phone']]
    return render_template('index.html', contacts=contacts, query=query)

@app.route('/add', methods=['POST'])
@login_required
def add_contact():
    name, phone, email, cat = request.form.get('name'), request.form.get('phone'), request.form.get('email'), request.form.get('category')
    contacts = load_db('contacts.json')
    new_contact = {
        'id': str(uuid.uuid4()),
        'owner': current_user.id,
        'name': name, 'phone': phone, 'email': email, 'category': cat,
        'date_added': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    contacts.append(new_contact)
    save_db('contacts.json', contacts)
    
    if email:
        try:
            msg = Message("Contact Saved!", sender=app.config['MAIL_USERNAME'], recipients=[email])
            msg.body = f"Hi {name}, you have been added to {current_user.email}'s Contact Book."
            mail.send(msg)
            flash('Contact added and Email sent!')
        except: flash('Contact added, but Email failed.')
    return redirect(url_for('index'))

@app.route('/delete/<string:contact_id>')
@login_required
def delete_contact(contact_id):
    contacts = load_db('contacts.json')
    contacts = [c for c in contacts if not (c.get('id') == contact_id and c.get('owner') == current_user.id)]
    save_db('contacts.json', contacts)
    flash('Contact deleted.')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)