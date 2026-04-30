from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'contacts.json'

def load_contacts():
    if not os.path.exists(DATA_FILE): return []
    with open(DATA_FILE, 'r') as f: return json.load(f)

def save_contacts(contacts):
    with open(DATA_FILE, 'w') as f: json.dump(contacts, f, indent=4)

@app.route('/')
def index():
    query = request.args.get('search', '').lower()
    all_contacts = load_contacts()
    
    # Advanced Feature: Search/Filter logic
    if query:
        contacts = [c for c in all_contacts if query in c['name'].lower() or query in c['phone']]
    else:
        contacts = all_contacts
        
    return render_template('index.html', contacts=contacts, query=query)

@app.route('/add', methods=['POST'])
def add_contact():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    category = request.form.get('category')
    
    if name and phone:
        contacts = load_contacts()
        contacts.append({
            'name': name,
            'phone': phone,
            'email': email,
            'category': category,
            'date_added': datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        save_contacts(contacts)
    return redirect(url_for('index'))

@app.route('/delete/<int:contact_id>')
def delete_contact(contact_id):
    contacts = load_contacts()
    if 0 <= contact_id < len(contacts):
        contacts.pop(contact_id)
        save_contacts(contacts)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)