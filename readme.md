App Description:
The Following Application runs an api which can be used to get gitlab health status
As part of testing the following uses a mock response and needs to reconfigured to actual calls to the gitlab instance

To disable Mock
In App.py update the mock variable to false and ensure base URL is pointing to the corresponding gitlab instance

To run the health check manually
go the the url or if in local access as follows: http://localhost:8080/status


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
