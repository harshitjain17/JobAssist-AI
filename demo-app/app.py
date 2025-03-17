from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hackathon-demo-secret-key'
app.config['STATIC_FOLDER'] = 'static'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Placeholder for database - in a real app, this would be a database
# For demo purposes, we'll use simple dictionaries
from models import users, consumers, appointments, notes

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/')
@login_required
def index():
    # print(consumers)
    # print(current_user.id)
    return render_template('dashboard.html', 
                          user=current_user,
                          consumers=consumers,
                          appointments=appointments,
                          notes=notes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple demo authentication
        if username in users and users[username]['password'] == password:
            user_obj = users[username]
            user_obj['id'] = username  # Use username as ID
            login_user(UserObject(user_obj))
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/consumer/<consumer_id>')
@login_required
def consumer_detail(consumer_id):
    if consumer_id in consumers:
        consumer = consumers[consumer_id]
        consumer_notes = [note for note in notes if note['consumer_id'] == consumer_id]
        consumer_appointments = [appt for appt in appointments if appt['consumer_id'] == consumer_id]
        return render_template('consumer_detail.html', 
                              consumer=consumer,
                              notes=consumer_notes,
                              appointments=consumer_appointments)
    return redirect(url_for('index'))

# Add to demo-app/app.py after the existing routes
@app.route('/ai/job-match', methods=['POST'])
@login_required
def ai_job_match():
    consumer_id = request.json.get('consumer_id')
    # In a real implementation, this would call Azure OpenAI
    # For demo purposes, return mock data
    return jsonify({
        'matches': [
            {
                'title': 'Data Entry Specialist',
                'company': 'Acme Corporation',
                'match_score': 95,
                'location': 'Remote',
                'description': 'Remote position with flexible hours perfect for someone with mobility challenges.',
                'tags': ['Remote', 'Full-time', 'Entry Level']
            },
            {
                'title': 'Customer Support Representative',
                'company': 'TechServe Inc.',
                'match_score': 87,
                'location': 'Remote',
                'description': 'Work-from-home position answering customer inquiries via email and chat.',
                'tags': ['Remote', 'Part-time', 'Customer Service']
            }
        ]
    })

@app.route('/ai/task-breakdown', methods=['POST'])
@login_required
def ai_task_breakdown():
    # In a real implementation, this would call Azure OpenAI
    # Mimicking the functionality in streamlit-app/pages/2_task_breakdown.py
    return jsonify({
        'steps': [
            '1. Open the pizza box flat on a clean surface',
            '2. Identify the fold lines on the box',
            '3. Fold the side panels inward along the fold lines',
            '4. Fold the bottom panel up',
            '5. Fold the top panel down and tuck the tab into the slot'
        ],
        'accommodations': [
            'Use visual markers on fold lines for better visibility',
            'Place a weighted object to hold the box while folding',
            'Consider using a folding jig for consistency'
        ]
    })
# User class for Flask-Login
class UserObject:
    def __init__(self, user_dict):
        self.id = user_dict['id']
        self.name = user_dict['name']
        self.role = user_dict['role']
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        user_dict = users[user_id]
        user_dict['id'] = user_id
        return UserObject(user_dict)
    return None

if __name__ == '__main__':
    app.run(debug=True)