from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from datetime import datetime
import json
import sys
import io
import time
from azure.storage.blob import BlobServiceClient
import mimetypes
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Azure Blob Storage configuration
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
BLOB_CONTAINER_NAME = "case-notes"

# Azure Function configuration
FUNCTION_HTTP_OPENAI_URL = os.getenv("FUNCTION_HTTP_OPENAI_URL")
SYSTEM_ROLE_TASKBREAKDOWN = os.getenv("SYSTEM_ROLE_TASKBREAKDOWN")

# Initialize Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

# Add the parent directory to sys.path to import from chat package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chat.chat import create_chat_completion

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

@app.route('/upload_note', methods=['POST'])
@login_required
def upload_note():
    try:
        file = request.files.get('file')
        category = request.form.get('category')
        consumer_id = request.form.get('consumer_id', 'c001')  # Default to 'c001' if not provided
        
        if not file:
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        # Generate unique note_id
        note_id = f"note_{int(time.time())}"
        blob_path = f"arriving-files/{note_id}_{file.filename}"
        blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=blob_path)
        
        # Upload file to Azure Blob Storage
        blob_client.upload_blob(file, overwrite=True)

        # Add note to the notes list
        new_note = {
            'id': f"n{str(len(notes) + 1).zfill(3)}",
            'consumer_id': consumer_id,
            'coach_id': current_user.id,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'content': f"Uploaded file: {file.filename}",
            'category': category,
            'filename': file.filename
        }
        notes.append(new_note)

        return jsonify({
            'success': True,
            'note_id': note_id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/check_reports/<note_id>', methods=['GET'])
@login_required
def check_reports(note_id):
    try:
        container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)
        processed_prefix = "processed/"
        blobs = list(container_client.list_blobs(name_starts_with=processed_prefix))
        
        print(f"Blobs in processed folder: {[blob.name for blob in blobs]}")
        
        # Look for any files ending with _government_report.pdf and _employer_report.pdf
        gov_blob = next((b for b in blobs if b.name.endswith('_government_report.pdf')), None)
        emp_blob = next((b for b in blobs if b.name.endswith('_employer_report.pdf')), None)

        print(f"Found gov_blob: {gov_blob.name if gov_blob else 'None'}")
        print(f"Found emp_blob: {emp_blob.name if emp_blob else 'None'}")

        if gov_blob and emp_blob:
            processed_files = [
                {
                    'name': gov_blob.name.split('/')[-1],
                    'url': f"/download_processed/{gov_blob.name.split('/')[-1]}"
                },
                {
                    'name': emp_blob.name.split('/')[-1],
                    'url': f"/download_processed/{emp_blob.name.split('/')[-1]}"
                }
            ]
            print(f"Reports found: {processed_files}")
            return jsonify({
                'reports_ready': True,
                'processed_files': processed_files
            })
        else:
            print("Reports not ready yet")
            return jsonify({'reports_ready': False})
    except Exception as e:
        print(f"Error in check_reports: {str(e)}")
        return jsonify({'reports_ready': False, 'error': str(e)}), 500

@app.route('/download_processed/<filename>')
@login_required
def download_processed(filename):
    try:
        blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=f"processed/{filename}")
        blob_data = blob_client.download_blob().readall()
        mime_type, _ = mimetypes.guess_type(filename)
        return send_file(
            io.BytesIO(blob_data),
            mimetype=mime_type,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        flash(f"Error downloading file: {str(e)}")
        return redirect(url_for('index'))
            
@app.route('/ai/task-breakdown', methods=['POST'])
@login_required
def ai_task_breakdown():
    try:
        data = request.json
        task_name = data.get('task_name')
        task_details = data.get('task_details')
        accommodations = data.get('accommodations', {})
        consumer_id = data.get('consumer_id', 'c001')  # Default to 'c001' if not provided

        if not task_name or not task_details:
            return jsonify({'error': 'Task name and details are required'}), 400

        # Get consumer info from models
        consumer = consumers.get(consumer_id, {})
        disability_type = consumer.get('disability', '')
        employee_info = f"Name: {consumer.get('name', 'Unknown')}, Job Interests: {', '.join(consumer.get('job_interests', []))}"

        # Construct the user prompt
        user_prompt = f"Task to complete: {task_name}\nTask details: {task_details}\n"
        if disability_type:
            user_prompt += f"Employee has disability: {disability_type}\n"
        user_prompt += f"Employee Info: {employee_info}"
        if accommodations.get('needsVisual'):
            user_prompt += "\nInclude visual aid accommodations"
        if accommodations.get('needsSimplified'):
            user_prompt += "\nInclude simplified instructions"

        # Prepare payload for Azure Function
        payload = {
            "system_role": SYSTEM_ROLE_TASKBREAKDOWN,
            "user_prompt": user_prompt
        }

        # Call Azure Function
        response = requests.post(FUNCTION_HTTP_OPENAI_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            message = result.get('message', '')

            # Parse the response (assuming it’s a string with steps and accommodations)
            steps = []
            accommodations_list = []
            current_list = steps
            for line in message.split('\n'):
                line = line.strip()
                if line.startswith('Steps:') or line.startswith('Step-by-Step Instructions:'):
                    current_list = steps
                elif line.startswith('Accommodations:') or line.startswith('Suggested Accommodations:'):
                    current_list = accommodations_list
                elif line and line[0].isdigit():
                    current_list.append(line)
                elif line.startswith('- ') or line.startswith('* '):
                    current_list.append(line[2:])

            return jsonify({
                'steps': steps,
                'accommodations': accommodations_list
            })
        else:
            return jsonify({'error': f"Failed to generate breakdown: {response.text}"}), 500

    except Exception as e:
        print(f"Error in task breakdown: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Add this new route for the AI chat functionality
@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    try:
        data = request.json
        user_content = data.get('user_content')
        
        if not user_content:
            return jsonify({
                'error': 'No content provided',
                'response': 'Please provide a question or message.'
            }), 400
        
        # For debugging, let's log the request
        print(f"Chat request received: {user_content}")
        
        # Add a user_context parameter to request simple HTML formatting
        user_context = {
            "response_format": "simple_html"
        }
        
        # Get the response from the OpenAI API with the formatting context
        response = create_chat_completion(
            user_content=user_content,
            user_context=user_context
        )
        
        # Extract the assistant's message
        if response and hasattr(response, 'choices') and len(response.choices) > 0:
            ai_response = response.choices[0].message.content
        else:
            ai_response = "Sorry, I couldn't process your request. Please try again."
        
        # For debugging, let's log the response
        print(f"Chat response sent: {ai_response[:100]}...")
        
        return jsonify({
            'response': ai_response
        })
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': str(e),
            'response': "Sorry, an error occurred while processing your request."
        }), 500

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