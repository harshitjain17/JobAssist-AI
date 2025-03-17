# JobAssistAI Demo Application

## Overview

A Flask-based web application for job coaches to manage supported employment programs. This demo provides case management tools, AI-powered job matching, and task breakdown assistance for supporting clients with disabilities in their employment journey.

## Features

- **Case Management Dashboard**: View and manage client information, appointments, and case notes
- **AI Job Matching**: Get intelligent job recommendations based on client profiles
- **Task Breakdown Analysis**: AI-powered analysis of job tasks with accommodation suggestions
- **Secure Authentication**: Role-based access control for job coaches
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5

## Directory Structure
```
demo-app/
├── app.py              # Flask application main file
├── models.py           # Data models and mock database
├── static/
│   ├── css/
│   │   └── style.css  # Custom styling
│   └── js/
│       └── script.js  # Client-side functionality
├── templates/
│   ├── base.html      # Base template
│   ├── dashboard.html # Main dashboard view
│   ├── login.html    # Authentication page
│   └── consumer_detail.html # Client profile view
└── requirements.txt   # Python dependencies
```

## Prerequisites

- Python 3.12+
- Flask and its dependencies
- Modern web browser (Chrome, Firefox, Safari, or Edge)

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Access the application at `http://localhost:5000`

## Usage

1. Log in using demo credentials (see login page)
2. Navigate the dashboard to view clients and appointments
3. Access client profiles for detailed information
4. Use AI features for job matching and task analysis

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: Bootstrap 5, JavaScript
- **Icons**: Font Awesome 6
- **AI Integration**: Prepared for Azure OpenAI integration (mock data in demo)

## Development

The application uses Flask's development server with debug mode enabled. Key files:

- `app.py`: Route definitions and application logic
- `models.py`: Mock data structures
- `static/js/script.js`: Client-side interactivity
- `templates/*.html`: Jinja2 templates for views