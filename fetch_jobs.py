import os
import requests
from dotenv import load_dotenv

# Load variables from .env into this script's environment
load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

# Adzuna's endpoint for UK job search, page 1
url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "results_per_page": 10,
    "what": "graduate software engineer",
    "content-type": "application/json"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    jobs = data["results"]
    print(f"Found {len(jobs)} jobs:\n")
    for job in jobs:
        print(job["title"], "-", job["company"]["display_name"])
        print(job["location"]["display_name"])
        print(job["redirect_url"])
        print("---")
else:
    print(f"Error {response.status_code}: {response.text}")