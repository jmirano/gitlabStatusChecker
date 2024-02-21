To run locally
follow the following steps:
1. Install Docker if you haven't
2. go inside the BE folder and run the following command to build the image:
    docker build -t flask-app .       
3. Run the following command to start the app:
    docker run -d -p 8080:5000 flask-app


To download CSV reports simply run
go to URL or if in local http://localhost:8080/download-csv

To run perodically:
run the following commands (the example below is set to 10 minutes)
crontab -e
*/10 * * * * /path/to/python /path/to/cron_job.py
