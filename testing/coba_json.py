import json
import requests

response = requests.get('https://trinanda.github.io/json/gmail_api_clien_secret.json')

json_data = json.loads(response.text)

print(json_data)