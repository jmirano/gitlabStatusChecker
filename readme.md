To run go to be folder and run the following command:
python -m flask run

To download CSV reports simply run
go to URL or if in local http://127.0.0.1:5000/download-csv

Turn Off Mock:
for local testing the app is configured to mock responses can turn off by setting mock to false

update any URLs needed in app.py

Should there any issues with the database:
Run the following

flask shell

once flask shell is open

from app import db, Status
db.create_all()

To run perodically:
run the following commands (the example below is set to 10 minutes)
crontab -e
*/10 * * * * /path/to/python /path/to/cron_job.py
