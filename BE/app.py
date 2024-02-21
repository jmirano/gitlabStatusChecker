from datetime import datetime
import os
from flask import Flask, Response, make_response
from flask_sqlalchemy import SQLAlchemy
import requests
import schedule
import time
import json
import csv
from io import StringIO

app = Flask(__name__)

base_url = 'https://gitlab.example.com/api/v4'
base_dir = os.path.abspath(os.path.dirname(__file__))
gitlab_version = "16.9"
mock = True
scheduled_job_running = False

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(base_dir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Status Model
class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    health_status = db.Column(db.Text)
    readiness_status = db.Column(db.Text)
    version = db.Column(db.String(50))



# Fetch Status Task
@app.route('/status')
def fetch_and_save_gitlab_status():
    global scheduled_job_running
    scheduled_job_running = True
    print('Fetching and saving GitLab status...')
    try:
        if mock == True:
            print('Mocking GitLab status...')
            response_health = {'health_status': 'ok'}
            response_readiness = {'readines_status': 'ok'}
            
            status_entry = Status(health_status=json.dumps(response_health), readiness_status=json.dumps(response_readiness), version=gitlab_version)
            db.session.add(status_entry)
            db.session.commit()
        
        else:
            print('Fetching GitLab status...')
            # GitLab health check
            gitlab_health_url = f'{base_url}/health_check'
            response_health = requests.get(gitlab_health_url)

            # GitLab readiness check
            gitlab_readiness_url = f'{base_url}/readiness'
            response_readiness = requests.get(gitlab_readiness_url)

            status_entry = Status(health_status=json.dumps(response_health), readiness_status=json.dumps(response_readiness), version=gitlab_version)
            db.session.add(status_entry)
            db.session.commit()
        scheduled_job_running = False
        print('GitLab status check completed and saved to database at:', datetime.now())
        return 'GitLab status check completed'

    except Exception as e:
        scheduled_job_running = False
        print('Error occurred during GitLab status check:', e)
        return 'Error occurred during GitLab status check'


# download csv Endpoint
@app.route('/download-csv')
def download_csv():
    responses = Status.query.all()

    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerow(['Timestamp', 'Health_status', 'Readiness_status', 'Version'])

    for response in responses:
        csv_writer.writerow([response.timestamp, response.health_status, response.readiness_status, response.version])
        
    response = make_response(csv_data.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename=gitlab_status.csv'
    response.headers['Content-Type'] = 'text/csv'

    return response


@app.route('/')
def index():
    global scheduled_job_running
    if scheduled_job_running:
        return 'Scheduled job for gitlab status check is running.'
    else:
        return 'Gitlab status check is running.'
    
@app.cli.command("initdb")
def init_db():
    with app.app_context():
        db.create_all()
        print("Database tables created.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)