from datetime import datetime, timedelta

# Sample users (job coaches)
users = {
    'coach1': {
        'name': 'Tiffany Williams',
        'password': 'demo1234',
        'role': 'Job Placement Specialist',
        'email': 'tiffany.williams@ky.gov',
        'phone': '555-123-4567'
    },
    'coach2': {
        'name': 'Michael Rodriguez',
        'password': 'demo1234',
        'role': 'Senior Job Coach',
        'email': 'michael.r@example.org',
        'phone': '555-987-6543'
    }
}

# Sample consumers (disabled persons seeking employment)
consumers = {
    'c001': {
        'id': 'c001',
        'name': 'James Wilson',
        'age': 28,
        'disability': 'Physical - Mobility',
        'skills': ['Data entry', 'Customer service', 'MS Office'],
        'job_interests': ['Admin assistant', 'Remote customer support'],
        'status': 'Active',
        'coach_id': 'coach1',
        'email': 'james.w@example.com',
        'phone': '555-111-2222',
        'address': '123 Main St, Portland, OR',
        'emergency_contact': {
            'name': 'Mary Wilson',
            'relation': 'Mother',
            'phone': '555-333-4444'
        }
    },
    'c002': {
        'id': 'c002',
        'name': 'Emily Chen',
        'age': 32,
        'disability': 'Hearing impairment',
        'skills': ['Graphic design', 'Web development', 'ASL fluent'],
        'job_interests': ['Design', 'Web development'],
        'status': 'Active',
        'coach_id': 'coach1',
        'email': 'emily.c@example.com',
        'phone': '555-555-6666',
        'address': '456 Oak Ave, Portland, OR',
        'emergency_contact': {
            'name': 'David Chen',
            'relation': 'Brother',
            'phone': '555-777-8888'
        }
    },
    'c003': {
        'id': 'c003',
        'name': 'Robert Taylor',
        'age': 25,
        'disability': 'Learning disability',
        'skills': ['Organization', 'Warehousing', 'Inventory management'],
        'job_interests': ['Warehouse associate', 'Stock clerk'],
        'status': 'Job placement',
        'coach_id': 'coach2',
        'email': 'robert.t@example.com',
        'phone': '555-999-0000',
        'address': '789 Pine St, Portland, OR',
        'emergency_contact': {
            'name': 'Susan Taylor',
            'relation': 'Sister',
            'phone': '555-222-3333'
        }
    }
}

# Sample appointments
now = datetime.now()
appointments = [
    {
        'id': 'a001',
        'consumer_id': 'c001',
        'coach_id': 'coach1',
        'title': 'Resume Review',
        'date': (now + timedelta(days=1)).strftime('%Y-%m-%d'),
        'time': '10:00 AM',
        'status': 'Scheduled',
        'location': 'Office'
    },
    {
        'id': 'a002',
        'consumer_id': 'c001',
        'coach_id': 'coach1',
        'title': 'Mock Interview',
        'date': (now + timedelta(days=3)).strftime('%Y-%m-%d'),
        'time': '2:00 PM',
        'status': 'Scheduled',
        'location': 'Virtual'
    },
    {
        'id': 'a003',
        'consumer_id': 'c002',
        'coach_id': 'coach1',
        'title': 'Job Search Strategy',
        'date': (now + timedelta(days=2)).strftime('%Y-%m-%d'),
        'time': '11:30 AM',
        'status': 'Scheduled',
        'location': 'Office'
    },
    {
        'id': 'a004',
        'consumer_id': 'c003',
        'coach_id': 'coach2',
        'title': 'Employer Interview',
        'date': (now + timedelta(days=5)).strftime('%Y-%m-%d'),
        'time': '1:00 PM',
        'status': 'Scheduled',
        'location': 'Employer Site'
    }
]

# Sample case notes
notes = [
    {
        'id': 'n001',
        'consumer_id': 'c001',
        'coach_id': 'coach1',
        'date': (now - timedelta(days=7)).strftime('%Y-%m-%d'),
        'content': 'James is making good progress on his resume. We identified several strengths to highlight including his attention to detail and data entry skills.',
        'category': 'Progress'
    },
    {
        'id': 'n002',
        'consumer_id': 'c001',
        'coach_id': 'coach1',
        'date': (now - timedelta(days=3)).strftime('%Y-%m-%d'),
        'content': 'Reached out to Acme Corp about potential data entry positions. They have an opening that would accommodate James\'s mobility needs with remote work options.',
        'category': 'Job Lead'
    },
    {
        'id': 'n003',
        'consumer_id': 'c002',
        'coach_id': 'coach1',
        'date': (now - timedelta(days=5)).strftime('%Y-%m-%d'),
        'content': 'Emily shared her updated portfolio. Her design skills are impressive. We discussed focusing on companies with inclusive hiring practices in the creative field.',
        'category': 'Progress'
    },
    {
        'id': 'n004',
        'consumer_id': 'c003',
        'coach_id': 'coach2',
        'date': (now - timedelta(days=1)).strftime('%Y-%m-%d'),
        'content': 'Great news! Metro Warehouse has offered Robert a part-time position. They were impressed with his organization skills and are willing to provide accommodations for his learning disability.',
        'category': 'Job Offer'
    }
]