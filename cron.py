import requests

status_endpoint_url = 'http://127.0.0.1:5000/status'  # Update the URL with your actual endpoint

response = requests.get(status_endpoint_url)

print('Response from status endpoint:', response.text)